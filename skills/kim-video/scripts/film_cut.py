#!/usr/bin/env python3
"""
Schneidet einen Film aus den erzeugten Teilen -- auf dem Rechner des Nutzers.

Warum hier und nicht auf dem Server
-----------------------------------
Der Schnitt lief bis 11.2026 auf dem KIMASTERMIND-Server. Das Erzeugen von Bild
und Ton muss dort laufen, der Schnitt nicht: er ist reine Rechenarbeit auf
Dateien, die der Nutzer ohnehin bekommt. Ein Film von zwei Minuten bedeutet ein
Dutzend H.264-Durchlaeufe, und der Server bedient waehrenddessen alle anderen
Nutzer schlechter. Also laedt der Nutzer die Teile herunter und schneidet
lokal. Das ist zugleich schneller, weil nichts mehr hoch- und wieder
runtergeladen wird.

Warum nichts ruckelt
--------------------
Eine Szene ist fast immer laenger als ihr Clip: der Sprecher braucht zehn
Sekunden, das Modell liefert fuenf. Dafuer gibt es drei Wege, und zwei davon
sehen schlecht aus.

  * Das letzte Bild einfrieren (tpad=stop_mode=clone). Bis 11.2026 der Weg
    hier. Das Bild steht still, waehrend weitergesprochen wird -- es sieht aus
    wie ein Standbild mit Tonspur, und genau das ist es dann auch.
  * Mit dem framerate-Filter oder fps= auf eine andere Bildrate bringen. Der
    Filter verdoppelt oder ueberblendet einzelne Bilder. Bei 24 auf 30 ist
    jedes fuenfte Bild doppelt, und das sieht man als Stottern.
  * Zeitlich strecken UND die fehlenden Bilder berechnen: setpts verlangsamt,
    minterpolate (mi_mode=mci) rechnet aus zwei Bildern die Bewegung dazwischen
    aus. Das ist der Weg hier.

Dasselbe gilt fuer Kamerafahrten auf Standbildern. ffmpeg-crop und zoompan
rechnen in ganzen Pixeln, also springt die Fahrt sichtbar. Hier wird Bild fuer
Bild mit einem Subpixel-Ausschnitt gerechnet (PIL, AFFINE), und das Bild wird
vorher mit Lanczos so weit verkleinert, dass nie stark heruntergerechnet werden
muss -- sonst flimmern feine Strukturen.

Der Preis dafuer ist Rechenzeit: eine Clip-Szene braucht etwa eine bis zwei
Minuten, eine Standbild-Szene je nach Laenge aehnlich lang. Ein Film mit zehn
Szenen laeuft also zehn bis zwanzig Minuten. **Immer im Hintergrund starten.**

Die wichtigste Regel steht nicht in diesem Skript, sondern im Storyboard: die
Clips so lang bestellen, wie die Szene wird. Mehr als etwa x1,5 gestreckt sieht
auch interpoliert nach Zeitlupe aus. Dann die Szene teilen oder ein Standbild
mit Kamerafahrt nehmen.

Was es sonst macht
------------------
Drei Durchlaeufe, bewusst nicht ein einziger Filtergraph: ein Graph fuer ein
Dutzend Szenen ist unlesbar und scheitert als Ganzes.

  1. Je Szene eine Datei mit identischen Parametern (Groesse, Bildrate, Codec),
     damit Durchlauf 2 kopieren kann.
  2. Zusammenfuegen ohne neu zu codieren (concat demuxer, Stream-Copy).
  3. Musik, eingebrannte Untertitel und Text-Einblendungen, nur wenn verlangt.

Der Eigenton der Clips wird leise beigemischt, nicht stummgeschaltet: das
Videomodell erzeugt Atmosphaere, und eine Spur davon unter dem Sprecher klingt
lebendig, wo reine Stille wie eine Diaschau klingt. Wird der Clip gestreckt,
wird sein Eigenton mit atempo mitgestreckt, sonst endet er mitten in der Szene.

Die Musik duckt sich selbst weg (sidechaincompress, der Radiotrick): ein fester
Pegel ist zweimal falsch -- zu laut unter der Stimme, zu leise in den Pausen.

Aufruf
------
  python film_cut.py check
      Sagt, ob ffmpeg, ffprobe und (fuer Standbilder und Text) Pillow da sind.

  python film_cut.py fetch manifest.json
      Laedt alle in manifest.json genannten URLs in den Arbeitsordner und
      ersetzt sie durch die lokalen Dateinamen. Danach ist das Manifest offline
      verwendbar.

  python film_cut.py cut manifest.json
      Schneidet den Film. Schreibt die Zieldatei und, bei subtitles "file",
      eine .srt daneben.

Manifest
--------
{
  "out": "film.mp4",
  "subtitles": "file",            // "none" | "file" | "burn"
  "fps": 25,                      // optional, Standard: Bildrate des 1. Clips
  "width": 1920, "height": 1080,  // optional, Standard: Groesse des 1. Clips
  "music": "musik.mp3",           // optional
  "musicVolume": 0.18,            // optional, 0 schaltet Musik aus
  "originalVolume": 0.1,          // optional, Eigenton der Clips
  "scenes": [
    { "video": "szene-01.mp4", "voice": "szene-01.mp3", "subtitle": "Was gesagt wird",
      "originalVolume": 0 },       // optional, ueberschreibt den Eigenton NUR dieser Szene
    { "image": "szene-02.jpg", "voice": "szene-02.mp3", "subtitle": "...",
      "motion": "zoom_in", "zoom": 0.12 }
  ],
  "overlays": [                   // optional, Text-Einblendungen
    { "scene": 1, "title": "Kapitel 1", "sub": "Worum es geht", "at": 0.6, "dur": 4 }
  ]
}

Szene mit "video": Clip, wird auf die Szenenlaenge gestreckt und interpoliert.
Szene mit "image": Standbild mit Kamerafahrt. "motion" ist zoom_in (Standard),
zoom_out, pan_left, pan_right, pan_up, pan_down oder none; "zoom" ist die
Staerke (Standard 0.12), "zoomBase" der Startzoom (z. B. 1.08, um Raender
wegzuschneiden). Die Laenge kommt aus der Sprecherspur oder aus "seconds".

Relative Pfade gelten gegen den Ordner des Manifests. "voice" und "subtitle"
sind optional. Ein Manifest mit einer einzigen Szene ist genau der Fall "lege
mir die Stimme unter diesen einen Clip" -- dafuer braucht es kein zweites
Werkzeug.

In "overlays" ist "scene" die Szenennummer ab 1, "at" die Sekunden nach
Szenenbeginn (Standard 0.6) und "dur" die Dauer (Standard: bis kurz vor
Szenenende, hoechstens 7 Sekunden).
"""

