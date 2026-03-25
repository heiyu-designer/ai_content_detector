<script setup lang="ts">
/**
 * 句子卡片组件

显示单个句子的 AI 嫌疑分析
*/
import { computed } from "vue"
import type { SentenceCardProps } from "@/types"

const props = defineProps<SentenceCardProps>()

// 颜色配置
const levelConfig = computed(() => {
  switch (props.sentence.level) {
    case "high":
      return {
        bg: "bg-danger-50",
        border: "border-danger-200",
        badge: "badge-danger",
        icon: "🔴",
        label: "High",
      }
    case "medium":
      return {
        bg: "bg-warning-50",
        border: "border-warning-200",
        badge: "badge-warning",
        icon: "🟡",
        label: "Medium",
      }
    case "low":
      return {
        bg: "bg-success-50",
        border: "border-success-200",
        badge: "badge-success",
        icon: "🟢",
        label: "Low",
      }
    default:
      return {
        bg: "bg-gray-50",
        border: "border-gray-200",
        badge: "bg-gray-100 text-gray-800",
        icon: "⚪",
        label: "Unknown",
      }
  }
})
</script>

<template>
  <div
    :class="[
      'p-4 rounded-lg border transition-colors',
      levelConfig.bg,
      levelConfig.border,
    ]"
  >
    <div class="flex items-start justify-between">
      <!-- 句子内容 -->
      <div class="flex-1 pr-4">
        <p class="text-gray-900 leading-relaxed">
          {{ sentence.text }}
        </p>
        <!-- 分析原因 -->
        <p v-if="sentence.reason" class="mt-2 text-sm text-gray-600 italic">
          💡 {{ sentence.reason }}
        </p>
      </div>

      <!-- 嫌疑度标签 -->
      <div class="flex flex-col items-end space-y-1">
        <span :class="['badge', levelConfig.badge]">
          {{ levelConfig.icon }} {{ levelConfig.label }}
        </span>
        <span class="text-sm font-medium text-gray-700">
          {{ sentence.prob }}%
        </span>
      </div>
    </div>
  </div>
</template>
