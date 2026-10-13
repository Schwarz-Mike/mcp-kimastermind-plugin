---
name: kim-voice
description: Use whenever the user wants text spoken aloud or an audio voice-over. Triggers: lies das vor, sprich das, vertone das, mach daraus Audio, Stimme, Sprecher, Voiceover, Vorleser, Narration, Hoerbuch, Podcast-Intro, Ansage, als MP3, welche Stimmen gibt es, zeige alle Stimmen, Stimmen anhoeren, Stimmproben, read this aloud, text to speech, narrate this, which voices are available, show me the voices. Guides Claude through the workflow: let the USER pick the engine (Express fast and cheap, Studio slower and better), point at the free listening page https://mcp.kimastermind.net/voices/<engine>, state the balance and the exact cost before generating (billed per input character), call KIMASTERMIND_IMAGES voice_generate, then play the MP3, say what it cost and warn that the link expires after 24 hours. For IMAGES use kim-images, for VIDEO use kim-video. Provider and model names are never mentioned.
---

# KIM Voice Skill

## Purpose

Guide the user through a complete SPEECH generation workflow using the
KIMASTERMIND_IMAGES MCP tools. Provider names are NEVER mentioned -- the
capability is called the **Stimmen-Generator**. Generated audio comes from
https://mcp.kimastermind.net/aud/ as an MP3 and is available for **24 hours
only**. Credits are shown after every generation.

## Two engines -- the user picks, never you

There are two speech engines, and they are genuinely different trade-offs. The
choice belongs to the user:

| Engine | Speed | Quality | Voices | Price |
|---|---|---|---|---|
| **Express** | ~1-3 seconds | good, even, neutral | 28, multilingual, language selectable | cheaper |
| **Studio** | up to ~4 minutes | more natural stress and phrasing | 30, each with a documented character | pricier |

- **Express** is right for a quick read-aloud, a draft, a short announcement, or
  when the user is in a hurry or watching their credits.
- **Studio** is right for anything someone else will hear: voice-over, podcast
  intro, audiobook passage, a long narration where a flat delivery would show.
  It also accepts a `style` instruction ("warm und ruhig") and works out the
  language from the text itself.

`voice_listing` without an `engine` returns both with their live credit price per
1000 characters and per minute of audio. **Show those numbers and ask.** The two
sentences to use are in Step S3 — they name the price, the 1-credit minimum, and
the one thing that sets the engines apart besides price: Express speaks fifteen
selectable languages, Studio takes a spoken-style instruction. Only
skip the question when the user has already said which one they want, in their
own words ("schnell reicht", "bitte in bester Qualitaet", "Express", "Studio").

The voices do NOT overlap: an Express voice cannot be used on Studio or the
other way round. Switching the engine therefore means picking a new voice.

## Related Skills -- the KIM family

The same MCP server and the same credit balance power three skills. They are
siblings, not alternatives: if a request is not about speech, hand it to the
right one instead of improvising here.

| Skill | Use it for | MCP tools |
|---|---|---|
| **kim-voice** (this one) | Speech: text read aloud, voice-over, narration | `voice_listing`, `voice_sample`, `voice_generate` |
| **kim-images** | Still images: generate, edit, restyle, vary, combine | `generate_image`, `export_image`, `my_gallery` |
| **kim-video** | Video clips: text-to-video, animating an image, reference-to-video | `generate_video` |
| **kimastermind-setup** | Einrichtung pruefen: Verbindung, Guthaben, Fehlersuche | `my_credits`, `list_models` |

Routing rules:
- "funktioniert das", "bin ich verbunden", "wie viele Credits", "geht nicht" -> **kimastermind-setup**
- "generiere ein Bild", "bearbeite das Foto", "Logo", "Grafik" -> **kim-images**
- "mach ein Video daraus", "animiere das", "Reel", "Clip" -> **kim-video**
- Everything about spoken audio stays here.

A combined request is handled in sequence and announced as such. The common one:
- "Video mit Sprecherstimme" -> kim-video for the clip, then this skill for the
  narration. **The MCP cannot mux the audio into the video.** Deliver the MP4 and
  the MP3 as two files and say so plainly -- never imply the voice is inside the
  clip.

`my_credits` and `list_models` are shared by all three skills.

## Available MCP Commands

