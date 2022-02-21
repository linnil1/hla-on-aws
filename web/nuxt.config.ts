import { defineNuxtConfig } from 'nuxt3'

// https://v3.nuxtjs.org/docs/directory-structure/nuxt.config
export default defineNuxtConfig({
  meta: {
    link: [
      {'href': 'https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css', rel: 'stylesheet'},
    ],
    script: [
      {src: 'https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js'},
      {src: 'https://kit.fontawesome.com/3250e2e7c3.js'}
    ],
  },
  privateRuntimeConfig: {
    AWS_API: 'https://oy1431r9p1.execute-api.us-east-2.amazonaws.com/hla',
  }
})
