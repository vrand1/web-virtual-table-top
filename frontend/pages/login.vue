<template>
    <n-card title="Добро пожаловать в WebTTS">
      <div class="flex flex-col items-center gap-6">
        <n-text depth="3">
          Для входа в систему используйте ваш аккаунт Discord
        </n-text>
        
        <n-button 
          type="primary" 
          size="large" 
          @click="handleDiscordLogin"
          block
        >
          <template #icon>
            </template>
          Войти через Discord
        </n-button>
      </div>
    </n-card>  
</template>

<script setup>
definePageMeta({
  layout: 'blank' 
})

const handleDiscordLogin = () => {
  window.location.href = '/api/v1/auth/discord/login'
}
</script>

