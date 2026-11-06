---
name: kim-lernfilm
description: "Use when the user wants a complete video produced, not a single clip -- a learning film, explainer, course video, tutorial, product film or social clip with several scenes, narration, music and subtitles. Triggers: Lernvideo, Lernfilm, Erklaervideo, Tutorial-Video, Kursvideo, Schulungsvideo, Imagefilm, Produktvideo, Reel mit Sprecher, Video mit mehreren Szenen, Storyboard, mach mir ein Video ueber, learning video, explainer video, course video, tutorial video. Runs the whole chain: questions, local environment check (FFmpeg, Python, Pillow), model choice, storyboard for approval, scene images, narration, clips, music, and then the final cut ON THE USER'S OWN MACHINE with FFmpeg -- the server generates, it does not edit. Expensive -- a minute of finished film costs between roughly 180 and 770 credits depending on the video model, so the model is chosen WITH the user and the budget is named before anything is generated. For ONE clip use kim-video, for speech alone kim-voice, for music alone kim-music."
version: 1.6.0
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

**1. A clip is 4 to 15 seconds** (3 to 15 on `gemini-omni-flash` and the old `happyhorse-1.0`). A scene cannot be longer. A two-minute film is
at least eight scenes, and each is generated separately.

**2. The narration decides the scene length, never the picture.** Generate the
narration first, measure it, then order a clip of **that** length. Since 11.2026
the cut no longer freezes a short clip on its last frame: it stretches it and
computes the missing frames from the motion, so the picture keeps moving. That
has a limit. **Above roughly x1.5 it reads as slow motion**, whatever the cut
does. Five seconds of clip under twelve seconds of narration is a bad scene, not
a cheap one — split it in two, or make it a still image with a camera move,
which is sharp at any length and costs 1 credit instead of 25 to 60. **Keep each
scene's text under ~240 characters**, which is about 15 seconds of speech.

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

Die Ausgabe nennt die Version von Python, ffmpeg, ffprobe und Pillow und endet
mit `BEREIT` oder `NICHT BEREIT`. Laeuft der Befehl gar nicht, fehlt Python.

**Pillow steht getrennt**, weil es nur zwei Dinge betrifft: Standbild-Szenen mit
Kamerafahrt und Text-Einblendungen. Ein Film aus reinen Clips laeuft ohne
Pillow, und `BEREIT` sagt genau das. Soll eine dieser beiden Sachen vorkommen
und Pillow fehlt, gilt dieselbe Regel wie fuer FFmpeg: fragen, nicht einfach
installieren.

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
| Pillow fehlt (fuer Standbilder und Text) | `python -m pip install pillow` |

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
Kosten, und zwischen dem guenstigsten und dem teuersten Modell liegt ein Vielfaches.
Dazu koennen die Modelle **Verschiedenes**: eines bringt eigenen Ton mit, nur die
H3-Modelle koennen lippensynchron sprechen, nur eines liefert 2K. Ein Modell
still zu waehlen heisst, Geld oder Faehigkeiten zu verschenken. Also:

1. **Immer fragen, welches Modell der Nutzer moechte** -- bevor gerechnet wird,
   und auch dann, wenn die Anfrage es nicht erwaehnt. Nie ein Standardmodell
   unterstellen. Nur wenn der Nutzer schon eines genannt hat, entfaellt die
   Frage; passt es nicht zum Auftrag, sag es.
2. **Die Moeglichkeiten erklaeren**, die fuer diesen Film in Frage kommen: was
   jedes gut kann, was nicht, was 60 Sekunden kosten. Zwei, drei Saetze je Modell.
3. **Beraten**: eine Empfehlung mit Grund, passend zum Film (zweite Tabelle), und
   sagen, was die Alternative aendern wuerde.
4. **Sagen, was ausgeschieden ist**, wenn der Film etwas verlangt, das nicht jedes
   Modell kann (Moderator, der spricht; 2K) -- in einem Satz, nicht still.

