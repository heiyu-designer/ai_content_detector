"""
Redis 客户端模块

管理 Redis 连接和常用操作
"""
import json
import logging
from datetime import date, timedelta
from typing import Any, Literal, Optional

import redis.asyncio as redis

from app.core.config import settings

logger = logging.getLogger(__name__)


class RedisClient:
    """
    Redis 客户端封装类（单例模式）

    提供常用的 Redis 操作方法
    """

    _instance: Optional["RedisClient"] = None
    _client: Optional[redis.Redis] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def connect(self) -> None:
        """
        建立 Redis 连接
        """
        if self._client is None:
            logger.info("正在连接 Redis...")
            self._client = redis.Redis(
                host=settings.redis_host,
                port=settings.redis_port,
                db=settings.redis_db,
                password=settings.redis_password or None,
                decode_responses=True,
            )
            # 测试连接
            await self._client.ping()
            logger.info("Redis 连接成功")

    async def close(self) -> None:
        """
        关闭 Redis 连接
        """
        if self._client:
            logger.info("正在关闭 Redis 连接...")
            await self._client.close()
            self._client = None
            logger.info("Redis 连接已关闭")

    @property
    def client(self) -> redis.Redis:
        """
        获取 Redis 客户端实例
        """
        if self._client is None:
            raise RuntimeError("Redis 未连接，请先调用 connect()")
        return self._client

    def _get_quota_key(self, identifier: str) -> str:
        """
        获取配额 key

        Args:
            identifier: session_id 或 user_id

        Returns:
            Redis key
        """
        today = date.today().isoformat()
        return f"quota:{identifier}:{today}"

    async def get_quota(self, identifier: str) -> dict[str, int]:
        """
        获取当日配额

        Args:
            identifier: session_id 或 user_id

        Returns:
            配额信息 {"detect": 3, "humanize": 2}
        """
        key = self._get_quota_key(identifier)
        data = await self.client.hgetall(key)

        if not data:
            return {"detect": 0, "humanize": 0}

        return {
            "detect": int(data.get("detect", 0)),
            "humanize": int(data.get("humanize", 0)),
        }

    async def increment_quota(
        self,
        identifier: str,
        action: Literal["detect", "humanize"],
    ) -> int:
        """
        增加配额计数

        Args:
            identifier: session_id 或 user_id
            action: 操作类型

        Returns:
            增加后的计数
        """
        key = self._get_quota_key(identifier)
        count = await self.client.hincrby(key, action, 1)

        # 设置过期时间（48小时，避免过多 key 堆积）
        await self.client.expire(key, timedelta(hours=48))

        logger.info(
            f"配额增加: {identifier} - {action}",
            extra={"key": key, "action": action, "count": count},
        )
        return count

    async def check_quota_available(
        self,
        identifier: str,
        action: Literal["detect", "humanize"],
        daily_limit: int = 5,
        is_premium: bool = False,
    ) -> tuple[bool, int]:
        """
        检查配额是否可用

        Args:
            identifier: session_id 或 user_id
            action: 操作类型
            daily_limit: 每日限制次数
            is_premium: 是否是会员

        Returns:
            (是否可用, 剩余次数)
        """
        # 会员无限制
        if is_premium:
            return True, -1

        quota = await self.get_quota(identifier)
        used = quota.get(action, 0)
        remaining = max(0, daily_limit - used)

        return remaining > 0, remaining

    async def set_cache(self, key: str, value: Any, expire: int = 3600) -> None:
        """
        设置缓存

        Args:
            key: 缓存 key
            value: 缓存值
            expire: 过期时间（秒）
        """
        if isinstance(value, (dict, list)):
            value = json.dumps(value)

        await self.client.set(key, value, ex=expire)

    async def get_cache(self, key: str) -> Optional[Any]:
        """
        获取缓存

        Args:
            key: 缓存 key

        Returns:
            缓存值，不存在返回 None
        """
        value = await self.client.get(key)

        if value is None:
            return None

        # 尝试解析 JSON
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value


# 全局 Redis 客户端实例
redis_client = RedisClient()


async def get_redis() -> RedisClient:
    """
    获取 Redis 客户端的依赖注入函数
    """
    return redis_client
