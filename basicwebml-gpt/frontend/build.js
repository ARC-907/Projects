const esbuild = require('esbuild');
const fs = require('fs');
const path = require('path');

const buildDir = path.join(__dirname, 'build');
fs.rmSync(buildDir, { recursive: true, force: true });
fs.mkdirSync(buildDir, { recursive: true });

esbuild.buildSync({
  entryPoints: ['src/index.js'],
  bundle: true,
  outfile: path.join(buildDir, 'bundle.js'),
  loader: { '.js': 'jsx', '.jsx': 'jsx' },
  platform: 'browser',
});

fs.copyFileSync('index.html', path.join(buildDir, 'index.html'));
