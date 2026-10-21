---
name: kim-images
description: "Use whenever the user wants to generate, edit, restyle, vary or combine an IMAGE, attaches images asking to modify them, references their gallery, or asks about credits. Triggers: generiere/erstelle/bearbeite/aendere ein Bild, mache eine Variante, kombiniere Bilder, im Stil von, Logo, Grafik, Foto, generate/edit/restyle this image; meine Galerie, zeig meine Bilder, Credits/Guthaben. Guides Claude through an interactive workflow: detect attached or gallery reference images first, collect prompt/style/format/quality, recommend suitable models (reference-capable when refs are present), call KIMASTERMIND_IMAGES generate_image with up to 16 reference images, and display results as native image artifacts. For VIDEO clips use the kim-video skill, for SPEECH/text-to-voice use the kim-voice skill. Provider and model names are never mentioned."
version: 1.1.0
---

# KIM Images Skill

## Purpose

Guide the user through a complete IMAGE generation workflow using the KIMASTERMIND_IMAGES MCP tools. Provider names are NEVER mentioned. All images come from https://mcp.kimastermind.net/img/. Images are saved locally (Claude Desktop / Windows) or shown as widget fallback (claude.ai web / mobile). Credits are shown after every generation.

## Related Skills -- the KIM family

The same MCP server and the same credit balance power three skills. They are
siblings, not alternatives: if a request is not about still images, hand it to
the right one instead of improvising here.

| Skill | Use it for | MCP tools |
|---|---|---|
| **kim-images** (this one) | Still images: generate, edit, restyle, vary, combine | `generate_image`, `export_image`, `my_gallery` |
| **kim-video** | Video clips: text-to-video, animating an image, reference-to-video | `generate_video` |
| **kim-voice** | Speech: text read aloud, voice-over, narration. TWO engines -- the user picks Express (fast, cheap) or Studio (slower, higher quality) | `voice_listing`, `voice_sample`, `voice_generate` |
| **kimastermind-setup** | Einrichtung pruefen: Verbindung, Guthaben, Fehlersuche | `my_credits`, `list_models` |

Routing rules:
- "funktioniert das", "bin ich verbunden", "wie viele Credits", "geht nicht" -> **kimastermind-setup**
- "mach ein Video daraus", "animiere das", "Text-zu-Video", "Reel", "Clip" -> **kim-video**
- "lies das vor", "Stimme", "Sprecher", "Voiceover", "Audio", "vertonen", "Podcast" -> **kim-voice**
- Everything about a still picture stays here.

A combined request ("Bild erstellen und dann vertonen") is handled in sequence:
generate the image here, then invoke the sibling skill for the second half. Say
so plainly rather than silently doing only one half. `my_credits` and
`list_models` are shared by all three.

## Available MCP Commands

- KIMASTERMIND_IMAGES:generate_image -- Generate image with model, prompt, aspect ratio, quality, reference_images
- KIMASTERMIND_IMAGES:generate_video -- VIDEO clips. Not handled here: use the **kim-video** skill.
- KIMASTERMIND_IMAGES:voice_listing / voice_sample / voice_generate -- SPEECH, with a
  choice of two engines. Not handled here: use the **kim-voice** skill.
- KIMASTERMIND_IMAGES:request_upload_url -- PREFERRED for reference uploads. Returns short-lived HTTPS URL for direct binary POST (curl --data-binary). Avoids base64-in-tool-call entirely.
- KIMASTERMIND_IMAGES:upload_reference -- Fallback ONLY for tiny inline base64 (< 200 KB). Slower because the bytes go through MCP/SSE.
- KIMASTERMIND_IMAGES:list_models -- All models with prices, strengths, keywords
- KIMASTERMIND_IMAGES:my_credits -- Current credit balance
- KIMASTERMIND_IMAGES:my_gallery -- The user's gallery with URLs, model, prompt, date

Login portal: https://mcp.kimastermind.net/login

---

## Handling Non-Generation Requests

### Credits Query

Trigger: credits, Guthaben, wie viel habe ich noch, my credits

Call KIMASTERMIND_IMAGES:my_credits and display:
Dein aktuelles Guthaben: X Credits
Link: https://mcp.kimastermind.net/login

### Gallery Query

