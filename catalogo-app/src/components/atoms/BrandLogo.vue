<script setup>
// Átomo: logotipo de Anaya Co. que enlaza a la página principal.
defineProps({
  marca: { type: String, default: 'Anaya Co.' },
  href: { type: String, default: '../' },
})
// Rutas en tiempo de ejecución (atributos enlazados): el logo ya está publicado en el sitio
// principal, así que Vite no debe copiarlo dentro del catálogo.
const EMBLEMA = '../img/marca/logo-emblema-128'
</script>

<template>
  <a class="logo" :href="href">
    <picture>
      <source type="image/webp" :srcset="`${EMBLEMA}.webp`">
      <img :src="`${EMBLEMA}.png`" alt="" width="120" height="128">
    </picture>
    <span class="wordmark">{{ marca }}</span>
    <span class="visually-hidden">: ir a la página principal</span>
  </a>
</template>

<style scoped>
.logo { display: inline-flex; align-items: center; gap: 0.6rem; text-decoration: none; }
img { inline-size: 2.1rem; block-size: auto; }
.wordmark {
  font-family: var(--font-display);
  font-size: 1.6rem;
  font-weight: 500;
  color: var(--gold-text);
  letter-spacing: 0.01em;
  white-space: nowrap;
}
</style>
