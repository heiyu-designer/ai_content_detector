"""
配额管理接口路由

提供次数查询和配额管理功能
"""
import logging
from typing import Optional

from fastapi import APIRouter, Cookie

from app.core.redis_client import redis_client
from app.schemas.quota import QuotaResponse
from app.services.quota_service import QuotaService

logger = logging.getLogger(__name__)

router = APIRouter()

# 配额服务实例
quota_service = QuotaService(redis_client)


@router.get("/quota", response_model=QuotaResponse)
async def get_quota(
    session_id: Optional[str] = Cookie(None),
    user_id: Optional[str] = None,
):
    """
    查询配额接口

    返回当日已使用次数和剩余次数

    - 未登录用户：返回 session_id 对应的配额
    - 登录用户：返回 user_id 对应的配额
    - 会员用户：返回无限制
    """
    identifier = user_id or session_id or "anonymous"
    is_premium = False  # TODO: 从用户信息中获取

    logger.info(
        "查询配额",
        extra={"identifier": identifier, "is_premium": is_premium},
    )

    return await quota_service.get_quota(identifier, is_premium)
