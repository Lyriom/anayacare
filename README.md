# Anaya Care · Sitio web

Sitio estático de **Anaya Care**, cosmética botánica artesanal elaborada en Ecuador.

**En vivo:** https://lyriom.github.io/anayacare/

## Contenido

- **Productos destacados** con fotos reales: Tratamiento Crecimiento de Pestañas, Sérum de Ácido Hialurónico, Protector Térmico Capilar y Tratamiento Capilar & Barba. Cada uno tiene un diálogo con galería, ingredientes, modo de uso y precauciones tomados de su etiqueta.
- **Catálogo bajo pedido** con el resto de productos artesanales.
- **Misión, visión y valores**.
- **Contacto por WhatsApp**: +593 93 992 9104 (botón flotante y mensajes precargados por producto).
- **Política de privacidad** conforme a la Ley Orgánica de Protección de Datos Personales del Ecuador (`privacidad.html`).

## Estructura

```
index.html          Página principal
privacidad.html     Política de privacidad y protección de datos
css/styles.css      Estilos
js/main.js          Navegación adaptable, polyfills condicionales, cierre de diálogos
js/vendor/          Polyfills (popover, invoker commands) con licencia MIT
fonts/              Cormorant Garamond y Jost (SIL OFL), auto-alojadas
img/                Foto de colección (hero) e imagen para redes sociales
img/productos/      Fotos de producto en AVIF, WebP y JPEG (480, 800 y 1200 px)
```

## Fotos

Las fotos originales (iPhone, HEIC) se procesaron localmente: recorte del producto, ajuste automático de exposición y color, fondo de estudio con sombra suave y exportación en AVIF/WebP/JPEG a varios tamaños. Se eliminaron todos los metadatos (incluida la ubicación GPS).

## Prácticas web aplicadas

Basado en la guía [Modern Web Guidance](https://github.com/GoogleChrome/modern-web-guidance) de Google Chrome:

- Imágenes responsive con `<picture>`, `srcset`/`sizes`, `width`/`height` y `fetchpriority="high"` solo en la imagen principal (LCP); `loading="lazy"` en el resto.
- Diálogos nativos `<dialog>` abiertos con `command="show-modal"`, cierre al tocar fuera (`closedby="any"` + fallback) y animación de entrada/salida con `@starting-style`.
- Navegación con menú `popover` cuando no cabe en una fila.
- Animaciones de aparición con `animation-timeline: view()` (respetando `prefers-reduced-motion`).
- Tipografía fluida con `clamp()` y `text-wrap: balance`/`pretty`.
- Transiciones entre páginas con `@view-transition`.

## Publicar cambios

Es un sitio estático sin dependencias de compilación: edita los archivos y haz `git push` a `main`. GitHub Pages lo publica automáticamente.
