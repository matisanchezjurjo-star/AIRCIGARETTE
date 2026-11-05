"""Engraving reference for the real F1A device (black mouthpiece + walnut body, ~105 x 15 mm),
drawn from the supplier's photos, with the exact pita logo engraved at the tip of the wood. Run: python3 build_device.py"""
import os, sys, math, subprocess
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,os.path.dirname(HERE)); os.chdir(HERE)
from artlib import text, logo, logo_h, WINE
D=15; X0,Y0=18,30; CY=Y0+D/2; MP=40; L=105
# mouthpiece radius profile (x from the tip, mm) -> radius (mm), from the photos
KEYS=[(0,5.3),(1.2,5.6),(3,5.0),(8,3.8),(12,3.5),(14.5,3.6),(15.5,4.4),(17,4.4),(18,3.6),(29,3.5),(33,4.6),(35.5,6.6),(36.5,7.1),(40,7.1)]
def r_at(x):
    for (x1,r1),(x2,r2) in zip(KEYS,KEYS[1:]):
        if x1<=x<=x2:
            t=(x-x1)/(x2-x1); t=(1-math.cos(math.pi*t))/2; return r1+(r2-r1)*t
    return KEYS[-1][1]
xs=[i*0.25 for i in range(int(MP/0.25)+1)]
top=[(X0+x,CY-r_at(x)) for x in xs]; bot=[(X0+x,CY+r_at(x)) for x in reversed(xs)]
mp='M'+' L'.join(f'{x:.2f} {y:.2f}' for x,y in top+bot)+' Z'
grain=''.join(f'<path d="M{X0+MP} {Y0+1.2+i*1.15} C{X0+60} {Y0+0.6+i*1.15+((i*7)%3-1)*0.5} {X0+85} {Y0+1.8+i*1.15} {X0+L} {Y0+1.1+i*1.15}" stroke="#2E1A0F" stroke-width="0.18" fill="none" opacity="0.45"/>' for i in range(12))
lw=14; lh=logo_h(lw); LXp=X0+L-3-lw
eng=f'<g opacity="0.92">{logo(LXp,CY-lh/2,lw,"#24130A","#24130A")}</g>'
# end view inset
EX,EY=X0+L+14,CY
endv=(f'<circle cx="{EX}" cy="{EY}" r="7.5" fill="url(#woodr)"/><circle cx="{EX}" cy="{EY}" r="4.6" fill="#8d8d8d"/><circle cx="{EX}" cy="{EY}" r="3.9" fill="#c9c9c9"/>'
      f'<circle cx="{EX}" cy="{EY}" r="2.9" fill="#3a3a3a"/>'+''.join(f'<path d="M{EX-2.6} {EY-2.2+i*0.75} H{EX+2.6}" stroke="#9a9a9a" stroke-width="0.25"/>' for i in range(7)))
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="160mm" height="80mm" viewBox="0 0 160 80">
<defs><linearGradient id="metal" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3c3c3c"/><stop offset=".3" stop-color="#121212"/><stop offset=".62" stop-color="#202020"/><stop offset="1" stop-color="#050505"/></linearGradient>
<linearGradient id="wood" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7A4E30"/><stop offset=".4" stop-color="#5E3922"/><stop offset="1" stop-color="#341E12"/></linearGradient>
<radialGradient id="woodr"><stop offset="0" stop-color="#6B4126"/><stop offset="1" stop-color="#3E2416"/></radialGradient></defs>
<rect width="160" height="80" fill="#F3E6C4"/>
<ellipse cx="{X0+55}" cy="{Y0+D+5}" rx="54" ry="2.2" fill="#000" opacity=".12"/>
<rect x="{X0+MP-0.5}" y="{Y0}" width="{L-MP+0.5}" height="{D}" rx="1.6" fill="url(#wood)"/>{grain}
<path d="{mp}" fill="url(#metal)"/>
{eng}{endv}
<path d="M{LXp} {Y0+D+9} H{LXp+lw} M{LXp} {Y0+D+7.5} V{Y0+D+10.5} M{LXp+lw} {Y0+D+7.5} V{Y0+D+10.5}" stroke="{WINE}" stroke-width="0.3"/>
{text(f"≈ {lw} mm",LXp+lw/2,Y0+D+14,2.5,"semibold",WINE,"middle")}{text("3 mm from the end",LXp+lw/2,Y0+D+18,2.2,"medium",WINE,"middle")}
{text("black mouthpiece",X0+MP/2,Y0-7,2.6,"semibold",WINE,"middle")}
{text("walnut body",X0+(MP+L)/2,Y0-7,2.6,"semibold",WINE,"middle")}
{text("end view",EX,Y0-7,2.6,"semibold",WINE,"middle")}
{text("metal ring:",EX,Y0+D+6,2.2,"medium",WINE,"middle")}{text("no engraving",EX,Y0+D+9,2.2,"medium",WINE,"middle")}
{text("pita · F1A engraving reference · logo laser-engraved at the tip of the walnut body",8,72,2.6,"medium",WINE)}
</svg>'''
open('pita-device-engraving.svg','w').write(svg)
open('preview.html','w').write('<html><body style="margin:0"><img src="pita-device-engraving.svg" style="width:1512px;display:block"></body></html>')
js=f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage({{viewport:{{width:1512,height:756}}}});
await p.goto('file://{HERE}/preview.html');await p.screenshot({{path:'{HERE}/pita-device-engraving.png'}});
await p.goto('file://{HERE}/pita-device-engraving.svg');await p.pdf({{path:'{HERE}/pita-device-engraving.pdf',width:'160mm',height:'80mm',printBackground:true,pageRanges:'1'}});await b.close();}})();"""
open('/tmp/_rd.js','w').write(js); subprocess.run(['node','/tmp/_rd.js'],check=True); os.remove('/tmp/_rd.js'); print('ok')
