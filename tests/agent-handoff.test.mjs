import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';

const docs = [
  'AGENTS.md',
  'docs/START_HERE.md',
  'docs/UI_SPEC.md',
  'docs/ROADMAP.md',
  'docs/ARCHITECTURE.md',
  'docs/THIRD_PARTY.md',
  'docs/REFERENCE_REPOS.md',
  'docs/DECISIONS.md',
  'docs/CODEX_START_PROMPT.md',
  'docs/tasks/UI-001.md',
  'docs/tasks/UI-002.md',
  'docs/tasks/UI-003.md'
];
for (const path of docs) assert(existsSync(new URL('../' + path, import.meta.url)), 'Missing handoff document: ' + path);
const read = (p) => readFileSync(new URL('../' + p, import.meta.url), 'utf8');
const agents = read('AGENTS.md');
const ui = read('docs/UI_SPEC.md');
const task = read('docs/tasks/UI-001.md');
const license = read('docs/THIRD_PARTY.md');
const roadmap = read('docs/ROADMAP.md');

for (const phrase of ['UI-001', 'PicoScope', 'VDS1022I', 'shared', 'licence']) {
  const combined = [agents, ui, task, license, roadmap].join('\n');
  assert(combined.toLowerCase().includes(phrase.toLowerCase()), 'Missing important project term: ' + phrase);
}
for (const phrase of ['CKP', 'Elektronica', 'Automotive', 'DEMO', 'information', 'simulation']) {
  const combined = [agents, ui, task].join('\n');
  assert(combined.toLowerCase().includes(phrase.toLowerCase()), 'Missing critical UI term: ' + phrase);
}
assert(agents.includes('before implementing real acquisition') || agents.includes('then build real software features'), 'UI-first rule is missing');
assert(task.includes('Do not implement USB integration'), 'First task must defer hardware');
assert(license.includes('florentbr') && license.includes('neowon'), 'Third-party status missing');
assert(roadmap.indexOf('UI-003') < roadmap.indexOf('ENG-002'), 'Hardware stage should be after UI milestone');
console.log('Agent handoff specification checks passed.');
