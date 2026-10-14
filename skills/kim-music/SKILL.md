---
name: kim-music
description: Use whenever the user wants music, a soundtrack, background music or a musical bed generated. Triggers: mach Musik, generiere Musik, Hintergrundmusik, Musik fuer mein Video, Soundtrack, Jingle, Intro-Musik, Begleitmusik, Musikbett, Lounge-Musik, Entspannungsmusik, make music, background music, soundtrack, generate music, music for my video. Guides Claude through four short questions (with or without vocals, style, mood, length), turns the answers into the ENGLISH prompt the engine requires, states the balance and the exact cost before generating, then plays the result. Two engines: Advanced can sing and returns the lyrics with second marks, Basic is instrumental only. Clips run about 30 seconds and the length cannot be set. For speech use kim-voice, for video kim-video, for still images kim-images. Provider and model names are never mentioned.
version: 1.0.0
---

# KIM Music Skill

## Purpose

Generate background music with the KIMASTERMIND_IMAGES MCP tools. The capability
is called the **Musik-Generator**. Output is an MP3 (48 kHz stereo) available for
**24 hours**, exactly like generated speech.

What makes this skill worth having: **the user describes the music in German, in
everyday words, and never sees the prompt.** The engine only accepts English and
reacts strongly to naming instruments and tempo — that translation is this
skill's actual job. Never ask the user to write English.

## Two engines, and the one limit that applies to both

| Engine | Gesang | Laenge je Stueck | Wartezeit | Credits |
|---|---|---|---|---|
| **Mastermind Music Advanced** (`song`, Standard) | **ja**, mit Text und Zeitmarken | **2:30 bis 3:00 am Stueck** | ~30 Sek | **16** |
| **Mastermind Music Basic** (`score`) | nein, nur instrumental | 33 Sek | ~30 Sek | **12** |

**Use `song` unless there is a reason not to.** It is faster, cheaper and can do
everything Basic can — instrumental included, just say "no vocals" in the
prompt. Basic exists as the fallback: it runs on a different account, so it
still works when Advanced is unavailable. Only name the choice to the user when they
ask or when Advanced fails.

**Neither lets you set the length.** Advanced returns one continuous piece of
roughly two and a half to three minutes (148, 149, 168, 174 and 178 seconds
measured); asking for six minutes in the prompt does not go past three. Basic
returns exactly 33 seconds. **Quote the length the tool reports**, never a round
number — it measures the file.

**For anything longer than three minutes, do not generate more pieces.** Two
pieces from the same prompt are two different compositions and the seam is
audible — that is exactly the complaint that led here. Generate ONE piece and
let `audio_assemble` loop it. Looping costs nothing. Longer music is several clips joined, 1 to 4 per request, so the
length comes in steps: 30 / 60 / 90 / 120 seconds on Advanced, 33 / 66 / 98 / 131 on
Basic. A piece of exactly 45 seconds does not exist — generate 60 and cut.

**When the piece is sung, the lyrics come back with second marks**, like
`[2.0:6.0] Oh, the world just got bigger now`. That is a finished subtitle
track. Hand it to the user whenever there are vocals; for a learning video it
saves a separate step.

---

## Available MCP Commands

- KIMASTERMIND_IMAGES:music_generate -- `prompt` (REQUIRED, **English**),
  `engine` (`song` or `score`, default `song`), `clips` (1-4, default 1),
  `negative_prompt` (English, Basic only), `seed` (Basic only).
- KIMASTERMIND_IMAGES:my_credits -- current balance. **Call before every
  generation**; a figure from earlier in the conversation is stale.
- KIMASTERMIND_IMAGES:list_models -- all models with their credit costs.

Login portal: https://mcp.kimastermind.net/login

---

## The Four Questions

Ask only what the user has not already said. Someone who writes "mach mir ruhige
Klaviermusik fuer ein Meditationsvideo, etwa eine Minute" has answered all four —
ask nothing, state the cost and go.

**1. Instrumental oder mit Gesang?**
This decides nothing about the engine — Advanced does both — but everything about
the prompt. With vocals, **the engine writes the words itself**; the user says
what the song should be ABOUT, not what it should say. If someone brings their
own lyrics, say plainly that the text cannot be dictated, and offer the
alternative that actually works: instrumental music plus a spoken voice-over
through kim-voice.

