// Utilidades puras (sin estado): formato de dinero, búsqueda y enlaces de WhatsApp.

const dinero = new Intl.NumberFormat('es-EC', { style: 'currency', currency: 'USD' })

/** 12.9 -> "$12,90" */
export const formatoDinero = (valor) => dinero.format(valor)

/** Texto en minúsculas y sin tildes, para que «jabon» encuentre «Jabón». */
export const normalizar = (texto = '') =>
  texto.normalize('NFD').replace(/\p{Diacritic}/gu, '').toLowerCase().trim()

/** Rutas de la foto de un producto: <base>/<slug>-<ancho>.<formato> */
export const BASE_FOTOS = '../img/productos'
export const ANCHOS_FOTOS = [480, 800, 1200]
export const srcsetFoto = (slug, formato) =>
  ANCHOS_FOTOS.map((ancho) => `${BASE_FOTOS}/${slug}-${ancho}.${formato} ${ancho}w`).join(', ')
export const srcFoto = (slug, ancho = 800) => `${BASE_FOTOS}/${slug}-${ancho}.jpg`

export const enlaceWhatsApp = (numero, texto) =>
  `https://wa.me/${numero}?text=${encodeURIComponent(texto)}`
