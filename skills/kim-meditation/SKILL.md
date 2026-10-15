---
name: kim-meditation
description: "Use when the user wants a guided meditation, a relaxation, a sleep journey, a hypnosis session, a breathing exercise, a body scan or an affirmation track produced as audio. Triggers: Meditation, meditieren, gefuehrte Meditation, Entspannung, Entspannungsreise, Traumreise, Fantasiereise, Einschlafhilfe, Schlafmeditation, Achtsamkeitsuebung, Atemuebung, Bodyscan, Hypnose, Trance, Affirmationen, Autogenes Training, Visualisierung, mach mir eine Meditation, guided meditation, relaxation, sleep story, body scan, breathing exercise, hypnosis session. Leads through the questions that decide quality -- goal, imagery world, tone, intensity, voice, music -- then runs four approved steps: script, music, voice sample, final mix. Mixing happens on the KIMASTERMIND server, never by downloading files. For a plain read-aloud use kim-voice, for music alone kim-music."
version: 3.0.1
---

# KIM Meditation Skill

## Was eine Meditation gut macht

Eine gute Meditation ist nicht ein ruhig vorgelesener Text. Sie hat vier Dinge,
die man einzeln hinbekommen muss:

1. **Stille an den richtigen Stellen.** Die Pausen sind der Teil, in dem der
   Hoerende arbeitet. Ohne sie bleibt es eine Ansage.
2. **Bilder statt Begriffe.** „Entspanne dich" ist eine Aufforderung. „Dein Atem
   wird schwer wie warmer Sand" ist ein Bild, das der Koerper selbst umsetzt.
3. **Einladung statt Befehl.** „Vielleicht magst du bemerken" laesst Raum.
   „Jetzt entspann dich" erzeugt Widerstand, besonders bei Angespannten.
4. **Eine Stimme, die traegt.** Nicht jede ruhige Stimme traegt zehn Minuten.

Dieser Skill fuehrt durch alle vier. Der Nutzer bestimmt die Richtung, du
bringst das Handwerk.

---

## Festgelegt — hier gibt es nichts zu waehlen

| | Vorgabe | Warum |
|---|---|---|
| **Stimme** | `voice_generate` mit `engine: "studio"` | Express traegt die Betonung ueber zehn Minuten nicht |
| **`style`-Parameter** | **IMMER setzen, je Abschnitt** — siehe den eigenen Abschnitt unten | das Tempo ist damit wirklich steuerbar. Gemessen mit Despina: 16,2 s ohne, 27,4 s mit. Englisch ODER Deutsch — beides wirkt, welche Formulierung staerker zieht haengt am Satz, nicht an der Sprache. Aber NIEMALS in den Text |
| **Abmischen mit Zahlen** | `voice_lufs: -18`, `music_lufs: -29`, `duck_amount: 0.05`, SFX `lufs: -42`, `lead_in: 30`, `lead_out: 50`, `fade_out: 40` | alles an einer echten Produktion erhoert, nicht gewaehlt |
| **Musik** | `music_generate` mit `engine: "song"` | wird ohnehin geloopt, also zaehlt nur der Preis je Sekunde — und der ist hier mit Abstand der niedrigste |
| **Musikmenge** | **genau EIN Stueck**, egal wie lang die Meditation wird | zwei Stuecke sind zwei Kompositionen, die Naht hoert man. `audio_assemble` loopt das eine Stueck, und das kostet nichts |
| **Abmischen** | **`audio_assemble` auf dem Server** | das Material liegt dort; kostet nichts |
| **Lokal mischen** | **nur wenn `audio_assemble` fehlschlaegt** | sonst wandern hunderte Megabyte hin und her |

**Lade keine Dateien herunter, um sie zu mischen.** Gib `audio_assemble` die
IDs. Du brauchst kein ffmpeg, kein Python, keinen fremden Dienst. Nur wenn das
Werkzeug fehlt oder scheitert, ist der lokale Weg erlaubt — und dann sag dem
Nutzer, dass es der Ausweichweg ist.

