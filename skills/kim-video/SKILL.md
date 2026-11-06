---
name: kim-video
description: "Use whenever the user wants to generate, animate or EDIT a VIDEO clip, or make a photo talk. Triggers: generiere/erstelle ein Video, mach ein Video daraus, animiere dieses Bild, bring das zum Leben, Text-zu-Video, Bild-zu-Video, Reel, Clip, Kurzvideo, Video bearbeiten, Figur austauschen, Kleidung aendern, Hintergrund ersetzen, Lippensynchron, sprechendes Portrait, Avatar, generate/animate/edit a video, make this move, lip sync, talking head. SIX models that differ in price AND in what they can do (one is a talking-portrait specialist) -- ALWAYS ask the user which one they want, explain the options and give a recommendation before generating. Guides Claude through an interactive workflow: detect the mode (text / image / reference), upload reference images, clips and voice tracks via the binary upload flow, collect prompt, format, resolution and duration, warn about per-second cost AND the 1-5 minute wait, call KIMASTERMIND_IMAGES generate_video, then download or display the clip as a native video artifact. Any CUTTING runs on the user's own machine with FFmpeg and Python, never on the server: muxing a voice-over or music under a clip, joining several clips, trimming. The skill ships the script and checks for FFmpeg before promising it. For still IMAGES use the kim-images skill, for SPEECH/text-to-voice use the kim-voice skill. Provider names are never mentioned."
version: 1.7.1
---

# KIM Video Skill

## Purpose

Guide the user through a complete VIDEO generation workflow using the
KIMASTERMIND_IMAGES MCP tools. Provider names are NEVER mentioned -- the
capability is called the **Video-Generator**. The five MODELS may be named: choosing
one is the user's decision. All clips come from
https://mcp.kimastermind.net/vid/. Clips are saved locally (Claude Desktop) or
shown as a widget fallback (claude.ai web / mobile). Credits are shown after
every generation.

## The six video models -- ALWAYS ask which one, explain, advise

There is no single video model any more. The six differ in price by a factor
of nine, and they do **different things**: only some can lip-sync or edit a
clip, only one brings its own sound, only one reaches 2K. Picking silently
either wastes the user's credits or hands them a model that cannot do the job.
So **every time a clip is about to be generated:**

1. **Ask which model the user wants.** Never choose for them and never lean on
   a default. The one exception is a model the user already NAMED in this
   conversation -- and even then check that it can do the job (table below).
2. **Explain the options** that can do the job, in plain words: what each is good
   at, what it cannot do, what a second costs. Two or three sentences, not a spec
   sheet.
3. **Advise.** Give ONE recommendation with its reason, matched to what the user
   wants (second table), and say what the alternative would change.
4. **Name what dropped out.** When the job rules models out (a voice to sync, a
   clip to edit, 2K), still show the choice among the rest and say in one line
   which ones cannot do it and why. Do not narrow silently.

| Modell (`model`) | Aufloesungen | Credits/Sek | 5 Sek. | Besonderheit |
|---|---|---|---|---|
| `minimax-h3-lite` | 480p, 768p | 2,5 / 4 | 13 / 20 | Guenstigstes der H3-Reihe. Entwuerfe und viele Clips. Kann lippensynchron und Clips bearbeiten |
| `gemini-omni-flash` | 360p, 720p, 1080p, 4K | 2,3 / 7 / 10,4 / 20,9 | 12 / 35 / 52 / 104 | **Schnell**, **Ton kommt mit**, 3 bis 15 Sekunden, Hoch- und Querformat. Kein Lip-Sync, keine Clip-Bearbeitung |
| `minimax-h3-highspeed` | 768p | 6 | 30 | Schneller als H3, Bildsprache naeher am vollen Modell. Lippensynchron und Bearbeitung moeglich |
| `minimax-h3` | 768p, 2K | 7,6 / 12,4 | 38 / 62 | Einziges mit 2K. Lippensynchron und Bearbeitung moeglich |
| `happyhorse-1.0` | 720p, 1080p | 8,3 / 14,8 | 42 / 74 | Das bisherige Modell. Weder Lip-Sync noch Bearbeitung |
| `omnihuman-1.5` | nur Bild + Tonspur | 16 je Sekunde **Tonspur** | 80 (bei 5 s) | **Sprechendes Portrait.** Ein Bild einer Person plus eine Tonspur unter 13 s, das Video ist so lang wie die Tonspur. Kein Text-zu-Video. Rechenzeit rund 45 bis 60 s je Sekunde Video |

(Several numbers mean: one per resolution, in the order listed. Always verify
with `list_models` before quoting a price -- the table is a guide, the tool is
the truth.)

**What to tell the user about `gemini-omni-flash`**, because it behaves unlike
the others:

