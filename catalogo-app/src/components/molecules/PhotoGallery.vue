<script setup>
// Galería con desplazamiento nativo: gestos táctiles, flechas e indicadores.
import { onBeforeUnmount, ref, watch } from 'vue'
import ProductPicture from '../atoms/ProductPicture.vue'

const props = defineProps({ fotos: { type: Array, required: true } })
const track = ref(null)
const activa = ref(0)
const anuncio = ref('')
let espera

function irA(index) {
  const elemento = track.value?.children[index]
  if (!elemento) return
  activa.value = index
  track.value.scrollTo({ left: elemento.offsetLeft - track.value.offsetLeft })
}
function mover(delta) {
  irA((activa.value + delta + props.fotos.length) % props.fotos.length)
}
function alDesplazar() {
  if (!track.value) return
  const zona = track.value
  const centro = zona.scrollLeft + zona.clientWidth / 2
  let mejor = 0
  let distancia = Infinity
  Array.from(zona.children).forEach((el, i) => {
    const d = Math.abs((el.offsetLeft - zona.offsetLeft) + el.offsetWidth / 2 - centro)
    if (d < distancia) { distancia = d; mejor = i }
  })
  activa.value = mejor
  clearTimeout(espera)
  espera = setTimeout(() => { anuncio.value = `${props.fotos[activa.value].etiqueta}, imagen ${activa.value + 1} de ${props.fotos.length}` }, 180)
}
watch(() => props.fotos, () => { activa.value = 0; anuncio.value = '' })
onBeforeUnmount(() => clearTimeout(espera))
</script>

<template>
  <section class="gallery" aria-roledescription="carrusel" aria-label="Fotos del producto">
    <div class="stage">
      <div v-if="fotos.length > 1" class="arrows">
        <button type="button" aria-label="Foto anterior" @click="mover(-1)">‹</button>
        <button type="button" aria-label="Foto siguiente" @click="mover(1)">›</button>
      </div>
      <div ref="track" class="track" tabindex="0" role="group" aria-label="Desliza para ver las fotos" @scroll.passive="alDesplazar">
        <figure v-for="(foto, i) in fotos" :key="foto.slug" role="group" aria-roledescription="imagen" :aria-label="`${foto.etiqueta}, ${i + 1} de ${fotos.length}`">
          <ProductPicture :slug="foto.slug" :alt="foto.alt" sizes="(min-width: 52rem) 29rem, 90vw" :carga="i === 0 ? 'eager' : 'lazy'" prioridad="low" />
        </figure>
      </div>
    </div>
    <div v-if="fotos.length > 1" class="gallery-footer">
      <span class="caption">{{ fotos[activa].etiqueta }}</span>
      <div class="dots" role="group" aria-label="Elegir foto">
        <button v-for="(foto, i) in fotos" :key="foto.slug" type="button" :aria-label="`Ver ${foto.etiqueta}`" :aria-current="i === activa ? 'true' : undefined" @click="irA(i)"><span /></button>
      </div>
      <span class="count">{{ activa + 1 }} / {{ fotos.length }}</span>
    </div>
    <p class="visually-hidden" role="status" aria-live="polite">{{ anuncio }}</p>
  </section>
</template>

<style scoped>
.gallery { min-inline-size: 0; padding: 1.25rem; background: #f7f0e8; }
.stage { position: relative; overflow: hidden; border-radius: 0.75rem; background: #f8eee3; }
.track {
  display: flex; overflow-x: auto; scroll-snap-type: x mandatory;
  overscroll-behavior-x: contain; scrollbar-width: none; touch-action: manipulation;
  block-size: clamp(17rem, 46dvh, 29rem);
}
.track::-webkit-scrollbar { display: none; }
.track:focus-visible { outline: 2px solid var(--gold-text); outline-offset: -3px; }
figure { flex: 0 0 100%; min-inline-size: 0; margin: 0; scroll-snap-align: center; scroll-snap-stop: always; }
figure :deep(picture) { display: block; block-size: 100%; }
figure :deep(img) { inline-size: 100%; block-size: 100%; aspect-ratio: auto; object-fit: contain; }
.arrows { position: absolute; inset: 0 0.65rem; z-index: 1; display: flex; align-items: center; justify-content: space-between; pointer-events: none; }
.arrows button { pointer-events: auto; display: grid; place-items: center; inline-size: 2.75rem; block-size: 2.75rem; border: 1px solid rgb(107 90 70 / .22); border-radius: 50%; background: rgb(255 253 249 / .9); color: var(--ink); font: 1.8rem/1 var(--font-body); cursor: pointer; }
.arrows button:hover { background: #fff; }
.arrows button:focus-visible, .dots button:focus-visible { outline: 2px solid var(--gold-text); outline-offset: 2px; }
.gallery-footer { display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; padding: 0.6rem 0.15rem 0; color: var(--ink-soft); font-size: 0.8rem; }
.caption { justify-self: start; }
.count { justify-self: end; font-variant-numeric: tabular-nums; }
.dots { display: flex; align-items: center; gap: 0.15rem; }
.dots button { display: grid; place-items: center; inline-size: 1.75rem; block-size: 1.75rem; padding: 0; border: 0; background: none; cursor: pointer; }
.dots span { inline-size: 0.45rem; block-size: 0.45rem; border-radius: 99px; background: #a59480; }
.dots button[aria-current="true"] span { inline-size: 1.05rem; background: var(--gold-text); }
@media (prefers-reduced-motion: no-preference) { .track { scroll-behavior: smooth; } }
@media (min-width: 52rem) { .gallery { position: sticky; top: 0; align-self: start; padding: 1.5rem; } }
@media (max-width: 40rem) { .gallery { padding: 0.8rem; } .track { block-size: clamp(15rem, 38dvh, 23rem); } }
</style>
