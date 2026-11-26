<script setup>
// Organismo: ficha del producto en un <dialog> modal (fotos, ingredientes, uso, precauciones y compra).
import { computed, useId } from 'vue'
import { useModal } from '../../composables/useModal.js'
import { enlaceWhatsApp, formatoDinero } from '../../utils/formato.js'
import BaseButton from '../atoms/BaseButton.vue'
import BaseIcon from '../atoms/BaseIcon.vue'
import CategoryTag from '../atoms/CategoryTag.vue'
import PriceTag from '../atoms/PriceTag.vue'
import RoundButton from '../atoms/RoundButton.vue'
import PhotoGallery from '../molecules/PhotoGallery.vue'
import ProductMedia from '../molecules/ProductMedia.vue'

const props = defineProps({
  producto: { type: Object, default: null },
  marca: { type: String, required: true },
  whatsapp: { type: String, required: true },
  /** Texto para lectores de pantalla: el resto de la página queda inerte mientras el modal está abierto. */
  anuncio: { type: String, default: '' },
})
const emit = defineEmits(['agregar'])

const { dialogo, abrir: mostrar } = useModal()
const abrir = () => {
  if (dialogo.value) dialogo.value.scrollTop = 0
  mostrar()
}
defineExpose({ abrir })

const titulo = useId()
const consulta = computed(() => props.producto && enlaceWhatsApp(
  props.whatsapp,
  `Hola ${props.marca}, quisiera consultar por: ${props.producto.nombre} (${formatoDinero(props.producto.precio)}).`,
))
</script>

<template>
  <dialog ref="dialogo" class="sheet" closedby="any" :aria-labelledby="titulo">
    <template v-if="producto">
      <form method="dialog" class="close">
        <RoundButton etiqueta="Cerrar" type="submit" value="cerrar">×</RoundButton>
      </form>
      <div class="layout">
        <PhotoGallery v-if="producto.fotos.length" :key="producto.id" :fotos="producto.fotos" />
        <div v-else class="sin-fotos"><ProductMedia :producto="producto" /></div>

        <div class="body">
          <header>
            <CategoryTag :texto="producto.categoria" />
            <h1 :id="titulo">{{ producto.nombre }}</h1>
            <p v-if="producto.lema" class="lema">{{ producto.lema }}</p>
          </header>
          <p v-if="producto.descripcion" class="desc">{{ producto.descripcion }}</p>

          <section>
            <h2>Ingredientes</h2>
            <p>{{ producto.ingredientes }}</p>
            <p v-if="producto.inci" class="inci">INCI: {{ producto.inci }}</p>
          </section>
          <section v-if="producto.uso?.length">
            <h2>Modo de uso</h2>
            <ol class="list"><li v-for="paso in producto.uso" :key="paso">{{ paso }}</li></ol>
          </section>
          <section v-if="producto.precauciones?.length">
            <h2>Precauciones</h2>
            <ul class="list"><li v-for="nota in producto.precauciones" :key="nota">{{ nota }}</li></ul>
          </section>
          <p v-if="!producto.uso?.length || !producto.precauciones?.length" class="nota">Las indicaciones que faltan no se distinguen o no figuran en las fotografías disponibles. Consulta la etiqueta o escríbenos para confirmarlas.</p>
          <p v-if="!producto.destacado" class="nota">Producto bajo pedido: lo preparamos en lotes pequeños y te confirmamos el tiempo de preparación por WhatsApp.</p>

          <div class="buy">
            <PriceTag :valor="producto.precio" tamano="l" />
            <BaseButton variante="gold" @click="emit('agregar', producto)">Agregar al pedido</BaseButton>
            <BaseButton variante="ghost" :href="consulta" externo>
              <BaseIcon nombre="whatsapp" />Consultar por WhatsApp
            </BaseButton>
          </div>
        </div>
      </div>
    </template>
    <p class="visually-hidden" aria-live="polite">{{ anuncio }}</p>
  </dialog>
</template>

<style scoped>
.close { position: sticky; inset-block-start: 0; z-index: 2; block-size: 0; }
.close :deep(.round) { position: absolute; inset-block-start: 0.75rem; inset-inline-end: 0.75rem; }
.layout { display: grid; align-items: start; }
@media (min-width: 52rem) {
  .layout { grid-template-columns: minmax(0, 1fr) minmax(0, 1.05fr); }
}
.sin-fotos { padding: 0.5rem; background: var(--sand); }
.sin-fotos :deep(.media) { border-radius: var(--radius-s); }
.body { display: grid; gap: 1.1rem; align-content: start; padding: clamp(1.5rem, 1rem + 2vw, 2.5rem); }
h1 { font-size: clamp(2rem, 1.6rem + 1.5vw, 2.7rem); margin-block: 0.4rem 0.25rem; padding-inline-end: 2.5rem; }
.lema { font-family: var(--font-display); font-style: italic; font-size: 1.25rem; color: var(--rose-ink); }
.desc { color: var(--ink-soft); }
h2 {
  font-family: var(--font-body);
  font-size: 0.8125rem;
  font-weight: 600;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--gold-text);
  margin-block-end: 0.6rem;
}
section p, section li { color: var(--ink-soft); }
.list { display: grid; gap: 0.35rem; padding-inline-start: 1.25rem; }
.inci { font-size: 0.9rem; margin-block-start: 0.6rem; }
.nota { font-size: 0.925rem; color: var(--ink-soft); padding: 0.85rem 1rem; border-inline-start: 2px solid var(--gold); background: var(--white); }
.buy {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.9rem;
  padding: 1.25rem;
  border: 1px solid var(--line);
  border-radius: var(--radius-m);
  background: var(--white);
}
.buy .price { flex: 1 1 100%; }
.buy :deep(.btn) { flex: 1 1 12rem; }
</style>
