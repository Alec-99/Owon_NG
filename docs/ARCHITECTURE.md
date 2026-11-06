> **Implemented native architecture (0.4.0):** Native Qt presentation; frozen capture data and schema-2 recordings; adapter-owner worker with bounded preview buffer and an indexed simulator. See ACQUISITION_CORE.md. The Rust/Tauri/Web UI proposal below is historical and superseded. Hardware integration remains unavailable pending implementation and physical validation.

> **Development sequence updated 2026-11-06:** The product owner requires the **complete UI first** (UI-001, UI-002, UI-003 in [ROADMAP.md](ROADMAP.md)), then validated signal-processing and real hardware features. The earlier P1–P5 bullets below are **conceptual engineering milestones**, not permission to begin USB or DSP work during the UI phase. See [UI_SPEC.md](UI_SPEC.md).

# Architecture and quality bar

Status: design proposal. Only `prototype/index.html` is implemented.

## Goal

A reliable, accessible two-channel oscilloscope workspace for automotive and electronics that approaches the *workflow quality* of professional desktop tools. This is not a claim that VDS1022I hardware will match any other instrument's resolution, bandwidth, record length or channel isolation.

## Layers

1. **Device adapters** — `SimulatedScope`, then a real `Vds1022Adapter`. An adapter owns acquisition settings, device connection lifecycle, calibration metadata, raw frame acquisition, error reporting, trigger capabilities and clock information. It must not silently emulate hardware controls.
2. **Acquisition and persistence** — versioned immutable captures with raw samples, units, channel configuration, time step, trigger state, probe factors, device identifiers and provenance (`simulation`, `hardware`, `import`). Never infer unsupported metadata.
3. **Signal processing** — RMS, Vpp, frequency, rise time, duty cycle, filtering and decoders in testable independent modules. Algorithms return uncertainty or `unavailable` where a signal is insufficiently sampled or too noisy.
4. **Test procedures** — data-driven step-by-step guided tests with expected patterns, safety prerequisites, validated reference traces, necessary accessories and confidence limits. No unconditional "sensor defective" classification.
5. **Presentation** — performant rendering, cursor and zoom interaction, reference comparison, explanations in basic and advanced modes, keyboard use and accessible controls.
6. **Desktop host** — proposed Rust local service or Tauri shell, with a Web UI. USB is owned by the native backend, not by the browser-only prototype.

## Proposed interface boundary

```ts
interface ScopeAdapter {
  connect(): Promise<DeviceInfo>;
  capabilities(): Promise<ScopeCapabilities>;
  configure(request: ScopeConfiguration): Promise<AppliedConfiguration>;
  start(onFrame: (frame: ScopeFrame) => void): Promise<void>;
  single(): Promise<ScopeFrame>;
  stop(): Promise<void>;
  disconnect(): Promise<void>;
}
type ScopeFrame = {
  source: "hardware" | "simulation" | "import";
  capturedAt?: string;
  sampleIntervalSeconds: number;
  channels: Array<{id: string; unit: "V"; values: Float32Array}>;
  trigger?: {channel: string; type: string; levelVolts: number};
  metadata?: Record<string, string | number | boolean>;
};
```

The exact VDS1022I driver capabilities and trigger semantics must be verified on the device before wiring controls to hardware. Reject unsupported commands explicitly.

## Technical references (not copied)

- [neowon](https://github.com/serjster/neowon): Rust, hardware-verified VDS1022/VDS1022I backend, protocol notes, data acquisition, graph rendering and decoder work. Its code is MIT/Apache-2.0 dual licensed; comply before vendor/adaptation.
- [OWON-VDS1022 by florentbr](https://github.com/florentbr/OWON-VDS1022): Python API and a useful behavioral reference; licensing must be verified before copying any code.
- PicoScope/PicoScope Automotive: usability and workflow benchmark, not a source of graphics, code or proprietary reference data.

## Quality gates

- **Correctness:** raw trace and time base must not be rescaled invisibly; exact volts/div, probe attenuation and sample rate are recorded; anti-aliasing and decoder minimum samples/bit are enforced.
- **Reproducibility:** capture + setup + metadata reopens exactly; comparison overlays do not mutate original samples.
- **Safety:** clearly identify shared channel ground, show accessory and voltage-range prerequisites, separate high-voltage procedures, do not claim USB isolation makes differential probing safe.
- **Reliability:** disconnected and stopped states shown; reconnect and USB errors explicit; recording has bounded memory and backpressure; latency and dropped data monitored.
- **Usability:** fast setup templates, help on every complex control, beginner/advanced explanations, dark/light contrast, keyboard navigation, no hidden mandatory workflow.
- **Validation:** simulated signals for deterministic tests; integration tests on actual hardware before claiming compatibility.

## MVP sequencing

- P0: UI prototype and safety/requirements documents (**this branch**).
- P1: split prototype into modular application; automated unit/UI tests and capture schema.
- P2: real OWON backend, device handshake, sampling/trigger tests on VDS1022I, calibration and safe disconnection.
- P3: professional live capture, history, reference overlays, cursors, zoom/pan, robust file format and reports.
- P4: automotive procedure library (CKP/CMP, narrowband/wideband O2, injector with appropriate probe, charging ripple, CAN), electronics procedures, decoder integration and diagnostic guidance.
- P5: validation with known-good datasets, Windows packaging, documentation and release process.

Important: the browser prototype is **not** a supported measurement instrument, and simulated traces must always remain distinguishable from measured data.