| Modell (`model`) | Credits/Sek | 60 s Clips | Wofuer |
|---|---|---|---|
| `minimax-h3-lite` 480p | 2,5 | 150 | Entwurf, interner Testlauf |
| `minimax-h3-lite` 768p | 4 | 240 | Der vernuenftige Standard |
| `gemini-omni-flash` 360p | 2,3 | 139 | Entwurf **mit Ton**, schnell |
| `gemini-omni-flash` 720p | 7 | 417 | Schnell, Ton kommt mit, bis 15 s |
| `gemini-omni-flash` 1080p / 4K | 10,4 / 20,9 | 626 / 1251 | Nur hochgerechnet aus 720p: teurer, kein Mehr an Detail |
| `minimax-h3-highspeed` 768p | 6 | 360 | Wenn Lite zu einfach wirkt |
| `minimax-h3` 768p | 7,6 | 456 | Hoechste Stufe ohne 2K |
| `minimax-h3` 2K | 12,4 | 744 | 2K, fuer grosse Projektion |
| `happyhorse-1.0` 720p | 8,33 | 500 | Das bisherige Modell |

Zahlen immer gegen `list_models` pruefen, nie aus dem Gedaechtnis zitieren.

| Der Film braucht ... | Passt | Hinweis |
|---|---|---|
| So wenig Credits wie moeglich, Entwurf | `minimax-h3-lite` 480p oder `gemini-omni-flash` 360p | Etwa gleich teuer. Omni bringt Ton mit (im Schnitt stummzuschalten, siehe unten) |
| Einen Standard fuer die fertige Fassung | `minimax-h3-lite` 768p | Guenstig, fuer die meisten Filme genug |
| Lebendigen Ton in den Szenen (Atmosphaere), schnelle Clips, Hochformat | `gemini-omni-flash` 720p | Native Stufe; 1080p/4K nur hochgerechnet |
| Einen Moderator, der mit der Stimme spricht (Lip-Sync) | ein H3-Modell | Omni nimmt keine eigene Tonspur; Ablauf in **kim-video**, Step V0.6 |
| 2K | `minimax-h3` | Das einzige |

**Was bei `gemini-omni-flash` im Film zu beachten ist:**

- **Der Ton kommt immer mit** (Atmosphaere, Effekte, manchmal Sprache oder Musik)
  und laesst sich beim Erzeugen nicht abschalten. Mit Sprecher darueber gehoert
  er im Schnitt **pro Szene auf 0**: `"originalVolume": 0` in der Szene (Step 8a).
  Ob ein Satz wie „ambient sound only, no speech, no music“ im Prompt ihn
  zuverlaessig leise haelt, ist nicht gemessen -- nicht versprechen.
- **Das Format folgt dem Szenenbild.** Die Szenenbilder in Step 4 im Filmformat
  erzeugen (16:9 oder 9:16), dann stimmt der Clip. Zwei Bilder (Start- und
  Schlussbild) begrenzen die Szene auf 10 Sekunden.
- **Nur 16:9 und 9:16**, kein Seed.

> **Noch offen:** welches Modell das *schoenere Bild* macht, ist nicht am eigenen
> Material verglichen und steht hier absichtlich nicht. Bei Unsicherheit den
> Vorschlag machen: **dieselbe Szene als Entwurf auf zwei Modellen** (H3 Lite 480p
> und Omni Flash 360p, zusammen rund 25 Credits fuer 5 Sekunden) und selbst
> vergleichen lassen. Bis dahin nach Faehigkeit, Preis, Tempo und Ton beraten.

So fragen -- mit einer Empfehlung, nicht als offene Liste:

