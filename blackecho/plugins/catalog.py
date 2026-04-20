from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable


@dataclass(frozen=True)
class PluginManifest:
    plugin_id: str
    name: str
    capabilities: tuple[str, ...] = field(default_factory=tuple)


class PluginCatalog:
    """In-memory plugin catalog foundation for marketplace-style extensions."""

    def __init__(self) -> None:
        self._plugins: Dict[str, PluginManifest] = {}

    def register(self, plugin: PluginManifest) -> None:
        self._plugins[plugin.plugin_id] = plugin

    def get(self, plugin_id: str) -> PluginManifest | None:
        return self._plugins.get(plugin_id)

    def list(self) -> Iterable[PluginManifest]:
        return tuple(self._plugins.values())
