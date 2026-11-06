# Third-party software and licence policy

Reviewed: 2026-11-06. This document describes the sources consulted for design, not vendored dependencies.

| Project | Observed licence status | Current usage | Reuse rule |
| --- | --- | --- | --- |
| [serjster/neowon](https://github.com/serjster/neowon) | Dual MIT OR Apache-2.0 (`LICENSE-MIT`, `LICENSE-APACHE` in upstream repository) | Documentation/architecture reference only | Code may be adapted in a future commit after preserving required copyright/licence/NOTICE information and documenting precise files/changes. |
| [florentbr/OWON-VDS1022](https://github.com/florentbr/OWON-VDS1022) | No top-level licence file found in inspected repository root; explicit permission not established | Public API documentation reference only, **no source copied** | Do not vendor or adapt source until permission/licence is verified. Reimplement behavior independently if necessary. |
| OWON vendor app/FPGA bitstreams | Vendor-owned; redistribution rights not established here | Not included | Do not vendor proprietary files or firmware absent explicit authorization. |
| PicoScope/Pico Automotive | Proprietary | Independent product-quality benchmark only | Do not copy code, artwork, example captures or proprietary guided tests. |

## Provenance of this branch

The HTML, CSS, JavaScript and Markdown in this branch are newly authored for Owon NG. They do not embed another repository's implementation, binary assets, reference waveforms or icons. All example traces are generated mathematically as synthetic simulations. No runtime dependencies or third-party fonts are used.

The repository owner has **not yet selected a licence for the new project**. Absence of a licence must not be interpreted as permission for outside copying or reuse. Choose a project licence as a separate explicit decision before distributing derived components.

## Rules for future contributions

1. Track upstream commit, URL, filename, original licence and changed lines for any imported code or asset.
2. Prefer upstream APIs and clearly documented adapters over indiscriminate copy/paste.
3. Check dependencies, transitive licences and platform distribution rules before release.
4. Bundle exact required copyright and licence notices when a dependency is incorporated.
5. Reject unclear/proprietary redistribution unless permission is documented.
6. Keep a separate hardware firmware provenance/redistribution register.


## Additional UX research references (no code imported)

- [sigrok/PulseView](https://github.com/sigrokproject/pulseview) — GPL-3.0 according to GitHub metadata. UX and protocol-timeline research only until project licensing is compatible and explicitly approved.
- [OpenHantek/OpenHantek6022](https://github.com/OpenHantek/OpenHantek6022) — GPL-3.0 according to GitHub metadata. UX/measurement control research only; don't copy code into the repo by default.
- [REFERENCE_REPOS.md](REFERENCE_REPOS.md) lists source investigation guidance and the steps required before adoption.

**Current implementation provenance:** The Codex instruction/requirements/task files added in the handoff are new project documents. No third-party source code, proprietary waveforms or vendor assets were imported in this handoff.

## UI-001 dependency and research update (2026-11-06)

The app foundation uses Vite and TypeScript as pinned development dependencies; no third-party runtime library, UI framework, chart package, font, asset or upstream source code was added. The trace renderer and fixture models are original project code. Existing reference survey remains research-only. GitHub API queries for live upstream metadata and open PR/issue/CI status were rejected with `Forbidden` during this task, so no new licence claims are made and no upstream code was reused.

## Versioned launchers (2026-11-06)

Python launcher source, Go launcher source, Android Activity and packaging scripts are newly authored. Android uses only platform classes supplied by the device; no AndroidX or other runtime libraries are bundled. Python is a prerequisite and is not bundled. The Windows EXE includes the Go standard library/runtime (BSD-3-Clause); its LICENSE and vendored library licences from the actual build toolchain are copied to artifacts/THIRD_PARTY_NOTICES. The local build used the checksum-verified official Go 1.27.3 toolchain. SDK/build tools are build prerequisites and are not redistributed in the APK. No code from the previously surveyed oscilloscope projects was incorporated.
