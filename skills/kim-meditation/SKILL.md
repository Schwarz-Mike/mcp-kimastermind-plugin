---
name: kim-meditation
description: "Use when the user wants a guided meditation, a relaxation, a sleep journey, a hypnosis session, a breathing exercise, a body scan or an affirmation track produced as audio. Triggers: Meditation, meditieren, gefuehrte Meditation, Entspannung, Entspannungsreise, Traumreise, Fantasiereise, Einschlafhilfe, Schlafmeditation, Achtsamkeitsuebung, Atemuebung, Bodyscan, Hypnose, Trance, Affirmationen, Autogenes Training, Visualisierung, mach mir eine Meditation, guided meditation, relaxation, sleep story, body scan, breathing exercise, hypnosis session. Leads through the questions that decide quality -- goal, imagery world, tone, intensity, voice, music -- then runs four approved steps: script, music, voice sample, final mix. Mixing happens on the KIMASTERMIND server, never by downloading files. For a plain read-aloud use kim-voice, for music alone kim-music."
version: 2.4.0
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
| **`style`-Parameter** | **setzen**: `speaking slowly, calm and meditative, with long pauses` | das Tempo ist damit wirklich steuerbar — gemessen 7 s ohne, 14 s mit der Angabe. Auf Englisch, und NIEMALS in den Text |
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
| **3. Stimmprobe** | NUR der erste Abschnitt, angehoert | 1–3 Credits |
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

| Stelle | Pause |
|---|---|
| nach einer Anweisung zum Spueren | 8–15 s |
| nach einer Atemanweisung | 10–20 s (ein Atemzug ~6 s) |
| zwischen zwei Saetzen desselben Gedankens | 3–5 s |
| nach einem Bild, das wirken soll | 15–30 s |
| nach einer Suggestion | 10–15 s, damit sie sich setzt |
| vor dem Abschluss | 10 s |

**Faustregel: etwa die Haelfte einer Meditation ist Stille.** Wer 10 Minuten
Text schreibt, bekommt 20 Minuten Audio. Bei „eindringlich" etwas weniger
Pause, bei „Einschlafen" deutlich mehr.

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

## Schritt 3: Musik

Ein Stueck, `music_generate(engine: "song")`. Es wird beim Abmischen geloopt —
eines reicht fuer jede Laenge, auch fuer eine halbe Stunde, und Loopen kostet
nichts.

**Warum `song` und nicht `pro`:** weil die Laenge hier gleichgueltig ist. Das
Stueck wird ohnehin geloopt, also zaehlt nur der Preis je Sekunde Material — und
da ist `song` mit 16 Credits fuer rund 165 Sekunden das guenstigste der drei
(0,10 gegen 0,17 bei `pro` und 0,18 bei `score`). Es liefert ausserdem das
laengste Stueck, und je laenger die Schleife, desto weniger faellt sie auf.

**Eine Ausnahme:** soll die Musik **nicht** loopen, sondern genau mit der
Meditation enden, nimm `music_generate(engine: "pro", seconds: <Laenge>)` — bis
fuenf Minuten. Das kostet 10 Credits je Minute, also mehr, und lohnt sich nur
bei einer kurzen Meditation, bei der eine Schleife auffiele.

Der Prompt muss **englisch** sein; du uebersetzt, der Nutzer sieht ihn nie.
Nach Bildwelt:

| Bildwelt | Prompt |
|---|---|
| Natur, Erdung | `calm ambient meditation music, soft warm pad, sparse piano, very slow, organic and grounded, no percussion, no vocals` |
| Wasser, Loslassen | `flowing ambient meditation music, slow swelling pads, gentle and weightless, no rhythm, no vocals` |
| Licht, Heilung | `warm ambient meditation music, soft strings and glowing pad, slowly rising, hopeful but very calm, no vocals` |
| Koerper, Schmerz | `deep ambient meditation music, low warm drone and soft pad, extremely slow, grounding, no vocals` |
| Atem, Angst | `very sparse ambient music, single soft pad, almost still, reassuring, no melody, no vocals` |
| Himmel, Trauer | `spacious ambient music, distant soft pad, wide and open, melancholic but gentle, no vocals` |

Was zu vermeiden ist und warum:
- **kein Schlagzeug, kein Beat** — ein Puls zwingt die Atmung in fremdes Tempo
- **kein Gesang** — Worte ueber Worten
- **keine Melodiebogen** — sie ziehen Aufmerksamkeit auf sich
- **nichts, was sich stark entwickelt** — es wird geloopt

**Vorspielen** und fragen: passt die Stimmung? Ein neues Stueck kostet 16
Credits, eine ganze Meditation mit falscher Musik kostet alles.

---

## Schritt 4: Die Stimme

**Zeig immer zuerst die Hoerproben**, auch wenn der Nutzer einen Wunsch
geaeussert hat — hoeren schlaegt beschreiben:

```
https://mcp.kimastermind.net/voices/studio?for=trance
```

Das `?for=trance` waehlt genau die Stimmen vor, deren Charakter traegt. Ist ein
Browser-Werkzeug da, oeffne die Seite direkt. Nenne zusaetzlich **zwei bis drei
konkret**, mit Charakter und wofuer sie taugen:

| Stimme | Charakter | Passt zu |
|---|---|---|
| **Sulafat** (w) | warm | der sichere Standard, fast alles |
| **Vindemiatrix** (w) | sanft | Einschlafen, Angst |
| **Achernar** (w) | weich | Trauer, Selbstmitgefuehl |
| **Enceladus** (m) | hauchig | Einschlafen, sehr nah |
| **Algieba** (m) | geschmeidig | Koerperreisen, Erdung |
| **Schedar** (m) | gleichmaessig | lange Stuecke, Hypnose |

Dann **nur den ersten Abschnitt** erzeugen:

```
voice_generate(
  engine = "studio",
  voice  = <Stimme>,
  text   = <Abschnitt 1>,
  style  = "speaking slowly, calm and meditative, with long pauses"
)
```

**Die `style`-Angabe ist hier das wichtigste Werkzeug ueberhaupt**, denn eine
Meditation lebt vom Tempo. Gemessen am 15.10.2026 mit Despina, vier Saetze,
identischer Text: **16,2 s** ohne Angabe, **27,4 s** mit der oben genannten.
69 % mehr Zeit fuer dieselben Worte — das ist keine Nuance.

**Du setzt sie selbst, ungefragt.** Niemand bittet um einen `style`; jeder hoert
aber, wenn eine Meditation im Tempo einer Ansage gelesen wird. Du hast das
Skript geschrieben, du weisst, welcher Abschnitt wie klingen muss.

**Und du setzt sie pro Abschnitt, nicht einmal fuer alles.** Das ist der
Unterschied zwischen einer vorgelesenen Meditation und einer gefuehrten: eine
Trance wird langsamer, nicht gleichmaessig langsam, und am Ende kommt der
Mensch zurueck.

| Abschnitt | `style` | Warum |
|---|---|---|
| **Ankommen** | `calm and warm, unhurried, gentle` | noch nicht fluesternd — der Mensch ist wach und muss dir folgen koennen |
| **Vertiefen** | `speaking slowly, calm and meditative, with long pauses, soft and warm` | hier entsteht die Trance, hier wirkt das Tempo am meisten |
| **Hauptteil** | `speaking slowly, calm and meditative, with long pauses, soft and warm` | gleich bleiben — ein Wechsel mitten im Bild weckt auf |
| **Verankern** | `speaking slowly, warm and affirming, with long pauses` | etwas mehr Traglast auf dem Satz, der mitgenommen wird |
| **Abschluss, Einschlafen** | `extremely slow, very soft, barely above a whisper, with very long pauses` | es soll ausklingen, nicht enden |
| **Abschluss, Zurueckholen** | `calm but clearer, gradually more present, moderate pace` | wer zurueckkommt, braucht wieder Kontur |

Zwei Dinge dazu:

- **Zwischen zwei Abschnitten nur eine Stufe wechseln**, nie von fluesternd auf
  wach. Der Sprung ist hoerbar und reisst heraus.
- **Die Stimme bleibt dieselbe** ueber alle Abschnitte. Nur der `style` wandert.
  Eine wechselnde Stimme ist ein Schnittfehler, kein Stilmittel.

Zwei Regeln dazu:

- **Auf Englisch**, auch wenn der Text deutsch ist. Die Anweisung ist technisch,
  nicht Teil der Aufnahme.
- **Niemals in den `text` schreiben.** Der Text ist ein woertliches Transkript —
  was dort steht, wird vorgelesen. Daran ist es bis zum 14.10.2026 gescheitert,
  und daraus hatten wir den falschen Schluss gezogen, die Engine koenne keinen
  Stil.

Reicht das Tempo noch nicht, verlaengere zusaetzlich die **Pausen** zwischen den
Abschnitten; klingt die Stimme selbst falsch, nimm eine **andere Stimme**.

Vorspielen, fragen, erst dann weiter. Eine andere Stimme kostet 1–3 Credits
statt der ganzen Aufnahme.

---

## Schritt 5: Alle Abschnitte und die Abmischung

Restliche Abschnitte **einzeln** mit derselben Stimme. Je Abschnitt die
**Audio-ID** aus der Download-URL notieren.

Vorher Gesamtkosten und Guthaben nennen (`my_credits`). Je Abschnitt mindestens
1 Credit, bei 600 Zeichen auf Studio etwa 2.

```
audio_assemble(
  segments = [{ audio_id, pause_after_seconds }, ...],   // in Reihenfolge
  music_id = <id>,
  music_volume = 0.25,
  lead_in_seconds = 8,
  lead_out_seconds = 15
)
```

Was von selbst passiert: Musik wird **geloopt**, blendet ein und aus; **jeder
Abschnitt auf denselben Pegel** gebracht; Musik **unter der Stimme** leiser und
in den Pausen zurueck; Vor- und Nachlauf sind Musik ohne Worte.

Richtwerte: `music_volume` 0.2–0.3, bei „eindringlich" eher 0.15. Zum
Einschlafen `lead_out_seconds` auf 30–60.

**Schlaegt es fehl**, erst dann der lokale Weg — und sag, dass es der Ausweichweg
ist. Dort dasselbe nachbauen: Pegel angleichen, Musik unter die Stimme,
Ein- und Ausblende, Pausen.

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