- KIMASTERMIND_IMAGES:voice_listing -- Called WITHOUT `engine`: both engines with
  speed, voice count and live credit price. Call this FIRST when the user has not
  chosen an engine. Called WITH `engine`: that engine's voices with name, gender,
  character and a free sample URL.
- KIMASTERMIND_IMAGES:voice_sample -- The sample URL for one voice (or all of
  them, grouped by engine). Costs NO credits. Every sample speaks the same
  sentence, so voices are directly comparable across both engines.
- KIMASTERMIND_IMAGES:voice_generate -- Generate the MP3. `text` and `engine` are
  REQUIRED; `voice`, `language` and `style` are optional. Billed per input
  character.
- KIMASTERMIND_IMAGES:my_credits -- Current credit balance. **Call this before
  every generation**, so cost and remaining balance go out together (Step S3).
  A balance from earlier in the conversation is stale.
- KIMASTERMIND_IMAGES:list_models -- All models with prices (voice model included)

Login portal: https://mcp.kimastermind.net/login

---

## Offer listening before anything is paid for

**Every time speech comes up, say in one sentence that the voices can be heard
for free first.** Most people do not know it, and a voice chosen blind is the
single most common reason a clip gets generated twice. One line is enough:

> „Du kannst alle Stimmen vorher kostenlos anhoeren — sag einfach *zeige alle
> Stimmen*."

On **„zeige alle Stimmen"** (and anything like it) give BOTH pages, Studio first
because its voices carry a documented character:

```
Studio  (30 Stimmen, mit Charakter):  https://mcp.kimastermind.net/voices/studio
Express (28 Stimmen, schnell):        https://mcp.kimastermind.net/voices/express
```

**Open the page yourself when a browser tool is available.** In Claude Desktop
there is a built-in browser pane; open the Studio page in it so the person can
click a tile right away instead of switching windows:

- built-in browser pane available -> open `https://mcp.kimastermind.net/voices/studio`
  in it, then name the second link in the text
- no browser tool -> give both links as text, nothing else

Do NOT open a page the person did not ask about, and never open more than one.

---

## Handling Non-Generation Requests

### Credits Query

Trigger: credits, Guthaben, wie viel habe ich noch, my credits

Call KIMASTERMIND_IMAGES:my_credits and display:
Dein aktuelles Guthaben: X Credits
Link: https://mcp.kimastermind.net/login

### Voice Catalogue Query

Trigger: welche Stimmen gibt es, zeig mir die Stimmen, Stimmenliste,
which voices, list voices

First establish WHICH engine the user means. If they have not said, call
`voice_listing` without an engine, show both and ask -- do not list 58 voices.

Once the engine is known, call `voice_listing` with it and present the voices as
a **table grouped by gender**, with the sample link per voice. Do NOT dump the
raw ids as a flat list -- that is unusable.

Express (gender is all the catalogue knows; every voice is multilingual, so the
choice is purely about sound, not about language):

```
| Stimme | Geschlecht | Anhören |
|---|---|---|
| Eve | weiblich | https://mcp.kimastermind.net/api/voice/sample/eve.mp3 |
| Orion | männlich | https://mcp.kimastermind.net/api/voice/sample/orion.mp3 |
```

Studio (each voice has a documented character -- use it, it is the only thing
that tells thirty star names apart):

```
| Stimme | Geschlecht | Charakter | Anhören |
|---|---|---|---|
| Sulafat | weiblich | warm | https://mcp.kimastermind.net/api/voice/sample/sulafat.mp3 |
| Charon | männlich | sachlich | https://mcp.kimastermind.net/api/voice/sample/charon.mp3 |
```

Better than any table: hand out the listening page, where every voice of the
engine plays on one click -- see "Stimmen anhoeren" below. The table is for
naming two or three candidates with their character, not for the full catalogue.

