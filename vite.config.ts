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
      outDir: './public/vite_output/',
      copyPublicDir: false,
      manifest: true,
      sourcemap: true,
      rollupOptions: {
        input: {
          main: './frontend/index.tsx',
          login: './frontend/apps/login/index.tsx'
        },
      },
    },
    test: {
      globals: true,
      environment: 'jsdom',
      setupFiles: './frontend/tests/setup.ts',
      include: [
        '**/__tests__/*.{test,spec}.{js,mjs,cjs,ts,mts,cts,jsx,tsx}',
        '**/__snapshots__/*.{test,spec}.{js,mjs,cjs,ts,mts,cts,jsx,tsx}',
        '**/*.{test,spec}.{js,mjs,cjs,ts,mts,cts,jsx,tsx}',
      ],
      exclude: [
        '**/node_modules/**',
        '**/dist/**',
        '**/.{idea,git,cache,output,temp}/**',
        '**/{rollup,vite,vitest,tailwind,postcss}.config.*',
      ],
      coverage: {
        reporter: ['text', 'json', 'html'],
      },
    },
  }
})
