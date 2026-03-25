"""
Humanize 相关数据模型

定义文本改写相关的请求和响应数据结构
"""
from typing import Literal

from pydantic import BaseModel, Field


class HumanizeRequest(BaseModel):
    """
    Humanize 改写请求
    """

    text: str = Field(..., min_length=10, max_length=5000, description="待改写文本")
    strength: Literal["light", "medium", "deep"] = Field(
        default="medium", description="改写强度"
    )
    lang: Literal["en", "zh"] = Field(default="en", description="文本语言")

    model_config = {
        "json_schema_extra": {
            "example": {
                "text": "The evolution of technology has brought significant changes to human society...",
                "strength": "medium",
                "lang": "en",
            }
        }
    }


class HumanizeResponse(BaseModel):
    """
    Humanize 改写响应
    """

    original: str = Field(..., description="原文")
    rewritten: str = Field(..., description="改写后文本")
    remaining_quota: int = Field(..., description="剩余配额")

    model_config = {
        "json_schema_extra": {
            "example": {
                "original": "The evolution of technology has...",
                "rewritten": "Tech's moving so fast these days...",
                "remaining_quota": 3,
            }
        }
    }
