# KI Mastermind für Claude

Bilder, Videos und Stimmen direkt in Claude erzeugen — über den KI-Mastermind-Server.
Das Plugin bringt die Serververbindung und fünf fertige Skills in einem Schritt mit.

---

## ⚠️ Voraussetzung: Konto und Credits

Ohne KI-Mastermind-Konto funktioniert die Verbindung nicht.

1. **Konto anlegen:** [mcp.kimastermind.net/register](https://mcp.kimastermind.net/register)
2. **Credits** — jede Generierung kostet Credits. Neue Konten starten mit 20 Credits gratis;
   danach wird im Dashboard aufgeladen. Ohne Guthaben lehnt der Server jede Anfrage ab,
   auch wenn die Verbindung steht.
3. **Anmelden**, wenn Claude beim ersten Aufruf danach fragt (siehe unten).

Fragen oder Probleme: **support@kimastermind.net**

---

## Installation

### Schon KIM-Skills einzeln installiert?

Dann bitte vorher entfernen, sonst hast du sie doppelt — das Plugin bringt alle mit und
hält sie aktuell:

```bash
rm -rf ~/.claude/skills/{kim-images,kim-video,kim-voice,kim-music,kimastermind-setup,image-generator}
```

Unter Windows in der PowerShell:

```powershell
"kim-images","kim-video","kim-voice","kimastermind-setup","image-generator" | ForEach-Object {
  Remove-Item -Recurse -Force "$env:USERPROFILE\.claude\skills\$_" -ErrorAction SilentlyContinue }
```

### Variante A — Claude Desktop, über die Oberfläche (empfohlen)

**Anpassen → Plugins → Marketplace hinzufügen** → eintragen:

```
Schwarz-Mike/mcp-kimastermind-plugin
```

Dann das Plugin **KI Mastermind** installieren. Anschliessend fragt Claude, ob der
KI-Mastermind-Server verbunden werden darf — das bestätigen. Kein Terminal nötig.

### Variante B — Terminal

Wer die `claude`-CLI nutzt:

```bash
claude plugin marketplace add Schwarz-Mike/mcp-kimastermind-plugin
claude plugin install kimastermind@kimastermind
```

Dieselben Befehle funktionieren auch als Slash-Befehle in einer Claude-Code-Sitzung:
`/plugin marketplace add Schwarz-Mike/mcp-kimastermind-plugin`, dann
`/plugin install kimastermind@kimastermind`.

Nur die Serververbindung ohne Plugin:

```bash
claude mcp add --transport http --scope user kimastermind https://mcp.kimastermind.net/image
```

> **Nur einen Weg wählen.** Das Plugin bringt die Serververbindung schon mit. Wer
> zusätzlich `claude mcp add` ausführt oder den Server ein zweites Mal bestätigt, hat ihn
> doppelt registriert und sieht jedes Werkzeug zweimal.

Danach Claude neu starten.

**Beim ersten Aufruf öffnet sich ein Anmeldefenster im Browser.** Dort meldest du dich mit
deinem KI-Mastermind-Konto an und bestätigst den Zugriff. Das passiert einmalig — danach
bleibt die Verbindung bestehen.

Zum Prüfen, ob alles läuft, sag einfach:

> „Prüf mal meine KI-Mastermind-Einrichtung"

Claude geht dann durch, ob die Verbindung steht, wie viel Guthaben du hast und was
verfügbar ist.

---

## Was das Plugin mitbringt

### Die Serververbindung

Ein Remote-MCP-Server mit **12 Werkzeugen**:

| Bereich | Was möglich ist |
|---|---|
| **Bilder** | 21 Modelle, Text-zu-Bild, Bearbeiten, Stiltransfer, Varianten, bis zu 16 Referenzbilder, bis 4K |
| **Videos** | Clips aus Text, ein Bild animieren, Motiv/Stil aus Referenzbildern, 3–15 s, 720p/1080p |
| **Stimmen** | Text-zu-Sprache als MP3, **zwei Engines** zur Wahl, 58 Stimmen zusammen, kostenlose Hörproben |
| **Musik** | Hintergrundmusik, Intro oder ein gesungenes Stück, **zwei Engines** — eine davon singt und liefert den Liedtext mit Zeitmarken |
| **Export** | Format und Grösse ändern (JPEG, PNG, WebP), Download-Link |
| **Galerie** | die letzten 30 Bilder mit Modell, Prompt und Datum |
| **Konto** | aktuelles Credit-Guthaben |

### Bilder

21 Modelle, unter anderem für Fotorealismus, Text im Bild (Logos, Poster, Verpackungen),
Produktaufnahmen und schnelle Entwürfe. Du beschreibst, was du brauchst — der Skill fragt
nach Zweck, Stil, Format und Qualität und schlägt passende Modelle vor.

> „Erstelle ein Produktfoto einer Parfumflasche auf Marmor, Studiolicht"

> „Nimm dieses Bild und tausch den Hintergrund gegen eine sonnige Küche"

Bis zu **16 Referenzbilder** pro Aufruf: zum Bearbeiten, für Stiltransfer oder um mehrere
Vorlagen zu kombinieren. Bilder landen in deiner Galerie und werden in Claude Desktop
automatisch lokal gespeichert.

### Videos

Clips von 3 bis 15 Sekunden in 720p oder 1080p, in drei Modi: aus reinem Text, aus **einem**
Bild, das animiert wird, oder aus 1–9 Referenzbildern für Motiv und Stil.

> „Mach ein Video daraus: langsame Kamerafahrt, aufsteigender Dampf"

Abgerechnet wird **pro Sekunde** — ein längerer oder hochauflösender Clip kostet
entsprechend mehr. Der Skill nennt die Kosten vorher. Die Generierung läuft synchron und
dauert je nach Länge **1–5 Minuten**; das Fenster muss offen bleiben.

### Stimmen

Texte als MP3 vorlesen lassen. Es gibt **zwei Engines**, und du wählst:

| | Express | Studio |
|---|---|---|
| Stimmen | 28 (9 weiblich, 19 männlich) | 30 (14 weiblich, 16 männlich) |
| Tempo | fertig in 1–3 Sekunden | mehrere Minuten bei langen Texten |
| Klang | gleichmässig, neutral | natürlichere Betonung und Satzmelodie |
| Sprache | wählbar, 15 Sprachen | wird aus dem Text erkannt |
| Sprechstil | — | steuerbar, z. B. „warm und ruhig" |
| Credits pro 1 000 Zeichen | 3.00 | 3.84 |

**Express** für den schnellen Fall: etwas kurz anhören, ein Entwurf, eine Ansage.
**Studio**, wenn es jemand anders hört — Voiceover, Podcast-Intro, eine längere
Erzählung, bei der eine flache Lesung auffallen würde.

Claude fragt dich, welche Engine du willst, und nennt vorher beide Preise. Die
Stimmen der beiden Engines sind getrennt: eine Express-Stimme läuft nicht auf
Studio und umgekehrt.

> „Welche Stimmen gibt es?"

> „Lies das mit Eve vor" · „Nimm Sulafat, warm und ruhig"

**Hörproben sind kostenlos.** Alle 58 Stimmen sprechen denselben Satz, du kannst sie also
direkt vergleichen — auch quer über die beiden Engines. Am einfachsten auf der
Hörproben-Seite, eine Kachel pro Stimme, Antippen spielt ab, ohne Anmeldung:

- **Express:** [mcp.kimastermind.net/voices/express](https://mcp.kimastermind.net/voices/express)
- **Studio:** [mcp.kimastermind.net/voices/studio](https://mcp.kimastermind.net/voices/studio)

Für einen bestimmten Zweck hängst du ihn an, dann sind die passenden Stimmen
vorgewählt: `?for=trance`, `?for=podcast`, `?for=werbung`, `?for=hoerbuch`,
`?for=erklaervideo` — das setzt dokumentierte Stimmcharaktere voraus und wirkt
deshalb nur bei Studio.

Einzeln geht weiterhin `https://mcp.kimastermind.net/api/voice/sample/eve.mp3`
(Stimmen-ID austauschen); dieselben MP3s liegen auch im Skill, nach Engine sortiert.

Bis 5 000 Zeichen pro Aufruf. Abgerechnet wird nach **Eingabezeichen**, nicht nach
Audiolänge — die Kosten stehen also vor der Generierung fest. Am Ende bekommst du einen
Download-Link, der **24 Stunden** gilt; danach wird die Datei gelöscht.

Was die Sprachausgabe **nicht** kann: keine eigenen oder geklonten Stimmen, keine
Hintergrundmusik, kein Zusammenlegen mit einem Video, keine Untertitel. Express hat
zusätzlich keine Stilsteuerung; bei Studio ist der Stil eine Anweisung, keine Garantie, und
die Sprache lässt sich nicht erzwingen — sie folgt dem Text.

### Die Skills

Vier Arbeitsanleitungen, die Claude automatisch heranzieht, wenn sie passen. Sie kennen
einander: fragt jemand im Bild-Skill nach einem Video, gibt er die Anfrage weiter.

**`kim-images`** — Bilder erstellen, bearbeiten, umstilisieren, Varianten und
Kombinationen. Erkennt angehängte oder in der Galerie liegende Referenzbilder von selbst,
fragt Zweck, Stil, Format und Qualität ab und schlägt vier passende Modelle zur Auswahl
vor.

**`kim-video`** — Videoclips. Bestimmt den Modus aus dem, was du mitlieferst, sammelt
Format, Auflösung und Dauer und nennt Kosten **und** Wartezeit vorher.

**`kim-voice`** — Sprachausgabe. Fragt zuerst, welche Engine du willst, und nennt beide
Preise. Listet dann die Stimmen der gewählten Engine, lässt dich kostenlos reinhören,
bereitet den Text fürs Vorlesen auf (Markdown, Abkürzungen, Zahlen), warnt bei Studio vor
der Wartezeit und immer vor dem 24-Stunden-Fenster.

**`kimastermind-setup`** — prüft die Einrichtung: Verbindung, Guthaben, was verfügbar ist.
Greift automatisch bei Fragen wie „funktioniert das?" oder wenn ein Aufruf scheitert, und
enthält eine Fehlersuch-Tabelle für die häufigen Fälle — doppelt registrierte Werkzeuge,
abgelaufener Download-Link, scheinbar hängendes Video.

Nach der Installation sind sie als `/kimastermind:kim-images`, `/kimastermind:kim-video`,
`/kimastermind:kim-voice` und `/kimastermind:kimastermind-setup` auch direkt aufrufbar.

---

## Credits

| Was | Abrechnung |
|---|---|
| Bilder | pro Bild, je nach Modell und Qualitätsstufe |
| Videos | pro Sekunde, je nach Auflösung |
| Stimmen | pro 1 000 Eingabezeichen, je nach Engine, mindestens 1 Credit pro Aufnahme |
| Musik | pro Clip von rund 30 Sekunden, je nach Engine |

Die aktuellen Preise nennt Claude jederzeit — frag einfach „Was kosten die Modelle?",
oder schau im [Dashboard](https://mcp.kimastermind.net/dashboard) unter *Verfügbare
Modelle*. Scheitert eine Generierung, werden die Credits automatisch zurückgebucht.

---

## Ohne Plugin: nur die Skills

Wer den Server schon verbunden hat und nur die Skills möchte, lädt sie einzeln im
Dashboard unter *Setup MCP / Hilfe* herunter:

- [kim-images.skill](https://mcp.kimastermind.net/skills/kim-images.skill)
- [kim-video.skill](https://mcp.kimastermind.net/skills/kim-video.skill)
- [kim-voice.skill](https://mcp.kimastermind.net/skills/kim-voice.skill)
- [kimastermind-setup.skill](https://mcp.kimastermind.net/skills/kimastermind-setup.skill)

In Claude Desktop unter **Customize** hinzufügen.

---

## Lizenz

MIT — siehe `plugin.json`. Der Zugang zum Server selbst läuft über dein
KI-Mastermind-Konto.
