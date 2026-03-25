<script setup lang="ts">
/**
 * 登录视图
*/
import { ref } from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"

const router = useRouter()
const authStore = useAuthStore()

// 表单数据
const email = ref("")
const password = ref("")
const isLoading = ref(false)
const error = ref<string | null>(null)

// 提交登录
async function handleSubmit() {
  if (!email.value || !password.value) {
    error.value = "Please fill in all fields"
    return
  }

  isLoading.value = true
  error.value = null

  const success = await authStore.loginAction(email.value, password.value)

  if (success) {
    router.push("/")
  } else {
    error.value = authStore.error || "Login failed"
  }

  isLoading.value = false
}
</script>

<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center px-4">
    <div class="w-full max-w-md">
      <!-- Logo -->
      <div class="text-center mb-8">
        <router-link to="/" class="inline-flex items-center space-x-2">
          <div class="w-12 h-12 bg-primary-600 rounded-xl flex items-center justify-center">
            <span class="text-white font-bold text-2xl">U</span>
          </div>
          <span class="text-2xl font-bold text-gray-900">Unbot AI</span>
        </router-link>
      </div>

      <!-- 登录表单 -->
      <div class="card p-8">
        <h1 class="text-2xl font-bold text-gray-900 mb-6">Login</h1>

        <!-- 错误提示 -->
        <div
          v-if="error"
          class="mb-6 p-4 bg-danger-50 border border-danger-200 rounded-lg text-danger-700"
        >
          {{ error }}
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-4">
          <!-- 邮箱 -->
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 mb-1">
              Email
            </label>
            <input
              id="email"
              v-model="email"
              type="email"
              class="input"
              placeholder="you@example.com"
              :disabled="isLoading"
            />
          </div>

          <!-- 密码 -->
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-1">
              Password
            </label>
            <input
              id="password"
              v-model="password"
              type="password"
              class="input"
              placeholder="••••••••"
              :disabled="isLoading"
            />
          </div>

          <!-- 提交按钮 -->
          <button
            type="submit"
            :disabled="isLoading"
            class="btn-primary w-full py-3"
          >
            <span v-if="isLoading" class="mr-2">⏳</span>
            {{ isLoading ? "Logging in..." : "Login" }}
          </button>
        </form>

        <!-- 注册链接 -->
        <p class="mt-6 text-center text-gray-600">
          Don't have an account?
          <router-link
            to="/register"
            class="text-primary-600 hover:text-primary-700 font-medium"
          >
            Sign up
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>
