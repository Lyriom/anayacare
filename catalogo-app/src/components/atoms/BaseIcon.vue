<script setup>
// Átomo: icono SVG decorativo. Los trazos son los mismos del sitio principal (tools/iconos.py).
import { computed } from 'vue'

const ICONOS = {
  whatsapp: '<path d="M12 3a9 9 0 0 0-7.8 13.5L3 21l4.6-1.2A9 9 0 1 0 12 3z"/><path d="M9.1 8.2c.3-.3.8-.3 1 .1l.8 1.4c.2.3.1.7-.1.9l-.5.5a6 6 0 0 0 2.6 2.6l.5-.5c.2-.2.6-.3.9-.1l1.4.8c.4.2.4.7.1 1l-.6.6c-.5.5-1.3.7-2 .4a9 9 0 0 1-4.6-4.6c-.3-.7-.1-1.5.4-2z" fill="currentColor" stroke="none"/>',
  rostro: '<path d="M12 3c2.5 3.2 5 6 5 9a5 5 0 0 1-10 0c0-3 2.5-5.8 5-9z"/>',
  cabello: '<path d="M12 21V9"/><path d="M12 13c-3 0-5-2-5-5 3 0 5 2 5 5zM12 10c0-3 2-5 5-5 0 3-2 5-5 5zM12 17c3 0 5-2 5-5-3 0-5 2-5 5z"/>',
  jabones: '<rect x="3" y="9" width="18" height="10" rx="3"/><circle cx="8" cy="5" r="1.5"/><circle cx="13" cy="4" r="1"/><circle cx="17" cy="6" r="1.5"/>',
  labios: '<rect x="8" y="10" width="8" height="11" rx="1.5"/><path d="M9 10V6l6-3v7"/>',
  bienestar: '<path d="M12 3c1.5 2 2.5 3.5 2.5 5a2.5 2.5 0 0 1-5 0c0-1.5 1-3 2.5-5z"/><rect x="6" y="12" width="12" height="9" rx="2"/>',
  hoja: '<path d="M5 19c0-8 5-13 15-14-1 10-6 15-14 15"/><path d="M5 19c3-4 6-7 10-9"/>',
  buscar: '<circle cx="11" cy="11" r="6.5"/><path d="m20 20-4.3-4.3"/>',
  bolsa: '<path d="M5.5 8h13l-1.2 12.5H6.7z"/><path d="M9 8V6.5a3 3 0 0 1 6 0V8"/>',
  atras: '<path d="M14.5 6 8.5 12l6 6"/>',
}

const props = defineProps({
  nombre: { type: String, required: true },
})
const trazos = computed(() => ICONOS[props.nombre] ?? ICONOS.hoja)
</script>

<template>
  <!-- eslint-disable-next-line vue/no-v-html -- trazos fijos definidos arriba, no vienen del usuario -->
  <svg
    viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"
    stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"
    v-html="trazos"
  />
</template>