import json
import math
import os
import shutil
import subprocess
import sys
import urllib.request

# Sprecher werden auf einen festen Pegel gebracht, bevor irgendetwas anderes
# passiert. Szenen sind getrennte Erzeugungen, und getrennte Erzeugungen sind
# nicht gleich laut -- ein Film daraus laesst den Zuschauer alle paar Sekunden
# zur Lautstaerke greifen. -16 LUFS ist der uebliche Wert fuer Sprache im Netz,
# -1.5 dBTP laesst Luft, damit die Mischung nicht uebersteuert.
NARRATION_LOUDNESS = "loudnorm=I=-16:TP=-1.5:LRA=11"

# Die Schwelle ist niedrig genug, dass die leise Atmosphaere unter dem Sprecher
# sie nicht allein ausloest.
MUSIC_DUCKING = "sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400:makeup=1"

DEFAULT_MUSIC_VOLUME = 0.18
DEFAULT_ORIGINAL_VOLUME = 0.1
MUSIC_FADE = 2.0
# Laenger wird nicht geschnitten, sondern in Teilen -- sonst laeuft es in einen
# Zeitablauf, nachdem schon eine Stunde gerechnet wurde.
MAX_FILM_SECONDS = 600

# Bewegungsinterpolation: aus zwei echten Bildern wird das Bild dazwischen
# gerechnet, statt eines zu verdoppeln. mci = motion compensated interpolation,
# aobmc glaettet die Bloeckgrenzen, bidir schaut in beide Richtungen.
INTERPOLATE = ("minterpolate=fps={fps}:mi_mode=mci:mc_mode=aobmc"
               ":me_mode=bidir:vsbmc=1")

# Ab hier sieht auch interpolierte Streckung nach Zeitlupe aus.
STRETCH_WARN = 1.5

DEFAULT_ZOOM = 0.12
MOTIONS = ("zoom_in", "zoom_out", "pan_left", "pan_right", "pan_up", "pan_down", "none")

# Fuer die Text-Einblendungen. Die erste Schrift, die es gibt, wird genommen.
FONTS_BOLD = (
    "C:/Windows/Fonts/segoeuib.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
)
FONTS_PLAIN = (
    "C:/Windows/Fonts/segoeui.ttf",
    "C:/Windows/Fonts/arial.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/Library/Fonts/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
)

WARNINGS = []


def warn(msg: str):
    WARNINGS.append(msg)
    print(f"HINWEIS: {msg}")


def die(msg: str, code: int = 1):
    print(f"FEHLER: {msg}", file=sys.stderr)
    sys.exit(code)


def tool_path(name: str):
    return shutil.which(name) or shutil.which(name + ".exe")


