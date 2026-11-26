<script setup>
// Átomo: botón o enlace con aspecto de botón. Sin estado propio.
defineProps({
  /** primary | gold | wa | ghost | light */
  variante: { type: String, default: 'primary' },
  /** Si tiene href se dibuja como enlace <a>. */
  href: { type: String, default: null },
  /** Abre el enlace en otra pestaña (WhatsApp). */
  externo: { type: Boolean, default: false },
  /** Estado de confirmación breve (por ejemplo, «Agregado ✓»). */
  hecho: { type: Boolean, default: false },
})
</script>

<template>
  <a
    v-if="href"
    :href="href"
    :class="['btn', `btn-${variante}`]"
    :target="externo ? '_blank' : null"
    :rel="externo ? 'noopener' : null"
  ><slot /></a>
  <button v-else type="button" :class="['btn', `btn-${variante}`, { 'is-done': hecho }]"><slot /></button>
</template>

<style scoped>
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  min-block-size: 2.75rem;
  padding: 0.6rem 1.25rem;
  border: 1px solid transparent;
  border-radius: 999px;
  font: 500 0.9375rem/1.2 var(--font-body);
  letter-spacing: 0.02em;
  text-decoration: none;
  text-align: center;
  cursor: pointer;
  transition: background-color 0.2s ease, color 0.2s ease, border-color 0.2s ease;
}
.btn :deep(svg) { inline-size: 1.15em; block-size: 1.15em; flex: none; }
.btn-primary { background: var(--ink); color: var(--ivory); }
.btn-primary:hover { background: #4a3d35; }
.btn-gold { background: var(--gold-text); color: #fff; }
.btn-gold:hover { background: #6f4f17; }
.btn-wa { background: var(--wa); color: #fff; }
.btn-wa:hover { background: var(--wa-hover); }
.btn-ghost { background: transparent; color: var(--ink); border-color: var(--line); }
.btn-ghost:hover { border-color: var(--gold); background: var(--white); }
.btn-light { background: var(--gold-light); color: var(--ink); }
.btn-light:hover { background: #e7c788; }
.btn.is-done { background: var(--sage-ink); border-color: var(--sage-ink); color: #fff; }

@media (forced-colors: active) {
  .btn { border-color: ButtonText; }
}
</style>