If the request was the broad one („zeige alle Stimmen"), do not build a table of
58 rows at all. Give the two page links, open one in the browser pane if there
is one, and name three fitting voices with their character as a starting point.

---

## Speech Generation Workflow

### Step S0: Check What is Already Known

Never ask for something the user already gave you. Scan the request for:
- the **text** to speak (often the whole point of the message, or a document /
  earlier answer the user points at)
- an **engine** preference, stated as a preference rather than a name
  ("schnell", "guenstig", "beste Qualitaet", "fuer einen Podcast")
- a **voice** by name ("mit Eve", "mit Sulafat", "eine männliche Stimme")
- a **language** ("auf Englisch", "in French")
- a **style** ("ruhig vorlesen", "sachlich", "lebendig") -- Studio only

A named voice already implies its engine, so do not ask again -- just say which
engine that is. If text, engine, voice and language are all clear, skip straight
to Step S3.

### Step S1: Get the Text

If no text was supplied, ask what should be spoken. If the user points at
something ("lies die Zusammenfassung vor", "vertone den Blogpost"), take that
text rather than asking them to paste it again.

**Advise against very long clips before the limit even matters.** A clip is
produced in one go and billed in one go, so a long one means a long wait and a
single file nobody can edit. Rule of thumb to give the person:

| Laenge | ca. Woerter | Audio | Empfehlung |
|---|---|---|---|
| bis 1500 Zeichen | ~250 | ~1,5 Min | ideal, auch auf Studio schnell |
| 1500–3000 Zeichen | ~250–500 | 1,5–3 Min | geht gut; auf Studio ~2 Min Wartezeit |
| ueber 3000 Zeichen | ueber 500 | ueber 3 Min | **in Abschnitte teilen anbieten** — je Kapitel eine Datei |

Splitting is not only about the wait: a correction in minute four otherwise
means paying for the whole clip again.

**The hard limit is 5000 characters per clip**, enforced by the server. If the
text is longer:
- Say so with the actual number ("Der Text hat 8400 Zeichen, pro Aufnahme sind
  5000 möglich").
- Offer to split it at paragraph or sentence boundaries into several clips, and
  generate them in sequence. NEVER cut mid-sentence.
- Each clip is billed and delivered separately, each with its own 24h link.

Written text is not spoken text. Before generating, silently clean up anything
that reads badly aloud, and mention it only if it changes the meaning:
- Markdown syntax (`**`, `##`, `-`, link brackets) -> remove
- URLs and e-mail addresses -> either drop them or spell them out in words
- Abbreviations like "z.B.", "etc.", "Nr." -> write out ("zum Beispiel")
- Numbers, dates and currency -> write out when pronunciation is ambiguous
- Tables, code blocks, footnotes -> these do not work as audio; ask what to do

### Step S1b: Pick the Engine

Skip only if the user already made the choice clear (see S0) or named a voice.

1. Call `voice_listing` with no `engine`.
2. Show both, with the actual numbers the tool returned -- credits per 1000
   characters AND roughly per minute of audio -- plus the speed difference.
   Keep it to two lines each, and include what the text at hand would cost:

```
Zwei Engines:

**Express** -- fertig in 1-2 Sekunden, 28 Stimmen. 1.80 Credits / 1000 Zeichen,
ca. 1.62 Credits pro Minute Audio. Für diesen Text: 2 Credits.

**Studio** -- natürlichere Betonung, 30 Stimmen mit Charakter, Sprechstil
steuerbar. Braucht bei langen Texten mehrere Minuten. 2.56 Credits / 1000
Zeichen, ca. 2.46 Credits pro Minute Audio. Für diesen Text: 3 Credits.

Was nimmst du?
```

3. If the user is unsure, give ONE recommendation with a reason tied to their
   purpose -- "wenn das jemand anders hoert, würde ich Studio nehmen" -- and let
   them overrule it.
4. **Do not pick silently.** The engines differ in price and in wait time; both
   are the user's money and the user's patience.

### Step S2: Pick a Voice (the part users care about most)

If the user has not named a voice:

1. Call `voice_listing` with the chosen `engine`.
2. Suggest **two or three** fitting voices rather than all of them, and say why,
   based on what the audio is for. Keep it short.
3. Give the sample link for each, and say explicitly that listening is free:
   "Hör gern erst rein -- die Beispiele kosten nichts."
4. Wait for the choice. Do not generate with a guessed voice: the clip costs
   credits and the user will almost always want a different voice afterwards.

If the user asks for a "deep", "warm", "friendly" or "young" voice:
- On **Studio**, each voice has a documented character (warm, sachlich, hauchig,
  rauchig, jugendlich, bestimmt ...). Match against that and say which label you
  matched -- that is real information, not a guess.
- On **Express**, the catalogue only exposes **name and gender**, so anything
  beyond that is a guess. Say so and offer two samples instead of inventing
  characteristics. If the user clearly cares about character, that is a good
  moment to mention Studio.

#### Stimmen anhoeren

Wants the user to HEAR the voices, give them the listening page. One link, every
voice of that engine, each playable on one tap, no login, no credits:

```
https://mcp.kimastermind.net/voices/express
https://mcp.kimastermind.net/voices/studio
```

The link also comes back in the `voice_listing` answer for that engine, so take
it from there rather than from memory.

Does a purpose fit, append `?for=<zweck>` and the page pre-selects the fitting
voices: `trance`, `podcast`, `werbung`, `hoerbuch`, `erklaervideo` (German and
English synonyms work too -- meditation, hypnose, audiobook, ad, tutorial ...).
Example: `https://mcp.kimastermind.net/voices/studio?for=trance`.
This needs documented voice characters, so it only has an effect on **Studio**;
on Express the page says so instead of inventing a selection.

**Do NOT build an inline widget with
`<audio src="https://mcp.kimastermind.net/...">`.** claude.ai blocks audio from
other domains (Content Security Policy), so the user gets a dead player and a
bare "open link" -- which is exactly the complaint this page fixes. The page
works because the MP3s come from its own domain.

Name two or three fitting voices with their character in the chat on top of the
link, so the user knows where to start.

Fallback if the page is unreachable AND Bash is available in the workspace:
download the samples, shrink them (`ffmpeg -i in.mp3 -ac 1 -b:a 56k out.mp3`),
embed them as base64 `data:` URIs in one HTML page and publish that as an
artifact -- a `data:` URI is same-origin, so it plays. Without Bash: a table of
sample links plus the honest note that playing them inside the chat is not
possible.

### Step S3: Balance and Cost BEFORE Generating

Two numbers go out before a single credit is spent: **what it costs** and **what
is left**. Never generate without having shown both.

**1. Fetch the balance.** Call `KIMASTERMIND_IMAGES:my_credits`. It is one cheap
call and it is the only way to know; never quote a balance from earlier in the
conversation, it is stale after every generation.

**2. Work out the price.** Speech is billed **per input character**, so unlike
video the exact price is known in advance. Take the rate from the `voice_listing`
answer for the chosen engine, never from memory, and apply:

```
credits = max(1, round(characters / 1000 * credits_per_1000))
```

As of 2026-10-13 the rates are **1,8 Credits je 1000 Zeichen auf Express** and
**2,56 auf Studio**. That gives this orientation table — use it to sanity-check
your arithmetic, but quote the live rate:

| Zeichen | ca. Woerter | Express | Studio | Audio ca. |
|---|---|---|---|---|
| 500 | 80 | 1 Credit | 1 Credit | 0:35 |
| 1 000 | 165 | 2 Credits | 3 Credits | 1:05 |
| 2 000 | 330 | 4 Credits | 5 Credits | 2:15 |
| 3 000 | 500 | 5 Credits | 8 Credits | 3:20 |
| 5 000 | 830 | 9 Credits | 13 Credits | 5:30 |

Eine ganze Stunde Audio kostet damit rund 96 Credits auf Express und 144 auf
Studio — nenne das, wenn jemand ein langes Projekt plant.

**Wording for each engine**, to use when you name the engine's terms. These are
the sentences the listening page shows, so chat and page say the same thing:

> **Express** kostet 1.8 Credits pro 1000 Zeichen (ca. 1.62 Credits pro Minute
> Audio), mindestens 1 Credit pro Clip. Jede Stimme spricht jede unterstuetzte
> Sprache (de, en, fr, it, es, pt, nl, pl, ru, tr, ar, hi, ja, ko, zh).

> **Studio** kostet 2.56 Credits pro 1000 Zeichen (ca. 2.46 Credits pro Minute
> Audio), mindestens 1 Credit pro Clip. Den Sprechstil kannst du beim Generieren
> vorgeben, zum Beispiel „ruhig, langsam, tief entspannend".

Check the numbers against `voice_listing` before quoting them — it carries the
live rate, and these were right on 2026-10-13.

**3. Say it in one sentence**, cost and balance together:

> „Der Text hat 820 Zeichen — das kostet **1 Credit** auf Express und ergibt ca.
> 55 Sekunden Audio. Du hast aktuell **23 Credits**, danach noch 22.
> Soll ich mit **Eve** loslegen?"

(820 × 1,8 / 1000 = 1,48, gerundet 1 — die Rundung geht mal zugunsten des
Nutzers, mal gegen ihn. Rechne, rate nicht.)

**4. Not enough credits?** Say exactly how many are missing, and do not call
`voice_generate` — it would fail and look like a bug:

> „Das kostet 5 Credits, du hast 3. Es fehlen 2 — aufladen unter
> https://mcp.kimastermind.net/dashboard. Mit Express statt Studio waeren es
> 3 Credits, das ginge sofort."

Offering the cheaper engine when the balance is tight is genuinely useful; pushing
the expensive one is not.

Three things to be straight about:
- **There is a 1-credit minimum per clip.** A short sentence costs the same as
  half a page. If the user is generating several short clips, mention that
  combining them into one text is cheaper.
- **On Express, generation is fast** -- a few seconds, not minutes. No wait
  warning needed.
- **On Studio, warn about the wait BEFORE calling.** Long texts are produced in
  sections and stitched together. Measured: roughly 40 seconds per 1000
  characters, so a full 5000-character script takes about three to four minutes.
  Say so first, then call, and do not abort or retry while the call is running --
  a retry pays for the same clip twice.

### Step S4: Generate

Express:

```
KIMASTERMIND_IMAGES:voice_generate(
  text = "Willkommen bei KI Mastermind. Hier entstehen Bilder, Videos und Stimmen aus einem einzigen Werkzeug.",
  engine = "express",
  voice = "eve",
  language = "de"
)
```

Studio:

```
KIMASTERMIND_IMAGES:voice_generate(
  text = "Willkommen bei KI Mastermind. Hier entstehen Bilder, Videos und Stimmen aus einem einzigen Werkzeug.",
  engine = "studio",
  voice = "Sulafat",
  style = "warm und ruhig"
)
```

- `engine` is REQUIRED and must be the one the user chose.
- Omit `voice` only if the user truly has no preference.
- `language` applies to **Express only** (de, en, fr, it, es, pt, nl, pl, ru, tr,
  ar, hi, ja, ko, zh; default de). Studio reads the language off the text, so
  passing it there changes nothing -- do not promise it does.
- `style` applies to **Studio only** and is a plain instruction, not a tag:
  "warm und ruhig", "sachlich und zuegig", "lebendig, wie eine Erzaehlerin".
  Passing it on Express is silently ignored, so never offer style control there.
- Studio voice ids are capitalised ("Sulafat"), Express ids are lowercase
  ("eve"). Either spelling is accepted; the response gives the canonical one.

Returns `Download URL: https://mcp.kimastermind.net/aud/UUID.mp3` plus characters,
file size, credits used and remaining.

Call the capability the **Stimmen-Generator** and the two options **Express**
and **Studio**. If the user asks outright which model is behind an engine,
`list_models` answers that -- model names are not secret. The supply chain is
(see Language and Tone).

### Step S5: Deliver the MP3, Play It, Show What It Cost

Three things belong in this answer, every time:

**a) What it cost.** `voice_generate` returns the charge and the new balance —
pass both on, do not make the person work it out:

> „Fertig. **1 Credit** verbraucht, **22 Credits** uebrig."

If the charge differs from your estimate in S3, say so and say why (the 1-credit
minimum on short clips is the usual reason).

**b) The audio, playable.** Try these in order and stop at the first that works:

