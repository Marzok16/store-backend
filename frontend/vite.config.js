import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: '/frontend-store/', // add this line
  server: {
    host: '0.0.0.0', // Allow external connections
    port: 5173,
    allowedHosts: 'all',
    proxy: {
      '/media': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
