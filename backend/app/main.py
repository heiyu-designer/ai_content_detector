"""
Unbot AI 后端应用入口

FastAPI 应用主文件
"""
import logging
import sys
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.database import close_db, init_db
from app.core.exceptions import APIException
from app.core.redis_client import redis_client
from app.routers import auth, detect, humanize, quota

# 配置日志
logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    应用生命周期管理

    启动时初始化数据库和 Redis
    关闭时清理资源
    """
    # 启动时
    logger.info("正在启动 Unbot AI 服务...")

    try:
        # 初始化数据库
        await init_db()
        logger.info("数据库初始化完成")

        # 连接 Redis
        await redis_client.connect()
        logger.info("Redis 连接完成")

        # 导入并注册 Provider
        from app.services.ai_provider import AIProviderFactory

        logger.info(
            f"可用 AI Provider: {AIProviderFactory.get_available_providers()}"
        )

        logger.info("Unbot AI 服务启动完成")

    except Exception as e:
        logger.error(f"服务启动失败: {str(e)}")
        raise

    yield

    # 关闭时
    logger.info("正在关闭 Unbot AI 服务...")

    try:
        # 关闭 Redis
        await redis_client.close()
        logger.info("Redis 连接已关闭")

        # 关闭数据库
        await close_db()
        logger.info("数据库连接已关闭")

        logger.info("Unbot AI 服务已关闭")

    except Exception as e:
        logger.error(f"服务关闭时出错: {str(e)}")


# 创建 FastAPI 应用
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI Content Detector & Humanizer API",
    lifespan=lifespan,
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 全局异常处理器
@app.exception_handler(APIException)
async def api_exception_handler(request: Request, exc: APIException):
    """
    API 业务异常处理

    将业务异常转换为统一的 JSON 响应
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
            },
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    通用异常处理

    捕获未处理的异常，返回友好错误信息
    """
    logger.error(
        f"未处理的异常: {str(exc)}",
        extra={"path": request.url.path},
        exc_info=True,
    )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "服务器内部错误，请稍后重试",
            },
        },
    )


# 注册路由
app.include_router(detect.router, prefix="/api/v1", tags=["AI 检测"])
app.include_router(humanize.router, prefix="/api/v1", tags=["Humanize 改写"])
app.include_router(quota.router, prefix="/api/v1", tags=["配额管理"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["用户认证"])


# 健康检查接口
@app.get("/health", tags=["健康检查"])
async def health_check():
    """
    健康检查接口

    用于部署时的服务健康检查
    """
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version,
    }


@app.get("/", tags=["首页"])
async def root():
    """
    首页接口

    返回服务基本信息
    """
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "description": "AI Content Detector & Humanizer",
        "docs": "/docs",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