- **The sound comes with the clip** -- ambience, effects, sometimes speech or
  music -- and there is no switch to turn it off. Good for a finished reel; a
  problem when a voice-over goes on top (in a film the cut mutes it, see
  kim-lernfilm). Whether a sentence like "ambient sound only, no speech, no music"
  in the prompt keeps it quiet has NOT been measured; do not promise it.
- **Native resolution is 720p.** 1080p and 4K are computed up from it: they cost
  1,5x and 3x and add no detail. Recommend 720p unless the user needs a bigger
  file; 360p is the cheap draft.
- **In mode `image` the format follows the photo** (landscape gives 16:9, portrait
  gives 9:16), whatever `aspect_ratio` says. Measured: a portrait photo asked for
  as 16:9 comes back as a different picture. Only 16:9 and 9:16 exist.
- **Two pictures in mode `image` are opening and closing frame** and cap the clip
  at 10 seconds. Up to 6 pictures in mode `reference`.
- **No reference clip, no reference voice track.** It cannot lip-sync to a given
  voice and cannot edit a clip. No `seed`.
- **Speed:** a 3-second clip at 360p arrived in under 20 seconds, much faster than
  the H3 models. Longer clips and higher resolutions take longer; how much longer
  has not been measured.

**What to tell the user about `omnihuman-1.5`**, a specialist unlike the rest:

- **It does one thing: a person speaks to a voice track.** ONE picture of a person
  plus ONE voice track (mode `reference`) gives a video in which that person speaks
  or sings it, with expression, mouth and hands. No text-to-video, no picture
  without a voice, no clip editing. There is **no duration setting**: the video is
  as long as the track, and the price is per second of it (16 Credits).
- **The track must be under 13 seconds.** The service takes more, but the compute
  runs 45 to 60 seconds per second of video (measured: a 3,9 s clip took under
  three minutes, a 6,6 s clip with two people almost seven) and a request that
  runs past fifteen minutes is cut off. Longer speech is cut into parts and the
  clips joined locally.
- **It runs as a JOB.** `generate_video` answers AT ONCE with a **Job ID**, and the
  credits are taken then. Say the wait up front (a 10-second clip is 8 to 10
  minutes), then call `video_status` with the Job ID about every 60 to 90 seconds
  until it says the clip is ready, and give the user the URL. **Never call
  `generate_video` again for the same clip: that charges again.** If the chat is
  closed first the clip still finishes: `video_status` (with the Job ID) or
  `my_gallery` with `kind: "videos"` hands it over later, and a job that fails
  refunds itself.
- **The picture must show a person clearly.** A picture WITHOUT a person is not
  refused: it is rendered and billed (measured). Check what was uploaded.
- **The track can be the user's OWN voice.** A recording they upload
  (`request_upload_url`, kind `audio`) works exactly like a generated voice -- the
  model does not change a voice, it only animates the mouth to it. So "my photo,
  my voice" works; "my photo, a different voice" means generating that voice first
  with `voice_generate`.
- **Two people in the picture** work only in a limited sense, measured: both
  animate and the listener turns to the speaker. There is still only ONE track,
  and which person speaks is not kept cleanly apart -- the other mouth moves too.
  There is no way to give each person their own voice. Put both voices in one track
  and say in the prompt who speaks when, and expect that to be approximate.
- `prompt` is optional and steers scene, camera and who speaks. No `aspect_ratio`
  and no `quality`: the format follows the picture.

| Was soll der Clip koennen? | Passt | Hinweis |
|---|---|---|
| Ein Foto spricht zu einer vorgegebenen Stimme (auch ein Foto des Nutzers, auch mit der eigenen Aufnahme) | `minimax-h3-lite`, `minimax-h3-highspeed`, `minimax-h3` oder `omnihuman-1.5` | H3: bis 15 s, 4 bis 7,6 Credits/s, und es bearbeitet auch Clips. OmniHuman: nur dieser eine Zweck, Tonspur unter 13 s, 16 Credits/s und viel laenger in der Rechenzeit. Omni Flash nimmt keine eigene Tonspur |
| Zwei Personen in einem Bild, eine Tonspur mit beiden Stimmen | `omnihuman-1.5` | Nur ungefaehr: beide bewegen sich, der Zuhoerer reagiert, aber wer spricht, ist nicht sauber getrennt. Eine eigene Stimme je Person gibt es nicht |
| Einen vorhandenen Clip bearbeiten (Figur, Kleidung, Hintergrund) | die drei H3-Modelle | Nur sie nehmen Referenzvideos |
| 2K | `minimax-h3` | Das einzige |
| Ton gleich im Clip, schnell, Hochformat-Reel, bis 15 Sekunden am Stueck | `gemini-omni-flash` | Ton nicht abschaltbar |
| So wenig Credits wie moeglich: Entwuerfe, viele Clips | `minimax-h3-lite` 480p oder `gemini-omni-flash` 360p | Rund 13 bzw. 12 Credits je 5 Sekunden. Omni bringt Ton mit, Lite kann Lip-Sync |
| Ein Foto animieren, ohne dass jemand spricht | jedes | Omni Flash, wenn Ton erwuenscht ist |

