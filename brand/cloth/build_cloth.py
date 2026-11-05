"""pita cleaning cloth: bordo (wine) microfiber 100x100 mm, cream pita logo (1 color). Run: python3 build_cloth.py"""
import os, sys, subprocess
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,os.path.dirname(HERE)); os.chdir(HERE)
from artlib import text, logo, logo_h, CREAM, ORANGE
S=100; BLACK='#6B1621'
def cloth(variant):
    if variant=='corner':
        lw=22; body=logo(S-lw-8,S-logo_h(lw)-8,lw,CREAM,CREAM)
    else:
        lw=46; body=logo((S-lw)/2,(S-logo_h(lw))/2,lw,CREAM,CREAM)
    edge=f'<rect x="1.5" y="1.5" width="{S-3}" height="{S-3}" fill="none" stroke="#4E0F18" stroke-width="0.6" stroke-dasharray="1.2 0.6"/>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{S}mm" height="{S}mm" viewBox="0 0 {S} {S}"><rect width="{S}" height="{S}" fill="{BLACK}"/>{edge}{body}</svg>'
for v in ('corner',): open(f'pita-cloth-{v}.svg','w').write(cloth(v))
open('preview.html','w').write('<html><body style="margin:0;background:#e9e4da;display:flex;align-items:center;justify-content:center;height:560px;font-family:Inter;color:#3A1418"><div style="text-align:center"><img src="pita-cloth-corner.svg" style="width:420px;box-shadow:0 8px 24px #0004"><div style="margin-top:12px">pita · paño de limpieza 10 × 10 cm</div></div></body></html>')
js=f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();
for(const v of ['corner']){{await p.goto('file://{HERE}/pita-cloth-'+v+'.svg');await p.pdf({{path:'{HERE}/pita-cloth-'+v+'.pdf',width:'{S}mm',height:'{S}mm',printBackground:true,pageRanges:'1'}});}}
await p.setViewportSize({{width:700,height:560}});await p.goto('file://{HERE}/preview.html');await p.screenshot({{path:'{HERE}/preview.png'}});await b.close();}})();"""
open('/tmp/_rc.js','w').write(js); subprocess.run(['node','/tmp/_rc.js'],check=True); os.remove('/tmp/_rc.js'); print('ok')
