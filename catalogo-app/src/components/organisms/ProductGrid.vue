<script setup>
// Organismo: cuadrícula de tarjetas. Si no hay resultados muestra el contenido del slot «vacio».
import ProductCard from './ProductCard.vue'

defineProps({
  productos: { type: Array, required: true },
})
const emit = defineEmits(['agregar', 'ver'])
</script>

<template>
  <ul v-if="productos.length" class="grid">
    <li v-for="(producto, i) in productos" :key="producto.id">
      <ProductCard
        :producto="producto" :carga="i < 4 ? 'eager' : 'lazy'"
        @agregar="(p) => emit('agregar', p)" @ver="(p) => emit('ver', p)"
      />
    </li>
  </ul>
  <div v-else class="empty">
    <slot name="vacio" />
  </div>
</template>

<style scoped>
.grid {
  list-style: none;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(min(100%, 16.5rem), 1fr));
  gap: 1.5rem;
}
/* Subgrid: foto, texto y precio quedan alineados entre tarjetas de la misma fila. */
.grid > li { display: grid; grid-template-rows: subgrid; grid-row: span 3; }
.empty {
  display: grid;
  justify-items: center;
  gap: 1rem;
  padding: 3rem 1.5rem;
  text-align: center;
  border: 1px dashed var(--line);
  border-radius: var(--radius-m);
  color: var(--ink-soft);
}
</style>