Trigger: Galerie, meine Bilder, zeig meine Bilder, my gallery, generated images

Call KIMASTERMIND_IMAGES:my_gallery then display as visual grid via visualize:show_widget.
Do NOT show model names -- use KI-Generator instead.

Gallery widget HTML template:

```html
<div style="padding: 1rem 0;">
  <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 12px;">
    <div style="background: var(--color-background-secondary); border-radius: var(--border-radius-md); overflow: hidden;">
      <img src="IMAGE_URL" style="width:100%; display:block; aspect-ratio:1; object-fit:cover;" />
      <div style="padding: 8px;">
        <p style="font-size: 11px; color: var(--color-text-secondary); margin: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">PROMPT_HERE</p>
        <p style="font-size: 11px; color: var(--color-text-tertiary); margin: 4px 0 0;">DATE_HERE</p>
      </div>
    </div>
  </div>
</div>
```

---

### How long images are kept (ask-and-answer)

Trigger: wie lange bleiben meine Bilder, werden Bilder geloescht, Speicherdauer,
how long are my images kept, do images get deleted

- The newest **100 images** and **50 films** per user stay for as long as the
  account does, however old they get.
- Anything beyond that stays **30 days**. Then the owner gets an **email**, and
  deletion follows **7 days after that email** -- 37 days at the earliest.
- **Nothing is deleted without that mail having gone out a week earlier.** If the
  mail cannot be sent, the file stays.
- Files whose mail has gone out are marked in the library at
  https://mcp.kimastermind.net/login with the date they go, so they are easy to
  find and download.
- Uploaded reference images: **30 days**, no mail (they are an input, not a
  deliverable).
- Generated speech is the exception and still **24 hours** -- see kim-voice.

Until 21.10.2026 this was a hard cap instead: the newest 30 images, enforced the
moment a new one was written, so a batch of ten deleted the ten oldest on the
spot. If a user says older images or their reference URLs vanished, that is why,
and it is fixed -- but what was deleted then is gone and has to be generated
again.

---

## Image Generation Workflow

### Step 0: Check What is Already Known

Only ask for what is genuinely missing. If the user already provided prompt AND aspect ratio AND style AND quality AND model -- skip directly to Step 7.

---

### Step 0.5: Detect Reference Images (CRITICAL -- check FIRST every turn)

Before anything else, check if the user has attached image(s) to this turn or
referenced images from their gallery. This drives model selection later.

Sources of reference images:
1. **Plus-button attachments in Claude Desktop** -- the user clicked + and added one or more
   image files. In your tool call, pass each as a base64 data URL of the form
   `data:image/(png|jpeg|webp);base64,<base64-string>`. Claude will substitute the
   actual image data automatically when you reference attached images in tool args.
2. **Gallery references** -- the user says things like "wie das gestrige Bild",
   "das letzte Foto", "Bild Nummer 3 aus meiner Galerie". Call
   KIMASTERMIND_IMAGES:my_gallery, identify the right entry, and use its
   `https://mcp.kimastermind.net/img/<uuid>.jpg` URL as a reference.
3. **External HTTPS URLs** -- the user pasted a public image URL. Use it directly.

If reference image(s) are present, set the user intent to one of:
- **Edit** -- modify the existing image (change colors, remove/add objects, replace text).
- **Style transfer** -- adopt style/mood/colors from a reference for a new image.
- **Composition** -- combine multiple reference images (Marketing-Spezialist only).
- **Variation** -- generate similar image based on the reference.

How to detect intent:
- "bearbeite", "aendere", "ersetze X durch Y", "entferne", "edit", "modify" -> Edit
- "im Stil von", "wie dieses", "Stimmung wie", "in this style" -> Style transfer
- "kombiniere", "fuege zusammen", "mit Hintergrund von Bild 2" -> Composition
- "Variante", "aehnliches Bild", "anderes Bild davon" -> Variation

Confirm briefly with the user: "Ich sehe X Referenzbild(er). Soll ich [Edit/Stiltransfer/Komposition/Variante] machen?"

Do NOT ask about reference images if none were provided. Skip this step silently in that case.

#### Step 0.5b: Upload Reference Images (PREFERRED: HTTP binary upload)

