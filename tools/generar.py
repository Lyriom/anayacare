"""Genera index.html y privacidad.html de Anaya Co.

Uso (desde la raíz del repositorio):
    python3 tools/generar.py

Para cambiar precios edita datos/precios.json y vuelve a ejecutar el script.
Los textos de productos están en las listas PRODUCTS y CATALOG de este archivo;
el texto de la política de privacidad está en tools/privacidad-articulo.html.

Los costos de producción están en datos/costos.json. La sección es temporal:
para quitarla de la página pon MOSTRAR_COSTOS = False y vuelve a ejecutar el script.
"""
import json
import sys
from html import escape
from pathlib import Path
from urllib.parse import quote

TOOLS = Path(__file__).resolve().parent
REPO = TOOLS.parent
sys.path.insert(0, str(TOOLS))
from iconos import ICON  # noqa: E402

PRICES = json.loads((REPO / "datos" / "precios.json").read_text(encoding="utf-8"))
COSTS = json.loads((REPO / "datos" / "costos.json").read_text(encoding="utf-8"))
SPECS = json.loads((REPO / "datos" / "especificaciones.json").read_text(encoding="utf-8"))
MOSTRAR_COSTOS = False  # la información de costos es interna
PRIVACY_ARTICLE = (TOOLS / "privacidad-articulo.html").read_text(encoding="utf-8")

WA_NUMBER = "593963160557"
WA_DISPLAY = "+593 96 316 0557"
SITE = "https://lyriom.github.io/anayacare/"
BRAND = "Anaya Co."


def wa(text):
    return f"https://wa.me/{WA_NUMBER}?text={quote(text, safe='')}"


def money(v):
    return "$" + f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def picture(slug, alt, sizes, *, base="img/productos", widths=(480, 800, 1200), dims=(800, 1000),
            fallback=800, loading="lazy", fetchpriority=None):
    def srcset(ext):
        return ", ".join(f"{base}/{slug}-{w}.{ext} {w}w" for w in widths)

    attrs = [f'src="{base}/{slug}-{fallback}.jpg"', f'srcset="{srcset("jpg")}"', f'sizes="{sizes}"',
             f'width="{dims[0]}" height="{dims[1]}"', f'alt="{escape(alt)}"', 'decoding="async"']
    if loading:
        attrs.append(f'loading="{loading}"')
    if fetchpriority:
        attrs.append(f'fetchpriority="{fetchpriority}"')
    avif = f'<source type="image/avif" srcset="{srcset("avif")}" sizes="{sizes}">' if (REPO / base / f"{slug}-480.avif").exists() else ""
    return ("<picture>"
            f'{avif}'
            f'<source type="image/webp" srcset="{srcset("webp")}" sizes="{sizes}">'
            f"<img {' '.join(attrs)}></picture>")


def logo_img(name, alt, w, h, cls="", loading=None, fetchpriority=None):
    extra = (f' loading="{loading}"' if loading else "") + (f' fetchpriority="{fetchpriority}"' if fetchpriority else "")
    c = f' class="{cls}"' if cls else ""
    return (f'<picture><source type="image/webp" srcset="img/marca/{name}.webp">'
            f'<img{c} src="img/marca/{name}.png" width="{w}" height="{h}" alt="{escape(alt)}" decoding="async"{extra}></picture>')


PRODUCTS = [
    {
        "id": "pestanas", "category": "Mirada", "name": "Tratamiento Crecimiento de Pestañas",
        "tagline": "Realza tu mirada",
        "summary": "Mezcla de aceites vegetales con vitamina E para nutrir y acondicionar tus pestañas desde la raíz.",
        "tags": ["Aceite de ricino", "Aceite de almendras", "Vitamina E"],
        "ingredients_text": "Aceite de ricino, aceite de almendras y vitamina E.", "inci": None,
        "usage": ["Aplicar una pequeña cantidad en la raíz de las pestañas con el aplicador, preferiblemente en la noche."],
        "cautions": ["Uso externo únicamente.", "Evitar el contacto con los ojos.",
                     "Suspender su uso en caso de irritación o reacción adversa.", "Mantener fuera del alcance de los niños."],
        "photos": [
            ("pestanas-frente-ia", "Frasco gotero ámbar del Tratamiento Crecimiento de Pestañas, etiqueta frontal rosa con ilustración de ojo", "Frente"),
            ("pestanas-reverso-ia", "Reverso de la etiqueta del tratamiento de pestañas con ingredientes, modo de uso y precauciones", "Reverso"),
        ],
    },
    {
        "id": "serum", "category": "Rostro", "name": "Sérum de Ácido Hialurónico",
        "tagline": "Hidratación · Firmeza · Juventud",
        "summary": "Sérum ligero con ácido hialurónico, glicerina y vitamina E para el cuidado diario del rostro y el cuello.",
        "tags": ["Ácido hialurónico", "Glicerina", "Vitamina E"],
        "ingredients_text": "Glicerina, propilenglicol, vitamina E y ácido hialurónico.", "inci": None,
        "usage": ["Aplicar unas gotas sobre la piel limpia y seca, en rostro y cuello, realizando un suave masaje hasta su completa absorción."],
        "cautions": ["Uso externo únicamente.", "Evitar el contacto con los ojos.",
                     "Suspender su uso en caso de irritación o reacción adversa.", "Mantener fuera del alcance de los niños.",
                     "Conservar en un lugar fresco y seco, protegido de la luz."],
        "photos": [
            ("serum-hialuronico-frente-ia", "Frasco gotero de vidrio transparente del Sérum de Ácido Hialurónico con tapa dorada", "Frente"),
            ("serum-hialuronico-reverso-ia", "Reverso de la etiqueta del sérum con ingredientes, modo de uso, precauciones y fechas de elaboración y vencimiento", "Reverso"),
        ],
    },
    {
        "id": "protector", "category": "Cabello", "name": "Protector Térmico Capilar",
        "tagline": "Ricino, aguacate, jojoba y argán",
        "summary": "Mezcla de aceites vegetales con extracto de romero para aplicar de medios a puntas antes de usar herramientas de calor.",
        "tags": ["Ricino", "Aguacate", "Jojoba", "Argán", "Romero"],
        "ingredients_text": "Aceites de ricino, aguacate, jojoba y argán, extracto de romero y vitamina E.",
        "inci": "Ricinus Communis (Castor) Seed Oil, Persea Gratissima (Avocado) Oil, Simmondsia Chinensis (Jojoba) Seed Oil, Argania Spinosa Kernel Oil, Rosmarinus Officinalis Leaf Extract, Tocopheryl Acetate.",
        "usage": ["Utilizar sobre cabello húmedo.", "Aplicar unas gotas en la palma de la mano.",
                  "Distribuir uniformemente de medios a puntas.", "Usar antes de herramientas de calor.", "Peinar como de costumbre."],
        "cautions": ["Uso externo solamente.", "Evitar contacto con los ojos.", "No ingerir.",
                     "Mantener fuera del alcance de los niños.", "Suspender su uso si presenta irritación.", "Conservar en lugar fresco."],
        "photos": [
            ("protector-termico-frente-ia", "Frasco gotero ámbar del Protector Térmico Capilar con etiqueta botánica de romero y aguacate", "Frente"),
            ("protector-termico-uso-ia", "Lateral de la etiqueta del protector térmico con el modo de uso", "Modo de uso"),
            ("protector-termico-precauciones-estudio", "Lateral de la etiqueta del protector térmico con las precauciones", "Precauciones"),
        ],
    },
    {
        "id": "capilar-barba", "category": "Cabello y barba", "name": "Tratamiento Capilar & Barba",
        "tagline": "Botanical Care · aceites esenciales naturales",
        "summary": "Aceites de almendras dulces y ricino con aceites esenciales de bergamota y romero, pensado para el cuidado del cabello y la barba.",
        "tags": ["Almendras dulces", "Ricino", "Bergamota", "Romero"],
        "ingredients_text": "Aceite de almendras dulces, aceite de ricino, aceite esencial de bergamota, aceite esencial de romero y vitamina E (tocopherol).",
        "inci": None, "usage": None, "cautions": None,
        "photos": [
            ("capilar-barba-frente-ia", "Frasco gotero ámbar del Tratamiento Capilar & Barba con etiqueta gris oscuro Botanical Care", "Frente"),
            ("capilar-barba-reverso-estudio", "Reverso de la etiqueta del tratamiento capilar y barba con ingredientes INCI, elaboración, expiración y lote", "Reverso"),
        ],
    },
]

