<script setup lang="ts">
/**
 * Humanize 改写视图

提供文本 Humanize 改写功能（需要登录）
*/
import { ref, onMounted, watch } from "vue"
import { useRouter } from "vue-router"
import { useQuotaStore } from "@/stores/quota"
import { useAuthStore } from "@/stores/auth"
import { useTextStore } from "@/stores/text"
import { humanizeText } from "@/services/api"
import PricingModal from "@/components/PricingModal.vue"
import type { HumanizeResponse, RewriteStrength } from "@/types"

const router = useRouter()
const quotaStore = useQuotaStore()
const authStore = useAuthStore()
const textStore = useTextStore()

// 状态
const text = ref("")
const lang = ref<"en" | "zh">("en")
const strength = ref<RewriteStrength>("medium")
const isLoading = ref(false)
const error = ref<string | null>(null)
const result = ref<HumanizeResponse | null>(null)
const showPricingModal = ref(false)

// 检测语言
function detectLanguage(input: string): "en" | "zh" {
  const chineseChars = (input.match(/[\u4e00-\u9fff]/g) || []).length
  const totalChars = input.replace(/\s/g, "").length
  if (totalChars === 0) return "en"
  return chineseChars / totalChars > 0.3 ? "zh" : "en"
}

// 监听文本变化自动检测语言
watch(text, (newText) => {
  if (newText.trim()) {
    lang.value = detectLanguage(newText)
  }
})

// 初始化
onMounted(() => {
  // 未登录，跳转到登录页
  if (!authStore.isAuthenticated) {
    router.push({ name: "login" })
    return
  }

  // 从 store 获取待改写文本
  const storeText = textStore.getAndClearText()
  if (storeText) {
    text.value = storeText
    lang.value = detectLanguage(storeText)
  }
  // 获取配额
  quotaStore.fetchQuota()
})

// 退出登录
function handleLogout() {
  authStore.logout()
  router.push({ name: "home" })
}

// 提交改写
async function handleHumanize() {
  if (!text.value.trim()) {
    error.value = "Please enter some text to humanize"
    return
  }

  if (quotaStore.isQuotaExhausted) {
    error.value = "Daily quota exhausted. Please upgrade or try again tomorrow."
    return
  }

  isLoading.value = true
  error.value = null

  try {
    result.value = await humanizeText({
      text: text.value,
      strength: strength.value,
      lang: lang.value,
    })
    // 更新配额
    quotaStore.updateQuota(result.value.remaining_quota)
  } catch (e) {
    error.value = e instanceof Error ? e.message : "Humanize failed"
    result.value = null
  } finally {
    isLoading.value = false
  }
}

// 复制结果
async function copyResult() {
  if (result.value?.rewritten) {
    await navigator.clipboard.writeText(result.value.rewritten)
  }
}

// 重写一次
async function rewriteAgain() {
  if (result.value) {
    text.value = result.value.rewritten
    lang.value = detectLanguage(result.value.rewritten)
    result.value = null
  }
}

