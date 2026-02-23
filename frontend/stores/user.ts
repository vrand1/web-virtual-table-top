export const useUserStore = defineStore('user', {
  state: () => ({
    userData: null as any
  }),
  getters: {
    isLoggedIn: (state) => !!state.userData,
  },
  actions: {
    async fetchUser() {
      try {

        const data = await $fetch('/api/v1/auth/me')
        this.userData = data
      } catch (error: any) {
        if (error.status === 401) {
          console.warn('Юзер не авторизован (куки нет или протухла)')
        } else {
          console.error('Ошибка профиля:', error)
        }
        this.userData = null
      }
    },

    async logout() {
        try {
            await $fetch('/api/v1/auth/logout', { method: 'POST' })
        } catch (e) {
            console.error('Ошибка при выходе на бэкенде', e)
        } finally {
            this.userData = null
            navigateTo('/login')
        }
    }

  }
})