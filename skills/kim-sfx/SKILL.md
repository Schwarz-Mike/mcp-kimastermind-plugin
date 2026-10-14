---
name: kim-sfx
description: Use when the user wants a SOUND rather than music or speech -- rain, sea, wind, fire, a gong, a bell, a door, footsteps, room tone, a whoosh, a notification sound, an atmosphere for a video or a meditation. Triggers: Geraeusch, Sound, Soundeffekt, SFX, Atmo, Atmosphaere, Hintergrundgeraeusch, Regen, Meer, Wellen, Feuer, Wind, Gong, Klangschale, Vogelgezwitscher, Tuer, Schritte, Raumklang, Ambience, sound effect, ambience, foley, whoosh, make a rain sound. The length is freely selectable from half a second to 22, billed per second. For music use kim-music, for speech kim-voice -- the music engine cannot make real noises, it returns music that evokes them.
version: 1.0.0
---

# KIM SFX Skill

## Purpose

Generate a real sound from a description: rain on a window, a single gong, a
crackling fire, a door closing. The capability is called the
**Geraeusch-Generator**.

**This is the only engine here that makes noises.** The music generator, asked
for rain, returns music that evokes rain — it is trained on music and no prompt
changes that. Whenever someone wants an actual sound, this is the tool.

---

## What makes it different from music

| | Geraeusch | Musik |
|---|---|---|
| Laenge | **frei, 0,5 bis 22 Sekunden** | fest, 33 Sek oder bis 3 Min |
| Abrechnung | **pro Sekunde** | pro Stueck |
| 10 Sekunden kosten | **2 Credits** | — |
| 22 Sekunden kosten | **5 Credits** | — |
| Fertig in | ~3 Sekunden | ~30 Sekunden |

Die freie Laenge ist der eigentliche Grund, warum es hierher gehoert: ein Gong
braucht vier Sekunden, eine Atmosphaere zwanzig.

---

## Available MCP Commands

- `sfx_generate` — `prompt` (what it should sound like), `seconds` (0.5–22,
  default 10), `prompt_influence` (0–1, default 0.3)
- `my_credits` — balance. Fetch fresh before naming a price
- `audio_assemble` — mixes a sound under speech, and loops it to any length

---

## Die Fragen

Meist genuegt eine. Frag nur, was wirklich offen ist:

1. **Was genau soll zu hoeren sein?** Je konkreter, desto besser — „Regen auf
   ein Fenster, dahinter fernes Donnern" schlaegt „Regen"
2. **Wie lang?** Default 10 Sekunden. Fuer einen einzelnen Klang (Gong, Tuer,
   Klick) 3–5, fuer eine Atmosphaere 15–22
3. **Soll es sich wiederholen lassen?** Wenn es unter einem laengeren Stueck
   liegen soll, sag es — dann wird es geloopt statt verlaengert

Was nicht gefragt werden muss: die Sprache des Prompts. Du schreibst ihn, am
besten auf Englisch.

---

## Den Prompt bauen

Drei Dinge machen den Unterschied:

**1. Die Schallquelle benennen, nicht die Stimmung.** „Gemuetlich" ist kein
Geraeusch. „Crackling campfire, close" ist eins.

**2. Die Entfernung mitgeben.** `close`, `distant`, `in a large hall`, `outside
behind a window` — das aendert mehr als jedes Adjektiv.

**3. Dauerhaft oder einmalig unterscheiden.** `steady`, `continuous`, `looping`
fuer Atmosphaeren; `single`, `once`, `one hit` fuer einzelne Klaenge.

