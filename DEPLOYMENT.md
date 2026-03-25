# Unbot AI 服务器部署指南

本文档提供在全新 Linux 服务器上部署 Unbot AI 的完整步骤。服务器无需预装 Python 环境，所有服务将通过 Docker 容器运行。

---

## 目录

- [一、服务器准备](#一服务器准备)
- [二、安装 Docker](#二安装-docker)
- [三、安装 Docker Compose](#三安装-docker-compose)
- [四、服务器环境配置](#四服务器环境配置)
- [五、部署项目](#五部署项目)
- [六、配置域名和 SSL](#六配置域名和-ssl)
- [七、验证部署](#七验证部署)
- [八、日常维护](#八日常维护)
- [九、故障排查](#九故障排查)

---

## 一、服务器准备

### 1.1 服务器要求

| 项目 | 最低配置 | 推荐配置 |
|------|----------|----------|
| CPU | 2 核 | 4 核 |
| 内存 | 4 GB | 8 GB |
| 硬盘 | 40 GB | 80 GB SSD |
| 操作系统 | Ubuntu 20.04+ / CentOS 8+ / Debian 11+ | Ubuntu 22.04 LTS |
| 网络 | 独立 IP，带宽 5Mbps+ | 带宽 10Mbps+ |

### 1.2 开放端口

| 端口 | 用途 | 备注 |
|------|------|------|
| 22 | SSH | 服务器管理 |
| 80 | HTTP | Web 访问（必须） |
| 443 | HTTPS | SSL 加密访问（可选） |

**在云服务器控制台的安全组中开放 80 和 443 端口。**

### 1.3 连接服务器

使用 SSH 连接到服务器：

```bash
ssh root@你的服务器IP
```

---

## 二、安装 Docker

### 2.1 Ubuntu / Debian 系统

```bash
# 1. 更新软件包索引
apt-get update

# 2. 安装必要的基础软件
apt-get install -y ca-certificates curl gnupg lsb-release

# 3. 添加 Docker 官方 GPG 密钥
mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# 4. 设置 Docker 仓库
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

# 5. 安装 Docker
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# 6. 验证安装
docker --version
```

### 2.2 CentOS / RHEL 系统

```bash
# 1. 安装必要软件
yum install -y yum-utils

# 2. 添加 Docker 仓库
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# 3. 安装 Docker
yum install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# 4. 启动 Docker
systemctl start docker
systemctl enable docker

# 5. 验证安装
docker --version
```

### 2.3 启动 Docker 服务

```bash
# 启动 Docker
systemctl start docker

# 设置开机自启
systemctl enable docker

# 验证 Docker 运行状态
systemctl status docker
```

---

## 三、安装 Docker Compose

Docker Compose V2 已随 Docker 安装（`docker compose` 命令）。验证：

```bash
docker compose version
```

如果版本低于 2.0，手动安装：

```bash
# 下载 Docker Compose
curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# 设置执行权限
chmod +x /usr/local/bin/docker-compose

# 创建软链接
ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

# 验证
docker-compose --version
```

---

## 四、服务器环境配置

### 4.1 创建项目目录

```bash
# 创建项目目录
mkdir -p /www/unbot-ai
cd /www/unbot-ai

# 创建数据目录（用于持久化存储）
mkdir -p data/mysql data/redis
```

### 4.2 创建 SSL 证书目录

```bash
mkdir -p /www/unbot-ai/docker/nginx/ssl
```

### 4.3 安装可选工具

```bash
# 安装 git（用于代码更新）
apt-get install -y git

# 安装 curl（用于健康检查）
apt-get install -y curl
```

---

## 五、部署项目

### 5.1 上传项目代码

**方式一：使用 Git 克隆（推荐）**

```bash
cd /www/unbot-ai

# 如果使用 GitHub 仓库（替换为你的仓库地址）
git clone https://github.com/你的用户名/ai_content_detector.git .

# 如果使用私有仓库，需要先配置 SSH Key 或 Token
# git clone git@github.com:你的用户名/ai_content_detector.git .
```

**方式二：使用 scp 上传**

在本地电脑上执行：

```bash
# 打包项目（排除 node_modules 和 __pycache__）
cd /本地项目目录
tar --exclude='ai_content_detector/node_modules' \
    --exclude='ai_content_detector/backend/__pycache__' \
    --exclude='ai_content_detector/.git' \
    -czvf unbot-ai.tar.gz ai_content_detector/

# 上传到服务器
scp unbot-ai.tar.gz root@你的服务器IP:/www/unbot-ai/

# 在服务器解压
cd /www/unbot-ai
tar -xzvf unbot-ai.tar.gz --strip-components=1
rm unbot-ai.tar.gz
```

### 5.2 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑环境变量
nano .env
```

填写以下必要配置：

```env
# =============================================
# 应用配置
# =============================================
APP_NAME=Unbot AI
DEBUG=false
HOST=0.0.0.0
PORT=30001

# =============================================
# 数据库配置 (MySQL)
# =============================================
MYSQL_ROOT_PASSWORD=你的MySQL根密码（至少16位，复杂密码）
MYSQL_DATABASE=unbot_ai
MYSQL_USER=unbot
MYSQL_PASSWORD=你的数据库密码（至少16位）

# =============================================
# Redis 配置
# =============================================
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=

# =============================================
# JWT 配置（必须修改！）
# =============================================
JWT_SECRET_KEY=你的JWT密钥（至少32位随机字符串）
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# =============================================
# MiniMax API 配置（必须填写！）
# =============================================
MINIMAX_API_KEY=你的MiniMax API Key
MINIMAX_API_BASE=https://api.minimax.chat
MINIMAX_MODEL=abab6.5s-chat

# =============================================
# 限流配置
# =============================================
DAILY_FREE_QUOTA=5
```

**重要安全提醒：**
- `JWT_SECRET_KEY` 必须使用强随机密码，可使用以下命令生成：
  ```bash
  openssl rand -base64 32
  ```
- `MYSQL_ROOT_PASSWORD` 和 `MYSQL_PASSWORD` 必须设置为复杂密码
- `MINIMAX_API_KEY` 必须填写有效值，否则 AI 功能无法使用

### 5.3 构建前端

前端需要构建后才能部署到 Nginx：

```bash
cd /www/unbot-ai/frontend

# 安装依赖
npm install

# 构建生产版本
npm run build

# 返回项目目录
cd /www/unbot-ai
```

构建完成后，前端文件会生成在 `/www/unbot-ai/frontend/dist` 目录。

### 5.4 修改 Docker Compose 配置

编辑 `docker-compose.yml`，确保生产环境配置正确：

```bash
nano docker-compose.yml
```

关键配置检查：

```yaml
# 确保后端服务配置正确
backend:
  build:
    context: ./backend
    dockerfile: Dockerfile
  environment:
    # 确保环境变量正确引用
    - DB_HOST=mysql
    - DB_PORT=3306
    - DB_NAME=${MYSQL_DATABASE:-unbot_ai}
    - DB_USER=${MYSQL_USER:-unbot}
    - DB_PASSWORD=${MYSQL_PASSWORD:-unbot_password}
    - JWT_SECRET_KEY=${JWT_SECRET_KEY:-your-secret-key}
    - MINIMAX_API_KEY=${MINIMAX_API_KEY:-}
```

### 5.5 启动服务

```bash
# 构建并启动所有服务（后台运行）
docker compose up -d --build

# 查看服务状态
docker compose ps

# 查看日志
docker compose logs -f
```

预期输出：
```
NAME                IMAGE               COMMAND                  SERVICE
unbot_mysql         mysql:8.0           "docker-entrypoint.s…"   mysql
unbot_redis         redis:7-alpine      "docker-entrypoint.s…"   redis
unbot_backend       unbot-ai-backend    "uvicorn app.main:ap…"   backend
unbot_nginx         nginx:alpine         "/docker-entrypoint.…"   nginx
```

### 5.6 等待服务启动

MySQL 和 Redis 需要时间初始化：

```bash
# 查看 MySQL 日志（等待 "ready for connections" 消息）
docker compose logs -f mysql

# 查看后端日志（等待 "Application startup complete" 消息）
docker compose logs -f backend
```

通常需要等待 1-2 分钟所有服务才能完全启动。

---

## 六、配置域名和 SSL

### 6.1 配置域名 DNS

在域名服务商处添加 DNS 记录：

| 记录类型 | 主机记录 | 记录值 |
|----------|----------|--------|
| A | @ | 你的服务器IP |
| A | www | 你的服务器IP |

等待 DNS 生效（通常 5 分钟到 24 小时）。

### 6.2 申请 SSL 证书（Let's Encrypt 免费）

```bash
# 安装 Certbot
apt-get install -y certbot python3-certbot-nginx

# 申请证书（替换为你的域名）
certbot --nginx -d your-domain.com -d www.your-domain.com

# 按提示输入邮箱地址和同意条款
```

证书自动续期已配置，无需手动操作。

### 6.3 配置 Nginx SSL

证书申请成功后，编辑 Nginx 配置：

```bash
nano /www/unbot-ai/docker/nginx/conf.d/unbot.conf
```

更新为完整的 HTTPS 配置：

```nginx
upstream backend {
    server backend:30001;
    keepalive 32;
}

# HTTP 重定向到 HTTPS
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    return 301 https://$server_name$request_uri;
}

# HTTPS 配置
server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    # SSL 证书（Certbot 自动配置）
    ssl_certificate /etc/nginx/ssl/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/live/your-domain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 1d;

    # 根目录
    root /usr/share/nginx/html;
    index index.html;

    # 前端 SPA 路由
    location / {
        try_files $uri $uri/ /index.html;
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }

    # API 代理
    location /api/ {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Connection "";
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 8 4k;
    }

    # 健康检查
    location /health {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
    }
}
```

重启 Nginx：

```bash
docker compose restart nginx
```

---

## 七、验证部署

### 7.1 本地测试

在浏览器中访问：
- HTTP: `http://你的服务器IP`
- HTTPS: `https://你的域名`

### 7.2 API 健康检查

```bash
# 检查后端健康状态
curl http://localhost:30001/health

# 预期响应
{"status":"ok","service":"unbot-ai-backend"}
```

### 7.3 测试 AI 检测功能

```bash
curl -X POST http://localhost/api/v1/detect \
  -H "Content-Type: application/json" \
  -d '{"text": "This is a test text to check if it is AI generated.", "lang": "en"}'
```

预期响应格式：
```json
{
  "success": true,
  "data": {
    "ai_probability": 75,
    "human_probability": 25,
    "sentence_analysis": [...],
    "remaining_quota": 4
  }
}
```

### 7.4 检查容器日志

```bash
# 查看所有服务日志
docker compose logs -f

# 查看指定服务日志
docker compose logs -f backend
docker compose logs -f mysql
docker compose logs -f nginx
```

---

## 八、日常维护

### 8.1 查看服务状态

```bash
# 查看运行状态
docker compose ps

# 查看资源使用
docker stats
```

### 8.2 更新代码

```bash
cd /www/unbot-ai

# 拉取最新代码
git pull origin main

# 重新构建
docker compose up -d --build
```

### 8.3 备份数据

```bash
# 备份 MySQL 数据
docker compose exec mysql mysqldump -u root -p unbot_ai > backup_$(date +%Y%m%d).sql

# 备份 Redis 数据
docker compose exec redis redis-cli SAVE
cp -r data/redis dump.rdb backup_redis_$(date +%Y%m%d).rdb
```

### 8.4 查看磁盘使用

```bash
# 查看 Docker 磁盘使用
docker system df

# 清理未使用的镜像和容器
docker system prune -a
```

### 8.5 日志管理

```bash
# 查看 Nginx 访问日志
docker compose exec nginx tail -f /var/log/nginx/access.log

# 查看 Nginx 错误日志
docker compose exec nginx tail -f /var/log/nginx/error.log

# 日志轮转配置（添加到 /etc/logrotate.d/docker-compose）
/www/unbot-ai/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
    create 0644 root root
    sharedscripts
    postrotate
        docker compose -f /www/unbot-ai/docker-compose.yml kill -s USR1
    endscript
}
```

---

## 九、故障排查

### 9.1 服务无法启动

```bash
# 查看详细日志
docker compose logs 服务名

# 常见问题：
# 1. 端口被占用
netstat -tlnp | grep 端口号

# 2. 权限问题
chown -R 1000:1000 data/
```

### 9.2 MySQL 连接失败

```bash
# 查看 MySQL 日志
docker compose logs mysql

# 常见问题：
# 1. 首次启动需要时间初始化
# 2. 密码不匹配 - 检查 .env 配置

# 手动重置 MySQL（慎用，会丢失数据）
docker compose down
rm -rf data/mysql/*
docker compose up -d mysql
```

### 9.3 前端显示 502 Bad Gateway

```bash
# 检查后端是否正常运行
docker compose ps backend

# 检查 Nginx 日志
docker compose logs nginx

# 常见问题：
# 1. 前端未构建 - 执行 npm run build
# 2. 后端服务未启动 - 查看 backend 日志
```

### 9.4 API 返回 500 错误

```bash
# 查看后端详细日志
docker compose logs backend

# 常见问题：
# 1. MiniMax API Key 未配置或无效
# 2. 数据库连接失败
```

### 9.5 重启所有服务

```bash
# 停止所有服务
docker compose down

# 清理网络
docker network prune -f

# 重新启动
docker compose up -d

# 查看状态
docker compose ps
```

### 9.6 完全重置（慎用！会丢失所有数据）

```bash
# 停止服务
docker compose down

# 删除数据卷
rm -rf data/mysql/* data/redis/*

# 删除容器和镜像
docker compose rm -f
docker image prune -a -f

# 重新构建和启动
docker compose up -d --build
```

---

## 附录：常用命令速查

```bash
# 启动服务
docker compose up -d

# 停止服务
docker compose down

# 重启服务
docker compose restart 服务名

# 查看日志
docker compose logs -f

# 查看状态
docker compose ps

# 进入容器
docker compose exec 服务名 /bin/sh

# 重新构建
docker compose up -d --build

# 查看资源使用
docker stats

# 查看网络
docker network ls

# 查看卷
docker volume ls
```

---

## 附录：服务架构说明

```
                    ┌─────────────┐
                    │   用户浏览器  │
                    └──────┬──────┘
                           │
                           │ HTTPS (443)
                           ▼
┌──────────────────────────────────────────────────────┐
│                    Nginx (反向代理)                    │
│  ┌─────────────────┐    ┌─────────────────────────┐  │
│  │   前端静态文件   │    │     API 代理 (/api/)    │  │
│  │   /usr/share/   │    │   proxy_pass backend   │  │
│  │   nginx/html    │    │                         │  │
│  └─────────────────┘    └───────────┬─────────────┘  │
└───────────────────────────────────────┼───────────────┘
                                        │ HTTP (30001)
                                        ▼
                              ┌─────────────────────┐
                              │  FastAPI Backend    │
                              │    (Python 3.11)    │
                              │    /app/main.py     │
                              └─────────┬───────────┘
                                        │
                    ┌───────────────────┼───────────────────┐
                    │                   │                   │
                    ▼                   ▼                   ▼
            ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
            │    MySQL     │    │    Redis     │    │   MiniMax    │
            │   (8.0)      │    │    (7)       │    │    API       │
            │   :3306      │    │    :6379     │    │  (外部服务)   │
            └──────────────┘    └──────────────┘    └──────────────┘
```

---

## 附录：环境变量参考

| 变量名 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| `MYSQL_ROOT_PASSWORD` | 是 | - | MySQL Root 密码 |
| `MYSQL_DATABASE` | 是 | unbot_ai | 数据库名 |
| `MYSQL_USER` | 是 | unbot | 数据库用户 |
| `MYSQL_PASSWORD` | 是 | - | 数据库密码 |
| `JWT_SECRET_KEY` | 是 | - | JWT 密钥（至少32位） |
| `MINIMAX_API_KEY` | 是 | - | MiniMax API Key |
| `MINIMAX_API_BASE` | 否 | https://api.minimax.chat | MiniMax API 地址 |
| `DAILY_FREE_QUOTA` | 否 | 5 | 每日免费次数 |
| `DEBUG` | 否 | false | 调试模式 |

---

*文档版本：1.0*
*最后更新：2026-03-25*
*适用版本：Unbot AI v1.0.0+*