CATALOG = [
    ("tonico-descongestivo", "Rostro", "Tónico descongestivo", "Manzanilla, caléndula y vitamina E."),
    ("espuma-facial", "Rostro", "Espuma facial limpiadora", "Agua de hamamelis, aloe vera, glicerina vegetal y betaína de coco."),
    ("agua-micelar", "Rostro", "Agua micelar", "Agua, glicerina, extracto de manzanilla, extracto de caléndula, conservante y tensioactivo suave."),
    ("contorno-ojos", "Rostro", "Contorno de ojos", "Extracto de pepino, ácido hialurónico y vitamina E."),
    ("exfoliante-arroz", "Rostro", "Exfoliante de arroz", "Harina de arroz, avena, caolín y óxido de zinc."),
    ("tonico-capilar", "Cabello", "Tónico capilar", "Romero, ortiga y vitamina E."),
    ("shampoo", "Cabello", "Shampoo líquido de cebolla", "Extracto de cebolla y vitamina E."),
    ("jabon-arroz", "Jabones", "Jabón aclarante de arroz", "Harina de arroz, manteca de karité y aceite de almendras."),
    ("jabon-carbon", "Jabones", "Jabón de carbón activado", "Carbón activado, aceite de jojoba y árbol de té."),
    ("jabon-avena", "Jabones", "Jabón de avena", "Avena, manteca de karité, aceite de coco y vainilla."),
    ("jabon-cafe", "Jabones", "Jabón exfoliante de café", "Café, manteca de karité y aceite de coco."),
    ("balsamo-labial", "Labios", "Bálsamo labial de cera de abejas", "Cera de abejas, aceite de almendras y vitamina E."),
    ("vela-masaje", "Bienestar", "Vela de masaje", "Cera de soja, manteca de karité, aceite de almendras y lavanda."),
    ("refresh", "Bienestar", "Refresh roll-on", "Aceite de almendras y aceite esencial de menta."),
    ("gel-neutro", "Bienestar", "Gel neutro", "Gel de textura ligera, sin fragancia."),
]

CATALOG_PHOTOS = {
    'shampoo': [("shampoo-referencial", "Ilustración del frente del shampoo de cebolla", "Frente · ilustración"), ("shampoo-reverso-ilustrado", "Ilustración del reverso del shampoo de cebolla", "Reverso · ilustración")],
    'jabon-cafe': [("jabon-cafe-referencial", "Ilustración del frente del jabón exfoliante de café", "Frente · ilustración"), ("jabon-cafe-reverso-ilustrado", "Ilustración del reverso del jabón exfoliante de café", "Reverso · ilustración")],
    'exfoliante-arroz': [("exfoliante-arroz-frente-ia", "Exfoliante de arroz: fotografía del producto", "Frente"), ("exfoliante-arroz-reverso-estudio", "Exfoliante de arroz: etiqueta posterior", "Reverso")],
    'vela-masaje': [("vela-masaje-frente-ia", "Vela de masaje: fotografía del producto", "Frente"), ("vela-masaje-reverso-estudio", "Vela de masaje: etiqueta posterior", "Reverso")],
    'gel-neutro': [("gel-neutro-frente-ia", "Gel neutro: fotografía del producto", "Frente"), ("gel-neutro-reverso-estudio", "Gel neutro: etiqueta posterior", "Reverso")],
    'tonico-capilar': [("tonico-capilar-frente-ia", "Tónico capilar: fotografía del producto", "Frente"), ("tonico-capilar-reverso-estudio", "Tónico capilar: vista posterior ilustrativa", "Reverso")],
    'contorno-ojos': [("contorno-ojos-frente-ia", "Contorno de ojos: fotografía del producto", "Frente"), ("contorno-ojos-reverso-estudio", "Contorno de ojos: etiqueta posterior", "Reverso")],
    'tonico-descongestivo': [("tonico-descongestivo-frente-ia", "Tónico descongestivo: fotografía del producto", "Frente"), ("tonico-descongestivo-reverso-estudio", "Tónico descongestivo: etiqueta posterior", "Reverso")],
    'espuma-facial': [("espuma-facial-frente-ia", "Espuma facial limpiadora: fotografía del producto", "Frente"), ("espuma-facial-reverso-estudio", "Espuma facial limpiadora: etiqueta posterior", "Reverso")],
    'agua-micelar': [("agua-micelar-frente-ia", "Agua micelar: fotografía del producto", "Frente"), ("agua-micelar-reverso-estudio", "Agua micelar: etiqueta posterior", "Reverso")],
    'jabon-arroz': [("jabon-arroz-frente-ia", "Jabón aclarante de arroz: fotografía del producto", "Frente"), ("jabon-arroz-reverso-estudio", "Jabón aclarante de arroz: etiqueta posterior", "Reverso")],
    'jabon-avena': [("jabon-avena-frente-ia", "Jabón de avena: fotografía del producto", "Frente"), ("jabon-avena-reverso-estudio", "Jabón de avena: etiqueta posterior", "Reverso")],
    'jabon-carbon': [("jabon-carbon-frente-ia", "Jabón de carbón activado: fotografía del producto", "Frente"), ("jabon-carbon-reverso-ilustrado", "Ilustración del reverso del jabón de carbón activado", "Reverso · ilustración")],
    'balsamo-labial': [("balsamo-labial-frente-ia", "Bálsamo labial de cera de abejas: fotografía del producto", "Frente"), ("balsamo-labial-reverso-estudio", "Bálsamo labial de cera de abejas: etiqueta posterior", "Reverso")],
    'refresh': [("refresh-frente-ia", "Refresh roll-on: fotografía del producto", "Vista de producto"), ("refresh-frente-estudio", "Etiqueta con indicaciones del Refresh roll-on", "Etiqueta posterior")],
}

