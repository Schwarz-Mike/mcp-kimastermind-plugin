---
name: kim-music
description: Use whenever the user wants music, a soundtrack, background music or a musical bed generated. Triggers: mach Musik, generiere Musik, Hintergrundmusik, Musik fuer mein Video, Soundtrack, Jingle, Intro-Musik, Begleitmusik, Musikbett, Lounge-Musik, Entspannungsmusik, make music, background music, soundtrack, generate music, music for my video. Asks what the music is FOR, picks the engine from that, turns the answer into the ENGLISH prompt the engines require, states balance and exact cost before generating, then plays the result. THREE engines that differ in LENGTH and in whether they can sing, not in quality: Pro delivers the exact length that is asked for, from 10 seconds to 5 minutes; Advanced sings but its length follows the description; Basic is instrumental only and fixed at 33 seconds. For noises use kim-sfx, for speech kim-voice, for video kim-video, for still images kim-images. Provider and model names are never mentioned.
version: 2.2.0
---

# KIM Music Skill

## Purpose

Generate music with the KIMASTERMIND MCP tools. The capability is called the
**Musik-Generator**. Output is an MP3, available for **24 hours**, exactly like
generated speech.

What makes this skill worth having is two things the user should never have to
deal with:

1. **The engines only accept English.** The user describes the music in German
   and never sees the prompt. Naming instruments and tempo changes the result
   far more than any adjective — that translation is this skill's actual job.
   Never ask the user to write English.
2. **The three engines differ in LENGTH, not in quality.** Picking by "which is
   the best one" is picking wrong. Picking by what the music is for is picking
   right, every time.

---

## Three engines. The difference is length and vocals.

| Engine | Gesang | Laenge | Wartezeit | Credits |
|---|---|---|---|---|
| **Mastermind Music Pro** (`pro`) | **ja** | **exakt wie bestellt, 10 Sek bis 5 Min** | ~15-25 Sek | **10 pro Minute** |
| **Mastermind Music Advanced** (`song`) | **ja**, mit Text und Zeitmarken | 1 bis 3 Min, **folgt der Beschreibung** | ~20-30 Sek | **16 pro Stueck** |
| **Mastermind Music Basic** (`score`) | **nein, nur instrumental** | **fest 33 Sek** | ~25-30 Sek | **6 pro Stueck** |

Alles gemessen am 14.10.2026, nicht aus einem Datenblatt abgeschrieben.

### Welche nehmen

**Frag nicht „welche Engine?", frag „wofuer ist die Musik?"** — danach ist die
Wahl eindeutig:

- **Die Musik muss unter etwas Fertiges passen** (Video, Meditation, Podcast-
  Intro von genau 20 Sekunden) → **Pro**. Sie ist die einzige, bei der 90
  Sekunden bestellt auch 90 Sekunden geliefert heisst (gemessen: 180 bestellt →
  180,04 geliefert, 300 → 300,04). Nichts muss geschnitten oder geloopt werden,
  und das Stueck endet dort, wo der Film endet. Das klingt komponiert.
- **Ein langes Bett, das sowieso geloopt wird** (Meditation, Hoerbuch,
  Hintergrund fuer eine halbe Stunde) → **Advanced**. Es ist mit Abstand das
  guenstigste pro Sekunde, und ob das Stueck 150 oder 178 Sekunden lang wird,
  ist beim Loopen gleichgueltig.
- **Ein Lied mit Gesang** → **Advanced** oder **Pro**. Advanced gibt den
  gesungenen Text mit Sekundenmarken zurueck, was eine fertige Untertitelspur
  ist; das kann Pro nicht.
- **Advanced faellt aus** → **Basic** laeuft auf einem anderen Zugang und ist
  dann noch da.

**Was eine Minute Musik wirklich kostet** — danach entscheidet sich fast jede
Frage nach dem Preis:

