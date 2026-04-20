from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from blackecho.core.media_engine import LocalMediaStreamingEngine, StreamRequest
from blackecho.plugins.catalog import PluginCatalog, PluginManifest
from blackecho.security.telemetry_killswitch import TelemetryKillswitch
from blackecho.ui.dashboard import DashboardLayout


class FakeTransport:
    def __init__(self) -> None:
        self.calls = []

    def send_stream(self, device_id: str, local_uri: str) -> None:
        self.calls.append((device_id, local_uri))


class ArchitectureTests(unittest.TestCase):
    def test_media_engine_streams_supported_local_file(self) -> None:
        transport = FakeTransport()
        engine = LocalMediaStreamingEngine(transport)

        with TemporaryDirectory() as tmp:
            source = Path(tmp) / "sample.mp3"
            source.write_bytes(b"ID3")
            uri = engine.stream_file(StreamRequest(device_id="echo-1", source_file=source))

        self.assertTrue(uri.startswith("file://"))
        self.assertEqual([("echo-1", uri)], transport.calls)

    def test_media_engine_streams_persona_audio_formats(self) -> None:
        transport = FakeTransport()
        engine = LocalMediaStreamingEngine(transport)

        with TemporaryDirectory() as tmp:
            streamed = []
            for name in ("persona-alpha.mp3", "persona-beta.flac", "persona-gamma.WAV"):
                source = Path(tmp) / name
                source.write_bytes(b"\x00")

                uri = engine.stream_file(
                    StreamRequest(device_id="echo-dot-kitchen", source_file=source)
                )

                self.assertTrue(uri.endswith(name))
                streamed.append(("echo-dot-kitchen", uri))

        self.assertEqual(streamed, transport.calls)

    def test_media_engine_rejects_unsupported_extension(self) -> None:
        transport = FakeTransport()
        engine = LocalMediaStreamingEngine(transport)

        with TemporaryDirectory() as tmp:
            source = Path(tmp) / "sample.ogg"
            source.write_bytes(b"\x00")
            with self.assertRaises(ValueError):
                engine.stream_file(StreamRequest(device_id="echo-1", source_file=source))

        self.assertEqual([], transport.calls)

    def test_media_engine_rejects_missing_or_non_file_source(self) -> None:
        transport = FakeTransport()
        engine = LocalMediaStreamingEngine(transport)

        with TemporaryDirectory() as tmp:
            missing = Path(tmp) / "missing.mp3"
            with self.assertRaises(FileNotFoundError):
                engine.stream_file(StreamRequest(device_id="echo-1", source_file=missing))

            directory_path = Path(tmp) / "persona.wav"
            directory_path.mkdir()
            with self.assertRaises(FileNotFoundError):
                engine.stream_file(
                    StreamRequest(device_id="echo-1", source_file=directory_path)
                )

        self.assertEqual([], transport.calls)

    def test_media_engine_requires_device_id(self) -> None:
        transport = FakeTransport()
        engine = LocalMediaStreamingEngine(transport)

        with TemporaryDirectory() as tmp:
            source = Path(tmp) / "persona.mp3"
            source.write_bytes(b"ID3")
            with self.assertRaises(ValueError):
                engine.stream_file(StreamRequest(device_id=" ", source_file=source))

        self.assertEqual([], transport.calls)

    def test_telemetry_killswitch_blocks_external_and_hot_mic(self) -> None:
        killswitch = TelemetryKillswitch("192.168.0.0/16")

        self.assertTrue(killswitch.evaluate("8.8.8.8", mic_enabled=False).blocked)
        self.assertTrue(killswitch.evaluate("192.168.1.22", mic_enabled=True).blocked)
        self.assertFalse(killswitch.evaluate("192.168.1.22", mic_enabled=False).blocked)

    def test_plugin_catalog_registers_and_lists(self) -> None:
        catalog = PluginCatalog()
        plugin = PluginManifest("media.local", "Local Media", ("stream",))
        catalog.register(plugin)

        self.assertEqual(plugin, catalog.get("media.local"))
        self.assertEqual([plugin], list(catalog.list()))

    def test_dashboard_layout_adds_cards(self) -> None:
        layout = DashboardLayout()
        layout.add_card("Media", "radio", "fadeIn")

        self.assertEqual(1, len(layout.cards))
        self.assertEqual("Media", layout.cards[0].title)


if __name__ == "__main__":
    unittest.main()
