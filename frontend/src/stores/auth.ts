/**
 * 认证 Store

管理用户登录状态
*/
import { defineStore } from "pinia"
import { ref, computed } from "vue"
import { login, register } from "@/services/api"
import type { LoginResponse, User } from "@/types"

export const useAuthStore = defineStore("auth", () => {
  // 状态
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // 计算属性
  const isAuthenticated = computed(() => !!token.value)
  const isPremium = computed(() => user.value?.is_premium ?? false)
  const userEmail = computed(() => user.value?.email ?? "")

  // 初始化：从 localStorage 恢复状态
  function init() {
    const savedToken = localStorage.getItem("access_token")
    const savedUser = localStorage.getItem("user")

    if (savedToken) {
      token.value = savedToken
    }

    if (savedUser) {
      try {
        user.value = JSON.parse(savedUser)
      } catch {
        localStorage.removeItem("user")
      }
    }
  }

  // 登录
  async function loginAction(email: string, password: string) {
    isLoading.value = true
    error.value = null

    try {
      const response = await login({ email, password })
      handleLoginSuccess(response)
      return true
    } catch (e) {
      error.value = e instanceof Error ? e.message : "登录失败"
      return false
    } finally {
      isLoading.value = false
    }
  }

  // 注册
  async function registerAction(email: string, password: string) {
    isLoading.value = true
    error.value = null

    try {
      const response = await register({ email, password })
      handleLoginSuccess(response)
      return true
    } catch (e) {
      error.value = e instanceof Error ? e.message : "注册失败"
      return false
    } finally {
      isLoading.value = false
    }
  }

  // 处理登录成功
  function handleLoginSuccess(response: LoginResponse) {
    user.value = response.user
    token.value = response.token.access_token

    // 保存到 localStorage
    localStorage.setItem("access_token", response.token.access_token)
    localStorage.setItem("user", JSON.stringify(response.user))
  }

  // 登出
  function logout() {
    user.value = null
    token.value = null
    error.value = null

    // 清除 localStorage
    localStorage.removeItem("access_token")
    localStorage.removeItem("user")
  }

  // 清除错误
  function clearError() {
    error.value = null
  }

  return {
    // 状态
    user,
    token,
    isLoading,
    error,
    // 计算属性
    isAuthenticated,
    isPremium,
    userEmail,
    // 方法
    init,
    loginAction,
    registerAction,
    logout,
    clearError,
  }
})
