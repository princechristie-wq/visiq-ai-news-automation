"""
============================================================
Visiq AI
AI Provider Layer
Version : 1.0.0
============================================================

Only this file should communicate with LLM providers.

Engines must NEVER import Groq, Gemini,
OpenAI or OpenRouter directly.
"""

from groq import Groq

from config import (
    AI_PROVIDER,
    PRIMARY_MODEL,
    get_current_api_key,
    validate_provider,
)


class AIProvider:

    def __init__(self):

        validate_provider()

        self.provider = AI_PROVIDER

        self.api_key = get_current_api_key()

        if not self.api_key:
            raise RuntimeError(
                f"No API key configured for provider: {self.provider}"
            )

        if self.provider == "groq":

            self.client = Groq(
                api_key=self.api_key
            )

        else:

            raise NotImplementedError(
                f"{self.provider} provider is not implemented yet."
            )

    def generate_text(
        self,
        prompt,
        temperature=0.7,
        max_tokens=2048,
    ):

        if self.provider != "groq":
            raise RuntimeError(
                "Unsupported provider."
            )

        response = self.client.chat.completions.create(

            model=PRIMARY_MODEL,

            temperature=temperature,

            max_tokens=max_tokens,

            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return (
            response.choices[0]
            .message.content
            .strip()
        )


_provider = AIProvider()


def generate_text(
    prompt,
    temperature=0.7,
    max_tokens=2048,
):
    """
    Public function used by every engine.
    """

    return _provider.generate_text(
        prompt,
        temperature,
        max_tokens,
    )
