/**
 * 待处理文本 Store

用于在页面间传递待检测/改写的文本
*/
import { defineStore } from "pinia"
import { ref } from "vue"

export const useTextStore = defineStore("text", () => {
  // 待处理的文本
  const pendingText = ref("")

  // 设置待处理文本
  function setText(text: string) {
    pendingText.value = text
  }

  // 获取并清空文本
  function getAndClearText(): string {
    const text = pendingText.value
    pendingText.value = ""
    return text
  }

  // 清空文本
  function clearText() {
    pendingText.value = ""
  }

  return {
    pendingText,
    setText,
    getAndClearText,
    clearText,
  }
})