1. **Inline abspielbar.** Only a `data:` URI plays inside the chat — audio loaded
   from `mcp.kimastermind.net` is blocked there by the Content Security Policy.
   So: if a shell is available and the file is **under ~1,5 MB** (roughly 90
   seconds), download it, base64 it, and put it in a small HTML artifact as
   `<audio controls src="data:audio/mpeg;base64,...">`. Above that size skip
   straight to 2 — a huge artifact is slower to build than the clip is to play.
2. **Mit dem Systemplayer oeffnen.** Download, then hand it to the OS. The file
   stays, so it survives the 24-hour window:
   ```powershell
   $folder = "$env:USERPROFILE\Music\KI-Stimmen"; if (!(Test-Path $folder)) { New-Item -ItemType Directory -Path $folder | Out-Null }; $file = "$folder\AUDIO_FILENAME.mp3"; Invoke-WebRequest -Uri "AUDIO_URL_HERE" -OutFile $file; Start-Process $file
   ```
   macOS: `curl -s -o ~/Music/KI-Stimmen/NAME.mp3 "URL" && afplay ~/Music/KI-Stimmen/NAME.mp3`
   Linux: `curl -s -o ~/Musik/NAME.mp3 "URL" && xdg-open ~/Musik/NAME.mp3`
   Say which folder it landed in — people look for the file later.