For ALL real-world reference images (logos, photos, attachments from + button):
**use the `request_upload_url` flow, NOT `upload_reference`.** Inlining base64
into ANY tool call (including upload_reference) causes Claude's tool-call
pipeline to truncate or hit token limits for files larger than ~50-100 KB.

**Recommended flow (presigned URL + binary HTTP upload — no base64 anywhere):**

1. **Get an attachment file path on disk.** + attachments may already be in
   `/mnt/user-data/uploads/` (web sandbox) or be base64 only (Desktop). If only
   base64 is available, materialize it to a temp file first:
   - PowerShell (Desktop / Windows): `[IO.File]::WriteAllBytes("$env:TEMP\ref.png", [Convert]::FromBase64String($b64))`
   - bash sandbox: `echo "$b64" | base64 -d > /tmp/ref.png`

2. **Call `KIMASTERMIND_IMAGES:request_upload_url`** (no args). The response
   contains:
   - `upload_url` — where to PUT the binary (single-use HMAC token, 5 min TTL)
   - `ref_url` — the public reference URL for `generate_image` (known up-front)
   - `method` — always `"PUT"`
   - `curl_example` and `powershell_example` — copy-paste ready

3. **PUT the binary directly to upload_url.** Use whatever shell is available:
   - **bash / curl:**
     `curl -X PUT -H "Content-Type: image/png" --data-binary @ref.png "<upload_url>"`
   - **PowerShell (Claude Desktop on Windows):**
     `Invoke-WebRequest -Uri "<upload_url>" -Method Put -ContentType "image/png" -InFile "C:\path\to\ref.png"`
   Always match the Content-Type to the actual file format
   (image/png, image/jpeg, or image/webp). Wrong type = 400.

4. **Verify HTTP 2xx** in the response. The body JSON is:
   `{ url, ref_url, expires_at, size_bytes }` — `url` and `ref_url` are
   identical and match the `ref_url` you got in step 2. On 4xx/5xx, retry
   step 2 (the token is single-use and already burned).

5. **Pass `ref_url` into `generate_image.reference_images`.** Do NOT pass the
   `upload_url` — that's only for the upload itself, not for the model.

**Why HTTP binary upload is faster:** the image bytes never pass through MCP's
JSON-RPC / SSE pipe. They stream directly via standard HTTP. A 5 MB image takes
~1 second instead of timing out the tool call.

**Use the legacy `upload_reference` MCP tool ONLY when:**
- The image is < 100 KB raw and easy to inline as a small base64 string.
- desktop-commander / shell access is not available in the session.

**Skip uploads entirely when:**
- The reference is already an `https://...` URL (gallery via `my_gallery`,
  external public URL). Pass the URL through unchanged.

For each `+` attachment from Claude Desktop:

1. Build the base64 data URL once: `data:image/(jpeg|png|webp);base64,<BASE64>`
   — Claude Desktop substitutes the actual image data when you reference an
   attached image inside a tool call argument. Even multi-MB images work here
   because upload_reference is the only place where the big string lives;
   it never reaches generate_image.

2. Call `KIMASTERMIND_IMAGES:upload_reference(image_base64 = "...", mime_type = "image/png", filename = "logo.png")`.
   - `image_base64`: either a full data URL (data:image/png;base64,...) OR raw base64
     without prefix. Both work.
   - `mime_type`: only needed if you sent raw base64 (no data: prefix). One of
     image/png, image/jpeg, image/webp.
   - `filename`: optional, useful for debug logs.

   The server:
   - Decodes the base64 (max 15 MB after decoding)
   - Resizes to max 1024 px longest edge (preserves aspect, never upscales)
   - Re-encodes as JPEG quality 80 (with EXIF rotation honored)
   - Stores at `data/refs/{userId}/{uuid}.jpg` (auto-purged after 24 h)
   - Returns JSON: `{ url, expires_at, size_bytes, filename }`

3. Collect all returned URLs. Then call `generate_image` with
   `reference_images = [<url1>, <url2>, ...]`.

**Why this matters:** if you inline a 2 MB image as base64 into the
generate_image call, the call payload becomes ~2.7 MB and may hit Claude's
input limits or simply be slow. With upload_reference, the generate_image
call only contains short HTTPS URLs (~80 chars each).

**Skip upload_reference ONLY when:**
- The reference is already an `https://...` URL (gallery item via my_gallery,
  or external public URL). Pass the URL through unchanged.
