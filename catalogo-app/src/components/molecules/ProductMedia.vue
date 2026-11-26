<script setup>
// Molécula: la primera foto del producto o, si aún no tiene, una lámina con el icono de su grupo.
import { computed } from 'vue'
import BaseIcon from '../atoms/BaseIcon.vue'
import ProductPicture from '../atoms/ProductPicture.vue'

const ICONO_POR_GRUPO = {
  'Rostro y mirada': 'rostro',
  'Cabello y barba': 'cabello',
  Jabones: 'jabones',
  Labios: 'labios',
  Bienestar: 'bienestar',
}

const props = defineProps({
  producto: { type: Object, required: true },
  sizes: { type: String, default: undefined },
  carga: { type: String, default: 'lazy' },
})
const foto = computed(() => props.producto.fotos[0])
const icono = computed(() => ICONO_POR_GRUPO[props.producto.grupo] ?? 'hoja')
</script>

<template>
  <div class="media">
    <ProductPicture v-if="foto" :slug="foto.slug" :alt="foto.alt" :sizes="sizes" :carga="carga" />
    <div v-else class="lamina" aria-hidden="true">
      <span class="sello"><BaseIcon :nombre="icono" /></span>
      <span class="nombre">{{ producto.nombre }}</span>
      <span class="hecho">Hecho a mano</span>
    </div>
  </div>
</template>

<style scoped>
.media { border-radius: inherit; overflow: clip; }
.lamina {
  display: grid;
  place-content: center;
  justify-items: center;
  gap: 0.75rem;
  aspect-ratio: 4 / 5;
  padding: 1.5rem;
  text-align: center;
  background:
    radial-gradient(120% 80% at 50% 0%, #fff9ee 0%, transparent 60%),
    linear-gradient(160deg, var(--paper), var(--sand));
  outline: 1px solid rgb(184 141 59 / 0.45);
  outline-offset: -0.6rem;
  border-radius: inherit;
}
.sello {
  display: grid;
  place-items: center;
  inline-size: 4.5rem;
  block-size: 4.5rem;
  border: 1px solid var(--gold);
  border-radius: 50%;
  color: var(--gold-text);
  background: rgb(255 253 249 / 0.7);
}
.sello :deep(svg) { inline-size: 2rem; block-size: 2rem; }
.nombre {
  font-family: var(--font-display);
  font-size: 1.45rem;
  line-height: 1.15;
  color: var(--ink);
  text-wrap: balance;
  max-inline-size: 14ch;
}
.hecho { font-size: 0.7rem; letter-spacing: 0.2em; text-transform: uppercase; color: var(--gold-text); }
</style>
