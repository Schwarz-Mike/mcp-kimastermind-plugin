---
name: kimastermind-setup
description: "Prüft die Verbindung zu KI Mastermind und führt durch die Einrichtung. Verwende diesen Skill, wenn jemand die Einrichtung prüfen will, fragt ob die Verbindung steht, nach dem Credit-Guthaben fragt, wissen will welche Skills oder Möglichkeiten verfügbar sind, oder wenn ein Aufruf an KI Mastermind scheitert — Trigger: \"kimastermind setup\", \"einrichtung prüfen\", \"funktioniert kimastermind\", \"bin ich verbunden\", \"wie viele credits habe ich\", \"kimastermind geht nicht\", \"verbindung testen\", \"was kann ich hier machen\", \"welche modelle gibt es\", \"welche skills gibt es\", \"sind die skills installiert\", \"ist alles eingerichtet\", \"warum klappt das nicht\"."
version: 1.4.1
---

# KI Mastermind — Einrichtung prüfen

Prüfe die Einrichtung von KI Mastermind und führe die Person durch, was noch fehlt.
Arbeite die Schritte der Reihe nach ab und berichte in einem Stück, nicht pro Schritt.

## Verwandte Skills — die KIM-Familie

Derselbe Server und dasselbe Credit-Guthaben treiben drei Arbeits-Skills an. Dieser hier
prüft nur die Einrichtung; sobald jemand wirklich etwas erzeugen will, übernimmt der
passende:

| Skill | Wofür |
|---|---|
| **kimastermind-setup** (dieser) | Verbindung, Guthaben, was verfügbar ist, Fehlersuche |
| **kim-images** | Bilder: erstellen, bearbeiten, umstilisieren, Varianten, kombinieren |
| **kim-video** | Videoclips: Text-zu-Video, ein Bild animieren, Referenz-zu-Video |
| **kim-voice** | Sprache: Text vorlesen, Voiceover, Vertonung — zwei Engines zur Wahl |
| **kim-music** | Musik: Hintergrund, Intro, Lied mit Gesang — drei Engines, Unterschied ist die Laenge |
| **kim-lernfilm** | Der ganze Film: Storyboard, Bilder, Stimme, Musik, Clips und Schnitt in einem Ablauf |
| **kim-meditation** | Gefuehrte Meditation: Skript, Musik, Stimme und Abmischung in vier freigegebenen Schritten |
| **kim-sfx** | Geraeusche und Atmosphaeren, Laenge frei waehlbar |

### Welche davon sind hier wirklich aktiv?

Nenne nicht nur, was es gibt, sondern was **in dieser Sitzung geladen ist**. Du siehst
deine eigenen Skills — gleiche sie gegen die Liste oben ab und berichte als Tabelle:

| Skill | Status | Wofür |
|---|---|---|
| kimastermind-setup | ✅ aktiv | Einrichtung und Fehlersuche |
| kim-images | ✅ aktiv / ❌ fehlt | Bilder |
| kim-video | ✅ aktiv / ❌ fehlt | Videoclips |
| kim-voice | ✅ aktiv / ❌ fehlt | Sprache |
| kim-music | ✅ aktiv / ❌ fehlt | Musik |
| kim-lernfilm | ✅ aktiv / ❌ fehlt | Ganze Filme |
| kim-meditation | ✅ aktiv / ❌ fehlt | Meditationen |
| kim-sfx | ✅ aktiv / ❌ fehlt | Geraeusche |

`KIMASTERMIND_IMAGES:list_skills` nennt zusätzlich, welche Skill-Dateien der Server
aktuell anbietet, mit Download-Link. Weicht das von dem ab, was hier geladen ist, ist
die Plugin-Version veraltet — dann in den Plugin-Einstellungen auf **Aktualisieren**
klicken und Claude neu starten.

Fehlt ein Skill ganz, liegt das fast immer daran, dass das Plugin nach der Installation
noch nicht neu geladen wurde. Claude neu starten löst es.

## Vorgehen

**1. Verbindung prüfen**

Rufe `KIMASTERMIND_IMAGES:my_credits` auf. Das ist der günstigste Aufruf und beweist
dreierlei zugleich: der Server ist erreichbar, die Anmeldung steht, und das Konto
existiert.

- **Antwort kommt** → Verbindung steht, die Anmeldung ist gültig, das Konto existiert.
  Nenne das Guthaben. Damit ist „MCP funktioniert" belegt — nicht durch das blosse
  Vorhandensein der Werkzeuge, sondern durch einen echten Aufruf.
