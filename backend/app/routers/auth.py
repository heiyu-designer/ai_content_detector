"""
用户认证接口路由

提供用户注册、登录等功能
"""
import logging
from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, Depends, Header
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.core.exceptions import (
    ForbiddenException,
    NotFoundException,
    UnauthorizedException,
    ValidationException,
)
from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)
from app.models import User
from app.schemas.auth import (
    LoginResponse,
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/register", response_model=LoginResponse)
async def register(
    request: UserRegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    用户注册接口

    - **email**: 邮箱地址
    - **password**: 密码（至少 6 位）

    返回用户信息和访问令牌
    """
    logger.info(f"收到注册请求: {request.email}")

    # 检查邮箱是否已存在
    stmt = select(User).where(User.email == request.email)
    result = await db.execute(stmt)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise ValidationException(message="该邮箱已注册")

    # 创建用户
    user = User(
        email=request.email,
        password_hash=hash_password(request.password),
        is_premium=False,
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    # 生成令牌
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email},
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
    )

    logger.info(f"用户注册成功: {user.email}", extra={"user_id": user.id})

    return LoginResponse(
        success=True,
        user=UserResponse.model_validate(user),
        token=TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.access_token_expire_minutes * 60,
        ),
    )


@router.post("/login", response_model=LoginResponse)
async def login(
    request: UserLoginRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    用户登录接口

    - **email**: 邮箱地址
    - **password**: 密码

    返回用户信息和访问令牌
    """
    logger.info(f"收到登录请求: {request.email}")

    # 查找用户
    stmt = select(User).where(User.email == request.email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user or not verify_password(request.password, user.password_hash):
        logger.warning(f"登录失败: 邮箱或密码错误 - {request.email}")
        raise UnauthorizedException(message="邮箱或密码错误")

    # 生成令牌
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email},
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
    )

    logger.info(f"用户登录成功: {user.email}", extra={"user_id": user.id})

    return LoginResponse(
        success=True,
        user=UserResponse.model_validate(user),
        token=TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.access_token_expire_minutes * 60,
        ),
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    authorization: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db),
):
    """
    获取当前用户信息

    需要在请求头中携带 Bearer Token

    Authorization: Bearer <token>
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise UnauthorizedException(message="请先登录")

    token = authorization.replace("Bearer ", "")
    payload = decode_access_token(token)

    if not payload:
        raise UnauthorizedException(message="令牌无效或已过期")

    user_id = payload.get("sub")

    # 查找用户
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise NotFoundException(resource="用户")

    return UserResponse.model_validate(user)
