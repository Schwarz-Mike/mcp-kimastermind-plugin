---
name: kim-avatar
description: "Use when the user wants a talking person on video -- UGC reel, avatar, presenter, testimonial look, 'a person speaks into the camera', Mundart / Swiss German reel, lip sync with their own voice, talking head. Triggers: UGC-Reel, Avatar, Sprecher, Person spricht in die Kamera, Talking Head, Mundart-Reel, Schweizerdeutsch, Lip-Sync mit eigener Stimme, sprechendes Foto, Foto von mir sprechen lassen. Covers TWO ways and makes the user choose: (A) UGC with gemini-omni-flash (the voice is made INSIDE the clip, no lip sync to a given audio), (B) lip sync with omnihuman-1.5 or minimax-h3* (a given voice plus a photo). Includes the start-image recipe, cutting, subtitles, the checks before delivery, and fetching slow jobs and finished clips. For a plain clip without a speaking person use kim-video, for speech alone kim-voice. Provider names are never mentioned."
version: 1.0.0
---

# kim-avatar -- sprechende Personen als Video

## Purpose

Eine Person spricht in die Kamera: ein UGC-Reel, ein Avatar, ein Testimonial-Look, ein
Foto des Nutzers, das zu seiner eigenen Stimme spricht. Alle Clips kommen von
`https://mcp.kimastermind.net/vid/`. Anbieternamen werden NIE genannt; die **Modelle** duerfen
und muessen genannt werden, denn der Nutzer waehlt eines.

## Zuerst: Weg UND Modell mit dem Nutzer waehlen -- immer fragen

Es gibt zwei Wege, und sie koennen **Verschiedenes**. Waehle nie still, und nimm kein Modell,
nur weil es das Standardmodell des Werkzeugs ist.

1. **Fragen, welcher Weg** (Tabelle unten), mit einer Empfehlung und einem Satz Grund.
2. **Die Optionen erklaeren**: was jedes kann, was nicht, was es kostet, wie lange es dauert.
3. **Sagen, was ausscheidet.** Will der Nutzer eine vorgegebene Stimme (eigene Aufnahme,
   Voiceover), faellt Weg A aus, weil `gemini-omni-flash` keine Tonspur annimmt. Will er
   Mundart per Text, faellt Weg B aus.
4. Erst dann Kosten und Wartezeit nennen und starten.

Ein Modell, das der Nutzer schon genannt hat, bleibt gesetzt; passt es nicht zum Auftrag (Lip-Sync
auf `gemini-omni-flash`), sag das und biete ein passendes an.

| | A) UGC mit `gemini-omni-flash` | B) Lip-Sync mit `omnihuman-1.5` / `minimax-h3*` |
|---|---|---|
| Stimme | entsteht IM Clip (aus Startbild + Prompt), nicht steuerbar | kommt von mir (`voice_generate`, eigener Stimmklon, eigene Aufnahme) |
| Dialekt (z. B. Aargauer Mundart) | ja, ueber den Prompt | nur wenn das Audio schon Mundart ist |
| Person | Startbild (Frau/Mann im Raum), meist KI-erzeugt | Foto einer echten Person (z. B. der Nutzer selbst) |
| Eigenes Audio hochladen | **NEIN** | ja |
| Lip-Sync auf gegebenes Audio | **NEIN** | ja |
| Laenge | 3 bis 15 s pro Clip | OmniHuman: Audio **unter 13 s**; H3: Audio 2 bis 15 s |
| Kosten (gegen `list_models` pruefen) | 7 Credits/s in 720p, 2,3 in 360p (Entwurf) | OmniHuman 16 Credits/s der Tonspur; H3 Lite 4, Highspeed 6, H3 7,6 |
| Wartezeit | Sekunden bis wenige Minuten | OmniHuman 30 bis 60 s Rechenzeit **je Sekunde Video**, laeuft als Auftrag |

