<script setup>
// Átomo: botón circular con un símbolo (×, −, +) y nombre accesible.
defineProps({
  /** Texto para lectores de pantalla, por ejemplo «Cerrar». */
  etiqueta: { type: String, required: true },
  type: { type: String, default: 'button' },
  value: { type: String, default: null },
})
</script>

<template>
  <button class="round" :type="type" :value="value" :aria-label="etiqueta">
    <span aria-hidden="true"><slot /></span>
  </button>
</template>

<style scoped>
.round {
  display: grid;
  place-items: center;
  inline-size: 2.75rem;
  block-size: 2.75rem;
  padding: 0;
  border: 1px solid var(--line);
  border-radius: 50%;
  background: rgb(255 253 249 / 0.94);
  font-size: 1.35rem;
  line-height: 1;
  cursor: pointer;
}
.round:hover { border-color: var(--gold); background: #fff; }
@media (forced-colors: active) {
  .round { border-color: ButtonText; }
}
</style>
