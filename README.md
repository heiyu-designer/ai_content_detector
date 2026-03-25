# Unbot AI - AI Content Detector & Humanizer

> *"Know if it's AI. Make it human."*

---

## 一、项目简介

**Unbot AI** 是一款帮助用户检测文本是否由 AI 生成，并将 AI 味文本改写成更像人类写作的工具。

### 核心功能

- **AI 文本检测**：粘贴任意文本，返回 AI 概率和人类概率
- **句子级别高亮**：标出最可能由 AI 生成的句子
- **一键 Humanize**：将检测结果一键改写成人类风格（轻度 / 中度 / 深度 三档）

### 目标用户

- 内容创作者（博主、写手、SEO 工作者）
- 教育工作者（老师、内容审核者）
- 求职者（需要撰写简历、自荐信）

---

## 二、技术栈

### 前端

- **框架**：Vue 3 + Vite
- **样式**：TailwindCSS
- **类型**：TypeScript

### 后端

- **框架**：Python FastAPI
- **数据库**：MySQL
- **缓存**：Redis
- **AI Provider**：MiniMax API（支持抽象替换其他大模型）

### 部署

- **容器化**：Docker + Docker Compose
- **服务器**：4核8G（端口以 3 开头）

---

## 三、项目结构

```
ai_content_detector/
├── backend/                  # Python FastAPI 后端
│   ├── app/
│   │   ├── core/           # 核心配置
│   │   ├── routers/        # API 路由
│   │   ├── services/       # 业务逻辑
│   │   ├── models/         # 数据模型
│   │   └── main.py         # 入口文件
│   ├── requirements.txt    # Python 依赖
│   └── Dockerfile
│
├── frontend/               # Vue 3 前端（待创建）
│
├── docker-compose.yml       # Docker 编排文件
├── .env.example            # 环境变量示例
└── README.md
```

---

## 四、环境准备

### 4.1 必需的服务

| 服务 | 用途 | 说明 |
|------|------|------|
| Docker | 容器化部署 | 服务器需安装 Docker |
| MySQL | 数据库 | 通过 Docker 运行 |
| Redis | 次数统计/缓存 | 通过 Docker 运行 |

### 4.2 必需的 API Key

| 服务 | 用途 | 申请地址 |
|------|------|----------|
| MiniMax API | AI 检测 + Humanize | MiniMax 开放平台 |
| PayPal | 会员支付 | PayPal 商家账户 |

### 4.3 环境变量配置

复制 `.env.example` 为 `.env`，填入以下配置：

```bash
# AI Provider
MINIMAX_API_KEY=your_minimax_api_key
MINIMAX_API_BASE=https://api.minimax.chat

# 数据库
DB_HOST=localhost
DB_PORT=3306
DB_NAME=unbot_ai
DB_USER=root
DB_PASSWORD=your_password

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# JWT
JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# PayPal
PAYPAL_CLIENT_ID=your_paypal_client_id
PAYPAL_CLIENT_SECRET=your_paypal_client_secret
PAYPAL_MODE=sandbox  # or live
```

---

## 五、快速启动

### 5.1 后端启动

```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 启动服务
uvicorn app.main:app --reload --port 3000
```

### 5.2 Docker 启动（推荐）

```bash
# 启动所有服务（MySQL + Redis + Backend）
docker-compose up -d

# 查看日志
docker-compose logs -f
```

### 5.3 前端启动

```bash
cd frontend
npm install
npm run dev
```

---

## 六、API 接口

### 6.1 AI 检测

```
POST /api/v1/detect
```

**请求：**
```json
{
  "text": "需要检测的文本内容",
  "lang": "en"
}
```

**响应：**
```json
{
  "success": true,
  "data": {
    "ai_probability": 82,
    "human_probability": 18,
    "sentence_analysis": [
      { "text": "...", "prob": 92, "level": "high" },
      { "text": "...", "prob": 45, "level": "medium" },
      { "text": "...", "prob": 12, "level": "low" }
    ],
    "remaining_quota": 4
  }
}
```

