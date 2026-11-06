# Open-source reference survey and reuse policy

**Reviewed initially:** 2026-11-06. Code reuse is encouraged **only with verified licences**. Codex should investigate other relevant libraries and repos per component, but must update this survey and provenance before adopting external code.

| Project | Why research it | Licence observed in GitHub repository | Reuse guidance |
| --- | --- | --- | --- |
| [serjster/neowon](https://github.com/serjster/neowon) | Rust OWON VDS1022(I) hardware integration, triggering, plotting, history, measurement UI, simulated backend | **MIT OR Apache-2.0** (both licence files present) | Strong future adapter candidate; inspect exact files/notices/third-party dependencies. UI ideas may be studied immediately. |
| [sigrok/PulseView](https://github.com/sigrokproject/pulseview) | Oscilloscope/logic-decoder workflows, protocol timelines, channel handling | **GPL-3.0** (GitHub metadata) | Study functionality/UX. **Do not import GPL code** into unlicensed/new project without owner-approved compatibility and distribution plan. |
| [OpenHantek/OpenHantek6022](https://github.com/OpenHantek/OpenHantek6022) | Scope controls, acquisition UI and performance patterns | **GPL-3.0** (GitHub metadata) | UX reference only by default; keep source separate. Different hardware. |
| [florentbr/OWON-VDS1022](https://github.com/florentbr/OWON-VDS1022) | VDS1022 API behaviors, calibration and documented hardware specifics | **No clear explicit licence located at inspected root** | Read docs for reference, do not copy source or assets absent explicit permission. |
| [Pico Technology / PicoScope](https://www.picotech.com/) | Usability/feature-quality benchmark, guided tests and workflow expectations | **Proprietary** | Never copy code, reference captures, proprietary procedures, text or UI artwork. Independent redesign only. |

## Mandatory research procedure before borrowing

1. Verify the current upstream repository, commit/tag, contributor/licence ownership and licence **for specific files**. A GitHub licence badge is not sufficient for every subdirectory or vendored asset.
2. Evaluate architecture integration, runtime/packaging cost, security and maintenance, and suitability for VDS1022I.
3. Verify dependencies and any copyleft, patent, NOTICE, attribution and redistribution conditions. Dual-licence choice must be recorded.
4. Record **exact URL + commit SHA + path(s) + licence + modifications + included notices** in \`docs/THIRD_PARTY.md\`.
5. Only then vendor/adapt code. Prefer adapter/API integration over copy/paste; avoid pulling in whole applications for small UI components.
6. If uncertain, do not copy; implement independently, note the missing legal permission or ask user for a licence choice.

## Suggested investigation for UI-001

- Compare neowon's core oscilloscope controls and state transitions and review any available demo UI.
- Review PulseView and OpenHantek as UX references without incorporating GPL source.
- Survey **small charting/Canvas, accessible UI controls and keyboard shortcut libraries**: record each candidate's exact licence and evaluate whether custom Canvas drawing is sufficient.
- Concentrate on maintaining correct waveform grids, cursor interaction, source badges, trigger affordances, accessibility and simple explanatory UX.
- Do not add device drivers or decoders to UI-001. That research is for architecture only.

## Native layout review — 0.3.2

- OpenHantek6022 revision 00a622ab2e18290af7c4290e492dadbec3321fb7: README.md and docs/images/screenshot_mainwindow.png visually reviewed. Useful patterns: dominant dark plotting surface, compact light control panels, colored channel identifiers and readouts below the trace.
- PulseView revision af02198741b4e57c9f9b796bd5e6c0f2ae9f2f2b: README and pv/mainwindow.cpp inspected for native toolbar, menu and dock organization. This motivated grouping secondary tools instead of presenting every explanation simultaneously.
- Both remain GPL research references. No source, icons, screenshots or other assets were copied into the application or this repository. The screenshot in docs/images/native-ui-0.3.2.png is an original rendering of Owon NG.
- PicoScope remains a workflow-quality benchmark; no proprietary materials were imported.

## Decoder UX direction supplied during acquisition-core work

The owner supplied a PicoScope screenshot demonstrating compact channel controls, synchronized analogue/digital traces and byte/field annotations on the signal time axis. Treat it as a workflow reference; no image, code, branding or proprietary example data is incorporated.

LabNation SmartScopeApp revision 76ceff0d6f2c7b91293c58612c59525ea50e074c: README.md, Drawables/GraphArea/Waveform/WaveformDecoded.cs and Drawables/GraphArea/Panorama.cs inspected. Useful general concepts: time-bounded decoder items, filtering annotations to the visible time window, numeric display formats and a capture overview. No explicit root licence grant was established by this inspection; do not reuse source/assets. No LabNation code is imported. Follow-up: immutable decode events tied to capture ID/sample indices and time-aligned native decoder lanes.
