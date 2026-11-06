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

## 2026-11-06 — Native application replaces browser packaging

Owner explicitly rejected browser and WebView variants. Supersedes the earlier packaging decision. Use Python/PySide6 Qt Widgets and QPainter directly for the desktop app. Python source and Windows EXE share the same native implementation. Retire Go browser launchers and Android WebView packaging. Android native implementation remains outstanding rather than relabeling a WebView as native. UI remains synthetic until validated hardware engineering is authorized.

## 2026-11-06 — Two product workspaces and initial sample analysis

Owner reconfirmed Automotive plus general electronics workflows, inspired by PicoScope workflow quality without copying proprietary material. Add an automotive passive PWM actuator example and offline UART 8N1, I²C byte/ACK decoding and PWM duty/frequency analysis. Initial algorithms operate on actual synthetic/imported demo samples, with fixed documented threshold, explicit UART baud selection and basic sampling checks. They are not hardware/noise validated. SPI/CAN protocol UI entries are marked planned. Guided tests are passive instructions, never commands to energize actuators or automatic diagnostic verdicts.

## 2026-11-06 — Instrument-oriented native layout

Owner found the first UI generic. Replace dashboard styling with a native instrument layout: menus and compact toolbars, a dominant dark scope surface, light neutral channel controls, a test-help tab, decoder/note tabs and a native profile table. Use yellow/blue channel identity consistently; show voltage/time axes and minor grid subdivisions. Preserve an always-visible shared-ground warning and source badge; put detailed instructions in the test-help panel. Consulted OpenHantek screenshot and PulseView native toolbar/dock organization without copying their code/assets. Separate layout construction into native/layout.py.

## 2026-11-06 — Owner authorizes autonomous functional work

Supersedes UI-only review gates. Implement acquisition and recording foundations and keep device-dependent work open. Use immutable voltage frames, explicit sample clocks and unknown physical metadata; separate view state from samples. One adapter-owner worker and generation tokens prevent UI blocking and late-profile/import overwrite. A bounded queue is explicitly a preview buffer, not a lossless recorder. Schema 2 persists exact current samples/settings with digest and atomic replacement; schema 1 remains readable. Display min/max envelopes retain sampled spikes. Real USB support remains unavailable rather than guessed.

## 2026-11-06 — Time-aligned native decoder lane

Following owner feedback, render decoder events under the waveform using the same sample-to-time transform. Events are tied to a frozen capture ID; new captures/settings invalidate stale output. Analysis freezes the current simulated frame. Use a single implementation for numeric output and visual spans; expose hexadecimal/decimal/ASCII/binary representations and click-through sample/time details. First lane covers UART 8N1, I²C 7-bit address/data/ACK and sampled PWM periods. No protocol/hardware validation parity claim with PicoScope or LabNation is made.
