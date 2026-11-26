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
c.showPage()

# Fichas editoriales: foto principal y detalles propios de cada producto.
w,h=A4
ACCENTS = {
    'Rostro': '#65765c', 'Mirada': '#a15f6d', 'Cabello': '#607b66',
    'Cabello y barba': '#4c6458', 'Jabones': '#9a7745',
    'Labios': '#a15f6d', 'Bienestar': '#82765d',
}
for index,p in enumerate(data['productos']):
    background(w,h,index+3)
    accent=colors.HexColor(ACCENTS.get(p['categoria'],'#65765c'))
    c.setFillColor(accent); c.setFont('AnayaSansBold',8.5)
    c.drawString(36,h-41,p['categoria'].upper() + '  /  ANAYA CARE')
    c.setFillColor(MUTED); c.setFont('AnayaSans',8.5)
    c.drawRightString(w-36,h-41,f"{index+1:02d} / {len(data['productos']):02d}")
    title_height=paragraph(p['nombre'],36,h-54,w-72,22,25,'AnayaSerif')
    if title_height > 52: raise ValueError(f"Título demasiado largo: {p['nombre']}")
    c.setStrokeColor(LINE); c.line(36,h-115,w-36,h-115)
    photos=p['fotos']; left=36; left_w=230; image_top=h-132; main_h=287.5
    c.setFillColor(SAND); c.rect(left,image_top-main_h,left_w,main_h,fill=1,stroke=0)
    first=photos[0]
    photo(ROOT/'img/productos'/f"{first['slug']}-800.jpg",left,image_top-main_h,left_w,main_h)
    c.setFillColor(MUTED); c.setFont('AnayaSans',8)
    c.drawString(left,image_top-main_h-13,first['etiqueta'])
    if len(photos)>1:
        others=([photos[1], photos[-1]] if len(photos)>3 else photos[1:3]); gap=9; small_w=(left_w-gap*(len(others)-1))/len(others)
        small_top=image_top-main_h-27; small_h=210 if len(others)==1 else 130
        for i,f in enumerate(others):
            image_path=ROOT/'img/productos'/f"{f['slug']}-800.jpg"
            iw,ih=ImageReader(str(image_path)).getSize()
            actual_w=min(small_w,small_h*iw/ih)
            x=left+i*(small_w+gap)
            c.setFillColor(SAND); c.rect(x,small_top-small_h,actual_w,small_h,fill=1,stroke=0)
            photo(image_path,x,small_top-small_h,actual_w,small_h)
            paragraph(f['etiqueta'],x,small_top-small_h-4,small_w,7,9,color=MUTED)
    elif 'referencial' in first['slug']:
        paragraph('Imagen referencial. Consulta la presentación disponible.',left,image_top-main_h-32,left_w,9,13,color=MUTED)
    else:
        paragraph('Vista disponible del producto.',left,image_top-main_h-32,left_w,9,13,color=MUTED)
    x=292; col_w=w-36-x; top=image_top-2
    if p.get('lema'):
        top-=paragraph(p['lema'],x,top,col_w,10.5,15,'AnayaSerif',accent)+19
    if p.get('descripcion'):
        top-=paragraph(p['descripcion'],x,top,col_w,9.5,14,color=MUTED)+20
    def section(title, lines):
        global top
        c.setStrokeColor(LINE); c.line(x,top+4,x+col_w,top+4)
        c.setFillColor(accent); c.setFont('AnayaSansBold',8)
        c.drawString(x,top-10,title.upper()); top-=19
        for line in lines:
            used=paragraph(line,x,top,col_w,10.5,16,color=INK)
            top-=used+7
        top-=17
    section('Ingredientes', [p['ingredientes']])
    if p.get('uso'): section('Modo de uso',p['uso'])
    if p.get('precauciones'): section('Precauciones',p['precauciones'])
    if p.get('orientativo'):
        section('Guía orientativa', ['Las indicaciones de uso y precauciones son generales; confirma las instrucciones específicas en la etiqueta.'])
    if not p.get('uso') or not p.get('precauciones'):
        missing=[]
        if not p.get('uso'): missing.append('modo de uso')
        if not p.get('precauciones'): missing.append('precauciones')
        section('Información por confirmar', ['Consulta la etiqueta o escríbenos para confirmar ' + ' y '.join(missing) + '.'])
    if top < 105: raise ValueError(f"La ficha de {p['nombre']} no cabe: {top:.1f}")
    # Franja de compra constante y fuera de la zona de lectura.
    c.setFillColor(colors.HexColor('#edf0e9')); c.rect(36,48,w-72,43,fill=1,stroke=0)
    c.setFillColor(INK); c.setFont('AnayaSerif',17); c.drawString(48,62,money(p['precio']))
    c.setFillColor(accent); c.setFont('AnayaSansBold',8.5); c.drawRightString(w-48,64,'PEDIDOS  ·  +593 96 316 0557')
    c.showPage()
c.save()
print('PDF creado:', OUT)
