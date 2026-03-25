"""
应用配置模块

统一管理所有配置项，从环境变量读取
"""
from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    应用配置类

    从环境变量读取配置，遵循 12-Factor App 原则
    """

    # 应用基础配置
    app_name: str = "Unbot AI"
    app_version: str = "1.0.0"
    debug: bool = False

    # 服务配置
    host: str = "0.0.0.0"
    port: int = 30001

    # 数据库配置
    db_host: str = "localhost"
    db_port: int = 3306
    db_name: str = "unbot_ai"
    db_user: str = "root"
    db_password: str = ""

    # Redis 配置
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str = ""

    # JWT 配置
    jwt_secret_key: str = "your-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # MiniMax API 配置
    minimax_api_key: str = ""
    minimax_api_base: str = "https://api.minimax.chat"
    minimax_model: str = "abab6.5s-chat"

    # AI Provider 配置（支持切换）
    ai_provider: Literal["minimax", "openai", "anthropic"] = "minimax"
    openai_api_key: str = ""
    openai_api_base: str = "https://api.openai.com/v1"
    anthropic_api_key: str = ""
    anthropic_api_base: str = "https://api.anthropic.com"

    # 限流配置
    daily_free_quota: int = 5

    # PayPal 配置
    paypal_client_id: str = ""
    paypal_client_secret: str = ""
    paypal_mode: Literal["sandbox", "live"] = "sandbox"

    @property
    def database_url(self) -> str:
        """
        获取数据库连接 URL
        """
        return (
            f"mysql+aiomysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @property
    def redis_url(self) -> str:
        """
        获取 Redis 连接 URL
        """
        if self.redis_password:
            return f"redis://:{self.redis_password}@{self.redis_host}:{self.redis_port}/{self.redis_db}"
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache()
def get_settings() -> Settings:
    """
    获取配置单例

    使用 lru_cache 缓存配置实例，避免重复读取环境变量
    """
    return Settings()


# 全局配置实例
settings = get_settings()