- **Fehler „not authenticated" / Anmeldefenster** → die Anmeldung fehlt noch. Sag der
  Person, dass sich beim ersten Aufruf ein Browserfenster öffnet, in dem sie sich mit
  ihrem KI-Mastermind-Konto anmeldet und den Zugriff bestätigt. Das passiert einmalig.
- **Werkzeuge gar nicht vorhanden** → der Server ist nicht verbunden. Weiter bei Schritt 4.

**2. Guthaben beurteilen**

Nenne den Stand und ordne ihn ein, statt nur eine Zahl zu melden:

- **0 Credits** → es funktioniert nichts, auch wenn die Verbindung steht. Verweise auf
  https://mcp.kimastermind.net/dashboard zum Aufladen.
- **1–4 Credits** → reicht noch für ein einfaches Bild oder eine kurze Sprachaufnahme,
  aber nicht für ein Video. Sag das klar.
- **ab 5 Credits** → alles möglich; ein Video kostet je nach Länge und Auflösung deutlich
  mehr, also bei Videowünschen vorher rechnen lassen.

Neue Konten starten mit 20 Credits gratis.

**3. Die vier Fähigkeiten einzeln prüfen**

Ein Check, der nur „Verbindung steht" meldet, ist wertlos — er sagt nichts
darüber, ob das, was die Person vorhat, auch wirklich geht. Prüfe deshalb jede
Fähigkeit einzeln und melde sie als Tabelle. **Alle Prüfungen sind kostenlos**,
keine davon erzeugt etwas:

| Fähigkeit | Prüfung | Beweist |
|---|---|---|
| **MCP-Verbindung** | `my_credits` | Server erreichbar, Anmeldung gültig, Konto existiert |
| **Bilder** | `list_models` → Einträge mit `kind: image` | Bildmodelle vorhanden, mit Credit-Preis je Stufe |
| **Video** | `list_models` → `kind: video` | Videomodell vorhanden, Credits **pro Sekunde** |
| **Stimmen** | `voice_listing` ohne Engine | beide Engines antworten, mit Preis und Stimmenzahl |
| **Musik** | `list_models` → `kind: music` | **drei** Musik-Engines vorhanden, zwei pro Stueck, eine pro Minute |
| **Geraeusche** | `list_models` → `kind: sfx` | Geraeusch-Generator vorhanden, **ein Credit je Geraeusch**, Laenge egal |
| **Filmschnitt** | `film_assemble` ist in der Werkzeugliste | Zusammenschnitt moeglich, kostenlos |
| **Tonmischung** | `audio_assemble` ist in der Werkzeugliste | Meditation und Hoerbuch mischbar, kostenlos |

Melde das so:

```
Verbindung    ✅  Guthaben 96 Credits
Bilder        ✅  21 Modelle
Video         ✅  8.33 Credits/Sekunde (720p)
Stimmen       ✅  Express 3.0 / Studio 3.84 Credits je 1000 Zeichen, 58 Stimmen
Musik         ✅  Pro 10/Minute · Advanced 16 · Basic 6 je Stueck
Geraeusche    ✅  1 Credit je Geraeusch, 0,5-22 Sekunden
Schnitt       ✅  film_assemble und audio_assemble verfuegbar
```

Fehlt eine Fähigkeit, sag **welche** und was das praktisch heisst — „Musik ist
gerade nicht verfügbar, Bilder, Video und Stimmen laufen" ist brauchbar,
„teilweise verfügbar" nicht.

Zahlen immer aus der Antwort nehmen, nie aus dem Gedächtnis: die Preise stehen
in der Datenbank und ändern sich.

**4. Verfügbare Möglichkeiten zeigen**

Nur wenn die Person danach fragt oder neu ist — nicht ungefragt bei jedem Check.

Rufe `KIMASTERMIND_IMAGES:list_models` auf und fasse zusammen, **was** möglich ist, nicht
welche Modelle es gibt: Bilder (mit Referenzbild-Bearbeitung), Videoclips, Sprachausgabe.
Nenne die Credit-Kosten pro Bereich, denn die unterscheiden sich in der Einheit:

- Bilder: pro Bild, je nach Qualitätsstufe
- Videos: pro Sekunde
- Sprache: pro 1000 Eingabezeichen, mindestens 1 Credit. Es gibt **zwei Engines**
  mit unterschiedlichem Preis und Tempo — **Express** (schnell, guenstiger) und
  **Studio** (langsamer, hoehere Qualitaet). `voice_listing` ohne Engine nennt
  beide mit dem aktuellen Preis.

