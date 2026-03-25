"""
MiniMax AI Provider 实现

使用 MiniMax API 实现 AI 检测和 Humanize 功能
"""
import logging
import time
from abc import ABC, abstractmethod
from typing import Literal

import httpx

from app.core.config import settings
from app.services.ai_provider.base import (
    AIProviderFactory,
    BaseAIProvider,
    DetectResult,
    HumanizeResult,
)
from app.utils.api_retry import call_with_retry

logger = logging.getLogger(__name__)


class RewriteStrategy(ABC):
    """
    改写策略抽象基类
    """

    @abstractmethod
    def get_system_prompt(self) -> str:
        """获取系统提示词"""
        pass

    @abstractmethod
    def get_user_prompt(self, text: str, lang: str) -> str:
        """获取用户提示词"""
        pass


class LightRewriteStrategy(RewriteStrategy):
    """轻度改写策略"""

    def get_system_prompt(self) -> str:
        return """You are a professional text editor. Rewrite the given text to sound more natural and human-written.
Keep the core meaning and key points exactly the same.
Only adjust vocabulary and sentence structure slightly.
Do not add new ideas or remove existing ones.
Write in a natural, conversational tone.
【CRITICAL】You MUST output in the SAME language as the input text. If input is Chinese, output Chinese. If input is English, output English.
Never translate - only rewrite."""

    def get_user_prompt(self, text: str, lang: str) -> str:
        return f"Rewrite the following text to sound more natural (keep the SAME language as the input):\n\n{text}"


class MediumRewriteStrategy(RewriteStrategy):
    """中度改写策略"""

    def get_system_prompt(self) -> str:
        return """You are a human text rewriter. Rewrite the following AI-generated text to sound more naturally human-written.

Rules:
- Keep the core meaning and key points
- 【CRITICAL】Output MUST be in the SAME language as the input text. Chinese input → Chinese output. English input → English output.
- Never translate the content
- Add natural variations in sentence length
- Include occasional contractions and colloquialisms
- Vary the sentence structure
- Add subtle "human" markers (first-person hints, anecdotal touches)
- Make it sound like a real person wrote it, not a machine"""

    def get_user_prompt(self, text: str, lang: str) -> str:
        return f"Humanize this text (preserve the input language, detect it automatically):\n\n{text}"


class DeepRewriteStrategy(RewriteStrategy):
    """深度改写策略"""

    def get_system_prompt(self) -> str:
        return """You are a creative human writer. Completely rewrite the following text while keeping only the core观点.

Rules:
- Completely rewrite, but keep the main point
- 【CRITICAL】Output MUST be in the SAME language as the input text. Chinese input → Chinese output. English input → English output.
- Never translate the content
- Use a completely different structure and flow
- Write as if you are a different person with a different voice
- Add personal anecdotes or examples where appropriate
- Use casual, natural language
- Make it sound authentically human-written"""

    def get_user_prompt(self, text: str, lang: str) -> str:
        return f"Deep rewrite - completely reimagine this text in a new human voice (preserve the input language):\n\n{text}"


class RewriteStrategyFactory:
    """改写策略工厂"""

    _strategies: dict[str, type[RewriteStrategy]] = {
        "light": LightRewriteStrategy,
        "medium": MediumRewriteStrategy,
        "deep": DeepRewriteStrategy,
    }

    @classmethod
    def get_strategy(cls, strength: str) -> RewriteStrategy:
        """获取改写策略"""
        strategy_class = cls._strategies.get(strength, MediumRewriteStrategy)
        return strategy_class()