Vorab dem Nutzer sagen: Kosten pro Sekunde und Wartezeit (siehe unten). **Nie denselben Clip
erneut starten, solange ein Job laeuft** -- das wird doppelt berechnet.

**Noch offen:** welches Modell das *natuerlichere* Gesicht macht, ist nicht verglichen, und dazu gibt
es hier keine Behauptung. Bei Unsicherheit der Vorschlag: dasselbe Foto mit derselben Tonspur auf
`minimax-h3-lite` und auf `omnihuman-1.5` (bei 4 Sekunden zusammen rund 80 Credits) und selbst
vergleichen lassen.

---

## Weg A -- UGC-Reel mit gemini-omni-flash

### Harte Grenzen (so festhalten, nicht versprechen, was nicht geht)
- **Kein Lip-Sync zu vorgegebenem Audio, kein Audio-Upload, keine Referenzvideos.** Der Clip bringt
  seinen eigenen Ton mit (Stimme, Atmo), er laesst sich nicht abschalten.
- Nur 9:16 und 16:9. Im Modus `image` folgt das Format dem Startbild (Hochformat = 9:16),
  `aspect_ratio` wird ignoriert. Gemessen: ein Hochformat-Foto, als 16:9 angefordert, wird
  **neu gemalt** (anderer Hintergrund, anderes Bild).
- Kein Seed: jede Generierung klingt etwas anders. Reproduzierbarkeit gibt es nicht.
- 720p ist die ehrliche Wahl; 1080p und 4K sind nur hochgerechnet (1,5-faches und 3-faches des
  Preises, kein Detailgewinn). 360p ist der billige Entwurf.
- Zwei Bilder im Modus `image` (Start- und Schlussbild) begrenzen den Clip auf 10 s.

### Stimme konsistent halten
Die Stimme wird aus **Person im Startbild + Sprechstil im Prompt** abgeleitet. Fuer dieselbe Stimme
ueber mehrere Clips:
- identisches Startbild fuer alle Clips,
- identische Stimm-/Stilbeschreibung am Prompt-Anfang (Alter, Tonlage, Tempo, Waerme, Dialekt),
- Clips derselben Szene hintereinander generieren.
Trotzdem kommen selten leichte Abweichungen vor (vor allem zwischen verschiedenen Modellen, z. B.
H3 gegen Omni Flash) -> bei Auffaelligkeit neu generieren.

### Clip-Laenge und Text
- **Immer 15 s generieren**, auch wenn der Text kuerzer waere. Zu kurze Clips (12 s) schneiden die
  letzten Woerter ab. Das kostet in 720p rund 104 Credits je Clip; als Entwurf in 360p rund 35.
- Pro Clip ca. 2 Saetze / 35 bis 45 gesprochene Woerter. Laengere Reels = 2 Clips (je 15 s) und
  schneiden.
- Keinen Markennamen/Plattformnamen in den Text, den das Modell verstuemmelt (Beispiel: "Instagram"
  wurde zerhackt -> weglassen, "Social Media" sagen lassen). Schwierige Fremdwoerter vorher testen.

### Startbild fuer UGC: so sieht es nach "selbst gedreht" aus
Das Startbild entscheidet ueber Look, Stimme und Glaubwuerdigkeit des ganzen Clips. Es muss wie ein
echtes Handy-Selfie wirken, nicht wie ein Studiofoto. Mit `generate_image` erzeugen (empfohlen:
`gpt-image-2.5-flare` oder `-sunburst`, Hochformat `9:16` oder `2:3`, quality high; eine Variante mit
Referenzbild, wenn Person oder Raum feststehen sollen). **Ein Startbild des Nutzers hat Vorrang: wenn er
eines liefert, dieses unveraendert verwenden.** Das Modell fuer das Bild wird ebenfalls mit dem Nutzer
gewaehlt (kim-images, Bildmodelle unterscheiden sich im Preis).