| Engine | Rechnung | pro Sekunde |
|---|---|---|
| **Advanced** | 16 Credits fuer rund 165 Sekunden | **0,10** |
| **Pro** | 10 Credits je Minute | **0,17** |
| **Basic** | 6 Credits fuer 33 Sekunden | **0,18** |

Advanced ist also das guenstigste Material, Pro der Aufschlag fuer eine Laenge,
die genau stimmt, und Basic liegt bewusst gleichauf mit Pro.

**Dass Basic billig aussieht, ist kein Grund, es zu empfehlen.** Sechs Credits
sind wenig, aber es sind sechs Credits fuer 33 Sekunden ohne Gesang und ohne
jede Einstellmoeglichkeit — pro Sekunde zahlst du dasselbe wie bei Pro und
bekommst weniger. Der niedrige Preis ist dafuer da, dass ein Ausfall der anderen
Engines auf der Rechnung nicht auffaellt, nicht als Kaufargument. Empfiehl Basic
weiterhin nur, wenn Advanced nicht verfuegbar ist.

### Die Laenge, Engine fuer Engine

- **Pro** nimmt `seconds` und haelt sich daran. 10 bis 300.
- **Advanced** hat **keine Laengenangabe**. Die Laenge ergibt sich aus der
  Beschreibung — und das Wort „short" darin wirkt wie eine Dauer: dieselbe
  Engine lieferte 61 Sekunden auf einen Prompt mit „a short calm instrumental
  test tone" und 148 bis 178 Sekunden auf gewoehnliche Prompts. Wer drei Minuten
  will, schreibt also nichts von „kurz"; wer eine Minute will, nimmt Pro.
- **Basic** ist bei 32,8 Sekunden hart gedeckelt. Vier Wege, mehr zu verlangen,
  wurden alle ignoriert.

**Quote die Laenge, die das Werkzeug zurueckmeldet**, nie eine runde Zahl — sie
wird an der Datei gemessen.

### Laenger als die Engine kann

**Nicht mehrere Stuecke generieren.** Zwei Stuecke aus demselben Prompt sind
zwei verschiedene Kompositionen, und die Naht ist hoerbar. Es gibt zwei richtige
Wege:

1. **Pro mit der gewuenschten Laenge** — bis fuenf Minuten am Stueck.
2. **Ein Stueck erzeugen und loopen.** `audio_assemble` und `film_assemble`
   legen eine Spur beliebig lang unter alles andere und wiederholen sie dabei.
   Loopen kostet nichts. Fuer Ambient und Flaechen faellt eine Schleife nicht
   auf; fuer ein Stueck mit klarem Anfang und Ende schon — dann Pro.

`clips` gibt es nur bei den beiden festen Engines (Basic bis 4, Advanced bis 2)
und ist fast nie die richtige Antwort.

---

## Available MCP Commands

- `music_generate` — `prompt` (REQUIRED, **English**), `engine`
  (`pro` | `song` | `score`), `seconds` (10-300, **nur `pro` beachtet das**),
  `clips` (nur bei den festen Engines), `negative_prompt` (English), `seed`
- `my_credits` — Guthaben. **Vor jeder Generierung aufrufen**; eine Zahl von
  weiter oben im Gespraech ist veraltet
- `list_models` — alle Engines mit Credits und Laengen. Die Saetze liegen in der
  Datenbank und koennen sich aendern; diese Tabelle hier kann veralten
- `audio_assemble` — mischt Musik unter Sprache und loopt sie dabei
- `film_assemble` — dasselbe fuer ein Video

Login: https://mcp.kimastermind.net/login

---

## Die Fragen

Ask only what the user has not already said, and **ask everything open in one
message**. Someone who writes „ruhige Klaviermusik fuer ein Meditationsvideo von
zehn Minuten" has answered all of it — frag nichts, nenne die Kosten, generiere.

**1. Wofuer ist die Musik?** Die wichtigste Frage, weil sie die Engine und die
Laenge zugleich entscheidet. „Unter ein Video von 90 Sekunden" ist eine
vollstaendige Antwort.

