---
name: kim-voice
description: Use whenever the user wants text spoken aloud or an audio voice-over. Triggers: lies das vor, sprich das, vertone das, mach daraus Audio, Stimme, Sprecher, Sprecherin, Voiceover, Vorleser, Narration, Hoerbuch, Podcast-Intro, Ansage, als MP3, welche Stimmen gibt es, Stimme anhoeren, read this aloud, text to speech, narrate this, which voices are available. Guides Claude through an interactive workflow: list the available voices, let the user hear a free sample before spending credits, collect the text and the language, state the exact cost up front (billed per input character, so it is known in advance), call KIMASTERMIND_IMAGES voice_generate, then hand over the MP3 and warn that the download link expires after 24 hours. For still IMAGES use the kim-images skill, for VIDEO clips use the kim-video skill. Provider and model names are never mentioned.
---

# KIM Voice Skill

## Purpose

Guide the user through a complete SPEECH generation workflow using the
KIMASTERMIND_IMAGES MCP tools. Provider names are NEVER mentioned -- the
capability is called the **Stimmen-Generator**. Generated audio comes from
https://mcp.kimastermind.net/aud/ as an MP3 and is available for **24 hours
only**. Credits are shown after every generation.

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

- KIMASTERMIND_IMAGES:voice_listing -- All available voices with name, gender and
  a free sample URL. Call this FIRST when the user has not named a voice.
- KIMASTERMIND_IMAGES:voice_sample -- The sample URL for one voice (or all of
  them). Costs NO credits. Every sample speaks the same sentence, so voices are
  directly comparable.
- KIMASTERMIND_IMAGES:voice_generate -- Generate the MP3 from `text`, with
  optional `voice` and `language`. Billed per input character. Fast (~1-3 s).
- KIMASTERMIND_IMAGES:my_credits -- Current credit balance
- KIMASTERMIND_IMAGES:list_models -- All models with prices (voice model included)

Login portal: https://mcp.kimastermind.net/login

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

Call `voice_listing` and present the voices as a **table grouped by gender**, with
the sample link per voice. Do NOT dump 28 raw ids as a flat list -- that is
unusable. Mention that every voice is multilingual, so the choice is purely about
sound, not about language.

```
| Stimme | Geschlecht | Anhören |
|---|---|---|
| Eve | weiblich | https://mcp.kimastermind.net/api/voice/sample/eve.mp3 |
| Orion | männlich | https://mcp.kimastermind.net/api/voice/sample/orion.mp3 |
```

In claude.ai web / mobile, an audio widget is nicer than bare links -- see the
"Voice Picker Widget" section below.

---

## Speech Generation Workflow

### Step S0: Check What is Already Known

Never ask for something the user already gave you. Scan the request for:
- the **text** to speak (often the whole point of the message, or a document /
  earlier answer the user points at)
- a **voice** by name ("mit Eve", "eine männliche Stimme", "tiefe Stimme")
- a **language** ("auf Englisch", "in French")

If text, voice and language are all clear, skip straight to Step S3.

### Step S1: Get the Text

If no text was supplied, ask what should be spoken. If the user points at
something ("lies die Zusammenfassung vor", "vertone den Blogpost"), take that
text rather than asking them to paste it again.

**The hard limit is 5000 characters per clip.** If the text is longer:
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

### Step S2: Pick a Voice (the part users care about most)

If the user has not named a voice:

1. Call `voice_listing`.
2. Suggest **two or three** fitting voices rather than all of them, and say why,
   based on what the audio is for. Keep it short.
3. Give the sample link for each, and say explicitly that listening is free:
   "Hör gern erst rein -- die Beispiele kosten nichts."
4. Wait for the choice. Do not generate with a guessed voice: the clip costs
   credits and the user will almost always want a different voice afterwards.

If the user asks for a "deep", "warm", "friendly" or "young" voice, be honest:
the catalogue only exposes **name and gender**, so a recommendation beyond that
is a guess. Offer two samples instead of inventing characteristics.

#### Voice Picker Widget (claude.ai web / mobile)

Where widgets work, a small player beats a list of links:

```html
<div style="padding: 1rem 0;">
  <div style="background: var(--color-background-secondary); border-radius: var(--border-radius-lg); padding: 1rem;">
    <p style="font-size:14px; color: var(--color-text-primary); margin:0 0 10px; font-weight:600;">Stimmen anhören (kostenlos)</p>
    <div style="display:flex; flex-direction:column; gap:10px;">
      <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
        <span style="font-size:13px; color: var(--color-text-primary); min-width:90px;">VOICE_NAME_HERE</span>
        <audio src="https://mcp.kimastermind.net/api/voice/sample/VOICE_ID_HERE.mp3" controls preload="none" style="height:34px; flex:1; min-width:180px;"></audio>
      </div>
    </div>
    <p style="font-size:12px; color: var(--color-text-tertiary); margin:10px 0 0;">Alle Beispiele sprechen denselben Satz -- so sind sie direkt vergleichbar.</p>
  </div>
</div>
```

Repeat the inner `div` per voice. Offer two or three, not twenty-eight.

