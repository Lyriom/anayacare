<script setup>
// Organismo: el pedido en un <dialog> modal, con envío de la lista por WhatsApp.
import { computed, nextTick, onMounted, ref } from 'vue'
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
  /** Texto para lectores de pantalla: el resto de la página queda inerte mientras el modal está abierto. */
  anuncio: { type: String, default: '' },
})
const emit = defineEmits(['cambiar', 'vaciar'])

const { dialogo, abrir } = useModal()
defineExpose({ abrir })
const titulo = ref(null)

const pago = ref(null)
const pagando = ref(false)
const errorPago = ref('')
const cliente = ref({ name: '', email: '', phone: '' })
onMounted(async () => {
  try {
    const respuesta = await fetch('../datos/pagos.json', { cache: 'no-store' })
    if (!respuesta.ok) return
    const config = await respuesta.json()
    if (config.habilitado === true && /^https:\/\/[a-z0-9-]+\.supabase\.co$/.test(config.supabaseUrl) && config.anonKey) pago.value = config
  } catch { /* WhatsApp sigue disponible si el servicio no está configurado. */ }
})
async function pagar() {
  if (!pago.value || pagando.value) return
  pagando.value = true
  errorPago.value = ''
  try {
    const response = await fetch(`${pago.value.supabaseUrl}/functions/v1/payment-prepare`, {
      method: 'POST', headers: { 'Content-Type': 'application/json', apikey: pago.value.anonKey },
      body: JSON.stringify({ ...cliente.value, items: props.lineas.map((linea) => ({ id: linea.id, quantity: linea.qty })) }),
    })
    const resultado = await response.json()
    if (!response.ok || !resultado.url) throw new Error(resultado.error || 'No se pudo iniciar el pago.')
    const destino = new URL(resultado.url)
    if (destino.protocol !== 'https:' || !(destino.hostname === 'payphonetodoesposible.com' || destino.hostname.endsWith('.payphonetodoesposible.com'))) throw new Error('El enlace de pago no es válido.')
    location.assign(destino.href)
  } catch (error) {
    errorPago.value = error.message || 'No se pudo iniciar el pago. Intenta de nuevo.'
  } finally { pagando.value = false }
}

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
      <p class="note">El costo de envío se coordina por WhatsApp.</p>
      <form v-if="lineas.length && pago" class="checkout" @submit.prevent="pagar">
        <h2>Pagar con PayPhone</h2>
        <p>El pago cubre los productos; coordina la entrega con nosotros.</p>
        <label for="pago-nombre">Nombre completo</label><input id="pago-nombre" v-model.trim="cliente.name" autocomplete="name" required minlength="2" maxlength="100">
        <label for="pago-email">Correo electrónico</label><input id="pago-email" v-model.trim="cliente.email" type="email" autocomplete="email" required maxlength="254">
        <label for="pago-telefono">Teléfono</label><input id="pago-telefono" v-model.trim="cliente.phone" type="tel" autocomplete="tel" required minlength="7" maxlength="30">
        <button type="submit" :disabled="pagando">{{ pagando ? 'Preparando pago…' : 'Continuar al pago' }}</button>
        <p role="status" aria-live="polite">{{ errorPago }}</p>
      </form>
      <div v-if="lineas.length" class="actions">
        <BaseButton variante="wa" :href="enlace" externo autofocus>
          <BaseIcon nombre="whatsapp" />Enviar pedido por WhatsApp
        </BaseButton>
        <button type="button" class="link" @click="vaciar">Vaciar pedido</button>
      </div>
    </div>
    <p class="visually-hidden" aria-live="polite">{{ anuncio }}</p>
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
.checkout { display: grid; gap: .45rem; border-block: 1px solid var(--line); padding-block: 1.2rem; }
.checkout h2 { font-size: 1.4rem; }
.checkout p { color: var(--ink-soft); font-size: .9rem; }
.checkout label { margin-top: .4rem; font-weight: 600; }
.checkout input { width: 100%; padding: .7rem; border: 1px solid var(--line); border-radius: .4rem; font: inherit; }
.checkout button { margin-top: .6rem; border: 0; border-radius: 2rem; padding: .8rem 1rem; background: #806022; color: white; font: inherit; cursor: pointer; }
.checkout button:disabled { opacity: .6; cursor: wait; }
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
