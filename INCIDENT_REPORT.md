# 问题复盘报告：MINIMAX_API_KEY 配置缺失

**日期**：2026-03-25
**问题类型**：环境配置问题
**影响范围**：AI 检测、Humanize 功能不可用

---

## 问题现象

用户登录后，点击 **Humanize** 或 **Detect** 按钮时，界面报错：
- "MiniMax Humanize暂时不可用，请稍后重试"
- "MiniMax AI检测暂时不可用，请稍后重试"

---

## 问题根因

重新部署时，`.env` 文件未创建，导致 `MINIMAX_API_KEY` 环境变量为空，MiniMax API 调用失败。

---

## 问题链路

```
1. 清理 Docker 环境时删除容器和卷
2. 重新 git clone 代码
3. 只拉取了代码，未创建 .env 文件
4. docker-compose up -d 启动服务
5. backend 容器内 MINIMAX_API_KEY 为空
6. MiniMax API 调用失败，返回 503
```

---

## 排查过程

| 步骤 | 操作 | 结果 |
|------|------|------|
| 1 | `docker compose logs backend` | 发现 MiniMax API 请求错误，重试 2 次后失败 |
| 2 | `docker exec unbot_backend env \| grep MINIMAX` | `MINIMAX_API_KEY=` (空) |
| 3 | 检查本地 `.env` 文件 | 不存在（只有 `.env.example`） |

---

## 修复步骤

```bash
# 1. 创建 .env 文件并配置 API Key
cat > /ziye/project/ai_content_detector/.env << 'EOF'
PROJECT_NAME=unbot
MYSQL_PORT=3307
REDIS_PORT=6379
BACKEND_PORT=30001
APP_NAME=Unbot AI
DEBUG=true
HOST=0.0.0.0
PORT=30001
DB_HOST=localhost
DB_PORT=3307
DB_NAME=unbot_ai
DB_USER=unbot
DB_PASSWORD=unbot_dev_password
MYSQL_ROOT_PASSWORD=root_dev_password
MYSQL_DATABASE=unbot_ai
MYSQL_USER=unbot
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=
JWT_SECRET_KEY=dev_secret_key_change_in_production_at_least_32_chars
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
MINIMAX_API_KEY=sk-cp-xxxxxxxxxx  # 实际 Key
MINIMAX_API_BASE=https://api.minimax.chat
MINIMAX_MODEL=abab6.5s-chat
AI_PROVIDER=minimax
DAILY_FREE_QUOTA=5
EOF

# 2. 重新构建并启动后端
docker compose down backend
docker compose build --no-cache backend
docker compose up -d backend

# 3. 验证
docker exec unbot_backend env | grep MINIMAX
```

---

## 经验教训

1. **重新部署前**，必须确认 `.env` 文件存在且配置正确
2. **代码与配置分离**：`.env` 不在 Git 中管理（见 `.gitignore`），部署时需手动创建
3. **敏感配置必须有值**：API Key 这类配置不能依赖默认值

---

## 预防措施

### 部署检查清单

- [ ] `.env` 文件存在
- [ ] `MINIMAX_API_KEY` 已配置（非空）
- [ ] 数据库连接正常
- [ ] Redis 连接正常
- [ ] 后端健康检查通过 (`/health`)
- [ ] AI 功能（检测/Humanize）测试通过

### 建议改进

1. **添加部署检查脚本**：启动前检查 `.env` 中的关键变量是否已设置
2. **添加启动告警**：后端启动时如果检测到 `MINIMAX_API_KEY` 为空，发送告警
3. **文档更新**：在 DEPLOYMENT.md 中添加「重新部署时需检查的配置项」章节