3. **Nur der Link.** On web and mobile nothing can be played locally. Give the
   URL plainly and say that it opens in a new tab.

Always give the direct link as well, whichever route worked.

**c) The 24-hour warning.** The link is valid for **24 hours**; after that the
file is deleted from the server and the link returns an error. Say it every
time, and offer to save the file — route 2 already does.

Saving without playing, when that is all the person wants:

- **Claude Desktop (Windows)**: save to `$env:USERPROFILE\Music\KI-Stimmen\` via
  Invoke-WebRequest (PowerShell rules: no curl, no &&, no ~).
  ```powershell
  $folder = "$env:USERPROFILE\Music\KI-Stimmen"; if (!(Test-Path $folder)) { New-Item -ItemType Directory -Path $folder | Out-Null }; Invoke-WebRequest -Uri "AUDIO_URL_HERE" -OutFile "$folder\AUDIO_FILENAME.mp3"; Get-Item "$folder\AUDIO_FILENAME.mp3" | Select-Object Name, Length
  ```
- **Claude Desktop (Mac/Linux)**: `curl -s -o ~/Music/KI-Stimmen/AUDIO_FILENAME.mp3 "AUDIO_URL_HERE"`
- **Web / Mobile / download failure**: give the download link in plain text with
  the expiry warning and the new balance. A widget may look nicer, but claude.ai
  blocks audio from `mcp.kimastermind.net`, so the `<audio>` element below stays
  silent there -- only the link works. Use the widget where you know audio from
  other domains plays; otherwise drop it and keep link, warning and balance:

```html
<div style="padding: 1rem 0;">
  <div style="background: var(--color-background-secondary); border-radius: var(--border-radius-lg); padding: 1rem;">
    <audio src="AUDIO_URL_HERE" controls preload="metadata" style="width:100%; display:block;"></audio>
    <div style="margin-top: 12px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
      <p style="font-size:13px; color: var(--color-text-secondary); margin:0;">Stimme: VOICE_HERE &middot; Sprache: LANG_HERE &middot; CHARS_HERE Zeichen &middot; SIZE_HERE KB</p>
      <a href="AUDIO_URL_HERE" target="_blank" style="font-size:13px; color: var(--color-text-info); text-decoration:none;">&#x2B07; Herunterladen</a>
    </div>
    <p style="font-size:12px; color: var(--color-text-warning, #d97706); margin:10px 0 0;">&#9888; Der Link ist 24 Stunden gültig, danach wird die Datei gelöscht. Bitte jetzt speichern.</p>
    <div style="margin-top:10px; padding:8px 10px; background: var(--color-background-primary); border-radius: var(--border-radius-md); border:0.5px solid var(--color-border-tertiary); display:flex; justify-content:space-between; align-items:center;">
      <span style="font-size:13px; color: var(--color-text-secondary);">Guthaben: <strong style="color: var(--color-text-primary);">CREDITS_HERE Credits</strong></span>
      <a href="https://mcp.kimastermind.net/login" target="_blank" style="font-size:12px; color: var(--color-text-info); text-decoration:none;">Aufladen &#x2197;</a>
    </div>
  </div>