**2. Instrumental oder mit Gesang?** Mit Gesang **schreibt die Engine die Worte
selbst** — der Nutzer sagt, worum es geht, nicht was gesungen wird. Bringt
jemand einen eigenen Text mit, sag klar, dass sich der Text nicht vorgeben
laesst, und nenne die Loesung, die wirklich funktioniert: instrumentale Musik
plus gesprochene Stimme ueber **kim-voice**.

**3. Stilrichtung?** Ambient, Pop, Rock, Klassisch, Jazz, Lo-Fi, Folk,
Elektronisch, Orchestral — ein Startpunkt, keine Liste zum Durchsetzen.

**4. Stimmung?** ruhig, schnell, gluecklich, traurig, feierlich, spannend,
verspielt, episch.

---

## Aus den Antworten den Prompt bauen

Hier entscheidet sich, ob die Musik gut wird. Ein englischer Satz aus vier
Teilen, in dieser Reihenfolge: **Stimmung, Genre, Instrumente, Tempo** — dann
`no vocals` anhaengen, was alle Engines zuverlaessig beachten.

| Deutsch | englisches Prompt-Fragment |
|---|---|
| ruhig | calm, warm, gentle |
| entspannt / meditativ | serene, meditative, spacious |
| traurig | melancholic, wistful, minor key |
| gluecklich | uplifting, bright, optimistic |
| feierlich | solemn, dignified |
| spannend | tense, driving, suspenseful |
| verspielt | playful, light-hearted |
| episch | epic, cinematic, sweeping |
| schnell | fast tempo, energetic |
| langsam | slow tempo |
| Ambient | ambient, atmospheric pad |
| Pop | modern pop, catchy chord progression |
| Rock | rock, electric guitar, drum kit |
| Klassisch | classical, orchestral strings |
| Lo-Fi | lo-fi hip hop, soft vinyl texture |
| Jazz | jazz, brushed drums, upright bass |
| Elektronisch | electronic, synth arpeggio |

**Immer Instrumente nennen**, auch wenn der Nutzer keine genannt hat: ein Genre
allein ergibt Beliebiges. „ruhig + Klassisch" wird *gentle piano and soft
strings*, nicht bloss *classical*.

**Bei Advanced kein Wort ueber Kuerze in den Prompt**, sonst kommt ein kurzes
Stueck zurueck — siehe oben.

Zwei Beispiele:

> „ruhige Ambient-Musik fuer ein Meditationsvideo"
> → `serene ambient music, soft atmospheric pad and sparse piano, very slow tempo, no vocals`

> „fetzige Rockmusik fuers Intro"
> → `energetic rock, electric guitar riff and punchy drum kit, fast tempo, driving, no vocals`

`negative_prompt` nur gegen etwas, das der Nutzer ausdruecklich nicht will
(„ohne Schlagzeug" → `drums, percussion`). Sonst leer lassen.

**Zeig dem Nutzer auf Deutsch in einer Zeile, was du erzeugst** — nicht den
englischen String, sondern was du verstanden hast: „Ich erzeuge: ruhige
Ambient-Musik, weiches Flaechen-Pad und sparsames Klavier, sehr langsam, 90
Sekunden." Dort wird ein Missverstaendnis gefangen, bevor Credits weg sind.

---

## Kosten, bevor generiert wird

Dieselbe Regel wie bei Sprache: Kosten und Guthaben zusammen, in einem Satz,
vor dem Aufruf.

1. `my_credits` aufrufen.
2. Kosten rechnen: **Pro 10 Credits pro Minute** (90 Sek = 15, 33 Sek = 6),
   **Advanced 16 pro Stueck**, **Basic 6 pro Stueck**. Gegen `list_models`
   pruefen.
3. Sagen:

> „90 Sekunden Ambient kosten **15 Credits**. Du hast **96**, danach noch 81.
> Soll ich?"

Nicht genug Credits: die Fehlmenge exakt nennen und die kuerzere Variante
anbieten — bei Pro ist das eine echte Alternative, denn halbe Laenge ist halber
Preis.

**Die Generierung dauert 15 bis 30 Sekunden.** Sag es vorher, und brich nicht ab
und starte nicht neu, solange sie laeuft: ein zweiter Versuch bezahlt dieselbe
Musik zweimal.

---

## Die Musik ausliefern

**a) Was es gekostet hat.** `music_generate` gibt Abbuchung und neues Guthaben
zurueck. Beides weitergeben.

