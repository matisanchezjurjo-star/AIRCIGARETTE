"""pita gift box artwork on the F1 die-line (book box 81 x 152 x 48 mm).
Die-line RECONSTRUCTED from a screenshot of the supplier's template 'F1 box 81x152x48mm-out.pdf':
final placement must be checked on the supplier's original file.
All units in mm. Text is converted to outlines. Run: python3 build_box.py"""
import os, re, subprocess
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
HERE=os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
WINE,CREAM,ORANGE,TERRA="#6B1621","#F3E6C4","#D9481E","#C4562E"
FONTS={'semibold':'/usr/share/fonts/opentype/inter/Inter-SemiBold.otf','medium':'/usr/share/fonts/opentype/inter/Inter-Medium.otf','bold':'/usr/share/fonts/opentype/inter/Inter-Bold.otf'}
_f={}
def text(s,x,y,size,font='semibold',fill=WINE,anchor='start',track=0.0):
    """Text as outlined path. size = cap-height-ish em size in mm. y = baseline."""
    f=_f.setdefault(font,TTFont(FONTS[font])); gs=f.getGlyphSet(); cmap=f.getBestCmap(); upm=f['head'].unitsPerEm
    sc=size/upm; hm=f['hmtx']; total=0; glyphs=[]
    for ch in s:
        g=cmap.get(ord(ch)); adv=hm[g][0] if g else upm*0.3
        glyphs.append((g,total)); total+=adv+track/sc
    total-=track/sc
    x0={'start':x,'middle':x-total*sc/2,'end':x-total*sc}[anchor]
    pen=SVGPathPen(gs); d=[]
    for g,off in glyphs:
        if not g: continue
        p=SVGPathPen(gs); tp=TransformPen(p,(sc,0,0,-sc,x0+off*sc,y)); gs[g].draw(tp); d.append(p.getCommands())
    return f'<path d="{" ".join(d)}" fill="{fill}"/>'
# --- logo (exact traced client logo) ---
src=open('../logo/pita-logo-vino.svg').read()
LX,LY,LW,LH=map(float,re.search(r'viewBox="([^"]+)"',src).group(1).split())
_p=re.findall(r'<path[^>]*d="([^"]+)"',src); LOGO_WM,LOGO_DOT=_p[0],_p[1]
def logo(x,y,w,fg=WINE,dot=ORANGE,rot=0):
    s=w/LW; h=LH*s
    t=f'translate({x} {y}) rotate({rot} {w/2} {h/2}) scale({s:.5f}) translate({-LX} {-LY})'
    return f'<g transform="{t}"><path d="{LOGO_WM}" fill="{fg}" fill-rule="evenodd"/><path d="{LOGO_DOT}" fill="{dot}"/></g>'