> **Noch offen:** welches Modell das *schoenere Bild* macht, ist nicht am eigenen
> Material verglichen, und dazu gibt es hier absichtlich keine Behauptung. Wer
> unsicher ist, bekommt den Vorschlag: **zwei Entwuerfe mit demselben Prompt**
> (`minimax-h3-lite` in 480p und `gemini-omni-flash` in 360p, zusammen rund 25
> Credits fuer je 5 Sekunden) und vergleicht selbst. Bis es Vergleichsmaterial
> gibt: nach Faehigkeit, Preis, Tempo und Ton beraten, nicht nach vermuteter
> Qualitaet.

> **Auch offen:** ob `omnihuman-1.5` oder ein H3-Modell das *natuerlichere* sprechende
> Portrait macht, ist nicht verglichen. Bei Unsicherheit der Vorschlag: **dasselbe
> Foto mit derselben Tonspur auf beiden** (`minimax-h3-lite` und `omnihuman-1.5`,
> bei 4 Sekunden zusammen rund 80 Credits) und selbst vergleichen lassen. Der
> Preisunterschied ist gross, ein Qualitaetsvorsprung nicht belegt.

A worked phrasing when the user just says "mach mir ein Video":

> "Dafuer hast du fuenf Modelle. Soll der Clip gleich Atmosphaere und Ton haben
> und schnell da sein, empfehle ich **Omni Flash** in 720p (5 Sekunden ca. 35
> Credits). Fuer einen billigen Entwurf ist **H3 Lite** die Wahl (ca. 13
> Credits), und wenn jemand sprechen oder ein Clip bearbeitet werden soll, geht
> nur ein **H3**-Modell. Welches soll es sein -- oder machen wir zwei Entwuerfe
> mit demselben Prompt und du entscheidest?"

Starting cheap and re-running is usually the better advice: a 5-second draft
costs a fraction of the same clip in the top tier, and the prompt decides most of
the result anyway.

## Related Skills -- the KIM family

The same MCP server and the same credit balance power three skills. They are
siblings, not alternatives: if a request is not about video, hand it to the
right one instead of improvising here.

| Skill | Use it for | MCP tools |
|---|---|---|
| **kim-video** (this one) | Video clips: text-to-video, animating an image, reference-to-video | `generate_video` |
| **kim-images** | Still images: generate, edit, restyle, vary, combine | `generate_image`, `export_image`, `my_gallery` |
| **kim-voice** | Speech: text read aloud, voice-over, narration. TWO engines -- the user picks Express (fast, cheap) or Studio (slower, higher quality) | `voice_listing`, `voice_sample`, `voice_generate` |
| **kim-music** | Music: background score, intro, a sung piece. TWO engines -- Advanced can sing, Basic is instrumental | `music_generate` |
| **kim-lernfilm** | A whole film: storyboard, scene images, narration, music, clips and the final cut | `film_assemble` plus all of the above |
| **kim-meditation** | A guided meditation: script, music, voice and the mix, in four approved steps | `audio_assemble` plus voice and music |
| **kim-sfx** | Sound effects and atmospheres: rain, sea, fire, a gong. Free length, billed per second | `sfx_generate` |
| **kim-avatar** | A speaking person on video: UGC reel, talking head, a photo that speaks with the user's own voice. Chooses between `gemini-omni-flash` and the lip-sync models | `generate_video`, `video_status`, `my_gallery` |
| **kimastermind-setup** | Einrichtung pruefen: Verbindung, Guthaben, Fehlersuche | `my_credits`, `list_models` |

Routing rules:
- "funktioniert das", "bin ich verbunden", "wie viele Credits", "geht nicht" -> **kimastermind-setup**
- "generiere ein Bild", "bearbeite das Foto", "Logo", "Grafik" -> **kim-images**
- "lies das vor", "Stimme", "Sprecher", "Voiceover", "vertonen" -> **kim-voice**
- Everything about a moving clip stays here.

A combined request is handled in sequence and announced as such. Typical chains:
- "Bild erstellen und animieren" -> kim-images, then this skill with mode `image`
- "Video mit Sprecherstimme" -> this skill, then kim-voice for the narration. That
  skill will ask which speech engine to use; a voice-over someone else hears is
  usually a Studio case.
  **The MCP does not mux** — it generates, it does not edit. But you can put the
  voice under the clip **on the user's machine**: see "Local post-processing"
  below. Until that has run, deliver the MP4 and the MP3 separately and say so,
  rather than implying the voice is already inside the video.

