"""
自定义异常模块

定义业务异常和 API 异常
"""
import logging
from typing import Any, Optional

from fastapi import HTTPException, status

logger = logging.getLogger(__name__)


class APIException(Exception):
    """
    API 业务异常基类

    用于抛出业务逻辑错误，统一格式返回
    """

    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = 400,
        details: Optional[Any] = None,
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details

        # 记录日志
        logger.warning(
            f"业务异常: {code} - {message}",
            extra={"code": code, "details": details},
        )

        super().__init__(message)

    def to_http_exception(self) -> HTTPException:
        """
        转换为 FastAPI HTTPException
        """
        return HTTPException(
            status_code=self.status_code,
            detail={
                "success": False,
                "error": {
                    "code": self.code,
                    "message": self.message,
                    "details": self.details,
                },
            },
        )


# 常用业务异常
class QuotaExceededException(APIException):
    """配额超出异常"""

    def __init__(self, remaining: int = 0):
        super().__init__(
            code="QUOTA_EXCEEDED",
            message="今日免费次数已用完",
            status_code=429,
            details={"remaining": remaining},
        )


class UnauthorizedException(APIException):
    """未认证异常"""

    def __init__(self, message: str = "请先登录"):
        super().__init__(
            code="UNAUTHORIZED",
            message=message,
            status_code=401,
        )


class ForbiddenException(APIException):
    """无权限异常"""

    def __init__(self, message: str = "无权限访问"):
        super().__init__(
            code="FORBIDDEN",
            message=message,
            status_code=403,
        )


class NotFoundException(APIException):
    """资源不存在异常"""

    def __init__(self, resource: str = "资源"):
        super().__init__(
            code="NOT_FOUND",
            message=f"{resource}不存在",
            status_code=404,
        )


class ValidationException(APIException):
    """参数验证异常"""

    def __init__(self, message: str = "参数验证失败"):
        super().__init__(
            code="VALIDATION_ERROR",
            message=message,
            status_code=400,
        )


class AIServiceException(APIException):
    """AI 服务异常"""

    def __init__(self, message: str = "AI 服务暂时不可用，请稍后重试"):
        super().__init__(
            code="AI_SERVICE_UNAVAILABLE",
            message=message,
            status_code=503,
        )


class PaymentException(APIException):
    """支付异常"""

    def __init__(self, message: str = "支付失败"):
        super().__init__(
            code="PAYMENT_ERROR",
            message=message,
            status_code=400,
        )