**Prompt-Bausteine fuer den Selfie-Look**
- Kamera: "front-camera smartphone selfie, shot on iPhone, arm's length, slightly wide-angle, vertical 9:16".
- Licht: "natural window light / ordinary room light, slightly uneven, no studio lighting, no softbox, no cinematic grading".
- Realismus: "real skin texture, visible pores, slight imperfections, flyaway hairs, no retouching, no beauty filter, no plastic skin".
- Komposition: Person leicht aussermittig, Kopf + Schultern + Oberkoerper bis Brust, Kamera auf
  Augenhoehe oder minimal darunter, Blick **in die Linse**, Raum im Hintergrund leicht unaufgeraeumt und
  lebendig (Regal, Pflanze, Behandlungsraum, Kueche), Hintergrund leicht unscharf wie bei Handykameras.
- Ausdruck: **entspannt, Mund geschlossen oder nur ganz leicht offen, freundlicher Blick**, kein breites
  Lachen und kein Zahnlaecheln (das Startbild praegt den Mundausdruck des ganzen Clips; Lachen wirkt spaeter starr).
- Kleidung: alltaeglich, ohne Logos und Text (sonst entstehen verzerrte Schriften).
- Haende: tief oder aus dem Bild, nicht in Posen (Haende sind im Bild oft fehlerhaft; Gesten entstehen erst im Video).
- Verbote in den Prompt: "no text, no watermark, no logo, no ring light, no professional microphone, no studio backdrop, no perfect symmetry".

**Beispiel-Prompt**
"Authentic front-camera smartphone selfie of a friendly woman in her late 30s, brown shoulder-length hair,
casual cardigan, sitting in a bright therapy practice room with a plant and bookshelf behind her, natural
window light, slightly uneven exposure, real skin texture with pores, no retouching, relaxed neutral
expression with a faint kind smile, mouth closed, looking straight into the lens, head and upper body,
slightly off-center, vertical 9:16, shot on iPhone, shallow depth of field, no text, no logo, no watermark."

**Checkliste vor dem Video**
1. Gesicht scharf, Augen schauen in die Kamera, Mund neutral, keine verzerrten Haende/Zaehne/Ohrringe.
2. Kein Text im Bild, keine Logos auf der Kleidung.
3. Raum passt zum Angebot (Praxis, Buero, Wohnzimmer) und wirkt bewohnt.
4. Bildformat Hochformat; fuer Omni Flash bestimmt das Bild das Videoformat.
5. Mehrere Varianten (2 bis 3) erzeugen und die natuerlichste waehlen; **dasselbe Bild fuer alle Clips
   eines Reels** verwenden (Stimme und Aussehen bleiben konsistent).
6. Wirkt es zu glatt oder KI-haft: "less polished, more casual, slight motion blur, imperfect framing"
   ergaenzen und neu erzeugen.

Ehrlichkeit: Die Person ist KI-generiert. Nicht als echte Kundin ausgeben (siehe Ethik).

### Prompt-Aufbau (UGC, Selfie-Stil)
1. Stil: "Authentic selfie-style UGC, handheld, vertical, natural light, real person, no studio look".
2. Person + Ort wie im Startbild (nicht umdeuten).
3. **Stimme + Dialekt explizit**, z. B. "Speaks in authentic Swiss German, Aargau dialect (Aargauer
   Mundart), warm, natural, not Standard German, not Zurich dialect". Den gesprochenen Text **in
   Mundart-Schreibweise woertlich** in den Prompt schreiben.
4. **Zeitstrahl mit Gestik und Mimik** (0-3 s, 3-6 s, ..., 12-15 s): Blick in die Kamera, Augenbrauen,
   Laecheln, offene Handgeste, Zeigen nach unten ("Klick unten"), Kopfnicken. Gestik konkret beschreiben,
   nicht nur "natuerlich".
