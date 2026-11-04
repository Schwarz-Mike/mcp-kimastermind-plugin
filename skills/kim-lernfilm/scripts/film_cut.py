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

Was es macht
------------
Drei Durchlaeufe, bewusst nicht ein einziger Filtergraph: ein Graph fuer ein
Dutzend Szenen ist unlesbar und scheitert als Ganzes.

  1. Je Szene eine Datei mit identischen Parametern. Clip und Sprecher sind fast
     nie gleich lang -- der kuerzere wird aufgefuellt: ein kurzer Clip friert
     auf dem letzten Bild, ein kurzer Sprecher bekommt Stille dahinter.
     Strecken waere hoerbar, deshalb wird nicht gestreckt.
  2. Zusammenfuegen ohne neu zu codieren (concat demuxer, Stream-Copy).
  3. Musik und Untertitel in einem letzten Durchlauf, nur wenn verlangt.

Der Eigenton der Clips wird leise beigemischt, nicht stummgeschaltet: das
Videomodell erzeugt Atmosphaere, und eine Spur davon unter dem Sprecher klingt
lebendig, wo reine Stille wie eine Diaschau klingt.

Die Musik duckt sich selbst weg (sidechaincompress, der Radiotrick): ein fester
Pegel ist zweimal falsch -- zu laut unter der Stimme, zu leise in den Pausen.

Aufruf
------
  python film_cut.py check
      Sagt, ob ffmpeg und ffprobe da sind, und mit welcher Version.

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
  "music": "musik.mp3",           // optional
  "musicVolume": 0.18,            // optional, 0 schaltet Musik aus
  "originalVolume": 0.1,          // optional, Eigenton der Clips
  "scenes": [
    { "video": "szene-01.mp4", "voice": "szene-01.mp3", "subtitle": "Was gesagt wird" },
    { "video": "szene-02.mp4", "voice": "szene-02.mp3", "subtitle": "..." }
  ]
}

Relative Pfade gelten gegen den Ordner des Manifests. "voice" und "subtitle"
sind optional. Ein Manifest mit einer einzigen Szene ist genau der Fall "lege
mir die Stimme unter diesen einen Clip" -- dafuer braucht es kein zweites
Werkzeug.
"""

import json
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


def probe_seconds(path: str) -> float:
    res = subprocess.run(
        [tool_path("ffprobe"), "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", path],
        capture_output=True, text=True,
    )
    try:
        value = float((res.stdout or "").strip())
    except ValueError:
        die(f"Laenge von {path} nicht lesbar. Ist die Datei vollstaendig heruntergeladen?")
    if value <= 0:
        die(f"{path} ist 0 Sekunden lang.")
    return value


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
        for key, ext in (("video", "mp4"), ("voice", "mp3")):
            url = scene.get(key)
            if isinstance(url, str) and url.startswith("http"):
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

    scene_files = []
    starts = []
    elapsed = 0.0

    # ---- Durchlauf 1: je Szene eine Datei -------------------------------
    for i, scene in enumerate(data["scenes"]):
        video = resolve(base, scene["video"])
        if not os.path.isfile(video):
            die(f"Clip {video} nicht gefunden. Erst 'fetch' laufen lassen?")
        voice = resolve(base, scene["voice"]) if scene.get("voice") else None
        if voice and not os.path.isfile(voice):
            die(f"Sprecherdatei {voice} nicht gefunden.")

        video_seconds = probe_seconds(video)
        voice_seconds = probe_seconds(voice) if voice else 0.0
        scene_seconds = max(video_seconds, voice_seconds)
        starts.append(elapsed)
        elapsed += scene_seconds
        if elapsed > MAX_FILM_SECONDS:
            die(f"Der Film waere laenger als {round(MAX_FILM_SECONDS / 60)} Minuten. In Teilen schneiden.")

        out = os.path.join(work, f"scene-{i:03d}.mp4")
        args = ["-i", video]
        if voice:
            args += ["-i", voice]

        pad = max(0.0, scene_seconds - video_seconds)
        video_chain = (
            "[0:v]scale=trunc(iw/2)*2:trunc(ih/2)*2,fps=25,"
            f"tpad=stop_mode=clone:stop_duration={pad:.3f}[v]"
        )
        # Der Sprecher wird zuerst auf Pegel gebracht, dann die Atmosphaere
        # DARUNTER gemischt. amix wuerde beide halbieren, deshalb normalize=0.
        if voice:
            audio_chain = (
                f"[0:a]volume={original_volume}[amb];"
                f"[1:a]{NARRATION_LOUDNESS},volume=1.0[nar];"
                "[amb][nar]amix=inputs=2:duration=longest:dropout_transition=0:normalize=0,"
                f"apad=whole_dur={scene_seconds:.3f}[a]"
            )
        else:
            audio_chain = f"[0:a]volume={original_volume},apad=whole_dur={scene_seconds:.3f}[a]"

        args += [
            "-filter_complex", f"{video_chain};{audio_chain}",
            "-map", "[v]", "-map", "[a]",
            "-t", f"{scene_seconds:.3f}",
            # Identische Parameter fuer jede Szene, damit Durchlauf 2 kopieren
            # kann statt neu zu codieren.
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
            "-movflags", "+faststart",
            out,
        ]
        print(f"Szene {i + 1}/{len(data['scenes'])}: {scene_seconds:.1f}s"
              + (f" (Bild {video_seconds:.1f}s aufgefuellt)" if pad > 0.05 else ""))
        run_ffmpeg(args, f"Szene {i + 1}")
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

    # ---- Durchlauf 3: Musik und eingebrannte Untertitel -----------------
    burn = subtitles == "burn" and srt
    wants_music = bool(music_path) and music_volume > 0

    if not burn and not wants_music:
        run_ffmpeg(["-i", body, "-c", "copy", "-movflags", "+faststart", out_path], "abschliessen")
    else:
        args = ["-i", body]
        if wants_music:
            args += ["-stream_loop", "-1", "-i", music_path]
        chains = []
        if wants_music:
            fade_start = max(0.0, elapsed - MUSIC_FADE)
            # Die Tonspur des Films ist der Schluessel: wo sie laut ist -- wo
            # also gesprochen wird -- wird die Musik heruntergedrueckt.
            chains += [
                "[0:a]asplit=2[body][key]",
                f"[1:a]volume={music_volume},afade=t=out:st={fade_start:.3f}:d={MUSIC_FADE}[musraw]",
                f"[musraw][key]{MUSIC_DUCKING}[mus]",
                "[body][mus]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[a]",
            ]
        if burn:
            srt_file = os.path.join(work, "subs.srt")
            with open(srt_file, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(srt)
            chains.append(
                f"[0:v]subtitles='{filter_path(srt_file)}'"
                ":force_style='FontSize=18,Outline=1,Shadow=0'[v]"
            )
        args += ["-filter_complex", ";".join(chains)]
        args += ["-map", "[v]" if burn else "0:v"]
        args += ["-map", "[a]" if wants_music else "0:a"]
        args += ["-t", f"{elapsed:.3f}"]
        if burn:
            args += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p"]
        else:
            args += ["-c:v", "copy"]
        args += ["-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out_path]
        print("Mische Musik" + (" und brenne Untertitel ein" if burn else ""))
        run_ffmpeg(args, "Musik und Untertitel")

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
