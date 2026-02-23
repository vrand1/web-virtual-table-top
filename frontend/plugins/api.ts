export default defineNuxtPlugin(() => {
  const userStore = useUserStore()

  globalThis.$api = $fetch.create({
    baseURL: '/api/v1',
    onResponseError({ response }) {
      if (response.status === 401) {
        console.error('Сессия истекла или невалидна')
        
        userStore.userData = null
        
        navigateTo('/login')
      }
    }
  })
})