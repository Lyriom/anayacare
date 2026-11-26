<script setup>
// Organismo: buscador + filtro por categoría + resultado, dentro de <search>.
import CategoryFilter from '../molecules/CategoryFilter.vue'
import SearchField from '../molecules/SearchField.vue'

const busqueda = defineModel('busqueda', { type: String, default: '' })
const grupo = defineModel('grupo', { type: String, required: true })
defineProps({
  grupos: { type: Array, required: true },
  visibles: { type: Number, required: true },
  total: { type: Number, required: true },
})
</script>

<template>
  <search class="toolbar" aria-label="Buscar y filtrar productos">
    <SearchField v-model="busqueda" etiqueta="Buscar producto o ingrediente" ayuda="Ej.: romero, jabón, ácido hialurónico" />
    <CategoryFilter v-model="grupo" :opciones="grupos" />
    <p class="result" role="status">
      <template v-if="visibles === total">{{ total }} productos</template>
      <template v-else>{{ visibles }} de {{ total }} productos</template>
    </p>
  </search>
</template>

<style scoped>
.toolbar {
  display: grid;
  gap: 1.25rem;
  padding: 1.25rem;
  border: 1px solid var(--line);
  border-radius: var(--radius-m);
  background: rgb(255 253 249 / 0.7);
}
@media (min-width: 60rem) {
  .toolbar { grid-template-columns: minmax(16rem, 22rem) 1fr; align-items: end; }
  .result { grid-column: 1 / -1; }
}
.result { font-size: 0.9rem; color: var(--ink-soft); }
</style>
