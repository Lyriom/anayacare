<script setup>
// Plantilla: define la estructura de la página (zonas) sin saber qué contenido va en cada una.
</script>

<template>
  <a class="skip" href="#contenido">Saltar al catálogo</a>
  <slot name="encabezado" />
  <main id="contenido" tabindex="-1">
    <section class="intro wrap" aria-labelledby="catalogo-titulo">
      <slot name="introduccion" />
    </section>
    <div class="wrap toolbar">
      <slot name="herramientas" />
    </div>
    <div class="wrap content">
      <slot />
    </div>
  </main>
  <slot name="pie" />
  <!-- Diálogos, barra del pedido y región de anuncios -->
  <slot name="capas" />
</template>

<style scoped>
.skip {
  position: absolute;
  inset-inline-start: 1rem;
  inset-block-start: -10rem;
  z-index: 100;
  padding: 0.75rem 1.25rem;
  background: var(--ink);
  color: var(--ivory);
  border-radius: 999px;
  text-decoration: none;
}
.skip:focus-visible { inset-block-start: 1rem; }
main:focus { outline: none; }
.intro { padding-block: clamp(2.5rem, 1.5rem + 4vw, 4.5rem) clamp(1.5rem, 1rem + 2vw, 2.25rem); }
.toolbar { position: relative; z-index: 1; }
.content { margin-block-start: clamp(1.5rem, 1rem + 2vw, 2.5rem); }
</style>
