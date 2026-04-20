from __future__ import annotations

from dataclasses import dataclass
from ipaddress import ip_address, ip_network


@dataclass(frozen=True)
class TelemetryDecision:
    blocked: bool
    reason: str


class TelemetryKillswitch:
    """Local-network guardrail for telemetry containment and mic safety state checks."""

    def __init__(self, allow_local_cidr: str = "192.168.0.0/16") -> None:
        self._local_network = ip_network(allow_local_cidr, strict=False)

    def evaluate(self, destination_ip: str, mic_enabled: bool) -> TelemetryDecision:
        target = ip_address(destination_ip)
        if target not in self._local_network:
            return TelemetryDecision(True, "external-network-blocked")
        if mic_enabled:
            return TelemetryDecision(True, "mic-hot-blocked")
        return TelemetryDecision(False, "local-safe")
