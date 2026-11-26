"""Genera catalogo-anaya.pdf desde los mismos datos que la página.

Requiere reportlab y Pillow. Ejecutar desde la raíz: python3 tools/generar_pdf.py
"""
from pathlib import Path
import json
import runpy
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.utils import ImageReader

ROOT = Path(__file__).resolve().parent.parent
site = runpy.run_path(str(ROOT / 'tools/generar.py'))
data = json.loads((ROOT / 'datos/catalogo.json').read_text(encoding='utf-8'))
FONT_DIR = Path('/System/Library/Fonts/Supplemental')
pdfmetrics.registerFont(TTFont('AnayaSans', str(FONT_DIR / 'Arial.ttf')))
pdfmetrics.registerFont(TTFont('AnayaSansBold', str(FONT_DIR / 'Arial Bold.ttf')))
pdfmetrics.registerFont(TTFont('AnayaSerif', str(FONT_DIR / 'Georgia.ttf')))
INK = colors.HexColor('#2c2521')
MUTED = colors.HexColor('#655950')
GOLD = colors.HexColor('#9a7126')
PAPER = colors.HexColor('#faf8f3')
LINE = colors.HexColor('#e7d9c4')
SAND = colors.HexColor('#f6ecdf')
OUT = ROOT / 'catalogo-anaya.pdf'
c = canvas.Canvas(str(OUT), pagesize=A4, pageCompression=1)
c.setTitle('Anaya Co. - Catálogo de productos')
c.setAuthor('Anaya Co.')

def paragraph(text, x, top, width, size=10, leading=15, font='AnayaSans', color=INK):
    style = ParagraphStyle('p', fontName=font, fontSize=size, leading=leading, textColor=color, spaceAfter=0)
    p = Paragraph(escape(str(text)), style)
    _, h = p.wrap(width, 1000)
    p.drawOn(c, x, top-h)
    return h

def background(w,h, num):
    c.setFillColor(PAPER); c.rect(0,0,w,h,fill=1,stroke=0)
    c.setStrokeColor(LINE); c.line(36,34,w-36,34)
    c.setFont('AnayaSans',8); c.setFillColor(MUTED)
    c.drawString(36,20,'ANAYA CO.  |  Cosmética botánica artesanal')
    c.drawRightString(w-36,20,str(num))

def photo(path, x, y, w, h):
    im=ImageReader(str(path)); iw,ih=im.getSize(); ratio=min(w/iw,h/ih)
    dw,dh=iw*ratio,ih*ratio
    c.drawImage(im,x+(w-dw)/2,y+(h-dh)/2,dw,dh,mask='auto')

def money(v): return '$' + f'{v:.2f}'.replace('.',',')

# Portada y propósito
w,h=A4; background(w,h,1)
photo(ROOT/'img/marca/logo-completo.png',w/2-75,h-190,150,145)
c.setFillColor(GOLD); c.setFont('AnayaSansBold',9); c.drawCentredString(w/2,h-222,'BELLEZA  ·  BIENESTAR  ·  CUIDADO')
c.setFillColor(INK); c.setFont('AnayaSerif',25); c.drawCentredString(w/2,h-258,'Catálogo de productos')
c.setFillColor(MUTED); c.setFont('AnayaSans',10); c.drawCentredString(w/2,h-279,'Cosmética botánica artesanal elaborada en Ecuador')
c.setStrokeColor(LINE);c.line(55,h-301,w-55,h-301)
top=h-325
for _,title,body in site['ESSENCE']:
    c.setFillColor(GOLD);c.setFont('AnayaSerif',15);c.drawString(55,top,title)
    used=paragraph(body,55,top-10,w-110,10,15,color=MUTED)
    top-=used+46
c.setFillColor(GOLD);c.setFont('AnayaSansBold',10);c.drawString(55,top-3,'WhatsApp  +593 96 316 0557')
c.showPage()

