<script setup>
// Organismo: barra flotante con el resumen del pedido.
import BaseButton from '../atoms/BaseButton.vue'
import PriceTag from '../atoms/PriceTag.vue'

defineProps({
  cantidad: { type: Number, required: true },
  total: { type: Number, required: true },
})
const emit = defineEmits(['ver'])
</script>

<template>
  <div v-if="cantidad > 0" class="bar">
    <p>
      <span class="visually-hidden">Tu pedido: </span>
      {{ cantidad }} {{ cantidad === 1 ? 'producto' : 'productos' }} ·
      <PriceTag :valor="total" class="total" />
    </p>
    <BaseButton variante="light" @click="emit('ver')">Ver pedido</BaseButton>
  </div>
</template>

<style scoped>
.bar {
  position: fixed;
  z-index: 16;
  inset-inline: max(0.75rem, env(safe-area-inset-left)) max(0.75rem, env(safe-area-inset-right));
  inset-block-end: max(0.75rem, env(safe-area-inset-bottom));
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem 1rem;
  max-inline-size: 40rem;
  margin-inline: auto;
  padding: 0.65rem 0.65rem 0.65rem 1.25rem;
  border-radius: 999px;
  background: var(--ink);
  color: var(--ivory);
  box-shadow: 0 18px 40px -14px rgb(43 36 32 / 0.6);
}
p { font-size: 0.95rem; min-inline-size: 0; }
.total { font-size: 1.35rem; color: var(--gold-light); }
</style>