---

## Der Ablauf: vier Schritte, jeder freigegeben

| Schritt | Was passiert | Kostet |
|---|---|---|
| **1. Skript** | Text mit Pausenplan, als Tabelle gezeigt | nichts |
| **2. Musik** | EIN Stueck, angehoert | ~16 Credits |
| **3. Stimmprobe** | NUR der erste Abschnitt, **mit Stil**, angehoert | 1–3 Credits |
| **4. Rest + Abmischung** | alle Abschnitte, dann `audio_assemble` | der Hauptteil |

Nie zusammenziehen. Nach dem zwanzigsten Abschnitt zu merken, dass die Stimme
falsch ist, kostet zwanzig Abschnitte. Einer kostet einen.

---

## Schritt 1: Die Fragen

Stell alles Offene **in einer Nachricht**, nummeriert. Was schon gesagt wurde,
wird nicht gefragt.

**Die vier, die das Ergebnis entscheiden:**

**1. Ziel — was soll danach anders sein?**
Einschlafen, Stress loslassen, Angst beruhigen, Fokus finden, Selbstwert
staerken, Schmerz lindern, Trauer halten, Dankbarkeit, Koerperreise, Atem.
Frag nach dem *Zustand danach*, nicht nach dem Thema: „ruhig und bei mir" ist
brauchbarer als „Achtsamkeit".

**2. Bildwelt — worin soll die Reise spielen?**
Das ist die wichtigste kreative Entscheidung und die, die am meisten
unterscheidet. Biete konkret an:

| Welt | Passt zu | Beispielbild |
|---|---|---|
| **Natur** | Erdung, Ruhe | Waldboden, Moos, Sonnenflecken zwischen Blaettern |
| **Wasser** | Loslassen, Fliessen | Du treibst auf warmem Wasser, es traegt dich ganz |
| **Licht / Waerme** | Heilung, Selbstwert | Goldenes Licht sammelt sich in deiner Brust |
| **Koerper** | Schmerz, Anspannung | Von den Fuessen aufwaerts wird alles schwer |
| **Atem** | Angst, Panik | Der Atem kommt und geht wie eine Welle |
| **Raum / Haus** | Ordnung, Klarheit | Ein Zimmer, in dem nur steht, was dir guttut |
| **Himmel / Weite** | Perspektive, Trauer | Gedanken ziehen vorbei wie Wolken |

Hat der Nutzer keine Vorstellung, schlag **eine** vor, die zum Ziel passt, und
begruende sie in einem Satz.

**3. Ton — wie nah soll es gehen?**

| Stufe | Klingt so |
|---|---|
| **sachlich** | „Richte die Aufmerksamkeit auf den Atem." Fuer Geuebte, fuer den Arbeitsplatz |
| **warm** (Standard) | „Nimm dir einen Moment. Es muss gerade nichts geschehen." |
| **poetisch** | „Der Abend legt sich auf deine Schultern wie ein Mantel, den jemand fuer dich gewaermt hat." |
| **eindringlich** | Kurze Saetze, Wiederholung, direkte Suggestion. Fuer Veraenderung, nicht zum Einschlafen |

**4. Laenge** in Minuten. Dazu: **Einschlafen oder zurueckkommen?** Eine
Einschlafmeditation weckt nicht zurueck und blendet aus. Eine Tagesmeditation
holt zurueck: Finger bewegen, tief einatmen, Augen oeffnen.

**Die vier kleineren, die man schnell abhandelt:**

5. **Du oder Sie**
6. **Erfahrung**: Anfaenger brauchen mehr Fuehrung und kuerzere Stillen; Geuebte
   vertragen lange Pausen und weniger Erklaerung
7. **Stimme**: weiblich oder maennlich, und welcher Charakter (warm, sanft,
   tief, hauchig)? Weiss der Nutzer es nicht — Schritt 3 zeigt die Hoerproben
8. **Musik**: Richtung in eigenen Worten. Weiss er es nicht, schlag etwas vor,
   das zur Bildwelt passt (Wasser → weite Flaechen; Koerper → tiefe Toene)

