<script setup>
// Átomo: foto de producto responsive (AVIF → WebP → JPEG, 480/800/1200 px).
import { srcFoto, srcsetFoto } from '../../utils/formato.js'

defineProps({
  slug: { type: String, required: true },
  alt: { type: String, required: true },
  /** Ancho que ocupará la imagen, para que el navegador elija el archivo adecuado. */
  sizes: { type: String, default: '(min-width: 76rem) 17rem, (min-width: 36rem) 45vw, 92vw' },
  carga: { type: String, default: 'lazy' },
})
</script>

<template>
  <picture>
    <source v-if="['pestanas-frente', 'pestanas-reverso', 'serum-hialuronico-frente', 'serum-hialuronico-reverso', 'protector-termico-frente', 'protector-termico-uso', 'protector-termico-precauciones', 'capilar-barba-frente', 'capilar-barba-reverso'].includes(slug)" type="image/avif" :srcset="srcsetFoto(slug, 'avif')" :sizes="sizes">
    <source type="image/webp" :srcset="srcsetFoto(slug, 'webp')" :sizes="sizes">
    <img
      :src="srcFoto(slug)" :srcset="srcsetFoto(slug, 'jpg')" :sizes="sizes"
      :alt="alt" width="800" height="1000" :loading="carga" decoding="async"
    >
  </picture>
</template>

<style scoped>
img { inline-size: 100%; aspect-ratio: 4 / 5; object-fit: contain; background: #f8e9d9; border-radius: inherit; }
</style>