KITS = [
    ("kit-mirada", "Kit Mirada & Rostro", "Para tu ritual de noche: pestañas y piel hidratadas.",
     ["pestanas", "serum"], ["pestanas-frente-ia", "serum-hialuronico-frente-ia"]),
    ("kit-cabello", "Kit Cabello Botánico", "Limpieza, tónico y protección antes del calor.",
     ["protector", "tonico-capilar", "shampoo"], ["protector-termico-frente-ia"]),
    ("kit-jabones", "Kit Jabones Artesanales", "Los cuatro jabones de la casa: arroz, carbón activado, avena y café.",
     ["jabon-arroz", "jabon-carbon", "jabon-avena", "jabon-cafe"], []),
]


FAQ = [
    ("¿Cómo hago mi pedido?",
     "<p>Agrega los productos que quieras con el botón «Agregar al pedido» y pulsa «Enviar pedido por WhatsApp». Se abrirá un chat con la lista y el total listos para enviar. También puedes escribirnos directamente al " + WA_DISPLAY + ".</p>"),
    ("¿Los precios incluyen el envío?",
     "<p>No. Los precios corresponden al producto. El costo y la forma de entrega se coordinan por WhatsApp según tu ubicación.</p>"),
    ("¿Dónde entregan y cuánto tarda?",
     "<p>La cobertura, el costo y el plazo de entrega se confirman por WhatsApp según tu ubicación y la disponibilidad del producto.</p>"),
    ("¿Cómo puedo pagar?",
     "<p>Al recibir tu pedido por WhatsApp te indicamos las formas de pago disponibles y coordinamos contigo la entrega.</p>"),
    ("¿Cuánto duran los productos?",
     "<p>Cada frasco indica en su etiqueta la fecha de elaboración y la de vencimiento. Revisa la fecha indicada en tu envase y consulta si tienes dudas.</p>"),
    ("¿Sirven para piel sensible?",
     "<p>Usamos ingredientes de origen natural, pero cualquier piel puede reaccionar a un ingrediente. Te recomendamos probar el producto en una zona pequeña antes del primer uso y suspenderlo si notas irritación. Si tienes alergias conocidas, cuéntanos y te orientamos.</p>"),
    ("¿Cómo debo conservarlos?",
     "<p>En un lugar fresco y seco, protegidos de la luz y bien cerrados. Los aceites en frasco ámbar ya vienen protegidos de la luz.</p>"),
    ("¿Qué significa «bajo pedido»?",
     "<p>Son productos que preparamos en lotes pequeños según la demanda. Escríbenos o agrégalos a tu pedido y te confirmamos el tiempo de preparación.</p>"),
]

CARD_SIZES = "(min-width: 76rem) 17rem, (min-width: 36rem) 45vw, 92vw"
DIALOG_SIZES_MAIN = "(min-width: 62rem) 29rem, (min-width: 52rem) 46vw, 92vw"
DIALOG_SIZES_THUMB = "(min-width: 62rem) 14rem, (min-width: 52rem) 23vw, 46vw"


def add_button(pid, name, price, cls="btn btn-gold", label="Agregar al pedido"):
    return (f'<button type="button" class="{cls} js-only" data-add="{pid}" data-name="{escape(name)}" data-price="{price}">'
            f'<span class="label">{label}</span><span class="visually-hidden">: {escape(name)}, {money(price)}</span></button>')


def wa_direct(text, label, cls="btn btn-wa no-js-only", hidden_suffix=""):
    return (f'<a class="{cls}" href="{escape(wa(text))}" target="_blank" rel="noopener">{ICON["whatsapp"]}{label}'
            f'{f"<span class=visually-hidden>{hidden_suffix}</span>" if hidden_suffix else ""}</a>')


def product_card(p):
    front = p["photos"][0]
    price = PRICES[p["id"]]
    tags = "".join(f"<li>{escape(t)}</li>" for t in p["tags"])
    name = escape(p["name"])
    n = len(p["photos"])
    return f"""
        <li>
          <article class="card reveal">
            <button type="button" class="card-media" command="show-modal" commandfor="dlg-{p["id"]}">
              {picture(front[0], front[1], CARD_SIZES)}
              <span class="badge">{n} fotos</span>
              <span class="visually-hidden">Ver fotos y detalles de {name}</span>
            </button>
            <hgroup>
              <p class="eyebrow">{escape(p["category"])}</p>
              <h3>{name}</h3>
              <p class="tagline">{escape(p["tagline"])}</p>
            </hgroup>
            <div>
              <p>{escape(p["summary"])}</p>
              <ul class="tags" aria-label="Ingredientes destacados">{tags}</ul>
            </div>
            <footer>
              <p class="price">{money(price)} <small>USD</small></p>
              <div class="actions">
                {add_button(p["id"], p["name"], price)}
                {wa_direct(f"Hola {BRAND}, quiero pedir: {p['name']} ({money(price)}).", "Pedir", hidden_suffix=f" {name} por WhatsApp")}
                <button type="button" class="btn btn-ghost" command="show-modal" commandfor="dlg-{p["id"]}">Detalles<span class="visually-hidden"> de {name}</span></button>
              </div>
            </footer>
          </article>
        </li>"""


