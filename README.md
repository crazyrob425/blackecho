# blackecho

BlackEcho is a local-first Amazon Echo experimentation toolkit with a modular architecture.

## Current foundation

- **Core media engine** for local audio stream orchestration (MP3, FLAC, WAV)
- **Telemetry killswitch module** to evaluate local-vs-external traffic and mic safety state
- **Plugin catalog primitives** for marketplace-style extension support
- **Decoupled UI models + dashboard mock** for tablet-oriented control surfaces

## Repository layout

- `/blackecho/core` — streaming and core orchestration services
- `/blackecho/security` — telemetry guardrails
- `/blackecho/plugins` — plugin manifest and catalog APIs
- `/blackecho/ui` — dashboard models and HTML mock view
- `/tests` — focused unit tests for foundational modules
