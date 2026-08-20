import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from "path"

export default defineConfig(({ mode }) => ({
  base: mode === 'production' ? '/static/' : './', // /static/ for prod | / for dev
  plugins: [vue()],
  css: {
    transformer: "lightningcss",
    lightningcss: {
      drafts: {
        nesting: true,
      },
    },
  },
  build: {
    target: "es2020",
    outDir: 'dist',
    assetsDir: 'assets', // all CSS/JS will go under dist/assets
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "src"),
    },
  },
}))