</div>
```

Also show the plain link: 📥 Direktlink: https://mcp.kimastermind.net/aud/UUID.mp3

### Step S6: Offer a Variant

After delivering, offer the useful next step rather than a generic "noch etwas?":
- same text with a different voice (so the user can compare in context)
- the next chunk, if the text was split
- a different language version

Each variant is a new generation and costs credits again -- say so.

---

## What the Stimmen-Generator Cannot Do

Be upfront instead of letting the user discover it.

Both engines:
- **No custom or cloned voices.** The catalogues are fixed -- a user's own voice
  cannot be added.
- **No background music, no mixing, no muxing into video.** The output is a bare
  MP3 of the spoken text.
- **No subtitle or timestamp output.**
- **No speed control** as a parameter, and no markup tags like `[lacht]`.
- **Maximum 5000 characters per clip** on either engine.

Express only:
- **No emotion or style control at all.** There is no "fröhlich", "traurig",
  "flüsternd" parameter. Tone comes from the written text and the chosen voice.
- **The speaking pace is effectively identical across all voices**; only the
  timbre differs.

Studio only:
- **Style is an instruction, not a guarantee.** `style` steers the delivery; it
  does not switch on a named emotion, and the same instruction can land slightly
  differently between runs.
- **The language cannot be forced.** It follows the text. A German sentence
  inside an English text may be read with an English accent.
- **It is slow.** Roughly 40 seconds of waiting per 1000 characters, so three
  to four minutes for a full-length 5000-character script.

If the user needs any of these, say it is not available here rather than
generating something that will disappoint them.

---

## Environment Summary

| Umgebung | Download-Methode | Speicherort |
|---|---|---|
| Claude Desktop (Windows) | desktop-commander + Invoke-WebRequest | %USERPROFILE%\Music\KI-Stimmen\ |
| Claude Desktop (Mac/Linux) | bash_tool + curl | ~/Music/KI-Stimmen/ |
| claude.ai Web | nicht moeglich | Download-Link + Hinweis 24h |
| Claude Mobile (iOS/Android) | nicht moeglich | Download-Link + Hinweis 24h |

Hoerproben in Web und Mobile: `https://mcp.kimastermind.net/voices/<engine>`.
Inline-Audio von fremden Domains ist dort gesperrt, die Seite umgeht das.

