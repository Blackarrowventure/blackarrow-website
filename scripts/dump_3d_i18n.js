// Refreshes scripts/_3d-i18n-dump.json (read by generate_3d_static.py) from 3d/assets/js/3d-i18n.js.
// Usage: node scripts/dump_3d_i18n.js
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const root = path.join(__dirname, '..');
const src = fs.readFileSync(path.join(root, '3d/assets/js/3d-i18n.js'), 'utf8');
// Evaluate only the DICT literal, so nothing touches a DOM.
const start = src.indexOf('var DICT = {');
let i = src.indexOf('{', start), depth = 0, end = -1, q = null;
for (; i < src.length; i++) {
  const c = src[i];
  if (q) { if (c === '\\') { i++; continue; } if (c === q) q = null; continue; }
  if (c === "'" || c === '"' || c === '`') { q = c; continue; }
  if (c === '{') depth++;
  else if (c === '}') { depth--; if (depth === 0) { end = i + 1; break; } }
}
const DICT = vm.runInNewContext('(' + src.slice(src.indexOf('{', start), end) + ')');
const out = {};
for (const k of Object.keys(DICT.en).sort()) out[k] = { en: DICT.en[k], ar: DICT.ar[k] !== undefined ? DICT.ar[k] : DICT.en[k] };
for (const k of Object.keys(DICT.ar)) if (!out[k]) out[k] = { en: k, ar: DICT.ar[k] };
fs.writeFileSync(path.join(root, 'scripts/_3d-i18n-dump.json'), JSON.stringify(out, null, 2) + '\n');
console.log('keys:', Object.keys(out).length);