**b) Abspielen.** In dieser Reihenfolge, beim ersten Erfolg aufhoeren:

1. **Inline** als `data:`-URI in einem kleinen HTML-Artifact — nur das spielt im
   Chat, Audio von `mcp.kimastermind.net` ist dort blockiert. 33 Sekunden sind
   rund 800 KB, zwei Minuten rund 2 MB; ab etwa 3 MB nicht mehr inline.
2. **Systemplayer.** Herunterladen, dann dem Betriebssystem uebergeben:
   ```powershell
   $folder = "$env:USERPROFILE\Music\KI-Musik"; if (!(Test-Path $folder)) { New-Item -ItemType Directory -Path $folder | Out-Null }; $file = "$folder\AUDIO_FILENAME.mp3"; Invoke-WebRequest -Uri "AUDIO_URL_HERE" -OutFile $file; Start-Process $file
   ```
   macOS `afplay`, Linux `xdg-open`. Den Ordner nennen — Leute suchen die Datei
   spaeter.
3. **Der Link**, schlicht, mit dem Hinweis, dass er in einem neuen Tab aufgeht.

**c) Die 24-Stunden-Warnung**, jedes Mal. Weg 2 speichert die Datei schon.

**d) Bei gesungenen Stuecken den Text weitergeben.** Advanced liefert ihn mit
Sekundenmarken wie `[2.0:6.0] Oh, the world just got bigger now` — das ist eine
fertige Untertitelspur und spart bei einem Lernfilm einen ganzen Schritt.

**e) Den naechsten Schritt anbieten**, wenn er naheliegt, nicht „noch etwas?":
- dasselbe mit anderem `seed`, wenn es fast gepasst hat
- dieselbe Beschreibung eine Stufe ruhiger oder schneller
- **die Sprecherstimme dazu** (kim-voice), **das Video** (kim-video), **ein
  Geraeusch darunter** (kim-sfx)
- **abmischen** mit `audio_assemble`, wenn Stimme und Musik beide da sind

Jede Variante ist eine neue Generierung und kostet wieder — das sagen.

---

## Ein Stueck wiederfinden