**Eine Frage, die man NICHT stellt:** nach dem Tempo. Das Tempo kommt aus den
Pausen, nicht aus einer Einstellung — und einstellen laesst es sich ohnehin
nicht.

---

## Schritt 2: Das Skript

Schreib es selbst. Diese Regeln sind der Unterschied zwischen einer Meditation
und einem vorgelesenen Text.

### Aufbau

Zeiten fuer 10 Minuten, proportional anpassen:

| Teil | Anteil | Was passiert |
|---|---|---|
| **Ankommen** | ~15 % | Haltung, Augen, erste Atemzuege. Kurze Saetze, lange Pausen |
| **Vertiefen** | ~20 % | Atem, Schwere, der Koerper sinkt. Hier entsteht die Trance |
| **Hauptteil** | ~45 % | Die Bildwelt und die Suggestionen. Das eigentliche Stueck |
| **Verankern** | ~10 % | Ein Satz zum Mitnehmen, mit dem Gefuehl verknuepft |
| **Abschluss** | ~10 % | Einschlafen: ausklingen. Sonst: zurueckholen |

### Sprache

- **Gegenwart und positiv.** „Du atmest ruhig", nie „du wirst nicht mehr
  unruhig". Das Unbewusste hoert „unruhig", nicht „nicht"
- **Kurze Hauptsaetze.** Nebensaetze zwingen zum Mitdenken — das Gegenteil des
  Ziels
- **Einladend**: „vielleicht magst du", „wenn du so weit bist", „erlaube dir",
  „du kannst". Nie „du musst", nie „jetzt sofort"
- **Zweite Person, nie „man"**
- **Sinne ansprechen**: was spuerst du, was hoerst du, was waermt, was wiegt
- **Keine Fragen**, auf die jemand antworten moechte
- **Kein Fachjargon**, kein Englisch, keine Zahlen zum Rechnen

### Suggestionen, die wirken

Vier Bauweisen, die den Unterschied machen:

**Ja-Kette** — drei Dinge, die unbestreitbar stimmen, dann die eigentliche
Suggestion. Der Kopf hat dreimal zugestimmt und stimmt beim vierten Mal weiter:

> „Du liegst hier. Du hoerst meine Stimme. Dein Atem geht von selbst.
> *Und mit jedem Ausatmen wirst du ein Stueck schwerer.*"

**Verknuepfung** — koppele das Gewuenschte an etwas, das ohnehin passiert:

> „Jedes Mal, wenn du ausatmest, loest sich ein Stueck Anspannung."

Der Atem kommt sowieso. Die Entspannung reitet mit.

**Eingebettete Aufforderung** — das Wesentliche steckt im Nebensatz, so umgeht
es den Widerstand:

> „Du musst gar nichts tun, ausser *ganz ruhig zu werden*."

**Zeitliche Offenheit** — kein Zeitdruck, keine Erfolgskontrolle:

> „Irgendwann in den naechsten Minuten wird dein Koerper von selbst wissen, wie
> tief er gehen darf."

