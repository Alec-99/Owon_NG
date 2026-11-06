> **Current owner authorization (2026-11-06):** The owner now requests autonomous functional development starting with the acquisition/recording core, incorporating feedback without recurring review gates. This supersedes the earlier UI-only/stop-after-UI-001 instructions below. Native Qt is the chosen desktop UI. Keep hardware-dependent validation explicitly open; do not merge PRs or claim untested hardware support. See docs/ACQUISITION_CORE.md and docs/HARDWARE_VALIDATION.md.

# Codex agent instructions — Owon NG

Applies to the entire repository. This is an instruction document, not evidence that any feature has been implemented. Project name is provisional.

## Product vision

Build oscilloscope **software at PicoScope-grade UX and engineering quality**, for automotive diagnostics, electronics troubleshooting and learning. PicoScope is a benchmark for workflow quality, not a source of proprietary code, artwork, test descriptions or UI cloning. The first supported instrument is the OWON VDS1022I; its physical limits must be respected.

**Owner's mandated development order: complete the entire UI/UX foundation first, then build real software features and device integrations.**
- **Phase UI (now):** polished application experience, all principal screens, accessible controls, help, guided component-test catalogue, reference waveforms, measurements, cursors, diagnostics workflow, history, recording/replay, export, settings and failure/empty states. Use synthetic fixture signals, mock services and explicitly labeled demo-only actions. For UI completeness, all main user journeys must be clickable and coherent; no unimplemented action may pretend to have succeeded.
- **Phase functional (later, user approval required):** real signal-processing algorithms, driver connection and live acquisition, trigger implementation, protocol decoders, validated diagnostic rules and export.
- **Phase hardware validation (later):** test real devices/accessories and confirm voltages, calibrated scaling, timing, limits and stability.

## Before each task

Read, in order:
1. \`docs/START_HERE.md\` — branch strategy / commands / current state
2. \`docs/UI_SPEC.md\` — full UI/UX coverage and acceptance criteria
3. \`docs/ROADMAP.md\` — sequence
4. \`docs/tasks/UI-001.md\` — initial assigned task
5. \`docs/ARCHITECTURE.md\` and \`docs/THIRD_PARTY.md\`
6. \`docs/REFERENCE_REPOS.md\` — external-repository research and reuse rules

Default task: **UI-001**. Do not undertake UI-002 or UI-003 unless explicitly assigned. After completing a batch, open a PR and stop for review.

## Working practices

- Check branch, working tree, existing open PRs and CI before modifications. Preserve unrelated changes.
- Never push to \`main\` or merge a PR without explicit user approval. Use a task-named branch and open a PR against the base instructed in START_HERE.
- Implement assigned scope autonomously. Document substantial technical decisions in \`docs/DECISIONS.md\`; ask only on blocking legal, safety or incompatible product choices.
- Keep the prototype available as a runnable reference while migrating UI to a modular app; keep mock/demo mode usable without a connected device.
- Choose a small maintainable UI stack, preferably TypeScript + Vite + Canvas (or another choice with recorded justification). Keep components, presets, fixture generators, device boundary, persistence and visual rendering separate.
- Use predictable, deterministic samples for automated tests. Add accessibility and interaction checks. Verify build, lint and tests before stating success.
- Prioritize correct behavior, responsive performance and clarity over visual effects. Full coverage includes keyboard/mouse, small screens and error states.
- User interface language defaults to **Dutch**, structured for later i18n.
- Each important control has an **(i)** help action with brief plain-language explanation and optional engineering depth.

## External-source research: encouraged, with licences

Actively research existing projects for ideas or implementation building blocks, including **serjster/neowon**, **sigrok/PulseView**, **OpenHantek6022**, **florentbr/OWON-VDS1022**, and suitable open-source charting and UI libraries. Identify what to reuse and what to build independently.

Before copying any source, assets, examples or documentation: verify the **exact licence** at the target commit/file, copyright and NOTICE obligations, dependency/transitive licences, and project compatibility. Record upstream repository URL, revision, relevant file(s), licence, notices and our modifications in \`docs/THIRD_PARTY.md\` (or companion provenance table). Preserve notices in distribution. A repo without an explicit grant is *not* presumed reusable. GPL-3.0 projects are research/UX references by default: do not merge GPL source into this project unless the owner deliberately selects a compatible distribution/licensing strategy. Do not import OWON proprietary firmware or vendor assets without redistribution rights. Never copy PicoScope proprietary materials. Avoid importing external source for UI-001 unless clearly advantageous.

## Hard safety and truthfulness rules

- The **VDS1022I's two channels share a common ground**, even though the USB connection is isolated. Never show instructions connecting separate probe grounds to different electrical potentials.
- Never say a test of ignition high voltage, injector flyback, mains, EV high voltage or any other hazardous circuit is safe without validated probes, appropriate ratings and a safe approved procedure.
- Always label data as **DEMO / SIMULATED**, **IMPORTED**, or **LIVE HARDWARE** (live only when genuinely verified). Demo performance, measured numbers and pass/fail states must never masquerade as real hardware data.
- Do not fabricate precision, supported device settings, waveforms or diagnostic certainty; explicitly mark unimplemented and unavailable operations.
- Do not commit secrets, binary firmware, third-party copyright assets of unclear provenance or personal vehicle measurements.

## Definition of done for a batch

1. One cohesive working UI increment with realistic demo interactions; no dead buttons presented as working controls.
2. Accessibility basics: labels, focus order, contrast, no keyboard traps, reduced-motion where relevant.
3. Automated tests and CI updated for delivered behaviors; report exact commands and observed results.
4. README/run instructions and current implemented-versus-mocked status updated.
5. Licensing and safety audit recorded, including external code attribution when applicable.
6. PR with summary, screenshots if helpful, test results, known limitations and next milestones.
7. **Stop** at the assigned batch; wait for user's feedback.