def product_dialog(p):
    name = escape(p["name"])
    price = PRICES[p["id"]]
    figs = []
    for i, (slug, alt, cap) in enumerate(p["photos"]):
        sizes = DIALOG_SIZES_MAIN if i == 0 else DIALOG_SIZES_THUMB
        figs.append(f'<figure>{picture(slug, alt, sizes, fetchpriority="low")}<figcaption>{escape(cap)}</figcaption></figure>')
    sections = [f"""<section>
              <h2>Ingredientes</h2>
              <p>{escape(p["ingredients_text"])}</p>
              {f'<p class="inci"><strong>INCI:</strong> {escape(p["inci"])}</p>' if p["inci"] else ""}
            </section>"""]
    usage = p["usage"] or SPECS.get(p["id"], {}).get("uso")
    cautions = p["cautions"] or SPECS.get(p["id"], {}).get("precauciones")
    if usage:
        if len(usage) > 1:
            items = "".join(f"<li>{escape(u)}</li>" for u in usage)
            sections.append(f'<section><h2>Modo de uso</h2><ol class="steps">{items}</ol></section>')
        else:
            sections.append(f'<section><h2>Modo de uso</h2><p>{escape(usage[0])}</p></section>')
    else:
        sections.append('<section><h2>Modo de uso</h2><p>Escríbenos por WhatsApp y te indicamos cómo aplicarlo según tu necesidad.</p></section>')
    if cautions:
        items = "".join(f"<li>{escape(c)}</li>" for c in cautions)
        sections.append(f'<section><h2>Precauciones</h2><ul class="cautions">{items}</ul></section>')
    if SPECS.get(p["id"], {}).get("orientativo"):
        sections.append('<p class="nota">La guía de uso y las precauciones son orientativas; confirma las indicaciones específicas en la etiqueta.</p>')
    return f"""
  <dialog id="dlg-{p["id"]}" class="sheet" closedby="any" aria-labelledby="dlg-{p["id"]}-title">
    <form method="dialog" class="dialog-close-form">
      <button class="dialog-close" value="close" autofocus><span aria-hidden="true">×</span><span class="visually-hidden">Cerrar</span></button>
    </form>
    <div class="dialog-layout">
      <div class="photos" role="group" aria-label="Fotos de {name}">{"".join(figs)}</div>
      <div class="dialog-body">
        <hgroup>
          <p class="eyebrow">{escape(p["category"])}</p>
          <h1 id="dlg-{p["id"]}-title">{name}</h1>
          <p class="tagline">{escape(p["tagline"])}</p>
        </hgroup>
        <div class="buy-box">
          <p class="price">{money(price)} <small>USD · envío por coordinar</small></p>
          <div class="actions">
            {add_button(p["id"], p["name"], price)}
            {wa_direct(f"Hola {BRAND}, quiero pedir: {p['name']} ({money(price)}).", "Pedir por WhatsApp", cls="btn btn-wa")}
          </div>
        </div>
        <p>{escape(p["summary"])}</p>
        {"".join(sections)}
      </div>
    </div>
    <p class="visually-hidden" data-live aria-live="polite"></p>
  </dialog>"""


def catalog_card(pid, cat, name, ingredients):
    price = PRICES[pid]
    photos = CATALOG_PHOTOS.get(pid, [])
    media = (f'<a class="mini-media" href="catalogo/?producto={quote(pid)}" aria-label="Ver detalles de {escape(name)} en el catálogo">'
             f'{picture(photos[0][0], photos[0][1], CARD_SIZES)}'
             f'{"<span class=mini-reference>Ilustración</span>" if pid in ("shampoo", "jabon-cafe") else ""}</a>') if photos else ''
    return f"""
        <li>
          <article class="mini reveal">
            {media}<header>{ICON[cat]}<hgroup><p class="eyebrow">{escape(cat)}</p><h3>{escape(name)}</h3></hgroup></header>
            <p>{escape(ingredients)} <a class="mini-detail" href="catalogo/?producto={quote(pid)}">Ver detalles<span class="visually-hidden"> de {escape(name)}</span></a></p>
            <footer>
              <p class="price">{money(price)}</p>
              {add_button(pid, name, price, cls="btn btn-ghost", label="Agregar")}
              {wa_direct(f"Hola {BRAND}, quisiera consultar la disponibilidad de: {name} ({money(price)}).", "Consultar", cls="btn btn-ghost no-js-only", hidden_suffix=f" {escape(name)} por WhatsApp")}
            </footer>
          </article>
        </li>"""


def item_name(pid):
    for p in PRODUCTS:
        if p["id"] == pid:
            return p["name"]
    for c in CATALOG:
        if c[0] == pid:
            return c[2]
    raise KeyError(pid)


def kit_card(kid, name, desc, items, photos):
    price = PRICES[kid]
    regular = round(sum(PRICES[i] for i in items), 2)
    saving = round(regular - price, 2)
    lis = "".join(f"<li>{escape(item_name(i))} <span>{money(PRICES[i])}</span></li>" for i in items)
    thumbs = "".join(
        f'<img src="img/productos/{ph}-480.jpg" width="480" height="600" alt="" loading="lazy" decoding="async">'
        for ph in photos)
    media = f'<div class="kit-thumbs" aria-hidden="true">{thumbs}</div>' if photos else f'<div class="kit-thumbs kit-icon" aria-hidden="true">{ICON["Jabones"]}</div>'
    return f"""
        <li>
          <article class="kit reveal">
            {media}
            <hgroup><p class="eyebrow">Kit · ahorras {money(saving)}</p><h3>{escape(name)}</h3></hgroup>
            <div>
              <p>{escape(desc)}</p>
              <ul class="kit-items" aria-label="Incluye">{lis}</ul>
            </div>
            <footer>
              <p class="price">{money(price)} <s aria-label="Precio por separado {money(regular)}">{money(regular)}</s></p>
              {add_button(kid, name, price)}
              {wa_direct(f"Hola {BRAND}, quiero pedir el {name} ({money(price)}).", "Pedir", hidden_suffix=f" {escape(name)} por WhatsApp")}
            </footer>
          </article>
        </li>"""


