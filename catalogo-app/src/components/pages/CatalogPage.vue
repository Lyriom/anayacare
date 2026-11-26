<script setup>
// Página: conecta los datos (composables) con la plantilla y los organismos.
import { computed, nextTick, ref } from 'vue'
import { useAnnouncer } from '../../composables/useAnnouncer.js'
import { useCatalog } from '../../composables/useCatalog.js'
import { usePedido } from '../../composables/usePedido.js'
import { formatoDinero } from '../../utils/formato.js'
import BaseButton from '../atoms/BaseButton.vue'
import BaseIcon from '../atoms/BaseIcon.vue'
import CatalogFooter from '../organisms/CatalogFooter.vue'
import CatalogHeader from '../organisms/CatalogHeader.vue'
import CatalogToolbar from '../organisms/CatalogToolbar.vue'
import OrderBar from '../organisms/OrderBar.vue'
import OrderDialog from '../organisms/OrderDialog.vue'
import ProductDialog from '../organisms/ProductDialog.vue'
import ProductGrid from '../organisms/ProductGrid.vue'
import CatalogTemplate from '../templates/CatalogTemplate.vue'

const MARCA = 'Anaya Co.'
const WHATSAPP = '593939929104'

const {
  datos, estado, cargar, productos, grupos, visibles, precioMinimo, articulos,
  busqueda, grupo, limpiarFiltros,
} = useCatalog()
const pedido = usePedido(articulos)
const { mensaje, anunciar } = useAnnouncer()

const marca = computed(() => datos.value?.marca ?? MARCA)
const whatsapp = computed(() => datos.value?.whatsapp ?? WHATSAPP)

const unidades = (n) => `${n} ${n === 1 ? 'producto' : 'productos'}`

function agregar(producto) {
  pedido.cambiar(producto.id, producto.nombre, producto.precio, 1)
  anunciar(`${producto.nombre} agregado al pedido. Llevas ${unidades(pedido.cantidad.value)}, total ${formatoDinero(pedido.total.value)}.`)
}

function cambiarLinea(linea, delta) {
  const cantidad = pedido.cambiar(linea.id, linea.name, linea.price, delta)
  anunciar(cantidad > 0
    ? `${linea.name}: ${cantidad}. Total ${formatoDinero(pedido.total.value)}.`
    : `${linea.name} quitado del pedido.`)
}

function vaciar() {
  pedido.vaciar()
  anunciar('Pedido vaciado.')
}

// Ficha del producto: se elige el producto y luego se abre el diálogo.
const seleccionado = ref(null)
const ficha = ref(null)
async function verProducto(producto) {
  seleccionado.value = producto
  await nextTick()
  ficha.value.abrir()
}

const pedidoDialogo = ref(null)
const verPedido = () => pedidoDialogo.value.abrir()
</script>

<template>
  <CatalogTemplate>
    <template #encabezado>
      <CatalogHeader :marca="marca" :cantidad="pedido.cantidad.value" @ver-pedido="verPedido" />
    </template>

    <template #introduccion>
      <p class="eyebrow">Catálogo completo</p>
      <h1 id="catalogo-titulo">Todos nuestros productos</h1>
      <div class="ornament" aria-hidden="true"><span></span></div>
      <p class="lead">
        Cosmética botánica artesanal elaborada en Ecuador. Busca por nombre o ingrediente,
        filtra por categoría y arma tu pedido: te llega a WhatsApp con la lista y el total.
      </p>
      <ul v-if="estado === 'listo'" class="facts">
        <li><strong>{{ productos.length }}</strong> productos</li>
        <li>Desde <strong>{{ formatoDinero(precioMinimo) }}</strong></li>
        <li><BaseIcon nombre="hoja" />Ingredientes de origen natural</li>
      </ul>
    </template>

    <template #herramientas>
      <CatalogToolbar
        v-if="estado === 'listo'"
        v-model:busqueda="busqueda" v-model:grupo="grupo"
        :grupos="grupos" :visibles="visibles.length" :total="productos.length"
      />
    </template>

    <p v-if="estado === 'cargando'" class="state" aria-busy="true">Cargando productos…</p>
    <div v-else-if="estado === 'error'" class="state">
      <p>No pudimos cargar el catálogo. Revisa tu conexión e inténtalo de nuevo.</p>
      <div class="state-actions">
        <BaseButton @click="cargar">Reintentar</BaseButton>
        <BaseButton variante="wa" :href="`https://wa.me/${WHATSAPP}`" externo><BaseIcon nombre="whatsapp" />Escríbenos</BaseButton>
      </div>
    </div>
    <ProductGrid v-else :productos="visibles" @agregar="agregar" @ver="verProducto">
      <template #vacio>
        <p>No encontramos productos<template v-if="busqueda"> con «{{ busqueda }}»</template><template v-if="grupo !== 'Todos'"> en {{ grupo }}</template>.</p>
        <BaseButton variante="ghost" @click="limpiarFiltros">Ver todos los productos</BaseButton>
      </template>
    </ProductGrid>

    <template #pie>
      <CatalogFooter :marca="marca" :whatsapp="whatsapp" />
    </template>

    <template #capas>
      <OrderBar :cantidad="pedido.cantidad.value" :total="pedido.total.value" @ver="verPedido" />
      <ProductDialog
        ref="ficha" :producto="seleccionado" :marca="marca" :whatsapp="whatsapp" :anuncio="mensaje"
        @agregar="agregar"
      />
      <OrderDialog
        ref="pedidoDialogo" :lineas="pedido.lineas.value" :total="pedido.total.value"
        :marca="marca" :whatsapp="whatsapp" :anuncio="mensaje" @cambiar="cambiarLinea" @vaciar="vaciar"
      />
      <p class="visually-hidden" aria-live="polite">{{ mensaje }}</p>
    </template>
  </CatalogTemplate>
</template>

<style scoped>
.eyebrow {
  font-size: 0.8125rem;
  font-weight: 500;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--gold-text);
}
h1 { font-size: clamp(2.6rem, 1.8rem + 3.2vw, 4.4rem); margin-block: 0.5rem 0.9rem; }
.ornament { display: flex; align-items: center; gap: 0.75rem; color: var(--gold); inline-size: min(100%, 14rem); }
.ornament::before, .ornament::after { content: ""; flex: 1; border-block-start: 1px solid currentColor; }
.ornament span { inline-size: 0.45rem; block-size: 0.45rem; rotate: 45deg; background: currentColor; }
.lead { margin-block-start: 1rem; max-inline-size: 60ch; color: var(--ink-soft); font-size: 1.1rem; }
.facts { list-style: none; display: flex; flex-wrap: wrap; gap: 0.6rem; margin-block-start: 1.5rem; }
.facts li {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.35rem 0.9rem;
  border: 1px solid var(--gold);
  border-radius: 999px;
  font-size: 0.9rem;
  color: var(--gold-text);
}
.facts strong { font-family: var(--font-display); font-size: 1.2rem; font-weight: 600; color: var(--ink); }
.facts :deep(svg) { inline-size: 1rem; block-size: 1rem; }
.state { display: grid; gap: 1rem; justify-items: start; padding-block: 2rem; color: var(--ink-soft); }
.state-actions { display: flex; flex-wrap: wrap; gap: 0.75rem; }
</style>
