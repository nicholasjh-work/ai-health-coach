"""
LiteLLM routing configuration for local Ollama models.

Routes all LLM calls to locally-hosted models via Ollama.
No paid API keys required. Architecture supports swapping in
cloud providers (Claude, GPT-4) by updating router config only.

Compliance tiers mirror HILO pattern:
- RESTRICTED: PHI/PII context -> local only (enforced)
- STANDARD: general coaching -> local preferred
- EVALUATION: quality scoring -> local preferred
"""

import logging
from dataclasses import dataclass, field
from enum import Enum

import litellm

logger = logging.getLogger(__name__)

# Suppress LiteLLM verbose logging
litellm.suppress_debug_info = True


class ComplianceTier(str, Enum):
    RESTRICTED = "restricted"   # PHI-adjacent, must stay local
    STANDARD = "standard"       # general coaching
    EVALUATION = "evaluation"   # quality scoring


@dataclass
class RouterConfig:
    """LLM routing configuration. All tiers route to local Ollama by default."""

    ollama_base_url: str = "http://localhost:11434"
    primary_model: str = "ollama/llama3.1:8b"
    fallback_model: str = "ollama/llama3.2"
    evaluation_model: str = "ollama/llama3.1:8b"
    max_tokens: int = 512
    temperature: float = 0.7
    timeout: int = 120

    # Cloud models (disabled by default, no API keys needed)
    cloud_models: dict[str, str] = field(default_factory=dict)


_config = RouterConfig()


def configure(
    ollama_base_url: str | None = None,
    primary_model: str | None = None,
    fallback_model: str | None = None,
) -> None:
    """Update router configuration."""
    global _config
    if ollama_base_url:
        _config.ollama_base_url = ollama_base_url
    if primary_model:
        _config.primary_model = primary_model
    if fallback_model:
        _config.fallback_model = fallback_model


def _select_model(tier: ComplianceTier) -> str:
    """Select model based on compliance tier. All tiers route local."""
    if tier == ComplianceTier.RESTRICTED:
        return _config.primary_model
    elif tier == ComplianceTier.EVALUATION:
        return _config.evaluation_model
    return _config.primary_model


async def generate(
    prompt: str,
    system_prompt: str = "",
    tier: ComplianceTier = ComplianceTier.STANDARD,
    temperature: float | None = None,
    max_tokens: int | None = None,
) -> dict:
    """
    Generate a completion via LiteLLM routing to local Ollama.

    Returns dict with keys: text, model, tokens_used, tier.
    """
    model = _select_model(tier)
    temp = temperature or _config.temperature
    tokens = max_tokens or _config.max_tokens

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    try:
        response = await litellm.acompletion(
            model=model,
            messages=messages,
            temperature=temp,
            max_tokens=tokens,
            timeout=_config.timeout,
            api_base=_config.ollama_base_url,
        )

        text = response.choices[0].message.content or ""
        usage = response.usage

        return {
            "text": text.strip(),
            "model": model,
            "tokens_used": usage.total_tokens if usage else 0,
            "tier": tier.value,
        }

    except Exception as e:
        logger.warning(f"Primary model {model} failed: {e}. Trying fallback.")

        try:
            response = await litellm.acompletion(
                model=_config.fallback_model,
                messages=messages,
                temperature=temp,
                max_tokens=tokens,
                timeout=_config.timeout,
                api_base=_config.ollama_base_url,
            )
            text = response.choices[0].message.content or ""
            return {
                "text": text.strip(),
                "model": _config.fallback_model,
                "tokens_used": 0,
                "tier": tier.value,
                "fallback": True,
            }
        except Exception as fallback_err:
            logger.error(f"Fallback model also failed: {fallback_err}")
            raise