def require_tools():
    missing = [t for t in ("ffmpeg", "ffprobe") if not tool_path(t)]
    if missing:
        die(
            f"{', '.join(missing)} nicht gefunden. Fuer den Videoschnitt muss FFmpeg "
            "lokal installiert sein (es bringt ffmpeg und ffprobe mit). "
            "Windows: winget install Gyan.FFmpeg -- "
            "macOS: brew install ffmpeg -- "
            "Linux: sudo apt install ffmpeg"
        )


def require_pillow(what: str):
    """Pillow braucht es nur fuer Standbilder und Text, nicht fuer Clips."""
    try:
        from PIL import Image  # noqa: F401
    except ImportError:
        die(
            f"{what} braucht Pillow, und Pillow ist nicht installiert. "
            "Installieren mit: python -m pip install pillow"
        )
    from PIL import Image
    return Image


def cmd_check():
    print(f"python   {sys.version.split()[0]}  ({sys.executable})")
    ok = True
    for name in ("ffmpeg", "ffprobe"):
        p = tool_path(name)
        if not p:
            print(f"{name:8} FEHLT")
            ok = False
            continue
        try:
            out = subprocess.run([p, "-version"], capture_output=True, text=True, timeout=20)
            first = (out.stdout or out.stderr).splitlines()[0]
        except Exception as e:  # noqa: BLE001
            print(f"{name:8} gefunden, aber nicht ausfuehrbar: {e}")
            ok = False
            continue
        print(f"{name:8} {first}")
    try:
        from PIL import Image
        print(f"pillow   {getattr(Image, '__version__', 'vorhanden')}")
    except ImportError:
        print("pillow   FEHLT -- nur fuer Standbild-Kamerafahrten und Text-Einblendungen "
              "noetig (python -m pip install pillow)")
    print()
    print("BEREIT" if ok else "NICHT BEREIT -- FFmpeg fehlt")
    sys.exit(0 if ok else 2)


def run_ffmpeg(args, label: str):
    cmd = [tool_path("ffmpeg"), "-hide_banner", "-loglevel", "error", "-y", *args]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        tail = (res.stderr or "").strip()[-800:]
        die(f"ffmpeg scheiterte bei: {label}\n{tail}")
    return res.stderr or ""


def ffprobe(args):
    res = subprocess.run([tool_path("ffprobe"), "-v", "error", *args],
                         capture_output=True, text=True)
    return (res.stdout or "").strip()


def probe_seconds(path: str) -> float:
    try:
        value = float(ffprobe(["-show_entries", "format=duration",
                               "-of", "default=nw=1:nk=1", path]))
    except ValueError:
        die(f"Laenge von {path} nicht lesbar. Ist die Datei vollstaendig heruntergeladen?")
    if value <= 0:
        die(f"{path} ist 0 Sekunden lang.")
    return value


def probe_fps(path: str) -> float:
    raw = ffprobe(["-select_streams", "v:0", "-show_entries", "stream=r_frame_rate",
                   "-of", "default=nw=1:nk=1", path])
    try:
        if "/" in raw:
            num, den = raw.split("/", 1)
            value = float(num) / float(den)
        else:
            value = float(raw)
    except (ValueError, ZeroDivisionError):
        return 0.0
    return round(value, 3) if 1.0 < value < 121.0 else 0.0


def probe_size(path: str):
    raw = ffprobe(["-select_streams", "v:0", "-show_entries", "stream=width,height",
                   "-of", "csv=p=0", path])
    try:
        w, h = [int(x) for x in raw.split(",")[:2]]
    except (ValueError, IndexError):
        return None
    return (w - w % 2, h - h % 2)


def has_audio(path: str) -> bool:
    return bool(ffprobe(["-select_streams", "a:0", "-show_entries", "stream=codec_type",
                         "-of", "default=nw=1:nk=1", path]))