> Fuer die Clips hast du fuenf Modelle. Ich wuerde **H3 Lite in 768p** nehmen: 60
> Sekunden kosten etwa 240 Credits. Wenn die Szenen lebendigen Ton haben sollen,
> ist **Omni Flash** in 720p die Alternative (rund 417 Credits, der Ton kommt mit
> und wird unter dem Sprecher stummgeschaltet). Soll ein Moderator sprechen, geht
> nur ein **H3**-Modell, und fuer 2K nur **H3**. Welches soll es sein -- oder
> machen wir erst einen Entwurf auf zwei Modellen?

**Der Entwurfsweg ist der ehrlichste Rat bei einem ersten Film:** eine Minute in
480p kostet ein Fuenftel und zeigt bereits, ob Storyboard, Schnittrhythmus und
Stimme zusammenpassen. Erst danach lohnt die teure Fassung.

Das gewaehlte Modell gilt fuer **alle** Clips des Films. Mitten im Film zu
wechseln bricht die Bildsprache und faellt im Schnitt auf. Einzige sinnvolle
Ausnahme: eine Moderator-Szene, die ein H3-Modell braucht -- das ausdruecklich
mit dem Nutzer besprechen.

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

Regeln fuer die Spalte Sek — hier entscheidet sich, ob der Film spaeter ruckelt:
- **Die Clipdauer wird so bestellt, wie die Szene lang wird**, nicht kuerzer.
  Der Schnitt streckt einen zu kurzen Clip und rechnet die Zwischenbilder aus,
  aber ueber etwa x1.5 sieht man es als Zeitlupe
- Eine Szene, deren Text ueber 15 Sekunden laeuft, wird **geteilt**. Zwei Szenen
  mit je acht Sekunden sind besser als eine gestreckte mit sechzehn
- Eine Szene darf auch ein **Standbild mit Kamerafahrt** sein: ein langsamer
  Zoom oder Schwenk ueber das Szenenbild. Das kostet 1 Credit statt 25 bis 60,
  ist bei jeder Laenge scharf und ruckelt nie. Bei Diagrammen, Zitaten, Karten,
  Tabellen und allem, was gelesen werden soll, ist es die bessere Wahl als ein
  animierter Clip — dort zerfaellt Schrift ohnehin. Markier solche Szenen im
  Storyboard, etwa mit „Standbild, langsamer Zoom hinein"
- Diese Mischung ist zugleich der staerkste Hebel auf den Preis. Vier Clips und
  vier Standbilder kosten ungefaehr die Haelfte von acht Clips, und bei einem
  Erklaerfilm faellt es kaum auf

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
  quality = <zum Modell passend: 480p/768p, 768p, 768p/2k, 720p/1080p oder bei Omni Flash 360p/720p/1080p/4k>
)
```

`model` **immer mitgeben**, und zwar das, das der Nutzer in Step 1.5 gewaehlt hat.
Ohne Angabe nimmt das Werkzeug `happyhorse-1.0`, und das ist in fast allen
Faellen nicht das, was gewaehlt wurde: teurer als H3 Lite bei nicht mehr
Aufloesung. Eine vergessene Zeile kostet hier ueber 200 Credits pro Filmminute.

Auf den H3-Modellen und auf Omni Flash darf `reference_images` ein **zweites**
Bild tragen, das Schlussbild der Szene (bei Omni Flash dann hoechstens 10 Sekunden). Das ist nuetzlich, wenn eine Szene von einem Zustand in
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

**Die Dauer nicht kuerzen, um zu sparen.** Wer fuer zwoelf Sekunden Text einen
Clip von fuenf Sekunden bestellt, bekommt keine sieben geschenkten Sekunden,
sondern eine Szene in Zeitlupe: der Schnitt streckt den Clip auf x2.4 und
rechnet die fehlenden Bilder dazu. Billiger wird es durch Teilen der Szene oder
durch ein Standbild mit Kamerafahrt, nie durch einen zu kurzen Clip.

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
    },
    {
      "image": "https://mcp.kimastermind.net/img/<id>.png",
      "voice": "https://mcp.kimastermind.net/aud/<id>.mp3",
      "subtitle": "Diese Szene ist ein Standbild mit langsamem Zoom",
      "motion": "zoom_in",
      "zoom": 0.12
    }
  ],
  "overlays": [
    { "scene": 1, "title": "Kapitel 1", "sub": "Worum es geht", "at": 0.6 }
  ]
}
```

