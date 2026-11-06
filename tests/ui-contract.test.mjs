import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { Script } from 'node:vm';

const html = readFileSync(new URL('../prototype/index.html', import.meta.url), 'utf8');
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];
assert.equal(scripts.length, 1, 'One inline standalone script is expected');
new Script(scripts[0][1], { filename: 'prototype-inline.js' });

const ids = [...html.matchAll(/\bid="([^"]+)"/g)].map((x) => x[1]);
assert.equal(new Set(ids).size, ids.length, 'DOM element IDs must be unique');
const references = [...scripts[0][1].matchAll(/\$\('([^']+)'\)/g)].map((x) => x[1]);
for (const id of references) assert(ids.includes(id), 'Missing element id: ' + id);
assert(html.includes('DEMOMODUS'), 'Simulated data must be labeled');
assert(html.includes('Gedeelde massa'), 'Shared-ground warning must be visible');
assert(html.includes('origin:\'synthetic-demo\''), 'Export origin must identify simulation');
assert(!/<script[^>]+src=/.test(html), 'Prototype should work without third-party script URLs');
assert(!/<link[^>]+href=/.test(html), 'Prototype should work without external stylesheets');
console.log('Standalone HTML syntax and UI contract checks passed.');
