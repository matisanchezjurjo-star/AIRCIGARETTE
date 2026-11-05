"""pita welcome letter: A6 card (105x148 mm, 2 sides) + C6 envelope front (162x114 mm).
3 mm bleed, text outlined, exact pita logo. Run: python3 build_letter.py"""
import os, sys, subprocess
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,os.path.dirname(HERE)); os.chdir(HERE)
from artlib import text, text_width, logo, logo_h, WINE, CREAM, ORANGE
B=3; INK='#3A1418'
def page(w,h,body,bg):
    W,H=w+2*B,h+2*B
    marks=''.join(f'<path d="{d}" stroke="#000" stroke-width="0.15"/>' for d in (
        f'M0 {B} H{B-1} M{W} {B} H{W-B+1} M0 {H-B} H{B-1} M{W} {H-B} H{W-B+1}',
        f'M{B} 0 V{B-1} M{W-B} 0 V{B-1} M{B} {H} V{H-B+1} M{W-B} {H} V{H-B+1}'))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">'
            f'<rect width="{W}" height="{H}" fill="{bg}"/><g transform="translate({B} {B})">{body}</g>{marks}</svg>'),W,H
def arcs(cx,cy,r1,r2,clipw,cliph,cid):
    return (f'<clipPath id="{cid}"><rect x="-{B}" y="-{B}" width="{clipw+2*B}" height="{cliph+2*B}"/></clipPath><g clip-path="url(#{cid})">'
            f'<circle cx="{cx}" cy="{cy}" r="{r1}" fill="{WINE}"/><circle cx="{cx-r1*0.55}" cy="{cy+r1*0.25}" r="{r2}" fill="{ORANGE}"/></g>')
CW,CH=105,148
# ---------- FRONT ----------
f=[]
f.append(arcs(CW+8,CH+10,46,30,CW,CH,'af'))
f.append(logo(10,12,34))
f.append(text('Bienvenido',10,52,10.5,'bold',WINE))
f.append(text('a tu ratito',10,63,10.5,'bold',WINE)); f.append(f'<circle cx="{10+text_width("a tu ratito",10.5,"bold")+1.9}" cy="62.0" r="1.3" fill="{ORANGE}"/>')
y=75
for s in ('Gracias por sumarte. pita es tu ratito:','el gesto de siempre, ahora con aire','y sabor. Sin humo. Sin nicotina.','Sin vapor. Sin batería.'):
    f.append(text(s,10,y,3.5,'medium',INK)); y+=5.2
y+=4
f.append(text('CÓMO USAR TU PITA',10,y,2.8,'bold','#C4562E',track=0.5)); y+=6
for n,s in enumerate(('Abrí una recarga y, con la pinza,','colocá el core en el dispositivo.','Cerralo y pitá suave.','Cambiá el core cuando baje el sabor.','Limpiá la boquilla con el paño.')):
    pass
steps=[('1','Con la pinza, colocá un core en tu pita.'),('2','Cerralo y pitá suave.'),('3','Cambiá el core cuando baje el sabor.'),('4','Limpiá la boquilla con el paño.')]
for n,s in steps:
    f.append(f'<circle cx="12.2" cy="{y-1.1}" r="2.2" fill="{WINE}"/>'); f.append(text(n,12.2,y,2.4,'bold',CREAM,'middle'))
    f.append(text(s,17,y,3.1,'medium',INK)); y+=5.6
f.append(text('Tu ratito tiene gusto.',10,CH-12,3.6,'bold',WINE))
f.append(text('@somospita_',10,CH-7,3.0,'semibold','#C4562E'))
front,W,H=page(CW,CH,''.join(f),CREAM)
# ---------- BACK ----------
b=[]
b.append(f'<rect x="-{B}" y="-{B}" width="{CW+2*B}" height="{30+B}" fill="{WINE}"/>')
b.append(text('Tu plan de 30 días',10,14,7.4,'bold',CREAM)); b.append(f'<circle cx="{10+text_width("Tu plan de 30 días",7.4,"bold")+1.4}" cy="13.1" r="0.95" fill="{ORANGE}"/>')
b.append(text('para dejar de fumar, un ratito a la vez',10,22,3.2,'medium',CREAM))
weeks=[('SEMANA 1','Conocé tus ratitos.',['Anotá cuándo fumás: el café, después','de comer, el estrés. Cambiá 1 cigarrillo','por día por un pita.']),
       ('SEMANA 2','Reemplazá los ratitos fáciles.',['El del café y el de después de comer,','siempre con pita.']),
       ('SEMANA 3','Bajá a la mitad.',['Guardá los cigarrillos lejos y llevá','tu pita a todos lados.']),
       ('SEMANA 4','Tu primer día sin cigarrillo.',['Elegí la fecha, contáselo a alguien','y usá pita cuando aparezcan las ganas.'])]
