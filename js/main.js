// Anaya Care — comportamiento mínimo del sitio.
// Todo es mejora progresiva: sin JS el contenido y los enlaces siguen funcionando.

const loadScript = (src) =>
  new Promise((resolve, reject) => {
    const s = document.createElement('script');
    s.src = src;
    s.onload = resolve;
    s.onerror = reject;
    document.head.append(s);
  });

// Polyfills locales, cargados solo cuando el navegador no soporta la API.
const polyfills = [];
if (!Object.hasOwn(HTMLElement.prototype, 'popover')) {
  polyfills.push(loadScript('js/vendor/popover-polyfill.min.js'));
}
if (!('commandForElement' in HTMLButtonElement.prototype)) {
  polyfills.push(loadScript('js/vendor/invokers-polyfill.min.js'));
}

// Cierre al tocar fuera del diálogo en navegadores sin <dialog closedby>.
if (!('closedBy' in HTMLDialogElement.prototype)) {
  // Se compara la posición del puntero (no event.target), porque el <dialog>
  // también es el target de su propio padding.
  const outside = (e, dialog) => {
    const r = dialog.getBoundingClientRect();
    return e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom;
  };
  for (const dialog of document.querySelectorAll('dialog[closedby="any"]')) {
    let pressedOutside = false;
    dialog.addEventListener('pointerdown', (e) => { pressedOutside = outside(e, dialog); });
    dialog.addEventListener('pointerup', (e) => {
      if (pressedOutside && outside(e, dialog)) dialog.close();
    });
  }
}

// Navegación: en línea cuando cabe, menú popover cuando no.
const header = document.querySelector('.site-header');
const inner = header?.querySelector('.header-inner');
const menu = document.getElementById('site-menu');

if (header && inner && menu) {
  let lastWidth = 0;
  const isOpen = () => menu.matches(':is(:popover-open, .\\:popover-open)');

  const sync = () => {
    const width = inner.clientWidth;
    const wide = header.classList.contains('is-wide');
    // En modo colapsado solo se vuelve a medir si el encabezado creció.
    if (!wide && lastWidth && width <= lastWidth) { lastWidth = width; return; }
    lastWidth = width;

    const wasOpen = !wide && isOpen();
    header.classList.add('is-measuring', 'is-wide');
    menu.removeAttribute('popover');
    const fits = inner.scrollWidth <= inner.clientWidth;
    if (!fits) {
      header.classList.remove('is-wide');
      menu.setAttribute('popover', 'auto');
      if (wasOpen) menu.showPopover();
    }
    requestAnimationFrame(() => header.classList.remove('is-measuring'));
  };

  Promise.allSettled(polyfills).then(() => {
    const ro = new ResizeObserver(sync);
    ro.observe(header);
    ro.observe(menu);
    document.fonts?.ready.then(sync);
  });

  // Al elegir una sección desde el menú colapsado, se cierra el menú.
  menu.addEventListener('click', (e) => {
    if (e.target.closest('a') && menu.hasAttribute('popover') && isOpen()) menu.hidePopover();
  });
}
