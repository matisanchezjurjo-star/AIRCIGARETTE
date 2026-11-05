"""pita cleaning cloth 100x100 mm, small logo bottom-right (about 22 mm). 3 color options. Run: python3 build_cloth.py"""
import os, sys, subprocess
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,os.path.dirname(HERE)); os.chdir(HERE)
from artlib import logo, logo_h, WINE, CREAM
S=100; BLACK='#111111'
VARIANTS=[  # name, cloth, logo, dot, stitch, caption
 ('negro-logo-crema',BLACK,CREAM,CREAM,'#2a2a2a','FINAL · Negro, logo crema'),
 ('bordo-logo-crema',WINE,CREAM,CREAM,'#4E0F18','A · Bordó, logo crema'),
 ('negro-logo-bordo',BLACK,WINE,WINE,'#2a2a2a','B · Negro, logo bordó entero'),
 ('negro-logo-bordo-punto-crema',BLACK,WINE,CREAM,'#2a2a2a','C · Negro, logo bordó + punto crema')]
def cloth(bg,fg,dot,st):
    lw=22; body=logo(S-lw-8,S-logo_h(lw)-8,lw,fg,dot)
    edge=f'<rect x="1.5" y="1.5" width="{S-3}" height="{S-3}" fill="none" stroke="{st}" stroke-width="0.6" stroke-dasharray="1.2 0.6"/>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{S}mm" height="{S}mm" viewBox="0 0 {S} {S}"><rect width="{S}" height="{S}" fill="{bg}"/>{edge}{body}</svg>'
for n,bg,fg,dot,st,_ in VARIANTS: open(f'pita-cloth-{n}.svg','w').write(cloth(bg,fg,dot,st))
cards=''.join(f'<div style="text-align:center"><img src="pita-cloth-{n}.svg" style="width:360px;box-shadow:0 8px 24px #0004"><div style="margin-top:12px">{c}</div></div>' for n,*_,c in VARIANTS)
open('preview.html','w').write(f'<html><body style="margin:0;background:#e9e4da;display:flex;gap:40px;align-items:center;justify-content:center;height:500px;font-family:Inter;color:#3A1418">{cards}</body></html>')
names=[v[0] for v in VARIANTS]
js=f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();
for(const v of {names!r}){{await p.goto('file://{HERE}/pita-cloth-'+v+'.svg');await p.pdf({{path:'{HERE}/pita-cloth-'+v+'.pdf',width:'{S}mm',height:'{S}mm',printBackground:true,pageRanges:'1'}});}}
await p.setViewportSize({{width:1700,height:500}});await p.goto('file://{HERE}/preview.html');await p.screenshot({{path:'{HERE}/preview.png'}});await b.close();}})();"""
open('/tmp/_rc.js','w').write(js); subprocess.run(['node','/tmp/_rc.js'],check=True); os.remove('/tmp/_rc.js'); print('ok')
