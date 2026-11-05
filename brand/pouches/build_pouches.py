"""pita RECARGAS flavor pouches on the supplier die-line:
三边封刀线 60x70mm (3-side seal pouch, front + back). Units: mm. Text outlined.
Die-line per supplier drawing: 60 x 70 mm, 5 mm seal margin (sides/bottom), zipper band 20-33 mm from the top, open direction = top.
Run: python3 build_pouches.py"""
import os, sys, subprocess
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,os.path.dirname(HERE)); os.chdir(HERE)
from artlib import text, text_width, logo, logo_h, WINE, CREAM, ORANGE
W,H,R,SEAL,Z1,Z2=60,70,6,5,20,33
FLAVORS=[  # key, label, bg, arc(dark), mid, logo/text color
 ('menta','MENTA','#A9BF98','#3F6B45','#6E9468',WINE),
 ('limon','LIMÓN','#F0C341','#E89A1F','#F2AE2E',WINE),
 ('cafe','CAFÉ','#5B3A2A','#3E2619','#4C3022',CREAM),
 ('frutos-rojos','FRUTOS ROJOS','#C8324F','#8E1F35','#A92841',CREAM),
 ('arandano','ARÁNDANO','#5468A8','#2F3B73','#41518D',CREAM)]
CUT='fill="none" stroke="#E6007E" stroke-width="0.25"'; FOLD='fill="none" stroke="#00A0E9" stroke-width="0.2"'
DASH='fill="none" stroke="#00A0E9" stroke-width="0.2" stroke-dasharray="1.2 0.8"'
def outline(x,y): return f'<rect x="{x}" y="{y}" width="{W}" height="{H}" rx="{R}" ry="{R}"/>'
def dieline(x,y):
    return (f'<rect x="{x}" y="{y}" width="{W}" height="{H}" rx="{R}" {CUT}/>'
            f'<path d="M{x+SEAL} {y} V{y+H-SEAL} H{x+W-SEAL} V{y}" {DASH}/><path d="M{x} {y} H{x+W}" {DASH}/>'
            f'<path d="M{x} {y+Z1} H{x+W} M{x} {y+Z2} H{x+W}" {FOLD}/><path d="M{x} {y+(Z1+Z2)/2} H{x+W}" {DASH}/>')
def arcs(x,y,dark,mid,cid,lift=0):
    return (f'<clipPath id="{cid}"><rect x="{x-2}" y="{y-2}" width="{W+4}" height="{H+4}" rx="{R+2}"/></clipPath><g clip-path="url(#{cid})">'
            f'<circle cx="{x+2}" cy="{y+H+8-lift}" r="27" fill="{mid}"/><circle cx="{x+W}" cy="{y+H+10-lift}" r="30" fill="{dark}"/></g>')
def front(x,y,f):
    k,lab,bg,dark,mid,fg=f; o=[]
    o.append(f'<rect x="{x-2}" y="{y-2}" width="{W+4}" height="{H+4}" rx="{R+2}" fill="{bg}"/>')
    o.append(arcs(x,y,dark,mid,'a'+k+str(x)))
    o.append(text('TU RATITO TIENE GUSTO.',x+W/2,y+11,1.9,'semibold',fg,'middle',0.35))
    lw=32; lh=logo_h(lw); ly=y+Z2+2.5
    o.append(logo(x+(W-lw)/2,ly,lw,fg,ORANGE))
    o.append(text('RECARGAS',x+W/2,ly+lh+3.4,2.0,'semibold',fg,'middle',0.55))
    pw=max(30,text_width(lab,2.6,'bold',0.25)+10); py=ly+lh+5.4
    o.append(f'<rect x="{x+(W-pw)/2}" y="{py}" width="{pw}" height="6.6" rx="1.6" fill="{CREAM}"/>')
    o.append(text(lab,x+W/2,py+4.35,2.6,'bold','#3A1418','middle',0.25))
    return ''.join(o)
