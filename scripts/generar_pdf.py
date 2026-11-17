"""Genera el PDF desde el HTML editable sin necesitar un navegador."""
from pathlib import Path
import argparse, base64, re, json
import pymupdf as fitz
from html import unescape
from html.parser import HTMLParser

class Node(dict):
    def __init__(self, attrs=()):
        super().__init__(attrs); self.text=""; self.children=[]
    def select(self, name):
        return [x for x in self.children if name.lstrip(".") in x.get("class", "").split()]
    def select_one(self, name):
        return self.select(name)[0]
    def get_text(self):
        return self.text

class ManualParser(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True); self.pages=[];self.page=None;self.span=None;self.feed(text)
    def handle_starttag(self, tag, attrs):
        n=Node(attrs)
        if tag=="section": self.page=n;self.pages.append(n)
        elif self.page is not None and tag=="img": self.page.children.append(n)
        elif self.page is not None and tag=="span": self.span=n;self.page.children.append(n)
        elif self.span is not None and tag=="br": self.span.text+="\n"
    def handle_endtag(self,tag):
        if tag=="section": self.page=None
        elif tag=="span": self.span=None
    def handle_data(self,text):
        if self.span is not None: self.span.text+=text
    def select(self, name): return self.pages

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--input', type=Path, default=Path(__file__).resolve().parents[1] / 'docs/Manual_de_instalacion_Yooz2SageNG_v1.2.html')
parser.add_argument('--output', type=Path, default=Path('dist/Manual_de_instalacion_Yooz2SageNG_v1.2.pdf'))
args = parser.parse_args()
source=args.input.read_text(encoding='utf-8')
soup=ManualParser(source)
fonts = {name: base64.b64decode(data) for name,data in re.findall(r'@font-face\{font-family:([^;]+);src:url\(data:font/ttf;base64,([^)]*)\)', source)}
def prop(style, key):
    return re.search(r'(?:^|;)'+re.escape(key)+r':([^;]+)', style).group(1)
doc = fitz.open()
for section in soup.select('section.page'):
    style=section['style']
    w,h=float(prop(style,'width')[:-2]),float(prop(style,'height')[:-2])
    page=doc.new_page(width=w,height=h)
    background=base64.b64decode(section.select_one('.background')['src'].split(',',1)[1])
    page.insert_image(page.rect,stream=background)
    for span in section.select('.text'):
        style=span['style']; x=float(prop(style,'left')[:-2]); y=float(span['data-baseline'])
        size=float(span['data-size']); family=prop(style,'font').split('pt ',1)[1]
        color=prop(style,'color').lstrip('#'); rgb=tuple(int(color[i:i+2],16)/255 for i in (0,2,4))
        if family in fonts:
            page.insert_font(fontname=family,fontbuffer=fonts[family])
            fontname=family
        else: fontname='symb' if family=='serif' else 'helv'
        text=span.get_text().replace('\uf0f0','⇒').replace('\uf0b7','•')
        page.insert_text((x,y),text,fontname=fontname,fontsize=size,color=rgb)
    for link in json.loads(section.get('data-links','[]')):
        page.insert_link({'kind':fitz.LINK_URI,'from':fitz.Rect(link['from']),'uri':link['uri']})
args.output.parent.mkdir(parents=True,exist_ok=True)
doc.save(args.output,garbage=4,deflate=True)
print(args.output)
