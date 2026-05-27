from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass(slots=True)
class ProviderRequest:
    prompt: str
    agent_id: str
    context: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ProviderResponse:
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)


class Provider(Protocol):
    id: str

    def generate(self, request: ProviderRequest) -> ProviderResponse:
        """Generate a response for an agent request."""