**2. Stilrichtung?** Ambient, Pop, Rock, Klassisch — or anything they name
themselves (Jazz, Lo-Fi, Folk, Elektronisch, Orchestral ...). The four are a
starting point, not a menu to enforce.

**3. Stimmung?** ruhig, schnell, gluecklich, traurig — again a starting point.
Feierlich, spannend, verspielt, episch and so on all work.

**4. Dauer?**

| Wahl | Advanced | Basic |
|---|---|---|
| **kurz** (Jingle, Intro) | 1 Stueck bis 3 Min, 16 Credits | 1 Clip 33 Sek, 12 Credits |
| **mittel / lang** | dasselbe eine Stueck, beim Mischen geloopt | mehrere Clips noetig |

Bei Advanced ist „laenger" keine Frage der Anzahl, sondern des Loopens. Frag
also nicht nach der Laenge der Musik, sondern nach der Laenge des **Projekts**
— und erzeuge ein Stueck.

Ask all open questions **in one message**, not one at a time. Four short
questions in a row is a form, not a conversation.

---

## Turning the answers into the prompt

This is the part that decides whether the music is good. Build an English
sentence from four pieces in this order: **mood, genre, instruments, tempo** —
then append `no vocals`, which the engine honours reliably.

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

**Always name instruments**, even when the user did not: a genre alone gives a
generic result. "ruhig + Klassisch" becomes *gentle piano and soft strings*, not
just *classical*.

Two worked examples:

> „ruhige Ambient-Musik fuer ein Meditationsvideo"
> → `serene ambient music, soft atmospheric pad and sparse piano, very slow tempo, no vocals`

> „fetzige Rockmusik fuers Intro, kurz"
> → `energetic rock, electric guitar riff and punchy drum kit, fast tempo, driving, no vocals`

Use `negative_prompt` only against something the user explicitly does not want
("ohne Schlagzeug" → `drums, percussion`). Leave it empty otherwise.

**Show the user the prompt you built, in German, in one line** — not the English
string, but what you understood: „Ich erzeuge: ruhige Ambient-Musik, weiches
Flaechen-Pad und sparsames Klavier, sehr langsam." That is where a
misunderstanding gets caught, before credits are spent.

---

## Cost BEFORE generating

Same rule as speech: cost and balance together, in one sentence, before the
call.

1. Call `my_credits`.
2. Credits are **16 per piece on Advanced, 12 per clip on Basic** (check against
   `list_models`; the rate lives in the database and can change).
3. Say it:

> „Das sind 2 Clips, zusammen 60 Sekunden und **16 Credits**. Du hast aktuell
> **96 Credits**, danach noch 80. Soll ich?"

Not enough credits: name the exact shortfall and offer the shorter version,
which is a real alternative here — half the length is half the price.

**Generation takes about 30 seconds on either engine.** Say so
before calling, and do not abort or retry while it runs: a retry pays for the
same music twice.

---

## Delivering the music

Like a generated clip in kim-voice:

**a) What it cost.** `music_generate` returns the charge and the new balance.
Pass both on.

**b) Play it.** In this order, stop at the first that works:

1. **Inline** as a `data:` URI in a small HTML artifact — only this plays inside
   the chat, audio from `mcp.kimastermind.net` is blocked there. A 33-second
   clip is about 800 KB, two clips 1.6 MB; from three clips up go to 2.
2. **System player.** Download, then hand it to the OS:
   ```powershell
   $folder = "$env:USERPROFILE\Music\KI-Musik"; if (!(Test-Path $folder)) { New-Item -ItemType Directory -Path $folder | Out-Null }; $file = "$folder\AUDIO_FILENAME.mp3"; Invoke-WebRequest -Uri "AUDIO_URL_HERE" -OutFile $file; Start-Process $file
   ```
   macOS `afplay`, Linux `xdg-open`. Name the folder — people look for the file
   later.
3. **The link**, plainly, with the note that it opens in a new tab.

**c) The 24-hour warning**, every time. Route 2 already saves the file.

**d) Offer the useful next step**, not "noch etwas?":
- the same music again with a different seed, if it was nearly right
- the same description one step calmer or faster
- more clips, if it turned out too short
- **the voice-over to go with it** (kim-voice), or **the video** (kim-video)