| Feld | Wofuer |
|---|---|
| `subtitles` | `"file"` legt eine .srt daneben, `"burn"` brennt sie ins Bild, `"none"` laesst sie weg |
| `musicVolume` | Standard 0.18, `0` schaltet die Musik aus |
| `originalVolume` | Standard 0.1, der Eigenton der Clips. **Eine Szene darf ihn ueberschreiben**: `"originalVolume": 0` in der Szene schaltet nur ihren Clipton aus -- der Weg fuer Clips von `gemini-omni-flash`, deren Ton sich nicht abschalten laesst |
| `fps`, `width`, `height` | Nur setzen, wenn es einen Grund gibt. Ohne Angabe nimmt der Schnitt Groesse und Bildrate des **ersten Clips** und bringt alle anderen Szenen darauf |

**Eine Szene ist entweder `video` oder `image`.** Bei `image` faehrt die Kamera
ueber das Standbild, und zwar subpixelgenau, also ohne Springen:

| Feld | Wofuer |
|---|---|
| `motion` | `zoom_in` (Standard), `zoom_out`, `pan_left`, `pan_right`, `pan_up`, `pan_down`, `none` |
| `zoom` | Staerke der Fahrt, Standard 0.12. Mehr als 0.25 wirkt unruhig |
| `zoomBase` | Startzoom, z. B. 1.08, um Raender oder Balken wegzuschneiden |
| `seconds` | Nur noetig, wenn die Szene keine Sprecherspur hat |

**`overlays` sind Text-Einblendungen** als Bauchbinde im unteren Drittel:
`scene` ist die Szenennummer ab 1, `at` die Sekunden nach Szenenbeginn
(Standard 0.6), `dur` die Dauer (Standard: bis kurz vor Szenenende, hoechstens
sieben Sekunden), `sub` ist optional. Dafuer braucht es Pillow und eine Schrift
im System; fehlt eines von beiden, wird die Einblendung uebersprungen und der
Film trotzdem fertig — mit einem Hinweis am Ende.

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
- jede Szene dauert so lange wie ihre laengere Haelfte. Ein zu kurzer Clip wird
  **gestreckt und interpoliert**: `setpts` verlangsamt, `minterpolate` rechnet
  aus zwei echten Bildern das Bild dazwischen. Deshalb ruckelt nichts. Mit dem
  framerate-Filter auf eine andere Bildrate zu gehen wuerde einzelne Bilder
  verdoppeln, und genau das sieht man als Stottern. Der Eigenton des Clips wird
  mitgestreckt, sonst endet er mitten in der Szene. Eine kurze Sprecherspur
  bekommt Stille dahinter
- **alle Szenen bekommen dieselbe Groesse und Bildrate**, die des ersten Clips.
  Clips verschiedener Modelle haben verschiedene Bildraten, und ohne diesen
  Schritt kann der zweite Durchlauf nicht kopieren
- bei einer Standbild-Szene faehrt die Kamera **subpixelgenau** ueber das Bild,
  und das Bild wird vorher mit Lanczos passend verkleinert. ffmpeg-zoompan
  rechnet in ganzen Pixeln, da springt die Fahrt sichtbar, und feine Strukturen
  flimmern
- **alle Sprecheraufnahmen werden auf denselben Pegel gebracht** (-16 LUFS) —
  ohne das springt die Lautstaerke von Szene zu Szene
- die Musik wird gedrueckt, solange gesprochen wird: **die Stimme ist immer
  lauter als die Musik**, und in den Pausen kommt die Musik von selbst zurueck
- der Originalton der Clips bleibt leise darunter (10 %) statt stumm
- Untertitel entstehen aus den Szenentexten und den **gemessenen** Laengen, sind
  also zwangslaeufig synchron
