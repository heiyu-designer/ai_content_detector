"""
认证依赖项

提供登录验证等依赖注入函数
"""
import logging
from typing import Annotated, Optional

from fastapi import Depends, Header, HTTPException, status
from pydantic import BaseModel

from app.core.security import get_user_id_from_token

logger = logging.getLogger(__name__)


class AuthUser(BaseModel):
    """认证用户信息"""

    user_id: str
    is_premium: bool = False


async def get_current_user(
    authorization: Annotated[Optional[str], Header()] = None,
) -> AuthUser:
    """
    获取当前登录用户

    从 Authorization Header 中解析 JWT token 获取用户信息

    Args:
        authorization: Authorization Header (Bearer token)

    Returns:
        AuthUser: 当前登录用户信息

    Raises:
        HTTPException: 未登录或 token 无效时抛出 401
    """
    if not authorization:
        logger.warning("请求缺少 Authorization Header")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="请先登录后再使用",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 解析 Bearer token
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        logger.warning("Authorization Header 格式错误")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token 格式无效",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = parts[1]
    user_id = get_user_id_from_token(token)

    if not user_id:
        logger.warning("Token 无效或已过期")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="登录已过期，请重新登录",
            headers={"WWW-Authenticate": "Bearer"},
        )

    logger.info("用户认证成功", extra={"user_id": user_id})
    return AuthUser(user_id=user_id)
