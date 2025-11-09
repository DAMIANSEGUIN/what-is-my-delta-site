// inject_build_id.js
const fs = require('fs');
const path = require('path');
const BUILD_ID = process.env.BUILD_ID || 'local-dev';
const SPEC_SHA = process.env.SPEC_SHA || '0000000';

const targetRoot = process.env.BUILD_ID_TARGET_ROOT
  ? path.resolve(process.env.BUILD_ID_TARGET_ROOT)
  : process.cwd();

const files = process.env.BUILD_ID_TARGETS
  ? process.env.BUILD_ID_TARGETS.split(',').map(file => file.trim()).filter(Boolean)
  : ['frontend/index.html', 'mosaic_ui/index.html'];

let injected = 0;

files.forEach(filePath => {
  const entryPath = path.isAbsolute(filePath)
    ? filePath
    : path.resolve(targetRoot, filePath);
  if (fs.existsSync(entryPath)) {
    let html = fs.readFileSync(entryPath, 'utf8');
    html = html.replace(/<!-- BUILD_ID:.*? -->/, `<!-- BUILD_ID:${BUILD_ID}|SHA:${SPEC_SHA} -->`);
    fs.writeFileSync(entryPath, html);
    injected++;
  } else {
    console.warn(`BUILD_ID injection skipped: ${entryPath} not found`);
  }
});

console.log(`BUILD_ID injected successfully into ${injected} file(s).`);
