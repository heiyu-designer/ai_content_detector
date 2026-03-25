"""
认证相关数据模型

定义用户注册、登录相关的请求和响应数据结构
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserRegisterRequest(BaseModel):
    """
    用户注册请求
    """

    email: EmailStr = Field(..., description="邮箱地址")
    password: str = Field(..., min_length=6, max_length=128, description="密码")

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123",
            }
        }
    }


class UserLoginRequest(BaseModel):
    """
    用户登录请求
    """

    email: EmailStr = Field(..., description="邮箱地址")
    password: str = Field(..., description="密码")

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123",
            }
        }
    }


class UserResponse(BaseModel):
    """
    用户信息响应
    """

    id: str = Field(..., description="用户 ID")
    email: str = Field(..., description="邮箱地址")
    is_premium: bool = Field(default=False, description="是否会员")
    premium_expires_at: Optional[datetime] = Field(
        default=None, description="会员过期时间"
    )
    created_at: datetime = Field(..., description="创建时间")

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "user@example.com",
                "is_premium": False,
                "premium_expires_at": None,
                "created_at": "2026-03-23T10:00:00Z",
            }
        }
    }


class TokenResponse(BaseModel):
    """
    登录令牌响应
    """

    access_token: str = Field(..., description="访问令牌")
    token_type: str = Field(default="bearer", description="令牌类型")
    expires_in: int = Field(..., description="过期时间（秒）")

    model_config = {
        "json_schema_extra": {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 1800,
            }
        }
    }


class LoginResponse(BaseModel):
    """
    登录响应
    """

    success: bool = Field(..., description="是否成功")
    user: UserResponse = Field(..., description="用户信息")
    token: TokenResponse = Field(..., description="令牌信息")