def back(x,y,f):
    k,lab,bg,dark,mid,fg=f; o=[]
    o.append(f'<rect x="{x-2}" y="{y-2}" width="{W+4}" height="{H+4}" rx="{R+2}" fill="{bg}"/>')
    o.append(text('ABRÍ ACÁ',x+W/2,y+11,2.0,'semibold',fg,'middle',0.5))
    lw=24; lh=logo_h(lw); ly=y+Z2+3
    o.append(logo(x+(W-lw)/2,ly,lw,fg,ORANGE))
    yy=ly+lh+4.6
    o.append(text('RECARGAS · '+lab,x+W/2,yy,2.0,'bold',fg,'middle',0.35)); yy+=3.6
    for s_ in ('Sin nicotina · No ingerir','Mantener fuera del alcance de los niños'):
        o.append(text(s_,x+W/2,yy,1.7,'medium',fg,'middle')); yy+=2.6
    o.append(text('Lote ____',x+W/2,yy+0.4,1.6,'medium',fg,'middle'))
    return ''.join(o)
def page(f,with_dl=True):
    PW,PH=160,96; ax,ay,bx_=12,16,88
    lbl=lambda s,x,y: text(s,x,y,2.4,'semibold','#00A0E9','middle')
    body=front(ax,ay,f)+back(bx_,ay,f)
    if with_dl:
        body+=dieline(ax,ay)+dieline(bx_,ay)+lbl('FRONT 60×70',ax+W/2,ay-5)+lbl('BACK 60×70',bx_+W/2,ay-5)
        body+=text(f'pita RECARGAS · {f[1]} · 3-side seal pouch 60×70 mm · magenta = cut, blue = zipper band 20–33 mm, dashed = 5 mm seal / safe area',12,ay+H+8,2.1,'medium',WINE)
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{PW}mm" height="{PH}mm" viewBox="0 0 {PW} {PH}"><rect width="{PW}" height="{PH}" fill="#fff"/>{body}</svg>'
names=[]
for f in FLAVORS:
    for dl,suf in ((True,'dieline'),(False,'art')):
        n=f'pouch-{f[0]}-{suf}'; open(n+'.svg','w').write(page(f,dl)); names.append(n)
# overview of all 5 fronts
ov=''.join(front(8+i*68,8,f) for i,f in enumerate(FLAVORS))
open('overview-fronts.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" width="348mm" height="86mm" viewBox="0 0 348 86"><rect width="348" height="86" fill="#F7EEDB"/>{ov}</svg>')
js=f"""const {{chromium}}=require('playwright');const {{execSync}}=require('child_process');(async()=>{{const b=await chromium.launch();const p=await b.newPage();
const names={names!r};
for(const n of names){{await p.goto('file://{HERE}/'+n+'.svg');await p.pdf({{path:'{HERE}/'+n+'.pdf',width:'160mm',height:'96mm',printBackground:true,pageRanges:'1'}});}}
await p.setViewportSize({{width:1315,height:325}});await p.goto('file://{HERE}/overview-fronts.svg');await p.screenshot({{path:'{HERE}/overview-fronts.png'}});
await p.setViewportSize({{width:907,height:544}});await p.goto('file://{HERE}/pouch-menta-dieline.svg');await p.screenshot({{path:'{HERE}/preview-menta-front-back.png'}});
await b.close();}})();"""
open('/tmp/_rp.js','w').write(js); subprocess.run(['node','/tmp/_rp.js'],check=True); os.remove('/tmp/_rp.js')
# merge into 2 multi-page PDFs
from pypdf import PdfReader, PdfWriter
for suf in ('dieline','art'):
    w=PdfWriter()
    for f in FLAVORS: w.add_page(PdfReader(f'pouch-{f[0]}-{suf}.pdf').pages[0])
    w.write(f'pita-recargas-pouches-{suf}.pdf')
    for f in FLAVORS: os.remove(f'pouch-{f[0]}-{suf}.pdf')
print('ok')
