# Owon NG

An experimental, user-friendly oscilloscope and diagnostics workspace for **OWON VDS1022I**, with guided automotive and electronics workflows. The name is provisional.

## Current state

**v0.1 — interactive UX prototype, simulation only.** No USB device control, verified hardware sampling, actual trigger, CAN decoder or automatic diagnostic verdicts yet.

### Try the prototype

Open [`prototype/index.html`](prototype/index.html) in a modern desktop browser. It is a **standalone HTML file**: no build, sign-in, server, npm install or internet connection required.

Available now:

- Automotive demo profiles: inductive crankshaft (60−2), narrowband oxygen sensor, simplified low-side injector, alternator ripple, and complementary CAN lines.
- Electronics demo profiles: PWM, sine, UART bits, and switch-mode power supply ripple.
- Two simulated channels with visibility toggles, timebase, volts/div, trigger-level marker, running/stopped/single states.
- Draggable A/B cursors with Δt, calculated Vpp/RMS and approximate frequency.
- Scroll-wheel horizontal timebase zoom, CSV export and self-describing JSON snapshot import/export.
- Inline **i** explanations, beginner and advanced text, illustrated safe connection guidance per profile.
- Responsive desktop/tablet layout and clear **DEMO** origin labeling.

**Safety:** the VDS1022I has **common ground between its two channels**. USB isolation does not mean CH1 and CH2 are independently isolated. Never connect probe ground clips to different potentials. Automotive inductive/ignition/high-voltage and mains measurements require suitable equipment and a validated procedure. The demo is not a connection authorization.

## Engineering direction

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the backend/frontend boundary, reliability and data-quality requirements, and phased plan. See [`docs/THIRD_PARTY.md`](docs/THIRD_PARTY.md) for licence research and reuse policy.

The long-term target is **professional-grade workflow and software correctness**, not a clone of PicoScope's appearance or a promise to overcome VDS1022I hardware limits.

## Prototype checks

1. Select CKP; observe two channels, the main trace and a simulated companion cam trace.
2. Switch to Electronics → PWM; observe only CH1 and change timebase/volts-div.
3. Drag cursor A/B in the graph and observe Δt; use the mouse wheel to zoom.
4. Click every **i** help control and switch the technical explanation on/off.
5. Pause, select Single and resume. The trigger is a marker only (not hardware-triggered).
6. Export CSV. Save a JSON recording and re-open it via **Open opname**.
7. Resize to a narrow viewport and check labels and buttons remain usable.
8. Confirm simulated/hardware provenance is never ambiguous.

## Licence

The project's own licence is **not decided yet**. No third-party code has been copied into this branch. See `docs/THIRD_PARTY.md`.
