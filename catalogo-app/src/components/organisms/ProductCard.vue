<script setup>
// Organismo: tarjeta de producto (foto, categoría, nombre, descripción, precio y acciones).
import { onBeforeUnmount, ref } from 'vue'
import BaseButton from '../atoms/BaseButton.vue'
import CategoryTag from '../atoms/CategoryTag.vue'
import PriceTag from '../atoms/PriceTag.vue'
import ProductMedia from '../molecules/ProductMedia.vue'

const props = defineProps({
  producto: { type: Object, required: true },
  /** La primera fila se carga sin lazy para no retrasar lo que se ve al abrir. */
  carga: { type: String, default: 'lazy' },
})
const emit = defineEmits(['agregar', 'ver'])

// Confirmación visual breve después de agregar.
const agregado = ref(false)
let temporizador
function agregar() {
  emit('agregar', props.producto)
  agregado.value = true
  clearTimeout(temporizador)
  temporizador = setTimeout(() => { agregado.value = false }, 1600)
}
onBeforeUnmount(() => clearTimeout(temporizador))
</script>

<template>
  <article class="card">
    <button type="button" class="media-button" @click="emit('ver', producto)">
      <ProductMedia :producto="producto" :carga="carga" />
      <span v-if="['shampoo', 'jabon-cafe'].includes(producto.id)" class="badge">Ilustración</span>
      <span v-else-if="producto.fotos.length > 1" class="badge">{{ producto.fotos.length }} fotos</span>
      <span class="visually-hidden">Ver detalle de {{ producto.nombre }}</span>
    </button>
    <div class="body">
      <CategoryTag :texto="producto.categoria" />
      <h3>{{ producto.nombre }}</h3>
      <p class="desc">{{ producto.lema ?? producto.ingredientes }}</p>
    </div>
    <footer>
      <PriceTag :valor="producto.precio" />
      <div class="actions">
        <BaseButton variante="ghost" @click="emit('ver', producto)">
          Detalle<span class="visually-hidden"> de {{ producto.nombre }}</span>
        </BaseButton>
        <BaseButton :variante="producto.destacado ? 'gold' : 'primary'" :hecho="agregado" @click="agregar">
          {{ agregado ? 'Agregado ✓' : 'Agregar' }}<span class="visually-hidden"> {{ producto.nombre }} al pedido</span>
        </BaseButton>
      </div>
    </footer>
  </article>
</template>

<style scoped>
.card {
  container-type: inline-size;
  display: grid;
  grid-template-rows: subgrid;
  grid-row: span 3;
  row-gap: 0.9rem;
  block-size: 100%;
  padding: 0.75rem 0.75rem 1.1rem;
  background: var(--white);
  border: 1px solid var(--line);
  border-radius: var(--radius-m);
  transition: border-color 0.2s ease;
}
.card:hover { border-color: var(--gold); }
.media-button {
  position: relative;
  display: block;
  padding: 0;
  border: 0;
  border-radius: calc(var(--radius-m) - 0.4rem);
  background: none;
  cursor: zoom-in;
  overflow: clip;
}
.media-button :deep(img) { transition: scale 0.5s ease; }
@media (prefers-reduced-motion: no-preference) {
  .media-button:hover :deep(img) { scale: 1.03; }
}
.badge {
  position: absolute;
  inset-inline-end: 0.6rem;
  inset-block-end: 0.6rem;
  padding: 0.2rem 0.65rem;
  border-radius: 999px;
  background: rgb(255 253 249 / 0.92);
  font-size: 0.75rem;
  color: var(--ink-soft);
}
.body { display: grid; gap: 0.35rem; align-content: start; padding-inline: 0.35rem; }
h3 { font-size: 1.55rem; font-weight: 600; }
.desc { font-size: 0.925rem; color: var(--ink-soft); }
footer {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  padding-inline: 0.35rem;
  align-self: end;
}
.actions { display: flex; gap: 0.5rem; }
@container (width < 17rem) {
  .actions { inline-size: 100%; }
  .actions > * { flex: 1; }
}
</style>
