# UI specification — professional oscilloscope & component diagnostics

**Status: UI requirements. Not a claim of feature completeness.**
**Reference standard:** PicoScope-quality usability and reliability, without copying PicoScope's look or assets. Main language: Dutch.

## Product principles

1. The waveform is the central workspace, usable without digging through menus.
2. Guided mode for newcomers, expert mode for advanced oscilloscope controls; same underlying concepts.
3. Every nontrivial control has an information button: **what is this?** / **when do I need it?** / **technical details**.
4. Do not treat a waveform as a definitive vehicle fault. Show environmental conditions, wiring cautions, uncertainty, expected vs observed and next checks.
5. A powerful, complete UI must still accurately label **synthetic simulation vs hardware vs imported** data.
6. The GUI should be responsive, consistent, keyboard-operable and visually readable (dark theme default with future theming).

## Global structure and navigation

- **Top bar:** device/capability and connection state, source (DEMO/IMPORT/LIVE), active workspace, save/import/session, visible errors.
- **Navigation:** Automotive, Elektronica, Vrij meten, Bibliotheek (tests/references), Opnames/Geschiedenis, Rapporten, Instellingen, Help.
- **Waveform canvas:** dual-channel scale labels, independent channel toggles/offsets, time grid, cursors, horizontal and vertical zoom, pan, reference/ghost traces, trigger marker and explicit sample/time metadata.
- **Side panels:** acquisition controls, channel setup, measurements, math, protocol-decode UI, notes/annotations and optional help; responsive collapse without losing state.
- **Session:** save/open/capture annotations, named presets, bookmarks, reference comparison and history scrubber. For UI stage, simulate storage or use local files, but never claim non-existent durability.
- **Global overlays:** keyboard shortcut sheet, warnings, command/search palette (can be minimal in first UI batch), clear empty/error/loading/disconnected states.

## Scope workspace (design all before hardware)

- Run/Pause/Single and visible acquisition states; simulated-only if no hardware.
- Time/div, V/div, channel enable, offsets, probe x1/x10 etc. and AC/DC coupling represented in UI.
- Trigger source, type, level, edge, holdoff and mode; unsupported hardware settings visibly unavailable.
- Measurement picker: Vpp, RMS, min/max, frequency, period, duty cycle, pulse width, rise/fall time and statistics; later plug into validated DSP.
- Movable voltage and time cursors, Δt / ΔV readings, clear and keyboard interactions.
- Math/ref overlay UI (CH1-CH2, filters, FFT tab) with explicit demo/placeholder states.
- Zoom/pan, capture history, record/replay, timeline, export, comparison with saved references.
- Diagnostics/annotation pane so the operator can comment, bookmark anomalies and prepare a report.

## Automotive guided testing

Target workflow:

1. Select **vehicle subsystem / component / sensor type** from searchable categorized catalogue.
2. See **what the component does** and what symptoms prompt this measurement.
3. See **prerequisites and safety**, pin/signal type, whether measuring voltage or current, probe/accessory requirements, correct ground/connection diagrams (conceptual until verified, never model-specific pin claims).
4. Apply a recommended **simulated preset** and visualize a clearly labeled synthesized reference trace.
5. Guide user through capture, wave comparison, relevant measurements and why they matter.
6. Show possible causes of a deviation with confidence and limitations, and suggested follow-up checks (UI-only until analysis verified).
7. Save snapshot, annotation and report.

Minimum catalog groups to **design**:
- **Engine position/timing:** CKP inductive and Hall, CMP and correlation, missing-tooth wheels, RPM.
- **Fuel/air/ignition:** narrowband oxygen; wideband oxygen clearly separate; injector voltage/current with appropriate probe; ignition primary / secondary with specialized accessories; MAP, MAF, TPS, temperature sensors; PWM solenoids and actuators.
- **Charging/start:** 12 V battery, starter voltage drop, alternator ripple, charging control.
- **Communications:** CAN-H/L, LIN, PWM signaling; bus physical layer vs protocol decode explicitly distinguished.
- **Other sensors:** wheel-speed/ABS, Hall and inductive signals.

Start with representative **illustrative fixtures** for CKP, narrowband O2, injector, CAN, PWM and electronics. Do not assert every fixture is a measured "known good" waveform. Component profiles should be data-driven and expandable.

**Critical:** The VDS1022I has shared ground across its two inputs. A guided test may be marked **unavailable until suitable accessories / safe procedure are confirmed**. Never assume a 10x probe is enough for every high-voltage transient.

## Electronics guided testing

Catalog navigation: power supplies and ripple; PWM/frequency/duty-cycle; analogue filters/amplifiers; logic levels and transitions; UART, I²C and SPI; simple RC response; noise, harmonics and FFT; motor/inductive load safely with rated equipment. Show basic/advanced help and simulated expected signals.

## High-quality interaction requirements

- Every clickable item has a defined state change, navigation or honest disabled tooltip. No decorative dead buttons.
- Discovery: search and filtering for test profiles, favourites/recent items and reusable presets.
- Guided vs Expert toggle should affect explanation density, not hide essential safety information.
- Controls update instantly, never rescale raw measurements silently and maintain appropriate physical units.
- Error/disconnected/unavailable states with actionable descriptions rather than fake success.
- Keyboard focus, accessible names, adequate contrast and responsive layouts are testable.
- Recording and session UI should make provenance, capture time, scale, device and accessory metadata legible.

## UI acceptance for completing the UI phase

- Every global navigation screen exists and supports a coherent demo journey.
- All key controls respond in the UI. Any back-end-only operation is clearly mocked or disabled with explanation.
- A first-time automotive user can complete a simulated CKP diagnostic journey without knowing scope terminology.
- An electronics user can inspect simulated PWM, zoom and measure with cursors, add a note and export/save a **demo** session.
- Beginner/expert help, reference compare, history, session screens and reports all have testable UI flows.
- Automated browser/interaction tests, screenshot review, keyboard smoke tests, responsive checks and state tests pass.
- User explicitly reviews and accepts the UI milestone **before real hardware/feature engineering**.