class MiniMaxProvider(BaseAIProvider):
    """
    MiniMax AI Provider

    使用 MiniMax API 实现 AI 检测和文本改写
    """

    provider_name = "minimax"

    def __init__(self):
        self.api_key = settings.minimax_api_key
        self.api_base = settings.minimax_api_base
        self.model = settings.minimax_model
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        """获取 HTTP 客户端"""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                timeout=httpx.Timeout(60.0),
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
            )
        return self._client

    async def close(self) -> None:
        """关闭 HTTP 客户端"""
        if self._client and not self._client.is_closed:
            await self._client.aclose()

    async def detect_ai(self, text: str, lang: str) -> DetectResult:
        """
        使用 MiniMax API 检测文本是否为 AI 生成

        通过分析文本特征判断 AI 生成概率
        """
        start_time = time.time()

        async def _call_api():
            client = await self._get_client()
            response = await client.post(
                f"{self.api_base}/v1/text/chatcompletion_v2",
                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "user",
                            "content": self._build_detection_prompt(text, lang),
                        }
                    ],
                    "stream": False,
                },
            )
            response.raise_for_status()
            return response.json()

        try:
            result = await call_with_retry(
                _call_api,
                max_retries=2,
                timeout=30.0,
                api_name="MiniMax AI检测",
            )

            # 解析响应
            analysis = self._parse_detection_result(result, text)

            processing_time = int((time.time() - start_time) * 1000)

            logger.info(
                "MiniMax AI 检测完成",
                extra={
                    "ai_probability": analysis["ai_probability"],
                    "processing_time_ms": processing_time,
                },
            )

            return DetectResult(
                ai_probability=analysis["ai_probability"],
                human_probability=analysis["human_probability"],
                sentence_analysis=analysis["sentence_analysis"],
                processing_time_ms=processing_time,
                summary=analysis.get("summary", ""),
                patterns=analysis.get("patterns", {}),
            )

        except Exception as e:
            logger.error(f"MiniMax AI 检测失败: {str(e)}")
            # 降级处理：返回模拟数据
            return self._fallback_detection(text)

    def _build_detection_prompt(self, text: str, lang: str) -> str:
        """构建检测提示词"""
        return f"""分析文本，判断AI生成概率。只返回JSON：
{{"ai":0-100,"sum":"一句话总结","ai_m":["AI特征词1","AI特征词2"],"hu_m":["人类特征词1"]}}

判断依据：
- AI特征：公式化开头如"随着XX发展"、buzzword如"赋能、生态、深刻改变"、缺乏具体细节、泛泛而谈
- 人类特征：口语化表达、个人感受"我觉得"、具体数据、表情符号自然使用

文本：{text}
JSON："""

    def _parse_detection_result(self, result: dict, original_text: str) -> dict:
        """解析 MiniMax API 响应"""
        import json
        import re

        try:
            content = result.get("choices", [{}])[0].get("message", {}).get(
                "content", ""
            )

            # 移除 markdown 代码块标记
            json_str = re.sub(r"```json\s*", "", content)
            json_str = re.sub(r"\s*```", "", json_str)
            json_str = json_str.strip()

            data = json.loads(json_str)

            # 提取整体 AI 概率
            ai_prob = data.get("ai", 50)
            ai_markers = data.get("ai_m", data.get("ai_markers", []))
            human_markers = data.get("hu_m", data.get("human_markers", []))
            summary = data.get("sum", data.get("summary", ""))

            # 用 Python 分割句子
            sentence_analysis = self._split_sentences(original_text, ai_prob, ai_markers)

            return {
                "ai_probability": ai_prob,
                "human_probability": 100 - ai_prob,
                "summary": summary,
                "patterns": {
                    "ai_markers": ai_markers,
                    "human_markers": human_markers,
                },
                "sentence_analysis": sentence_analysis,
            }
        except (json.JSONDecodeError, KeyError, IndexError):
            logger.warning("解析检测结果失败，使用默认分析")
            return self._fallback_analysis(original_text)

    def _split_sentences(self, text: str, ai_prob: int, ai_markers: list) -> list:
        """用 Python 分割句子"""
        import re

        # 按中文句子结束符分割
        sentences = re.split(r'([。！？\n]+)', text)
        chunks = []
        current = ""

        for i, part in enumerate(sentences):
            if i % 2 == 0:  # 文本部分
                current += part
            else:  # 分隔符部分
                current += part
                if current.strip():
                    chunks.append(current.strip())
                current = ""

        if current.strip():
            chunks.append(current.strip())

        # 过滤空句子和太短的
        chunks = [c for c in chunks if c.strip() and len(c.strip()) > 3]

        # 分析每个句子
        sentence_analysis = []
        for chunk in chunks:
            chunk_prob = ai_prob
            reason = ""

            # 检查是否包含 AI 特征词
            for marker in ai_markers:
                if marker in chunk:
                    chunk_prob = min(95, chunk_prob + 10)
                    reason = f"含AI特征"
                    break

            level = "high" if chunk_prob >= 70 else "medium" if chunk_prob >= 40 else "low"
            sentence_analysis.append({
                "text": chunk,
                "prob": chunk_prob,
                "level": level,
                "reason": reason,
            })

        return sentence_analysis

    def _fallback_detection(self, text: str) -> DetectResult:
        """降级处理：返回默认分析结果"""
        analysis = self._fallback_analysis(text)
        return DetectResult(
            ai_probability=analysis["ai_probability"],
            human_probability=analysis["human_probability"],
            sentence_analysis=analysis["sentence_analysis"],
            processing_time_ms=0,
            summary=analysis.get("summary", "分析服务暂时不可用"),
            patterns=analysis.get("patterns", {}),
        )

    def _fallback_analysis(self, text: str) -> dict:
        """生成默认分析结果"""
        import re

        # 按中文句子结束符分割
        sentences = re.split(r'([。！？\n]+)', text)
        chunks = []
        current = ""

        for i, part in enumerate(sentences):
            if i % 2 == 0:
                current += part
            else:
                current += part
                if current.strip():
                    chunks.append(current.strip())
                current = ""

        if current.strip():
            chunks.append(current.strip())

        chunks = [c for c in chunks if c.strip() and len(c.strip()) > 3]

        sentence_analysis = []
        for chunk in chunks[:8]:
            prob = 50
            level = "medium"
            sentence_analysis.append({
                "text": chunk,
                "prob": prob,
                "level": level,
                "reason": "",
            })

        return {
            "ai_probability": 50,
            "human_probability": 50,
            "sentence_analysis": sentence_analysis,
            "summary": "分析服务暂时不可用",
            "patterns": {"ai_markers": [], "human_markers": []},
        }

    def _detect_language(self, text: str, lang_hint: str) -> str:
        """检测文本语言"""
        # 如果有明确的语言提示，优先使用
        if lang_hint in ("en", "zh"):
            return lang_hint

        # 基于字符范围检测
        chinese_count = sum(1 for c in text if "\u4e00" <= c <= "\u9fff")
        total_chars = len(text.strip())

        if total_chars == 0:
            return "en"

        chinese_ratio = chinese_count / total_chars
        return "zh" if chinese_ratio > 0.3 else "en"

    async def humanize(
        self,
        text: str,
        strength: Literal["light", "medium", "deep"],
        lang: str,
    ) -> HumanizeResult:
        """
        使用 MiniMax API 进行 Humanize 改写
        """
        # 自动检测语言
        output_lang = self._detect_language(text, lang)

        # 根据输出语言选择系统提示词（使用对应语言）
        if output_lang == "zh":
            system_prompt = """你是一个专业的文本改写专家。将以下文本改写得更自然、像真人写作。

要求：
- 保持核心含义和关键要点不变
- 只调整词汇和句子结构
- 不添加新观点，不删除原有内容
- 使用自然、口语化的表达
- 【关键】必须使用中文输出，不要翻译原文"""
            user_prompt = f"请将以下中文文本改写得更自然：\n\n{text}"
        else:
            system_prompt = """You are a professional text editor. Rewrite the given text to sound more natural and human-written.
Keep the core meaning and key points exactly the same.
Only adjust vocabulary and sentence structure slightly.
Do not add new ideas or remove existing ones.
Write in a natural, conversational tone.
IMPORTANT: Respond in English only."""

            user_prompt = f"Rewrite the following text to sound more natural:\n\n{text}"

        async def _call_api():
            client = await self._get_client()

            response = await client.post(
                f"{self.api_base}/v1/text/chatcompletion_v2",
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    "temperature": 0.8,
                    "stream": False,
                },
            )
            response.raise_for_status()
            return response.json()

        try:
            result = await call_with_retry(
                _call_api,
                max_retries=2,
                timeout=60.0,
                api_name="MiniMax Humanize",
            )

            rewritten = result.get("choices", [{}])[0].get("message", {}).get(
                "content", text
            )

            logger.info(
                "MiniMax Humanize 完成",
                extra={
                    "strength": strength,
                    "original_length": len(text),
                    "rewritten_length": len(rewritten),
                },
            )

            return HumanizeResult(
                original=text,
                rewritten=rewritten.strip(),
                strength=strength,
            )

        except Exception as e:
            logger.error(f"MiniMax Humanize 失败: {str(e)}")
            raise

    async def health_check(self) -> bool:
        """健康检查"""
        try:
            client = await self._get_client()
            response = await client.post(
                f"{self.api_base}/v1/text/chatcompletion_v2",
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": "Hi"}],
                    "stream": False,
                },
            )
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"MiniMax 健康检查失败: {str(e)}")
            return False


# 注册 MiniMax Provider
AIProviderFactory.register("minimax", MiniMaxProvider)
