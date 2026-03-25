# AI Content Detector + Humanizer
## MVP 产品手册

> 版本：v1.0
> 日期：2026-03-23
> 产品名代号：Unbot AI
> 开发周期：一周

---

## 一、产品定位

### 一句话定位
帮助用户检测文本是否由 AI 生成，并将 AI 味文本改写成更像人类写作的工具。

### 核心用户
- **内容创作者**：博主、写手、SEO 工作者
- **教育工作者**：老师、内容审核者
- **求职者**：需要撰写简历、自荐信

### 用户核心痛点
1. 不确定自己写的内容是否"AI 味太重"
2. 希望改写后保留原意但更像真人写的
3. 不想注册就能快速验证

### 产品口号建议
> *"Know if it's AI. Make it human."*

---

## 二、核心功能（MVP 范围）

### 2.1 免费功能（无需注册）

| 功能 | 描述 | 限制 |
|------|------|------|
| AI 文本检测 | 粘贴任意文本，返回 AI 概率和人类概率 | 5次/天 |
| 句子级别高亮 | 标出最可能由 AI 生成的句子 | ✅ |
| 一键 Humanize | 将检测结果一键改写成人类风格 | 5次/天 |
| 改写强度选择 | 轻度 / 中度 / 深度 三档可选 | ✅ |

### 2.2 付费功能（会员解锁）

| 功能 | 描述 | 价格策略 |
|------|------|---------|
| 无限检测 | 解除每日5次限制 | 会员专属 |
| 无限 Humanize | 解除每日5次限制 | 会员专属 |
| 批量检测 | 一次上传多个文件/多段文本 | 会员专属 |
| 历史记录 | 保存最近30天的检测记录 | 会员专属 |
| 详细报告导出 | 生成 PDF 报告 | 会员专属 |

### 2.3 不在 MVP 范围的功能

- 用户注册/登录系统
- API 访问
- Chrome 插件
- 多语言界面（仅中英双语内容检测）
- 移动端适配

---

## 三、用户体验流程

### 3.1 用户路径图

```
┌─────────────────────────────────────────────────────┐
│                      首页                            │
│         [Logo]  Unbot AI                           │
│                                                     │
│    ┌───────────────────────────────────────┐       │
│    │  粘贴或输入文本...                      │       │
│    │                                        │       │
│    │                                        │       │
│    └───────────────────────────────────────┘       │
│                                                     │
│         [ 🔍 检测 AI ]  [ ✍️ Humanize ]           │
│                                                     │
│         今日剩余次数：5 / 5                         │
│                                                     │
│    ─────────── 或 ───────────                       │
│                                                     │
│    [📁 拖拽文件上传]  支持 .txt .docx .pdf          │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 3.2 检测结果页

```
┌─────────────────────────────────────────────────────┐
│                    检测结果                          │
│                                                     │
│   AI 生成概率          人类写作概率                  │
│   ████████████░░ 82%  ██░░░░░░░░░░ 18%             │
│                                                     │
│   句子级别分析：                                      │
│   ┌─────────────────────────────────────────┐      │
│   │ The evolution of technology has...     │ 🔴   │
│   │ [AI 嫌疑度 92%]                          │      │
│   ├─────────────────────────────────────────┤      │
│   │ I believe this topic matters because.. │ 🟡   │
│   │ [AI 嫌疑度 67%]                          │      │
│   ├─────────────────────────────────────────┤      │
│   │ Let me share my personal experience...  │ 🟢   │
│   │ [AI 嫌疑度 12%]                          │      │
│   └─────────────────────────────────────────┘      │
│                                                     │
│   改写建议强度：  [轻度] [中度●] [深度]              │
│                                                     │
│   [ ✍️ Humanize 改写 ]                              │
│                                                     │
│   ───────────────────────────────                   │
│   升级会员解锁无限次检测和改写                        │
│   [ ⭐ 立即升级 ]                                   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 3.3 Humanize 改写结果页

