// Anaya Co. — comportamiento del sitio.
// Todo es mejora progresiva: sin JS, los enlaces directos a WhatsApp siguen funcionando.

document.documentElement.classList.add('has-js');

const WA_NUMBER = '593963160557';

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

/* ---------- Navegación: en línea cuando cabe, menú popover cuando no ---------- */
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

  menu.addEventListener('click', (e) => {
    if (e.target.closest('a') && menu.hasAttribute('popover') && isOpen()) menu.hidePopover();
  });
}

/* ---------- Pedido por WhatsApp ---------- */
const money = new Intl.NumberFormat('es-EC', { style: 'currency', currency: 'USD' });
const STORAGE_KEY = 'anaya-co-pedido';
const order = new Map(); // id -> { name, price, qty }

try {
  const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
  // Nombre y precio se toman siempre de la página actual, por si cambiaron desde la última visita.
  for (const item of saved) {
    const btn = item?.id && document.querySelector(`[data-add="${CSS.escape(item.id)}"]`);
    const qty = Math.floor(Number(item?.qty));
    if (btn && qty > 0) {
      order.set(item.id, { name: btn.dataset.name, price: Number(btn.dataset.price), qty });
    }
  }
} catch { /* almacenamiento no disponible: el pedido vive solo en esta visita */ }

const save = () => {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify([...order.entries()].map(([id, v]) => ({ id, ...v }))));
  } catch { /* sin almacenamiento */ }
};

const totals = () => {
  let count = 0, sum = 0;
  for (const { price, qty } of order.values()) { count += qty; sum += price * qty; }
  return { count, sum };
};

const waLink = (text) => `https://wa.me/${WA_NUMBER}?text=${encodeURIComponent(text)}`;

const orderMessage = () => {
  const lines = [...order.values()].map(
    ({ name, price, qty }) => `• ${qty} × ${name} — ${money.format(price * qty)}`
  );
  return [
    'Hola Anaya Co., quiero hacer este pedido:',
    ...lines,
    `Total: ${money.format(totals().sum)}`,
    '¿Me confirman disponibilidad, forma de pago y entrega?',
  ].join('\n');
};

// Anuncios para lectores de pantalla: ariaNotify() o región viva como respaldo.
const announce = (text) => {
  const target = document.querySelector('dialog[open]') ?? document;
  if (typeof target.ariaNotify === 'function') { target.ariaNotify(text); return; }
  const region = (target === document ? document : target).querySelector('[data-live]');
  if (!region) return;
  region.textContent = '';
  requestAnimationFrame(() => { region.textContent = text; });
};

const bar = document.getElementById('order-bar');
const barCount = document.getElementById('order-bar-count');
const barTotal = document.getElementById('order-bar-total');
const list = document.getElementById('order-list');
const empty = document.getElementById('order-empty');
const totalOut = document.getElementById('order-total');
const send = document.getElementById('order-send');
const clear = document.getElementById('order-clear');
const itemTpl = document.getElementById('order-item');

const render = () => {
  const { count, sum } = totals();
  if (bar) {
    bar.hidden = count === 0;
    barCount.textContent = `${count} ${count === 1 ? 'producto' : 'productos'}`;
    barTotal.textContent = money.format(sum);
  }
  if (!list) return;
  list.replaceChildren();
  for (const [id, { name, price, qty }] of order) {
    const li = itemTpl.content.firstElementChild.cloneNode(true);
    li.querySelector('.name').textContent = name;
    li.querySelector('.unit').textContent = `${money.format(price)} c/u`;
    li.querySelector('output').textContent = qty;
    li.querySelector('.line-total').textContent = money.format(price * qty);
    const [minus, plus] = li.querySelectorAll('.qty button');
    minus.dataset.id = plus.dataset.id = id;
    minus.setAttribute('aria-label', `Quitar una unidad de ${name}`);
    plus.setAttribute('aria-label', `Agregar una unidad de ${name}`);
    li.querySelector('output').setAttribute('aria-label', `Cantidad de ${name}`);
    list.append(li);
  }
  empty.hidden = count > 0;
  list.hidden = count === 0;
  totalOut.textContent = money.format(sum);
  send.hidden = clear.hidden = count === 0;
  send.href = waLink(orderMessage());
};

const add = (id, name, price, delta = 1) => {
  const item = order.get(id) ?? { name, price, qty: 0 };
  item.qty += delta;
  if (item.qty <= 0) order.delete(id); else order.set(id, item);
  save();
  render();
  return item.qty;
};

document.addEventListener('click', (e) => {
  const addBtn = e.target.closest('[data-add]');
  if (addBtn) {
    const { add: id, name, price } = addBtn.dataset;
    add(id, name, Number(price));
    const { count, sum } = totals();
    announce(`${name} agregado al pedido. Llevas ${count} ${count === 1 ? 'producto' : 'productos'}, total ${money.format(sum)}.`);
    const label = addBtn.querySelector('.label');
    if (label) {
      const original = label.dataset.original ?? label.textContent;
      label.dataset.original = original;
      label.textContent = 'Agregado ✓';
      addBtn.setAttribute('data-added', '');
      clearTimeout(addBtn._t);
      addBtn._t = setTimeout(() => { label.textContent = original; addBtn.removeAttribute('data-added'); }, 1600);
    }
    return;
  }
  const step = e.target.closest('.qty button');
  if (step) {
    const item = order.get(step.dataset.id);
    if (!item) return;
    const qty = add(step.dataset.id, item.name, item.price, step.value === 'plus' ? 1 : -1);
    announce(qty > 0 ? `${item.name}: ${qty}. Total ${money.format(totals().sum)}.` : `${item.name} quitado del pedido.`);
    // Si se quitó el producto, mover el foco a un lugar estable dentro del diálogo.
    if (qty <= 0) document.getElementById('order-title')?.focus();
  }
});

clear?.addEventListener('click', () => {
  order.clear();
  save();
  render();
  announce('Pedido vaciado.');
  document.getElementById('order-title')?.focus();
});

render();
