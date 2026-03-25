# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 在本仓库中工作时提供指导。

## 语言要求

- **所有对话使用中文汇报**
- **文档类文件以中文为主编写**

## 项目概述

**Unbot AI** 是一款 AI 内容检测与人性化改写工具，能够检测文本是否由 AI 生成，并将 AI 风格的文本改写得更像真人写作。

- **前端**: Vue 3 + Vite + TailwindCSS + TypeScript + Pinia
- **后端**: Python FastAPI
- **数据库**: MySQL 8.0
- **缓存**: Redis 7
- **AI 提供商**: MiniMax API（抽象层支持切换提供商）
- **部署**: Docker + Docker Compose

---

## 常用命令

### 后端

```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 运行开发服务器（端口 30001）
uvicorn app.main:app --reload --port 30001

# 格式化代码
black app/
isort app/

# Docker 方式（代码修改后需重新构建）
docker-compose up -d --build backend
docker-compose logs -f backend
```

### 前端

```bash
cd frontend

# 安装依赖
npm install

# 运行开发服务器（Vite）
npm run dev

# 生产构建
npm run build

# 代码检查和格式化
npm run lint
npm run format
npm run type-check
```

### Docker（完整栈）

```bash
# 启动所有服务（MySQL + Redis + 后端）
docker-compose up -d

# 查看日志
docker-compose logs -f

# 代码修改后重启后端
docker restart unbot_backend

# 测试时重置 Redis 配额
docker exec unbot_redis redis-cli FLUSHDB
```

---

## 架构设计

### 后端结构 (`backend/app/`)

```
app/
├── main.py              # FastAPI 入口，lifespan，CORS，异常处理器
├── core/                # 核心基础设施
│   ├── config.py        # 配置（通过 pydantic-settings 读取环境变量）
│   ├── database.py      # MySQL/SQLAlchemy 异步初始化
│   ├── redis_client.py  # Redis 单例（配额追踪、缓存）
│   └── exceptions.py     # APIException 异常体系
├── routers/             # API 路由处理器
│   ├── detect.py         # POST /api/v1/detect
│   ├── humanize.py       # POST /api/v1/humanize
│   ├── quota.py          # GET /api/v1/quota
│   └── auth.py           # 认证接口（register, login, /me）
├── schemas/              # Pydantic 请求/响应模型
├── services/
│   ├── ai_provider/      # AI 提供商抽象层
│   │   ├── base.py       # BaseAIProvider 抽象类 + AIProviderFactory
│   │   └── minimax.py    # MiniMax 实现
│   └── quota_service.py  # 配额检查逻辑
├── models/               # SQLAlchemy ORM 模型
└── utils/
    └── api_retry.py      # 第三方 API 重试封装（带超时、指数退避）
```

### Docker/Nginx 配置 (`docker/`)

```
docker/
├── mysql/
│   └── init.sql          # MySQL 初始化脚本（建表语句）
└── nginx/
    ├── nginx.conf        # Nginx 主配置（Gzip、Worker、连接数）
    └── conf.d/
        └── unbot.conf    # 站点配置（SPA 路由、API 代理、SSL）
```

### 前端结构 (`frontend/src/`)

```
src/
├── main.ts              # Vue 应用入口
├── App.vue              # 根组件
├── router/index.ts      # Vue Router（含路由守卫：已登录用户访问 login/register 时跳转首页）
├── stores/              # Pinia 状态管理
│   ├── auth.ts          # 认证状态（isAuthenticated, userEmail, isPremium, logout）
│   ├── quota.ts         # 配额状态（remaining, dailyLimit, fetchQuota, updateQuota）
│   └── text.ts          # 视图间共享文本（避免 URL 参数传递长文本）
├── services/api.ts      # Axios API 客户端
├── types/index.ts        # TypeScript 接口定义
├── components/           # 可复用组件
│   └── PricingModal.vue  # 定价弹窗（支持 Free/Monthly/Yearly 套餐）
└── views/               # 页面组件
    ├── HomeView.vue      # 首页（文本输入 + Detect/Humanize 按钮 + 定价弹窗）
    ├── DetectView.vue    # 检测页面（概率展示 + 句子分析 + Humanize 跳转）
    ├── HumanizeView.vue  # 改写页面（原文/改写对比 + 复制/重写功能）
    ├── LoginView.vue    # 登录页面
    ├── RegisterView.vue  # 注册页面
    └── PricingView.vue   # 定价页面
```

### API 响应格式

所有 API 响应遵循以下结构：
```json
// 成功响应
{ "success": true, "data": { ... } }

// 错误响应
{ "success": false, "error": { "code": "QUOTA_EXCEEDED", "message": "..." } }
```

