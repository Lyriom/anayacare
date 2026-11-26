<script setup>
// Átomo: etiqueta de categoría en mayúsculas doradas.
defineProps({
  texto: { type: String, required: true },
})
</script>

<template>
  <p class="tag">{{ texto }}</p>
</template>

<style scoped>
.tag {
  font-size: 0.75rem;
  font-weight: 500;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--gold-text);
}
</style>
