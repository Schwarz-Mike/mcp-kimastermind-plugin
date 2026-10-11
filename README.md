# KI Mastermind für Claude

Bilder, Videos und Stimmen direkt in Claude erzeugen — über den KI-Mastermind-Server.
Das Plugin bringt die Serververbindung und vier fertige Skills in einem Schritt mit.

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
rm -rf ~/.claude/skills/{kim-images,kim-video,kim-voice,kimastermind-setup,image-generator}
```

Unter Windows in der PowerShell:

```powershell
"kim-images","kim-video","kim-voice","kimastermind-setup","image-generator" | ForEach-Object {
  Remove-Item -Recurse -Force "$env:USERPROFILE\.claude\skills\$_" -ErrorAction SilentlyContinue }
```

### Variante A — Terminal (empfohlen)

Drei Befehle, danach nur noch anmelden:

```bash
claude plugin marketplace add Schwarz-Mike/mcp-kimastermind-plugin
claude plugin install kimastermind@kimastermind
claude mcp add --transport http --scope user kimastermind https://mcp.kimastermind.net/image
```

### Variante B — über die Oberfläche

Einstellungen → Plugins → Marketplace hinzufügen → `Schwarz-Mike/mcp-kimastermind-plugin`
eintragen → Plugin installieren. Anschliessend fragt Claude, ob der KI-Mastermind-Server
verbunden werden darf — das bestätigen.

> **Nur eine der beiden Varianten wählen.** Wer den dritten Befehl aus Variante A nutzt,
> soll den Server in Variante B **nicht** zusätzlich bestätigen — sonst ist er doppelt
> registriert und alle Werkzeuge erscheinen zweimal.

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
| **Stimmen** | Text-zu-Sprache als MP3, 28 mehrsprachige Stimmen, kostenlose Hörproben |
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

Texte als MP3 vorlesen lassen — **28 mehrsprachige Stimmen** (9 weiblich, 19 männlich).
Gedacht für Sprechertexte, Erklärfilme, Podcast-Intros oder um sich einen Text einfach
anzuhören.

> „Welche Stimmen gibt es?"

> „Lies das mit Eve vor"

**Hörproben sind kostenlos.** Jede Stimme spricht denselben Satz, du kannst sie also direkt
vergleichen, bevor du Credits ausgibst — im Browser abspielbar unter
`https://mcp.kimastermind.net/api/voice/sample/eve.mp3` (Stimmen-ID austauschen), und als
MP3 im Skill mitgeliefert.

Bis 5 000 Zeichen pro Aufruf. Abgerechnet wird nach **Eingabezeichen**, nicht nach
Audiolänge — die Kosten stehen also vor der Generierung fest. Am Ende bekommst du einen
Download-Link, der **24 Stunden** gilt; danach wird die Datei gelöscht. Jede Stimme spricht
jede unterstützte Sprache, ein Stimmwechsel pro Sprache ist nicht nötig.

Was die Sprachausgabe **nicht** kann: keine Emotions- oder Stilsteuerung, keine
Geschwindigkeitsregelung, keine eigenen oder geklonten Stimmen, keine Hintergrundmusik und
kein Zusammenlegen mit einem Video. Das Ergebnis ist eine reine Sprachaufnahme.

### Die Skills

Vier Arbeitsanleitungen, die Claude automatisch heranzieht, wenn sie passen. Sie kennen
einander: fragt jemand im Bild-Skill nach einem Video, gibt er die Anfrage weiter.

**`kim-images`** — Bilder erstellen, bearbeiten, umstilisieren, Varianten und
Kombinationen. Erkennt angehängte oder in der Galerie liegende Referenzbilder von selbst,
fragt Zweck, Stil, Format und Qualität ab und schlägt vier passende Modelle zur Auswahl
vor.

**`kim-video`** — Videoclips. Bestimmt den Modus aus dem, was du mitlieferst, sammelt
Format, Auflösung und Dauer und nennt Kosten **und** Wartezeit vorher.

**`kim-voice`** — Sprachausgabe. Listet die Stimmen, lässt dich kostenlos reinhören,
bereitet den Text fürs Vorlesen auf (Markdown, Abkürzungen, Zahlen) und warnt vor dem
24-Stunden-Fenster.

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
| Stimmen | pro 1 000 Eingabezeichen, mindestens 1 Credit pro Aufnahme |

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
