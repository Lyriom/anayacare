import { ref } from 'vue'

/**
 * Anuncios para lectores de pantalla: ariaNotify() cuando existe y, si no,
 * una región viva (aria-live) que la plantilla muestra con el texto de `mensaje`.
 */
export function useAnnouncer() {
  const mensaje = ref('')

  function anunciar(texto) {
    const destino = document.querySelector('dialog[open]') ?? document
    if (typeof destino.ariaNotify === 'function') {
      destino.ariaNotify(texto)
      return
    }
    mensaje.value = ''
    requestAnimationFrame(() => { mensaje.value = texto })
  }

  return { mensaje, anunciar }
}