// 重置
function handleReset() {
  text.value = ""
  result.value = null
  error.value = null
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 头部 -->
    <header class="bg-white shadow-sm">
      <nav class="max-w-6xl mx-auto px-4 py-4">
        <div class="flex items-center justify-between">
          <router-link to="/" class="flex items-center space-x-2">
            <div class="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
              <span class="text-white font-bold text-xl">U</span>
            </div>
            <span class="text-xl font-bold text-gray-900">Unbot AI</span>
          </router-link>

          <!-- 用户信息和配额 -->
          <div class="flex items-center space-x-4">
            <span class="text-gray-600 text-sm">{{ authStore.userEmail }}</span>
            <span v-if="authStore.isPremium" class="text-xs bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full">
              Premium
            </span>
            <span class="text-sm text-gray-600">
              Daily Quota: {{ quotaStore.remaining }}/{{ quotaStore.dailyLimit }}
            </span>
            <button
              @click="showPricingModal = true"
              class="text-sm text-primary-600 hover:text-primary-700 font-medium"
            >
              Upgrade
            </button>
            <button
              @click="handleLogout"
              class="text-sm text-gray-600 hover:text-red-600"
            >
              Logout
            </button>
          </div>
        </div>
      </nav>
    </header>

    <!-- 主内容 -->
    <main class="max-w-6xl mx-auto px-4 py-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">Humanize Text</h1>
      <p class="text-gray-600 mb-8">Transform AI text into natural, human-sounding content</p>

      <!-- 输入区域 -->
      <div class="card p-6 mb-8">
        <!-- 语言和强度选择 -->
        <div class="flex flex-wrap items-center gap-6 mb-4">
          <!-- 语言选择 -->
          <div class="flex items-center space-x-2">
            <label class="text-sm font-medium text-gray-700">Language:</label>
            <div class="flex space-x-2">
              <button
                @click="lang = 'en'"
                :class="[
                  'px-3 py-1.5 rounded-lg text-sm font-medium transition-colors',
                  lang === 'en'
                    ? 'bg-primary-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                ]"
              >
                English
              </button>
              <button
                @click="lang = 'zh'"
                :class="[
                  'px-3 py-1.5 rounded-lg text-sm font-medium transition-colors',
                  lang === 'zh'
                    ? 'bg-primary-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                ]"
              >
                中文
              </button>
            </div>
          </div>

          <!-- 强度选择 -->
          <div class="flex items-center space-x-2">
            <label class="text-sm font-medium text-gray-700">Strength:</label>
            <div class="flex space-x-2">
              <button
                @click="strength = 'light'"
                :class="[
                  'px-3 py-1.5 rounded-lg text-sm font-medium transition-colors',
                  strength === 'light'
                    ? 'bg-success-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                ]"
              >
                Light
              </button>
              <button
                @click="strength = 'medium'"
                :class="[
                  'px-3 py-1.5 rounded-lg text-sm font-medium transition-colors',
                  strength === 'medium'
                    ? 'bg-warning-500 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                ]"
              >
                Medium
              </button>
              <button
                @click="strength = 'deep'"
                :class="[
                  'px-3 py-1.5 rounded-lg text-sm font-medium transition-colors',
                  strength === 'deep'
                    ? 'bg-danger-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                ]"
              >
                Deep
              </button>
            </div>
          </div>
        </div>

        <!-- 文本输入 -->
        <textarea
          v-model="text"
          class="input h-48 resize-none mb-4"
          :placeholder="lang === 'en' ? 'Enter or paste your AI-generated text here...' : '在此输入或粘贴 AI 生成的文本...'"
          :disabled="isLoading"
        />

        <!-- 错误提示 -->
        <div
          v-if="error"
          class="mb-4 p-4 bg-danger-50 border border-danger-200 rounded-lg text-danger-700"
        >
          {{ error }}
        </div>

        <!-- 操作按钮 -->
        <div class="flex space-x-4">
          <button
            @click="handleHumanize"
            :disabled="isLoading || !text.trim()"
            class="btn-primary flex-1 py-3"
          >
            <span v-if="isLoading" class="mr-2">⏳</span>
            <span v-else class="mr-2">✍️</span>
            {{ isLoading ? "Humanizing..." : "Humanize" }}
          </button>
          <button
            @click="handleReset"
            class="btn-secondary py-3"
          >
            Reset
          </button>
        </div>
      </div>

      <!-- 改写结果 -->
      <div v-if="result" class="card p-6 animate-fade-in">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-xl font-semibold text-gray-900">Humanized Result</h2>
          <span class="badge bg-gray-100 text-gray-800">
            Strength: {{ strength }}
          </span>
        </div>

        <!-- 原文 -->
        <div class="mb-4">
          <h3 class="text-sm font-medium text-gray-700 mb-2">Original:</h3>
          <div class="p-4 bg-gray-50 rounded-lg">
            <p class="text-gray-700 whitespace-pre-wrap">{{ result.original }}</p>
          </div>
        </div>

        <!-- 改写后 -->
        <div class="mb-6">
          <h3 class="text-sm font-medium text-gray-700 mb-2">Rewritten:</h3>
          <div class="p-4 bg-success-50 border border-success-200 rounded-lg">
            <p class="text-gray-900 whitespace-pre-wrap font-medium">
              {{ result.rewritten }}
            </p>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="flex space-x-4">
          <button
            @click="copyResult"
            class="btn-primary flex-1 py-3"
          >
            <span class="mr-2">📋</span>
            Copy Result
          </button>
          <button
            @click="rewriteAgain"
            class="btn-secondary flex-1 py-3"
          >
            <span class="mr-2">🔄</span>
            Rewrite Again
          </button>
        </div>

        <!-- 剩余配额 -->
        <p class="text-sm text-gray-500 text-center mt-4">
          Remaining daily quota: {{ result.remaining_quota }}
        </p>
      </div>
    </main>

    <!-- 定价弹窗 -->
    <PricingModal v-model="showPricingModal" />
  </div>
</template>