- The user explicitly says "use the original full-resolution file" AND the
  image is small (< 500 KB raw).

**If upload_reference fails (e.g. file > 15 MB):**
- Tell the user: "Das Bild ist zu gross. Bitte ein Bild unter 15 MB hochladen."
- Do NOT fall back to inlining base64 in generate_image — that will be worse.

---

### Step 1: Ask What to Generate (if missing)

Ask: Was soll auf dem Bild zu sehen sein? Beschreibe es so genau wie moeglich.

---

### Step 2: Ask for Usage (if missing)

Use ask_user_input_v0 or inline list. User may also type freely.

1. Website / Landingpage
2. Blogbeitrag / Artikel
3. Social Media Post (Instagram, Facebook, LinkedIn)
4. PDF / Print / Flyer
5. Praesentation / Slides
6. E-Mail / Newsletter
7. YouTube-Thumbnail / Cover
Plus free text field.

---

### Step 3: Ask for Style (if missing)

1. Photorealistisch - wie ein echtes Foto
2. Comic / Illustration - zeichnerisch, cartoon-artig
3. Kunst / Fine Art - malerisch, kuenstlerisch
4. Minimalistisch - clean, reduziert, modern
5. Cinematic - dramatisch, filmisch, atmosphaerisch
6. Kindgerecht / Freundlich - weich, bunt, einladend
Plus free text field.

---

### Step 4: Ask for Quality (if missing)

1. Niedrig - schnell und guenstig (Entwuerfe)
2. Mittel - ausgewogen (Standard Web)
3. Hoch - detailreich (Print, Marketing)
4. Sehr hoch - maximale Qualitaet (Premium)

Map: Niedrig->0.5K/low, Mittel->1K/medium, Hoch->2K/high, Sehr hoch->4K/premium

---

### Step 5: Ask for Format (if missing)

1. 1:1 - Quadrat
2. 16:9 - Querformat
3. 9:16 - Hochformat
4. 4:3 - Klassisch Quer
5. 3:4 - Klassisch Hoch
6. 21:9 - Ultrabreit / Cinematic
Plus free text field.

Mapping: 1->1:1, 2->16:9, 3->9:16, 4->4:3, 5->3:4, 6->21:9

Smart defaults: Website/Blog->16:9, Social->1:1, Stories->9:16, Print->4:3, YouTube->16:9

---

### Step 6: Present 4 Recommended Models for the User to Choose (if no model specified)

Call KIMASTERMIND_IMAGES:list_models to get fresh model data with current prices.

Based on the user inputs (style, quality, usage, prompt content), select the 4 most suitable models.
Present them to the user using ask_user_input_v0 or an inline list.
Include a descriptive German label, one-line strength, and price per image in Credits for each.

Example presentation format:

Welchen KI-Generator moechtest du verwenden?

1. Fotorealist-Generator -- perfekt fuer naturgetreue Fotos -- ca. 20 Credits
2. Text-Spezialist -- ideal wenn Text im Bild vorkommt -- ca. 25 Credits
3. Schnell-Generator -- guenstig und schnell fuer Entwuerfe -- ca. 2 Credits
4. Premium-Generator -- hoechste Qualitaet bis 4K -- ca. 27 Credits

Oder schreib selbst, welchen Generator du moechtest.
Alle verfuegbaren Generatoren anzeigen? Schreib einfach "alle zeigen".

IMPORTANT rules for model presentation:
- Lead with the German labels below -- they are friendlier than a model key and
  they are what the user chooses from. Naming the model itself is allowed when
  the user asks; naming the provider or aggregator is not.
