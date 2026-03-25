"""
Humanize 改写接口路由

提供 AI 文本改写为人类风格的功能（需要登录）
"""
import logging

from fastapi import APIRouter, Depends

from app.core.dependencies import AuthUser, get_current_user
from app.core.exceptions import AIServiceException, QuotaExceededException
from app.core.redis_client import redis_client
from app.schemas.humanize import HumanizeRequest, HumanizeResponse
from app.services.ai_provider import AIProviderFactory
from app.services.quota_service import QuotaService

logger = logging.getLogger(__name__)

router = APIRouter()

# 配额服务实例
quota_service = QuotaService(redis_client)


@router.post("/humanize", response_model=HumanizeResponse)
async def humanize_text(
    request: HumanizeRequest,
    current_user: AuthUser = Depends(get_current_user),
):
    """
    Humanize 改写接口（需要登录）

    将 AI 生成的文本改写成更像人类写作的风格

    - **text**: 待改写的文本（长度 10-5000 字符）
    - **strength**: 改写强度 (light/medium/deep)
    - **lang**: 文本语言 (en/zh)

    返回改写后的文本
    """
    logger.info(
        "收到 Humanize 请求",
        extra={
            "user_id": current_user.user_id,
            "text_length": len(request.text),
            "strength": request.strength,
            "lang": request.lang,
        },
    )

    # 检查配额（使用 user_id 计数）
    available, remaining = await quota_service.check_and_increment(
        current_user.user_id, "humanize", is_premium=current_user.is_premium
    )

    if not available:
        raise QuotaExceededException(remaining=0)

    try:
        # 调用 AI Provider 进行改写
        ai_provider = AIProviderFactory.get_provider("minimax")
        result = await ai_provider.humanize(
            request.text, request.strength, request.lang
        )

        logger.info(
            "Humanize 改写完成",
            extra={
                "user_id": current_user.user_id,
                "strength": request.strength,
                "original_length": len(result.original),
                "rewritten_length": len(result.rewritten),
            },
        )

        return HumanizeResponse(
            original=result.original,
            rewritten=result.rewritten,
            remaining_quota=remaining,
        )

    except AIServiceException:
        raise

    except Exception as e:
        logger.error(
            f"Humanize 改写失败: {str(e)}",
            extra={"user_id": current_user.user_id},
        )
        raise AIServiceException()