5. Kein Text, kein Untertitel, kein Logo im Bild generieren lassen (kommt spaeter im Schnitt).
6. Am Schluss ruhiger Abschluss ohne zusaetzliche Woerter ("ends speaking, no extra words").
Der Text des Nutzers gilt woertlich: nicht umformulieren oder kuerzen. Liefert der Nutzer einen Prompt,
diesen verwenden und nur ergaenzen.

### Typische Fehler und Gegenmittel
| Fehler | Gegenmittel |
|---|---|
| Letzte Woerter fehlen | 15 s statt 12 s; Text kuerzen |
| Zusatzwoerter ("komm damit"), gedehntes "und" | neu generieren oder die Stelle im Schnitt entfernen |
| Verstuemmelter Eigenname (Instagram) | Wort aus dem Text streichen |
| Dauerton / "Ding" in Sprechpausen | Pause wegschneiden und ueberblenden (siehe Schnitt); per Spektrogramm pruefen |
| Dialekt zu "hochdeutsch" | Text in Mundart schreiben, Dialekt im Prompt doppelt nennen, Zuercher Woerter vermeiden |
| Der Chat meldet einen Timeout, kein Clip | Der Clip kann fertig sein: `my_gallery` mit `kind: "videos"` ansehen, **nicht neu erzeugen** |
| "rejected by the content safety filter" | Es wurde nichts abgebucht. Prompt umformulieren oder anderes Startbild (ein Foto einer Person ist der haeufigste Ausloeser) |

### Schnitt (ffmpeg) -- saubere Uebergaenge
Braucht FFmpeg auf dem Rechner des Nutzers (Pruefung und Installation: **kim-video**, Step L1, nie
stillschweigend installieren). Wenn zwei Clips zu einem Reel werden oder eine Pause raus muss:
- Videos vor `xfade` normalisieren: `fps=30,settb=AVTB,setpts=PTS-STARTPTS` (sonst Timebase-Fehler).
- Bild: `xfade=transition=fade:duration=0.25-0.4:offset=<Schnittpunkt>`.
- Ton parallel: `acrossfade=d=0.4`; bei einem Pausenschnitt `atrim` vorher/nachher, `apad`, concat.
  Ton-Schnitt auf Wortenden setzen.
- Schnittpunkte per Wort-Zeitstempeln finden (siehe Pruefen). Pausen ueber ca. 0,8 s kuerzen, "Ding"
  oder Dauerton komplett entfernen.
- Zielwerte, die gut funktioniert haben: Cross-Fade 0,4 s zwischen Clip 1 und 2; Pausenschnitt mit 0,25 s Blende.

### Logo einblenden (nur wenn ein Markenname gesagt wird)
- Das Logo erscheint, **wenn die Person den Markennamen sagt** (Zeitstempel aus Whisper), nicht fix.
- **Unterhalb des Gesichts**, nie ueber dem Gesicht. Mitte, Breite ca. 200 px bei 1080 px Video,
  Position y ca. 850 (bei 1080x1920).
- Sanft ein- und ausblenden (Alpha-Fade 0,3 s), darf ruhig laenger stehen (ca. 3 s und mehr).
- Overlay per `overlay` mit `fade=t=in:alpha=1` / `fade=t=out:alpha=1`, `enable='between(t,a,b)'`.

### Untertitel -- perfekte Hochdeutsch-Untertitel zur Mundart
- **Hochdeutsch** (auch wenn Mundart gesprochen wird), im **unteren Drittel**.
- ASS-Datei, per `subtitles`-Filter einbrennen. Schrift: Inter Bold (`fontsdir` zeigt auf den
  Schriftordner; der Pfad haengt vom System ab, z. B. `/usr/share/fonts/opentype/inter` unter Linux),
  Groesse ca. 46 bei 1080x1920, weisse Schrift, dunkle Outline/Schatten, MarginV ca. 85, zentriert.
  Fehlt die Schrift, eine vorhandene Fettschrift nehmen und es sagen.
