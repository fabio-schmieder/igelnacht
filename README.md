# Igelnacht

Ein kooperatives Spiel für Kinder ab 5 Jahren, gemacht fürs iPad. Ein Igel hat sich in der Nacht verlaufen: Gemeinsam sucht ihr ihn mit euren Glühwürmchen im dunklen Garten und bringt ihn vor Sonnenaufgang heim ins Nest. Gewürfelt wird mit einem echten Würfel.

**Spielen:** [igelnacht.ch](https://igelnacht.ch) im Safari auf dem iPad öffnen und über Teilen → „Zum Home-Bildschirm“ als App speichern. Danach läuft das Spiel im ganzen Bildschirm und ohne Internet.

## Aufbau

- `site/` – die veröffentlichte Website (wird von GitHub Pages ausgeliefert)
- `tools/igelnacht-quelle.html` – das Spiel als einzelne Datei
- `tools/build.py` – baut daraus `site/index.html` und die Offline-Datei `site/sw.js`
- `tools/icons.py` – rendert die App-Symbole

Nach einer Änderung am Spiel: `python3 tools/build.py tools/igelnacht-quelle.html`

## Datenschutz

Das Spiel sammelt keine Daten, setzt keine Cookies und lädt nichts von fremden Servern. Auf dem Gerät gespeichert werden nur die Einstellung für Geräusche und ob die Installationsanleitung schon gezeigt wurde.