def header(current_privacy=False):
    pre = "./" if current_privacy else ""
    cta = "" if current_privacy else f'<a class="btn btn-wa header-cta" href="{escape(wa(f"Hola {BRAND}, quisiera información sobre sus productos."))}" target="_blank" rel="noopener">{ICON["whatsapp"]}WhatsApp</a>'
    priv = '<li><a href="privacidad.html" aria-current="page">Privacidad</a></li>' if current_privacy else ""
    return f"""
  <a class="skip-link" href="#main">Saltar al contenido</a>
  <header class="site-header">
    <div class="header-inner">
      <a class="site-logo" href="./">{logo_img("logo-emblema-128", "", 120, 128)}<span class="wordmark">{BRAND}</span></a>
      <nav class="site-nav" aria-label="Principal">
        <button class="menu-button" type="button" popovertarget="site-menu" popovertargetaction="toggle" aria-controls="site-menu">{ICON["menu"]}<span>Menú</span></button>
        <ul id="site-menu" class="site-menu" popover="auto">
          <li><a href="{pre}#productos">Productos</a></li>
          <li><a href="catalogo/">Catálogo</a></li>
          <li><a href="{pre}#nosotros">Nosotros</a></li>
          <li><a href="{pre}#preguntas">Preguntas</a></li>
          <li><a href="{pre}#contacto">Contacto</a></li>
          {priv}
        </ul>
      </nav>
      {cta}
    </div>
  </header>"""


def footer(current_privacy=False):
    pre = "./" if current_privacy else ""
    cur = ' aria-current="page"' if current_privacy else ""
    return f"""
  <footer class="site-footer">
    <div class="wrap footer-inner">
      <div class="footer-brand">
        {logo_img("logo-completo", f"{BRAND} — Equilibrio, ritual, bienestar", 900, 864, loading="lazy")}
        <p>Cosmética botánica artesanal elaborada en Ecuador.</p>
      </div>
      <nav aria-labelledby="footer-nav-title">
        <h2 id="footer-nav-title">Explora</h2>
        <ul>
          <li><a href="{pre}#productos">Productos y precios</a></li>
          <li><a href="catalogo/">Catálogo completo</a></li>
          <li><a href="{pre}#esencia">Misión, visión y objetivo</a></li>
          <li><a href="{pre}#preguntas">Preguntas frecuentes</a></li>
        </ul>
      </nav>
      <div>
        <h2>Contacto</h2>
        <ul>
          <li><a href="{escape(wa(f"Hola {BRAND}"))}" target="_blank" rel="noopener">WhatsApp {WA_DISPLAY}</a></li>
          <li><a href="privacidad.html"{cur}>Política de privacidad</a></li>
        </ul>
      </div>
      <p class="footer-note">© 2026 {BRAND} · Equilibrio · Ritual · Bienestar. Productos cosméticos artesanales de uso externo. Precios en dólares estadounidenses (USD).</p>
    </div>
  </footer>

  <a class="wa-float" href="{escape(wa(f"Hola {BRAND}, quisiera información sobre sus productos."))}" target="_blank" rel="noopener">{ICON["whatsapp"]}<span class="visually-hidden">Escríbenos por WhatsApp</span></a>"""