- Use descriptive German labels based on strengths:
  -- Fotorealist-Generator (maps to flux-1.1-pro)
  -- Text-Spezialist (maps to ideogram-v3-balanced)
  -- Text-Spezialist Premium (maps to ideogram-v3-quality)
  -- Schnell-Generator (maps to flux-schnell or z-image-turbo)
  -- Premium-Generator (maps to nano-banana-pro)
  -- Kunst-Generator (maps to wan-image or sd-3.5-large)
  -- Kinder-Generator (maps to gpt-image-1.5)
  -- Marketing-Spezialist (maps to gpt-image-2.5-flare -- newest OpenAI generation, up to 16 reference images, ideal for product photos, marketing assets, controlled multi-image edits, strong typography, fast)
  -- Marketing-Spezialist Premium (maps to gpt-image-2.5-sunburst -- same family, quality-optimised: highest fidelity, most precise edits, inpainting; a bit slower)
  -- (legacy: gpt-image-2 is still selectable but superseded by the two above -- do not offer it unless a user explicitly asks for the older model)
  -- Kino-Generator (maps to seedream-5)
  -- Budget-Generator (maps to sdxl)
  -- Praezisions-Generator (maps to sd-3.5-large, supports negative prompts)
- Show price per image in Credits (get from list_models data)
- Internally map the user choice back to the real model key for generate_image

If the user writes "alle zeigen": display all available models as a clean list with
their German labels, strengths, and prices. Let user pick freely.

Selection logic for which 4 to recommend:
- Text or Schrift im Bild -> include Text-Spezialist
- Portrait or Menschen -> include Fotorealist-Generator
- Hoechste Qualitaet or Print or 4K -> include Premium-Generator
- Schnell or Entwurf or Niedrig quality -> include Schnell-Generator
- Cinematic or Film -> include Kino-Generator
- Kunst or Illustration -> include Kunst-Generator
- Kindgerecht -> include Kinder-Generator
- Marketing or Produkt or Werbung or Multi-Bild-Komposition -> include Marketing-Spezialist
  (use Marketing-Spezialist Premium when the user asks for hoechste Detailtreue, Retusche or Print)
- Logo or Branding -> include Text-Spezialist
- Always include at least one budget option and one premium option
- Always fill up to exactly 4 recommendations

REFERENCE IMAGE OVERRIDES (highest priority -- applies if Step 0.5 found refs):
- More than 5 reference images provided -> ONLY recommend Marketing-Spezialist
  (gpt-image-2.5-flare, max 16 refs) or Marketing-Spezialist Premium
  (gpt-image-2.5-sunburst, max 16 refs). Do not show other options unless user insists.
- Composition intent (combine multiple images) -> Marketing-Spezialist first.
- Edit/Variation intent with 1-5 refs -> recommend in this order:
  Marketing-Spezialist Premium (most precise edits, inpainting),
  Marketing-Spezialist (same quality, faster), Premium-Generator (4K),
  Kino-Generator (4K editing), Kinder-Generator (friendly edits).
- Style transfer intent -> Text-Spezialist (ideogram, adopts style) is good;
  Marketing-Spezialist also works.
- Pure text-to-image (no refs) -> use the existing logic above.

Filter out non-supporting models when refs are present. Models without
reference support (flux-*, sd-*, sdxl, ideogram-v3-turbo, imagen-4-fast,
grok-imagine, z-image-turbo, wan-image) MUST NOT be offered if the user
attached images.

---

### Step 7: Enrich the Prompt (silent -- show only if asked)

Write enriched prompt in ENGLISH. Keep 100% of original intent.

Photorealistisch: add photorealistic, hyperdetailed, sharp focus, professional photography, 8K, natural lighting
Cinematic: add cinematic lighting, dramatic atmosphere, movie still, shallow depth of field, color grading
Comic/Illustration: add illustration style, clean linework, vibrant colors, digital art
Kunst/Fine Art: add fine art, painterly, rich textures, expressive brushwork, gallery quality
Minimalistisch: add minimalist design, clean composition, white space, modern aesthetic
Kindgerecht: add child-friendly, soft colors, friendly, warm, welcoming, cartoon style
Portraits: add professional portrait, studio lighting, sharp focus
Products: add product photography, studio setup, clean background

---

### Step 7.5: Inform About Wait Time (CRITICAL for premium models)

Some generators take noticeably longer than others. BEFORE calling generate_image
with a slow model, tell the user a short wait is expected so they do not think it
hung. Generation runs synchronously -- the tool call stays open the whole time.

Expected wait times (rough guide):
- **Schnell-/Budget-Generator** (flux-schnell, z-image-turbo, sdxl, imagen-4-fast):
  a few seconds -- no notice needed.