`seed` mit demselben Prompt liefert dieselbe Musik. Nenne den Seed in deiner
Antwort, sobald jemand sagt, dass ihm ein Stueck gefaellt („Seed 4711, damit wir
es wiederfinden"). Ohne ihn ist ein gelungenes Stueck weg, sobald der Link
ablaeuft.

---

## Was der Musik-Generator nicht kann

- **Der gesungene Text laesst sich nicht vorgeben.** Die Engine schreibt ihre
  eigenen Worte aus dem Thema. Deutsch singt sie nicht zuverlaessig — von
  Englisch ausgehen.
- **Basic kann ueberhaupt nicht singen.** Will jemand auf Basic Gesang, wechsle
  die Engine, statt die Grenze zu erklaeren.
- **Keine Geraeusche.** Regen, Meer, Feuer, Gong macht **kim-sfx**. Ein
  Geraeusch-Prompt ergibt hier Musik, die an Regen erinnert — das ist keine
  Fehlbedienung, sondern die Natur der Sache.
- **Kein bestimmtes Lied, kein Kuenstler, keine Band.** Vorhandene Musik wird
  nicht reproduziert, und „wie Hans Zimmer" ist unzuverlaessig und eine schlechte
  Idee. Den Klang beschreiben: *epic, cinematic, sweeping orchestral strings and
  deep drums*.
- **Laenger als fuenf Minuten am Stueck geht nicht.** Darueber wird geloopt.
- **Keine Stems**, keine getrennten Spuren, kein MIDI. Ein fertiger Stereomix.
- **Kein Ein- und Ausblenden eingebaut.** Liegt die Musik unter Sprache, braucht
  sie Absenkung und eine Blende — das machen `audio_assemble` und
  `film_assemble` **auf dem Server**, es muss nichts installiert werden.

Das klar sagen, wenn es aufkommt, statt etwas zu generieren, das enttaeuscht.

---

## Related Skills — die KIM-Familie

Ein Server, ein Guthaben:

| Skill | Wofuer |
|---|---|
| **kim-music** (dieser) | Musik: Hintergrund, Intro, Musikbett, Lied |
| **kim-sfx** | Geraeusche: Regen, Meer, Feuer, Gong, Tuer — Laenge frei |
| **kim-voice** | Sprache: Vorlesen, Voiceover, Vertonung |
| **kim-images** | Bilder: erstellen, bearbeiten, Varianten |
| **kim-video** | Videoclips: Text-zu-Video, Bild animieren |
| **kim-lernfilm** | Der ganze Film: Storyboard, Bilder, Stimme, Musik, Schnitt |
| **kim-meditation** | Gefuehrte Meditation: Skript, Musik, Stimme, Abmischung |
| **kimastermind-setup** | Verbindung, Guthaben, Fehlersuche |

**Musik kommt selten allein.** Wer Hintergrundmusik bestellt, will meist auch
ein Video oder eine Sprecherstimme. Den Nachbar-Skill einmal nennen, konkret:

> „Wenn eine Sprecherstimme dazu soll, sagt *kim-voice* — die Stimmen kannst du
> vorher kostenlos anhoeren."

Gehen Musik und Sprache zusammen, **erst die Sprache generieren**: ihre Laenge
steht durch den Text fest, und die Musik wird danach gewaehlt — mit Pro sogar
auf die Sekunde. Nie umgekehrt.

---

## Error Handling

| Fehlermeldung | Ursache | Was zu tun ist |
|---|---|---|
| „must be written in English" | ein deutscher Prompt ist durchgerutscht | Dein Fehler, nicht der des Nutzers. Uebersetzen und ohne Rueckfrage neu aufrufen |
| „Insufficient credits" | Guthaben zu klein | Fehlmenge nennen, kuerzere Variante anbieten, Link zum Aufladen |
| Beschreibung abgelehnt | Inhaltsfilter des Anbieters | Umformulieren, ohne Namen und Marken |
| „rate limited" | zu viele Anfragen | Eine Minute warten, einmal erneut |
| „not configured on this server" | Serverkonfiguration | Nicht der Nutzer. Andere Engine anbieten, Meldung an support@kimastermind.net |
| Generierung bricht ab | anbieterseitige Stoerung | Credits werden **automatisch zurueckgebucht** — das sagen. Einmal erneut versuchen |

---

## Sprache und Ton

- Standardsprache: Deutsch, Du-Form
- Schweizer Schreibweise: ss statt sz
- Die Faehigkeit heisst **Musik-Generator**, die Engines heissen **Mastermind
  Music Basic / Advanced / Pro** — und sonst gar nichts
- **Nicht genannt werden der Anbieter, die API, das darunterliegende Modell und
  jeder Einkaufspreis.** Credits sind der einzige Preis, den ein Nutzer sieht.
  Fragt jemand, wer dahintersteckt: das wird nicht offengelegt
- Den englischen Prompt nie als Arbeit des Nutzers darstellen und nie von ihm
  verlangen — er beschreibt auf Deutsch, die Uebersetzung ist unsere Aufgabe
- Kurz halten. Eine Frage, eine Kostenzeile, dann Musik
