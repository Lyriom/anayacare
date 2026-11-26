# Anaya Co. · Sitio web

Sitio estático de **Anaya Co.** — *Equilibrio · Ritual · Bienestar* —, cosmética botánica artesanal elaborada en Ecuador (línea de productos Anaya Care).

**En vivo:** https://lyriom.github.io/anayacare/

## Qué incluye

- **Productos destacados con precio**: Tratamiento Crecimiento de Pestañas, Sérum de Ácido Hialurónico, Protector Térmico Capilar y Tratamiento Capilar & Barba. Cada uno abre una ficha con **todas sus fotos** (enderezadas y sobre fondo de estudio), ingredientes, modo de uso y precauciones tomados de la etiqueta.
- **Kits con ahorro** (Mirada & Rostro, Cabello Botánico, Jabones Artesanales).
- **Catálogo bajo pedido** con precio de los demás productos artesanales.
- **Pedido por WhatsApp**: se agregan productos, se ajustan cantidades y se envía la lista con el total a **+593 93 992 9104**. Sin JavaScript, cada producto tiene su enlace directo a WhatsApp.
- **Misión, visión y objetivo** al inicio de la página, justo después de la portada.
- **Cómo comprar**, **nosotros y valores**, **preguntas frecuentes** y **contacto**.
- **Costos de producción por unidad** (sección temporal al final): materia prima, envase y etiqueta, mano de obra, costos indirectos, costo unitario, utilidad y margen.
- **Política de privacidad** conforme a la Ley Orgánica de Protección de Datos Personales del Ecuador (`privacidad.html`).

## Cambiar precios o textos

1. Edita los precios en `datos/precios.json` (en dólares, con punto decimal: `12.90`).
2. Desde la raíz del repositorio ejecuta `python3 tools/generar.py`.
3. Haz `git commit` y `git push`.

Los costos de producción están en `datos/costos.json` (mismos nombres que en `precios.json`); el costo unitario, la utilidad y el margen se calculan solos. Para **quitar la sección de costos**, cambia `MOSTRAR_COSTOS = True` a `False` en `tools/generar.py` y vuelve a ejecutar el script.

El script regenera `index.html` y `privacidad.html`: precios visibles, botones de pedido, mensajes de WhatsApp, kits con su ahorro y datos para buscadores. Los textos de productos y kits están en `tools/generar.py`; la política de privacidad, en `tools/privacidad-articulo.html`.

## Estructura

```
index.html          Página principal (generada)
privacidad.html     Política de privacidad (generada)
datos/precios.json  Precios en USD
datos/costos.json   Costos de producción por unidad (sección temporal)
tools/generar.py    Genera las dos páginas
css/styles.css      Estilos (paleta marfil y dorado del logo)
js/main.js          Navegación adaptable, pedido por WhatsApp, polyfills condicionales
js/vendor/          Polyfills (popover, invoker commands) con licencia MIT
fonts/              Cormorant Garamond y Jost (SIL OFL), auto-alojadas
img/marca/          Logo de Anaya Co. con fondo transparente
img/productos/      Fotos de producto en AVIF, WebP y JPEG (480, 800 y 1200 px)
img/                Foto de la colección e imagen para redes sociales
```

## Fotos

Las fotos originales (iPhone, HEIC) se procesaron localmente: recorte del producto, ajuste automático de exposición y color, fondo de estudio con sombra suave y exportación en AVIF/WebP/JPEG a varios tamaños. Se eliminaron todos los metadatos, incluida la ubicación GPS.

## Prácticas web aplicadas

Basado en [Modern Web Guidance](https://github.com/GoogleChrome/modern-web-guidance) de Google Chrome:

- Imágenes responsive con `<picture>`, `srcset`/`sizes`, `width`/`height` y `fetchpriority="high"` solo en la imagen principal.
- Fichas y pedido en `<dialog>` nativo (`command="show-modal"`, `closedby="any"` con respaldo) y animación con `@starting-style`.
- Navegación que pasa a menú `popover` cuando no cabe en una fila.
- Preguntas frecuentes con `<details>` y animación de `::details-content`.
- Anuncios accesibles del pedido con `ariaNotify()` y región viva de respaldo.
- Tipografía fluida con `clamp()`, `text-wrap: balance`/`pretty` y transiciones entre páginas con `@view-transition`.

## Publicar cambios

Es un sitio estático sin compilación: edita los archivos y haz `git push` a `main`. GitHub Pages lo publica automáticamente.