def head(title, description, canonical, og_image=True, preload_hero=False):
    og = f"""
  <meta property="og:type" content="website">
  <meta property="og:locale" content="es_EC">
  <meta property="og:site_name" content="{BRAND}">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(description)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{SITE}img/og-anaya-co.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">""" if og_image else ""
    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(description)}">
  <meta name="theme-color" content="#faf8f3">
  <link rel="canonical" href="{canonical}">
  <link rel="icon" href="favicon-32.png" sizes="32x32" type="image/png">
  <link rel="icon" href="favicon-192.png" sizes="192x192" type="image/png">
  <link rel="apple-touch-icon" href="apple-touch-icon.png">
  <link rel="preload" href="fonts/cormorant-garamond-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="css/styles.css?v=8">
  <script>document.documentElement.classList.add('has-js')</script>{og}"""


min_price = min(PRICES[p["id"]] for p in PRODUCTS)
all_min = min(PRICES.values())

product_ld = [{
    "@type": "Product",
    "name": p["name"],
    "description": p["summary"],
    "brand": {"@type": "Brand", "name": BRAND},
    "image": [f"{SITE}img/productos/{s}-800.jpg" for s, _, _ in p["photos"]],
    "offers": {"@type": "Offer", "price": f"{PRICES[p['id']]:.2f}", "priceCurrency": "USD",
               "availability": "https://schema.org/InStock", "url": f"{SITE}#productos"},
} for p in PRODUCTS]
json_ld = json.dumps({
    "@context": "https://schema.org",
    "@graph": [{
        "@type": "Organization", "name": BRAND, "url": SITE, "logo": f"{SITE}favicon-512.png",
        "slogan": "Equilibrio · Ritual · Bienestar",
        "contactPoint": {"@type": "ContactPoint", "telephone": "+593-93-992-9104", "contactType": "customer service",
                         "areaServed": "EC", "availableLanguage": "es"},
    }, *product_ld],
}, ensure_ascii=False, indent=2)
json_ld = json_ld.replace(f"{SITE}favicon-512.png", f"{SITE}img/marca/logo-completo.png")

ESSENCE = [
    ("leaf", "Misión",
     "Elaborar cosméticos artesanales de origen botánico, con ingredientes naturales y procesos cuidadosos, que conviertan el autocuidado diario en un ritual de bienestar, con productos honestos, seguros y accesibles, y una atención cercana y personalizada."),
    ("eye", "Visión",
     "Ser una marca ecuatoriana referente en cosmética natural artesanal, reconocida por la calidad de sus fórmulas, la transparencia de sus ingredientes y la confianza de una comunidad que elige cuidarse de forma consciente."),
    ("target", "Objetivo",
     f"Elaborar y comercializar cosméticos botánicos artesanales de calidad, con ingredientes naturales, etiquetado transparente y precios accesibles, para consolidar a {BRAND} como una marca ecuatoriana de confianza en el cuidado natural de la piel, el cabello y el bienestar."),
]


def essence_card(icon, title, text):
    return f"""
          <article class="essence-card reveal">
            {ICON[icon]}
            <h3>{escape(title)}</h3>
            <p>{escape(text)}</p>
          </article>"""


# ---------- Costos de producción (sección temporal) ----------
COST_FIELDS = [
    ("materia_prima", "Materia prima"),
    ("envase_etiqueta", "Envase y etiqueta"),
    ("mano_obra", "Mano de obra"),
    ("cif", "Costos indirectos"),
]


def cents(v):
    return round(v * 100)


def percent(v):
    return f"{v:.1f}".replace(".", ",") + " %"


def cost_rows():
    """Calcula costo unitario, utilidad y margen de cada producto (en centavos, para que todo cuadre)."""
    ids = [p["id"] for p in PRODUCTS] + [c[0] for c in CATALOG]
    missing = [i for i in ids if i not in COSTS]
    extra = [k for k in COSTS if k not in ids]
    if missing or extra:
        raise SystemExit(f"datos/costos.json no coincide con los productos. Faltan: {missing}. Sobran: {extra}.")
    rows = []
    for pid in ids:
        entry = COSTS[pid]
        absent = [k for k, _ in COST_FIELDS if k not in entry]
        if absent:
            raise SystemExit(f"datos/costos.json: a «{pid}» le faltan {absent}.")
        parts = [cents(entry[k]) for k, _ in COST_FIELDS]
        total, price = sum(parts), cents(PRICES[pid])
        if total >= price:
            raise SystemExit(f"datos/costos.json: el costo de «{pid}» ({money(total / 100)}) no es menor que su precio ({money(price / 100)}).")
        rows.append((item_name(pid), parts, total, price, price - total, (price - total) / price * 100))
    return rows


def cost_section():
    labels = [label for _, label in COST_FIELDS] + ["Costo unitario", "Precio de venta", "Utilidad", "Margen sobre el precio"]
    head_cells = "".join(f'<th scope="col">{escape(l)}</th>' for l in ["Producto", *labels])
    body = []
    for name, parts, total, price, profit, margin in cost_rows():
        values = [money(c / 100) for c in parts] + [money(total / 100), money(price / 100), money(profit / 100), percent(margin)]
        classes = [""] * len(parts) + [' class="is-total"', "", ' class="is-profit"', ' class="is-margin"']
        cells = "".join(f'<td{c} data-label="{escape(l)}">{v}</td>' for l, v, c in zip(labels, values, classes))
        body.append(f'\n              <tr><th scope="row">{escape(name)}</th>{cells}</tr>')
    return f"""

    <section class="section" id="costos" aria-labelledby="costos-title">
      <div class="wrap">
        <div class="section-head reveal">
          <p class="eyebrow">Costos de producción</p>
          <h2 id="costos-title">¿Cuánto cuesta elaborar cada producto?</h2>
          <p>Costo estimado de producción por unidad de cada producto, comparado con su precio de venta.</p>
        </div>
        <div class="table-wrap" tabindex="0" role="region" aria-labelledby="costos-caption">
          <table class="cost-table">
            <caption id="costos-caption">Costos de producción por unidad, en dólares (USD)</caption>
            <thead>
              <tr>{head_cells}</tr>
            </thead>
            <tbody>{"".join(body)}
            </tbody>
          </table>
        </div>
        <dl class="cost-notes">
          <div><dt>Materia prima</dt><dd>Ingredientes de cada fórmula: aceites, extractos, activos y conservantes.</dd></div>
          <div><dt>Envase y etiqueta</dt><dd>Frasco, gotero o tapa, etiqueta impresa y empaque.</dd></div>
          <div><dt>Mano de obra</dt><dd>Tiempo de elaboración, envasado y etiquetado de cada unidad.</dd></div>
          <div><dt>Costos indirectos de fabricación</dt><dd>Energía, agua, gas, limpieza y desinfección, utensilios y desgaste de equipos.</dd></div>
          <div><dt>Costo unitario</dt><dd>Materia prima + envase y etiqueta + mano de obra + costos indirectos.</dd></div>
          <div><dt>Utilidad y margen</dt><dd>Utilidad = precio de venta − costo unitario. Margen = utilidad ÷ precio de venta.</dd></div>
        </dl>
        <p class="price-note">Valores estimados de referencia. No incluyen envío, impuestos ni gastos de venta.</p>
      </div>
    </section>"""


STEPS = [
    ("Elige tus productos", "Revisa fotos, ingredientes y precios. Pulsa «Agregar al pedido» en los que quieras."),
    ("Envía tu pedido por WhatsApp", "Con un toque se abre el chat con la lista y el total. Solo tienes que enviarlo."),
    ("Coordinamos pago y entrega", "Te confirmamos disponibilidad, forma de pago y entrega según tu ubicación."),
]

index = head(f"{BRAND} · Cosmética botánica artesanal en Ecuador",
             f"{BRAND}: sérum de ácido hialurónico, tratamiento de pestañas, protector térmico capilar, jabones artesanales y más, desde {money(all_min)}. Ingredientes naturales, pedidos por WhatsApp {WA_DISPLAY}.",
             SITE) + f"""
  <script type="application/ld+json">
{json_ld}
  </script>
  <script src="js/main.js?v=5" type="module"></script>