y=40
for k,t,ls in weeks:
    b.append(f'<rect x="10" y="{y-3.6}" width="4.2" height="4.2" rx="0.8" fill="none" stroke="{WINE}" stroke-width="0.45"/>')
    b.append(text(k,17,y,2.5,'bold','#C4562E',track=0.4)); b.append(text(t,36,y,3.3,'bold',WINE)); y+=4.8
    for s in ls: b.append(text(s,17,y,2.85,'medium',INK)); y+=4.0
    y+=3.2
b.append(text('MARCÁ CADA DÍA',10,y+1,2.5,'bold','#C4562E',track=0.4)); y+=5
for i in range(30):
    r,c=divmod(i,10); cx=12.5+c*8.8; cy=y+r*7.2
    b.append(f'<circle cx="{cx}" cy="{cy}" r="2.7" fill="none" stroke="{WINE}" stroke-width="0.4"/>')
    b.append(text(str(i+1),cx,cy+0.85,2.1,'semibold',WINE,'middle'))
y+=3*7.2+2.5
for s in ('pita no es un medicamento ni un tratamiento. Si querés ayuda','para dejar de fumar, consultá a tu médico o llamá gratis a la','Línea Nacional para Dejar de Fumar: 0800-999-3040.'):
    b.append(text(s,10,y,2.3,'medium','#7A5A50')); y+=3.3
b.append(f'<circle cx="{CW-12}" cy="{CH-10}" r="3" fill="{ORANGE}"/>')
back,_,_=page(CW,CH,''.join(b),CREAM)
# ---------- ENVELOPE (C6, front) ----------
EW,EH=162,114; e=[]
lw=60; e.append(logo((EW-lw)/2,(EH-logo_h(lw))/2-6,lw,CREAM,ORANGE))
e.append(text('TU RATITO TIENE GUSTO.',EW/2,EH/2+logo_h(lw)/2+6,3.4,'semibold',CREAM,'middle',0.8))
env,EWb,EHb=page(EW,EH,''.join(e),WINE)
for n,s in (('card-front',front),('card-back',back),('envelope-front',env)): open(n+'.svg','w').write(s)
js=f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();
const pages=[['card-front','{W}mm','{H}mm'],['card-back','{W}mm','{H}mm'],['envelope-front','{EWb}mm','{EHb}mm']];
for(const [n,w,h] of pages){{await p.goto('file://{HERE}/'+n+'.svg');await p.pdf({{path:'{HERE}/'+n+'.pdf',width:w,height:h,printBackground:true,pageRanges:'1'}});}}
await p.setViewportSize({{width:1700,height:700}});await p.goto('file://{HERE}/preview.html');await p.screenshot({{path:'{HERE}/preview.png'}});await b.close();}})();"""
open('preview.html','w').write('<html><body style="margin:0;background:#e9e4da;display:flex;gap:30px;align-items:center;justify-content:center;height:700px">'
  '<img src="card-front.svg" style="height:600px;box-shadow:0 6px 20px #0003"><img src="card-back.svg" style="height:600px;box-shadow:0 6px 20px #0003">'
  '<img src="envelope-front.svg" style="width:640px;box-shadow:0 6px 20px #0003"></body></html>')
open('/tmp/_rl.js','w').write(js); subprocess.run(['node','/tmp/_rl.js'],check=True); os.remove('/tmp/_rl.js')
from pypdf import PdfReader, PdfWriter
w=PdfWriter()
for n in ('card-front','card-back'): w.add_page(PdfReader(n+'.pdf').pages[0])
w.write('pita-carta-bienvenida-A6.pdf')
os.replace('envelope-front.pdf','pita-sobre-C6.pdf'); os.remove('card-front.pdf'); os.remove('card-back.pdf')
print('ok')
