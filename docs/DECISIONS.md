# Architectural and product decisions

Maintain an append-only dated record. Each entry should state rationale, alternatives and implications.

## 2026-11-06 — UI-first milestone

**Decision:** Finish and review full UI/UX before implementing acquisition features and real hardware.

**Rationale:** Prioritize a coherent PicoScope-grade diagnostic workflow, including guided tests for components and info buttons, without coupling design iterations to low-level USB work. Simulated inputs let us test interaction first.

**Implications:** All demonstrations must be labeled as synthetic; controls that have no actual implementation must say so. UI-001/UI-002/UI-003 must be reviewed before engineering phase.

## 2026-11-06 — Repository and licensing

**Decision:** Keep \`Owon_NG\` as a provisional name. Do not select the project's own licence without owner approval. External code reuse is allowed subject to licence verification and attribution.

**Alternatives:** Starting from a fork of neowon or a GPL frontend. Neither is automatically chosen: their frameworks and obligations might constrain independent architecture or project licence.

## 2026-11-06 — Initial device

**Decision:** VDS1022I first; future hardware must use a separate adapter.

**Constraint:** Both input channels share a ground even though the USB connection is isolated. No unsupported high-energy use may be presented as safe.

## 2026-11-06 — UI-001 frontend foundation

**Decision:** Use Vite + TypeScript with a small native Canvas renderer and explicit fixture/state modules.

**Rationale:** The current UI scope needs a fast, responsive trace without adopting a large charting dependency. This keeps rendering and simulated acquisition replaceable behind typed modules, while avoiding third-party code and licence obligations during UI-001.

**Implications:** The current renderer and measurements are illustrative only. Real signal processing, calibrated units and device-control semantics remain deferred until the UI phase is accepted.

## 2026-11-06 — Versioned distribution requested by owner

The owner superseded the earlier step/review gate and requested Android APK, Python launch and a Windows EXE with version numbers. Reuse the existing offline frontend: Python stdlib zipapp, a small Go stdlib HTTP/browser launcher for Windows, and an Android platform-only WebView shell. This avoids rewriting UI logic in three languages. All package names derive from package.json. Windows and Python are local browser applications; the Android APK is a debug build. Device acquisition remains outside these packages. CI builds artifacts rather than automatically publishing a release.
