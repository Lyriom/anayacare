<script setup>
// Átomo: precio en dólares con el formato de Ecuador ($12,90).
import { computed } from 'vue'
import { formatoDinero } from '../../utils/formato.js'

const props = defineProps({
  valor: { type: Number, required: true },
  /** m | l */
  tamano: { type: String, default: 'm' },
})
const texto = computed(() => formatoDinero(props.valor))
</script>

<template>
  <span :class="['price', `price-${tamano}`]">{{ texto }}</span>
</template>

<style scoped>
.price {
  font-family: var(--font-display);
  font-weight: 600;
  line-height: 1;
  color: var(--ink);
  font-variant-numeric: lining-nums;
}
.price-m { font-size: 1.6rem; }
.price-l { font-size: 2.2rem; }
</style>
