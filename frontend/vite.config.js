import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'
import dotenv from 'dotenv'

dotenv.config({ path: '../.env' })

// https://vite.dev/config/
export default defineConfig({
  plugins: [svelte()],
  server: {
    host: '0.0.0.0',  // Permite acceso desde la red
    port: process.env.FRONTEND_PORT || 5173
  }
})
