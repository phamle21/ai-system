from __future__ import annotations

from providers.base import ProviderRequest, ProviderResponse


class LocalLLMProvider:
    id = "local"

    def generate(self, request: ProviderRequest) -> ProviderResponse:
        # TODO: Add adapter for Ollama, llama.cpp, vLLM, or local HTTP providers.
        raise NotImplementedError("Local LLM provider is reserved for a future integration.")