- **Standard generators** (flux-1.1-pro, ideogram-*, sd-3.5-*): ~10-30 seconds.
- **Marketing-Spezialist** (gpt-image-2.5-flare): noticeably faster than the rest
  of this group -- roughly half the latency of gpt-image-2, usually under a minute.
- **Premium-/Marketing-Premium/Kino-/Kinder-Generator** (gpt-image-2.5-sunburst,
  gpt-image-2, gpt-image-1.5,
  nano-banana-pro/2, seedream-*, owen-image*): **typically 1-2 minutes, and up to
  2-3 minutes** for high quality (2K/4K) or when reference images are attached.

When the selected model is a premium one (or quality is Hoch/Sehr hoch, or
reference images are present), say something brief like:

"Ich erstelle das Bild jetzt mit dem [Generator-Label]. Das kann bei dieser
Qualitaet **2-3 Minuten** dauern -- bitte einen Moment Geduld, ich melde mich,
sobald es fertig ist."

Then call generate_image. Do NOT abort or retry while the call is still running --
it is working, not stuck.

---

### Step 8: Generate the Image

Call KIMASTERMIND_IMAGES:generate_image with:
- prompt: enriched prompt in English
- model: the real model key mapped from the user choice in Step 6
- aspect_ratio: selected format
- quality: if applicable for selected model
- reference_images: see "Reference Images" section below

Quality mapping per model:
- nano-banana-pro: 0.5K (Niedrig), 1K (Mittel), 2K (Hoch), 4K (Sehr hoch)
- gpt-image-1.5: low, medium, high
- gpt-image-2: low, medium, high (default medium, up to 4K)
- gpt-image-2.5-flare / gpt-image-2.5-sunburst: low, medium, high, xhigh, max
  (default high, up to 4K). IMPORTANT: these tiers are shifted one step down
  against gpt-image-2 -- "high" here produces the same output size as the old
  "medium". Map the German levels like this:
    Niedrig    -> medium   (1 Credit, draft)
    Mittel     -> high     (5 Credits, the normal choice -- matches what the
                            Marketing-Spezialist used to deliver)
    Hoch       -> xhigh    (8 Credits)
    Sehr hoch  -> max      (19 Credits)
  "low" exists as an ultra-cheap scribble tier (1 Credit) -- only use it when the
  user explicitly asks for a rough draft. ALWAYS warn before Sehr hoch: billing is
  token-based and max costs roughly 16x a draft image.
- Others: omit quality param or use model default

Returns Image URL: https://mcp.kimastermind.net/img/UUID.jpg

---

### Reference Images: How to Pass Them in the Tool Call

If Step 0.5 found reference image(s), pass them as the `reference_images`
parameter (an array of strings) when calling KIMASTERMIND_IMAGES:generate_image.

Two accepted item formats (you can mix them in the same array):

**1. Base64 data URL** (rarely needed — only as a fallback)
Format: `data:image/(jpeg|png|webp);base64,<BASE64_STRING>`. Server cap 10 MB.
**Strongly prefer the upload_reference flow** (Step 0.5b): call upload_reference
first with the base64, get back a short HTTPS URL, then pass the URL here.
This keeps the generate_image payload small.

**2. HTTPS URL** (for gallery items or external sources)
Any `https://...` URL works. The most common case is an image from the user's
own gallery: `https://mcp.kimastermind.net/img/<uuid>.jpg`.

**Recommended two-step flow** (gpt-image-2.5-flare / Marketing-Spezialist with 3 refs):

Step A — upload each + attachment via upload_reference:
```
KIMASTERMIND_IMAGES:upload_reference(
  image_base64 = "data:image/png;base64,iVBOR...",   // or raw base64 + mime_type
  filename = "logo.png"
)
  -> { url: "https://mcp.kimastermind.net/img/ref/<userId>/aaaa-...jpg",
       expires_at: "2026-04-29T...Z", size_bytes: 142000, filename: "logo.png" }

KIMASTERMIND_IMAGES:upload_reference(
  image_base64 = "/9j/4AAQ...",       // raw base64 without prefix
  mime_type = "image/jpeg",
  filename = "product.jpg"
)
  -> { url: "https://mcp.kimastermind.net/img/ref/<userId>/cccc-...jpg", ... }
```

