from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

SUPPORTED_EXTENSIONS = {".mp3", ".flac", ".wav"}


class EchoTransport(Protocol):
    def send_stream(self, device_id: str, local_uri: str) -> None:
        """Send a local stream URI to a target Echo device."""


@dataclass(frozen=True)
class StreamRequest:
    device_id: str
    source_file: Path


class LocalMediaStreamingEngine:
    """Local-first streaming coordinator for personal audio files."""

    def __init__(self, transport: EchoTransport) -> None:
        self._transport = transport

    def stream_file(self, request: StreamRequest) -> str:
        source = request.source_file.expanduser().resolve()
        suffix = source.suffix.lower()
        if suffix not in SUPPORTED_EXTENSIONS:
            raise ValueError(f"Unsupported media format: {suffix}")
        if not source.exists() or not source.is_file():
            raise FileNotFoundError(source)

        uri = source.as_uri()
        self._transport.send_stream(request.device_id, uri)
        return uri
