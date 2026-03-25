<script setup lang="ts">
/**
 * 概率条组件

显示 AI/人类概率
*/
import { computed } from "vue"
import type { ProgressBarProps } from "@/types"

const props = withDefaults(defineProps<ProgressBarProps>(), {
  max: 100,
  color: "primary",
  showLabel: true,
})

// 计算百分比
const percentage = computed(() => {
  return Math.min(100, Math.max(0, (props.value / props.max) * 100))
})

// 颜色映射
const colorClasses = computed(() => {
  switch (props.color) {
    case "primary":
      return "bg-primary-600"
    case "success":
      return "bg-success-500"
    case "danger":
      return "bg-danger-500"
    default:
      return "bg-primary-600"
  }
})
</script>

<template>
  <div class="w-full">
    <div
      v-if="showLabel"
      class="flex items-center justify-between mb-1 text-sm"
    >
      <span class="text-gray-600">Probability</span>
      <span class="font-medium text-gray-900">{{ value }}%</span>
    </div>
    <div class="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
      <div
        :class="['h-full rounded-full transition-all duration-500', colorClasses]"
        :style="{ width: `${percentage}%` }"
      />
    </div>
  </div>
</template>