Musik gibt es in **drei Engines**, die sich in der **Laenge** unterscheiden,
nicht in der Qualitaet: **Pro** liefert exakt die bestellte Laenge von 10
Sekunden bis 5 Minuten und wird pro Minute abgerechnet; **Advanced** kann singen
und liefert den Text mit Zeitmarken, seine Laenge folgt aber der Beschreibung
und laesst sich nicht einstellen; **Basic** ist nur instrumental und fest bei 33
Sekunden. Wer eine bestimmte Laenge braucht, nimmt Pro — das ist bei kurzen
Stuecken sogar das Guenstigste.

Geraeusche sind etwas anderes als Musik: Regen, Meer, Feuer, Gong, Tuer. Die
Laenge ist frei waehlbar von einer halben bis 22 Sekunden, und **ein Geraeusch
kostet einen Credit, unabhaengig von der Laenge**. Der Musikgenerator kann keine
Geraeusche machen — nach Regen gefragt liefert er Musik, die an Regen erinnert.

Für die Stimmen gibt es `voice_listing` (beide Engines) und **kostenlose Hörproben auf
einer Seite pro Engine** — erwähne das, weil es der einzige Bereich ist, in dem man vor
dem Bezahlen reinhören kann:

```
https://mcp.kimastermind.net/voices/studio
https://mcp.kimastermind.net/voices/express
```

Eine Kachel pro Stimme, Antippen spielt ab, ohne Anmeldung. Ist ein Browser-Werkzeug
vorhanden, öffne die Studio-Seite gleich darin.

**5. Wenn die Werkzeuge fehlen**

Dann ist der Server nicht verbunden. Nenne beide Wege und weise auf die Doppelregistrierung
hin:

```bash
claude plugin marketplace add Schwarz-Mike/mcp-kimastermind-plugin
claude plugin install kimastermind@kimastermind
```

Oder von Hand nur die Serververbindung:

```bash
claude mcp add --transport http --scope user kimastermind https://mcp.kimastermind.net/image
```

> **Nur einen der beiden Wege wählen.** Das Plugin bringt die Serververbindung schon mit.
> Wer zusätzlich `claude mcp add` ausführt, hat den Server doppelt registriert und sieht
> jedes Werkzeug zweimal.

Danach Claude neu starten. Konto anlegen unter https://mcp.kimastermind.net/register.

**6. Bericht**

Fasse zusammen: Verbindung, Guthaben, geladene Skills, die vier Fähigkeiten, und
was als Nächstes zu tun ist. Fünf Zeilen, keine Prosa.
Wenn alles steht, frag nicht „kann ich sonst helfen?", sondern biete den konkreten
nächsten Schritt an — ein Bild, einen Clip oder eine Sprachaufnahme.

---

## Fehlersuche

| Symptom | Ursache | Was zu tun ist |
|---|---|---|
| Werkzeuge erscheinen **doppelt** | Server über Plugin **und** `claude mcp add` registriert | Einen der beiden entfernen: `claude mcp remove kimastermind` oder das Plugin deinstallieren |
| „Insufficient credits" | Guthaben zu niedrig für diese Generierung | Die Fehlermeldung nennt die benötigte Zahl. Aufladen im Dashboard |
| Anmeldefenster kommt immer wieder | Sitzung wird nicht gespeichert | Claude neu starten; hält es dann nicht, an support@kimastermind.net |
| Download-Link einer Sprachaufnahme liefert einen Fehler | Der Link gilt nur **24 Stunden**, danach wird die Datei gelöscht | Neu generieren (kostet wieder Credits). Vorher speichern |
| Generierung bricht ab | Anbieterseitige Störung | Credits werden **automatisch zurückgebucht** — das sagen, damit niemand denkt, der Versuch habe Geld gekostet. Einmal erneut versuchen |
| Video „hängt" | Videogenerierung läuft synchron und dauert 1–5 Minuten | Nicht abbrechen, nicht neu starten. Es arbeitet |
| Skills fehlen nach dem Plugin-Install | Plugin lädt erst beim nächsten Sitzungsstart | Claude neu starten, oder `/reload-plugins` |

Hilft nichts davon: **support@kimastermind.net**, mit der genauen Fehlermeldung.

---

## Sprache und Ton

- Standardsprache: Deutsch, Du-Form
- Schweizer Schreibweise: ss statt sz
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
- Beschreibende Bezeichnungen verwenden: **Bild-Generator**, **Video-Generator**,
  **Stimmen-Generator**
- Kurz halten. Ein Einrichtungs-Check ist eine Statusmeldung, kein Aufsatz.
