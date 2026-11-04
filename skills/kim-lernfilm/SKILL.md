---
name: kim-lernfilm
description: "Use when the user wants a complete video produced, not a single clip -- a learning film, explainer, course video, tutorial, product film or social clip with several scenes, narration, music and subtitles. Triggers: Lernvideo, Lernfilm, Erklaervideo, Tutorial-Video, Kursvideo, Schulungsvideo, Imagefilm, Produktvideo, Reel mit Sprecher, Video mit mehreren Szenen, Storyboard, mach mir ein Video ueber, learning video, explainer video, course video, tutorial video. Runs the whole chain: questions, local environment check (FFmpeg and Python), model choice, storyboard for approval, scene images, narration, clips, music, and then the final cut ON THE USER'S OWN MACHINE with FFmpeg -- the server generates, it does not edit. Expensive -- a minute of finished film costs between roughly 180 and 770 credits depending on the video model, so the model is chosen WITH the user and the budget is named before anything is generated. For ONE clip use kim-video, for speech alone kim-voice, for music alone kim-music."
version: 1.4.0
---

# KIM Lernfilm Skill

## Purpose

Produce a finished film from nothing: storyboard, pictures, narration, music,
clips, cut. Everything runs through the KIMASTERMIND_IMAGES MCP tools and ends
as one MP4 with optional subtitles.

**This is the most expensive thing on the platform.** Say what it costs before
generating anything — see "Budget" below. A user with 20 free credits can afford
about two and a half seconds of film.

---

## The three constraints that shape everything

Learn these before writing a storyboard; they are not negotiable and every one
of them has cost someone money.

**1. A clip is 4 to 15 seconds** (3 on the old `happyhorse-1.0`). A scene cannot be longer. A two-minute film is
at least eight scenes, and each is generated separately.

**2. The narration decides the scene length, never the picture.** Generate the
narration first, measure it, then order a clip of that length. The other way
round the picture freezes on its last frame while the voice runs on — the cut
does that deliberately rather than stretching anything, and it looks like a
fault. **Keep each scene's text under ~240 characters**, which is about 15
seconds of speech.

**3. Everything must be assembled on the same day.** Narration and music are
deleted after **24 hours**. A storyboard from yesterday cannot be cut without
generating the voice again. Say this before a long session, and assemble as soon
as the material is complete. **Download every piece right after it is
generated**, not at the end — then a 24-hour boundary in the middle of a long
session costs nothing.

**4. The cut runs on the user's machine, not on the server.** The server
generates pictures and sound; joining them is plain computation on files the
user gets anyway. A two-minute film means a dozen H.264 passes, and while those
ran on the server every other customer was served worse. So: download the
parts, cut locally with FFmpeg. That needs **FFmpeg and Python** on the user's
computer, which is why Step 0 checks for them **before** a single credit is
spent.

---

## Available MCP Commands

- `voice_listing`, `voice_generate` — narration. See kim-voice for the engines
- `music_generate` — music. See kim-music
- `generate_image` — one reference picture per scene
- `generate_video` — the clips, mode `image` with the scene picture
- `my_credits` — balance. Fetch it fresh before the budget line

Der Schnitt ist **kein** MCP-Werkzeug mehr. Er laeuft lokal ueber
`scripts/film_cut.py` (Step 0 und Step 8). Das serverseitige `film_assemble`
gibt es im Protokoll noch, wird von diesem Ablauf aber nicht mehr benutzt:
Filmproduktion gehoert nicht auf den Server.

---

## Step 0: Die Umgebung pruefen, bevor Credits fliessen

Der Schnitt braucht **FFmpeg** und **Python** lokal. Das zuerst zu pruefen ist
kein Formalismus: wer acht Clips erzeugt und dann merkt, dass er sie nicht
zusammenfuegen kann, hat mehrere hundert Credits fuer Einzelteile bezahlt.

