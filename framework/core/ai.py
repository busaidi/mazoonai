from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict


@dataclass
class ChatMessage:
    role: str
    content: str


class QwenChatService:
    """Lazy Qwen chat service built on Hugging Face transformers.

    This is intentionally lightweight and can be swapped with any model that
    follows chat templates.
    """

    def __init__(
        self,
        model_name: str = "Qwen/Qwen2.5-1.5B-Instruct",
        max_new_tokens: int = 256,
        temperature: float = 0.7,
    ):
        self.model_name = model_name
        self.max_new_tokens = max_new_tokens
        self.temperature = temperature
        self._pipeline = None

    def _load(self):
        if self._pipeline is not None:
            return

        try:
            from transformers import pipeline
        except ImportError as exc:
            raise RuntimeError(
                "transformers is not installed. Install with: pip install transformers torch"
            ) from exc

        self._pipeline = pipeline(
            "text-generation",
            model=self.model_name,
            device_map="auto",
        )

    def chat(self, user_message: str, history: List[Dict[str, str]] | None = None) -> str:
        self._load()
        history = history or []

        messages = [
            {"role": "system", "content": "You are a helpful assistant like ChatGPT."},
            *history,
            {"role": "user", "content": user_message},
        ]

        outputs = self._pipeline(
            messages,
            max_new_tokens=self.max_new_tokens,
            temperature=self.temperature,
            do_sample=True,
        )

        # transformers chat pipeline returns a conversation list in generated_text.
        generated = outputs[0].get("generated_text", [])
        if isinstance(generated, list) and generated:
            return generated[-1].get("content", "")
        if isinstance(generated, str):
            return generated
        return ""
