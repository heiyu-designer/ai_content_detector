<script setup lang="ts">
/**
 * AI 检测视图

提供文本 AI 检测功能（需要登录）
*/
import { ref, onMounted, watch } from "vue"
import { useRouter } from "vue-router"
import { useQuotaStore } from "@/stores/quota"
import { useAuthStore } from "@/stores/auth"
import { useTextStore } from "@/stores/text"
import { detectText } from "@/services/api"
import ProgressBar from "@/components/ProgressBar.vue"
import SentenceCard from "@/components/SentenceCard.vue"
import PricingModal from "@/components/PricingModal.vue"
import type { DetectResponse, SentenceAnalysis } from "@/types"

const router = useRouter()
const quotaStore = useQuotaStore()
const authStore = useAuthStore()
const textStore = useTextStore()

// 状态
const text = ref("")
const lang = ref<"en" | "zh">("en")
const isLoading = ref(false)
const error = ref<string | null>(null)
const result = ref<DetectResponse | null>(null)
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

  // 从 store 获取待检测文本
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

// 提交检测
async function handleDetect() {
  if (!text.value.trim()) {
    error.value = "Please enter some text to detect"
    return
  }

  if (quotaStore.isQuotaExhausted) {
    error.value = "Daily quota exhausted. Please upgrade or try again tomorrow."
    return
  }

  isLoading.value = true
  error.value = null

  try {
    result.value = await detectText({
      text: text.value,
      lang: lang.value,
    })
    // 更新配额
    quotaStore.updateQuota(result.value.remaining_quota)
  } catch (e) {
    error.value = e instanceof Error ? e.message : "Detection failed"
    result.value = null
  } finally {
    isLoading.value = false
  }
}

// 跳转到 Humanize
function goToHumanize() {
  if (result.value) {
    // 获取所有句子，不只是 high 级别
    const allSentences = result.value.sentence_analysis
      .map((s: SentenceAnalysis) => s.text)
      .join(" ")

    if (allSentences) {
      textStore.setText(allSentences)
    }
  }
  router.push({ name: "humanize" })
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
    <main class="max-w-4xl mx-auto px-4 py-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">AI Content Detection</h1>
      <p class="text-gray-600 mb-8">Detect if your text was written by AI</p>

      <!-- 输入区域 -->
      <div class="card p-6 mb-8">
        <!-- 语言选择 -->
        <div class="flex items-center space-x-4 mb-4">
          <label class="text-sm font-medium text-gray-700">Language:</label>
          <div class="flex space-x-2">
            <button
              @click="lang = 'en'"
              :class="[
                'px-4 py-2 rounded-lg text-sm font-medium transition-colors',
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
                'px-4 py-2 rounded-lg text-sm font-medium transition-colors',
                lang === 'zh'
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              ]"
            >
              中文
            </button>
          </div>
        </div>

        <!-- 文本输入 -->
        <textarea
          v-model="text"
          class="input h-48 resize-none mb-4"
          :placeholder="lang === 'en' ? 'Enter or paste your text here...' : '在此输入或粘贴文本...'"
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
            @click="handleDetect"
            :disabled="isLoading || !text.trim()"
            class="btn-primary flex-1 py-3"
          >
            <span v-if="isLoading" class="mr-2">⏳</span>
            <span v-else class="mr-2">🔍</span>
            {{ isLoading ? "Detecting..." : "Detect AI" }}
          </button>
          <button
            @click="handleReset"
            class="btn-secondary py-3"
          >
            Reset
          </button>
        </div>
      </div>

      <!-- 检测结果 -->
      <div v-if="result" class="card p-6 animate-fade-in">
        <h2 class="text-xl font-semibold text-gray-900 mb-6">Detection Results</h2>

        <!-- 概率显示 -->
        <div class="grid md:grid-cols-2 gap-6 mb-8">
          <!-- AI 概率 -->
          <div>
            <div class="flex items-center justify-between mb-2">
              <span class="text-sm font-medium text-gray-700">AI Generated</span>
              <span class="text-2xl font-bold text-danger-600">
                {{ result.ai_probability }}%
              </span>
            </div>
            <ProgressBar
              :value="result.ai_probability"
              color="danger"
              :show-label="false"
            />
          </div>

          <!-- 人类概率 -->
          <div>
            <div class="flex items-center justify-between mb-2">
              <span class="text-sm font-medium text-gray-700">Human Written</span>
              <span class="text-2xl font-bold text-success-600">
                {{ result.human_probability }}%
              </span>
            </div>
            <ProgressBar
              :value="result.human_probability"
              color="success"
              :show-label="false"
            />
          </div>
        </div>

        <!-- 句子级别分析 -->
        <div class="mb-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Sentence Analysis</h3>
          <div class="space-y-3">
            <SentenceCard
              v-for="(sentence, index) in result.sentence_analysis"
              :key="index"
              :sentence="sentence"
              :index="index"
            />
          </div>
        </div>

        <!-- 特征模式分析 -->
        <div v-if="result.patterns && (result.patterns.ai_markers?.length || result.patterns.human_markers?.length)" class="mb-6 p-4 bg-gray-50 rounded-lg">
          <h3 class="text-lg font-medium text-gray-900 mb-3">Pattern Analysis</h3>

          <!-- AI 特征 -->
          <div v-if="result.patterns.ai_markers?.length" class="mb-3">
            <span class="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-red-100 text-red-800 mr-2">
              AI Patterns
            </span>
            <div class="mt-2 flex flex-wrap gap-2">
              <span
                v-for="(marker, idx) in result.patterns.ai_markers"
                :key="idx"
                class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800"
              >
                {{ marker }}
              </span>
            </div>
          </div>

          <!-- Human 特征 -->
          <div v-if="result.patterns.human_markers?.length">
            <span class="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-green-100 text-green-800 mr-2">
              Human Patterns
            </span>
            <div class="mt-2 flex flex-wrap gap-2">
              <span
                v-for="(marker, idx) in result.patterns.human_markers"
                :key="idx"
                class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800"
              >
                {{ marker }}
              </span>
            </div>
          </div>
        </div>

        <!-- Humanize 按钮 -->
        <button
          @click="goToHumanize"
          class="btn-primary w-full py-3"
        >
          <span class="mr-2">✍️</span>
          Humanize High-Probability Sentences
        </button>

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
