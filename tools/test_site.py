import asyncio, json
from playwright.async_api import async_playwright
SHOT='/tmp/claude-0/-home-claude/a6fa72ec-5d98-51e7-9357-7a27bf17a9fb/scratchpad'
IPAD_UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.0 Safari/605.1.15'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        ctx=await b.new_context(viewport={'width':1180,'height':820}, user_agent=IPAD_UA, has_touch=True, is_mobile=False)
        await ctx.add_init_script("Object.defineProperty(navigator,'maxTouchPoints',{get:()=>5})")
        pg=await ctx.new_page(); errs=[]; reqs=[]
        pg.on('pageerror',lambda e: errs.append(str(e))); pg.on('request',lambda r: reqs.append(r.url))
        await pg.goto('http://localhost:8766/'); await pg.wait_for_timeout(1500)
        hint=await pg.evaluate("document.getElementById('installVeil').classList.contains('on')")
        font=await pg.evaluate("document.fonts.check('500 20px Fredoka')")
        await pg.screenshot(path=SHOT+'/site_hint.png')
        await pg.click('#installOk'); await pg.wait_for_timeout(300)
        await pg.reload(); await pg.wait_for_timeout(1200)
        hint2=await pg.evaluate("document.getElementById('installVeil').classList.contains('on')")
        btn=await pg.evaluate("!!document.getElementById('installBtn')")
        sw=await pg.evaluate("navigator.serviceWorker.getRegistration().then(r=>!!(r&&r.active))")
        external=[u for u in reqs if not u.startswith('http://localhost')]
        # Offline: Netz abschalten und neu laden
        await ctx.set_offline(True); await pg.reload(); await pg.wait_for_timeout(1200)
        offline_ok=await pg.evaluate("document.querySelectorAll('.choice').length")
        await ctx.set_offline(False)
        print(json.dumps({'Anleitung beim ersten Besuch':hint,'Anleitung beim zweiten Besuch':hint2,'Knopf Als App speichern':btn,'Schrift geladen':font,'Offline-Speicher aktiv':sw,'Auswahltasten offline':offline_ok,'Externe Anfragen':external,'Fehler':errs}, ensure_ascii=False, indent=1))
        # Desktop ohne iPad: keine Anleitung
        pg2=await b.new_page(); await pg2.goto('http://localhost:8766/'); await pg2.wait_for_timeout(900)
        print('Desktop-Browser zeigt Anleitung:', await pg2.evaluate("document.getElementById('installVeil').classList.contains('on')"))
        await b.close()
asyncio.run(main())