</head>
<body>
{header()}

  <main id="main">
    <section class="hero" aria-labelledby="hero-title">
      <div class="wrap hero-inner">
        <div class="hero-brand">
          <p class="hero-overline"><span>ANAYA CO.</span><span>CUIDADO BOTÁNICO · ECUADOR</span></p>
          <h1 id="hero-title">Un momento <em>para ti.</em></h1>
          <p class="lead">Cosmética artesanal para acompañar tus rituales de cuidado, creada en pequeños lotes con ingredientes de origen natural.</p>
          <nav class="hero-discover" aria-label="Descubre productos por ritual">
            <p class="hero-discover-title">ELIGE TU RITUAL <span>01 — 02</span></p>
            <a class="hero-path" href="catalogo/?categoria=Rostro+y+mirada">
              <span class="hero-path-number">01</span>
              <span class="hero-path-copy"><strong>Rostro y mirada</strong><small>Hidratación, luz y cuidado diario</small></span>
              <span class="hero-path-arrow" aria-hidden="true">↗</span>
            </a>
            <a class="hero-path" href="catalogo/?categoria=Cabello+y+barba">
              <span class="hero-path-number">02</span>
              <span class="hero-path-copy"><strong>Cabello y barba</strong><small>Nutrir, proteger y renovar</small></span>
              <span class="hero-path-arrow" aria-hidden="true">↗</span>
            </a>
            <a class="hero-collection" href="catalogo/"><span>Ver la colección completa</span><span aria-hidden="true">↗</span></a>
          </nav>
          <p class="hero-price">Cosmética artesanal desde {money(all_min)}</p>
          <p class="hero-signature">Equilibrio <span>·</span> ritual <span>·</span> bienestar</p>
        </div>
        <div class="hero-editorial" aria-label="Una selección de Anaya Care">
          <figure class="hero-product hero-product-main">
            {picture("serum-hialuronico-frente-ia", "Sérum de ácido hialurónico Anaya Care", "(min-width: 60rem) 27vw, 55vw", loading=None, fetchpriority="high")}
            <figcaption><span>01 / ROSTRO</span><span>Sérum de ácido hialurónico</span></figcaption>
          </figure>
          <figure class="hero-product hero-product-secondary">
            {picture("protector-termico-frente-ia", "Protector térmico capilar Anaya Care", "(min-width: 60rem) 19vw, 38vw", loading=None)}
            <figcaption><span>02 / CABELLO</span><span>Protector térmico capilar</span></figcaption>
          </figure>
        </div>
      </div>
    </section>

    <section class="trust" aria-label="Por qué elegirnos">
      <ul class="wrap">
        <li>{ICON["leaf"]}<span>Ingredientes de origen natural</span></li>
        <li>{ICON["hand"]}<span>Elaborado a mano en pequeños lotes</span></li>
        <li>{ICON["label"]}<span>Consulta los ingredientes y las indicaciones</span></li>
        <li>{ICON["chat"]}<span>Pedido y asesoría por WhatsApp</span></li>
      </ul>
    </section>

    <section class="section" id="productos" aria-labelledby="productos-title">
      <div class="wrap">
        <div class="section-head reveal">
          <p class="eyebrow">Productos destacados</p>
          <h2 id="productos-title">Rituales para tu piel, cabello y mirada</h2>
          <p>Toca la foto para ver todas las imágenes, ingredientes, modo de uso y precauciones de cada producto.</p>
          <p class="price-note">Precios en USD. Disponibilidad, pago, cobertura, costo y plazo de entrega se confirman por WhatsApp.</p>
        </div>
        <ul class="product-grid">{"".join(product_card(p) for p in PRODUCTS)}
        </ul>
        <div class="kits-head reveal">
          <h3 id="kits-title">Kits con ahorro</h3>
          <p>Combina productos que funcionan juntos y paga menos que por separado.</p>
        </div>
        <ul class="kit-grid" aria-labelledby="kits-title">{"".join(kit_card(*k) for k in KITS)}
        </ul>
      </div>
    </section>

    <section class="section" id="catalogo" aria-labelledby="catalogo-title">
      <div class="wrap">
        <div class="section-head reveal">
          <p class="eyebrow">Bajo pedido</p>
          <h2 id="catalogo-title">También elaboramos</h2>
          <p>Jabones artesanales, cuidado facial, labial y bienestar. Los preparamos en lotes pequeños: agrégalos a tu pedido y te confirmamos el tiempo de preparación.</p>
          <a class="btn btn-primary section-cta" href="catalogo/">Ver el catálogo completo</a>
          <a class="btn btn-ghost section-cta" href="catalogo-anaya.pdf" download>Descargar catálogo en PDF</a>
        </div>
        <ul class="catalog-grid">{"".join(catalog_card(*c) for c in CATALOG)}
        </ul>
      </div>
    </section>

    <section class="section" id="como-comprar" aria-labelledby="comprar-title">
      <div class="wrap">
        <div class="section-head center reveal">
          <p class="eyebrow">Cómo comprar</p>
          <h2 id="comprar-title">Tu pedido en tres pasos</h2>
        </div>
        <ol class="steps-grid">{"".join(f'<li class="reveal"><h3>{escape(t)}</h3><p>{escape(d)}</p></li>' for t, d in STEPS)}
        </ol>
      </div>
    </section>

    <section class="section" id="esencia" aria-labelledby="esencia-title">
      <div class="wrap">
        <div class="section-head center reveal">
          <p class="eyebrow">Nuestra esencia</p>
          <h2 id="esencia-title">Misión, visión y objetivo</h2>
          <div class="ornament" aria-hidden="true"><span></span></div>
        </div>
        <div class="essence-grid">{"".join(essence_card(*e) for e in ESSENCE)}
        </div>
      </div>
    </section>
{cost_section() if MOSTRAR_COSTOS else ""}


    <section class="section" id="nosotros" aria-labelledby="nosotros-title">
      <div class="wrap about-layout">
        <figure class="brand-card reveal">
          {logo_img("logo-completo", f"Logotipo de {BRAND}: figura dorada con brazos abiertos dentro de un círculo y el lema Equilibrio, ritual, bienestar", 900, 864, loading="lazy")}
          <figcaption>El cuidado diario como un ritual: un momento de equilibrio para ti.</figcaption>
        </figure>
        <div class="about-text">
          <div class="section-head reveal">
            <p class="eyebrow">Nosotros</p>
            <h2 id="nosotros-title">Equilibrio, ritual y bienestar</h2>
            <p>{BRAND} nace del gusto por la química cosmética y las plantas. Formulamos, envasamos y etiquetamos cada producto de forma artesanal, cuidando la calidad de los ingredientes y la información que llevas a casa.</p>
          </div>
          <ul class="values">
            <li class="reveal"><h3>Naturalidad</h3><p>Priorizamos aceites vegetales, extractos y activos de origen natural.</p></li>
            <li class="reveal"><h3>Transparencia</h3><p>Compartimos la información disponible y te ayudamos a confirmar cualquier detalle.</p></li>
            <li class="reveal"><h3>Calidad artesanal</h3><p>Lotes pequeños, elaborados y envasados a mano con higiene y precisión.</p></li>
            <li class="reveal"><h3>Cercanía</h3><p>Te asesoramos de forma personal para que elijas lo que tu piel y tu cabello necesitan.</p></li>
          </ul>
        </div>
      </div>
    </section>

    <section class="section" id="preguntas" aria-labelledby="preguntas-title">
      <div class="wrap faq-layout">
        <div class="section-head faq-intro reveal">
          <p class="eyebrow">Preguntas frecuentes</p>
          <h2 id="preguntas-title">Antes de pedir</h2>
          <div class="ornament" aria-hidden="true"><span></span></div>
          <p>Lo que más nos preguntan sobre pedidos, entrega y cuidado de los productos.</p>
          <p class="faq-cta">¿No encuentras tu respuesta?</p>
          <a class="btn btn-wa" href="{escape(wa(f"Hola {BRAND}, tengo una pregunta sobre sus productos."))}" target="_blank" rel="noopener">{ICON["whatsapp"]}Pregúntanos por WhatsApp</a>
        </div>
        <div class="faq">{"".join(f'<details><summary>{escape(q)}</summary><div>{a}</div></details>' for q, a in FAQ)}
        </div>
      </div>
    </section>

    <section class="section" id="contacto" aria-labelledby="contacto-title">
      <div class="wrap">
        <div class="contact reveal">
          <div>
            <p class="eyebrow">Contacto</p>
            <h2 id="contacto-title">¿Tienes dudas o quieres hacer un pedido?</h2>
            <p>Escríbenos por WhatsApp: te ayudamos a elegir tu producto, coordinamos la entrega y resolvemos cualquier pregunta sobre su uso.</p>
          </div>
          <div class="contact-box">
            <p class="contact-number">{WA_DISPLAY}</p>
            <a class="btn btn-wa" href="{escape(wa(f"Hola {BRAND}, quisiera hacer un pedido."))}" target="_blank" rel="noopener">{ICON["whatsapp"]}Abrir chat de WhatsApp</a>
          </div>
        </div>
      </div>
    </section>
  </main>
{footer()}

  <div class="order-bar" id="order-bar" hidden>
    <p><span class="visually-hidden">Tu pedido: </span><span id="order-bar-count">0 productos</span> · <strong id="order-bar-total">$0,00</strong></p>
    <button type="button" class="btn" command="show-modal" commandfor="dlg-pedido">Ver pedido</button>
  </div>
  <p class="visually-hidden" data-live aria-live="polite"></p>
{"".join(product_dialog(p) for p in PRODUCTS)}

  <dialog id="dlg-pedido" class="sheet narrow" closedby="any" aria-labelledby="order-title">
    <form method="dialog" class="dialog-close-form">
      <button class="dialog-close" value="close"><span aria-hidden="true">×</span><span class="visually-hidden">Cerrar</span></button>
    </form>
    <div class="order-body">
      <h1 id="order-title" tabindex="-1">Tu pedido</h1>
      <p class="order-empty" id="order-empty">Aún no has agregado productos.</p>
      <ul class="order-list" id="order-list" aria-label="Productos del pedido"></ul>
      <p class="order-total">Total <strong id="order-total">$0,00</strong></p>
      <p class="price-note">El costo de envío y la forma de pago se coordinan por WhatsApp.</p>
      <div class="order-actions">
        <a class="btn btn-wa" id="order-send" href="https://wa.me/{WA_NUMBER}" target="_blank" rel="noopener" autofocus>{ICON["whatsapp"]}Enviar pedido por WhatsApp</a>
        <button type="button" class="link-button" id="order-clear">Vaciar pedido</button>
      </div>
    </div>
    <p class="visually-hidden" data-live aria-live="polite"></p>
  </dialog>
  <template id="order-item">
    <li>
      <div><p class="name"></p><p class="unit"></p></div>
      <p class="line-total"></p>
      <div class="qty"><button type="button" value="minus"><span aria-hidden="true">−</span></button><output></output><button type="button" value="plus"><span aria-hidden="true">+</span></button></div>
    </li>
  </template>
