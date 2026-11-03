"""Build the supplier PDFs and the ZIP.  Run: python3 build.py
Put the kit photo at kit-contents.jpg (optional) and it is added to the 'What's inside' slide."""
import os, re, subprocess, shutil, zipfile
from pypdf import PdfReader, PdfWriter
os.chdir(os.path.dirname(os.path.abspath(__file__)))
def render(src_html, html_text, pdf):
    tmp='_tmp_'+src_html; open(tmp,'w').write(html_text)
    subprocess.run(['node','render.js',tmp,pdf],check=True); os.remove(tmp)
def number(s,start,label):
    n=[start-1]
    def f(m): n[0]+=1; return f'<div class="foot"><span>{label}</span><span>{n[0]}</span></div>'
    return re.sub(r'<div class="foot"><span>[^<]*</span><span>[^<]*</span></div>',f,s)
kit=os.path.exists('kit-contents.jpg')
photo='<img class="photo" src="kit-contents.jpg" style="margin-bottom:3mm"><p class="note">Visual reference (concept mock-up).</p>' if kit else ''
base=open('index.html').read().replace('<!--KITPHOTO-->',photo)
# 1) standalone branding proposal (cover + 6 pages)
prop=number(base,1,'PITA · BRANDING PROPOSAL')
prop=prop.replace('as in the photo on page 2','as in the photo on page 2').replace('(see page 3)','(see page 3)')
render('index.html',prop,'pita-branding-proposal.pdf')
# 2) quote request (3 pages)
render('quote-request.html',open('quote-request.html').read(),'pita-quote-request.pdf')
# 3) brand-guide section for the order pack (pages 4..8)
bg=number(base,4,'PITA · BRAND GUIDE').replace('<div class="kicker">01 / The brand</div>','<div class="kicker">Brand guide · 01 / The brand</div>')
bg=bg.replace('as in the photo on page 2','as in the photo on page 5').replace('(see page 3)','(see page 6)').replace('the gift box on page 2 is the one','the gift box on page 5 is the one')
render('index.html',bg,'_bg.pdf')
w=PdfWriter()
for p in PdfReader('pita-quote-request.pdf').pages: w.add_page(p)
r=PdfReader('_bg.pdf')
for i in range(1,len(r.pages)-1): w.add_page(r.pages[i])   # skip cover and order page
w.add_metadata({'/Title':'pita – Quote request, branding confirmation & brand guide'})
w.write('pita-order-pack.pdf'); os.remove('_bg.pdf')
# 4) zip
z=zipfile.ZipFile('pita-order-pack.zip','w',zipfile.ZIP_DEFLATED)
z.write('pita-order-pack.pdf','pita-order-pack/pita-order-pack.pdf')
z.write('gift-box.jpg','pita-order-pack/photos/01-gift-box.jpg'); z.write('flavors.jpg','pita-order-pack/photos/02-flavor-refills.jpg')
if kit: z.write('kit-contents.jpg','pita-order-pack/photos/03-kit-contents.jpg')
for a,b in (('pita-logo-vino.svg','pita-logo-wine.svg'),('pita-logo-crema.svg','pita-logo-cream.svg'),('pita-grabado-mono.svg','pita-engraving-1color.svg')):
    z.write('../logo/'+a,'pita-order-pack/logo/'+b)
z.writestr('pita-order-pack/README.txt',f"""pita - Order pack for Guangzhou Tropical Rainforest Industrial Co., Ltd. (Attn: Suki Li)

pita-order-pack.pdf
  p.1    Our first order + design photos
  p.2    Price breakdown (please complete)
  p.3    Branding confirmation before payment (please confirm each point)
  p.4-{len(w.pages)}  pita brand guide: brand, colors, gift box, what's inside, device, flavor refills

photos/  Design reference photos (mock-ups)
logo/    Logo files (SVG, filled shapes). pita-engraving-1color.svg = laser engraving on the wood.
""")
z.close(); print('pages:',len(w.pages),'kit photo:',kit)
