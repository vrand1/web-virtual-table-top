export default defineNuxtRouteMiddleware(async (to, from) => {
  const userStore = useUserStore()

  if (!userStore.userData) {
    await userStore.fetchUser()
  }

  if (userStore.isLoggedIn && to.path === '/login') {
    return navigateTo('/main')
  }

  if (!userStore.isLoggedIn && to.path !== '/login') {
    return navigateTo('/login')
  }
  
})