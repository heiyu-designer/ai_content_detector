<script setup lang="ts">
/**
 * 首页视图

主要功能入口页面
*/
import { ref } from "vue"
import { useRouter } from "vue-router"
import { useTextStore } from "@/stores/text"
import { useAuthStore } from "@/stores/auth"
import PricingModal from "@/components/PricingModal.vue"

const router = useRouter()
const textareaValue = ref("")
const textStore = useTextStore()
const authStore = useAuthStore()

// 定价弹窗状态
const showPricingModal = ref(false)

// 跳转到检测页面（需要登录）
function goToDetect() {
  // 未登录，跳转到登录页
  if (!authStore.isAuthenticated) {
    router.push({ name: "login" })
    return
  }

  if (textareaValue.value.trim()) {
    textStore.setText(textareaValue.value)
  }
  router.push({ name: "detect" })
}

// 跳转到 Humanize 页面（需要登录）
function goToHumanize() {
  // 未登录，跳转到登录页
  if (!authStore.isAuthenticated) {
    router.push({ name: "login" })
    return
  }

  if (textareaValue.value.trim()) {
    textStore.setText(textareaValue.value)
  }
  router.push({ name: "humanize" })
}

// 退出登录
function handleLogout() {
  authStore.logout()
  router.push({ name: "home" })
}

// 打开定价弹窗
function openPricing() {
  showPricingModal.value = true
}
</script>

<template>
  <div class="min-h-screen">
    <!-- 头部导航 -->
    <header class="bg-white shadow-sm">
      <nav class="max-w-6xl mx-auto px-4 py-4">
        <div class="flex items-center justify-between">
          <!-- Logo -->
          <div class="flex items-center space-x-2">
            <div class="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
              <span class="text-white font-bold text-xl">U</span>
            </div>
            <span class="text-xl font-bold text-gray-900">Unbot AI</span>
          </div>

          <!-- 导航链接 -->
          <div class="flex items-center space-x-6">
            <a href="#features" class="text-gray-600 hover:text-gray-900 transition-colors">
              Features
            </a>
            <button
              @click="openPricing"
              class="text-gray-600 hover:text-gray-900 transition-colors"
            >
              Pricing
            </button>

            <!-- 已登录状态 -->
            <template v-if="authStore.isAuthenticated">
              <span class="text-gray-600 text-sm">
                {{ authStore.userEmail }}
              </span>
              <span v-if="authStore.isPremium" class="text-xs bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full">
                Premium
              </span>
              <button
                @click="handleLogout"
                class="text-gray-600 hover:text-red-600 transition-colors"
              >
                Logout
              </button>
            </template>

            <!-- 未登录状态 -->
            <template v-else>
              <router-link
                to="/login"
                class="text-gray-600 hover:text-gray-900 transition-colors"
              >
                Login
              </router-link>
              <router-link to="/register" class="btn-primary">
                Get Started
              </router-link>
            </template>
          </div>
        </div>
      </nav>
    </header>

    <!-- Hero 区域 -->
    <section class="py-20 px-4">
      <div class="max-w-4xl mx-auto text-center">
        <h1 class="text-5xl font-bold text-gray-900 mb-6">
          Know if it's <span class="text-primary-600">AI</span>.<br />
          Make it <span class="text-success-600">human</span>.
        </h1>
        <p class="text-xl text-gray-600 mb-10 max-w-2xl mx-auto">
          Detect AI-generated content instantly. Transform robotic text into natural, human-written style with one click.
        </p>

        <!-- 主要功能入口 -->
        <div class="card p-8 max-w-2xl mx-auto">
          <!-- 文本输入 -->
          <textarea
            v-model="textareaValue"
            class="input h-40 mb-6 resize-none"
            placeholder="Paste or type your text here..."
          />

          <!-- 功能按钮 -->
          <div class="flex flex-col sm:flex-row gap-4">
            <button
              @click="goToDetect"
              class="flex-1 btn-primary py-4 text-lg"
            >
              <span class="mr-2">🔍</span>
              Detect AI
            </button>
            <button
              @click="goToHumanize"
              class="flex-1 btn-secondary py-4 text-lg"
            >
              <span class="mr-2">✍️</span>
              Humanize
            </button>
          </div>

          <!-- 配额提示 -->
          <p class="text-sm text-gray-500 mt-4">
            Free: 5 detections per day
          </p>
        </div>
      </div>
    </section>

    <!-- 功能特性 -->
    <section id="features" class="py-20 px-4 bg-white">
      <div class="max-w-6xl mx-auto">
        <h2 class="text-3xl font-bold text-center text-gray-900 mb-12">
          Features
        </h2>
        <div class="grid md:grid-cols-3 gap-8">
          <!-- 功能卡片 1 -->
          <div class="card p-6 text-center">
            <div class="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span class="text-3xl">🔍</span>
            </div>
            <h3 class="text-xl font-semibold mb-2">AI Detection</h3>
            <p class="text-gray-600">
              Instantly detect if text was written by AI. Get detailed probability scores and sentence-level analysis.
            </p>
          </div>

          <!-- 功能卡片 2 -->
          <div class="card p-6 text-center">
            <div class="w-16 h-16 bg-success-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span class="text-3xl">✍️</span>
            </div>
            <h3 class="text-xl font-semibold mb-2">One-Click Humanize</h3>
            <p class="text-gray-600">
              Transform AI-generated text into natural, human-sounding content. Choose from light, medium, or deep rewriting.
            </p>
          </div>

          <!-- 功能卡片 3 -->
          <div class="card p-6 text-center">
            <div class="w-16 h-16 bg-warning-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span class="text-3xl">⚡</span>
            </div>
            <h3 class="text-xl font-semibold mb-2">Fast & Free</h3>
            <p class="text-gray-600">
              No signup required. Get instant results with our free tier. Upgrade for unlimited access.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- 页脚 -->
    <footer class="py-8 px-4 border-t border-gray-200">
      <div class="max-w-6xl mx-auto text-center text-gray-500">
        <p>© 2026 Unbot AI. All rights reserved.</p>
      </div>
    </footer>

    <!-- 定价弹窗 -->
    <PricingModal v-model="showPricingModal" />
  </div>
</template>
