<script setup>
// Molécula: grupo de opciones exclusivas (radios con aspecto de chip) y su leyenda.
import { useId } from 'vue'

const seleccion = defineModel({ type: String, required: true })
defineProps({
  leyenda: { type: String, default: 'Categoría' },
  /** [{ valor: 'Jabones', cantidad: 4 }] */
  opciones: { type: Array, required: true },
})
const nombre = useId()
</script>

<template>
  <fieldset class="filter">
    <legend>{{ leyenda }}</legend>
    <div class="chips">
      <label v-for="opcion in opciones" :key="opcion.valor" class="chip">
        <input v-model="seleccion" type="radio" :name="nombre" :value="opcion.valor">
        <span>{{ opcion.valor }} <small>{{ opcion.cantidad }}</small></span>
      </label>
    </div>
  </fieldset>
</template>

<style scoped>
.filter { margin: 0; padding: 0; border: 0; min-inline-size: 0; }
legend { padding: 0; margin-block-end: 0.35rem; font-size: 0.875rem; font-weight: 500; color: var(--ink); }
.chips { display: flex; flex-wrap: wrap; gap: 0.5rem; }
.chip { position: relative; }
/* El radio sigue siendo el control real (teclado y lector de pantalla); solo se oculta su círculo. */
.chip input { position: absolute; inset: 0; opacity: 0; margin: 0; cursor: pointer; }
.chip span {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  min-block-size: 2.75rem;
  padding: 0.5rem 1rem;
  border: 1px solid var(--line);
  border-radius: 999px;
  background: var(--white);
  font-size: 0.9375rem;
  white-space: nowrap;
  transition: background-color 0.2s ease, border-color 0.2s ease, color 0.2s ease;
}
.chip small { font-size: 0.75rem; color: var(--ink-soft); font-variant-numeric: tabular-nums; }
.chip:hover span { border-color: var(--gold); }
.chip input:checked + span { background: var(--ink); border-color: var(--ink); color: var(--ivory); }
.chip input:checked + span small { color: var(--gold-light); }
.chip input:focus-visible + span { outline: 2px solid var(--gold-text); outline-offset: 3px; }
@media (forced-colors: active) {
  .chip span { border-color: ButtonText; }
  .chip input:checked + span { outline: 3px solid Highlight; }
}
</style>
