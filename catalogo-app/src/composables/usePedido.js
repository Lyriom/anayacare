import { computed, onBeforeUnmount, onMounted, ref } from 'vue'

// Misma clave y forma que js/main.js del sitio principal: [{ id, name, price, qty }].
// Así el pedido es el mismo en la página principal y en el catálogo.
const CLAVE = 'anaya-co-pedido'

function leer() {
  try {
    const guardado = JSON.parse(localStorage.getItem(CLAVE) || '[]')
    if (!Array.isArray(guardado)) return []
    return guardado
      .map((item) => ({ ...item, qty: Math.floor(Number(item?.qty)), price: Number(item?.price) }))
      .filter((item) => typeof item.id === 'string' && item.qty > 0 && Number.isFinite(item.price))
  } catch {
    return [] // almacenamiento no disponible: el pedido vive solo en esta visita
  }
}

/**
 * Pedido compartido con la página principal.
 * @param {import('vue').Ref<Map<string, {nombre: string, precio: number}>>} articulos
 *   nombre y precio vigentes de cada artículo, para corregir datos guardados antiguos.
 */
export function usePedido(articulos) {
  const lineas = ref(leer())

  // Actualiza nombre y precio de los artículos conocidos. Los desconocidos se dejan
  // tal cual para no borrar nada que se haya agregado en la otra página.
  // No se guarda aquí: abrir la página nunca modifica el pedido almacenado.
  const vigentes = computed(() =>
    lineas.value.map((linea) => {
      const actual = articulos.value.get(linea.id)
      return actual ? { ...linea, name: actual.nombre, price: actual.precio } : linea
    }),
  )

  function guardar() {
    lineas.value = vigentes.value
    try {
      localStorage.setItem(CLAVE, JSON.stringify(lineas.value))
    } catch { /* sin almacenamiento */ }
  }

  function cambiar(id, nombre, precio, delta) {
    const linea = lineas.value.find((l) => l.id === id)
    if (linea) linea.qty += delta
    else if (delta > 0) lineas.value.push({ id, name: nombre, price: precio, qty: delta })
    lineas.value = lineas.value.filter((l) => l.qty > 0)
    guardar()
    return lineas.value.find((l) => l.id === id)?.qty ?? 0
  }

  function vaciar() {
    lineas.value = []
    guardar()
  }

  const cantidad = computed(() => vigentes.value.reduce((n, l) => n + l.qty, 0))
  const total = computed(() => vigentes.value.reduce((s, l) => s + l.price * l.qty, 0))

  // Si el pedido cambia en otra pestaña (por ejemplo, en la página principal), se refleja aquí.
  const alCambiarEnOtraPestana = (e) => { if (e.key === CLAVE) lineas.value = leer() }
  onMounted(() => window.addEventListener('storage', alCambiarEnOtraPestana))
  onBeforeUnmount(() => window.removeEventListener('storage', alCambiarEnOtraPestana))

  return { lineas: vigentes, cantidad, total, cambiar, vaciar }
}
