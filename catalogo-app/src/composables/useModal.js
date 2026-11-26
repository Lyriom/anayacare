import { onBeforeUnmount, onMounted, ref } from 'vue'

/**
 * Controla un <dialog closedby="any"> abierto con showModal().
 * En navegadores sin `closedby` (Safari) agrega el cierre al tocar fuera del diálogo:
 * se compara la posición del puntero (no event.target), porque el <dialog> también es
 * el target de su propio padding, y se exige que presionar y soltar ocurran fuera.
 */
export function useModal() {
  const dialogo = ref(null)
  let presionFuera = false

  const fuera = (e) => {
    const r = dialogo.value.getBoundingClientRect()
    return e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom
  }
  const alPresionar = (e) => { presionFuera = fuera(e) }
  const alSoltar = (e) => { if (presionFuera && fuera(e)) dialogo.value.close() }
  const necesitaRespaldo = !('closedBy' in HTMLDialogElement.prototype)

  onMounted(() => {
    if (!necesitaRespaldo || !dialogo.value) return
    dialogo.value.addEventListener('pointerdown', alPresionar)
    dialogo.value.addEventListener('pointerup', alSoltar)
  })
  onBeforeUnmount(() => {
    dialogo.value?.removeEventListener('pointerdown', alPresionar)
    dialogo.value?.removeEventListener('pointerup', alSoltar)
  })

  const abrir = () => { if (!dialogo.value?.open) dialogo.value?.showModal() }
  const cerrar = () => dialogo.value?.close()

  return { dialogo, abrir, cerrar }
}
