# Roadmap — UI first, features later

The **UI phase must be completed and user-reviewed first**. Do not work on the functional acquisition or diagnostic backend in an early UI batch. Each task is independently reviewable; the agent stops between batches.

| ID | Phase | Deliverable | Status |
|---|---|---|---|
| P0 | Bootstrap | Offline HTML prototype, specs, CI and agent handoff | Existing prototype in draft PR #1; agent handoff in same branch |
| UI-001 | UI | Production-structured frontend, navigation, core scope workspace, responsive layout, fixture architecture | **NEXT** |
| UI-002 | UI | Complete guided testing library UI, reference comparisons, history/session/report user journeys | Planned |
| UI-003 | UI | End-to-end UX audit, accessibility, visual refinement, keyboard/test automation, user acceptance | Planned |
| ENG-001 | Features | Versioned lossless capture model, validated math and replay foundations | Blocked until UI accepted |
| ENG-002 | Features | Real VDS1022I adapter, USB communications, sampling, error states, trigger mapping, hardware verification | Blocked until UI accepted |
| ENG-003 | Features | Efficient rendering, recording, DSP analysis, protocol decoding and reference-validation engine | Blocked until UI accepted |
| ENG-004 | Features | Automotive/electronics guided-testing engine, tested diagnostics and reporting | Blocked until UI accepted |
| ENG-005 | Release | Windows installer, documented driver setup, regression and device-in-the-loop tests | Blocked |

Notes:
- "PicoScope-grade" is a **quality target**, not a statement of performance parity.
- Research other repos early. Copy/adapt components **only** after licence analysis and provenance recording.
- Hardware restrictions remain: dual inputs with common ground, limited bandwidth/sample depth/record length, and accessory-dependent high-voltage tests.
- Store product/architecture decisions in \`docs/DECISIONS.md\`.