```
┌─────────────────────────────────────────────────────┐
│                    Humanize 结果                    │
│                                                     │
│   改写强度：中度                                      │
│                                                     │
│   ┌─────────────────┐  ┌─────────────────┐         │
│   │ 原文              │  │ 改写后           │         │
│   ├─────────────────┤  ├─────────────────┤         │
│   │ The rapid       │  │ Tech's moving so │         │
│   │ advancement of  │→ │ fast these days. │         │
│   │ artificial      │  │ I remember when  │         │
│   │ intelligence... │  │ AI was just...  │         │
│   └─────────────────┘  └─────────────────┘         │
│                                                     │
│   [ 📋 复制改写结果 ]  [ 🔄 再改一次 ]               │
│                                                     │
│   今日剩余次数：4 / 5                               │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 四、UI/UX 设计规范

### 4.1 设计风格

| 属性 | 规范 |
|------|------|
| 风格 | 简洁、现代、工具属性强 |
| 配色 | 主色 #2563EB（蓝），辅助 #10B981（绿），警示 #EF4444（红） |
| 字体 | Inter + Noto Sans SC（中文） |
| 布局 | 单页应用，左文右图或上下结构 |
| 交互 | 强调无门槛——无需注册，直接使用 |

### 4.2 颜色语义

| 颜色 | 用途 |
|------|------|
| 🔵 蓝色 | 主操作按钮、Logo |
| 🟢 绿色 | 人类写作概率条、低嫌疑句子 |
| 🔴 红色 | AI 生成概率条、高嫌疑句子 |
| 🟡 黄色 | 中等嫌疑句子 |
| ⚪ 灰色 | 次要文字、禁用状态 |

### 4.3 组件清单

| 组件 | 状态 |
|------|------|
| 文本输入框 | 默认 / 聚焦 / 内容已输入 |
| 主按钮 | 默认 / Hover / Loading / Disabled |
| 概率条 | 动态填充 |
| 句子卡片 | 高嫌疑 / 中嫌疑 / 低嫌疑 |
| 次数显示 | 正常（5/5）/ 警告（1/5）/ 已用完（0/5） |
| 升级弹窗 | 触发时机：次数用完 或 检测完成后 |

---

## 五、技术架构

### 5.1 技术栈

| 层级 | 技术选型 | 说明 |
|------|---------|------|
| 前端 | Vue 3 + Vite + TailwindCSS | SPA 单页应用 |
| 后端 | Node.js + Express | RESTful API |
| 数据库 | PostgreSQL | 用户数据、历史记录 |
| 缓存/计数 | Redis | 免费次数统计、API 响应缓存 |
| AI 检测 | **GPTZero API**（默认）+ 接口抽象 | 可切换其他供应商 |
| AI 改写 | **OpenAI GPT-4o / Claude API** | Humanize 改写 |
| 部署 | Docker + 你的4核8G服务器 | 容器化部署 |

### 5.2 系统架构图

```
                    ┌──────────────┐
                    │   Nginx      │
                    │  (反向代理)   │
                    └──────┬───────┘
                           │
              ┌────────────┴────────────┐
              │                        │
        ┌─────┴─────┐          ┌──────┴──────┐
        │  前端静态  │          │   API Server │
        │  (Vue 3)  │          │  (Node.js)   │
        └───────────┘          └──────┬──────┘
                                       │
         ┌──────────────────────────────┼──────────────┐
         │                              │              │
         ▼                              ▼              ▼
  ┌─────────────┐              ┌─────────────┐  ┌─────────────┐
  │   Redis     │              │  PostgreSQL │  │ AI Provider │
  │ (次数统计)   │              │  (用户/数据) │  │ (GPTZero)  │
  └─────────────┘              └─────────────┘  └──────┬─────┘
                                                       │
                                              ┌────────┴────────┐
                                              │  Humanize API  │
                                              │ (OpenAI/Claude)│
                                              └────────────────┘
```

### 5.3 核心接口设计

#### POST /api/v1/detect
```
请求：
{
  "text": "需要检测的文本内容",
  "lang": "en" // or "zh"
}

响应：
{
  "success": true,
  "data": {
    "ai_probability": 82,
    "human_probability": 18,
    "sentence_analysis": [
      { "text": "The evolution of technology has...", "prob": 92, "level": "high" },
      { "text": "I believe this topic matters...", "prob": 45, "level": "medium" },
      { "text": "Let me share my personal experience...", "prob": 12, "level": "low" }
    ],
    "remaining_quota": 4
  }
}
```

#### POST /api/v1/humanize
```
请求：
{
  "text": "需要改写的文本",
  "strength": "medium", // "light" | "medium" | "deep"
  "lang": "en"
}

