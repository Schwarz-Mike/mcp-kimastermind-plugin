---
name: kim-video
description: Use whenever the user wants to generate or animate a VIDEO clip. Triggers: generiere/erstelle ein Video, mach ein Video daraus, animiere dieses Bild, bring das zum Leben, Text-zu-Video, Bild-zu-Video, Reel, Clip, Kurzvideo, generate/animate a video, make this move. Guides Claude through an interactive workflow: detect the mode (text / image / reference), upload reference images via the binary upload flow, collect prompt, format, resolution and duration, warn about per-second cost AND the 1-5 minute wait, call KIMASTERMIND_IMAGES generate_video, then download or display the clip as a native video artifact. For still IMAGES use the kim-images skill, for SPEECH/text-to-voice use the kim-voice skill. Provider and model names are never mentioned.
---

# KIM Video Skill

## Purpose

Guide the user through a complete VIDEO generation workflow using the
KIMASTERMIND_IMAGES MCP tools. Provider names are NEVER mentioned -- the
capability is called the **Video-Generator**. All clips come from
https://mcp.kimastermind.net/vid/. Clips are saved locally (Claude Desktop) or
shown as a widget fallback (claude.ai web / mobile). Credits are shown after
every generation.

## Related Skills -- the KIM family

The same MCP server and the same credit balance power three skills. They are
siblings, not alternatives: if a request is not about video, hand it to the
right one instead of improvising here.

| Skill | Use it for | MCP tools |
|---|---|---|
| **kim-video** (this one) | Video clips: text-to-video, animating an image, reference-to-video | `generate_video` |
| **kim-images** | Still images: generate, edit, restyle, vary, combine | `generate_image`, `export_image`, `my_gallery` |
| **kim-voice** | Speech: text read aloud, voice-over, narration | `voice_listing`, `voice_sample`, `voice_generate` |
| **kimastermind-setup** | Einrichtung pruefen: Verbindung, Guthaben, Fehlersuche | `my_credits`, `list_models` |

Routing rules:
- "funktioniert das", "bin ich verbunden", "wie viele Credits", "geht nicht" -> **kimastermind-setup**
- "generiere ein Bild", "bearbeite das Foto", "Logo", "Grafik" -> **kim-images**
- "lies das vor", "Stimme", "Sprecher", "Voiceover", "vertonen" -> **kim-voice**
- Everything about a moving clip stays here.

A combined request is handled in sequence and announced as such. Typical chains:
- "Bild erstellen und animieren" -> kim-images, then this skill with mode `image`
- "Video mit Sprecherstimme" -> this skill, then kim-voice for the narration.
  **Note:** the MCP cannot mux audio into the clip. Deliver the MP4 and the MP3
  separately and say so -- do not imply the voice is inside the video.

`my_credits` and `list_models` are shared by all three skills.

## Available MCP Commands

- KIMASTERMIND_IMAGES:generate_video -- Generate a VIDEO clip with model, mode
  (text/image/reference), prompt, aspect_ratio, quality (720p/1080p), duration
  (3-15s), reference_images. Takes 1-5 minutes.
- KIMASTERMIND_IMAGES:request_upload_url -- PREFERRED for reference uploads.
  Returns a short-lived HTTPS URL for direct binary PUT. Avoids base64 entirely.
- KIMASTERMIND_IMAGES:upload_reference -- Fallback ONLY for tiny inline base64 (< 100 KB).
- KIMASTERMIND_IMAGES:list_models -- All models with prices, strengths, keywords
- KIMASTERMIND_IMAGES:my_credits -- Current credit balance
- KIMASTERMIND_IMAGES:my_gallery -- Gallery of up to 30 images with URLs (source frames!)

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
- **image** -- Bild-zu-Video. Animates EXACTLY ONE attached/gallery image (it becomes
  the first frame / is brought to life). Use when the user attaches one image and
  says "mach ein Video daraus", "animiere das", "bring das zum Leben".
- **reference** -- Referenz-zu-Video. Uses 1-9 reference images for subject/style
  guidance (not a strict first frame). Use when the user provides multiple images
  or wants a character/style carried into a new scene.

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

### Step V1: Collect Parameters (ask only what's missing)

1. **Prompt** -- what should happen in the video. Encourage a short shot description
   (camera movement, action, mood). "Was soll im Video passieren?"
2. **Format (aspect_ratio)** -- 16:9 (default, Querformat), 9:16 (Hochformat/Reels),
   1:1, 4:3, 3:4.
3. **Auflösung (quality)** -- 720p (Standard, günstiger) or 1080p (HD, teurer).
   Default 720p.
4. **Dauer (duration)** -- 3 to 15 seconds, default 5. Longer = more credits.

Smart defaults: Social/Reels/Stories -> 9:16; Web/YouTube -> 16:9.

In mode `image` the clip takes its dimensions from the source frame, so the
aspect ratio is not asked and not sent.

### Step V2: Inform About Cost AND Wait Time (CRITICAL)

Video is billed **per second**: cost = (credits per second for the resolution) ×
duration. A 1080p or longer clip costs noticeably more. Call
`KIMASTERMIND_IMAGES:list_models` to get the current per-second credit price, compute
the estimate, and tell the user before generating, e.g.:

"Ich erstelle jetzt ein Video (Video-Generator), 720p, 5 Sekunden -- das kostet ca.
**X Credits** und dauert erfahrungsgemäss **1-5 Minuten**. Bitte einen Moment Geduld,
ich melde mich, sobald es fertig ist."

Video generation runs synchronously and takes **longer than images (typically
1-5 minutes**, more for 1080p/long clips). Do NOT abort or retry while the call is
still running -- it is working, not stuck.

### Step V3: Generate

```
KIMASTERMIND_IMAGES:generate_video(
  prompt = "A calm coffee cup on a wooden table, steam rising, slow zoom in, cinematic",
  mode = "text",            // or "image" / "reference"
  aspect_ratio = "16:9",
  quality = "720p",
  duration = 5,
  reference_images = []     // one URL for "image"; 1-9 for "reference"; omit for "text"
)
```

Omit `model` unless the user explicitly asked for a specific one -- the default is
the current video model. Returns
`Video URL: https://mcp.kimastermind.net/vid/UUID.mp4` plus credits used/remaining.
NEVER reveal the technical model name -- call it the **Video-Generator**.

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

Note: clips are stored on the server and listed in the user's library
(auto-pruned when the per-user limit is exceeded). Unlike generated speech, video
links do **not** expire after 24 hours.

---

## Environment Summary

| Umgebung | Download-Methode | Speicherort |
|---|---|---|
| Claude Desktop (Windows) | desktop-commander + Invoke-WebRequest | %USERPROFILE%\Videos\KI-Videos\ |
| Claude Desktop (Mac/Linux) | bash_tool + curl | ~/Videos/KI-Videos/ |
| claude.ai Web | nicht moeglich | Widget + Download-Link |
| Claude Mobile (iOS/Android) | nicht moeglich | Widget + Download-Link |

---

## Error Handling

Download fails:
- Always fall back to the Step V4 widget + direct download link

Generation error or API failure:
- Credits are refunded automatically on every failure -- say so, so the user does
  not think the attempt cost them anything
- Retry once; if the second attempt also fails, inform the user

Mode mismatch:
- Mode `image` with more than one reference -> keep the first and say so
- Mode `image`/`reference` with no reference at all -> ask for an image instead of
  silently falling back to `text`

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
- Use descriptive German labels for the three capabilities: **Video-Generator**
  (this skill), **Bild-Generator** (kim-images), **Stimmen-Generator** (kim-voice)
- Keep workflow smooth and conversational
