from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict

from blackecho.core.media_engine import LocalMediaStreamingEngine
from blackecho.plugins.catalog import PluginCatalog
from blackecho.security.telemetry_killswitch import TelemetryKillswitch


@dataclass
class BlackEchoCore:
    """Decoupled core services independent from UI implementation details."""

    media: LocalMediaStreamingEngine
    telemetry: TelemetryKillswitch
    plugins: PluginCatalog
    metadata: Dict[str, str] = field(default_factory=dict)

    def register_metadata(self, key: str, value: str) -> None:
        self.metadata[key] = value
