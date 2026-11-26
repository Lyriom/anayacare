<script setup>
// Molécula: etiqueta + campo de búsqueda + icono.
import { useId } from 'vue'
import BaseIcon from '../atoms/BaseIcon.vue'

const texto = defineModel({ type: String, default: '' })
defineProps({
  etiqueta: { type: String, default: 'Buscar' },
  ayuda: { type: String, default: '' },
})
const id = useId()
</script>

<template>
  <div class="search-field">
    <label :for="id">{{ etiqueta }}</label>
    <div class="control">
      <BaseIcon nombre="buscar" />
      <input
        :id="id" v-model="texto" type="search" :placeholder="ayuda"
        autocomplete="off" autocorrect="off" autocapitalize="none" spellcheck="false" enterkeyhint="search"
      >
    </div>
  </div>
</template>

<style scoped>
.search-field { display: grid; gap: 0.35rem; }
label { font-size: 0.875rem; font-weight: 500; color: var(--ink); }
.control { position: relative; }
.control svg {
  position: absolute;
  inset-inline-start: 1rem;
  inset-block-start: 50%;
  translate: 0 -50%;
  inline-size: 1.15rem;
  block-size: 1.15rem;
  color: var(--gold-text);
  pointer-events: none;
}
input {
  inline-size: 100%;
  min-block-size: 3rem;
  padding: 0.6rem 1rem 0.6rem 2.75rem;
  border: 1px solid var(--line);
  border-radius: 999px;
  background: var(--white);
  font-size: 1rem;
}
input::placeholder { color: #8c7b6e; }
input:hover { border-color: var(--gold); }
input:focus-visible { outline-offset: 2px; border-color: var(--gold); }
</style>