| Wunsch | Prompt |
|---|---|
| Regen | `steady rain on a window, distant soft thunder, continuous` |
| Meer | `gentle waves rolling onto a sandy beach, calm, continuous` |
| Feuer | `crackling campfire, close and warm, continuous` |
| Wald | `quiet forest ambience, soft wind in leaves, distant birds` |
| Gong | `single deep gong struck once, very long decay` |
| Klangschale | `single Tibetan singing bowl struck once, shimmering decay` |
| Wind | `soft wind through pine trees, continuous` |
| Tuer | `wooden door closing softly, one hit` |
| Raumklang | `quiet room tone, almost silent, faint air movement` |

**`prompt_influence`** entscheidet, wie woertlich es genommen wird:
- **0,2–0,4** fuer Atmosphaeren, die sich unterordnen sollen
- **0,6–0,8** fuer einen bestimmten, erkennbaren Klang (Gong, Tuer, Klick)

---

## Kosten, bevor generiert wird

`my_credits` holen, dann in einem Satz:

> „Zehn Sekunden Regen kosten **2 Credits**. Du hast **96**, danach noch 94.
> Soll ich?"

| Laenge | Credits |
|---|---|
| 5 Sek | 1 |
| 10 Sek | 2 |
| 22 Sek | 5 |

Gerechnet wird pro Sekunde; die genauen Werte stehen in `list_models`, denn der
Satz liegt in der Datenbank.

---

## Ausliefern

- **Abspielen**, nicht nur verlinken — wie in kim-voice: notfalls als
  `data:`-URI inline, sonst Systemplayer, sonst Link
- **Die 24-Stunden-Warnung**: die Datei wird geloescht
- **Den naechsten Schritt anbieten**, wenn er nahe liegt: unter eine Meditation
  legen (kim-meditation), unter ein Video (kim-lernfilm), oder mit
  `audio_assemble` unter eine vorhandene Aufnahme mischen

---

## Laenger als 22 Sekunden

Geht nicht am Stueck — und muss auch nicht. **Ein Geraeusch wird geloopt**, nicht
verlaengert: `audio_assemble` legt es als Spur unter ein beliebig langes Stueck
und wiederholt es dabei. Erzeuge also **ein** gutes Stueck von 15–22 Sekunden
statt mehrerer.

Damit eine Schleife nicht auffaellt: etwas Gleichfoermiges nehmen (Regen, Wind,
Raumklang) und `continuous` in den Prompt schreiben. Alles mit einem klaren
Anfang und Ende (ein Gong, eine Tuer) eignet sich nicht zum Loopen.

---

## Was nicht geht

- **Keine Musik** — dafuer kim-music. Wer hier Melodie bestellt, bekommt
  Geraeusch, das wie ein misslungenes Instrument klingt
- **Keine Stimmen, kein Sprechen, kein Gesang** — dafuer kim-voice
- **Keine bestimmten Marken oder Personen**: kein „Klingelton von …", keine
  erkennbare Melodie, keine Imitation einer realen Stimme
- **Nicht laenger als 22 Sekunden** am Stueck
- **Keine Garantie auf Wiedererkennbarkeit** bei sehr speziellen Wuenschen.
  Je gewoehnlicher das Geraeusch, desto besser das Ergebnis

---

## Related Skills — die KIM-Familie

| Skill | Wofuer |
|---|---|
| **kim-sfx** (dieser) | Geraeusche und Atmosphaeren |
| **kim-music** | Musik |
| **kim-voice** | Sprache |
| **kim-meditation** | Gefuehrte Meditation: Skript, Musik, Stimme, Abmischung |
| **kim-lernfilm** | Ganzer Film mit Bild |
| **kim-images**, **kim-video** | Bild und Clip |
| **kimastermind-setup** | Verbindung, Guthaben, Fehlersuche |

---

## Sprache und Ton

- Standardsprache: Deutsch, Du-Form
- Schweizer Schreibweise: ss statt sz
- Die Faehigkeit heisst **Geraeusch-Generator**. Anbieter, API und
  Einkaufspreise werden nie genannt
- Vor der Generierung die Credits nennen
- Kurz halten: eine Frage, eine Kostenzeile, dann das Geraeusch
