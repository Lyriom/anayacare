<script setup>
// Una imagen principal y botones para alternar las vistas de la etiqueta.
import { ref, watch } from 'vue'
import ProductPicture from '../atoms/ProductPicture.vue'
import { srcFoto } from '../../utils/formato.js'

const props = defineProps({ fotos: { type: Array, required: true } })
const activa = ref(0)
watch(() => props.fotos, () => { activa.value = 0 })
</script>

<template>
  <div class="gallery">
    <figure class="main-photo">
      <ProductPicture
        :slug="fotos[activa].slug" :alt="fotos[activa].alt"
        sizes="(min-width: 52rem) 29rem, 90vw" carga="eager" prioridad="low"
      />
      <figcaption>{{ fotos[activa].etiqueta }}</figcaption>
    </figure>
    <div v-if="fotos.length > 1" class="views" role="group" aria-label="Vistas del producto">
      <button
        v-for="(foto, i) in fotos" :key="foto.slug" type="button"
        class="view" :aria-pressed="i === activa" @click="activa = i"
      >
        <img :src="srcFoto(foto.slug, 480)" alt="" width="480" height="600" loading="lazy" fetchpriority="low">
        <span>{{ foto.etiqueta }}</span>
      </button>
    </div>
  </div>
</template>

<style scoped>
.gallery {
  display: grid;
  gap: 0.9rem;
  align-content: start;
  padding: 1.25rem;
  min-inline-size: 0;
  background: #f1e7db;
}
.main-photo {
  position: relative;
  display: grid;
  margin: 0;
  block-size: clamp(15rem, 42dvh, 26rem);
  min-inline-size: 0;
  overflow: hidden;
  border-radius: 0.75rem;
  background: #f8e9d9;
}
.main-photo :deep(picture) { display: block; min-block-size: 0; }
.main-photo :deep(img) { inline-size: 100%; block-size: 100%; aspect-ratio: auto; object-fit: contain; }
figcaption {
  position: absolute;
  inset-inline-start: 0.75rem;
  inset-block-end: 0.75rem;
  padding: 0.3rem 0.7rem;
  border-radius: 999px;
  background: rgb(255 253 249 / 0.94);
  color: var(--ink-soft);
  font-size: 0.8rem;
}
.views { display: flex; flex-wrap: wrap; gap: 0.6rem; }
.view {
  display: flex;
  align-items: center;
  gap: 0.55rem;
  min-block-size: 3.5rem;
  padding: 0.3rem 0.75rem 0.3rem 0.3rem;
  border: 1px solid var(--line);
  border-radius: 0.7rem;
  background: rgb(255 253 249 / 0.8);
  color: var(--ink);
  font: inherit;
  font-size: 0.85rem;
  cursor: pointer;
}
.view img { inline-size: 2.5rem; block-size: 2.75rem; object-fit: contain; border-radius: 0.4rem; background: #f8e9d9; }
.view[aria-pressed="true"] { border-color: var(--gold-text); box-shadow: 0 0 0 1px var(--gold-text); background: #fffdf9; }
.view:focus-visible { outline: 2px solid var(--gold-text); outline-offset: 3px; }
@media (min-width: 52rem) {
  .gallery { position: sticky; top: 0; align-self: start; padding: 1.5rem; }
}
@media (max-width: 40rem) {
  .gallery { padding: 1rem; }
  .main-photo { block-size: clamp(13rem, 36dvh, 20rem); }
}
</style>
