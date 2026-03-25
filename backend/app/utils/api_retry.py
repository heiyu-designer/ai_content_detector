"""
API 重试工具模块

提供带超时和重试机制的 API 调用封装
"""
import asyncio
import logging
from typing import Any, Callable, TypeVar

import httpx

from app.core.exceptions import AIServiceException

logger = logging.getLogger(__name__)

T = TypeVar("T")


async def call_with_retry(
    func: Callable[..., Any],
    max_retries: int = 2,
    timeout: float = 30.0,
    api_name: str = "第三方API",
) -> Any:
    """
    带超时和重试的 API 调用封装

    Args:
        func: 要执行的异步函数
        max_retries: 最大重试次数（默认2次）
        timeout: 超时时间（默认30秒）
        api_name: API 名称（用于日志）

    Returns:
        函数执行结果

    Raises:
        AIServiceException: 所有重试都失败后抛出
    """
    last_error = None

    for attempt in range(max_retries + 1):
        try:
            # 设置超时
            async with asyncio.timeout(timeout):
                result = await func()

            logger.info(
                f"{api_name} 调用成功",
                extra={"attempt": attempt + 1, "success": True},
            )
            return result

        except asyncio.TimeoutError:
            last_error = f"{api_name} 调用超时"
            logger.warning(
                f"{api_name} 调用超时",
                extra={
                    "attempt": attempt + 1,
                    "max_retries": max_retries,
                    "timeout": timeout,
                },
            )

        except httpx.HTTPStatusError as e:
            last_error = f"{api_name} HTTP 错误: {e.response.status_code}"
            logger.warning(
                f"{api_name} HTTP 错误",
                extra={
                    "attempt": attempt + 1,
                    "status_code": e.response.status_code,
                    "response": e.response.text[:200],
                },
            )

        except httpx.RequestError as e:
            last_error = f"{api_name} 请求错误"
            logger.warning(
                f"{api_name} 请求错误",
                extra={"attempt": attempt + 1, "error": str(e)},
            )

        except Exception as e:
            last_error = f"{api_name} 未知错误"
            logger.warning(
                f"{api_name} 未知错误",
                extra={"attempt": attempt + 1, "error": str(e)},
            )

        # 重试前等待（指数退避）
        if attempt < max_retries:
            wait_time = 2**attempt
            logger.info(
                f"等待 {wait_time}s 后重试...",
                extra={"next_attempt": attempt + 2, "wait_seconds": wait_time},
            )
            await asyncio.sleep(wait_time)

    # 所有重试都失败
    logger.error(
        f"{api_name} 调用失败，已重试 {max_retries} 次",
        extra={
            "max_retries": max_retries,
            "last_error": str(last_error),
        },
    )
    raise AIServiceException(message=f"{api_name}暂时不可用，请稍后重试")