def srt_time(seconds: float) -> str:
    ms = max(0, round(seconds * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, rest = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{rest:03d}"


def filter_path(p: str) -> str:
    """ffmpeg parst Doppelpunkte und Backslashes im subtitles-Filter selbst."""
    return p.replace("\\", "/").replace(":", "\\:").replace("'", "\\'")


def load_manifest(path: str):
    if not os.path.isfile(path):
        die(f"Manifest {path} nicht gefunden.")
    with open(path, encoding="utf-8") as fh:
        try:
            data = json.load(fh)
        except json.JSONDecodeError as e:
            die(f"Manifest ist kein gueltiges JSON: {e}")
    base = os.path.dirname(os.path.abspath(path)) or "."
    if not data.get("scenes"):
        die("Das Manifest hat keine Szenen.")
    return data, base


def resolve(base: str, value: str) -> str:
    return value if os.path.isabs(value) else os.path.join(base, value)


def cmd_fetch(manifest_path: str):
    data, base = load_manifest(manifest_path)
    changed = False

    def pull(url: str, name: str) -> str:
        target = os.path.join(base, name)
        print(f"  {name:28} <- {url}")
        req = urllib.request.Request(url, headers={"User-Agent": "kim-film-cut/1.0"})
        with urllib.request.urlopen(req, timeout=300) as resp, open(target, "wb") as out:
            shutil.copyfileobj(resp, out)
        size = os.path.getsize(target)
        if size == 0:
            die(f"{name} ist leer angekommen.")
        print(f"  {name:28}    {size // 1024} KB")
        return name

    print(f"Lade nach {base}")
    for i, scene in enumerate(data["scenes"], start=1):
        for key, ext in (("video", "mp4"), ("image", "jpg"), ("voice", "mp3")):
            url = scene.get(key)
            if isinstance(url, str) and url.startswith("http"):
                guess = os.path.splitext(url.split("?", 1)[0])[1].lstrip(".").lower()
                if key == "image" and guess in ("jpg", "jpeg", "png", "webp"):
                    ext = guess
                scene[key] = pull(url, f"szene-{i:02d}-{key}.{ext}")
                changed = True
    music = data.get("music")
    if isinstance(music, str) and music.startswith("http"):
        data["music"] = pull(music, "musik.mp3")
        changed = True

    if changed:
        with open(manifest_path, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
        print(f"\nManifest aktualisiert: {manifest_path}")
    else:
        print("\nNichts zu laden -- im Manifest stehen schon lokale Dateien.")


# ---- Kamerafahrt auf einem Standbild ------------------------------------
#
# Portiert aus der erprobten film_build.py: Subpixel-Ausschnitt statt
# ffmpeg-crop, und das Bild vorher mit Lanczos verkleinern, damit nie stark
# heruntergerechnet werden muss. Beides zusammen ergibt eine Fahrt, die nicht
# in ganzen Pixeln springt und bei der feine Strukturen nicht flimmern.

def still_frames(image_path: str, width: int, height: int, fps: float,
                 seconds: float, motion: str, zoom_base: float, zoom: float):
    Image = require_pillow("Eine Standbild-Szene")
    im = Image.open(image_path).convert("RGB")
    iw, ih = im.size

    # Der kleinste Zoom, der im Lauf der Fahrt vorkommt, bestimmt, wie gross
    # das Bild bleiben muss.
    zmin = zoom_base if motion in ("zoom_in", "zoom_out") else zoom_base + zoom
    crop_w = ih * width / height if iw / ih >= width / height else float(iw)
    k = min(1.0, width * zmin / crop_w) if crop_w else 1.0
    if k < 0.999:
        im = im.resize((max(width, round(iw * k)), max(height, round(ih * k))),
                       Image.LANCZOS)
        iw, ih = im.size

    if iw / ih >= width / height:
        crop_w, crop_h = ih * width / height, float(ih)
    else:
        crop_w, crop_h = float(iw), iw * height / width

    total = max(1, int(round(seconds * fps)))
    for i in range(total):
        # Weiches Ein- und Ausschwingen, damit die Fahrt nicht abrupt beginnt.
        e = (1 - math.cos(math.pi * i / max(1, total - 1))) / 2
        if motion == "zoom_in":
            z = zoom_base + zoom * e
        elif motion == "zoom_out":
            z = zoom_base + zoom - zoom * e
        else:
            z = zoom_base + zoom
        vw, vh = crop_w / z, crop_h / z
        x0, y0 = (iw - vw) / 2, (ih - vh) / 2
        if motion == "pan_right":
            x0 = (iw - vw) * e
        elif motion == "pan_left":
            x0 = (iw - vw) * (1 - e)
        elif motion == "pan_down":
            y0 = (ih - vh) * e
        elif motion == "pan_up":
            y0 = (ih - vh) * (1 - e)
        s = vw / width
        frame = im.transform(
            (width, height), Image.AFFINE,
            (s, 0, x0 + 0.5 * s - 0.5, 0, s, y0 + 0.5 * s - 0.5),
            resample=Image.BICUBIC,
        )
        yield frame.tobytes()


def render_still_scene(image_path, voice, out, width, height, fps, seconds,
                       motion, zoom_base, zoom, label):
    args = [tool_path("ffmpeg"), "-hide_banner", "-loglevel", "error", "-y",
            "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{width}x{height}",
            "-r", f"{fps:.3f}", "-i", "-"]
    if voice:
        args += ["-i", voice,
                 "-filter_complex",
                 f"[1:a]{NARRATION_LOUDNESS},apad=whole_dur={seconds:.3f}[a]",
                 "-map", "0:v", "-map", "[a]"]
    else:
        args += ["-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
                 "-map", "0:v", "-map", "1:a"]
    args += ["-t", f"{seconds:.3f}", "-r", f"{fps:.3f}",
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
             "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
             "-movflags", "+faststart", out]
    proc = subprocess.Popen(args, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        for raw in still_frames(image_path, width, height, fps, seconds,
                                motion, zoom_base, zoom):
            proc.stdin.write(raw)
        proc.stdin.close()
    except BrokenPipeError:
        pass
    err = proc.stderr.read().decode("utf-8", "replace")
    proc.wait()
    if proc.returncode != 0:
        die(f"ffmpeg scheiterte bei: {label}\n{err.strip()[-800:]}")


# ---- Text-Einblendungen -------------------------------------------------

def first_font(candidates):
    for p in candidates:
        if os.path.isfile(p):
            return p
    return None


def overlay_card(title: str, sub: str, out: str, width: int, height: int):
    """Schlichte Bauchbinde: dunkler Kasten, heller Text. Bewusst neutral --
    ein Markenlook gehoert in das Projekt, nicht in das Werkzeug."""
    require_pillow("Eine Text-Einblendung")
    from PIL import Image, ImageDraw, ImageFont, ImageFilter

    bold, plain = first_font(FONTS_BOLD), first_font(FONTS_PLAIN)
    if not bold:
        return False
    title_size = max(28, round(height * 0.052))
    sub_size = max(18, round(height * 0.026))
    tf = ImageFont.truetype(bold, title_size)
    sf = ImageFont.truetype(plain or bold, sub_size)

    im = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    tw = d.textlength(title, font=tf)
    sw = d.textlength(sub, font=sf) if sub else 0
    pad_x, pad_y = round(width * 0.03), round(height * 0.028)
    box_w = round(max(tw, sw) + 2 * pad_x)
    box_h = round(title_size + (sub_size + pad_y * 0.6 if sub else 0) + 2 * pad_y)
    x0 = (width - box_w) // 2
    y0 = round(height * 0.80) - box_h // 2
    x1, y1 = x0 + box_w, y0 + box_h
    radius = round(box_h * 0.22)

    shadow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle([x0 - 6, y0 - 6, x1 + 6, y1 + 6],
                                             radius + 6, fill=(0, 0, 0, 120))
    im = Image.alpha_composite(im, shadow.filter(ImageFilter.GaussianBlur(18)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([x0, y0, x1, y1], radius, fill=(16, 18, 24, 205),
                        outline=(255, 255, 255, 60), width=2)
    tb = d.textbbox((0, 0), title, font=tf)
    ty = (y0 + pad_y) - tb[1]
    d.text(((width - tw) / 2, ty), title, font=tf, fill=(255, 255, 255, 255))
    if sub:
        sb = d.textbbox((0, 0), sub, font=sf)
        d.text(((width - sw) / 2, ty + title_size + pad_y * 0.6 - sb[1]), sub,
               font=sf, fill=(226, 230, 238, 235))
    im.save(out)
    return True


def build_overlays(data, base, work, starts, scene_lengths, width, height):
    """Gibt (inputs, chains, letztes_video_label) zurueck, oder None."""
    items = data.get("overlays") or []
    if not items:
        return None
    try:
        from PIL import Image  # noqa: F401
    except ImportError:
        warn("Pillow fehlt, die Text-Einblendungen werden uebersprungen "
             "(python -m pip install pillow).")
        return None
    if not first_font(FONTS_BOLD):
        warn("Keine Schriftdatei gefunden, die Text-Einblendungen werden "
             "uebersprungen.")
        return None

    inputs, chains, placed = [], [], []
    for n, item in enumerate(items, start=1):
        try:
            idx = int(item.get("scene", 0)) - 1
        except (TypeError, ValueError):
            idx = -1
        if idx < 0 or idx >= len(starts):
            warn(f"Einblendung {n} nennt Szene {item.get('scene')}, die es nicht gibt.")
            continue
        title = (item.get("title") or "").strip()
        if not title:
            warn(f"Einblendung {n} hat keinen Titel.")
            continue
        at = float(item.get("at", 0.6))
        room = max(1.0, scene_lengths[idx] - at - 0.3)
        dur = float(item["dur"]) if item.get("dur") else max(3.0, min(7.0, room))
        dur = min(dur, room)
        start = starts[idx] + at
        png = os.path.join(work, f"overlay-{n:02d}.png")
        if not overlay_card(title, (item.get("sub") or "").strip(), png, width, height):
            continue
        inputs += ["-loop", "1", "-t", f"{dur:.3f}", "-i", png]
        placed.append((start, dur))
        print(f"  Einblendung {n}: {title} bei {start:.1f}s fuer {dur:.1f}s")

    if not placed:
        return None
    prev = "[0:v]"
    for n, (start, dur) in enumerate(placed, start=1):
        chains.append(
            f"[{n}:v]format=rgba,fade=t=in:st=0:d=0.5:alpha=1,"
            f"fade=t=out:st={max(0.0, dur - 0.6):.3f}:d=0.6:alpha=1,"
            f"setpts=PTS-STARTPTS+{start:.3f}/TB[ov{n}]"
        )
        label = f"[vo{n}]"
        chains.append(
            f"{prev}[ov{n}]overlay=0:0:eof_action=pass"
            f":enable='between(t,{start:.3f},{start + dur:.3f})'{label}"
        )
        prev = label
    return inputs, chains, prev


def cmd_cut(manifest_path: str):
    require_tools()
    data, base = load_manifest(manifest_path)

    out_path = resolve(base, data.get("out") or "film.mp4")
    subtitles = data.get("subtitles") or "none"
    if subtitles not in ("none", "file", "burn"):
        die('subtitles muss "none", "file" oder "burn" sein.')
    music_volume = float(data.get("musicVolume", DEFAULT_MUSIC_VOLUME))
    original_volume = float(data.get("originalVolume", DEFAULT_ORIGINAL_VOLUME))
    music_path = resolve(base, data["music"]) if data.get("music") else None
    if music_path and not os.path.isfile(music_path):
        die(f"Musikdatei {music_path} nicht gefunden.")

    work = os.path.join(base, "_schnitt")
    os.makedirs(work, exist_ok=True)

    # ---- Format des Films festlegen -------------------------------------
    # Jede Szene bekommt dieselbe Groesse und Bildrate, sonst kann Durchlauf 2
    # nicht kopieren. Die Vorgabe kommt vom ersten Clip, weil der vom Modell
    # kommt und niemand ihn hochrechnen will.
    first_clip = None
    for scene in data["scenes"]:
        if scene.get("video"):
            first_clip = resolve(base, scene["video"])
            break

    size = None
    if data.get("width") and data.get("height"):
        size = (int(data["width"]), int(data["height"]))
    elif first_clip and os.path.isfile(first_clip):
        size = probe_size(first_clip)
    width, height = size or (1920, 1080)
    width, height = width - width % 2, height - height % 2

    fps = float(data["fps"]) if data.get("fps") else 0.0
    if not fps and first_clip and os.path.isfile(first_clip):
        fps = probe_fps(first_clip)
    if not fps:
        fps = 25.0
    fps = round(fps, 3)

    print(f"Film: {width}x{height}, {fps:g} fps")

    scene_files = []
    starts = []
    scene_lengths = []
    elapsed = 0.0

    # ---- Durchlauf 1: je Szene eine Datei -------------------------------
    for i, scene in enumerate(data["scenes"]):
        label = f"Szene {i + 1}/{len(data['scenes'])}"
        voice = resolve(base, scene["voice"]) if scene.get("voice") else None
        if voice and not os.path.isfile(voice):
            die(f"Sprecherdatei {voice} nicht gefunden.")
        voice_seconds = probe_seconds(voice) if voice else 0.0

        is_still = bool(scene.get("image")) and not scene.get("video")
        if not is_still and not scene.get("video"):
            die(f"{label} hat weder video noch image.")

        out = os.path.join(work, f"scene-{i:03d}.mp4")

        if is_still:
            image = resolve(base, scene["image"])
            if not os.path.isfile(image):
                die(f"Bild {image} nicht gefunden. Erst 'fetch' laufen lassen?")
            seconds = float(scene.get("seconds") or voice_seconds)
            if seconds <= 0:
                die(f"{label} ist ein Standbild ohne Sprecher. Dann braucht es "
                    '"seconds".')
            motion = (scene.get("motion") or "zoom_in").lower()
            if motion not in MOTIONS:
                die(f"{label}: motion \"{motion}\" gibt es nicht. Erlaubt: "
                    f"{', '.join(MOTIONS)}.")
            zoom = 0.0 if motion == "none" else float(scene.get("zoom", DEFAULT_ZOOM))
            zoom_base = float(scene.get("zoomBase", 1.0))
            starts.append(elapsed)
            scene_lengths.append(seconds)
            elapsed += seconds
            if elapsed > MAX_FILM_SECONDS:
                die(f"Der Film waere laenger als {round(MAX_FILM_SECONDS / 60)} "
                    "Minuten. In Teilen schneiden.")
            print(f"{label}: {seconds:.1f}s (Standbild, {motion}, subpixel)")
            render_still_scene(image, voice, out, width, height, fps, seconds,
                               motion, zoom_base, zoom, label)
            scene_files.append(out)
            continue

        video = resolve(base, scene["video"])
        if not os.path.isfile(video):
            die(f"Clip {video} nicht gefunden. Erst 'fetch' laufen lassen?")
        video_seconds = probe_seconds(video)
        source_fps = probe_fps(video)
        seconds = max(video_seconds, voice_seconds)
        starts.append(elapsed)
        scene_lengths.append(seconds)
        elapsed += seconds
        if elapsed > MAX_FILM_SECONDS:
            die(f"Der Film waere laenger als {round(MAX_FILM_SECONDS / 60)} Minuten. "
                "In Teilen schneiden.")

        # Streckfaktor: so viel langsamer laeuft der Clip, damit er die Szene
        # ausfuellt. 1.0 heisst, er passt schon.
        stretch = seconds / video_seconds if video_seconds > 0 else 1.0
        stretching = stretch > 1.001
        rate_differs = source_fps <= 0 or abs(source_fps - fps) > 0.01
        interpolate = stretching or rate_differs

        if stretch > STRETCH_WARN + 0.001:
            warn(
                f"{label}: der Clip ist {video_seconds:.1f}s lang, die Szene "
                f"{seconds:.1f}s -- x{stretch:.2f} gestreckt. Ueber x"
                f"{STRETCH_WARN:g} sieht es nach Zeitlupe aus. Besser: den Clip "
                "laenger erzeugen, die Szene teilen, oder ein Standbild mit "
                "Kamerafahrt nehmen."
            )

        chain = []
        if stretching:
            chain.append(f"setpts={stretch:.5f}*PTS")
        if interpolate:
            chain.append(INTERPOLATE.format(fps=f"{fps:.3f}"))
        chain.append(
            f"scale={width}:{height}:force_original_aspect_ratio=decrease:flags=lanczos"
        )
        chain.append(f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=black")
        chain.append("setsar=1,format=yuv420p")
        video_chain = "[0:v]" + ",".join(chain) + "[v]"

        # Der Sprecher wird zuerst auf Pegel gebracht, dann die Atmosphaere
        # DARUNTER gemischt. amix wuerde beide halbieren, deshalb normalize=0.
        # Wird das Bild gestreckt, wird der Eigenton mitgestreckt (atempo),
        # sonst endet die Atmosphaere mitten in der Szene.
        args = ["-i", video]
        if voice:
            args += ["-i", voice]
        # Der Eigenton gilt filmweit, eine Szene darf ihn ueberschreiben: ein
        # Clip mit mitgeneriertem Ton (er laesst sich beim Erzeugen nicht
        # abschalten) gehoert unter den Sprecher auf 0, ein stiller Clip daneben
        # braucht das nicht.
        scene_volume = float(scene.get("originalVolume", original_volume))
        ambience = has_audio(video) and scene_volume > 0
        amb_chain = f"[0:a]volume={scene_volume}"
        if ambience and stretching:
            tempo = 1.0 / stretch
            # atempo kann nur 0.5 bis 2.0 -- darunter in Schritten.
            while tempo < 0.5 - 1e-9:
                amb_chain += ",atempo=0.5"
                tempo /= 0.5
            amb_chain += f",atempo={max(0.5, min(2.0, tempo)):.5f}"
        if voice and ambience:
            audio_chain = (
                f"{amb_chain}[amb];"
                f"[1:a]{NARRATION_LOUDNESS},volume=1.0[nar];"
                "[amb][nar]amix=inputs=2:duration=longest:dropout_transition=0:normalize=0,"
                f"apad=whole_dur={seconds:.3f}[a]"
            )
        elif voice:
            audio_chain = f"[1:a]{NARRATION_LOUDNESS},apad=whole_dur={seconds:.3f}[a]"
        elif ambience:
            audio_chain = f"{amb_chain},apad=whole_dur={seconds:.3f}[a]"
        else:
            args += ["-f", "lavfi", "-i",
                     "anullsrc=channel_layout=stereo:sample_rate=48000"]
            audio_chain = None

        if audio_chain:
            args += ["-filter_complex", f"{video_chain};{audio_chain}",
                     "-map", "[v]", "-map", "[a]"]
        else:
            args += ["-filter_complex", video_chain,
                     "-map", "[v]", "-map", f"{1 if not voice else 2}:a"]

        args += [
            "-t", f"{seconds:.3f}",
            "-r", f"{fps:.3f}",
            # Identische Parameter fuer jede Szene, damit Durchlauf 2 kopieren
            # kann statt neu zu codieren.
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
            "-movflags", "+faststart",
            out,
        ]
        note = f"Clip {video_seconds:.1f}s"
        if stretching:
            note += f", x{stretch:.2f} gestreckt und interpoliert"
        elif rate_differs:
            note += f", {source_fps:g} auf {fps:g} fps interpoliert"
        else:
            note += ", passt"
        print(f"{label}: {seconds:.1f}s ({note})")
        run_ffmpeg(args, label)
        scene_files.append(out)

    # ---- Untertitel aus den Szenentexten --------------------------------
    srt = None
    if subtitles != "none":
        blocks = []
        n = 0
        for i, scene in enumerate(data["scenes"]):
            text = (scene.get("subtitle") or "").strip()
            if not text:
                continue
            n += 1
            start = starts[i]
            end = starts[i + 1] if i + 1 < len(starts) else elapsed
            blocks.append(f"{n}\n{srt_time(start)} --> {srt_time(end)}\n{text}\n")
        if blocks:
            srt = "\n".join(blocks)

    # ---- Durchlauf 2: zusammenfuegen ohne neu zu codieren ---------------
    list_file = os.path.join(work, "scenes.txt")
    with open(list_file, "w", encoding="utf-8", newline="\n") as fh:
        for f in scene_files:
            fh.write("file '" + f.replace("\\", "/") + "'\n")
    body = os.path.join(work, "body.mp4")
    print("Fuege die Szenen zusammen")
    run_ffmpeg(["-f", "concat", "-safe", "0", "-i", list_file, "-c", "copy", body],
               "Szenen zusammenfuegen")

    # ---- Durchlauf 3: Musik, Untertitel, Einblendungen ------------------
    burn = subtitles == "burn" and srt
    wants_music = bool(music_path) and music_volume > 0
    overlays = build_overlays(data, base, work, starts, scene_lengths, width, height)

    if not burn and not wants_music and not overlays:
        run_ffmpeg(["-i", body, "-c", "copy", "-movflags", "+faststart", out_path],
                   "abschliessen")
    else:
        args = ["-i", body]
        video_label = "0:v"
        chains = []
        if overlays:
            ov_inputs, ov_chains, video_label = overlays
            args += ov_inputs
            chains += ov_chains
        if wants_music:
            # Die Musik kommt NACH den Einblendungs-Bildern, sonst zeigen die
            # Indizes in den Ketten auf den falschen Eingang. 0 ist der Film,
            # dann je Einblendung ein PNG, dann die Musik.
            music_index = 1 + (ov_inputs.count("-i") if overlays else 0)
            args += ["-stream_loop", "-1", "-i", music_path]
            fade_start = max(0.0, elapsed - MUSIC_FADE)
            # Die Tonspur des Films ist der Schluessel: wo sie laut ist -- wo
            # also gesprochen wird -- wird die Musik heruntergedrueckt.
            chains += [
                "[0:a]asplit=2[body][key]",
                f"[{music_index}:a]volume={music_volume},"
                f"afade=t=out:st={fade_start:.3f}:d={MUSIC_FADE}[musraw]",
                f"[musraw][key]{MUSIC_DUCKING}[mus]",
                "[body][mus]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[a]",
            ]
        if burn:
            srt_file = os.path.join(work, "subs.srt")
            with open(srt_file, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(srt)
            source = video_label if overlays else "[0:v]"
            if not source.startswith("["):
                source = f"[{source}]"
            chains.append(
                f"{source}subtitles='{filter_path(srt_file)}'"
                ":force_style='FontSize=18,Outline=1,Shadow=0'[vsub]"
            )
            video_label = "[vsub]"
        args += ["-filter_complex", ";".join(chains)]
        args += ["-map", video_label]
        args += ["-map", "[a]" if wants_music else "0:a"]
        args += ["-t", f"{elapsed:.3f}"]
        if burn or overlays:
            args += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                     "-pix_fmt", "yuv420p"]
        else:
            args += ["-c:v", "copy"]
        args += ["-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out_path]
        todo = [t for t, yes in (("Musik", wants_music), ("Untertitel", burn),
                                 ("Einblendungen", bool(overlays))) if yes]
        print("Letzter Durchlauf: " + ", ".join(todo))
        run_ffmpeg(args, "Musik, Untertitel und Einblendungen")

    if srt and subtitles == "file":
        srt_out = os.path.splitext(out_path)[0] + ".srt"
        with open(srt_out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(srt)
        print(f"Untertitel: {srt_out}")

    size_mb = os.path.getsize(out_path) / 1024 / 1024
    print()
    print(f"FERTIG  {out_path}")
    print(f"        {len(data['scenes'])} Szenen, {elapsed:.1f} Sekunden, {size_mb:.1f} MB")
    print(f"        Zwischendateien liegen in {work} und koennen geloescht werden.")
    if WARNINGS:
        print()
        print(f"{len(WARNINGS)} Hinweis(e), die das Ergebnis betreffen:")
        for w in WARNINGS:
            print(f"  - {w}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "check":
        cmd_check()
    elif cmd in ("fetch", "cut"):
        if len(sys.argv) < 3:
            die(f"{cmd} braucht den Pfad zum Manifest.")
        (cmd_fetch if cmd == "fetch" else cmd_cut)(sys.argv[2])
    else:
        die(f'Unbekannter Befehl "{cmd}". Erlaubt: check, fetch, cut.')


if __name__ == "__main__":
    main()
