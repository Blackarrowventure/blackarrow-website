#!/usr/bin/env node
/* Makes the minified copies the pages actually load:
     3d/assets/js/3d-store.js   -> 3d-store.min.js     (and the other files listed below)
     assets/css/styles.css      -> styles.min.css
     assets/css/styles.css      -> styles-3d.min.css   (only the rules the 3D store uses)

   Edit the normal (non-.min) files, then run this before committing:
     node scripts/minify_assets.js
   It is also run at the end of scripts/generate_3d_static.py.
   A .min file older than its source means the site is serving stale code, so
   run it whenever any of the files below changes, then bump the ?v= numbers.

   Tools are pinned and fetched with npx: terser 5.36.0, lightningcss-cli 1.28.2, purgecss 6.0.0. */
'use strict';
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const JS = [
  '3d/assets/js/3d-store.js',
  '3d/assets/js/3d-i18n.js',
  '3d/assets/js/3d-reviews.js',
  '3d/assets/js/3d-welcome.js',
  '3d/assets/js/3d-consent.js',
  'assets/js/app.js',
];
const CSS = [
  '3d/assets/css/3d-store.css',
  'assets/css/styles.css',
];

const q = (p) => '"' + p.replace(/\\/g, '/') + '"';
const run = (cmd) => execSync(cmd, { cwd: ROOT, stdio: ['ignore', 'pipe', 'inherit'], shell: true });
const minName = (f) => f.replace(/\.(js|css)$/, '.min.$1');
const kb = (f) => (fs.statSync(path.join(ROOT, f)).size / 1024).toFixed(0) + ' KB';

for (const f of JS) {
  const out = minName(f);
  run(`npx -y terser@5.36.0 ${q(f)} --compress --mangle --comments false -o ${q(out)}`);
  console.log(f.padEnd(34), kb(f).padStart(7), '->', kb(out));
}
for (const f of CSS) {
  const out = minName(f);
  run(`npx -y lightningcss-cli@1.28.2 --minify --targets ">= 0.25%" ${q(f)} -o ${q(out)}`);
  console.log(f.padEnd(34), kb(f).padStart(7), '->', kb(out));
}

/* styles.css is the company site's stylesheet; the 3D store pages only use part of it
   (navbar, footer, buttons, sections). Keep every rule whose selectors appear in any 3D page
   or in the scripts that run there, and drop the rest. */
const tmp = path.join(ROOT, 'scripts', '_purge-tmp');
fs.rmSync(tmp, { recursive: true, force: true });
fs.mkdirSync(path.join(tmp, 'assets', 'css'), { recursive: true }); // purgecss keeps the source's folder path
// Written as JS source (not JSON) so the safelist regexes survive.
const cfgSrc = `module.exports = {
  content: ['3d/**/*.html', '3d/assets/js/*.js', 'assets/js/app.js', 'assets/js/ai-assistant.js', 'assets/js/save-contact.js'],
  css: ['assets/css/styles.css'],
  safelist: {
    standard: [/^is-/, /^has-/, /^js$/, /^no-js$/, /^reveal/, /^visible$/, /^active$/, /^open$/, /^scrolled$/, /^ba-ai/],
    greedy: [/rtl/, /lang/],
  },
  keyframes: true,
  fontFace: false,
  variables: false,
  output: ${JSON.stringify(tmp.split(path.sep).join('/'))},
};
`;
fs.writeFileSync(path.join(tmp, 'purgecss.config.js'), cfgSrc);
run(`npx -y purgecss@6.0.0 --config ${q(path.join(tmp, 'purgecss.config.js'))}`);
run(`npx -y lightningcss-cli@1.28.2 --minify --targets ">= 0.25%" ${q(path.join(tmp, 'assets', 'css', 'styles.css'))} -o ${q('assets/css/styles-3d.min.css')}`);
fs.rmSync(tmp, { recursive: true, force: true });
console.log('assets/css/styles.css (3D subset)'.padEnd(34), kb('assets/css/styles.css').padStart(7), '->', kb('assets/css/styles-3d.min.css'));
