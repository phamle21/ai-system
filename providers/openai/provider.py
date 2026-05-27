from __future__ import annotations

from providers.base import ProviderRequest, ProviderResponse


class OpenAIProvider:
    id = "openai"

    def generate(self, request: ProviderRequest) -> ProviderResponse:
        # TODO: Integrate the official OpenAI SDK and model selection.
        raise NotImplementedError("OpenAI provider is reserved for a future integration.")

