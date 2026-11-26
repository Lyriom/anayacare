<script setup>
// Molécula: botones − y + con la cantidad en medio.
import RoundButton from '../atoms/RoundButton.vue'

defineProps({
  cantidad: { type: Number, required: true },
  nombre: { type: String, required: true },
})
const emit = defineEmits(['cambiar'])
</script>

<template>
  <div class="qty">
    <RoundButton :etiqueta="`Quitar una unidad de ${nombre}`" @click="emit('cambiar', -1)">−</RoundButton>
    <output :aria-label="`Cantidad de ${nombre}`">{{ cantidad }}</output>
    <RoundButton :etiqueta="`Agregar una unidad de ${nombre}`" @click="emit('cambiar', 1)">+</RoundButton>
  </div>
</template>

<style scoped>
.qty { display: inline-flex; align-items: center; gap: 0.25rem; }
output { min-inline-size: 2ch; text-align: center; font-weight: 600; font-variant-numeric: tabular-nums; }
</style>
