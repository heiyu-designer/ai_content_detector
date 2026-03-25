/**
 * Vue Router 配置
*/
import { createRouter, createWebHistory } from "vue-router"
import type { RouteRecordRaw } from "vue-router"
import { useAuthStore } from "@/stores/auth"

// 路由配置
const routes: RouteRecordRaw[] = [
  {
    path: "/",
    name: "home",
    component: () => import("@/views/HomeView.vue"),
    meta: {
      title: "Unbot AI - AI Content Detector & Humanizer",
    },
  },
  {
    path: "/detect",
    name: "detect",
    component: () => import("@/views/DetectView.vue"),
    meta: {
      title: "AI Detection - Unbot AI",
    },
  },
  {
    path: "/humanize",
    name: "humanize",
    component: () => import("@/views/HumanizeView.vue"),
    meta: {
      title: "Humanize - Unbot AI",
    },
  },
  {
    path: "/login",
    name: "login",
    component: () => import("@/views/LoginView.vue"),
    meta: {
      title: "Login - Unbot AI",
      guest: true, // 游客可访问
    },
  },
  {
    path: "/register",
    name: "register",
    component: () => import("@/views/RegisterView.vue"),
    meta: {
      title: "Register - Unbot AI",
      guest: true,
    },
  },
  {
    path: "/pricing",
    name: "pricing",
    component: () => import("@/views/PricingView.vue"),
    meta: {
      title: "Pricing - Unbot AI",
    },
  },
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})

// 路由守卫
router.beforeEach((to, _from, next) => {
  const authStore = useAuthStore()

  // 已登录用户访问 login/register 页面时跳转到首页
  if (to.meta.guest && authStore.isAuthenticated) {
    next({ name: "home" })
    return
  }

  // 更新页面标题
  const title = to.meta.title as string | undefined
  if (title) {
    document.title = title
  } else {
    document.title = "Unbot AI"
  }

  next()
})

export default router