响应：
{
  "success": true,
  "data": {
    "original": "The evolution of technology...",
    "rewritten": "Tech's moving so fast these days...",
    "remaining_quota": 3
  }
}
```

#### GET /api/v1/quota
```
响应：
{
  "success": true,
  "data": {
    "daily_limit": 5,
    "used": 2,
    "remaining": 3,
    "reset_at": "2026-03-24T00:00:00Z"
  }
}
```

### 5.4 数据模型

#### 用户表 (users)
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  is_premium BOOLEAN DEFAULT FALSE,
  premium_expires_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

#### 检测记录表 (detections)
```sql
CREATE TABLE detections (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  session_id VARCHAR(255), -- 未登录用户基于 cookie
  text_hash VARCHAR(64),   -- 文本哈希，用于去重
  text_preview VARCHAR(200),
  ai_probability INTEGER,
  human_probability INTEGER,
  sentence_count INTEGER,
  lang VARCHAR(10),
  created_at TIMESTAMP DEFAULT NOW()
);
```

#### 次数统计 (daily_usage)
```sql
CREATE TABLE daily_usage (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  session_id VARCHAR(255),
  usage_date DATE,
  detect_count INTEGER DEFAULT 0,
  humanize_count INTEGER DEFAULT 0,
  PRIMARY KEY (user_id, session_id, usage_date)
);
```

---

## 六、Humanize 实现方案

### 6.1 改写策略

| 强度 | Prompt 策略 |
|------|-----------|
| 轻度 | 保留原意，仅调整词汇和句式 |
| 中度 | 加入口语化表达、个人经历暗示 |
| 深度 | 完全重写，保持核心观点但风格大变 |

### 6.2 Humanize Prompt 示例（中度）

```
You are a human text rewriter. Rewrite the following AI-generated text
to sound more naturally human-written.

Rules:
- Keep the core meaning and key points
- Add natural variations in sentence length
- Include occasional contractions and colloquialisms
- Vary the sentence structure
- Add subtle "human" markers (first-person, anecdotes hints)

Original text:
[USER_TEXT]

Rewritten text:
```

### 6.3 安全边界

**禁止改写的内容**（检测并拒绝）：
- 明显恶意、歧视性内容
- 违法信息
- 医疗、法律等专业领域的正式文件

---

## 七、免费次数策略

### 7.1 次数控制逻辑

```
1. 用户首次访问 → 生成 session_id（存 Cookie）
2. 每次检测/改写 → 调用 /api/v1/quota 检查
3. 检查 Redis key: `quota:{session_id}:{date}`
4. 未登录用户：共用5次/天（检测+改写合计）
5. 已登录用户：独立计数，升级会员后解除限制
```

### 7.2 次数用完后的引导

```
触发时机：用户点击第6次操作时

引导流程：
1. 显示弹窗："今日免费次数已用完"
2. 展示产品价值：展示了检测结果，但改写需升级
3. 两个选项：
   - "注册账号，再获5次免费"（引导注册）
   - "升级会员，无限使用"（直接付费）
4. 同时提供"明天再来"的无压力选项
```

### 7.3 Redis Key 设计

```
quota:session:{session_id}:{YYYY-MM-DD}
  → { detect: 3, humanize: 2 }

quota:user:{user_id}:{YYYY-MM-DD}
  → { detect: 10, humanize: 8, is_premium: true }