`my_credits` and `list_models` are shared by all three skills.

## Available MCP Commands

- KIMASTERMIND_IMAGES:generate_video -- Generate a VIDEO clip with model, mode
  (text/image/reference), prompt, aspect_ratio, quality (model-dependent, see the
  table above), duration (3-15s, the H3 models from 4), reference_images, and on the H3 models
  reference_videos and reference_audios. Takes 1-5 minutes.
- KIMASTERMIND_IMAGES:request_upload_url -- PREFERRED for reference uploads.
  Takes `kind`: "image" (default), "video" (a clip to edit) or "audio" (a voice
  track for lip sync). Returns a short-lived HTTPS URL for direct binary PUT.
  Avoids base64 entirely.
- KIMASTERMIND_IMAGES:upload_reference -- Fallback ONLY for tiny inline base64 (< 100 KB).
- KIMASTERMIND_IMAGES:list_models -- All models with prices, strengths, keywords
- KIMASTERMIND_IMAGES:my_credits -- Current credit balance
- KIMASTERMIND_IMAGES:video_status -- Checks a video JOB by its Job ID (`omnihuman-1.5`
  runs as a job): still running, ready with the URL, or failed and refunded.
- KIMASTERMIND_IMAGES:my_gallery -- The user's finished work with URLs: images (source
  frames!), videos (`kind: "videos"`) and speech clips (`kind: "audio"`, kept 24 h)

Login portal: https://mcp.kimastermind.net/login

---

## Handling Non-Generation Requests

### Credits Query

Trigger: credits, Guthaben, wie viel habe ich noch, my credits

Call KIMASTERMIND_IMAGES:my_credits and display:
Dein aktuelles Guthaben: X Credits
Link: https://mcp.kimastermind.net/login

---

## Video Generation Workflow

### Step V0: Detect the Mode

There are three video modes. Pick based on what the user provides/asks:

- **text** -- Text-zu-Video. No reference image. The video is generated purely
  from the text prompt. Default when no image is attached.
- **image** -- Bild-zu-Video. `reference_images[0]` becomes the OPENING frame.
  On the three H3 models and on `gemini-omni-flash` an optional
  `reference_images[1]` becomes the CLOSING frame, so the clip moves from one
  picture to another (on Omni that caps the clip at 10 s); `happyhorse-1.0` takes
  the opening frame only. On Omni the clip's format follows the photo. Use when the user attaches an image and says "mach ein
  Video daraus", "animiere das", "bring das zum Leben".
- **reference** -- Referenz-zu-Video, and on the H3 models also the mode for
  **editing a clip** and for **lip sync**. Up to 9 reference images steer
  subject, motion and style (not a strict first frame). Use when the user
  provides several images, wants a character or style carried into a new scene,
  wants an existing clip changed, or wants a portrait to speak.

Check for attached or gallery images FIRST, every turn -- the mode follows from
what is there, and asking for an image the user already attached looks careless.

### Step V0.5: Upload Reference Images (modes "image" and "reference")

For ALL real-world reference images (attachments from the + button, photos,
gallery frames): **use the `request_upload_url` flow, NOT `upload_reference`.**
Inlining base64 into any tool call makes Claude's tool-call pipeline truncate or
hit token limits above ~50-100 KB.

1. **Get a file path on disk.** + attachments may already be in
   `/mnt/user-data/uploads/` (web sandbox) or exist only as base64 (Desktop). If
   only base64 is available, materialize it first:
   - PowerShell (Desktop / Windows): `[IO.File]::WriteAllBytes("$env:TEMP\ref.png", [Convert]::FromBase64String($b64))`
   - bash sandbox: `echo "$b64" | base64 -d > /tmp/ref.png`
2. **Call `KIMASTERMIND_IMAGES:request_upload_url`** (no args). You get
   `upload_url` (single-use, 5 min TTL), `ref_url` (the public URL to pass on),
   `method` (always PUT) and ready-made curl/PowerShell examples.
3. **PUT the binary to upload_url**, matching the real Content-Type
   (image/png, image/jpeg or image/webp -- a wrong type is a 400):
   - bash: `curl -X PUT -H "Content-Type: image/png" --data-binary @ref.png "<upload_url>"`
   - PowerShell: `Invoke-WebRequest -Uri "<upload_url>" -Method Put -ContentType "image/png" -InFile "C:\path\ref.png"`
4. **Verify HTTP 2xx.** On 4xx/5xx, go back to step 2 -- the token is single-use
   and already burned.
5. **Pass `ref_url` in `generate_video.reference_images`.** Never pass
   `upload_url` -- that is for the upload only.

