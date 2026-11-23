# Baut site/index.html und site/sw.js aus dem Spiel (igelnacht.html).
# Aufruf: python3 tools/build.py <pfad/zu/igelnacht.html>
import sys, re, hashlib, pathlib
src = pathlib.Path(sys.argv[1]).read_text(encoding='utf-8')
site = pathlib.Path(__file__).resolve().parent.parent / 'site'

GOOGLE = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600&display=swap">'
assert src.count(GOOGLE) == 1, 'Google-Fonts-Zeile nicht gefunden'
head = '\n'.join([
  '<meta name="description" content="Igelnacht: ein kooperatives Spiel für Kinder ab 5. Findet den verirrten Igel und bringt ihn vor Sonnenaufgang heim.">',
  '<meta name="theme-color" content="#10153a">',
  '<meta name="apple-mobile-web-app-capable" content="yes">',
  '<meta name="mobile-web-app-capable" content="yes">',
  '<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">',
  '<meta name="apple-mobile-web-app-title" content="Igelnacht">',
  '<link rel="manifest" href="manifest.webmanifest">',
  '<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">',
  '<link rel="icon" type="image/png" href="icons/icon-192.png">',
  # Schrift liegt lokal bei, damit nichts von Google geladen wird und das Spiel offline laeuft
  '<style>' + ''.join(
    f'@font-face{{font-family:"Fredoka";font-style:normal;font-weight:{w};font-display:swap;src:url(fonts/fredoka-latin-{w}-normal.woff2) format("woff2")}}'
    for w in (400, 500, 600)) + '</style>',
])
out = src.replace(GOOGLE, head)
reg = '<script>if("serviceWorker" in navigator){addEventListener("load",function(){navigator.serviceWorker.register("sw.js").catch(function(){});});}</script>\n</body>'
assert out.count('</body>') == 1
out = out.replace('</body>', reg)
(site / 'index.html').write_text(out, encoding='utf-8')

files = ['./', 'index.html', 'manifest.webmanifest'] + sorted(
  str(p.relative_to(site)) for p in list((site/'icons').glob('*.png')) + list((site/'fonts').glob('*.woff2')))
# Version aendert sich mit jedem Inhalt, so holen sich installierte Apps Updates
h = hashlib.sha1()
for f in files[1:]: h.update((site/f).read_bytes())
ver = h.hexdigest()[:10]
sw = f'''// Offline-Speicher fuer Igelnacht. Version wechselt automatisch mit jedem neuen Stand.
const CACHE = "igelnacht-{ver}";
const FILES = {files!r};
self.addEventListener("install", e => {{ e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting())); }});
self.addEventListener("activate", e => {{ e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())); }});
self.addEventListener("fetch", e => {{
  const req = e.request; if(req.method !== "GET" || new URL(req.url).origin !== location.origin) return;
  if(req.mode === "navigate"){{
    // Seite: zuerst aus dem Netz (fuer Updates), ohne Netz aus dem Speicher
    e.respondWith(fetch(req).then(r => {{ const c = r.clone(); caches.open(CACHE).then(x => x.put("index.html", c)); return r; }}).catch(() => caches.match("index.html")));
    return;
  }}
  e.respondWith(caches.match(req).then(hit => hit || fetch(req)));
}});
'''.replace("'", '"')
(site / 'sw.js').write_text(sw, encoding='utf-8')
print('gebaut, Cache-Version', ver, '| Dateien:', len(files))
