<script setup>
// Molécula: todas las fotos de un producto; la primera grande y el resto en mosaico.
import ProductPicture from '../atoms/ProductPicture.vue'

defineProps({
  /** [{ slug, alt, etiqueta }] */
  fotos: { type: Array, required: true },
})
const SIZES_GRANDE = '(min-width: 62rem) 29rem, (min-width: 52rem) 46vw, 92vw'
const SIZES_MINI = '(min-width: 62rem) 14rem, (min-width: 52rem) 23vw, 46vw'
</script>

<template>
  <div :class="['gallery', { pair: fotos.length === 2 }]">
    <figure v-for="(foto, i) in fotos" :key="foto.slug">
      <ProductPicture
        :slug="foto.slug" :alt="foto.alt"
        :sizes="i === 0 || fotos.length === 2 ? SIZES_GRANDE : SIZES_MINI"
        :carga="i === 0 ? 'eager' : 'lazy'"
      />
      <figcaption>{{ foto.etiqueta }}</figcaption>
    </figure>
  </div>
</template>

<style scoped>
.gallery {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
  padding: 0.5rem;
  background: var(--sand);
  align-content: start;
}
figure { margin: 0; position: relative; border-radius: var(--radius-s); overflow: hidden; }
figure:first-child, .pair figure { grid-column: 1 / -1; }
figcaption {
  position: absolute;
  inset-inline-start: 0.5rem;
  inset-block-end: 0.5rem;
  padding: 0.25rem 0.7rem;
  border-radius: 999px;
  background: rgb(255 253 249 / 0.9);
  font-size: 0.78rem;
  color: var(--ink-soft);
}
</style>
