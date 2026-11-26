import { readFile } from 'node:fs/promises'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import vue from '@vitejs/plugin-vue'
import { defineConfig } from 'vite'

// Raíz del sitio principal (la carpeta que contiene a catalogo-app/).
const SITIO = fileURLToPath(new URL('..', import.meta.url))
const TIPOS = {
  '.json': 'application/json', '.avif': 'image/avif', '.webp': 'image/webp',
  '.jpg': 'image/jpeg', '.png': 'image/png',
}

// En producción la página vive en catalogo/ y lee ../datos y ../img del sitio.
// En desarrollo (npm run dev) servimos esas dos carpetas desde el sitio principal.
function sitioPrincipal() {
  return {
    name: 'anaya-sitio-principal',
    configureServer(server) {
      server.middlewares.use(async (req, res, next) => {
        const ruta = decodeURIComponent((req.url ?? '').split('?')[0])
        if (!/^\/(datos|img)\//.test(ruta)) return next()
        const archivo = path.join(SITIO, ruta)
        if (!archivo.startsWith(SITIO)) return next()
        try {
          const cuerpo = await readFile(archivo)
          res.setHeader('Content-Type', TIPOS[path.extname(archivo)] ?? 'application/octet-stream')
          res.end(cuerpo)
        } catch {
          next()
        }
      })
    },
  }
}

export default defineConfig({
  // Rutas relativas: funciona en /anayacare/catalogo/ (GitHub Pages) y en /catalogo/ (Netlify).
  base: './',
  plugins: [vue(), sitioPrincipal()],
  build: {
    outDir: path.join(SITIO, 'catalogo'),
    emptyOutDir: true,
  },
  server: { fs: { allow: [SITIO] } },
})
