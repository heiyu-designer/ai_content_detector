"""
Humanize 改写接口路由

提供 AI 文本改写为人类风格的功能
"""
import logging
from typing import Optional

from fastapi import APIRouter, Cookie

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
    session_id: Optional[str] = Cookie(None),
    user_id: Optional[str] = None,
):
    """
    Humanize 改写接口

    将 AI 生成的文本改写成更像人类写作的风格

    - **text**: 待改写的文本（长度 10-5000 字符）
    - **strength**: 改写强度 (light/medium/deep)
    - **lang**: 文本语言 (en/zh)

    返回改写后的文本
    """
    identifier = user_id or session_id or "anonymous"

    logger.info(
        "收到 Humanize 请求",
        extra={
            "identifier": identifier,
            "text_length": len(request.text),
            "strength": request.strength,
            "lang": request.lang,
        },
    )

    # 检查配额
    available, remaining = await quota_service.check_and_increment(
        identifier, "humanize", is_premium=False
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
                "identifier": identifier,
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
            extra={"identifier": identifier},
        )
        raise AIServiceException()