**Was zu vermeiden ist:** Versprechen („danach ist deine Angst weg"),
Bewertungen („gut gemacht"), Bedingungen („wenn du dich richtig konzentrierst").
Alle drei erzeugen Druck, und Druck ist das Ende der Entspannung.

### Metaphern — dichter, nicht mehr

Eine Bildwelt, konsequent durchgehalten, schlaegt fuenf schoene Bilder. Wer im
Wald anfaengt, bleibt im Wald. Ein Bild darf wiederkehren und sich vertiefen —
das ist kein Mangel an Einfallsreichtum, sondern genau die Wirkung.

Gute Bilder sind **koerperlich** (Schwere, Waerme, Weite, Sinken), nicht
abstrakt (Harmonie, Energie, Balance). „Schwer wie warmer Sand" wirkt,
„energetisch ausgeglichen" ist Dekoration.

### Pausen — die wichtigste Spalte

An einer fertigen Zehn-Minuten-Meditation erhoert, nicht geschaetzt:

| Stelle | Pause |
|---|---|
| zwischen Saetzen in Ankommen und Koerperreise | **5-11 s** |
| nach einem Bild, das wirken soll | **12-16 s** |
| nach einer Suggestion | **9-11 s** |
| in der Ausleitung | **7-8 s** |
| gefuehrter Atem | nicht nach Gefuehl - **gerechnet**, siehe den Atem-Abschnitt |

Die frueheren Werte (bis 30 s nach einem Bild) waren zu lang: mit gesetztem
`style` spricht die Stimme ohnehin langsam, und die Pause kommt oben drauf.

**Faustregel: etwa die Haelfte einer Meditation ist Stille.** Und rechne damit,
dass der Vortrag mit `style` noch **20-30 % langsamer** wird - ein Skript, das
fuer 8 Minuten geschrieben war, wurde 10 1/2 Minuten lang. Lieber kuerzer
planen als den Nutzer ueberraschen.


### Darstellung

| Nr. | Teil | Text | Pause danach |
|---|---|---|---|
| 1 | Ankommen | „Leg dich so hin, wie es sich gut anfuehlt." | 10 s |
| 2 | Ankommen | „Und wenn du magst, schliess die Augen." | 12 s |
| 3 | Vertiefen | „Dein Atem geht von selbst. Du musst nichts tun." | 15 s |

**Je Abschnitt hoechstens ~600 Zeichen.** Laengeres laesst sich nicht einzeln
korrigieren, und ein misslungener Abschnitt kostet dann den ganzen Block.

**Dann fragen: passt das?** Korrekturen am Skript sind gratis — hier darf
beliebig oft geaendert werden. Erst nach dem Ja kostet es etwas.

---

## Die Sprechweise: der Grundstil plus einer je Teil

**Du setzt sie, ungefragt, bei jedem einzelnen Abschnitt.** Niemand bittet um
einen `style`; jeder hoert aber, wenn eine Meditation im Tempo einer
Bahnhofsansage gelesen wird.

**Englisch ist der Standard**, weil die Beispiele unten darauf abgestimmt sind
— aber **Deutsch wirkt genauso**. Zwei Messungen, zwei Ergebnisse: beim ersten
Satzpaar zog Englisch staerker (+46 % gegen +23 %), beim zweiten der deutsche
Satz (15,6 s gegen 14,6 s). Es haengt an der Formulierung, nicht an der Sprache.
Was dagegen immer gilt: **niemals in den `text`** — der ist ein woertliches
Transkript, was dort steht wird vorgelesen.

**Der Grundstil, an jeden Abschnitt:**

```
Speak like an experienced meditation guide: warm, deep, calm, close and soft.
Very slow pace, let every phrase ring out, natural breathing pauses at every
ellipsis, no stress peaks.
```

**Plus der Zusatz fuer den jeweiligen Teil** — angehaengt, nicht ersetzt:

| Teil | Zusatz |
|---|---|
| **Ankommen** | `Inviting and friendly, a quiet smile in the voice.` |
| **Koerperreise** | `Even slower and softer, stretch the body words gently, heavy and warm.` |
| **Atem erklaeren** | `Calm, clear and even, so the rhythm is easy to follow.` |
| **Atemkommando Ein** | `Very gentle, drawn out, almost breathed, following a slow inhale.` |
| **Atemkommando Aus** | `Long and fading like a slow exhale, letting go downwards.` |
| **Bilder, Visualisierung** | `Dreamlike, quietly marvelling, as if you saw the scene yourself.` |
| **Suggestionen** | `Deep, carried, grounded, with quiet certainty and confidence.` |
| **Ausleitung** | `Gently bringing back, gradually a little more awake and brighter.` |
| **Letzter Satz** | `Friendly, awake, warm-hearted, a quiet smile goodbye.` |

**Die Stimmprobe in Schritt 3 erzeugst du schon mit dem Stil.** Eine Probe ohne
`style` klingt anders als das Endergebnis — dann hat der Nutzer das Falsche
freigegeben.

### Die Textschreibweise, die das Tempo macht

**Drei Punkte zwischen den Phrasen** — `...` — verlangsamen den Vortrag hoerbar
und sind der Standard fuer jeden Meditationstext. Der Grundstil nennt sie
ausdruecklich (`natural breathing pauses at every ellipsis`), damit sie als
Atempause gelesen werden und nicht als Zoegern.

> Komm einen Moment zur Ruhe ... Atme tief ein ... und lass den Atem wieder
> fliessen ...

---

## Gefuehrte Atemzyklen, zum Beispiel 4-8-4

Das kann kein Fliesstext leisten, denn der Atem braucht **Takt**. Also je
Kommando ein **eigener kurzer Abschnitt**, und die Phasenlaenge entsteht aus der
Pause danach:

| Abschnitt | Text | `pause_after_seconds` |
|---|---|---|
| Ein | „Atme ein ..." | Phasendauer **minus** Cliplaenge → `4 - Clip` |
| Aus | „und langsam ausatmen ..." | Phasendauer minus Clip **plus** Haltephase → `8 - Clip + 4` |

**Die Haltephase wird nicht angesagt.** Kein „Ruhe", kein „Halten", kein
„Jetzt anhalten" — **die Stille ist die Anweisung.** Ein Wort an dieser Stelle
reisst aus dem Rhythmus, den man gerade aufgebaut hat.

**Die beiden Clips fuer jeden Zyklus wiederverwenden**: dieselbe `audio_id`
mehrfach in `segments`. `audio_assemble` kann das, und es kostet keinen Credit
mehr. Acht Zyklen sind also **zwei** Generierungen, nicht sechzehn.

---

## Musik: ein Stueck, und kein Klavier

`music_generate` mit `engine: "song"`, **ein** Stueck, der Server loopt es.

Bewaehrter Prompt — Klavier wurde als stoerend empfunden, deshalb ist es
ausdruecklich ausgeschlossen:

```
deep meditative ambient drone, warm soft synth pads slowly swelling and fading,
sustained gentle tones, very calm and carried, spacious and warm, no piano,
no melody, no rhythm, no percussion, no vocals, instrumental
```

```
negative_prompt: piano, keys, melody, drums, beat, percussion, vocals, singing, bright
```

Eine Melodie zieht Aufmerksamkeit auf sich, ein Puls zwingt die Atmung in ein
fremdes Tempo. Beides ist in einer Meditation ein Fehler, kein Geschmack.

---

## Geraeusche: nur zu Bildern, die im Text stehen

Ueber `kim-sfx`, **22 Sekunden**, der Server loopt sie. Nur dort, wo der Text
das Bild auch nennt — ein Wald, den niemand erwaehnt, ist Deko.

**Bewaehrt:**

| Bild | Prompt | `prompt_influence` |
|---|---|---|
| Wald | `calm forest ambience with gentle soft birdsong in the distance, peaceful, quiet and natural, no wind` | 0,35 |
| Bach | `a quiet small brook flowing softly in the background, distant gentle stream, smooth calm water, no splashing` | 0,45 |

**Nicht bewaehrt, und warum:**

- **Wind** klingt kuenstlich — weglassen, auch wenn der Text ihn nennt
- **„babbling brook"** gurgelt, statt zu fliessen
- **„birdsong"** ohne `distant` oder `soft` wird dominant und zieht nach vorn

**Platzierung:** 2–3 Sekunden **vor** dem Satz, der das Bild einfuehrt
(`start_at_segment` mit `offset_seconds: -2`), und ein paar Sekunden ueber den
Themenwechsel hinaus (`until_segment`). Nie mit `start_seconds` arbeiten, wenn
es auch ueber den Abschnitt geht: spricht die Stimme laenger als geplant,
stimmt eine feste Sekunde nicht mehr.

---

## Die Abmischung: die Zahlen, die funktionieren

Alles an einer echten Produktion erhoert. Diese Werte an `audio_assemble`
uebergeben:

```
voice_lufs: -18      music_lufs: -29      duck_amount: 0.05
sfx lufs:   -42      lead_in: 30          lead_out: 50       fade_out: 40
```

| Wunsch | Was aendern |
|---|---|
| „Musik mehr im Vordergrund" | `music_lufs: -27` |
| „Geraeusche leiser" | SFX `lufs: -45` |
| „Musik zu praesent beim Sprechen" | `duck_amount: 0.1` |

**Warum gerade diese Zahlen:**

- **−42 fuer Geraeusche** sind rund 13 dB unter der Musik. Mit −34 bis −39
  waren sie „zu laut, zu praesent" — ein Geraeusch soll man vermissen, wenn es
  fehlt, nicht hoeren, wenn es da ist.
- **`duck_amount: 0.05`** senkt die Musik nur um 5 %. Starkes Ducking zieht sie
  in jeder Pause wieder hoch, und das ist in einer Meditation Unruhe, nicht
  Dynamik.
- **50 s Nachlauf mit 40 s Blende**, weil eine Meditation nicht auf der letzten
  Silbe enden darf.

`audio_assemble` meldet zurueck, welchen Teil der Musik es als Schleife gewaehlt
hat und **wie leise die leiseste Sekunde des Bettes ist**. Liegt die mehr als
6 dB unter dem Ziel, hat die Schleife ein Loch — dann `music_start` und
`music_end` selbst setzen. Diese Zahl ersetzt das Nachhoeren.

---

## Was es kostet, und wie du es sagst

Ein Credit ist etwa 0,04–0,05 USD Verkaufspreis. Eine vollstaendige
Zehn-Minuten-Meditation:

| Posten | Credits |
|---|---|
| Musik, ein Stueck | 16 |
| Stimme, ~27 Abschnitte | ~27 |
| zwei Geraeusche | 2 |
| Abmischung | **0** |
| | **≈ 45 Credits** |

Das vorher in einem Satz nennen, mit dem Guthaben daneben. Und der Hinweis, der
wirklich spart: **die Abmischung kostet nichts**, also ist eine zweite Version
mit anderen Pegeln gratis — nur neue Sprachaufnahmen kosten wieder.

---

## Wenn `audio_assemble` ausfaellt

Dann, und nur dann, lokal mischen — und dem Nutzer sagen, dass es der
Ausweichweg ist. Die Referenz-Implementierung liegt als `mix_v3.py` beim
Besitzer; sie macht genau das, was der Server jetzt auch macht. Lade **nicht**
im Normalfall Dateien herunter, um sie zu mischen: das Material liegt auf dem
Server, und dort gehoert die Arbeit hin.


## Schritt 5: Alle Abschnitte und die Abmischung

Restliche Abschnitte **einzeln** mit derselben Stimme und dem **Stil des
jeweiligen Teils**. Je Abschnitt die **Audio-ID** aus der Download-URL notieren.

Vorher Gesamtkosten und Guthaben nennen (`my_credits`).

```
audio_assemble(
  segments = [{ audio_id, pause_after_seconds }, ...],   // in Reihenfolge,
                                                         // Atemclips mehrfach
  music_id   = <id>,
  voice_lufs = -18,
  music_lufs = -29,
  duck_amount = 0.05,
  lead_in_seconds  = 30,
  lead_out_seconds = 50,
  fade_out_seconds = 40,
  sfx_layers = [
    { audio_id: <wald>, start_at_segment: 17, offset_seconds: -2,
      until_segment: 21, lufs: -42 },
    { audio_id: <bach>, start_at_segment: 21, offset_seconds: -3,
      until_segment: 24, lufs: -42 }
  ]
)
```

Was von selbst passiert, und was es dir erspart:

- **Die Musik wird in ihrem stabilen Mittelteil geloopt**, mit Ueberblendung.
  Ein generiertes Stueck schwillt ueber die erste Minute an und blendet am Ende
  selbst aus — ganz geloopt gaebe das an jeder Naht zehn Sekunden Fast-Stille.
- **Jeder Abschnitt wird auf `voice_lufs` gemessen und angeglichen**, nicht
  geschaetzt. Das ist auch bei einem Zwei-Sekunden-Clip exakt.
- **Die Musik senkt sich sanft unter der Stimme**, mit 0,6-s-Rampe.
- **Geraeusche werden geloopt, gepegelt und relativ zum Abschnitt platziert.**

Es meldet zurueck: die Startzeit jedes Abschnitts, die jedes Geraeuschs, den
gewaehlten Schleifenbereich und **die leiseste Sekunde des Musikbettes**. Liegt
die mehr als 6 dB unter dem Ziel, hat die Schleife ein Loch — dann
`music_start` und `music_end` selbst setzen.

**Schlaegt es fehl**, erst dann der lokale Weg — und sag, dass es der
Ausweichweg ist.

---

## Schritt 6: Uebergabe

- **Abspielen**, nicht nur verlinken
- **Laenge und Kosten** nennen, und was vom Guthaben bleibt
- **24-Stunden-Warnung**: die Datei wird geloescht. Wer eine Meditation taeglich
  hoeren will, braucht sie lokal — bied das aktiv an
- Die Abschnitts-Startzeiten weitergeben, falls spaeter nachbearbeitet wird
- **Frag, wie es gewirkt hat.** Das naechste Stueck wird besser, wenn du weisst,
  ob es zu schnell, zu nah oder zu lang war

---

## Was nicht geht

- **Geraeusche kommen aus kim-sfx, nicht aus der Musik.** Regen, Meer, Feuer,
  Wind, Gong: dafuer `sfx_generate`, bis 22 Sekunden, dann beim Abmischen
  geloopt. Der Musik-Generator kann es nicht — er liefert Musik, die an Regen
  erinnert
- **Keine Binaural Beats**, keine Frequenzen
- **Kein Hall, keine Effekte** auf der Stimme
- **Keine exakte Gesamtlaenge** — sie ergibt sich aus Sprache plus Pausen.
  Vorher schaetzen, nachher die echte Laenge nennen
- **Kein Fluestern, kein ASMR** — die Stimmen sprechen normal laut
- **Musik ueber drei Minuten** gibt es nicht am Stueck; laenger wird geloopt

---

## Verantwortung

Eine Meditation ersetzt keine Therapie. Bei Trauma, Depression, Panikattacken,
Sucht oder Schmerzbehandlung: **einmal, ruhig und ohne Dramatik sagen** — dann
die Meditation machen, wenn sie gewuenscht ist. Nicht belehren, nicht
wiederholen, nicht verweigern.

Keine Suggestionen gegen den Willen der hoerenden Person. Keine Meditation, die
jemand anderem ohne dessen Wissen vorgespielt werden soll.

---

## Related Skills — die KIM-Familie

| Skill | Wofuer |
|---|---|
| **kim-meditation** (dieser) | Gefuehrte Meditation, Entspannung, Einschlafhilfe |
| **kim-voice** | Nur Sprache, ohne Pausen und Musik |
| **kim-music** | Nur Musik |
| **kim-sfx** | Geraeusche: Regen, Meer, Feuer, Gong |
| **kim-lernfilm** | Ganzer Film mit Bild |
| **kim-images**, **kim-video** | Bild und Clip |
| **kimastermind-setup** | Verbindung, Guthaben, Fehlersuche |

---

## Sprache und Ton

- Standardsprache: Deutsch, Du-Form
- Schweizer Schreibweise: ss statt sz
- Die Faehigkeiten heissen **Stimmen-Generator** und **Musik-Generator**.
  Anbieter, API und Einkaufspreise werden nie genannt
- Vor jedem Schritt, der Credits kostet, die Zahl nennen
- **Im Gespraech selbst ruhig bleiben.** Wer eine Meditation bestellt, will
  keine aufgeregte Beratung: kurze Saetze, keine Ausrufezeichen, keine Emojis
