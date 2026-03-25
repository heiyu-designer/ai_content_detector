/**
 * API 服务层

封装所有 API 调用
*/
import axios, { AxiosError } from "axios"
import type {
  DetectRequest,
  DetectResponse,
  ErrorResponse,
  HumanizeRequest,
  HumanizeResponse,
  LoginRequest,
  LoginResponse,
  QuotaResponse,
  RegisterRequest,
} from "@/types"

// API 基础配置
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "/api/v1"

// 创建 axios 实例
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000,
  headers: {
    "Content-Type": "application/json",
  },
})

// 请求拦截器：添加 Token
apiClient.interceptors.request.use(
  (config) => {
    // 从 localStorage 获取 token
    const token = localStorage.getItem("access_token")
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器：统一错误处理
apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  (error: AxiosError<ErrorResponse | { detail: unknown }>) => {
    const data = error.response?.data as Record<string, unknown> | undefined

    // 业务错误
    if (data?.error && typeof data.error === "object") {
      const err = data.error as { message?: string }
      return Promise.reject(new Error(err.message || "请求失败"))
    }

    // FastAPI 验证错误
    if (data?.detail) {
      const detail = data.detail
      if (typeof detail === "string") {
        return Promise.reject(new Error(detail))
      }
      if (Array.isArray(detail) && detail[0]?.msg) {
        return Promise.reject(new Error(detail[0].msg))
      }
    }

    // 网络错误
    if (error.code === "ECONNABORTED") {
      return Promise.reject(new Error("请求超时，请稍后重试"))
    }

    return Promise.reject(new Error("网络错误，请检查网络连接"))
  }
)

// ============== API 接口 ==============

/**
 * AI 检测接口
 */
export async function detectText(
  params: DetectRequest
): Promise<DetectResponse> {
  const response = await apiClient.post<DetectResponse>("/detect", params)
  return response.data
}

/**
 * Humanize 改写接口
 */
export async function humanizeText(
  params: HumanizeRequest
): Promise<HumanizeResponse> {
  const response = await apiClient.post<HumanizeResponse>("/humanize", params)
  return response.data
}

/**
 * 查询配额接口
 */
export async function getQuota(): Promise<QuotaResponse> {
  const response = await apiClient.get<QuotaResponse>("/quota")
  return response.data
}

// ============== 认证接口 ==============

/**
 * 用户注册
 */
export async function register(
  params: RegisterRequest
): Promise<LoginResponse> {
  const response = await apiClient.post<LoginResponse>("/auth/register", params)
  return response.data
}

/**
 * 用户登录
 */
export async function login(params: LoginRequest): Promise<LoginResponse> {
  const response = await apiClient.post<LoginResponse>("/auth/login", params)
  return response.data
}

/**
 * 获取当前用户信息
 */
export async function getCurrentUser(): Promise<{ user: unknown }> {
  const response = await apiClient.get("/auth/me")
  return response.data
}

// 导出 apiClient 供其他地方使用
export { apiClient }
