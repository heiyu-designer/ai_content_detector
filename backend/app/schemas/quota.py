"""
配额相关数据模型

定义次数限制相关的请求和响应数据结构
"""
from datetime import datetime

from pydantic import BaseModel, Field


class QuotaResponse(BaseModel):
    """
    配额查询响应
    """

    daily_limit: int = Field(..., description="每日限制次数")
    used: int = Field(..., description="已使用次数")
    remaining: int = Field(..., description="剩余次数")
    reset_at: datetime = Field(..., description="重置时间")

    model_config = {
        "json_schema_extra": {
            "example": {
                "daily_limit": 5,
                "used": 2,
                "remaining": 3,
                "reset_at": "2026-03-24T00:00:00Z",
            }
        }
    }


class QuotaInfo(BaseModel):
    """
    配额信息（内部使用）
    """

    daily_limit: int
    used: int
    remaining: int
    is_premium: bool = False
