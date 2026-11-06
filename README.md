> **Codex handoff (2026-11-06):** This repository is in a **UI-first** development phase. The complete agent brief is in [AGENTS.md](AGENTS.md); the working branch strategy and current status are in [docs/START_HERE.md](docs/START_HERE.md). The detailed UI quality spec is in [docs/UI_SPEC.md](docs/UI_SPEC.md), the first task in [docs/tasks/UI-001.md](docs/tasks/UI-001.md), and a copy-ready Dutch Codex prompt in [docs/CODEX_START_PROMPT.md](docs/CODEX_START_PROMPT.md). The name Owon_NG is provisional. **Real hardware support is intentionally deferred until the full UI is accepted.**

# Owon NG

An experimental, user-friendly oscilloscope and diagnostics workspace for **OWON VDS1022I**, with guided automotive and electronics workflows. The name is provisional.

## Current state

**v0.2 — modular UI foundation plus the retained v0.1 prototype; simulation only.** No USB device control, verified hardware sampling, actual trigger, CAN decoder or automatic diagnostic verdicts yet.

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

## UI-001 app foundation

The modular TypeScript/Vite workspace is under `src/`. Run `npm ci`, `npm run dev`, `npm run build`, or `npm run check`. The new workspace has Dutch navigation for all primary areas, simulated CKP/PWM/lambda profiles, a Canvas trace, channel toggles, demo run/single, zoom/cursor controls, safety and help messaging, notes, local demo save and JSON export. All traces are deterministic fixtures and labeled demo; hardware, decoder, trigger, and diagnostic functionality remain unavailable. The standalone `prototype/index.html` remains as a reference.

## Versie 0.2.0: Android, Python en Windows

Dezelfde demo-UI wordt geleverd als:
- `Owon_NG-0.2.0-android-debug.apk`: offline Android-app (Android 8/API 26 of hoger), met ingebouwde WebView.
- `Owon_NG-0.2.0-python.pyz`: starten met `python Owon_NG-0.2.0-python.pyz` (Python 3.10+). Op Linux/macOS werkt ook `python3`. Opent de UI in de browser; Ctrl+C stopt de lokale server.
- `Owon_NG-0.2.0-windows-x64.exe`: zelfstandige Windows x64-launcher, zonder Python/Node-installatie. Opent de UI in de standaardbrowser. Het consolevenster sluiten stopt de lokale server.

Deze pakketten bevatten dezelfde synthetische demo, zonder hardwareverbinding. Python en Windows luisteren uitsluitend op een lokale loopbackpoort. Android heeft geen internet-, USB- of bestandstoegangsrechten. De APK is met een ontwikkelsleutel ondertekend; een definitieve releasehandtekening is nog niet ingericht. Een APK uit een andere debug-build kan een andere sleutel hebben: verwijder in dat geval eerst de oudere demo. JSON-downloads via de Android WebView worden nog niet ondersteund; browserexports in Python/Windows blijven beschikbaar. Bewaren op Android is lokaal binnen de app en verdwijnt bij verwijderen van de app.

Bouwen: `npm ci && npm run build`, vervolgens:
```sh
python3 scripts/package.py python
python3 scripts/package.py windows
python3 scripts/package.py android
```
Voor Windows is een echte Go-toolchain (1.24+) op PATH vereist; `OWON_GO` kan een absoluut pad aanwijzen. Android vereist JDK 21, `ANDROID_HOME`, SDK platform 35 en build-tools 35.0.0. De APK-bouwer maakt zo nodig een debug-keystore buiten de checkout; `OWON_DEBUG_KEY` kan dat pad bepalen. De versie komt voor alle pakketten uit `package.json`; buildresultaten staan in `artifacts/`. De workflow **Versioned app packages** bouwt en uploadt ze als GitHub Actions artifacts, samen met SHA256-controlesommen en Go-licentieteksten. Binaire bestanden worden niet aan Git toegevoegd.

Validatie van de desktoplaunchers: bouw ook `python3 scripts/package.py linux` op Linux en voer `python3 -m unittest discover -s tests -p 'test_packaging.py' -v` uit. Dat test de Python-server en dezelfde native desktophost met echte HTTP-requests, plus de Windows PE-header. Dat is geen Windows- of Android-interactietest op een apparaat.
