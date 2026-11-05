import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'

// Production build goes straight into ../web, which the Python server serves.
export default defineConfig({
  plugins: [react()],
  build: { outDir: '../web', emptyOutDir: true, target: 'es2019', sourcemap: false },
  server: { port: 5173, proxy: { '/api': 'http://localhost:8000', '/p': 'http://localhost:8000' } },
  test: { environment: 'jsdom', setupFiles: ['./src/test/setup.js'], globals: true },
})