### 6.2 Humanize 改写

```
POST /api/v1/humanize
```

**请求：**
```json
{
  "text": "需要改写的文本",
  "strength": "medium",
  "lang": "en"
}
```

**响应：**
```json
{
  "success": true,
  "data": {
    "original": "The evolution of technology...",
    "rewritten": "Tech's moving so fast these days...",
    "remaining_quota": 3
  }
}
```

### 6.3 次数查询

```
GET /api/v1/quota
```

---

## 七、定价策略

| 套餐 | 价格 | 说明 |
|------|------|------|
| 免费 | $0 | 5次/天 |
| 月付 | $9.9/月 | 无限次 |
| 年付 | $79/年 | 约 $6.6/月，节省33% |

---

## 八、开发的要点

### 8.1 AI Provider 抽象

所有 AI 调用必须通过抽象层实现，方便后续更换 Provider：

```
AI Provider 抽象层
├── MiniMax（默认）
├── OpenAI（GPT-4）
└── Anthropic（Claude）
```

### 8.2 免费次数策略

- 未登录用户：基于 session_id（Cookie），共用 5次/天
- 已登录用户：独立计数
- 会员用户：无限次

### 8.3 安全边界

**禁止改写的内容：**
- 明显恶意、歧视性内容
- 违法信息
- 医疗、法律等专业领域的正式文件

---

## 九、开发规范

### 9.1 代码风格

#### Python（后端）

