<script setup>
// Molécula: una línea del pedido (nombre, precio unitario, cantidad y subtotal).
import { formatoDinero } from '../../utils/formato.js'
import PriceTag from '../atoms/PriceTag.vue'
import QuantityStepper from './QuantityStepper.vue'

defineProps({
  /** { id, name, price, qty } — misma forma que guarda la página principal. */
  linea: { type: Object, required: true },
})
const emit = defineEmits(['cambiar'])
</script>

<template>
  <li class="line">
    <div>
      <p class="name">{{ linea.name }}</p>
      <p class="unit">{{ formatoDinero(linea.price) }} c/u</p>
    </div>
    <PriceTag :valor="linea.price * linea.qty" class="subtotal" />
    <QuantityStepper :cantidad="linea.qty" :nombre="linea.name" @cambiar="(d) => emit('cambiar', d)" />
  </li>
</template>

<style scoped>
.line {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 0.5rem 1rem;
  align-items: center;
  padding: 0.9rem 1rem;
  border: 1px solid var(--line);
  border-radius: var(--radius-m);
  background: var(--white);
}
.name { font-weight: 500; }
.unit { font-size: 0.85rem; color: var(--ink-soft); }
.subtotal { font-size: 1.35rem; text-align: end; }
</style>
