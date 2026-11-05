"""Full pita kit flat-lay assembled from the real artwork files. Run after the other build scripts: python3 build_kit.py"""
import os, sys, subprocess
HERE=os.path.dirname(os.path.abspath(__file__)); BR=os.path.dirname(HERE); sys.path.insert(0,BR); os.chdir(HERE)
from artlib import text, WINE
import re
_n=[0]
def crop(src,vb,x,y,w,h,full,extra='',strip=False):
    """inline a crop (viewBox vb) of an SVG file at x,y size w,h (ids prefixed to avoid clashes)."""
    _n[0]+=1; p=f'k{_n[0]}_'
    raw=open(src).read()
    inner=re.sub(r'^.*?<svg[^>]*>','',raw,count=1,flags=re.S); inner=inner[:inner.rfind('</svg>')]
    inner=re.sub(r'id="([^"]+)"',lambda m:f'id="{p}{m.group(1)}"',inner)
    inner=re.sub(r'url\(#([^)]+)\)',lambda m:f'url(#{p}{m.group(1)})',inner)
    if strip:
        inner=re.sub(r'<rect width="[0-9]+" height="80" fill="#F3E6C4"/>','',inner); inner=re.sub(r'<ellipse[^>]*/>','',inner)
        inner=re.sub(r'<path d="M[^"]*" stroke="#6B1621"[^>]*/>','',inner)
    vx,vy,vw,vh=vb
    return f'<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="{vx} {vy} {vw} {vh}" preserveAspectRatio="none" overflow="hidden"><g {extra}>{inner}</g></svg>'
def shadow(x,y,w,h,r=1.5,o=.22,dy=2.5,blur=3):
    return f'<rect x="{x}" y="{y+dy}" width="{w}" height="{h}" rx="{r}" fill="#000" opacity="{o}" filter="url(#sh)"/>'
BOX='../box/pita-box-artwork-only.svg'; BOXF=(500,405)
o=[]
# ---- open box (top-down): flap inside, lid inside, tray with foam + device
X,Y=24,30
o.append(shadow(X,Y,147,45+81+81,2))
o.append(crop(BOX,(215,232,147,126),X,Y,147,126,BOXF))           # liner: inside flap + inside lid
TY=Y+127
o.append(f'<rect x="{X}" y="{TY}" width="147" height="81" rx="1" fill="#F3E6C4"/>')
o.append(f'<rect x="{X+5}" y="{TY+5}" width="137" height="71" rx="1" fill="#141414"/>')
o.append(f'<rect x="{X+30}" y="{TY+31}" width="88" height="19" rx="9" fill="#060606"/>')
o.append(crop('../device/pita-device-engraving.svg',(17.5,29.5,106,16),X+26,TY+33.3,106*0.88,16*0.88,(160,80),strip=True))
o.append(text('caja abierta',X+73.5,TY+92,4,'semibold',WINE,'middle'))
# ---- closed box (lid + flap visible)
CX,CY=194,30
o.append(shadow(CX,CY,152,81+46*0.35,2))
o.append(crop(BOX,(27,160,152,81),CX,CY,152,81,BOXF))
o.append(f'<rect x="{CX}" y="{CY+81}" width="152" height="7" fill="#5A121C"/>')
o.append(text('caja cerrada',CX+76,CY+81+16+6,4,'semibold',WINE,'middle'))
# ---- pouches (5)
names=['menta','limon','cafe','frutos-rojos','arandano']
PX,PY,pw,ph=194,150,48,56
for i,n in enumerate(names):
    x=PX+i*(pw+3.5)-(0 if i<5 else 0); 
    o.append(shadow(x,PY,pw,ph,5,.18,2))
    o.append(crop(f'../pouches/pouch-{n}-art.svg',(12,16,60,70),x,PY,pw,ph,(160,96)))
o.append(text('5 recargas',PX+(5*pw+4*3.5)/2,PY+ph+9,4,'semibold',WINE,'middle'))
# ---- letter + envelope
LX,LY=194,232
o.append(shadow(LX,LY,162*0.62,114*0.62,1,.2))
o.append(crop('../letter/envelope-front.svg',(3,3,162,114),LX,LY,162*0.62,114*0.62,(168,120)))
o.append(shadow(LX+82,LY-12,105*0.6,148*0.6,1,.2))
o.append(crop('../letter/card-front.svg',(3,3,105,148),LX+82,LY-12,105*0.6,148*0.6,(111,154)))
o.append(text('carta de bienvenida + sobre',LX+72,LY+86,4,'semibold',WINE,'middle'))
# ---- cloth + tweezers + pipe cleaner
KX,KY=24,258
o.append(shadow(KX,KY,60,60,1,.2))
o.append(crop('../cloth/pita-cloth-negro-logo-crema.svg',(0,0,100,100),KX,KY,60,60,(100,100)))
o.append(f'<g transform="translate({KX+72} {KY+6}) rotate(8)"><path d="M0 0 L3 0 L1.6 48 L0.8 48 Z" fill="#141414"/><path d="M6 0 L9 0 L8.2 48 L7.4 48 Z" fill="#141414" transform="rotate(4 4.5 0)"/><rect x="-0.5" y="-1" width="10" height="7" rx="1.5" fill="#141414"/></g>')
o.append(f'<path d="M{KX+100} {KY+8} C{KX+112} {KY+4} {KX+122} {KY+16} {KX+114} {KY+30} C{KX+106} {KY+44} {KX+118} {KY+56} {KX+130} {KY+52}" fill="none" stroke="#2E7D3A" stroke-width="2.6" stroke-linecap="round" stroke-dasharray="0.6 0.5"/>')
o.append(text('paño · pinza · cepillo',KX+73,KY+70,4,'semibold',WINE,'middle'))
o.append(text('pita · el kit completo',24,18,7,'bold',WINE))
W,H=470,345
svg=(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">'
     f'<defs><filter id="sh" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2.2"/></filter></defs>'
     f'<rect width="{W}" height="{H}" fill="#EADFCB"/>{"".join(o)}</svg>')
open('pita-kit-completo.svg','w').write(svg)
open('preview.html','w').write('<html><body style="margin:0"><img src="pita-kit-completo.svg" style="width:2350px;display:block"></body></html>')
js=f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage({{viewport:{{width:2350,height:1725}}}});
await p.goto('file://{HERE}/preview.html');await p.waitForTimeout(800);await p.screenshot({{path:'{HERE}/pita-kit-completo.png'}});
await p.goto('file://{HERE}/pita-kit-completo.svg');await p.waitForTimeout(800);await p.pdf({{path:'{HERE}/pita-kit-completo.pdf',width:'{W}mm',height:'{H}mm',printBackground:true,pageRanges:'1'}});await b.close();}})();"""
open('/tmp/_rk.js','w').write(js); subprocess.run(['node','/tmp/_rk.js'],check=True); os.remove('/tmp/_rk.js'); print('ok')
