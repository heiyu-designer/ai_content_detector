"""
检测相关数据模型

定义 AI 检测相关的请求和响应数据结构
"""
from typing import Literal, Optional

from pydantic import BaseModel, Field


class DetectRequest(BaseModel):
    """
    AI 检测请求
    """

    text: str = Field(..., min_length=10, max_length=10000, description="待检测文本")
    lang: Literal["en", "zh"] = Field(default="en", description="文本语言")

    model_config = {
        "json_schema_extra": {
            "example": {
                "text": "The rapid advancement of artificial intelligence has transformed various industries...",
                "lang": "en",
            }
        }
    }


class SentenceAnalysis(BaseModel):
    """
    句子级别分析结果
    """

    text: str = Field(..., description="句子原文")
    prob: int = Field(..., ge=0, le=100, description="AI 嫌疑度百分比")
    level: Literal["high", "medium", "low"] = Field(..., description="嫌疑等级")
    reason: Optional[str] = Field(default="", description="分析原因")

    model_config = {
        "json_schema_extra": {
            "example": {
                "text": "The evolution of technology has...",
                "prob": 92,
                "level": "high",
                "reason": "公式化表达，缺乏具体数据支持",
            }
        }
    }


class DetectResponse(BaseModel):
    """
    AI 检测响应
    """

    ai_probability: int = Field(..., ge=0, le=100, description="AI 生成概率")
    human_probability: int = Field(..., ge=0, le=100, description="人类写作概率")
    sentence_analysis: list[SentenceAnalysis] = Field(
        ..., description="句子级别分析"
    )
    remaining_quota: int = Field(..., description="剩余配额")
    summary: str = Field(default="", description="整体评估说明")
    patterns: dict = Field(default_factory=dict, description="检测到的特征模式")

    model_config = {
        "json_schema_extra": {
            "example": {
                "ai_probability": 82,
                "human_probability": 18,
                "sentence_analysis": [
                    {"text": "The evolution of technology has...", "prob": 92, "level": "high", "reason": "公式化开头"},
                    {"text": "I believe this topic matters...", "prob": 45, "level": "medium", "reason": "混合特征"},
                ],
                "remaining_quota": 4,
                "summary": "文本包含多个AI特征标记，整体倾向AI生成",
                "patterns": {
                    "ai_markers": ["公式化开头", "缺乏具体数据"],
                    "human_markers": [],
                },
            }
        }
    }