Step B — pass only the short URLs to generate_image:
```
KIMASTERMIND_IMAGES:generate_image(
  prompt = "Professional product photo of the bottle on white marble, soft natural lighting, advertising style",
  model = "gpt-image-2.5-flare",
  aspect_ratio = "4:3",
  quality = "high",
  reference_images = [
    "https://mcp.kimastermind.net/img/ref/<userId>/aaaa-bbbb-...jpg",  // upload 1
    "https://mcp.kimastermind.net/img/ref/<userId>/cccc-dddd-...jpg",  // upload 2
    "https://mcp.kimastermind.net/img/abc12345-...-...-...-.jpg"        // gallery item
  ]
)
```

Models that support reference images and their limits:
| Model key            | German label           | Max refs | Strengths                                |
|----------------------|------------------------|----------|------------------------------------------|
| gpt-image-2.5-flare  | Marketing-Spezialist   | 16       | newest OpenAI gen, fast, typography, product, transparent bg |
| gpt-image-2.5-sunburst | Marketing-Spezialist Premium | 16 | highest fidelity, most precise edits, inpainting |
| gpt-image-2          | (legacy, no label)     | 16       | typography, product, multi-image edit    |
| nano-banana-pro      | Premium-Generator      | 5        | up to 4K, top-tier text rendering        |
| nano-banana-2        | Premium-Generator      | 5        | fast variant of nano-banana-pro          |
| gpt-image-1.5        | Kinder-Generator       | 5        | OpenAI image, soft warm tone             |
| seedream-5           | Kino-Generator         | 5        | cinematic, deep reasoning                |
| seedream-4.5         | Kino-Generator         | 5        | 4K editing, multi-image composition      |
| owen-image           | (dedicated edit model) | 5        | image editing, text-in-image edits       |
| owen-image-plus      | (dedicated edit model) | 5        | enhanced editing                         |

Important rules:
- If the user attached refs but you selected a non-supporting model, the server
  will return an error. Always select a reference-capable model in Step 6.
- If the user provided more refs than the chosen model supports, either trim
  the list (use the most relevant first) or switch to gpt-image-2.5-flare (16 max).
- Uploaded reference images are kept **30 days** (they were kept 24 hours until
  21.10.2026, which made the upload fallback useless the next day).
- Never resend the same reference between two separate tool calls -- each turn
  the user re-attaches what they want; if you need the same ref across multiple
  generations in one conversation, save the gallery URL of the first result
  and reuse that.
- Provider/model names: still apply -- never expose them to the user.

---

### Step 9: Download and Display the Image

IMPORTANT: Always try local download first (Step 9a/9b). Only use fallback widget (Step 9c) if download fails or no local tool is available.

#### Step 9a: Claude Desktop (Windows) -- Invoke-WebRequest via Desktop Commander

If desktop-commander:start_process is available, use it with PowerShell.

CRITICAL PowerShell rules:
- NEVER use `curl` -- PowerShell maps curl to Invoke-WebRequest with incompatible flags
- ALWAYS use `Invoke-WebRequest` explicitly
- NEVER use `&&` to chain commands -- use semicolons `;`
- ALWAYS use `$env:USERPROFILE` for the home directory (never ~)

Target folder: $env:USERPROFILE\Pictures\KI-Bilder\

Full download command (single line, semicolons as separators):

```powershell
$folder = "$env:USERPROFILE\Pictures\KI-Bilder"; if (!(Test-Path $folder)) { New-Item -ItemType Directory -Path $folder | Out-Null }; Invoke-WebRequest -Uri "IMAGE_URL_HERE" -OutFile "$folder\IMAGE_FILENAME.jpg"; Get-Item "$folder\IMAGE_FILENAME.jpg" | Select-Object Name, Length
```

Replace IMAGE_URL_HERE and IMAGE_FILENAME.jpg before executing.

Filename convention: short descriptive name based on the prompt, e.g. `bergblick_tal_16x9.jpg`
Maximum filename length: 40 characters, lowercase, underscores, no spaces.

After successful download, confirm to user:
✅ Bild gespeichert: C:\Users\[Name]\Pictures\KI-Bilder\IMAGE_FILENAME.jpg

