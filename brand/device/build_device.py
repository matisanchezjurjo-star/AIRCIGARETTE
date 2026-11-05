"""Engraving reference: F1A device (black mouthpiece + walnut body, 105 x 15 mm) with the exact pita logo. Run: python3 build_device.py"""
import os, sys, subprocess
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,os.path.dirname(HERE)); os.chdir(HERE)
from artlib import text, logo, logo_h, WINE
# drawn horizontally, scale 1 unit = 1 mm. Mouthpiece left (0..45), wood body right (45..105). Diameter 15.
D=15; X0,Y0=20,30
mp=(f'<path d="M{X0} {Y0+2.5} C{X0+4} {Y0+1} {X0+7} {Y0+1} {X0+10} {Y0+3} C{X0+13} {Y0+5} {X0+15} {Y0+5} {X0+18} {Y0+3} '
    f'C{X0+21} {Y0+1} {X0+24} {Y0+1} {X0+27} {Y0+3} C{X0+30} {Y0+5} {X0+33} {Y0+4} {X0+36} {Y0+1.5} L{X0+40} {Y0+0.5} H{X0+45} '
    f'V{Y0+D-0.5} H{X0+40} L{X0+36} {Y0+D-1.5} C{X0+33} {Y0+D-4} {X0+30} {Y0+D-5} {X0+27} {Y0+D-3} C{X0+24} {Y0+D-1} {X0+21} {Y0+D-1} {X0+18} {Y0+D-3} '
    f'C{X0+15} {Y0+D-5} {X0+13} {Y0+D-5} {X0+10} {Y0+D-3} C{X0+7} {Y0+D-1} {X0+4} {Y0+D-1} {X0} {Y0+D-2.5} Z" fill="url(#metal)"/>')
grain=''.join(f'<path d="M{X0+45} {Y0+1.2+i*1.15} C{X0+65} {Y0+0.6+i*1.15+((i*7)%3-1)*0.5} {X0+85} {Y0+1.8+i*1.15} {X0+105} {Y0+1.1+i*1.15}" stroke="#3B2314" stroke-width="0.18" fill="none" opacity="0.45"/>' for i in range(12))
lw=14; lh=logo_h(lw)
eng=f'<g opacity="0.92">{logo(X0+105-3-lw,Y0+(D-lh)/2,lw,"#2A160C","#2A160C")}</g>'
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="145mm" height="80mm" viewBox="0 0 145 80">
<defs><linearGradient id="metal" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a3a3a"/><stop offset=".35" stop-color="#0d0d0d"/><stop offset=".7" stop-color="#1c1c1c"/><stop offset="1" stop-color="#050505"/></linearGradient>
<linearGradient id="wood" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8A5A38"/><stop offset=".4" stop-color="#6B4126"/><stop offset="1" stop-color="#3E2416"/></linearGradient></defs>
<rect width="145" height="80" fill="#F3E6C4"/>
<ellipse cx="{X0+55}" cy="{Y0+D+5}" rx="52" ry="2.2" fill="#000" opacity=".12"/>
{mp}<rect x="{X0+45}" y="{Y0}" width="60" height="{D}" rx="1.2" fill="url(#wood)"/>{grain}{eng}
<rect x="{X0+44.5}" y="{Y0}" width="1.5" height="{D}" fill="#111"/>
<path d="M{X0+88} {Y0+D+9} H{X0+88+lw} M{X0+88} {Y0+D+7.5} V{Y0+D+10.5} M{X0+88+lw} {Y0+D+7.5} V{Y0+D+10.5}" stroke="{WINE}" stroke-width="0.3"/>
{text(f"≈ {lw} mm",X0+88+lw/2,Y0+D+14,2.6,"semibold",WINE,"middle")}
<path d="M{X0+45} {Y0-6} H{X0+105} M{X0+45} {Y0-7.5} V{Y0-4.5} M{X0+105} {Y0-7.5} V{Y0-4.5}" stroke="{WINE}" stroke-width="0.3"/>
{text("walnut body",X0+75,Y0-9,2.6,"semibold",WINE,"middle")}
{text("black mouthpiece",X0+22,Y0-9,2.6,"semibold",WINE,"middle")}
{text("pita · F1A engraving reference · logo laser-engraved at the tip of the walnut body (3 mm from the end)",8,72,2.6,"medium",WINE)}
</svg>'''
open('pita-device-engraving.svg','w').write(svg)
open('preview.html','w').write('<html><body style="margin:0"><img src="pita-device-engraving.svg" style="width:1370px;display:block"></body></html>')
js=f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage({{viewport:{{width:1370,height:756}}}});
await p.goto('file://{HERE}/preview.html');await p.screenshot({{path:'{HERE}/pita-device-engraving.png'}});
await p.pdf({{path:'{HERE}/pita-device-engraving.pdf',width:'145mm',height:'80mm',printBackground:true,pageRanges:'1'}});await b.close();}})();"""
open('/tmp/_rd.js','w').write(js); subprocess.run(['node','/tmp/_rd.js'],check=True); os.remove('/tmp/_rd.js'); print('ok')
