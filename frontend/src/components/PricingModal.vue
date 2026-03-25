<script setup lang="ts">
/**
 * 定价弹窗组件

展示定价方案，支持免费版开始使用
*/
import { ref } from "vue"
import { useRouter } from "vue-router"

defineProps<{
  modelValue: boolean
}>()

const emit = defineEmits<{
  (e: "update:modelValue", value: boolean): void
}>()

const router = useRouter()

// 关闭弹窗
function close() {
  emit("update:modelValue", false)
}

// 免费版开始使用
function startFree() {
  close()
  router.push({ name: "register" })
}
</script>

<template>
  <Teleport to="body">
    <div
      v-if="modelValue"
      class="fixed inset-0 z-50 flex items-center justify-center p-4"
    >
      <!-- 遮罩层 -->
      <div
        class="absolute inset-0 bg-black/50"
        @click="close"
      />

      <!-- 弹窗内容 -->
      <div class="relative bg-white rounded-2xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <!-- 关闭按钮 -->
        <button
          @click="close"
          class="absolute top-4 right-4 text-gray-400 hover:text-gray-600 text-2xl w-8 h-8 flex items-center justify-center"
        >
          ×
        </button>

        <!-- 定价内容 -->
        <div class="p-8">
          <div class="text-center mb-8">
            <h2 class="text-3xl font-bold text-gray-900 mb-2">
              Simple, Transparent Pricing
            </h2>
            <p class="text-gray-600">
              Choose the plan that fits your needs
            </p>
          </div>

          <!-- 定价卡片 -->
          <div class="grid md:grid-cols-3 gap-6">
            <!-- 免费版 -->
            <div class="border border-gray-200 rounded-xl p-6">
              <h3 class="text-xl font-semibold text-gray-900 mb-2">Free</h3>
              <p class="text-gray-500 text-sm mb-4">Perfect for trying out</p>
              <div class="text-3xl font-bold text-gray-900 mb-4">
                $0
                <span class="text-base font-normal text-gray-500">/month</span>
              </div>

              <ul class="space-y-2 mb-6 text-sm">
                <li class="flex items-center text-gray-700">
                  <span class="text-green-500 mr-2">✓</span>
                  5 detections per day
                </li>
                <li class="flex items-center text-gray-700">
                  <span class="text-green-500 mr-2">✓</span>
                  5 humanize per day
                </li>
                <li class="flex items-center text-gray-700">
                  <span class="text-green-500 mr-2">✓</span>
                  Sentence-level analysis
                </li>
                <li class="flex items-center text-gray-400">
                  <span class="mr-2">✗</span>
                  Unlimited usage
                </li>
              </ul>

              <button
                @click="startFree"
                class="w-full py-2 px-4 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Get Started
              </button>
            </div>

            <!-- 月付版 -->
            <div class="border-2 border-blue-500 rounded-xl p-6 relative">
              <div class="absolute -top-3 left-1/2 transform -translate-x-1/2">
                <span class="bg-blue-500 text-white text-xs font-medium px-3 py-1 rounded-full">
                  Popular
                </span>
              </div>

              <h3 class="text-xl font-semibold text-gray-900 mb-2">Monthly</h3>
              <p class="text-gray-500 text-sm mb-4">For regular users</p>
              <div class="text-3xl font-bold text-gray-900 mb-4">
                $9.9
                <span class="text-base font-normal text-gray-500">/month</span>
              </div>

              <ul class="space-y-2 mb-6 text-sm">
                <li class="flex items-center text-gray-700">
                  <span class="text-green-500 mr-2">✓</span>
                  Unlimited detections
                </li>
                <li class="flex items-center text-gray-700">
                  <span class="text-green-500 mr-2">✓</span>
                  Unlimited humanize
                </li>
                <li class="flex items-center text-gray-700">
                  <span class="text-green-500 mr-2">✓</span>
                  Sentence-level analysis
                </li>
                <li class="flex items-center text-gray-700">
                  <span class="text-green-500 mr-2">✓</span>
                  All rewrite strengths
                </li>
              </ul>

              <button
                class="w-full py-2 px-4 bg-gray-100 text-gray-400 rounded-lg cursor-not-allowed"
                disabled
              >
                Coming Soon
              </button>
            </div>

            <!-- 年付版 -->
            <div class="border border-gray-200 rounded-xl p-6">
              <h3 class="text-xl font-semibold text-gray-900 mb-2">Yearly</h3>
              <p class="text-gray-500 text-sm mb-4">Best value for power users</p>
              <div class="text-3xl font-bold text-gray-900 mb-2">
                $79
                <span class="text-base font-normal text-gray-500">/year</span>
              </div>
              <p class="text-green-600 text-sm font-medium mb-4">Save 33% (~$6.6/month)</p>

              <ul class="space-y-2 mb-6 text-sm">
                <li class="flex items-center text-gray-700">
                  <span class="text-green-500 mr-2">✓</span>
                  Everything in Monthly
                </li>
                <li class="flex items-center text-gray-700">
                  <span class="text-green-500 mr-2">✓</span>
                  2 months free
                </li>
                <li class="flex items-center text-gray-700">
                  <span class="text-green-500 mr-2">✓</span>
                  Early access to new features
                </li>
              </ul>

              <button
                class="w-full py-2 px-4 bg-gray-100 text-gray-400 rounded-lg cursor-not-allowed"
                disabled
              >
                Coming Soon
              </button>
            </div>
          </div>

          <!-- FAQ -->
          <div class="mt-8 pt-8 border-t border-gray-200">
            <h3 class="text-lg font-semibold text-gray-900 mb-4 text-center">
              Frequently Asked Questions
            </h3>
            <div class="grid md:grid-cols-2 gap-4 text-sm">
              <div>
                <h4 class="font-medium text-gray-900 mb-1">
                  Do I need to sign up?
                </h4>
                <p class="text-gray-600">
                  No, you can use basic features without signing up.
                </p>
              </div>
              <div>
                <h4 class="font-medium text-gray-900 mb-1">
                  How does the daily limit work?
                </h4>
                <p class="text-gray-600">
                  Free users get 5 uses per day, resetting at midnight.
                </p>
              </div>
              <div>
                <h4 class="font-medium text-gray-900 mb-1">
                  Can I cancel anytime?
                </h4>
                <p class="text-gray-600">
                  Yes, cancel anytime. You'll keep access until your billing period ends.
                </p>
              </div>
              <div>
                <h4 class="font-medium text-gray-900 mb-1">
                  What payment methods?
                </h4>
                <p class="text-gray-600">
                  We accept PayPal and major credit cards.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>
