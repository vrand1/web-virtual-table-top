<template>
  <n-space vertical align="center" style="margin-top: 50px;">
    <n-gradient-text type="info" :size="24">
      Добро пожаловать, {{ userStore.userData?.username}}!
    </n-gradient-text>

    <n-avatar
      round
      :size="120"
      :src="userStore.userData?.avatar"
    />

  </n-space>
</template>

<script setup>
import { useUserStore } from '~/stores/user'
const userStore = useUserStore()
</script>