- Max. 2 Zeilen, ca. 4 bis 7 Woerter pro Einblendung, Wechsel an Satz-/Sinngrenzen.
- **Timing aus Whisper-Wortzeitstempeln**, nicht schaetzen. Untertitel duerfen nicht im Gesicht oder im
  Logo-Bereich liegen.
- Sinngemaess uebersetzen, nicht Wort fuer Wort ("Hesch du dich su scho gfoget" -> "Hast du dich auch schon gefragt").

### Pruefen (vor Lieferung, immer)
1. **Wort-Zeitstempel**: `faster-whisper` (small, CPU, `language="de"`). Bei einem `av`-Fehler
   (`metadata_errors`) keinen Dateipfad uebergeben, sondern die WAV mit numpy dekodieren und das Array
   uebergeben. Damit fehlende oder abgeschnittene Endwoerter und Zusatzwoerter finden. Ist
   `faster-whisper` nicht installiert, dem Nutzer das sagen und fragen, ob es installiert werden darf
   (`pip install faster-whisper`); nicht still weglassen und nicht schaetzen.
2. **Stille/Einsaetze**: `ffmpeg -af silencedetect` fuer Pausenlaengen.
3. **Tonartefakte**: Spektrogramm (`showspectrumpic`) auf Dauertoene in Pausen.
4. **Standbilder** (Contact Sheet, ein Bild alle 1 bis 1,5 s) auf Gesicht, Logo-Position, Untertitel.
5. Laenge, Format 9:16, Bitrate pruefen; das Ergebnis dem Nutzer schicken und Fehler offen benennen.

