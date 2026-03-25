"""
配额服务

管理用户的每日使用配额
"""
import logging
from datetime import date, datetime, timedelta, timezone

from app.core.config import settings
from app.core.redis_client import RedisClient
from app.schemas.quota import QuotaInfo, QuotaResponse

logger = logging.getLogger(__name__)


class QuotaService:
    """
    配额服务类

    管理免费次数和会员配额
    """

    def __init__(self, redis_client: RedisClient):
        self.redis = redis_client
        self.daily_limit = settings.daily_free_quota

    async def get_quota(
        self,
        identifier: str,
        is_premium: bool = False,
    ) -> QuotaResponse:
        """
        获取配额信息

        Args:
            identifier: session_id 或 user_id
            is_premium: 是否是会员

        Returns:
            配额响应
        """
        if is_premium:
            return QuotaResponse(
                daily_limit=-1,
                used=0,
                remaining=-1,
                reset_at=self._get_reset_time(),
            )

        quota = await self.redis.get_quota(identifier)
        used = quota.get("detect", 0) + quota.get("humanize", 0)
        remaining = max(0, self.daily_limit - used)

        logger.info(
            "查询配额",
            extra={
                "identifier": identifier,
                "used": used,
                "remaining": remaining,
            },
        )

        return QuotaResponse(
            daily_limit=self.daily_limit,
            used=used,
            remaining=remaining,
            reset_at=self._get_reset_time(),
        )

    async def check_and_increment(
        self,
        identifier: str,
        action: str,
        is_premium: bool = False,
    ) -> tuple[bool, int]:
        """
        检查并增加配额

        Args:
            identifier: session_id 或 user_id
            action: 操作类型 (detect/humanize)
            is_premium: 是否是会员

        Returns:
            (是否成功, 剩余配额)
        """
        # 会员无限制
        if is_premium:
            logger.info(
                "会员配额检查通过（无限制）",
                extra={"identifier": identifier, "action": action},
            )
            return True, -1

        # 检查配额
        available, remaining = await self.redis.check_quota_available(
            identifier, action, self.daily_limit, is_premium
        )

        if not available:
            logger.warning(
                "配额不足",
                extra={
                    "identifier": identifier,
                    "action": action,
                    "remaining": remaining,
                },
            )
            return False, 0

        # 增加配额
        new_count = await self.redis.increment_quota(identifier, action)
        new_remaining = max(0, self.daily_limit - new_count)

        logger.info(
            "配额增加成功",
            extra={
                "identifier": identifier,
                "action": action,
                "new_count": new_count,
                "remaining": new_remaining,
            },
        )

        return True, new_remaining

    def _get_reset_time(self) -> datetime:
        """
        获取配额重置时间

        配额在每天 UTC 0 点重置
        """
        tomorrow = date.today() + timedelta(days=1)
        return datetime.combine(tomorrow, datetime.min.time(), tzinfo=timezone.utc)

    async def get_quota_info(
        self,
        identifier: str,
        is_premium: bool = False,
    ) -> QuotaInfo:
        """
        获取配额信息（内部使用）

        Args:
            identifier: session_id 或 user_id
            is_premium: 是否是会员

        Returns:
            配额信息
        """
        if is_premium:
            return QuotaInfo(
                daily_limit=-1,
                used=0,
                remaining=-1,
                is_premium=True,
            )

        quota = await self.redis.get_quota(identifier)
        used = quota.get("detect", 0) + quota.get("humanize", 0)
        remaining = max(0, self.daily_limit - used)

        return QuotaInfo(
            daily_limit=self.daily_limit,
            used=used,
            remaining=remaining,
            is_premium=False,
        )