Then show inline summary:
- Stil: STYLE_HERE | Format: RATIO_HERE | Qualitaet: QUALITY_HERE
- Guthaben: CREDITS_HERE Credits ([Aufladen](https://mcp.kimastermind.net/login))

If download fails: go to Step 9c.

#### Step 9b: Claude Desktop (Mac / Linux) -- curl via bash_tool

If bash_tool is available (non-Windows):

```bash
mkdir -p ~/Pictures/KI-Bilder
curl -s -o ~/Pictures/KI-Bilder/IMAGE_FILENAME.jpg "IMAGE_URL_HERE"
echo "OK: $(du -h ~/Pictures/KI-Bilder/IMAGE_FILENAME.jpg)"
```

After successful download, confirm:
✅ Bild gespeichert: ~/Pictures/KI-Bilder/IMAGE_FILENAME.jpg

If download fails: go to Step 9c.

#### Step 9c: Fallback -- Widget + Download Link (Web / Mobile / Download-Fehler)

Used when: claude.ai Web, Claude Mobile (iOS/Android), or any local download failed.

First call KIMASTERMIND_IMAGES:my_credits to get updated balance.

Display image via visualize:show_widget:

```html
<div style="padding: 1rem 0;">
  <div style="background: var(--color-background-secondary); border-radius: var(--border-radius-lg); padding: 1rem;">
    <img src="IMAGE_URL_HERE" style="width:100%; border-radius: var(--border-radius-md); display:block;" alt="Generiertes Bild" />
    <div style="margin-top: 12px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
      <p style="font-size: 13px; color: var(--color-text-secondary); margin: 0;">Stil: STYLE_HERE &middot; Format: RATIO_HERE &middot; Qualitaet: QUALITY_HERE</p>
      <a href="IMAGE_URL_HERE" target="_blank" style="font-size: 13px; color: var(--color-text-info); text-decoration: none;">&#x2B07; Herunterladen</a>
    </div>
    <div style="margin-top: 10px; padding: 8px 10px; background: var(--color-background-primary); border-radius: var(--border-radius-md); border: 0.5px solid var(--color-border-tertiary); display: flex; justify-content: space-between; align-items: center;">
      <span style="font-size: 13px; color: var(--color-text-secondary);">Guthaben: <strong style="color: var(--color-text-primary);">CREDITS_HERE Credits</strong></span>
      <a href="https://mcp.kimastermind.net/login" target="_blank" style="font-size: 12px; color: var(--color-text-info); text-decoration: none;">Aufladen &#x2197;</a>
    </div>
    <details style="margin-top: 8px;">
      <summary style="font-size: 12px; color: var(--color-text-tertiary); cursor: pointer;">Erweiterter Prompt anzeigen</summary>
      <p style="font-size: 12px; color: var(--color-text-secondary); margin: 6px 0 0; font-style: italic;">ENRICHED_PROMPT_HERE</p>
    </details>
  </div>
</div>
```

Also show plain download link below the widget:
📥 Direktlink: https://mcp.kimastermind.net/img/UUID.jpg

---

### Step 10: Offer Model Comparison

After displaying, ask:
Moechtest du dasselbe Motiv mit einem anderen KI-Generator erstellen lassen, um direkt vergleichen zu koennen?

If yes: go back to Step 6, present remaining recommended models (excluding already used one).
Claude Desktop: download both images locally, confirm both file paths.
Web/Mobile: display both images as separate widget calls.

---

## Environment Summary

| Umgebung | Download-Methode | Speicherort |
|---|---|---|
| Claude Desktop (Windows) | desktop-commander + Invoke-WebRequest | %USERPROFILE%\Pictures\KI-Bilder\ |
| Claude Desktop (Mac/Linux) | bash_tool + curl | ~/Pictures/KI-Bilder/ |
| claude.ai Web | nicht moeglich | Widget + Download-Link |
| Claude Mobile (iOS/Android) | nicht moeglich | Widget + Download-Link |

---

## Error Handling

Download fails:
- Always fall back to Step 9c widget + direct download link

Model error or API failure:
- Silently retry with next best model
- If second attempt also fails, inform user

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
- Always use descriptive German labels (Fotorealist-Generator, Text-Spezialist, Video-Generator, etc.)
- Keep workflow smooth and conversational
- Use descriptive German labels for the three capabilities too: **Bild-Generator**
  (this skill), **Video-Generator** (kim-video), **Stimmen-Generator** (kim-voice)
