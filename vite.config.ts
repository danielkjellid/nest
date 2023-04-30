import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from 'tailwindcss'

// https://vitejs.dev/config/
export default defineConfig(() => {
  return {
    plugins: [react(), tailwindcss()],
    base: '/static/',
    server: {
      host: '0.0.0.0',
      port: 3000,
      strictPort: true,
    },
    build: {
      outDir: './static/dist/',
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
    css: {
      postcss: {
        plugins: [tailwindcss],
      },
    },
  }
})
