<script setup>
// Organismo: encabezado fijo con logo, navegación y acceso al pedido.
import BaseButton from '../atoms/BaseButton.vue'
import BaseIcon from '../atoms/BaseIcon.vue'
import BrandLogo from '../atoms/BrandLogo.vue'

defineProps({
  marca: { type: String, default: 'Anaya Co.' },
  /** Número de unidades en el pedido. */
  cantidad: { type: Number, default: 0 },
})
const emit = defineEmits(['ver-pedido'])
</script>

<template>
  <header class="header">
    <div class="inner">
      <BrandLogo :marca="marca" />
      <nav aria-label="Principal">
        <ul>
          <li><a href="../">Inicio</a></li>
          <li><a href="./" aria-current="page">Catálogo</a></li>
          <li><a href="../#contacto">Contacto</a></li>
        </ul>
      </nav>
      <BaseButton variante="ghost" class="cart" @click="emit('ver-pedido')">
        <BaseIcon nombre="bolsa" />
        <span>Pedido</span>
        <span class="count" :data-empty="cantidad === 0 || null">{{ cantidad }}</span>
        <span class="visually-hidden">{{ cantidad === 1 ? 'producto' : 'productos' }}</span>
      </BaseButton>
    </div>
  </header>
</template>

<style scoped>
.header {
  position: sticky;
  inset-block-start: 0;
  z-index: 10;
  background: rgb(250 248 243 / 0.9);
  backdrop-filter: blur(12px);
  border-block-end: 1px solid rgb(228 216 197 / 0.8);
}
.inner {
  display: flex;
  align-items: center;
  gap: 0.75rem 1.5rem;
  inline-size: min(100% - 2 * var(--gutter), var(--content));
  margin-inline: auto;
  padding-block: 0.6rem;
}
nav { margin-inline-start: auto; }
ul { list-style: none; display: flex; gap: 1.5rem; }
nav a { font-weight: 500; font-size: 0.975rem; text-decoration: none; text-underline-offset: 0.35em; }
nav a:hover, nav a[aria-current="page"] { text-decoration: underline; text-decoration-color: var(--gold); text-decoration-thickness: 2px; }
.count {
  display: grid;
  place-items: center;
  min-inline-size: 1.5rem;
  block-size: 1.5rem;
  padding-inline: 0.35rem;
  border-radius: 999px;
  background: var(--gold-text);
  color: #fff;
  font-size: 0.8rem;
  font-variant-numeric: tabular-nums;
}
.count[data-empty] { background: var(--sand); color: var(--ink-soft); }

/* En pantallas angostas solo quedan el logo, «Inicio» y el pedido. */
@media (width < 40rem) {
  nav li:not(:first-child) { display: none; }
  .cart > span:not(.count) { display: none; }
  .cart { padding-inline: 0.85rem; }
}
@media (width < 22rem) {
  :deep(.wordmark) { display: none; }
}
</style>