Gallery and external HTTPS URLs need no upload: pass them straight through.
For mode `image` pass **exactly one** URL; for `reference` pass 1-9.

### Step V0.6: Video editing and lip sync (H3 models; lip sync also `omnihuman-1.5`)

Both run through mode `reference`, and both need a file the server can reach.
`reference_videos` and `reference_audios` accept **only HTTPS URLs on
mcp.kimastermind.net** -- an external link is refused, by design. Three sources
qualify:

1. a clip from the user's own library (`https://mcp.kimastermind.net/vid/...`),
2. speech this server produced (`https://mcp.kimastermind.net/aud/...`),
3. anything uploaded with `request_upload_url`, `kind="video"` or `kind="audio"`.

The upload works exactly like the image flow in Step V0.5, with the kind set and
the real Content-Type on the PUT:

```
request_upload_url(kind = "video")    ->  upload_url, ref_url
curl -X PUT -H "Content-Type: video/mp4" --data-binary @clip.mp4 "<upload_url>"
# PowerShell:
Invoke-WebRequest -Uri "<upload_url>" -Method Put -ContentType "video/mp4" -InFile "C:\path\clip.mp4"
```

Accepted: MP4, MOV, WebM up to 60 MB; MP3, M4A, WAV, OGG up to 20 MB. Clips and
voice tracks must be **2 to 15 seconds**, at most 15 seconds per kind in total.

**Video bearbeiten** -- "tausche die Figur aus", "andere Kleidung", "anderer
Hintergrund", "mach aus dem Greenscreen eine Kueche":

```
generate_video(
  model = "minimax-h3-lite",
  mode = "reference",
  prompt = "Replace the background with a bright modern kitchen, keep the person and the camera motion unchanged",
  reference_videos = ["https://mcp.kimastermind.net/ref/<user>/<id>.mp4"],
  duration = 5, quality = "768p"
)
```
No reference image is needed here -- the clip takes its place. **Warning about
the price:** on `minimax-h3` the seconds of the reference clip are added to the
billed duration, so editing a 5-second clip into a 5-second result is charged
like 10 seconds. On Lite and Highspeed only the output is billed. Say this
before generating.

**Lippensynchronisation / sprechendes Portrait** -- the HeyGen-style case, "lass
mein Foto sprechen", "Avatar", "Talking Head":

1. Produce the speech first. Hand the text to **kim-voice** (`voice_generate`)
   and keep the URL it returns -- it is already on our host, so no upload.
   Keep it under 15 seconds, because that is the ceiling for a reference track.
   For a longer talk, cut the text into pieces of at most 15 seconds, render one
   clip per piece, and tell the user the pieces arrive separately.
2. Get the portrait in as a reference image (Step V0.5).
3. Then:

```
generate_video(
  model = "minimax-h3-lite",
  mode = "reference",
  prompt = "The person speaks to the camera, natural head movement, friendly expression, static shot",
  reference_images = ["https://mcp.kimastermind.net/img/ref/<user>/<id>.jpg"],
  reference_audios = ["https://mcp.kimastermind.net/aud/<id>.mp3"],
  duration = 10, quality = "768p"
)
```

Rules that the server enforces, so do not fight them:
- a voice track **never** stands alone -- it needs an image or a clip beside it,
- `reference_videos`/`reference_audios` work in mode `reference` only; in mode
  `image` they are refused,
- `happyhorse-1.0` and `gemini-omni-flash` take neither. If the user asks for
  editing or lip sync on one of them, say why it cannot and offer an H3 model,
  with its price. Do not switch silently: the choice is the user's.

Set `duration` to the length of the voice track, rounded up. A clip shorter than
the audio cuts the sentence off.

#### `omnihuman-1.5`: the talking portrait

Its own, shorter recipe, because it takes nothing else:

```
KIMASTERMIND_IMAGES:generate_video(
  model = "omnihuman-1.5",
  mode = "reference",
  prompt = "",                     // optional: scene, camera, who speaks
  reference_images = [<ONE portrait>],
  reference_audios = [<ONE voice track, under 13 s>]
)
```

No `duration`, no `quality`, no `aspect_ratio`: the server measures the track and
bills 16 Credits per second of it, rounded up. The call returns a **Job ID**, not
the clip: follow it with `video_status` (see above). Work out the price from the
track's length and tell the user BEFORE the call, together with the wait (45 to 60
seconds per second of video). The voice comes from `voice_generate`, or from a file
the user uploads with `request_upload_url` (kind `audio`); a track of 13 seconds or
more is refused before any credit is taken, and the answer is to cut it into
parts. Check the picture shows a person: one without is billed anyway.

### Step V1: Collect Parameters (ask only what's missing)

