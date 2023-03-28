import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig(() => {
  return {
    plugins: [react()],
    base: '/static/',
    server: {
      host: '0.0.0.0',
      port: 9002,
      strictPort: true,
      origin: 'http://localhost:9002',
    },
    build: {
      outDir: './static/vite_output/',
      copyPublicDir: false,
      manifest: true,
      sourcemap: true,
      rollupOptions: {
        input: {
          main: './frontend/index.tsx',
        },
      },
    },
    test: {
      globals: true,
      environment: 'jsdom',
      setupFiles: './frontend/tests/setup.ts',
      coverage: {
        reporter: ['text', 'json', 'html'],
      },
    },
  }
})
