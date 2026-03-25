"""
配额管理接口路由

提供次数查询和配额管理功能（需要登录）
"""
import logging

from fastapi import APIRouter, Depends

from app.core.dependencies import AuthUser, get_current_user
from app.core.redis_client import redis_client
from app.schemas.quota import QuotaResponse
from app.services.quota_service import QuotaService

logger = logging.getLogger(__name__)

router = APIRouter()

# 配额服务实例
quota_service = QuotaService(redis_client)


@router.get("/quota", response_model=QuotaResponse)
async def get_quota(
    current_user: AuthUser = Depends(get_current_user),
):
    """
    查询配额接口（需要登录）

    返回当前登录用户的当日已使用次数和剩余次数
    - 普通用户：每天 5 次
    - 会员用户：无限制
    """
    logger.info(
        "查询配额",
        extra={"user_id": current_user.user_id, "is_premium": current_user.is_premium},
    )

    return await quota_service.get_quota(
        current_user.user_id, is_premium=current_user.is_premium
    )
