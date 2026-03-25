"""
通用数据模型

定义统一的 API 响应格式
"""
from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    """
    统一 API 响应格式

    所有接口都应返回此格式
    """

    success: bool = Field(..., description="请求是否成功")
    data: Optional[T] = Field(default=None, description="响应数据")
    message: Optional[str] = Field(default=None, description="提示信息")

    model_config = {
        "json_schema_extra": {
            "example": {
                "success": True,
                "data": {"key": "value"},
                "message": "操作成功",
            }
        }
    }


class ErrorDetail(BaseModel):
    """
    错误详情
    """

    code: str = Field(..., description="错误码")
    message: str = Field(..., description="错误信息")
    details: Optional[Any] = Field(default=None, description="详细信息")


class ErrorResponse(BaseModel):
    """
    错误响应格式
    """

    success: bool = Field(default=False)
    error: ErrorDetail

    model_config = {
        "json_schema_extra": {
            "example": {
                "success": False,
                "error": {
                    "code": "QUOTA_EXCEEDED",
                    "message": "今日免费次数已用完",
                    "details": {"remaining": 0},
                },
            }
        }
    }