Bundled samples: this skill ships one sample clip per voice under
`samples/express/<voice_id>.mp3` and `samples/studio/<voice_id>.mp3`, plus an
`index.json` per engine with gender and, for Studio, the character of each
voice. The folder a voice sits in tells you its engine, which matters because
`voice_generate` rejects a voice from the other one.

The served URL `https://mcp.kimastermind.net/api/voice/sample/<id>.mp3` is the
preferred way to let the user listen, because a link actually plays in their
browser while a local file in the skill folder does not. That URL is flat for
both engines — the id alone identifies the voice.

---

## Error Handling

Unknown voice:
- The tool returns an error naming the voice. Call `voice_listing` for the chosen
  engine, show the closest matches and let the user pick. Do not substitute a
  voice silently.

Voice belongs to the other engine:
- The error says which engine the voice belongs to. Ask the user which they
  actually want -- the voice or the engine -- and do not quietly switch either.
  Switching the engine also changes the price, so state the new cost.

Studio rate limited:
- The error asks the user to retry in a minute or use Express. Offer Express with
  its price as the immediate alternative; no credits were spent.

Text too long:
- Over 5000 characters the call is rejected before any credits are spent. Split
  at sentence boundaries and generate in sequence.

Expired link:
- `/aud/...` returns HTTP 410 after 24 hours. The file is gone -- it cannot be
  recovered. Offer to generate it again (and say that this costs credits again).

Generation error or API failure:
- Credits are refunded automatically on every failure -- say so, so the user does
  not think the attempt cost them anything
- Retry once; if the second attempt also fails, inform the user

Credits too low:
- Inform user and link to https://mcp.kimastermind.net/login

PowerShell pitfalls (Windows):
- Never use && -- use ; instead
- Never use bare curl -- use Invoke-WebRequest
- Never use ~ -- use $env:USERPROFILE

---

## Language and Tone

- Default language: German, informal du form
- Swiss conventions: ss not sz
- Model names are NOT secret. If the user asks which model was used or which
  models exist, name it. `list_models` is there for exactly that.
- But NEVER name the marketplace or aggregator the models are bought through,
  and never name the supplier behind the voice generator. If someone asks who
  the provider is, where the models are hosted, or which API is called, say
  plainly that the supply chain is not disclosed -- then offer what is useful
  instead: which model fits, what it costs in credits, what it does well.
  Never guess or speculate about the provider.
- NEVER state a purchase price, a per-image or per-second cost in dollars, or
  any margin. Credits are the only price the user sees.
- Voice names (Eve, Orion, Sulafat, Charon ...) ARE fine to use -- they are the
  product. The supplier behind them is not named.
- The two engines are called **Express** and **Studio** in conversation. Those
  are the names the user chooses from; lead with them rather than with a model
  name, even though a model name is not secret if asked for directly.
- Use descriptive German labels for the three capabilities: **Stimmen-Generator**
  (this skill), **Bild-Generator** (kim-images), **Video-Generator** (kim-video)
- Keep workflow smooth and conversational
