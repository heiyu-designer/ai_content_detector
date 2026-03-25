/**
 * API 请求和响应的类型定义
 */

// 语言类型
export type Language = "en" | "zh"

// 改写强度
export type RewriteStrength = "light" | "medium" | "deep"

// 嫌疑等级
export type SuspicionLevel = "high" | "medium" | "low"

// ============== 通用响应 ==============

/**
 * 统一 API 响应格式
 */
export interface ApiResponse<T = unknown> {
  success: boolean
  data?: T
  message?: string
}

/**
 * 错误响应
 */
export interface ErrorResponse {
  success: false
  error: {
    code: string
    message: string
    details?: unknown
  }
}

// ============== 检测相关 ==============

/**
 * AI 检测请求
 */
export interface DetectRequest {
  text: string
  lang: Language
}

/**
 * 句子级别分析结果
 */
export interface SentenceAnalysis {
  text: string
  prob: number
  level: SuspicionLevel
  reason?: string
}

/**
 * AI 检测响应
 */
export interface DetectResponse {
  ai_probability: number
  human_probability: number
  sentence_analysis: SentenceAnalysis[]
  remaining_quota: number
  summary?: string
  patterns?: {
    ai_markers?: string[]
    human_markers?: string[]
  }
}

// ============== Humanize 相关 ==============

/**
 * Humanize 改写请求
 */
export interface HumanizeRequest {
  text: string
  strength: RewriteStrength
  lang: Language
}

/**
 * Humanize 改写响应
 */
export interface HumanizeResponse {
  original: string
  rewritten: string
  remaining_quota: number
}

// ============== 配额相关 ==============

/**
 * 配额响应
 */
export interface QuotaResponse {
  daily_limit: number
  used: number
  remaining: number
  reset_at: string
}

// ============== 用户认证相关 ==============

/**
 * 用户注册请求
 */
export interface RegisterRequest {
  email: string
  password: string
}

/**
 * 用户登录请求
 */
export interface LoginRequest {
  email: string
  password: string
}

/**
 * 用户信息
 */
export interface User {
  id: string
  email: string
  is_premium: boolean
  premium_expires_at: string | null
  created_at: string
}

/**
 * 登录响应
 */
export interface LoginResponse {
  success: boolean
  user: User
  token: {
    access_token: string
    token_type: string
    expires_in: number
  }
}

// ============== 组件 Props 类型 ==============

/**
 * 概率条组件 Props
 */
export interface ProgressBarProps {
  value: number
  max?: number
  color?: "primary" | "success" | "danger"
  showLabel?: boolean
}

/**
 * 句子卡片组件 Props
 */
export interface SentenceCardProps {
  sentence: SentenceAnalysis
  index: number
}
