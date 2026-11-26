import { computed, onMounted, ref } from 'vue'
import { normalizar } from '../utils/formato.js'

// Mismo archivo que genera tools/generar.py: así los precios del catálogo y de la
// página principal salen siempre de datos/precios.json.
const URL_DATOS = '../datos/catalogo.json'

export const TODOS = 'Todos'

/** Carga el catálogo y expone la búsqueda y el filtro por grupo. */
export function useCatalog() {
  const datos = ref(null)
  const estado = ref('cargando') // 'cargando' | 'listo' | 'error'
  const busqueda = ref('')
  const grupo = ref(TODOS)

  async function cargar() {
    estado.value = 'cargando'
    try {
      const respuesta = await fetch(URL_DATOS, { cache: 'no-cache' })
      if (!respuesta.ok) throw new Error(`HTTP ${respuesta.status}`)
      datos.value = await respuesta.json()
      estado.value = 'listo'
    } catch (error) {
      console.error('No se pudo cargar el catálogo', error)
      estado.value = 'error'
    }
  }
  onMounted(cargar)

  const productos = computed(() => datos.value?.productos ?? [])

  // Opciones del filtro con su número de productos.
  const grupos = computed(() => [
    { valor: TODOS, cantidad: productos.value.length },
    ...(datos.value?.grupos ?? []).map((g) => ({
      valor: g,
      cantidad: productos.value.filter((p) => p.grupo === g).length,
    })),
  ])

  const visibles = computed(() => {
    const termino = normalizar(busqueda.value)
    return productos.value.filter((p) => {
      if (grupo.value !== TODOS && p.grupo !== grupo.value) return false
      if (!termino) return true
      return normalizar(`${p.nombre} ${p.categoria} ${p.ingredientes}`).includes(termino)
    })
  })

  const precioMinimo = computed(() =>
    productos.value.length ? Math.min(...productos.value.map((p) => p.precio)) : 0,
  )

  /** Nombre y precio de cualquier artículo que se pueda pedir (productos y kits). */
  const articulos = computed(() => {
    const mapa = new Map()
    for (const p of productos.value) mapa.set(p.id, { nombre: p.nombre, precio: p.precio })
    for (const k of datos.value?.kits ?? []) mapa.set(k.id, { nombre: k.nombre, precio: k.precio })
    return mapa
  })

  function limpiarFiltros() {
    busqueda.value = ''
    grupo.value = TODOS
  }

  return {
    datos, estado, cargar, productos, grupos, visibles, precioMinimo, articulos,
    busqueda, grupo, limpiarFiltros,
  }
}
