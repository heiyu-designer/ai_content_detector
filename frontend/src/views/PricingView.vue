<script setup lang="ts">
/**
 * 定价视图

展示定价方案
*/
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"

const router = useRouter()
const authStore = useAuthStore()

// 退出登录
function handleLogout() {
  authStore.logout()
  router.push({ name: "home" })
}
</script>

<template>
  <div class="min-h-screen">
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

          <div class="flex items-center space-x-4">
            <router-link to="/" class="text-gray-600 hover:text-gray-900">
              Home
            </router-link>

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
              <router-link to="/login" class="btn-primary">
                Login
              </router-link>
            </template>
          </div>
        </div>
      </nav>
    </header>

    <!-- 定价内容 -->
    <main class="max-w-6xl mx-auto px-4 py-16">
      <div class="text-center mb-12">
        <h1 class="text-4xl font-bold text-gray-900 mb-4">
          Simple, Transparent Pricing
        </h1>
        <p class="text-xl text-gray-600">
          Choose the plan that fits your needs
        </p>
      </div>

      <!-- 定价卡片 -->
      <div class="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
        <!-- 免费版 -->
        <div class="card p-8">
          <h2 class="text-xl font-semibold text-gray-900 mb-2">Free</h2>
          <p class="text-gray-600 mb-6">Perfect for trying out</p>
          <div class="text-4xl font-bold text-gray-900 mb-6">
            $0
            <span class="text-lg font-normal text-gray-500">/month</span>
          </div>

          <ul class="space-y-3 mb-8">
            <li class="flex items-center text-gray-700">
              <span class="text-success-500 mr-2">✓</span>
              5 detections per day
            </li>
            <li class="flex items-center text-gray-700">
              <span class="text-success-500 mr-2">✓</span>
              5 humanize per day
            </li>
            <li class="flex items-center text-gray-700">
              <span class="text-success-500 mr-2">✓</span>
              Sentence-level analysis
            </li>
            <li class="flex items-center text-gray-400">
              <span class="mr-2">✗</span>
              Unlimited usage
            </li>
            <li class="flex items-center text-gray-400">
              <span class="mr-2">✗</span>
              Priority support
            </li>
          </ul>

          <button class="btn-secondary w-full py-3">
            Get Started
          </button>
        </div>

        <!-- 月付版 -->
        <div class="card p-8 border-2 border-primary-500 relative">
          <div class="absolute -top-3 left-1/2 transform -translate-x-1/2">
            <span class="bg-primary-600 text-white text-sm font-medium px-4 py-1 rounded-full">
              Popular
            </span>
          </div>

          <h2 class="text-xl font-semibold text-gray-900 mb-2">Monthly</h2>
          <p class="text-gray-600 mb-6">For regular users</p>
          <div class="text-4xl font-bold text-gray-900 mb-6">
            $9.9
            <span class="text-lg font-normal text-gray-500">/month</span>
          </div>

          <ul class="space-y-3 mb-8">
            <li class="flex items-center text-gray-700">
              <span class="text-success-500 mr-2">✓</span>
              Unlimited detections
            </li>
            <li class="flex items-center text-gray-700">
              <span class="text-success-500 mr-2">✓</span>
              Unlimited humanize
            </li>
            <li class="flex items-center text-gray-700">
              <span class="text-success-500 mr-2">✓</span>
              Sentence-level analysis
            </li>
            <li class="flex items-center text-gray-700">
              <span class="text-success-500 mr-2">✓</span>
              All rewrite strengths
            </li>
            <li class="flex items-center text-gray-700">
              <span class="text-success-500 mr-2">✓</span>
              Priority support
            </li>
          </ul>

          <button class="btn-primary w-full py-3">
            Subscribe Monthly
          </button>
        </div>

        <!-- 年付版 -->
        <div class="card p-8">
          <h2 class="text-xl font-semibold text-gray-900 mb-2">Yearly</h2>
          <p class="text-gray-600 mb-6">Best value for power users</p>
          <div class="text-4xl font-bold text-gray-900 mb-2">
            $79
            <span class="text-lg font-normal text-gray-500">/year</span>
          </div>
          <p class="text-success-600 font-medium mb-6">Save 33% (~$6.6/month)</p>

          <ul class="space-y-3 mb-8">
            <li class="flex items-center text-gray-700">
              <span class="text-success-500 mr-2">✓</span>
              Everything in Monthly
            </li>
            <li class="flex items-center text-gray-700">
              <span class="text-success-500 mr-2">✓</span>
              2 months free
            </li>
            <li class="flex items-center text-gray-700">
              <span class="text-success-500 mr-2">✓</span>
              Early access to new features
            </li>
            <li class="flex items-center text-gray-700">
              <span class="text-success-500 mr-2">✓</span>
              Dedicated support
            </li>
            <li class="flex items-center text-gray-700">
              <span class="text-success-500 mr-2">✓</span>
              API access (coming soon)
            </li>
          </ul>

          <button class="btn-primary w-full py-3">
            Subscribe Yearly
          </button>
        </div>
      </div>

      <!-- FAQ -->
      <div class="mt-20 max-w-3xl mx-auto">
        <h2 class="text-2xl font-bold text-gray-900 text-center mb-8">
          Frequently Asked Questions
        </h2>

        <div class="space-y-6">
          <div>
            <h3 class="text-lg font-medium text-gray-900 mb-2">
              Do I need to sign up to use the free tier?
            </h3>
            <p class="text-gray-600">
              No, you can use basic detection features without signing up. However, creating an account gives you more convenience and allows you to track your usage history.
            </p>
          </div>

          <div>
            <h3 class="text-lg font-medium text-gray-900 mb-2">
              Can I cancel my subscription anytime?
            </h3>
            <p class="text-gray-600">
              Yes, you can cancel your subscription at any time. You'll continue to have access until the end of your billing period.
            </p>
          </div>

          <div>
            <h3 class="text-lg font-medium text-gray-900 mb-2">
              What payment methods do you accept?
            </h3>
            <p class="text-gray-600">
              We currently accept PayPal and major credit cards through our secure payment processor.
            </p>
          </div>
        </div>
      </div>
    </main>

    <!-- 页脚 -->
    <footer class="py-8 px-4 border-t border-gray-200 mt-16">
      <div class="max-w-6xl mx-auto text-center text-gray-500">
        <p>© 2026 Unbot AI. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>