Der Skill bringt das Werkzeug mit: `scripts/film_cut.py` im Skill-Ordner. Den
Pfad findest du ueber `${CLAUDE_PLUGIN_ROOT}` oder im entpackten Skill-Ordner;
kopier das Skript in den Arbeitsordner des Films, dann sind die Befehle kurz.

```
python film_cut.py check
```

Die Ausgabe nennt die Version von Python, ffmpeg und ffprobe und endet mit
`BEREIT` oder `NICHT BEREIT`. Laeuft der Befehl gar nicht, fehlt Python.

**Fehlt etwas, wird NICHTS installiert, ohne zu fragen.** Sag, was fehlt, wofuer
es gebraucht wird, und warte auf ein ausdrueckliches Ja:

> "Fuer den Schnitt brauche ich FFmpeg auf deinem Rechner — damit werden die
> Clips, die Sprecherspur und die Musik zu einem Film zusammengefuegt. Das
> laeuft dann bei dir lokal statt auf dem Server und ist deshalb auch
> schneller. Installieren mit `winget install Gyan.FFmpeg`. Soll ich das
> ausfuehren?"

| System | Befehl |
|---|---|
| Windows | `winget install Gyan.FFmpeg` |
| macOS | `brew install ffmpeg` |
| Linux (Debian/Ubuntu) | `sudo apt install ffmpeg` |
| Python fehlt (Windows) | `winget install Python.Python.3.12` |

Erst nach dem Ja installieren, danach `check` erneut laufen lassen und **merken,
dass es jetzt da ist** — nicht bei jedem Film neu fragen.

**Sagt der Nutzer Nein**, ist das in Ordnung, aber es muss klar sein, was dann
herauskommt: die einzelnen Clips, die Sprecherspuren und die Musik als
getrennte Dateien, kein fertiger Film. Frag, ob er den Film unter dieser
Bedingung trotzdem will. Auf den Server wird der Schnitt **nicht** ausgelagert.

