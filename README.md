# Anaya Co. · Sitio web

Sitio estático de **Anaya Co.** — *Equilibrio · Ritual · Bienestar* —, cosmética botánica artesanal elaborada en Ecuador (línea de productos Anaya Care).

**En vivo:** https://lyriom.github.io/anayacare/ · **Catálogo (Vue):** https://lyriom.github.io/anayacare/catalogo/

## Qué incluye

- **Productos destacados con precio**: Tratamiento Crecimiento de Pestañas, Sérum de Ácido Hialurónico, Protector Térmico Capilar y Tratamiento Capilar & Barba. Cada uno abre una ficha con **todas sus fotos** (enderezadas y sobre fondo de estudio), ingredientes, modo de uso y precauciones tomados de la etiqueta.
- **Kits con ahorro** (Mirada & Rostro, Cabello Botánico, Jabones Artesanales).
- **Catálogo bajo pedido** con precio de los demás productos artesanales.
- **Página de catálogo en Vue 3 con Atomic Design** (`catalogo/`): los 19 productos con buscador, filtro por categoría, ficha con todas las fotos y el mismo pedido por WhatsApp que la página principal.
- **Pedido por WhatsApp**: se agregan productos, se ajustan cantidades y se envía la lista con el total a **+593 96 316 0557**. Sin JavaScript, cada producto tiene su enlace directo a WhatsApp.
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
datos/catalogo.json Datos del catálogo para la página en Vue (generado)
catalogo/           Página de catálogo compilada (generada por Vite)
catalogo-app/       Código fuente del catálogo en Vue 3 (Atomic Design)
tools/generar.py    Genera las dos páginas
css/styles.css      Estilos (paleta marfil y dorado del logo)
js/main.js          Navegación adaptable, pedido por WhatsApp, polyfills condicionales
js/vendor/          Polyfills (popover, invoker commands) con licencia MIT
fonts/              Cormorant Garamond y Jost (SIL OFL), auto-alojadas
img/marca/          Logo de Anaya Co. con fondo transparente
img/productos/      Fotos de producto en AVIF, WebP y JPEG (480, 800 y 1200 px)
img/                Foto de la colección e imagen para redes sociales
```

## Catálogo en Vue 3 con Atomic Design

La página `catalogo/` está hecha con **Vue 3** (componentes `.vue` con `<script setup>`) y **Vite**. El código fuente está en `catalogo-app/` y se organiza con **Atomic Design**:

| Nivel | Componentes | Qué hacen |
|---|---|---|
| **Átomos** (`components/atoms`) | `BaseButton`, `BaseIcon`, `PriceTag`, `CategoryTag`, `ProductPicture`, `BrandLogo`, `RoundButton` | Piezas mínimas: solo reciben props y emiten eventos, sin estado de la app. |
| **Moléculas** (`components/molecules`) | `SearchField`, `CategoryFilter`, `ProductMedia`, `QuantityStepper`, `OrderLine`, `PhotoGallery` | Combinan átomos en una unidad con un propósito (buscar, elegir categoría, cambiar cantidad…). |
| **Organismos** (`components/organisms`) | `CatalogHeader`, `CatalogToolbar`, `ProductCard`, `ProductGrid`, `ProductDialog`, `OrderDialog`, `OrderBar`, `CatalogFooter` | Secciones completas de la interfaz formadas por moléculas y átomos. |
| **Plantilla** (`components/templates`) | `CatalogTemplate` | Estructura de la página por zonas (encabezado, introducción, herramientas, contenido, pie, capas) sin contenido real. |
| **Página** (`components/pages`) | `CatalogPage` | Instancia de la plantilla con datos reales: conecta los composables con los organismos. |

La lógica compartida vive en **composables** (`src/composables`), no en los componentes:

- `useCatalog` carga `datos/catalogo.json` y resuelve búsqueda (sin tildes) y filtro por categoría.
- `usePedido` maneja el pedido en `localStorage` con la misma clave que la página principal, así el pedido es uno solo en las dos páginas.
- `useModal` abre los `<dialog>` con `showModal()` y agrega el cierre al tocar fuera en navegadores sin `closedby`.
- `useAnnouncer` anuncia cambios del pedido a lectores de pantalla (`ariaNotify()` o región `aria-live`).

**Precios:** la página lee `datos/catalogo.json` al abrirse, y ese archivo lo genera `tools/generar.py` desde `datos/precios.json`. Cambiar precios sigue siendo editar `precios.json` y ejecutar `python3 tools/generar.py`: no hace falta recompilar Vue.

**Fotos de los productos bajo pedido:** agrégalas en `CATALOG_PHOTOS` de `tools/generar.py` (mismo formato que las de los destacados) y vuelve a ejecutar el script. Mientras un producto no tenga foto, el catálogo muestra una lámina con el icono de su categoría.

**Cambiar el diseño o los componentes:**

```sh
cd catalogo-app
npm install        # solo la primera vez
npm run dev        # servidor local con recarga en http://localhost:5173
npm run build      # compila en ../catalogo (lo que se publica)
```

Después de `npm run build`, haz `git commit` y `git push` de la carpeta `catalogo/`.

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
