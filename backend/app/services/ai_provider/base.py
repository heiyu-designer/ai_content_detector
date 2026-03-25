"""
AI Provider 抽象基类

定义 AI 检测和改写的标准接口
"""
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Literal

logger = logging.getLogger(__name__)


@dataclass
class DetectResult:
    """
    AI 检测结果
    """

    ai_probability: int
    human_probability: int
    sentence_analysis: list[dict]
    processing_time_ms: int
    summary: str = ""  # 整体评估说明
    patterns: dict = None  # 检测到的特征模式

    def __post_init__(self):
        if self.patterns is None:
            self.patterns = {}


@dataclass
class HumanizeResult:
    """
    Humanize 改写结果
    """

    original: str
    rewritten: str
    strength: str


class BaseAIProvider(ABC):
    """
    AI Provider 抽象基类

    所有 AI 服务提供商都必须实现此接口
    """

    provider_name: str = "base"

    @abstractmethod
    async def detect_ai(self, text: str, lang: str) -> DetectResult:
        """
        检测文本是否为 AI 生成

        Args:
            text: 待检测文本
            lang: 文本语言 (en/zh)

        Returns:
            检测结果
        """
        pass

    @abstractmethod
    async def humanize(
        self,
        text: str,
        strength: Literal["light", "medium", "deep"],
        lang: str,
    ) -> HumanizeResult:
        """
        将 AI 文本改写成人类风格

        Args:
            text: 待改写文本
            strength: 改写强度 (light/medium/deep)
            lang: 文本语言 (en/zh)

        Returns:
            改写结果
        """
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """
        健康检查

        Returns:
            服务是否可用
        """
        pass


class AIProviderFactory:
    """
    AI Provider 工厂类

    根据配置返回对应的 Provider 实例
    """

    _providers: dict[str, type[BaseAIProvider]] = {}

    @classmethod
    def register(cls, name: str, provider_class: type[BaseAIProvider]) -> None:
        """
        注册 Provider

        Args:
            name: Provider 名称
            provider_class: Provider 类
        """
        cls._providers[name] = provider_class
        logger.info(f"注册 AI Provider: {name}")

    @classmethod
    def get_provider(cls, name: str = "minimax") -> BaseAIProvider:
        """
        获取 Provider 实例

        Args:
            name: Provider 名称

        Returns:
            Provider 实例
        """
        provider_class = cls._providers.get(name)

        if provider_class is None:
            logger.warning(
                f"未找到 Provider: {name}，使用默认 MiniMax",
                extra={"requested": name, "available": list(cls._providers.keys())},
            )
            # 默认使用 MiniMax
            from app.services.ai_provider.minimax import MiniMaxProvider
            return MiniMaxProvider()

        return provider_class()

    @classmethod
    def get_available_providers(cls) -> list[str]:
        """
        获取所有可用的 Provider

        Returns:
            Provider 名称列表
        """
        return list(cls._providers.keys())