---

## 核心设计模式

### AI 提供商抽象层 (`app/services/ai_provider/`)

AI 层采用**策略模式**结合工厂模式：
- `BaseAIProvider` 是定义 `detect_ai()` 和 `humanize()` 方法的抽象基类
- `AIProviderFactory.get_provider("minimax")` 返回对应的提供商实例
- 目前仅实现了 MiniMax；可通过实现 `BaseAIProvider` 添加 OpenAI/Anthropic
- 所有第三方 API 调用必须使用 `app/utils/api_retry.py` 中的重试封装

### 配额系统

- 使用 Redis，key 模式：`quota:{identifier}:{date}`（如 `quota:abc123:2026-03-24`）
- 每日免费配额：5 次（可通过 `daily_free_quota` 配置）
- 检测和改写共用同一个配额计数器
- 会员用户跳过配额检查（`is_premium=True`）

### 视图间传递文本

长文本**不通过** URL 查询参数传递（安全性和长度限制考虑）。替代方案：
- `HomeView.vue` 使用 `useTextStore().setText()` 存储文本
- `DetectView.vue` 和 `HumanizeView.vue` 在挂载时从 store 读取
- 读取后清空 store

### 登录状态 UI

前端使用 Pinia `useAuthStore` 管理登录状态：
- `isAuthenticated` - 是否已登录
- `userEmail` - 用户邮箱
- `isPremium` - 是否会员
- `logout()` - 退出登录

**路由守卫逻辑**：
- 已登录用户访问 `login/register` 页面时自动跳转到首页
- 在 `router/index.ts` 中通过 `to.meta.guest` 判断

### 定价弹窗

`PricingModal.vue` 是全站统一的定价弹窗组件：
- 三个套餐：Free（5次/天）、Monthly（$9.9/月）、Yearly（$79/年）
- "Get Started" 按钮跳转到注册页面
- 月付/年付按钮当前显示 "Coming Soon"

---

## 文档索引

| 文档 | 说明 |
|------|------|
| [DEPLOYMENT.md](DEPLOYMENT.md) | 完整服务器部署指南（从零开始安装 Docker 到生产环境上线） |
| [README.md](README.md) | 项目整体介绍、技术栈、快速启动 |
| [ISSUES_AND_FIXES.md](ISSUES_AND_FIXES.md) | 历史问题追踪与修复记录 |

---

## 常见问题与修复

完整的问题追踪见 [ISSUES_AND_FIXES.md](ISSUES_AND_FIXES.md)。关键问题：

| 问题 | 修复 |
|------|------|
| 后端修改不生效 | 运行 `docker restart unbot_backend`（Python 模块缓存） |
| 测试时配额耗尽 | `docker exec unbot_redis redis-cli FLUSHDB` |
| MiniMax API 404 错误 | 端点应为 `/v1/text/chatcompletion_v2`（不是 `/v1/text detection`） |
| Humanize 语言切换为英文 | 在提示词中强制指定输出语言，自动检测输入语言 |
| 句子分割破坏版本号 | 模型调用后使用 Python `_split_sentences()` 分割，而非让模型分割 |
| 前端显示"配额已用完"但实际还有配额 | 后端返回未包装的 JSON；前端期望 `response.data` 而非 `response.data.data` |
| 注册接口报"服务器内部错误" | 确认 `bcrypt==4.1.2` 已安装（与 passlib 兼容版本） |
| 注册/登录后 /me 接口失败 | 检查 `authorization` 参数是否使用 `Header(None)` 声明 |

---

## 开发规范

### Python 后端
- **类型提示**：所有函数必须使用类型注解
- **函数长度**：单个函数不超过 20 行（超出需拆分）
- **注释**：使用中文注释
- **异步**：所有 I/O 操作使用 `async/await`
- **格式化**：`black` + `isort`
- **第三方 API 调用**：必须使用 `app/utils/api_retry.py` 中的重试封装

### 前端
- **TypeScript**：避免使用 `any`；使用 `types/index.ts` 中的接口
- **Vue**：Composition API，`<script setup>`
- **样式**：仅使用 TailwindCSS（不使用行内样式）

### Git
- 分支命名：`feature/<name>`、`bugfix/<name>`、`hotfix/<name>`
- 提交格式：`type(scope): subject`（如 `feat(detect): 添加句子分析`）

---

## 环境变量

详见 `.env.example`。关键变量：
- `MINIMAX_API_KEY` / `MINIMAX_API_BASE` - AI 提供商
- `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD` - MySQL
- `REDIS_HOST`, `REDIS_PORT` - Redis
- `JWT_SECRET_KEY` - Token 签名
- `daily_free_quota` - 默认 5
