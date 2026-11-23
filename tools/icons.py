# Rendert das App-Symbol mit den Zeichnungen aus dem Spiel selbst (Igel, Gluehwuermchen)
import asyncio, sys
from playwright.async_api import async_playwright
SRC='file:///mnt/user-data/outputs/igelnacht.html'; OUT=sys.argv[1]
SVG = """(pad)=>{ const s=document.createElementNS('http://www.w3.org/2000/svg','svg');
  s.setAttribute('viewBox','0 0 512 512'); s.setAttribute('width','512'); s.setAttribute('height','512'); s.id='ico';
  s.style.cssText='position:fixed;left:0;top:0;z-index:999;display:block';
  let stars=''; const r=(n)=>{let x=Math.sin(n*99.1)*10000;return x-Math.floor(x)};
  for(let i=0;i<26;i++) stars+=`<circle cx="${(r(i)*512).toFixed(0)}" cy="${(r(i+40)*300).toFixed(0)}" r="${(1.5+r(i+80)*2.5).toFixed(1)}" fill="#fbf4e4" opacity="${(.35+r(i+7)*.5).toFixed(2)}"/>`;
  const k=pad?0.78:1;
  s.innerHTML=`<defs><radialGradient id="icBg" cx=".5" cy=".35" r=".85"><stop offset="0" stop-color="#3a3f8f"/><stop offset=".6" stop-color="#23296a"/><stop offset="1" stop-color="#10153a"/></radialGradient>
    <radialGradient id="icGround" cx=".5" cy=".2" r=".8"><stop offset="0" stop-color="#5d9a7c"/><stop offset="1" stop-color="#2c5d63"/></radialGradient>
    <radialGradient id="icLight"><stop offset="0" stop-color="#fff3c4" stop-opacity=".55"/><stop offset="1" stop-color="#fff3c4" stop-opacity="0"/></radialGradient></defs>
    <rect width="512" height="512" fill="url(#icBg)"/>${stars}
    <g transform="translate(256 256) scale(${k}) translate(-256 -256)">
      <g transform="translate(392 118)"><circle r="78" fill="#fbf4e4" opacity=".08"/><circle r="48" fill="#fbf4e4"/><circle cx="20" cy="-13" r="41" fill="#2f3580"/></g>
      <ellipse cx="256" cy="470" rx="330" ry="150" fill="url(#icGround)"/>
      <circle cx="250" cy="330" r="150" fill="url(#icLight)"/>
      <g transform="translate(244 352) scale(4.6)">${ART.hog('walk')}</g>
      <g transform="translate(300 196) scale(2.3)">${ART.fly(0)}</g>
    </g>`;
  document.body.appendChild(s); }"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for name,size,pad in [('apple-touch-icon.png',180,False),('icon-192.png',192,False),('icon-512.png',512,False),('icon-maskable-512.png',512,True)]:
            pg=await b.new_page(viewport={'width':512,'height':512}, device_scale_factor=size/512)
            await pg.goto(SRC); await pg.wait_for_timeout(200)
            await pg.evaluate(SVG, pad); await pg.wait_for_timeout(150)
            await pg.locator('#ico').screenshot(path=f'{OUT}/{name}')
            await pg.close()
        await b.close()
asyncio.run(main())