| 规范 | 要求 |
|------|------|
| 代码规范 | 遵循 [PEP 8](https://pep8.org/) |
| 类型提示 | 必须使用类型注解（type hints） |
| 异步编程 | I/O 操作使用 async/await |
| 格式化工具 | 使用 `black` 格式化代码 |
| 导入排序 | 使用 `isort` 排序导入 |
| **注释规范** | **必须使用中文注释，复杂逻辑要详细说明** |
| **函数行数** | **单个函数不超过 20 行，超出需拆分** |

```bash
# 安装格式化工具
pip install black isort

# 格式化命令
black app/
isort app/
```

**函数拆分原则示例：**
```python
# ❌ 错误：函数超过 20 行
def process_user_request(data):
    # 验证参数 (3行)
    validate_params(data)
    # 查询用户 (3行)
    user = query_user(data.user_id)
    # 检查权限 (3行)
    check_permission(user)
    # 处理业务逻辑 (5行)
    process_business(data)
    # 保存结果 (3行)
    save_result(data)
    # 发送通知 (3行)
    send_notification(user)
    # ... 一共超过 20 行

# ✅ 正确：拆分为多个小函数
def process_user_request(data: dict) -> Result:
    """处理用户请求主流程"""
    # 1. 验证参数
    params = validate_params(data)
    # 2. 获取用户信息
    user = get_user_info(params.user_id)
    # 3. 检查权限
    verify_permission(user)
    # 4. 处理核心业务
    result = execute_business_logic(params, user)
    # 5. 保存结果
    save_result(result)
    # 6. 发送通知
    notify_user(user, result)
    return result
```

#### TypeScript/Vue（前端）

| 规范 | 要求 |
|------|------|
| 代码规范 | 遵循 ESLint + Prettier |
| 类型定义 | 使用 TypeScript，避免 any |
| 组件规范 | SFC（单文件组件），Composition API |
| 样式规范 | 使用 TailwindCSS，不写行内样式 |

```bash
# 前端格式化
npm run lint
npm run format
```

---

### 9.2 Git 规范

#### 分支命名

```
feature/<功能名称>
bugfix/<问题描述>
hotfix/<紧急修复>
refactor/<重构内容>
docs/<文档更新>
```

**示例：**
```bash
feature/ai-detector-api
bugfix/quota-counting-fix
hotfix/login-session-error
```

#### Commit 规范

格式：`type(scope): subject`

```
feat(detect): 添加 AI 检测接口
fix(quota): 修复次数统计错误
docs(readme): 更新 README
style(api): 格式化 API 响应结构
refactor(auth): 重构用户认证模块
test(humanize): 添加 Humanize 单元测试
chore(deps): 更新依赖版本
```

**Type 类型：**

| Type | 说明 |
|------|------|
| feat | 新功能 |
| fix | Bug 修复 |
| docs | 文档更新 |
| style | 代码格式（不影响功能） |
| refactor | 重构（不是新功能也不是修复） |
| test | 测试相关 |
| chore | 构建/工具相关 |

#### Pull Request 规范

```markdown
## 描述
[简短描述这个 PR 解决的问题]

## 改动
- [ ] 功能1
- [ ] 功能2

## 测试
- [ ] 本地测试通过
- [ ] 单元测试通过

## 截图（UI 改动时）
[如有 UI 改动，添加截图]
```

---

### 9.3 API 设计规范

#### 路由设计

```
/api/v1/<资源>
```

| 方法 | 路由 | 说明 |
|------|------|------|
| GET | /api/v1/quota | 查询次数 |
| POST | /api/v1/detect | AI 检测 |
| POST | /api/v1/humanize | Humanize 改写 |
| POST | /api/v1/auth/register | 用户注册 |
| POST | /api/v1/auth/login | 用户登录 |

#### 响应格式

**成功响应：**
```json
{
  "success": true,
  "data": { ... },
  "message": "操作成功"
}
```

**错误响应：**
```json
{
  "success": false,
  "error": {
    "code": "QUOTA_EXCEEDED",
    "message": "今日免费次数已用完"
  }
}
```

#### 状态码规范

| 状态码 | 说明 |
|--------|------|
| 200 | 成功 |
| 201 | 创建成功 |
| 400 | 请求参数错误 |
| 401 | 未认证 |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 429 | 请求过于频繁（限流） |
| 500 | 服务器内部错误 |

---

### 9.4 数据库规范

#### 表命名

- 使用小写字母
- 单词间用下划线分隔
- 表名单数形式

```sql
-- 正确
users, detections, daily_usage

-- 错误
User, UserInfo, user_info_table
```

#### 字段命名

```sql
-- 使用下划线命名
user_id, created_at, is_premium

-- 避免
userId, CreateTime, isPremium
```

#### 必填字段

- 每个表必须有 `id`（主键）
- 每个表必须有 `created_at`、`updated_at`
- 敏感数据必须加密存储

---

### 9.5 安全规范

| 规范 | 要求 |
|------|------|
| 敏感信息 | 禁止硬编码，存入环境变量 |
| 密码存储 | 使用 bcrypt 加密 |
| API 认证 | JWT Token，过期时间 ≤ 24小时 |
| SQL 注入 | 使用 ORM 或参数化查询 |
| XSS 防护 | 前端做好转义，后端不做 DOM 操作 |
| CORS | 只允许指定域名 |

---

### 9.6 日志规范

```python
import logging

logger = logging.getLogger(__name__)

# 不同级别的日志
logger.info("用户登录成功", extra={"user_id": user_id})
logger.warning("检测次数超限", extra={"session_id": session_id})
logger.error("AI API 调用失败", extra={"error": str(e)})
```

**日志级别：**

| 级别 | 使用场景 |
|------|----------|
| DEBUG | 开发调试 |
| INFO | 正常流程（登录、检测、支付） |
| WARNING | 异常但可处理（次数超限、风控拦截） |
| ERROR | 错误需关注（API 失败、数据库异常） |

**核心逻辑必须打印日志的位置：**

```python
# 1. API 请求入口
async def detect_text(request: DetectRequest):
    """AI 检测接口"""
    logger.info("收到 AI 检测请求", extra={
        "session_id": request.session_id,
        "text_length": len(request.text)
    })

    # 2. 次数检查
    quota = await check_quota(request.session_id)
    if quota.remaining <= 0:
        logger.warning("检测次数已用完", extra={
            "session_id": request.session_id,
            "quota_used": quota.used
        })

    # 3. AI API 调用
    try:
        result = await ai_provider.detect(request.text)
        logger.info("AI 检测完成", extra={
            "ai_probability": result.ai_probability,
            "processing_time_ms": result.processing_time
        })
    except Exception as e:
        logger.error("AI 检测失败", extra={"error": str(e)})
        raise

    # 4. 结果保存
    await save_detection_result(result)
    logger.info("检测结果已保存", extra={"result_id": result.id})

    return result
```

**第三方 API 调用规范（超时重试机制）：**

> 所有第三方 API 调用必须实现超时重试机制，保障服务稳定性。

```python
import httpx
import asyncio
from typing import TypeVar, Callable

T = TypeVar("T")


async def call_with_retry(
    func: Callable[[], T],
    max_retries: int = 2,
    timeout: float = 30.0,
    api_name: str = "第三方API"
) -> T:
    """
    带超时和重试的 API 调用封装

    Args:
        func: 要执行的异步函数
        max_retries: 最大重试次数（默认2次）
        timeout: 超时时间（默认30秒）
        api_name: API 名称（用于日志）

    Returns:
        函数执行结果

    Raises:
        最后一次失败的异常
    """
    last_error = None

    for attempt in range(max_retries + 1):
        try:
            # 设置超时
            async with asyncio.timeout(timeout):
                result = await func()

            # 成功时打印日志
            logger.info(
                f"{api_name} 调用成功",
                extra={"attempt": attempt + 1, "success": True}
            )
            return result

        except asyncio.TimeoutError:
            last_error = f"{api_name} 调用超时"
            logger.warning(
                f"{api_name} 调用超时",
                extra={
                    "attempt": attempt + 1,
                    "max_retries": max_retries,
                    "timeout": timeout
                }
            )

        except httpx.HTTPError as e:
            last_error = f"{api_name} HTTP 错误"
            logger.warning(
                f"{api_name} HTTP 错误",
                extra={
                    "attempt": attempt + 1,
                    "error": str(e),
                    "status_code": getattr(e, "status_code", None)
                }
            )

        except Exception as e:
            last_error = f"{api_name} 未知错误"
            logger.warning(
                f"{api_name} 未知错误",
                extra={"attempt": attempt + 1, "error": str(e)}
            )

        # 重试前等待（指数退避）
        if attempt < max_retries:
            wait_time = 2 ** attempt  # 1s, 2s
            logger.info(f"等待 {wait_time}s 后重试...", extra={
                "next_attempt": attempt + 2,
                "wait_seconds": wait_time
            })
            await asyncio.sleep(wait_time)

    # 所有重试都失败
    logger.error(
        f"{api_name} 调用失败，已重试 {max_retries} 次",
        extra={
            "max_retries": max_retries,
            "last_error": str(last_error)
        }
    )
    raise APIException(
        code="AI_SERVICE_UNAVAILABLE",
        message=f"{api_name}暂时不可用，请稍后重试",
        status_code=503
    )


# 使用示例
class MiniMaxProvider:
    """MiniMax AI Provider"""

    async def detect_ai(self, text: str, lang: str) -> DetectResult:
        """检测文本是否为 AI 生成"""

        async def _call_api():
            """实际调用 MiniMax API"""
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.MINIMAX_API_BASE}/v1/detect",
                    json={"text": text, "lang": lang},
                    headers={
                        "Authorization": f"Bearer {settings.MINIMAX_API_KEY}",
                        "Content-Type": "application/json"
                    }
                )
                response.raise_for_status()
                return response.json()

        # 使用重试机制调用
        result = await call_with_retry(
            func=_call_api,
            max_retries=2,
            timeout=30.0,
            api_name="MiniMax AI检测"
        )

        return DetectResult(**result)
```

**重试策略：**

| 参数 | 默认值 | 说明 |
|------|--------|------|
| max_retries | 2 | 最大重试次数（首次 + 2次重试 = 3次） |
| timeout | 30s | 单次调用超时时间 |
| backoff | 指数退避 | 重试间隔：1s, 2s |

**日志告警级别：**

| 场景 | 日志级别 | 说明 |
|------|----------|------|
| 单次超时 | WARNING | 记录，触发重试 |
| 重试成功 | INFO | 记录，服务恢复 |
| 全部失败 | ERROR | 记录告警，返回用户友好错误 |

```python
# 1. API 请求入口
async def detect_text(request: DetectRequest):
    """AI 检测接口"""
    logger.info("收到 AI 检测请求", extra={
        "session_id": request.session_id,
        "text_length": len(request.text)
    })

    # 2. 次数检查
    quota = await check_quota(request.session_id)
    if quota.remaining <= 0:
        logger.warning("检测次数已用完", extra={
            "session_id": request.session_id,
            "quota_used": quota.used
        })

    # 3. AI API 调用
    try:
        result = await ai_provider.detect(request.text)
        logger.info("AI 检测完成", extra={
            "ai_probability": result.ai_probability,
            "processing_time_ms": result.processing_time
        })
    except Exception as e:
        logger.error("AI 检测失败", extra={"error": str(e)})
        raise

    # 4. 结果保存
    await save_detection_result(result)
    logger.info("检测结果已保存", extra={"result_id": result.id})

    return result
```

---

### 9.7 错误处理规范

```python
# 后端统一错误处理
class APIException(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400):
        self.code = code
        self.message = message
        self.status_code = status_code

# 抛出示例
raise APIException(
    code="QUOTA_EXCEEDED",
    message="今日免费次数已用完",
    status_code=429
)
```

---

### 9.8 设计模式规范

#### 抽象原则

> **相同功能出现 3 次或以上，必须抽象成公共模块或采用设计模式。**

#### 策略模式 - AI Provider 抽象

**场景：** AI 检测和改写需要支持多个 Provider（MiniMax、OpenAI、Claude）

```python
# 抽象接口
class BaseAIProvider(ABC):
    """AI Provider 抽象基类"""

    @abstractmethod
    async def detect_ai(self, text: str, lang: str) -> DetectResult:
        """检测文本是否为 AI 生成"""
        pass

    @abstractmethod
    async def humanize(self, text: str, strength: str, lang: str) -> HumanizeResult:
        """将 AI 文本改写成人类风格"""
        pass


# MiniMax 实现
class MiniMaxProvider(BaseAIProvider):
    """MiniMax AI Provider"""

    async def detect_ai(self, text: str, lang: str) -> DetectResult:
        """调用 MiniMax API 进行 AI 检测"""
        # 具体实现...
        pass


# OpenAI 实现
class OpenAIProvider(BaseAIProvider):
    """OpenAI AI Provider"""

    async def detect_ai(self, text: str, lang: str) -> DetectResult:
        """调用 OpenAI API 进行 AI 检测"""
        # 具体实现...
        pass


# 工厂类
class AIProviderFactory:
    """AI Provider 工厂"""

    _providers = {
        "minimax": MiniMaxProvider,
        "openai": OpenAIProvider,
    }

    @classmethod
    def get_provider(cls, name: str = "minimax") -> BaseAIProvider:
        """获取 AI Provider 实例"""
        provider_class = cls._providers.get(name, MiniMaxProvider)
        return provider_class()
```

#### 策略模式 - 改写强度

**场景：** Humanize 支持轻度/中度/深度三种强度

```python
class BaseRewriteStrategy(ABC):
    """改写策略抽象基类"""

    @abstractmethod
    def get_prompt(self, text: str, lang: str) -> str:
        """获取改写 Prompt"""
        pass


class LightRewriteStrategy(BaseRewriteStrategy):
    """轻度改写策略"""

    def get_prompt(self, text: str, lang: str) -> str:
        return f"轻度改写，仅调整词汇和句式，保留原意：\n{text}"


class MediumRewriteStrategy(BaseRewriteStrategy):
    """中度改写策略"""

    def get_prompt(self, text: str, lang: str) -> str:
        return f"中度改写，加入口语化表达和个人风格：\n{text}"


class DeepRewriteStrategy(BaseRewriteStrategy):
    """深度改写策略"""

    def get_prompt(self, text: str, lang: str) -> str:
        return f"深度改写，完全重写，保持核心观点但风格大变：\n{text}"


class RewriteStrategyFactory:
    """改写策略工厂"""

    _strategies = {
        "light": LightRewriteStrategy,
        "medium": MediumRewriteStrategy,
        "deep": DeepRewriteStrategy,
    }

    @classmethod
    def get_strategy(cls, strength: str) -> BaseRewriteStrategy:
        return cls._strategies.get(strength, MediumRewriteStrategy)()
```

#### 单例模式 - Redis 连接池

**场景：** 全局复用 Redis 连接

```python
class RedisManager:
    """Redis 连接管理器（单例）"""

    _instance: Optional["RedisManager"] = None
    _client: Optional[aioredis.Redis] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def get_client(self) -> aioredis.Redis:
        """获取 Redis 客户端（懒加载）"""
        if self._client is None:
            self._client = await aioredis.create_redis_pool(
                settings.REDIS_URL
            )
        return self._client

    async def close(self):
        """关闭连接"""
        if self._client:
            self._client.close()
            self._client = None
```

#### 模板方法模式 - API 响应处理

**场景：** 统一 API 响应格式和错误处理

```python
class BaseAPIHandler:
    """API 处理器基类（模板方法）"""

    async def handle(self, request) -> Response:
        """处理请求模板"""
        # 1. 记录请求
        logger.info("收到请求", extra={"path": request.url.path})

        try:
            # 2. 验证参数
            params = await self.validate(request)
            # 3. 检查权限
            await self.check_permission(request)
            # 4. 检查次数配额
            quota = await self.check_quota(request)
            # 5. 执行核心逻辑
            result = await self.process(params, quota)
            # 6. 更新配额
            await self.update_quota(quota)
            # 7. 返回成功响应
            return self.success_response(result)

        except APIException as e:
            logger.warning("业务异常", extra={"code": e.code})
            return self.error_response(e)

        except Exception as e:
            logger.error("系统异常", extra={"error": str(e)})
            return self.error_response(
                APIException("INTERNAL_ERROR", "服务器内部错误")
            )

    @abstractmethod
    async def validate(self, request) -> dict:
        """验证参数（子类实现）"""
        pass

    @abstractmethod
    async def process(self, params: dict, quota: Quota) -> Any:
        """核心处理逻辑（子类实现）"""
        pass
```

---

### 9.9 环境管理

| 环境 | 用途 | 访问权限 |
|------|------|----------|
| development | 本地开发 | 开发者 |
| staging | 测试环境 | 开发者 + 测试 |
| production | 正式环境 | 仅运维 |

**禁止事项：**
- ❌ 禁止在开发环境向生产数据库写入
- ❌ 禁止在代码中写死 API Key
- ❌ 禁止将 `.env` 文件提交到 Git
- ❌ 禁止在生产环境开启 DEBUG 模式

---

## 9.10 团队分工（TODO）

| 模块 | 负责人 | 状态 |
|------|--------|------|
| 项目初始化 | - | [ ] |
| 后端基础架构 | - | [ ] |
| AI Provider 抽象层 | - | [ ] |
| 前端 UI | - | [ ] |
| 支付集成 | - | [ ] |
| 部署上线 | - | [ ] |

---

## 9.11 参考资料

- [MVP 产品手册](./AI-Content-Detector-MVP-Handbook.md)
- [MiniMax API 文档](https://www.minimax.chat/)
- [FastAPI 文档](https://fastapi.tiangolo.com/)
- [Vue 3 文档](https://vuejs.org/)

---

*Last updated: 2026-03-23*