### Ethik / Plattform
UGC-Optik mit einer KI-Person ist als **Direktansprache** in Ordnung. **Keine erfundenen Kundenmeinungen,
keine falschen Erfolgsversprechen, keine echten Personen imitieren**, nichts als echtes Testimonial
ausgeben. Textformulierungen ehrlich halten ("Mach jetzt die erste Lektion gratis", nicht "Ich habe damit
10'000 Euro verdient"). Die Kennzeichnungsregeln der Plattform fuer KI-erzeugte Inhalte gelten; den Nutzer
darauf hinweisen, bevor er veroeffentlicht.

### Kosten / Wartezeit
`gemini-omni-flash`: je nach Laenge Sekunden bis wenige Minuten (ein 3-Sekunden-Clip in 360p kam in unter
20 s, ein 15-Sekunden-Clip in 720p braucht eher Minuten). Preis pro Sekunde ueber `list_models`
pruefen und **vor dem Start** nennen.

---

## Weg B -- Lip-Sync (omnihuman-1.5 oder minimax-h3*)

Einsatz: eine **echte Person** (Foto des Nutzers) mit einer **gegebenen Stimme** (`voice_generate`, ein eigener
Stimmklon, eine eigene Aufnahme).

**Zuerst: Die Person darf auf das Video.** Nur das eigene Foto oder das einer Person, die zugestimmt hat. Kein
Foto einer fremden Person nehmen, um sie etwas sagen zu lassen.

### Ablauf
1. **Foto vorbereiten**: Gesicht klar sichtbar, frontal, Blick in die Kamera. Das Foto bestimmt den
   Gesichtsausdruck des ganzen Clips: **ein breit lachendes Foto -> der Mund bleibt "laechelnd" und wirkt
   unnatuerlich**. Besser: neutraler, leicht freundlicher, geschlossener Mund, Oberkoerper, naeher an der Kamera,
   Haende unten. Bei Bedarf das Foto vorher mit `generate_image` anpassen (z. B. `gpt-image-2.5-flare`,
   Referenz = Originalfoto, "same man, closer framing, neutral closed mouth, hands low", 2:3, quality high).
   Ergebnis: eine Bild-URL aus der Galerie. Das Bild **muss eine Person klar zeigen**: ein Bild ohne erkennbare
   Person wird nicht abgelehnt, aber trotzdem berechnet.
2. **Stimme erzeugen**:
   - `voice_generate` (Express/Studio) -> spricht **Hochdeutsch**, kein Mundart. Die Engine waehlt der Nutzer
     (kim-voice).
   - Ein eigener Stimmklon aus einem anderen Sprachwerkzeug des Nutzers -> Audio herunterladen.
   - Eine eigene Aufnahme -> der einzige Weg zu Mundart auf Weg B. **Das Modell veraendert keine Stimme**, es
     animiert nur den Mund zu einer vorhandenen: "mein Foto, meine Stimme" geht, "mein Foto, eine andere Stimme"
     heisst, diese Stimme vorher zu erzeugen.
3. **Audio auf mcp.kimastermind.net hosten**: `request_upload_url(kind="audio")` -> `PUT` der Datei
   (`curl -X PUT -H "Content-Type: audio/mpeg" --data-binary @datei.mp3 "<upload_url>"`) -> die
   zurueckgegebene `ref_url` verwenden. Externe URLs werden abgelehnt. Das Gleiche gilt fuer Bilder
   (`kind="image"`) und Videos (`kind="video"`).
4. **Laenge pruefen**: OmniHuman nimmt nur Audio **unter 13 s** (z. B. mit `ffprobe` messen; eine Spur ab 13 s wird
   abgelehnt, bevor etwas abgebucht wird). Zu lange Texte in Teile unter 13 s schneiden, einzeln erzeugen und per
   ffmpeg verbinden (Bild, Kleidung, Position identisch lassen).
5. **Dem Nutzer vorher sagen**: Kosten **16 Credits je Sekunde der Tonspur** (9 s = 144), Rechenzeit **30 bis 60
   Sekunden je Sekunde Video** (gemessen: 9 s Video in 4 Min 27 s, 4 s in knapp 3 Min). Dann starten.
6. **Generieren**: `generate_video(model="omnihuman-1.5", mode="reference", reference_images=[<ein Foto>],
   reference_audios=[<eine Stimme>], prompt=...)`. Genau **ein** Bild und **ein** Audio, sonst nichts. Kein
   `duration` (die Laenge ist die der Tonspur), kein `quality`, kein `aspect_ratio` (das Format folgt dem Bild).
7. **Abholen**: siehe "Jobs & Galerie".

### Prompt (optional, steuert Szene und Mimik)
Englisch, kurz: "The man speaks directly to the camera, warm, friendly and calm. Natural lip-sync, relaxed
face, subtle eyebrow movement, slight natural head movement, small natural hand gestures, calm confident
posture." Bei einem lachenden Foto zusaetzlich "no exaggerated smile".

**Mehrere Personen im Bild: nicht empfohlen.** Gemessen bewegen sich alle, der Zuhoerer reagiert, aber auch sein
Mund bewegt sich mit. Eine eigene Stimme je Person gibt es nicht: es bleibt EIN Bild und EINE Tonspur.

### minimax-h3 / -lite / -highspeed
Modus `reference`, das Portraet in `reference_images`, die Sprache in `reference_audios` (1 bis 3 Spuren, je 2
bis 15 s, nur auf mcp.kimastermind.net gehostet). Auch Videobearbeitung (Charakter, Outfit, Hintergrund tauschen)
ueber `reference_videos` (2 bis 15 s; bei `minimax-h3` werden die Sekunden der Referenzvideos mitberechnet).
Preise und Aufloesungen (768p/2k, Lite 480p/768p, Highspeed nur 768p) ueber `list_models`.
Fuer Mundart muss das Audio selbst Mundart sein (eigene Aufnahme); Omni Flash ist der einzige Weg, Mundart per
Text zu bekommen, dafuer ohne Lip-Sync-Kontrolle.

### Welche Variante waehlen?
- Echte Person + Hochdeutsch-Stimme oder eigener Stimmklon -> OmniHuman (kurz, unter 13 s) oder H3. OmniHuman kostet
  das Zwei- bis Sechsfache einer H3-Variante (16 gegen 4 bis 7,6 Credits/s); ein Qualitaetsvorsprung ist nicht
  belegt (siehe "Noch offen").
- Laengere Lip-Sync-Clips, Videobearbeitung, mehrere Audiospuren -> H3.
- Mundart + natuerliche Gestik ohne eigene Aufnahme -> Weg A (Omni Flash).

---

## Jobs & Galerie (wichtig bei langen Jobs)

- Langsame Modelle (OmniHuman) antworten **sofort mit einer Job-ID**. Dann **`video_status(job_id)` alle 60 bis
  90 s** aufrufen, bis die Clip-URL kommt. Schlaegt der Job fehl, werden die Credits erstattet.
- **Nie erneut `generate_video` fuer denselben Clip** (doppelte Abbuchung). Ein Timeout beim Aufruf heisst nicht,
  dass der Job fehlgeschlagen ist: Credits koennen schon abgebucht sein.
- Fertige Clips stehen in **`my_gallery`** mit `kind: "videos"` (URL `https://mcp.kimastermind.net/vid/<id>.mp4`,
  Modell, Laenge, Datum, neueste oben). Das ist der Weg, wenn die Job-ID verloren ist oder der Chat geschlossen
  wurde. `kind: "images"` zeigt Bilder (unter `.../img/...`), `kind: "audio"` erzeugte Sprachclips (nur 24 Stunden).
  Ein Video, das noch laeuft, steht dort noch nicht: dafuer `video_status`.
- `my_credits` vor teuren Jobs pruefen und das Guthaben nennen.
- Referenzdateien (Bild/Audio/Video) liegen unter `.../img/ref/<user>/<id>.jpg` und `.../ref/<user>/<id>.mp3`;
  Upload-Links sind **einmalig und nur kurz gueltig** (ca. 5 Minuten). Dateien bleiben als Richtwert etwa 30 Tage;
  `voice_generate`-Links laufen nach 24 h ab -> sofort herunterladen.

## Auslieferung
- Den Clip per `curl` herunterladen, mit `ffprobe` (Dauer, Aufloesung, Audio) und Contact Sheet pruefen, dann dem
  Nutzer als Datei schicken, plus URL.
- Fuer einen Meta-Ads-Upload: 9:16, H.264/AAC, Dateien in der Regel unter 100 MB; Untertitel einbrennen (Ton aus
  ist ueblich).
- Kurz und ehrlich berichten: was gut ist, was nicht. Lippensynchronitaet laesst sich an einem Standbild nicht
  beurteilen: das sagen.

## Related Skills -- die KIM-Familie

| Skill | Wofuer |
|---|---|
| **kim-avatar** (dieser) | Eine sprechende Person: UGC-Reel, Talking Head, Foto mit eigener Stimme |
| **kim-video** | Videoclips ohne sprechende Person, Clip-Bearbeitung, Schnitt lokal mit FFmpeg |
| **kim-voice** | Die Stimme: Text vorlesen, zwei Engines zur Wahl |
| **kim-images** | Das Startbild und das Foto: erzeugen, anpassen, mehrere Varianten |
| **kim-lernfilm** | Ein ganzer Film aus mehreren Szenen mit Sprecher, Musik und Untertiteln |

## Sprache und Ton
- Du-Form, deutsch (ausser der Nutzer schreibt anders), kurz und direkt.
- Modellnamen duerfen genannt werden. **Nicht genannt werden der Anbieter, die Endpunkte und was wir selbst
  zahlen.** Den ganzen Dienst nennst du den **Video-Generator**.
- Preise in Credits, nie in Franken oder Dollar eines Anbieters.
