from __future__ import annotations

from providers.base import ProviderRequest, ProviderResponse


class CodexProvider:
    id = "codex"

    def generate(self, request: ProviderRequest) -> ProviderResponse:
        # TODO: Bridge to Codex execution sessions and code review workflows.
        raise NotImplementedError("Codex provider is reserved for a future integration.")

