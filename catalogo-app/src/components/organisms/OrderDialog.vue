<script setup>
// Organismo: el pedido en un <dialog> modal, con envío de la lista por WhatsApp.
import { computed, nextTick, ref } from 'vue'
import { useModal } from '../../composables/useModal.js'
import { enlaceWhatsApp, formatoDinero } from '../../utils/formato.js'
import BaseButton from '../atoms/BaseButton.vue'
import BaseIcon from '../atoms/BaseIcon.vue'
import PriceTag from '../atoms/PriceTag.vue'
import RoundButton from '../atoms/RoundButton.vue'
import OrderLine from '../molecules/OrderLine.vue'

const props = defineProps({
  lineas: { type: Array, required: true },
  total: { type: Number, required: true },
  marca: { type: String, required: true },
  whatsapp: { type: String, required: true },
})
const emit = defineEmits(['cambiar', 'vaciar'])

const { dialogo, abrir } = useModal()
defineExpose({ abrir })
const titulo = ref(null)

// Mismo mensaje que arma la página principal.
const mensaje = computed(() => [
  `Hola ${props.marca}, quiero hacer este pedido:`,
  ...props.lineas.map((l) => `• ${l.qty} × ${l.name} — ${formatoDinero(l.price * l.qty)}`),
  `Total: ${formatoDinero(props.total)}`,
  '¿Me confirman disponibilidad, forma de pago y entrega?',
].join('\n'))
const enlace = computed(() => enlaceWhatsApp(props.whatsapp, mensaje.value))

// Si desaparece la línea que tenía el foco, se lleva el foco a un lugar estable.
async function cambiar(linea, delta) {
  emit('cambiar', linea, delta)
  if (linea.qty + delta <= 0) { await nextTick(); titulo.value?.focus() }
}
async function vaciar() {
  emit('vaciar')
  await nextTick()
  titulo.value?.focus()
}
</script>

<template>
  <dialog ref="dialogo" class="sheet narrow" closedby="any" aria-labelledby="pedido-titulo">
    <form method="dialog" class="close">
      <RoundButton etiqueta="Cerrar" type="submit" value="cerrar">×</RoundButton>
    </form>
    <div class="body">
      <h1 id="pedido-titulo" ref="titulo" tabindex="-1">Tu pedido</h1>
      <p v-if="!lineas.length" class="empty">Aún no has agregado productos.</p>
      <template v-else>
        <ul class="lines" aria-label="Productos del pedido">
          <OrderLine v-for="linea in lineas" :key="linea.id" :linea="linea" @cambiar="(d) => cambiar(linea, d)" />
        </ul>
        <p class="total">Total <PriceTag :valor="total" tamano="l" /></p>
      </template>
      <p class="note">El costo de envío y la forma de pago se coordinan por WhatsApp.</p>
      <div v-if="lineas.length" class="actions">
        <BaseButton variante="wa" :href="enlace" externo autofocus>
          <BaseIcon nombre="whatsapp" />Enviar pedido por WhatsApp
        </BaseButton>
        <button type="button" class="link" @click="vaciar">Vaciar pedido</button>
      </div>
    </div>
  </dialog>
</template>

<style scoped>
.close { position: sticky; inset-block-start: 0; z-index: 2; block-size: 0; }
.close :deep(.round) { position: absolute; inset-block-start: 0.75rem; inset-inline-end: 0.75rem; }
.body { display: grid; gap: 1.25rem; padding: clamp(1.5rem, 1rem + 2vw, 2.25rem); }
h1 { font-size: 2.2rem; padding-inline-end: 2.5rem; }
h1:focus { outline: none; }
.lines { list-style: none; display: grid; gap: 0.75rem; }
.total {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  padding-block-start: 1rem;
  border-block-start: 1px solid var(--line);
  font-size: 1.05rem;
}
.empty, .note { color: var(--ink-soft); }
.note { font-size: 0.9rem; }
.actions { display: flex; flex-wrap: wrap; align-items: center; gap: 0.75rem; }
.actions :deep(.btn-wa) { flex: 1 1 14rem; }
.link {
  min-block-size: 2.75rem;
  padding: 0.5rem 0;
  border: 0;
  background: none;
  color: var(--ink-soft);
  text-decoration: underline;
  text-underline-offset: 0.25em;
  cursor: pointer;
}
</style>
