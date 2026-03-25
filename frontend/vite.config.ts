import { fileURLToPath, URL } from "node:url"
import { defineConfig } from "vite"
import vue from "@vitejs/plugin-vue"

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  // API 代理配置
  server: {
    port: 5173,
    proxy: {
      "/api": {
        target: "http://localhost:30001",
        changeOrigin: true,
      },
      "/health": {
        target: "http://localhost:30001",
        changeOrigin: true,
      },
    },
  },
})