```

---

## 八、SEO 策略

### 8.1 目标关键词

| 优先级 | 关键词 | 意图 |
|--------|--------|------|
| Primary | AI content detector | 信息型 |
| Primary | AI checker free | 交易型 |
| Secondary | detect AI written text | 信息型 |
| Secondary | AI humanizer | 交易型 |
| Long-tail | how to make AI text sound human | 信息型 |
| Long-tail | free AI detector no sign up | 交易型 |
| 中文 | AI检测免费 / AI文章检测 | 信息型 |

### 8.2 SEO 页面规划

| 页面 | 目标关键词 | 内容方向 |
|------|-----------|---------|
| 首页 | AI content detector | 工具入口 + 核心价值 |
| /blog/ai-detection-guide | how to detect AI written text | SEO 教程文章 |
| /blog/ai-humanizer-guide | AI humanizer | 工具教程 + 教程文章 |
| /pricing | AI detector pricing | 定价页 |

### 8.3 技术 SEO

- Core Web Vitals 优化（LCP < 2.5s）
- 结构化数据（Schema.org: WebApplication）
- Open Graph + Twitter Card
- Sitemap 自动生成
- robots.txt 配置

---

## 九、支付方案

### 9.1 定价策略

| 套餐 | 价格 | 说明 |
|------|------|------|
| 免费 | $0 | 5次/天 |
| 月付 | $9.9/月 | 无限次 |
| 年付 | $79/年 | 约 $6.6/月，节省33% |

### 9.2 支付接入

| 方案 | 接入难度 | 手续费 | 推荐度 |
|------|---------|--------|--------|
| Stripe | 中 | 2.9% + $0.3 | ✅ 推荐 |
| LemonSqueezy | 易 | 5% + $0.5 | 适合独立开发者 |
| Paddle | 易 | 5% + $0.3 | 偏SaaS |

**建议**：先接入 Stripe，技术成熟、用户信任度高。

### 9.3 会员系统简化

MVP 阶段会员逻辑：
1. 用户注册 → 普通账号（5次/天）
2. 购买会员 → `is_premium = true`
3. 不做复杂的订阅管理，先用 Stripe Checkout + Webhook 更新状态

---

## 十、开发计划（两周冲刺）

### Week 1：核心功能

| 天数 | 任务 | 交付物 |
|------|------|--------|
| Day 1-2 | 项目初始化：Vue3 + Vite + TailwindCSS + Node.js + Express | 可运行的空项目 |
| Day 3 | 主页 UI：文本输入框 + 主按钮 + 结果展示 | 静态页面 |
| Day 4 | 后端 API：detect 接口 + GPTZero 接入 | API 可用 |
| Day 5-6 | 检测结果展示：概率条 + 句子高亮 | 完整检测流程 |
| Day 7 | Humanize 接口接入 | 改写功能完成 |

### Week 2：完整功能

| 天数 | 任务 | 交付物 |
|------|------|--------|
| Day 8 | 次数限制系统：Redis 集成 | 限流功能 |
| Day 9-10 | 用户注册/登录 + JWT | 账户系统 |
| Day 11 | 升级弹窗 + Stripe 接入 | 支付流程 |
| Day 12 | 响应式适配 + 细节打磨 | 移动端适配 |
| Day 13 | 部署：Docker + Nginx + 域名 | 可访问的产品 |
| Day 14 | Bug 修复 + 监控接入 | 上线发布 |

---

## 十一、MVP 发布检查清单

### 功能检查
- [ ] 文本检测正常工作
- [ ] Humanize 改写正常输出
- [ ] 句子级别高亮准确
- [ ] 5次免费限制生效
- [ ] 升级弹窗正常弹出
- [ ] 用户注册/登录流程通
- [ ] Stripe 支付流程通

### 技术检查
- [ ] Redis 限流正常
- [ ] AI API 异常有降级处理
- [ ] 前端错误边界
- [ ] 日志记录完整
- [ ] HTTPS 配置
- [ ] 域名解析

### SEO 检查
- [ ] Meta title/description
- [ ] Sitemap 生成
- [ ] robots.txt
- [ ] 结构化数据

---

## 十二、风险与对策

| 风险 | 应对策略 |
|------|---------|
| GPTZero API 不稳定 | 抽象接口，准备备选（如 Copyleaks） |
| AI 检测准确率不高 | 诚实告知用户，提供置信度区间 |
| 被滥用做学术作弊 | 加免责声明，但工具本身无责 |
| Claude/OpenAI API 成本高 | 设置每用户调用上限，监控异常调用 |
| 竞品快速复制 | 快速迭代，保持体验差异化 |

---

## 附录

### A. 竞品参考
- **GPTZero** - 最知名竞品，定位教育市场
- **QuillBot** - Humanize + 检测结合
- **Undetectable AI** - 强调改写效果
- **Copyleaks** - 企业级，功能全

### B. 域名建议
- `unbot.ai` - 产品名直接相关
- `aicheckerpro.com` - 功能导向
- `humanizeai.io` - 差异化导向

### C. Logo 方向
- 机器人 / AI → 人类（变形方向）
- 盾牌 + 勾选（检测感）
- 简洁文字 + 一个独特符号

---

*本手册为 MVP 版本，后续根据用户反馈迭代。*