- die Musik blendet am Ende ueber zwei Sekunden aus

**Dauer: ungefaehr eine bis zwei Minuten je Szene**, weil jedes Zwischenbild
gerechnet wird. Acht Szenen sind also gut eine Viertelstunde — deutlich laenger
als vor 11.2026, und das ist der Preis dafuer, dass nichts mehr stottert.
**Den Befehl im Hintergrund starten**, nicht im Vordergrund warten, und solange
nichts anderes am Film tun.

Das Skript meldet je Szene die Laenge, den Streckfaktor und ob interpoliert
wurde, und sammelt am Ende alle Hinweise, die das Ergebnis betreffen — ein
Streckfaktor ueber x1.5 steht dort. Zwischendateien liegen im Unterordner
`_schnitt` und koennen danach weg.

### Wenn es scheitert

Das Skript nennt den Durchlauf und die letzte ffmpeg-Meldung. Die drei
haeufigsten Faelle:

| Meldung | Ursache |
|---|---|
| `ffmpeg nicht gefunden` | Step 0 uebersprungen. Nachinstallieren, nachfragen |
| `Clip ... nicht gefunden` | `fetch` lief nicht, oder im Manifest stehen noch URLs |
| `Laenge von ... nicht lesbar` | Download abgebrochen, Datei halb. Nochmal `fetch` |
| `... braucht Pillow` | Standbild-Szene oder Einblendung, aber Pillow fehlt. `python -m pip install pillow`, vorher fragen |
| `motion "..." gibt es nicht` | Tippfehler. Erlaubt sind zoom_in, zoom_out, pan_left, pan_right, pan_up, pan_down, none |
| Hinweis `x2.4 gestreckt` | Kein Fehler, der Film ist fertig — aber diese Szene laeuft in Zeitlupe. Clip laenger neu erzeugen oder Szene teilen, dann nur neu schneiden (kostet nichts) |

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
  schneiden — mit eingebrannten Untertiteln statt einer .srt, mit anderer
  Musiklautstaerke, mit Text-Einblendungen, oder nachdem eine zu knapp
  bestellte Szene durch einen laengeren Clip ersetzt wurde — ohne ein einziges
  Credit.
- **Die Gesamtkosten nennen**: was verbraucht wurde und was bleibt
- **Die 24-Stunden-Warnung**: Stimme und Musik verschwinden auf dem Server
  nach 24 Stunden. Nach `fetch` liegt alles lokal, die Warnung ist damit
  abgehakt — sag aber, dass die URLs selbst bald ins Leere zeigen. Die Clips
  bleiben laenger: die neuesten 50 Filme dauerhaft, der Rest 30 Tage mit
  Vorwarnung per Mail

---

## Was nicht geht

- **Kein Ton aus dem Videomodell steuerbar** — die Clips bringen eigene
  Umgebungsgeraeusche mit, die nur leiser oder stumm gestellt werden koennen.
  Bei `gemini-omni-flash` kommt der Ton immer, manchmal mit Sprache oder Musik:
  dort pro Szene `originalVolume: 0` setzen
- **Lippensynchronitaet nur auf den H3-Modellen** und nur in einer eigenen
  Szene: Portrait plus Sprecherspur ueber `mode = "reference"`, Ablauf in
  **kim-video**, Step V0.6. In den aus Szenenbildern animierten Clips bewegen
  sich keine Lippen passend zum Text
- **Keine exakte Szenenlaenge ueber 15 Sekunden**
- **Kein Text im Bild aus dem Modell** — Schrift in generierten Clips wird oft
  falsch. Titel und Beschriftungen gehoeren in die Untertitel oder in den Block
  `overlays` des Manifests, der sie beim Schnitt als saubere Bauchbinde ins Bild
  legt. Wo etwas gelesen werden soll, ist ein Standbild mit Kamerafahrt dem
  animierten Clip ohnehin vorzuziehen
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
