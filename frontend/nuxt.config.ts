import { defineNuxtConfig } from "nuxt/config";

export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  ssr: false, 
  
  modules: [
    '@bg-dev/nuxt-naiveui',
    '@pinia/nuxt'
  ],

  runtimeConfig: {
    public: {
      apiBase: '/api'
    },
  },
  
  devtools: { enabled: true }
})