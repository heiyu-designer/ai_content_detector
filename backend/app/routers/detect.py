"""
AI 检测接口路由

提供文本 AI 检测功能（需要登录）
"""
import logging

from fastapi import APIRouter, Depends

from app.core.dependencies import AuthUser, get_current_user
from app.core.exceptions import AIServiceException, QuotaExceededException
from app.core.redis_client import redis_client
from app.schemas.detect import DetectRequest, DetectResponse, SentenceAnalysis
from app.services.ai_provider import AIProviderFactory
from app.services.quota_service import QuotaService

logger = logging.getLogger(__name__)

router = APIRouter()

# 配额服务实例
quota_service = QuotaService(redis_client)


@router.post("/detect", response_model=DetectResponse)
async def detect_text(
    request: DetectRequest,
    current_user: AuthUser = Depends(get_current_user),
):
    """
    AI 检测接口（需要登录）

    检测文本是否由 AI 生成，并返回句子级别的分析结果

    - **text**: 待检测的文本（长度 10-10000 字符）
    - **lang**: 文本语言 (en/zh)

    返回 AI 生成概率和人类写作概率
    """
    logger.info(
        "收到 AI 检测请求",
        extra={
            "user_id": current_user.user_id,
            "text_length": len(request.text),
            "lang": request.lang,
        },
    )

    # 检查配额（使用 user_id 计数）
    available, remaining = await quota_service.check_and_increment(
        current_user.user_id, "detect", is_premium=current_user.is_premium
    )

    if not available:
        raise QuotaExceededException(remaining=0)

    try:
        # 调用 AI Provider 进行检测
        ai_provider = AIProviderFactory.get_provider("minimax")
        result = await ai_provider.detect_ai(request.text, request.lang)

        logger.info(
            "AI 检测完成",
            extra={
                "user_id": current_user.user_id,
                "ai_probability": result.ai_probability,
                "processing_time_ms": result.processing_time_ms,
            },
        )

        return DetectResponse(
            ai_probability=result.ai_probability,
            human_probability=result.human_probability,
            sentence_analysis=[
                SentenceAnalysis(**item) for item in result.sentence_analysis
            ],
            remaining_quota=remaining,
            summary=result.summary,
            patterns=result.patterns,
        )

    except AIServiceException:
        raise

    except Exception as e:
        logger.error(
            f"AI 检测失败: {str(e)}",
            extra={"user_id": current_user.user_id},
        )
        raise
