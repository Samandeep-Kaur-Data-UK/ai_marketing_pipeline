import os

import httpx


OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"
ANTHROPIC_MESSAGES_URL = "https://api.anthropic.com/v1/messages"
DEFAULT_TIMEOUT = float(os.getenv("LLM_API_TIMEOUT", "120"))


class LLMConfigurationError(RuntimeError):
    """Raised when no supported LLM API configuration is available."""


class LLMRequestError(RuntimeError):
    """Raised when an LLM request fails or returns no usable text."""


def available_provider() -> str | None:
    provider = os.getenv("LLM_PROVIDER", "").strip().lower()

    if provider in {"openai", "gpt"}:
        return "openai" if os.getenv("OPENAI_API_KEY") else None

    if provider in {"anthropic", "claude"}:
        return "anthropic" if os.getenv("ANTHROPIC_API_KEY") else None

    if os.getenv("OPENAI_API_KEY"):
        return "openai"

    if os.getenv("ANTHROPIC_API_KEY"):
        return "anthropic"

    return None


def provider_display_name(provider: str | None) -> str:
    mapping = {
        "openai": "GPT API",
        "anthropic": "Claude API",
        None: "local Python summary",
    }
    return mapping.get(provider, provider or "local Python summary")


def generate_text(
    *,
    system_prompt: str,
    user_prompt: str,
    max_tokens: int = 700,
    temperature: float = 0.4,
) -> str:
    provider = available_provider()

    if provider is None:
        raise LLMConfigurationError(
            "Set OPENAI_API_KEY or ANTHROPIC_API_KEY to enable Claude/GPT generation."
        )

    if provider == "openai":
        return _generate_openai_text(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=max_tokens,
            temperature=temperature,
        )

    return _generate_anthropic_text(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        max_tokens=max_tokens,
        temperature=temperature,
    )


def _generate_openai_text(
    *,
    system_prompt: str,
    user_prompt: str,
    max_tokens: int,
    temperature: float,
) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise LLMConfigurationError("OPENAI_API_KEY is not set.")

    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    payload = {
        "model": model,
        "input": [
            {
                "role": "system",
                "content": [{"type": "input_text", "text": system_prompt}],
            },
            {
                "role": "user",
                "content": [{"type": "input_text", "text": user_prompt}],
            },
        ],
        "max_output_tokens": max_tokens,
        "temperature": temperature,
    }

    with httpx.Client(timeout=DEFAULT_TIMEOUT) as client:
        response = client.post(
            OPENAI_RESPONSES_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
        )
        response.raise_for_status()
        data = response.json()

    output_text = data.get("output_text", "").strip()
    if output_text:
        return output_text

    chunks = []
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"} and content.get("text"):
                chunks.append(content["text"])

    joined = "\n".join(chunk.strip() for chunk in chunks if chunk.strip()).strip()
    if joined:
        return joined

    raise LLMRequestError(f"OpenAI response did not contain usable text for model {model}.")


def _generate_anthropic_text(
    *,
    system_prompt: str,
    user_prompt: str,
    max_tokens: int,
    temperature: float,
) -> str:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise LLMConfigurationError("ANTHROPIC_API_KEY is not set.")

    model = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-latest")
    anthropic_version = os.getenv("ANTHROPIC_VERSION", "2023-06-01")
    payload = {
        "model": model,
        "system": system_prompt,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": [{"role": "user", "content": user_prompt}],
    }

    with httpx.Client(timeout=DEFAULT_TIMEOUT) as client:
        response = client.post(
            ANTHROPIC_MESSAGES_URL,
            headers={
                "x-api-key": api_key,
                "anthropic-version": anthropic_version,
                "content-type": "application/json",
            },
            json=payload,
        )
        response.raise_for_status()
        data = response.json()

    text_parts = [
        block["text"].strip()
        for block in data.get("content", [])
        if block.get("type") == "text" and block.get("text")
    ]
    joined = "\n".join(part for part in text_parts if part).strip()
    if joined:
        return joined

    raise LLMRequestError(f"Anthropic response did not contain usable text for model {model}.")
