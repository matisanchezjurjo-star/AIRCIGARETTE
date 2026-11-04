"""Shared helpers: outlined text (Inter) and the exact traced pita logo, in mm."""
import os, re
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
WINE,CREAM,ORANGE="#6B1621","#F3E6C4","#D9481E"
FONTS={'semibold':'/usr/share/fonts/opentype/inter/Inter-SemiBold.otf','medium':'/usr/share/fonts/opentype/inter/Inter-Medium.otf','bold':'/usr/share/fonts/opentype/inter/Inter-Bold.otf'}
_f={}
def text_width(s,size,font='semibold',track=0.0):
    f=_f.setdefault(font,TTFont(FONTS[font])); cmap=f.getBestCmap(); upm=f['head'].unitsPerEm; hm=f['hmtx']
    w=sum((hm[cmap[ord(c)]][0] if ord(c) in cmap else upm*0.3) for c in s)*size/upm
    return w+track*(len(s)-1)
def text(s,x,y,size,font='semibold',fill=WINE,anchor='start',track=0.0):
    f=_f.setdefault(font,TTFont(FONTS[font])); gs=f.getGlyphSet(); cmap=f.getBestCmap(); upm=f['head'].unitsPerEm
    sc=size/upm; hm=f['hmtx']; tw=text_width(s,size,font,track)
    x0={'start':x,'middle':x-tw/2,'end':x-tw}[anchor]; d=[]; cur=x0
    for ch in s:
        g=cmap.get(ord(ch)); adv=(hm[g][0] if g else upm*0.3)*sc
        if g:
            p=SVGPathPen(gs); gs[g].draw(TransformPen(p,(sc,0,0,-sc,cur,y))); d.append(p.getCommands())
        cur+=adv+track
    return f'<path d="{" ".join(d)}" fill="{fill}"/>'
_src=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'logo','pita-logo-vino.svg')).read()
LX,LY,LW,LH=map(float,re.search(r'viewBox="([^"]+)"',_src).group(1).split())
LOGO_WM,LOGO_DOT=re.findall(r'<path[^>]*d="([^"]+)"',_src)[:2]
def logo_h(w): return LH*w/LW
def logo(x,y,w,fg=WINE,dot=ORANGE,rot=0):
    s=w/LW; h=LH*s
    return (f'<g transform="translate({x} {y}) rotate({rot} {w/2} {h/2}) scale({s:.5f}) translate({-LX} {-LY})">'
            f'<path d="{LOGO_WM}" fill="{fg}" fill-rule="evenodd"/><path d="{LOGO_DOT}" fill="{dot}"/></g>')