def logo_h(w): return LH*w/LW
CUT='fill="none" stroke="#E6007E" stroke-width="0.3"'
FOLD='fill="none" stroke="#00A0E9" stroke-width="0.3" stroke-dasharray="2 1.2"'
def lbl(s,x,y,anchor='middle'): return text(s,x,y,2.4,'medium','#00A0E9',anchor)
out=[]; dl=[]
# ============ 1) COVER WRAP (outer) ============
CX,CY=10,14; T=17            # turn-in
W=152; P=[81,48,81,46]       # back, spine, lid, flap
Ytop=[0,81,129,210]; H=sum(P)
ox,oy=CX,CY; bx,by=ox+T,oy+T  # board area origin
ow,oh=W+2*T,H+2*T; c=T     # chamfer
oct=f'M{ox+c} {oy} H{ox+ow-c} L{ox+ow} {oy+c} V{oy+oh-c} L{ox+ow-c} {oy+oh} H{ox+c} L{ox} {oy+oh-c} V{oy+c} Z'
out.append(f'<clipPath id="cw"><path d="{oct}"/></clipPath><g clip-path="url(#cw)">')
out.append(f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="{WINE}"/>')
# back panel (cream) incl. top turn-in
out.append(f'<rect x="{ox}" y="{oy}" width="{ow}" height="{T+P[0]}" fill="{CREAM}"/>')
# lid panel (cream) incl. side turn-ins
ly=by+Ytop[2]
out.append(f'<rect x="{ox}" y="{ly}" width="{ow}" height="{P[2]}" fill="{CREAM}"/>')
# lid arcs bottom-right
out.append(f'<clipPath id="lidc"><rect x="{ox}" y="{ly}" width="{ow}" height="{P[2]}"/></clipPath><g clip-path="url(#lidc)">'
           f'<circle cx="{bx+W+6}" cy="{ly+P[2]+12}" r="52" fill="{WINE}"/><circle cx="{bx+W-30}" cy="{ly+P[2]+18}" r="36" fill="{ORANGE}"/></g>')
lw=92; out.append(logo(bx+10,ly+12,lw))
out.append(text('Inhalador de madera con sabor',bx+12,ly+12+logo_h(lw)+9,4.6,'semibold',WINE))
# flap (wine) logo cream left
fy=by+Ytop[3]; fw=44; out.append(logo(bx+12,fy+(P[3]-logo_h(fw))/2,fw,CREAM,ORANGE))
out.append(text('TU RATITO TIENE GUSTO.',bx+W-10,fy+P[3]/2+1.6,3.2,'semibold',CREAM,'end',0.6))
# spine (wine) centered logo, rotated 180 (reads upright when box is closed, spine at the back)
sy=by+Ytop[1]; sw=40; out.append(logo(bx+(W-sw)/2,sy+(P[1]-logo_h(sw))/2,sw,CREAM,ORANGE,180))
# back panel content, rotated 180
bk=[]; B0=by  # content area by..by+81
bk.append(logo(bx+10,B0+9,34))
lines=[('Inhalador de madera con sabor','semibold',4.0,WINE),
       ('Sin humo · Sin nicotina · Sin vapor · Sin batería','medium',3.0,WINE),
       ('Contenido: 1 inhalador de madera · 5 recargas de sabor (Menta, Limón, Café,','medium',2.5,WINE),
       ('Frutos Rojos, Arándano) · paño de limpieza · pinza · carta de bienvenida','medium',2.5,WINE),
       ('Importado por: [RAZÓN SOCIAL] · CUIT [XX-XXXXXXXX-X] · [DIRECCIÓN], Argentina','medium',2.3,WINE),
       ('Origen: China · Instagram @[usuario] · [web]','medium',2.3,WINE)]
yy=B0+34
for s,fnt,sz,col in lines: bk.append(text(s,bx+10,yy,sz,fnt,col)); yy+=sz*1.9
bk.append(f'<rect x="{bx+W-44}" y="{B0+50}" width="34" height="20" fill="#fff" stroke="{WINE}" stroke-width="0.3"/>')
bk.append(text('CÓDIGO DE BARRAS',bx+W-27,B0+61.5,2.0,'semibold',WINE,'middle'))
bk.append(f'<circle cx="{bx+W-14}" cy="{B0+14}" r="5" fill="{ORANGE}"/>')
out.append(f'<g transform="rotate(180 {bx+W/2} {B0+P[0]/2})">'+''.join(bk)+'</g>')
out.append('</g>')
dl.append(f'<path d="{oct}" {CUT}/>')
for yv in [by, by+H]: dl.append(f'<path d="M{bx} {yv} H{bx+W}" {FOLD}/>')
for xv in [bx,bx+W]: dl.append(f'<path d="M{xv} {by} V{by+H}" {FOLD}/>')
for yv in Ytop[1:]: dl.append(f'<path d="M{bx} {by+yv} H{bx+W}" {FOLD}/>')
names=['BACK / BASE 152×81','SPINE 152×48','LID (FRONT) 152×81','MAGNETIC FLAP 152×46']
for n,yv,h in zip(names,Ytop,P): dl.append(lbl(n,bx+W/2,by+yv+h-2.5))
dl.append(lbl('1 · COVER WRAP (outside)',ox+ow/2,oy-4))
# ============ 2) TRAY WRAP ============
TX,TY=215,14; TW,TD,TH,TT=148,76,43,18
tbx,tby=TX+TH+TT,TY+TH+TT
shape=(f'M{tbx} {TY} H{tbx+TW} V{tby} H{tbx+TW+TH+TT} V{tby+TD} H{tbx+TW} V{tby+TD+TH+TT} H{tbx} V{tby+TD} H{TX} V{tby} H{tbx} Z')
out.append(f'<path d="{shape}" fill="{CREAM}"/>')
for yy0,yy1 in ((tby-TH,tby),(tby+TD,tby+TD+TH)):  # side glue tabs on long walls
    for xx,sgn in ((tbx,-1),(tbx+TW,1)):
        tab=f'M{xx} {yy0+2} L{xx+sgn*10} {yy0+6} V{yy1-6} L{xx} {yy1-2} Z'
        out.append(f'<path d="{tab}" fill="{CREAM}"/>'); dl.append(f'<path d="{tab}" {CUT}/>')
out.append(f'<circle cx="{tbx+TW/2}" cy="{tby-TH/2}" r="3.2" fill="{ORANGE}"/>')
dl.append(f'<path d="{shape}" {CUT}/>')
dl.append(f'<rect x="{tbx}" y="{tby}" width="{TW}" height="{TD}" {FOLD}/>')
for yv in (tby-TH,tby+TD+TH): dl.append(f'<path d="M{tbx} {yv} H{tbx+TW}" {FOLD}/>')
for xv in (tbx-TH,tbx+TW+TH): dl.append(f'<path d="M{xv} {tby} V{tby+TD}" {FOLD}/>')
dl.append(lbl('TRAY BASE 148×76 (under foam)',tbx+TW/2,tby+TD/2))
dl.append(lbl('2 · TRAY WRAP',TX+(TW+2*(TH+TT))/2,TY-4))
# ============ 3) LID LINER (inside) ============
LXo,LYo,LWd=215,232,147; LP=[45,81,20]
lsh=f'M{LXo} {LYo} H{LXo+LWd} V{LYo+LP[0]+LP[1]} L{LXo+LWd-3} {LYo+sum(LP)} H{LXo+3} L{LXo} {LYo+LP[0]+LP[1]} Z'
out.append(f'<clipPath id="lc"><path d="{lsh}"/></clipPath><g clip-path="url(#lc)"><path d="{lsh}" fill="{CREAM}"/>')
iy=LYo+LP[0]
out.append(f'<clipPath id="lidin"><rect x="{LXo}" y="{iy}" width="{LWd}" height="{LP[1]}"/></clipPath><g clip-path="url(#lidin)"><circle cx="{LXo-4}" cy="{iy-4}" r="36" fill="{WINE}"/><circle cx="{LXo-6}" cy="{iy-6}" r="22" fill="{ORANGE}"/></g>')
out.append(text('Bienvenido al ratito.',LXo+LWd-10,LYo+LP[0]/2+2,4.4,'semibold',WINE,'end'))
lw2=46; out.append(logo(LXo+(LWd-lw2)/2,iy+(LP[1]-logo_h(lw2))/2,lw2))
out.append('</g>')
dl.append(f'<path d="{lsh}" {CUT}/>')
for yv in (LYo+LP[0],LYo+LP[0]+LP[1]): dl.append(f'<path d="M{LXo} {yv} H{LXo+LWd}" {FOLD}/>')
for n,y0,h in zip(['INSIDE FLAP 147×45','INSIDE LID 147×81','SPINE 20'],[0,LP[0],LP[0]+LP[1]],LP): dl.append(lbl(n,LXo+LWd/2,LYo+y0+h-2))
dl.append(lbl('3 · LID LINER (inside, seen when the box is open)',LXo+LWd/2,LYo-4))
# legend
leg=[text('pita · F1 gift box 81 × 152 × 48 mm · artwork v1',10,388,4,'bold',WINE),
     text('Magenta = cut · Blue dashed = fold · Turn-in 17 mm (cover), 18 mm (tray). Die-line reconstructed from a screenshot: place the artwork on the original supplier file before printing.',10,394,2.6,'medium',WINE),
     text('Colors: Wine #6B1621 (≈C0 M79 Y69 K58) · Cream #F3E6C4 (≈C0 M5 Y19 K5) · Orange #D9481E (≈C0 M67 Y86 K15) · Please match to Pantone and send a printed proof. Matte / soft-touch finish.',10,399,2.6,'medium',WINE)]
CW,CH=500,405
def svg(with_dl=True):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{CW}mm" height="{CH}mm" viewBox="0 0 {CW} {CH}">'
            f'<rect width="{CW}" height="{CH}" fill="#fff"/><g id="artwork">{"".join(out)}</g>'
            + (f'<g id="dieline">{"".join(dl)}</g>' if with_dl else '') + f'<g id="legend">{"".join(leg)}</g></svg>')
open('pita-box-artwork-with-dieline.svg','w').write(svg(True))
open('pita-box-artwork-only.svg','w').write(svg(False))
js=f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();
for (const n of ['pita-box-artwork-with-dieline','pita-box-artwork-only']){{
 await p.goto('file://{HERE}/'+n+'.svg');
 await p.pdf({{path:'{HERE}/'+n+'.pdf',width:'{CW}mm',height:'{CH}mm',printBackground:true,pageRanges:'1'}});}}
await p.setViewportSize({{width:1890,height:1531}});await p.goto('file://{HERE}/pita-box-artwork-with-dieline.svg');
await p.screenshot({{path:'{HERE}/preview.png'}});await b.close();}})();"""
open('/tmp/_render_box.js','w').write(js); subprocess.run(['node','/tmp/_render_box.js'],check=True); os.remove('/tmp/_render_box.js')
print('ok')
