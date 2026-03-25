"""
AI 检测接口路由

提供文本 AI 检测功能
"""
import logging

from fastapi import APIRouter, Cookie
from typing import Optional

from app.core.exceptions import QuotaExceededException
from app.core.redis_client import redis_client
from app.schemas.detect import DetectRequest, DetectResponse, SentenceAnalysis
from app.schemas.quota import QuotaInfo
from app.services.ai_provider import AIProviderFactory
from app.services.quota_service import QuotaService

logger = logging.getLogger(__name__)

router = APIRouter()

# 配额服务实例
quota_service = QuotaService(redis_client)


def get_identifier(session_id: Optional[str] = Cookie(None)) -> str:
    """
    获取用户标识符

    优先使用 user_id（登录用户），其次使用 session_id（访客）
    """
    # TODO: 从 JWT token 中获取 user_id
    # 目前先使用 session_id
    if session_id is None:
        import uuid

        session_id = str(uuid.uuid4())

    return session_id


@router.post("/detect", response_model=DetectResponse)
async def detect_text(
    request: DetectRequest,
    session_id: Optional[str] = Cookie(None),
    user_id: Optional[str] = None,
):
    """
    AI 检测接口

    检测文本是否由 AI 生成，并返回句子级别的分析结果

    - **text**: 待检测的文本（长度 10-10000 字符）
    - **lang**: 文本语言 (en/zh)

    返回 AI 生成概率和人类写作概率
    """
    identifier = user_id or session_id or "anonymous"

    logger.info(
        "收到 AI 检测请求",
        extra={
            "identifier": identifier,
            "text_length": len(request.text),
            "lang": request.lang,
        },
    )

    # 检查配额
    quota_info = await quota_service.get_quota_info(identifier, is_premium=False)
    available, remaining = await quota_service.check_and_increment(
        identifier, "detect", is_premium=False
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
                "identifier": identifier,
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

    except Exception as e:
        logger.error(
            f"AI 检测失败: {str(e)}",
            extra={"identifier": identifier},
        )
        raise
