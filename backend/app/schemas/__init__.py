"""
数据模型导出模块

统一导出所有 Pydantic 数据模型
"""
from app.schemas.auth import (
    LoginResponse,
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
)
from app.schemas.common import APIResponse, ErrorDetail, ErrorResponse
from app.schemas.detect import DetectRequest, DetectResponse, SentenceAnalysis
from app.schemas.humanize import HumanizeRequest, HumanizeResponse
from app.schemas.quota import QuotaInfo, QuotaResponse

__all__ = [
    # Auth
    "UserRegisterRequest",
    "UserLoginRequest",
    "UserResponse",
    "TokenResponse",
    "LoginResponse",
    # Detect
    "DetectRequest",
    "DetectResponse",
    "SentenceAnalysis",
    # Humanize
    "HumanizeRequest",
    "HumanizeResponse",
    # Quota
    "QuotaResponse",
    "QuotaInfo",
    # Common
    "APIResponse",
    "ErrorDetail",
    "ErrorResponse",
]