# Tabla de precios para clientes.
w,h=A4; c.setPageSize(A4); background(w,h,2)
c.setFillColor(GOLD); c.setFont('AnayaSansBold',9); c.drawString(36,h-46,'CATÁLOGO  ·  PRECIOS EN USD')
c.setFillColor(INK); c.setFont('AnayaSerif',22); c.drawString(36,h-76,'Productos y precios')
c.setFillColor(MUTED); c.setFont('AnayaSans',9); c.drawString(36,h-97,'Disponibilidad, pago y envío se confirman por WhatsApp.')
x=36; y=h-122; rowh=29; width=w-72
c.setFillColor(colors.HexColor('#eee3d2')); c.rect(x,y-25,width,25,fill=1,stroke=0)
c.setFillColor(INK); c.setFont('AnayaSansBold',9); c.drawString(x+9,y-17,'Producto'); c.drawRightString(x+width-9,y-17,'Precio')
y-=25
for idx,p in enumerate(data['productos']):
    if idx%2==0:
        c.setFillColor(colors.HexColor('#f4eee5')); c.rect(x,y-rowh,width,rowh,fill=1,stroke=0)
    c.setFillColor(INK); c.setFont('AnayaSans',9.5); c.drawString(x+9,y-19,p['nombre'])
    c.setFont('AnayaSansBold',9.5); c.drawRightString(x+width-9,y-19,money(p['precio']))
    y-=rowh
c.setFillColor(MUTED); c.setFont('AnayaSans',8); c.drawString(36,y-19,'Precios en dólares estadounidenses. El envío se cotiza por separado.')
c.drawString(36,y-32,'Algunas imágenes fueron mejoradas con IA; consulta la etiqueta posterior cuando esté disponible.')
c.showPage()

# Una ficha por producto, con las vistas disponibles y las indicaciones verificables.
w,h=A4
for index,p in enumerate(data['productos']):
    background(w,h,index+3)
    c.setFillColor(GOLD);c.setFont('AnayaSansBold',9);c.drawString(36,h-43,p['categoria'].upper())
    title_height=paragraph(p['nombre'],36,h-54,w-72,21,25,'AnayaSerif')
    c.setFillColor(INK);c.setFont('AnayaSerif',15);c.drawRightString(w-36,h-45,money(p['precio']))
    photos=p['fotos']
    count=min(len(photos),3)
    gap=10; x0=36; image_top=h-108; image_h=195
    image_w=(w-72-gap*(count-1))/count
    for i,f in enumerate(photos[:3]):
        x=x0+i*(image_w+gap)
        c.setFillColor(SAND);c.roundRect(x,image_top-image_h,image_w,image_h,5,fill=1,stroke=0)
        photo(ROOT/'img/productos'/f"{f['slug']}-480.jpg",x,image_top-image_h,image_w,image_h)
        c.setFillColor(MUTED);c.setFont('AnayaSans',8);c.drawString(x+3,image_top-image_h-13,f['etiqueta'])
    top=image_top-image_h-40
    def section(title, lines):
        global top
        c.setFillColor(GOLD);c.setFont('AnayaSansBold',9);c.drawString(36,top,title.upper())
        top-=9
        for line in lines:
            used=paragraph(line,36,top,w-72,9.5,13,color=MUTED)
            top-=used+5
        top-=12
    section('Ingredientes', [p['ingredientes']])
    if p.get('uso'): section('Modo de uso',p['uso'])
    if p.get('precauciones'): section('Precauciones',p['precauciones'])
    if not p.get('uso') or not p.get('precauciones'):
        section('Información por confirmar',['Las indicaciones que faltan no se distinguen o no figuran en las fotografías disponibles. Consulta la etiqueta o contacta a Anaya Co.'])
    if len(photos)==1:
        section('Fotografías',['No se dispone de una imagen posterior para este producto.'])
    if any('referencial' in f['slug'] for f in photos):
        section('Imagen referencial',['La presentación mostrada es ilustrativa; consulta la presentación disponible.'])
    if top < 40:
        raise ValueError(f"La ficha de {p['nombre']} no cabe en una página: {top}")
    c.showPage()
c.save()
print('PDF creado:', OUT)