</body>
</html>
"""

privacy = head(f"Política de privacidad · {BRAND}",
               f"Política de privacidad y protección de datos personales de {BRAND}, conforme a la Ley Orgánica de Protección de Datos Personales del Ecuador.",
               f"{SITE}privacidad.html", og_image=False) + f"""
  <script src="js/main.js?v=5" type="module"></script>
</head>
<body>
{header(current_privacy=True)}

  <main id="main" class="legal">
    <div class="wrap">
      {PRIVACY_ARTICLE.strip()}
    </div>
  </main>
{footer(current_privacy=True)}
</body>
</html>
"""

# ---------- Datos para la página de catálogo en Vue (catalogo/) ----------
# Grupos del filtro: une categorías con un solo producto para que el filtro sea corto.
GROUPS = {"Mirada": "Rostro y mirada", "Rostro": "Rostro y mirada", "Cabello": "Cabello y barba",
          "Cabello y barba": "Cabello y barba", "Jabones": "Jabones", "Labios": "Labios", "Bienestar": "Bienestar"}
# Fotos de los productos bajo pedido: id -> [(slug, alt, etiqueta)]. Las imágenes van en
# img/productos/<slug>-{480,800,1200}.{avif,webp,jpg}, igual que las de los destacados.



def photo_json(photos):
    return [{"slug": s, "alt": alt, "etiqueta": label} for s, alt, label in photos]


catalog_json = {
    "marca": BRAND,
    "whatsapp": WA_NUMBER,
    "grupos": list(dict.fromkeys(GROUPS.values())),
    "productos": [{
        "id": p["id"], "nombre": p["name"], "categoria": p["category"], "grupo": GROUPS[p["category"]],
        "destacado": True, "lema": p["tagline"], "descripcion": p["summary"],
        "ingredientes": p["ingredients_text"], "inci": p["inci"], "uso": p["usage"] or SPECS.get(p["id"], {}).get("uso"), "precauciones": p["cautions"] or SPECS.get(p["id"], {}).get("precauciones"), "orientativo": SPECS.get(p["id"], {}).get("orientativo", False),
        "precio": PRICES[p["id"]], "fotos": photo_json(p["photos"]),
    } for p in PRODUCTS] + [{
        "id": pid, "nombre": name, "categoria": cat, "grupo": GROUPS[cat],
        "destacado": False, "lema": None, "descripcion": None,
        "ingredientes": ingredients, "inci": None, "uso": SPECS.get(pid, {}).get("uso"), "precauciones": SPECS.get(pid, {}).get("precauciones"), "orientativo": SPECS.get(pid, {}).get("orientativo", False),
        "precio": PRICES[pid], "fotos": photo_json(CATALOG_PHOTOS.get(pid, [])),
    } for pid, cat, name, ingredients in CATALOG],
    # Los kits no se muestran en el catálogo, pero así el pedido compartido conoce su nombre y precio.
    "kits": [{"id": kid, "nombre": name, "precio": PRICES[kid]} for kid, name, *_ in KITS],
}
(REPO / "datos" / "catalogo.json").write_text(json.dumps(catalog_json, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

(REPO / "index.html").write_text(index, encoding="utf-8")
(REPO / "privacidad.html").write_text(privacy, encoding="utf-8")
print("index", len(index), "privacy", len(privacy), "desde", money(all_min), "destacados desde", money(min_price))
