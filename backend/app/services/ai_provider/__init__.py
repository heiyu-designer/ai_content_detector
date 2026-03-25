"""
AI Provider 模块导出
"""
from app.services.ai_provider.base import (
    AIProviderFactory,
    BaseAIProvider,
    DetectResult,
    HumanizeResult,
)

# 导入所有 Provider 以触发注册
from app.services.ai_provider.minimax import MiniMaxProvider

__all__ = [
    "BaseAIProvider",
    "DetectResult",
    "HumanizeResult",
    "AIProviderFactory",
    "MiniMaxProvider",
]
