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