Dazu einen **Arbeitsordner** festlegen und nennen, zum Beispiel
`%USERPROFILE%\Videos\KI-Filme\<thema>-<datum>\`. Dort landet alles: Bilder,
Sprecherspuren, Clips, Musik, das Manifest, der Film.

---

## Step 1: The questions

Ask everything still open **in one message**, numbered. Never one at a time —
eleven questions one by one is an interrogation.

1. **Thema** des Films
2. **Zielpublikum** (bestimmt Ton und Tempo der Sprache)
3. **Wo veroeffentlicht?** Social Media / YouTube / Leinwand → bestimmt die
   Aufloesung. Es gibt **zwei** Stufen: 720p (Standard, guenstiger) und 1080p
   (fast doppelt so teuer). Leinwand heisst 1080p, alles andere 720p
4. **Format**: 16:9 (breit), 9:16 (Hochformat/Story), 1:1 (quadratisch),
   auch 4:3 und 3:4
5. **Laenge** in Sekunden oder Minuten
6. **Musik** ja/nein
7. **Welche Musik**, in eigenen Worten (Stil, Stimmung)
8. **Stil**: Cinematic, Comic, Normal, Abstrakt — oder frei beschrieben
9. **Schnitttempo**: schnell (3–5 s je Szene), mittel (6–9 s), langsam (10–15 s)
10. **Sprecherstimme** ja/nein
11. **Untertitel**: keine, ins Bild eingebrannt, oder als separate SRT-Datei

Was der Nutzer schon gesagt hat, wird nicht gefragt. „Mach mir ein 60-Sekunden-
Erklaervideo fuer Instagram ueber Photosynthese, mit Sprecher und ruhiger Musik"
beantwortet 1, 2, 3, 4, 5, 6, 7 und 10 — frag nur noch Stil, Tempo und
Untertitel.

**Auch gleich fragen: wohin soll das Material?** Ein lokaler Ordner fuer Bilder,
Clips, Stimme, Musik und den fertigen Film. Ohne Angabe: nach dem Pfad fragen,
bevor etwas erzeugt wird — nicht am Schluss, wenn schon alles bezahlt ist.

---

## Step 1.5: Das Videomodell mit dem Nutzer waehlen

**Das ist der groesste Hebel im ganzen Film.** Die Clips sind rund 90 % der
Kosten, und zwischen dem guenstigsten und dem teuersten Modell liegt Faktor
fuenf. Einen Film still im teuersten Modell zu rendern ist der Fehler, der hier
richtig Geld kostet — also **fragen, bevor gerechnet wird.**

| Modell (`model`) | Credits/Sek | 60 s Clips | Wofuer |
|---|---|---|---|
| `minimax-h3-lite` 480p | 2,5 | 150 | Entwurf, interner Testlauf |
| `minimax-h3-lite` 768p | 4 | 240 | Der vernuenftige Standard |
| `minimax-h3-highspeed` 768p | 6 | 360 | Wenn Lite zu einfach wirkt |
| `minimax-h3` 768p | 7,6 | 456 | Hoechste Stufe ohne 2K |
| `minimax-h3` 2K | 12,4 | 744 | 2K, fuer grosse Projektion |
| `happyhorse-1.0` 720p | 8,33 | 500 | Das bisherige Modell |

Zahlen immer gegen `list_models` pruefen, nie aus dem Gedaechtnis zitieren.

So fragen — mit einer Empfehlung, nicht als offene Liste:

> Fuer die Clips hast du mehrere Modelle. Ich wuerde **H3 Lite in 768p** nehmen:
> 60 Sekunden Film kosten damit etwa 240 Credits statt 500 beim alten Modell.
> Wenn du 2K brauchst, geht nur **H3**, dann sind es rund 744. Oder wir machen
> zuerst einen Entwurf in 480p fuer etwa 150 Credits und du schaust, ob die
> Bildsprache passt.

**Der Entwurfsweg ist der ehrlichste Rat bei einem ersten Film:** eine Minute in
480p kostet ein Fuenftel und zeigt bereits, ob Storyboard, Schnittrhythmus und
Stimme zusammenpassen. Erst danach lohnt die teure Fassung.

> **Noch offen:** welches Modell das *schoenere Bild* macht, steht hier
> absichtlich nicht. Die H3-Modelle sind neu (04.11.2026) und noch nicht am
> eigenen Material geprueft. Bis dahin nach Preis, Aufloesung und Tempo beraten.

Das gewaehlte Modell gilt fuer **alle** Clips des Films. Mitten im Film zu
wechseln bricht die Bildsprache und faellt im Schnitt auf.

---

## Step 2: Budget, bevor irgendetwas erzeugt wird

Rechne die Summe aus und nenne sie. Die Zahlen gegen `list_models` und
`voice_listing` pruefen, nie aus dem Gedaechtnis zitieren.

| Posten | Preis | Beispiel: 60 s, 8 Szenen, H3 Lite 768p |
|---|---|---|
| Clips | **nach Modell, siehe Step 1.5** | 240 |
| Szenenbilder | 1 Credit je Bild (Qualitaet „low") | 8 |
| Sprecher | je Szene mind. 1 Credit | 8 |
| Musik | 10 Credits je Minute (Pro, Laenge einstellbar) | 10 |
| Geraeusche | 1 Credit je Geraeusch, Laenge egal | 3 |
| Schnitt | **0** | 0 |
| | | **≈ 269 Credits ≈ 11 CHF** |

Nur die Clip-Zeile aendert sich mit dem Modell; alles andere bleibt. Dieselben
60 Sekunden kosten im Entwurfsmodus rund **179**, in 2K rund **773** Credits.

Sag es als einen Satz, mit dem Guthaben daneben:

> Das ergibt 8 Szenen zu je 7,5 Sekunden. Mit H3 Lite in 768p zusammen etwa
> **269 Credits**, davon 240 fuer die Clips. Du hast aktuell **900 Credits**.
> Soll ich?

**Ab 60 Sekunden Film ausdruecklich bestaetigen lassen** — nicht nur die Zahl
nennen, sondern auf ein Ja warten. Zwei Minuten sind beim Standardmodell rund
520 Credits, in 2K rund 1500.

Reicht das Guthaben nicht, rechne die Alternativen vor, statt nur abzulehnen:
ein guenstigeres Modell (der grosse Hebel), kuerzer, oder weniger Szenen bei
gleicher Laenge.

---

## Step 3: Storyboard

Erzeuge das Storyboard und zeig es als **Tabelle**:

| Nr. | Szene | Beschreibung | Sek | Stimme (Text) |
|---|---|---|---|---|
| 1 | Aufhaenger | Nahaufnahme eines Blattes, Sonne im Gegenlicht | 0–7 | „Jeden Tag macht dieses Blatt etwas, das kein Labor nachbaut." |
| 2 | Das Problem | … | 7–14 | … |

Regeln fuer die Spalte Stimme:
- **hoechstens ~240 Zeichen je Szene** (siehe Constraint 2)
- gesprochene Sprache, keine Schriftsprache: kurze Saetze, keine Klammern,
  keine Aufzaehlungszeichen
- was in der Spalte steht, ist spaeter woertlich der Untertitel

Regeln fuer die Beschreibung: was man **sieht**, nicht was es bedeutet. Der Text
geht als Bildprompt weiter.

**Dann fragen: Korrekturen oder freigeben?** Aendere so lange, bis ein Ja kommt.
Korrekturen am Storyboard sind gratis — alles danach kostet.

---

## Step 4: Szenenbilder

Nach der Freigabe: **ein Bild je Szene**, Modell `gpt-image-2.5-flare`,
`quality: "low"`, im gewaehlten Seitenverhaeltnis. Das ist 1 Credit je Szene und
die billigste Qualitaetssteigerung im ganzen Ablauf: ein Clip, der aus einem
Bild entsteht, folgt der Vorlage viel enger als einer aus blossem Text.

Sag das so, bevor du anfaengst — und sag auch, dass es optional ist:

> „Ich erzeuge zuerst ein Startbild je Szene, 8 Credits zusammen. Dann siehst du,
> wie der Film aussieht, bevor die teuren Clips entstehen. Ohne Bilder geht es
> auch, dann wird es weniger vorhersehbar."

Alle Bilder zusammen zeigen, dann fragen: einverstanden, oder einzelne neu?
Ein neues Bild kostet wieder 1 Credit — ein misslungener Clip 60.

---

## Step 5: Stimme

Nur wenn gewuenscht. Zeig **zuerst die Hoerproben**, bevor nach einer Stimme
gefragt wird:

```
Studio  (30 Stimmen, mit Charakter):  https://mcp.kimastermind.net/voices/studio
Express (28 Stimmen, schnell):        https://mcp.kimastermind.net/voices/express
```

Ist ein Browser-Werkzeug da, oeffne die Studio-Seite direkt. Fuer einen Lernfilm
passt meist **Studio** — die Betonung traegt ueber mehrere Minuten besser.
Empfiehl zwei, drei Stimmen mit Charakter aus dem Katalog.

Dann **je Szene eine eigene Aufnahme** mit dem Text aus dem Storyboard. Einzeln,
nicht am Stueck: nur so laesst sich jede Szene genau auf ihre Sprechdauer
schneiden, und eine misslungene Szene kostet nur sich selbst.

**Notiere je Szene die Audio-ID** aus der Download-URL (`/aud/<id>.mp3`) und die
gemeldete Laenge. Beides brauchst du gleich.

---

## Step 6: Clips

Jetzt erst, und **je Szene mit der gemessenen Sprechdauer als `duration`**,
gerundet auf ganze Sekunden, begrenzt auf 3–15:

```
generate_video(
  model = <das in Step 1.5 gewaehlte Modell>,
  mode = "image",
  prompt = <Beschreibung aus dem Storyboard, plus der gewaehlte Stil>,
  reference_images = [<URL des Szenenbilds>],
  duration = <Sprechdauer der Szene>,
  aspect_ratio = <gewaehltes Format>,
  quality = <zum Modell passend: 480p/768p, 768p, 768p/2k oder 720p/1080p>
)
```

`model` **immer mitgeben**. Ohne Angabe nimmt das Werkzeug `happyhorse-1.0`, und
das ist in fast allen Faellen das falsche: teurer als H3 Lite bei nicht mehr
Aufloesung. Eine vergessene Zeile kostet hier ueber 200 Credits pro Filmminute.

Auf den H3-Modellen darf `reference_images` ein **zweites** Bild tragen, das
Schlussbild der Szene. Das ist nuetzlich, wenn eine Szene von einem Zustand in
einen anderen fuehrt (Diagramm leer, dann Diagramm gefuellt): beide Bilder in
Step 4 erzeugen und als `[Startbild, Schlussbild]` uebergeben.

Ein **sprechendes Portrait** als Moderator-Szene geht ebenfalls, aber nur auf
den H3-Modellen und nur ueber `mode = "reference"` mit der Sprecherspur in
`reference_audios` — der genaue Ablauf steht in **kim-video**,
Step V0.6. Fuer eine solche Szene die Sprecherdauer auf maximal 15 Sekunden
halten.

**Vor dem ersten Aufruf sagen, dass es dauert**: jeder Clip braucht ein bis
fuenf Minuten, bei acht Szenen also gut eine halbe Stunde. Nicht abbrechen, nicht
neu starten — ein Abbruch bezahlt den Clip trotzdem.

Nach jedem Clip die **Video-ID** notieren (`/vid/<id>.mp4`).

---

## Step 7: Musik und Geraeusche

### Geraeusche je Szene — optional, aber wirkungsvoll

Ein Erklaervideo braucht sie nicht. Eine Szene mit Regen, Meer, Feuer, einer
zuschlagenden Tuer oder einem Gong gewinnt enorm. `sfx_generate`, Laenge frei
von 0,5 bis 22 Sekunden, **1 Credit je Geraeusch unabhaengig von der Laenge** —
gegen 500 fuer die Clips ist das nichts. Weil die Laenge nichts kostet, nimm die
Laenge, die die Szene braucht.

Frag einmal, nicht je Szene: „Sollen einzelne Szenen Geraeusche bekommen?" Wenn
ja, nenne die Szenen, bei denen es sich lohnt, und erzeuge sie. Beim Schnitt
kommen sie als zusaetzliche Tonspur dazu.

Wichtig: Der Videoclip bringt **bereits eigenen Ton** mit, der auf 10 % gedaempft
wird. Ein zusaetzliches Geraeusch legt sich darueber — also sparsam und nur dort,
wo es wirklich traegt.

### Musik

Nur wenn gewuenscht. Siehe kim-music fuer die Fragen und die Prompt-Uebersetzung
ins Englische.

**Nimm `engine: "pro"` und setze `seconds` auf die Filmlaenge.** Das ist die
einzige Engine, bei der die Musik genau so lang wird wie bestellt — bis fuenf
Minuten. Ein Stueck, das dort endet, wo der Film endet, klingt komponiert; ein
geloopte Flaeche klingt nach Hintergrund. Und sie wird pro Minute abgerechnet,
ist also fuer einen Film unter drei Minuten auch das Guenstigste.

Ueber fuenf Minuten Film: **ein** Stueck erzeugen und beim Schnitt loopen lassen.
Erzeuge niemals mehrere Stuecke fuer einen laengeren Film — zwei Aufrufe ergeben
zwei verschiedene Kompositionen mit hoerbarer Naht.

Die Musik wird beim Schnitt automatisch leiser, wenn gesprochen wird, und blendet
am Ende aus. Du musst nichts dafuer tun.

---

## Step 8: Der Schnitt — lokal, mit FFmpeg

**Kostet keine Credits**, weil nichts erzeugt wird: es wird nur gerechnet, und
zwar auf dem Rechner des Nutzers. Zwei Befehle.

### 8a: Ein Manifest schreiben

In den Arbeitsordner, als `manifest.json`. Die Szenen **in der Reihenfolge des
Storyboards**, mit den URLs, die die Erzeugung geliefert hat:

```json
{
  "out": "film.mp4",
  "subtitles": "file",
  "music": "https://mcp.kimastermind.net/aud/<id>.mp3",
  "scenes": [
    {
      "video": "https://mcp.kimastermind.net/vid/<id>.mp4",
      "voice": "https://mcp.kimastermind.net/aud/<id>.mp3",
      "subtitle": "Der Satz, der in dieser Szene gesprochen wird"
    }
  ]
}
```

`subtitles`: `"file"` legt eine .srt daneben, `"burn"` brennt sie ins Bild,
`"none"` laesst sie weg. Optional sind `musicVolume` (Standard 0.18) und
`originalVolume` (Standard 0.1, der Eigenton der Clips).

### 8b: Herunterladen und schneiden

```
python film_cut.py fetch manifest.json
python film_cut.py cut manifest.json
```

`fetch` holt alle URLs in den Arbeitsordner und schreibt die lokalen
Dateinamen ins Manifest zurueck. Danach ist es offline verwendbar — wichtig
wegen der 24-Stunden-Grenze: nach `fetch` kann der Schnitt auch morgen noch
wiederholt werden.

`cut` arbeitet in drei Durchlaeufen und sagt bei jedem, was es tut.

Was der Schnitt von selbst tut, ohne Zutun:
- jede Szene dauert so lange wie ihre laengere Haelfte: ein kurzer Clip friert
  auf dem letzten Bild, eine kurze Sprecherspur bekommt Stille dahinter.
  Gestreckt wird nichts, das waere hoerbar
- **alle Sprecheraufnahmen werden auf denselben Pegel gebracht** (-16 LUFS) —
  ohne das springt die Lautstaerke von Szene zu Szene
- die Musik wird gedrueckt, solange gesprochen wird: **die Stimme ist immer
  lauter als die Musik**, und in den Pausen kommt die Musik von selbst zurueck
- der Originalton der Clips bleibt leise darunter (10 %) statt stumm
- Untertitel entstehen aus den Szenentexten und den **gemessenen** Laengen, sind
  also zwangslaeufig synchron
- die Musik blendet am Ende ueber zwei Sekunden aus

Dauer: deutlich kuerzer als der Film selbst, auf einem normalen Rechner etwa ein
Viertel bis die Haelfte der Filmlaenge. Zwischendateien liegen im Unterordner
`_schnitt` und koennen danach weg.

### Wenn es scheitert

Das Skript nennt den Durchlauf und die letzte ffmpeg-Meldung. Die drei
haeufigsten Faelle:

| Meldung | Ursache |
|---|---|
| `ffmpeg nicht gefunden` | Step 0 uebersprungen. Nachinstallieren, nachfragen |
| `Clip ... nicht gefunden` | `fetch` lief nicht, oder im Manifest stehen noch URLs |
| `Laenge von ... nicht lesbar` | Download abgebrochen, Datei halb. Nochmal `fetch` |

Ein fehlgeschlagener Schnitt kostet **keine Credits** — das Material liegt schon
lokal. Sag das, damit niemand glaubt, er muesse neu erzeugen.

---

## Step 9: Uebergabe

- **Den Film abspielen oder oeffnen**, nicht nur verlinken — wie in kim-voice:
  herunterladen und dem Systemplayer uebergeben, sonst der Link
- **Alles liegt schon im Arbeitsordner** — `fetch` hat es dorthin geholt.
  Aufraeumen und benennen:
  ```
  <Arbeitsordner>/
    01-szene.png  02-szene.png  ...
    szene-01-voice.mp3  szene-02-voice.mp3  ...
    szene-01-video.mp4  szene-02-video.mp4  ...
    musik.mp3
    manifest.json      <- der Schnitt ist damit wiederholbar
    film.mp4
    film.srt
    storyboard.md
    _schnitt/          <- Zwischendateien, koennen weg
  ```
  **Das Manifest nicht loeschen.** Mit ihm laesst sich der Film erneut
  schneiden — etwa mit eingebrannten Untertiteln statt einer .srt oder mit
  anderer Musiklautstaerke — ohne ein einziges Credit.
- **Die Gesamtkosten nennen**: was verbraucht wurde und was bleibt
- **Die 24-Stunden-Warnung**: Stimme und Musik verschwinden auf dem Server
  nach 24 Stunden. Nach `fetch` liegt alles lokal, die Warnung ist damit
  abgehakt — sag aber, dass die URLs selbst bald ins Leere zeigen. Die Clips
  bleiben laenger: die neuesten 50 Filme dauerhaft, der Rest 30 Tage mit
  Vorwarnung per Mail

---

## Was nicht geht

- **Kein Ton aus dem Videomodell steuerbar** — die Clips bringen eigene
  Umgebungsgeraeusche mit, die nur leiser oder stumm gestellt werden koennen
- **Lippensynchronitaet nur auf den H3-Modellen** und nur in einer eigenen
  Szene: Portrait plus Sprecherspur ueber `mode = "reference"`, Ablauf in
  **kim-video**, Step V0.6. In den aus Szenenbildern animierten Clips bewegen
  sich keine Lippen passend zum Text
- **Keine exakte Szenenlaenge ueber 15 Sekunden**
- **Kein Text im Bild zuverlaessig** — Schrift in generierten Clips wird oft
  falsch. Titel und Beschriftungen gehoeren in die Untertitel oder in die
  Nachbearbeitung
- **Keine Wiederverwendung**: dieselbe Figur sieht in Szene 2 anders aus als in
  Szene 1. Das Szenenbild als Vorlage mildert es, loest es aber nicht. Bei
  Figuren im Mittelpunkt vorher warnen

---

## Related Skills — die KIM-Familie

| Skill | Wofuer |
|---|---|
| **kim-lernfilm** (dieser) | Der ganze Film: Storyboard bis Schnitt |
| **kim-video** | EIN Clip, ohne Storyboard und Schnitt |
| **kim-voice** | Nur Sprache |
| **kim-music** | Nur Musik |
| **kim-images** | Nur Bilder |
| **kim-meditation** | Gefuehrte Meditation: Skript, Musik, Stimme, Abmischung — reines Audio |
| **kim-sfx** | Geraeusche und Atmosphaeren fuer einzelne Szenen |
| **kimastermind-setup** | Verbindung, Guthaben, Fehlersuche |

Will jemand nur einen einzelnen Clip, schick ihn zu kim-video — dieser Ablauf
hier ist dafuer zu schwer.

---

## Sprache und Ton

- Standardsprache: Deutsch, Du-Form
- Schweizer Schreibweise: ss statt sz
- Modellnamen duerfen genannt werden. **Nicht genannt werden der Anbieter, die
  API und jeder Einkaufspreis.** Credits sind der einzige Preis
- Bei jedem Schritt, der Credits kostet, vorher die Zahl nennen. Bei diesem
  Ablauf summiert sich das schneller als irgendwo sonst
- Kurz halten. Der Nutzer wartet bei diesem Skill ohnehin lange genug
