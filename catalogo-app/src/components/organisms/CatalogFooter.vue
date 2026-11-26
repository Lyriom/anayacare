<script setup>
// Organismo: pie de página con enlaces al sitio principal y contacto.
import { computed } from 'vue'
import { enlaceWhatsApp } from '../../utils/formato.js'

const props = defineProps({
  marca: { type: String, required: true },
  whatsapp: { type: String, required: true },
})
const telefono = computed(() => props.whatsapp.replace(/^(\d{3})(\d{2})(\d{3})(\d{4})$/, '+$1 $2 $3 $4'))
const enlace = computed(() => enlaceWhatsApp(props.whatsapp, `Hola ${props.marca}`))
</script>

<template>
  <footer class="footer">
    <div class="inner">
      <p class="brand">{{ marca }} <span>· Equilibrio · Ritual · Bienestar</span></p>
      <ul>
        <li><a href="../">Página principal</a></li>
        <li><a href="../#nosotros">Nosotros</a></li>
        <li><a href="../privacidad.html">Política de privacidad</a></li>
        <li><a :href="enlace" target="_blank" rel="noopener">WhatsApp {{ telefono }}</a></li>
      </ul>
      <p class="note">© 2026 {{ marca }}. Cosmética artesanal elaborada en Ecuador. Precios en dólares (USD); el envío se coordina por WhatsApp.</p>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  margin-block-start: clamp(3rem, 2rem + 4vw, 5rem);
  padding-block: 2.5rem 7rem;
  border-block-start: 1px solid var(--line);
  color: var(--ink-soft);
  font-size: 0.95rem;
}
.inner { display: grid; gap: 1rem; inline-size: min(100% - 2 * var(--gutter), var(--content)); margin-inline: auto; }
.brand { font-family: var(--font-display); font-size: 1.5rem; color: var(--gold-text); }
.brand span { font-family: var(--font-body); font-size: 0.8rem; letter-spacing: 0.14em; text-transform: uppercase; color: var(--ink-soft); }
ul { list-style: none; display: flex; flex-wrap: wrap; gap: 0.5rem 1.5rem; }
a { text-underline-offset: 0.25em; }
a:hover { color: var(--ink); }
.note { font-size: 0.875rem; padding-block-start: 1rem; border-block-start: 1px solid var(--line); }
</style>
