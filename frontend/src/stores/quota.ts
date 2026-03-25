/**
 * 配额 Store

管理用户配额状态
*/
import { defineStore } from "pinia"
import { ref, computed } from "vue"
import { getQuota } from "@/services/api"
import type { QuotaResponse } from "@/types"

export const useQuotaStore = defineStore("quota", () => {
  // 状态
  const quota = ref<QuotaResponse | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // 计算属性
  const remaining = computed(() => quota.value?.remaining ?? 0)
  const dailyLimit = computed(() => quota.value?.daily_limit ?? 5)
  const used = computed(() => quota.value?.used ?? 0)
  const isPremium = computed(() => remaining.value === -1)
  const isQuotaExhausted = computed(() => remaining.value === 0)

  // 获取配额
  async function fetchQuota() {
    isLoading.value = true
    error.value = null

    try {
      quota.value = await getQuota()
    } catch (e) {
      error.value = e instanceof Error ? e.message : "获取配额失败"
      console.error("获取配额失败:", e)
    } finally {
      isLoading.value = false
    }
  }

  // 更新配额（从检测/改写响应中）
  function updateQuota(newRemaining: number) {
    if (quota.value) {
      quota.value.remaining = newRemaining
      quota.value.used += 1
    }
  }

  // 重置配额
  function resetQuota() {
    quota.value = null
  }

  return {
    // 状态
    quota,
    isLoading,
    error,
    // 计算属性
    remaining,
    dailyLimit,
    used,
    isPremium,
    isQuotaExhausted,
    // 方法
    fetchQuota,
    updateQuota,
    resetQuota,
  }
})
