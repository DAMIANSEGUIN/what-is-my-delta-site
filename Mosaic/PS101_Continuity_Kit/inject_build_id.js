// inject_build_id.js
const fs = require('fs');
const path = require('path');
const BUILD_ID = process.env.BUILD_ID || 'local-dev';
const SPEC_SHA = process.env.SPEC_SHA || '0000000';

// Inject into both frontend and mosaic_ui
const files = ['frontend/index.html', 'mosaic_ui/index.html'];
let injected = 0;

files.forEach(filePath => {
  const entryPath = path.resolve(filePath);
  if (fs.existsSync(entryPath)) {
    let html = fs.readFileSync(entryPath, 'utf8');
    html = html.replace(/<!-- BUILD_ID:.*? -->/, `<!-- BUILD_ID:${BUILD_ID}|SHA:${SPEC_SHA} -->`);
    fs.writeFileSync(entryPath, html);
    injected++;
  }
});

console.log(`BUILD_ID injected successfully into ${injected} file(s).`);