Each variant is a new generation and costs again — say so.

---

## Reproducing a piece

`seed` with the same prompt returns the same music. Note the seed in your answer
whenever a user says they like a piece ("Seed 4711, damit wir es wiederfinden").
Without it, a piece they liked is gone the moment the link expires.

---

## What the Musik-Generator cannot do

- **The sung text cannot be dictated.** The engine writes its own words from
  the topic. It also cannot sing in German reliably — assume English.
- **Basic cannot sing at all.** If the user is on Basic and wants vocals,
  switch to Advanced rather than explaining the limit.
- **Keine Geraeusche** — Regen, Meer, Feuer, Gong macht **kim-sfx**. Ein
  Geraeusch-Prompt ergibt hier Musik, die an Regen erinnert
- **No specific song, artist or band.** It does not reproduce existing music, and
  asking for "wie Hans Zimmer" is both unreliable and a bad idea. Describe the
  sound instead: *epic, cinematic, sweeping orchestral strings and deep drums*.
- **No exact length.** Only whole clips. For a 45-second video take two clips
  and cut the end, or fade out — that is an editing step, not a generation
  step.
- **No stems**, no separate tracks, no MIDI. One finished stereo mix.
- **No fade-in or fade-out** built in. If the music sits under speech, it needs
  ducking and a fade — ffmpeg does that locally.

Say these plainly when they come up instead of generating something that will
disappoint.

---

## Related Skills — die KIM-Familie

One server, one credit balance:

| Skill | Wofuer |
|---|---|
| **kim-music** (dieser) | Musik: Hintergrund, Intro, Musikbett |
| **kim-voice** | Sprache: Vorlesen, Voiceover, Vertonung — zwei Engines |
| **kim-images** | Bilder: erstellen, bearbeiten, Varianten |
| **kim-video** | Videoclips: Text-zu-Video, Bild animieren |
| **kim-sfx** | Geraeusche: Regen, Meer, Feuer, Gong, Tuer. Laenge frei waehlbar |
| **kim-lernfilm** | Der ganze Film: Storyboard, Bilder, Stimme, Musik, Clips, Schnitt |
| **kim-meditation** | Gefuehrte Meditation: Skript, Musik, Stimme und Abmischung |
| **kimastermind-setup** | Verbindung, Guthaben, Fehlersuche |

**Musik kommt selten allein.** Whoever asks for background music usually wants a
video or a voice-over too. Mention the neighbouring skill once, concretely:

> „Wenn eine Sprecherstimme dazu soll, sagt *kim-voice* — du kannst die Stimmen
> vorher kostenlos anhoeren."

When music and speech go together, generate **the speech first**: its length is
set by the text, and the music is then chosen to fit — never the other way round.

---

## Error Handling

| Fehlermeldung | Ursache | Was zu tun ist |
|---|---|---|
| „must be written in English" | ein deutscher Prompt ist durchgerutscht | Dein Fehler, nicht der des Nutzers. Prompt uebersetzen und ohne Rueckfrage neu aufrufen |
| „Insufficient credits" | Guthaben zu klein | Fehlmenge nennen, kuerzere Variante anbieten, Link zum Aufladen |
| „not available in region" | Serverkonfiguration | Nicht der Nutzer. An support@kimastermind.net |
| „needs ffmpeg" | Serverkonfiguration | Dasselbe |
| Generierung bricht ab | anbieterseitige Stoerung | Credits werden **automatisch zurueckgebucht** — das sagen. Einmal erneut versuchen |

---

## Sprache und Ton

- Standardsprache: Deutsch, Du-Form
- Schweizer Schreibweise: ss statt sz
- Die Faehigkeit heisst **Musik-Generator**
- Modellnamen duerfen genannt werden, wenn jemand fragt. **Nicht genannt werden
  der Anbieter, die API und jeder Einkaufspreis.** Credits sind der einzige
  Preis, den ein Nutzer sieht
- Den englischen Prompt nie als Arbeit des Nutzers darstellen und nie von ihm
  verlangen — er beschreibt auf Deutsch, die Uebersetzung ist unsere Aufgabe
- Kurz halten. Vier Fragen, eine Kostenzeile, dann Musik
