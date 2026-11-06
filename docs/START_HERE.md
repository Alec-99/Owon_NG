> **Current state, 0.4.0:** Native Python/Qt app runs with python app.py after installing requirements-native.txt. The owner authorized autonomous acquisition-core development beyond UI-001. Branch codex/acquisition-core is based on codex/UI-001-app-foundation (still unmerged). Target its PR at that branch; merge nothing. Active boundaries/tests: ACQUISITION_CORE.md. Hardware checks: HARDWARE_VALIDATION.md. Earlier HTML/TypeScript notes below are historical.

# Owon NG — start here (Codex)

## State of repository

Current base for this handoff is **\`feat/first-ux-prototype\`**, reviewed in draft pull request [#1](https://github.com/Alec-99/Owon_NG/pull/1). At creation, \`main\` contains only the original README. Do not assume the handoff files are already merged into \`main\`.

The current \`prototype/index.html\` is a stand-alone HTML/CSS/JS demo. It has mock automotive and electronics waveforms, two channels, time/div, volts/div, a visual (not actual) trigger marker, cursors, basic measurements, help, JSON/CSV support and guided example text. **No hardware connection, real decoder or validated diagnostic engine exists.**

## First task: UI-001

Read root \`AGENTS.md\`, \`docs/UI_SPEC.md\`, \`docs/ROADMAP.md\`, \`docs/tasks/UI-001.md\`, \`docs/THIRD_PARTY.md\` and \`docs/REFERENCE_REPOS.md\`. The first task builds a maintainable application UI rather than implementing device drivers.

## Worktree and PR workflow

For the first task:

\`\`\`bash
git clone https://github.com/Alec-99/Owon_NG.git
cd Owon_NG
git fetch origin
git switch --track origin/feat/first-ux-prototype
git switch -c codex/UI-001-app-foundation
node tests/ui-contract.test.mjs
\`\`\`

If the repo is already checked out, inspect the branch and use \`git fetch\` plus a fresh task branch from \`origin/feat/first-ux-prototype\`.

- Implement **UI-001 only**.
- Open a pull request: **base = \`feat/first-ux-prototype\`**, **head = \`codex/UI-001-app-foundation\`**.
- Do **not** merge either PR. Later the owner can merge the base PR and UI tasks in order.
- If \`main\` has already received PR #1, switch to updated \`main\` and target \`main\` instead, but confirm against actual repository state first.

## Baseline tests

\`\`\`bash
node tests/ui-contract.test.mjs
\`\`\`

CI: \`.github/workflows/prototype-check.yml\`. The new modular application may introduce its own npm scripts / tests; Codex must document and run them, and add appropriate CI checks.

## UX direction

- Target **Windows desktop first**, but remain responsive and platform-neutral.
- User-facing text: Dutch, prepared for translation.
- Support automotive, electronics and free oscilloscope workspaces.
- Guide people through **test selection → safe setup → example/reference → measurement → interpretation → notes/report**.
- Provide basic and advanced help behind information controls.
- Design all user workflows first; **defer functional hardware/decoders/diagnostic engines** until the owner approves the UI.
- Proactively study other open-source instrument applications, with licence checks before any reuse.

## Reporting

Write a PR summary that distinguishes demo-only UI, real implemented client-side operations, placeholders and future hardware-dependent work. Provide run/test instructions and screenshots where possible. Stop after UI-001.