1. **Prompt** -- what should happen in the video. Encourage a short shot description
   (camera movement, action, mood). "Was soll im Video passieren?"
2. **Format (aspect_ratio)** -- 16:9 (default, Querformat), 9:16 (Hochformat/Reels),
   1:1, 4:3, 3:4. `gemini-omni-flash` knows only 16:9 and 9:16.
3. **Auflösung (quality)** -- depends on the model, so never offer a value the
   chosen model does not have: `minimax-h3-lite` 480p/768p, `minimax-h3-highspeed`
   768p only, `minimax-h3` 768p/2k, `happyhorse-1.0` 720p/1080p,
   `gemini-omni-flash` 360p/720p/1080p/4k. Omit the parameter to take the
   model's default.
4. **Dauer (duration)** -- 4 to 15 seconds (happyhorse and Omni Flash from 3), default 5.
   Longer = more credits, linearly. `omnihuman-1.5` has no duration: the voice
   track is the length.

Smart defaults: Social/Reels/Stories -> 9:16; Web/YouTube -> 16:9.

In mode `image` the clip takes its dimensions from the source frame (on Omni
Flash from the photo's orientation), so the aspect ratio is not asked and not
sent.

### Step V2: Inform About Cost AND Wait Time (CRITICAL)

Video is billed **per second**: cost = (credits per second for the resolution) ×
duration. A higher resolution or a longer clip costs noticeably more, and on
`minimax-h3` the seconds of a reference clip are billed on top. Call
`KIMASTERMIND_IMAGES:list_models` to get the current per-second credit price, compute
the estimate, and tell the user before generating, e.g.:

"Ich erstelle jetzt ein Video (Video-Generator), 720p, 5 Sekunden -- das kostet ca.
**X Credits** und dauert erfahrungsgemäss **1-5 Minuten**. Bitte einen Moment Geduld,
ich melde mich, sobald es fertig ist."

Video generation runs synchronously and takes **longer than images (typically
1-5 minutes** on the H3 models and `happyhorse-1.0`, more for 1080p/long clips;
`gemini-omni-flash` is usually quicker, but still tell the user to expect a wait;
`omnihuman-1.5` is the slowest by far, 45 to 60 seconds per second of video, and
runs as a job instead of a wait: see Step V0.6). Do NOT abort or retry while the call is
still running -- it is working, not stuck.

### Step V3: Generate

```
KIMASTERMIND_IMAGES:generate_video(
  model = "minimax-h3-lite",   // the one the user chose; the default is still happyhorse-1.0
  prompt = "A calm coffee cup on a wooden table, steam rising, slow zoom in, cinematic",
  mode = "text",            // or "image" / "reference"
  aspect_ratio = "16:9",
  quality = "768p",
  duration = 5,
  reference_images = [],    // [opening] or [opening, closing] for "image"; 1-9 for "reference"; omit for "text"
  reference_videos = [],    // "reference" on H3 only: a clip to edit against
  reference_audios = []     // "reference" on H3 and omnihuman-1.5: the voice track for lip sync
)
```

**Pass `model` explicitly -- the one the user chose in the choice step.** The
tool still defaults to `happyhorse-1.0`, which is not what the user picked unless
they said so and cannot edit or lip-sync -- so leaving it out quietly picks the
wrong one for most requests. Returns
`Video URL: https://mcp.kimastermind.net/vid/UUID.mp4` plus credits used/remaining.
The model's name may be said -- it is the choice the user makes. The supplier
behind it, the endpoints and the prices we pay are never mentioned; the
capability as a whole is the **Video-Generator**.

### Step V4: Download and Display the Video

- **Claude Desktop (Windows)**: save to `$env:USERPROFILE\Videos\KI-Videos\` via
  Invoke-WebRequest (PowerShell rules: no curl, no &&, no ~).
  ```powershell
  $folder = "$env:USERPROFILE\Videos\KI-Videos"; if (!(Test-Path $folder)) { New-Item -ItemType Directory -Path $folder | Out-Null }; Invoke-WebRequest -Uri "VIDEO_URL_HERE" -OutFile "$folder\VIDEO_FILENAME.mp4"; Get-Item "$folder\VIDEO_FILENAME.mp4" | Select-Object Name, Length
  ```
- **Claude Desktop (Mac/Linux)**: `curl -s -o ~/Videos/KI-Videos/VIDEO_FILENAME.mp4 "VIDEO_URL_HERE"`
- **Web / Mobile / download failure**: show a widget with an HTML5 `<video controls>`
  element pointing at the URL, plus a direct download link and the updated credit balance:

```html
<div style="padding: 1rem 0;">
  <div style="background: var(--color-background-secondary); border-radius: var(--border-radius-lg); padding: 1rem;">
    <video src="VIDEO_URL_HERE" controls playsinline style="width:100%; border-radius: var(--border-radius-md); display:block; background:#000;"></video>
    <div style="margin-top: 12px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
      <p style="font-size:13px; color: var(--color-text-secondary); margin:0;">Format: RATIO_HERE &middot; Auflösung: QUALITY_HERE &middot; Dauer: DURATION_HERE s</p>
      <a href="VIDEO_URL_HERE" target="_blank" style="font-size:13px; color: var(--color-text-info); text-decoration:none;">&#x2B07; Herunterladen</a>
    </div>
    <div style="margin-top:10px; padding:8px 10px; background: var(--color-background-primary); border-radius: var(--border-radius-md); border:0.5px solid var(--color-border-tertiary); display:flex; justify-content:space-between; align-items:center;">
      <span style="font-size:13px; color: var(--color-text-secondary);">Guthaben: <strong style="color: var(--color-text-primary);">CREDITS_HERE Credits</strong></span>
      <a href="https://mcp.kimastermind.net/login" target="_blank" style="font-size:12px; color: var(--color-text-info); text-decoration:none;">Aufladen &#x2197;</a>
    </div>
  </div>
</div>
```

Also show the plain link: 📥 Direktlink: https://mcp.kimastermind.net/vid/UUID.mp4

Note: clips are stored on the server and listed in the user's library. Unlike
generated speech, video links do **not** expire after 24 hours: the newest **50
films** are kept for as long as the account exists, and anything beyond that is
kept 30 days, announced by email, and deleted 7 days after that mail. No film
ever disappears without the owner having been written to a week earlier.

---

## Local post-processing — voice under the clip, joining clips

The server **generates**; it does not edit. Cutting is plain computation on
files the user gets anyway, and doing it on the server made every other customer
wait. So it runs on the user's machine, with the script this skill ships:
`scripts/film_cut.py` (the same one kim-lernfilm uses — one scene is exactly the
"put this voice under this clip" case).

Reach for it when the user wants any of:
- a voice-over or music **inside** the clip instead of beside it,
- several clips **joined** into one file,
- a clip **stretched** to the length of its narration — it is slowed down and
  the missing frames are computed from the motion (`minterpolate`), so it keeps
  moving instead of freezing on the last frame. Above about x1.5 that reads as
  slow motion, so a clip should be ordered at the length it will need,
- a **still image with a camera move** (slow zoom or pan, subpixel-accurate) as
  a scene of its own,
- a **caption** burned in as a lower third (`overlays` in the manifest).

### Step L1: Check FFmpeg and Python — and ask before installing

```
python film_cut.py check
```

Prints the versions of Python, ffmpeg, ffprobe and Pillow and ends with
`BEREIT` or `NICHT BEREIT`. If the command does not run at all, Python is
missing. **Pillow is listed separately** because only two things need it: a
still image with a camera move, and a burned-in caption. Putting a voice under
a clip works without it.

**Nothing gets installed without asking.** Say what is missing, what it is for,
and wait for an explicit yes:

> "Damit die Stimme im Video landet, brauche ich FFmpeg auf deinem Rechner — das
> Zusammenfuegen laeuft lokal bei dir, nicht auf dem Server. Installieren mit
> `winget install Gyan.FFmpeg`. Soll ich das ausfuehren?"

| System | Befehl |
|---|---|
| Windows | `winget install Gyan.FFmpeg` |
| macOS | `brew install ffmpeg` |
| Linux (Debian/Ubuntu) | `sudo apt install ffmpeg` |
| Python fehlt (Windows) | `winget install Python.Python.3.12` |
| Pillow fehlt (Standbild, Text) | `python -m pip install pillow` |

After a yes, install, run `check` again, and **remember that it is there** — do
not ask again on the next clip. After a no, hand over the MP4 and the MP3
separately and say plainly that they stay separate. The cut is **not** moved to
the server.

### Step L2: A manifest, then two commands

In a working folder, e.g. `%USERPROFILE%\Videos\KI-Videos\<thema>/`:

```json
{
  "out": "clip-mit-stimme.mp4",
  "subtitles": "none",
  "music": "https://mcp.kimastermind.net/aud/<id>.mp3",
  "scenes": [
    {
      "video": "https://mcp.kimastermind.net/vid/<id>.mp4",
      "voice": "https://mcp.kimastermind.net/aud/<id>.mp3"
    }
  ]
}
```

```
python film_cut.py fetch manifest.json
python film_cut.py cut manifest.json
```

`fetch` downloads every URL into the folder and rewrites the manifest to point
at the local files — worth doing immediately, because generated speech and music
are deleted from the server after 24 hours.

What `cut` does by itself: levels the narration to a fixed loudness, keeps the
clip's own ambience quietly underneath instead of muting it, ducks the music
while someone speaks, fades the music out at the end, and — when the narration
outlasts the picture — stretches the clip with motion interpolation instead of
freezing its last frame, stretching the ambience along with it. Every scene is
brought to the size and frame rate of the first clip, because clips from
different models do not share a frame rate.

**It takes a while.** Interpolation computes every in-between frame: roughly one
to two minutes per scene. Start the command in the background and say so,
rather than letting the user watch a frozen prompt.

**To join several clips**, list them as several scenes, in order. Each may carry
its own `voice`. Leave `music` out if there is none, or set `"musicVolume": 0`.

**For subtitles** set `"subtitles": "file"` (an .srt next to the video) or
`"burn"` (written into the picture), and give each scene a `subtitle` text.

**A still image instead of a clip**: give the scene `image` instead of `video`,
plus `motion` (`zoom_in` by default, also `zoom_out`, `pan_left`, `pan_right`,
`pan_up`, `pan_down`, `none`) and optionally `zoom` (strength, default 0.12) and
`zoomBase`. The camera moves subpixel-accurate, so it does not jump the way
ffmpeg's `zoompan` does. Length comes from the voice track, or from `seconds`.

**A caption**: an `overlays` block next to `scenes`, e.g.
`[{ "scene": 1, "title": "Kapitel 1", "sub": "Worum es geht", "at": 0.6 }]`.
`scene` counts from 1, `at` is seconds after the scene starts. Needs Pillow and
a system font; without either the caption is skipped and the video still
finishes, with a note at the end.

The full manifest is documented in the script's own docstring
(`python film_cut.py` without arguments prints it).

### What it costs

Nothing. No credits, no server time. A failed cut costs nothing either — the
material is already local, so say that instead of letting the user think they
have to generate again.

---

## Environment Summary

| Umgebung | Download-Methode | Speicherort |
|---|---|---|
| Claude Desktop (Windows) | desktop-commander + Invoke-WebRequest | %USERPROFILE%\Videos\KI-Videos\ |
| Claude Desktop (Mac/Linux) | bash_tool + curl | ~/Videos/KI-Videos/ |
| claude.ai Web | nicht moeglich | Widget + Download-Link |
| Claude Mobile (iOS/Android) | nicht moeglich | Widget + Download-Link |

Der Schnitt braucht einen echten Rechner. Auf Web und Mobil gibt es ihn nicht —
dort bleiben MP4 und MP3 getrennt, und das gehoert gesagt statt umgangen.

---

## Error Handling

Download fails:
- Always fall back to the Step V4 widget + direct download link

Generation error or API failure:
- Credits are refunded automatically on every failure -- say so, so the user does
  not think the attempt cost them anything
- Retry once; if the second attempt also fails, inform the user

Mode mismatch:
- Mode `image` with more references than the model takes (1 on happyhorse, 2 on
  the H3 models and on Omni Flash) -> keep the allowed ones and say so
- Mode `image` with no reference at all -> ask for an image instead of silently
  falling back to `text`
- Mode `reference` with neither an image nor a clip -> ask; a clip alone is fine
  on the H3 models

Model cannot do what was asked:
- Editing a clip or lip sync on `happyhorse-1.0` or `gemini-omni-flash` -> the
  server refuses it. Say that this model cannot do it, offer an H3 model with its
  price, and let the user decide
- The request was refused by the content filter (the message says the video
  request was rejected by the content safety filter) -> nothing was charged. Tell
  the user to rephrase the prompt or use a different picture; a photo of a person
  is the likeliest trigger
- `omnihuman-1.5` called without exactly one picture and one voice track, or in
  mode `text`/`image` -> the answer names the recipe; ask for the missing piece
- The chat shows a timeout, or no answer, for a model that runs as a job -> it did
  NOT fail. Ask `video_status` with the Job ID; if the id is lost, `my_gallery` with
  `kind: "videos"` lists the finished clips. Do not generate again
- "The voice track is N seconds long" (13 s or more) -> nothing was charged; cut
  the speech into parts of under 13 s and join the clips locally
- A talking portrait that shows no person -> the service does NOT refuse it, so it
  was rendered and billed. Say so plainly, and check the picture before the next run
- 2K on anything but `minimax-h3` -> offer `minimax-h3` or the model's own top
  resolution

Reference clip or voice track rejected as "must be hosted on
mcp.kimastermind.net":
- the URL points somewhere else. Upload the file with
  `request_upload_url(kind="video"/"audio")`, or take the clip from the user's
  library and the voice from `voice_generate`

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
- Use descriptive German labels for the three capabilities: **Video-Generator**
  (this skill), **Bild-Generator** (kim-images), **Stimmen-Generator** (kim-voice)
- Keep workflow smooth and conversational