### Step S3: State the Cost BEFORE Generating

Speech is billed **per input character**, so unlike video the exact price is known
in advance -- use that. Call `list_models` or `voice_listing` for the current rate
(credits per 1000 characters), then:

```
credits = max(1, round(characters / 1000 * credits_per_1000))
```

Tell the user plainly, e.g.:

"Der Text hat 820 Zeichen -- das sind **1 Credit** und ergibt ca. 55 Sekunden
Audio. Soll ich mit der Stimme **Eve** loslegen?"

Two things to be straight about:
- **There is a 1-credit minimum per clip.** A short sentence costs the same as
  half a page. If the user is generating several short clips, mention that
  combining them into one text is cheaper.
- Generation itself is fast -- a few seconds, not minutes. No wait warning needed.

### Step S4: Generate

```
KIMASTERMIND_IMAGES:voice_generate(
  text = "Willkommen bei KI Mastermind. Hier entstehen Bilder, Videos und Stimmen aus einem einzigen Werkzeug.",
  voice = "eve",
  language = "de"
)
```

Omit `model` -- the default is the current voice model. Omit `voice` only if the
user truly has no preference. `language` defaults to `de`; set it whenever the
text is not German. Supported hints: de, en, fr, it, es, pt, nl, pl, ru, tr, ar,
hi, ja, ko, zh.

Returns `Download URL: https://mcp.kimastermind.net/aud/UUID.mp3` plus characters,
file size, credits used and remaining.

NEVER reveal the technical model name -- call it the **Stimmen-Generator**.

### Step S5: Deliver the MP3 and Warn About the 24h Window

**This is the step that must not be skipped.** The download link is valid for
**24 hours**; after that the file is deleted from the server and the link returns
an error. Always say this, and always offer to save the file locally.

- **Claude Desktop (Windows)**: save to `$env:USERPROFILE\Music\KI-Stimmen\` via
  Invoke-WebRequest (PowerShell rules: no curl, no &&, no ~).
  ```powershell
  $folder = "$env:USERPROFILE\Music\KI-Stimmen"; if (!(Test-Path $folder)) { New-Item -ItemType Directory -Path $folder | Out-Null }; Invoke-WebRequest -Uri "AUDIO_URL_HERE" -OutFile "$folder\AUDIO_FILENAME.mp3"; Get-Item "$folder\AUDIO_FILENAME.mp3" | Select-Object Name, Length
  ```
- **Claude Desktop (Mac/Linux)**: `curl -s -o ~/Music/KI-Stimmen/AUDIO_FILENAME.mp3 "AUDIO_URL_HERE"`
- **Web / Mobile / download failure**: show a widget with an HTML5 `<audio controls>`
  element, the download link, the expiry warning and the updated credit balance:

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

## What This Voice Model Cannot Do

Be upfront instead of letting the user discover it:

- **No emotion or style control.** There is no "fröhlich", "traurig", "flüsternd"
  parameter and no markup tags like `[lacht]`. Tone comes from the written text
  and the chosen voice only.
- **No speed control.** The speaking pace is effectively identical across all
  voices; only the timbre differs.
- **No custom or cloned voices.** The catalogue is fixed -- a user's own voice
  cannot be added.
- **No background music, no mixing, no muxing into video.** The output is a bare
  MP3 of the spoken text.
- **No subtitle or timestamp output.**

If the user needs any of these, say it is not available here rather than
generating something that will disappoint them.

---

## Environment Summary

| Umgebung | Download-Methode | Speicherort |
|---|---|---|
| Claude Desktop (Windows) | desktop-commander + Invoke-WebRequest | %USERPROFILE%\Music\KI-Stimmen\ |
| Claude Desktop (Mac/Linux) | bash_tool + curl | ~/Music/KI-Stimmen/ |
| claude.ai Web | nicht moeglich | Widget + Download-Link |
| Claude Mobile (iOS/Android) | nicht moeglich | Widget + Download-Link |

Bundled samples: this skill ships one sample clip per voice under
`samples/<voice_id>.mp3`, so the voices can be compared even without a network
round-trip. The served URL `https://mcp.kimastermind.net/api/voice/sample/<id>.mp3`
is the preferred way to let the user listen, because a link actually plays in
their browser while a local file in the skill folder does not.

---

## Error Handling

Unknown voice:
- The tool returns an error naming the voice. Call `voice_listing`, show the
  closest matches and let the user pick. Do not substitute a voice silently.

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
- NEVER name the technology behind a capability: no provider, vendor, lab,
  product or research name, no model family, and no technical model key -- not
  in passing, not in a comparison, and not when the user asks directly. If
  someone asks which models, which provider or which technology is used, say
  plainly that this is not disclosed and offer to help pick by result instead
  (speed, text in the image, photorealism, price). Never guess or speculate.
- Voice names (Eve, Orion, Altair ...) ARE fine to use -- they are the product,
  not the technology.
- Use descriptive German labels for the three capabilities: **Stimmen-Generator**
  (this skill), **Bild-Generator** (kim-images), **Video-Generator** (kim-video)
- Keep workflow smooth and conversational
