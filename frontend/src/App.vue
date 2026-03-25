<script setup lang="ts">
import { onMounted } from "vue"
import { RouterView } from "vue-router"
import { useAuthStore } from "@/stores/auth"

const authStore = useAuthStore()

// 初始化认证状态
onMounted(() => {
  authStore.init()
})
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <RouterView />
  </div>
</template>
