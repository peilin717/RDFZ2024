// Dependency-free static build: publish optimized artwork, not the source PNGs.
import {cp, mkdir, readFile, rm, stat, writeFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import path from 'node:path';

import {gameConfig} from './game_config.mjs';
const config = gameConfig(); // Validate before replacing any existing build.

const root = fileURLToPath(new URL('../', import.meta.url));
const output = path.join(root, 'dist');
const manifestSource = await readFile(path.join(root, 'asset-manifest.js'), 'utf8');
const manifest = JSON.parse(manifestSource.split(' = ')[1].trim().replace(/;$/, ''));
const musicSource = await readFile(path.join(root, 'music-manifest.js'), 'utf8');
const music = JSON.parse(musicSource.split(' = ')[1].trim().replace(/;$/, ''));
const sfxSource = await readFile(path.join(root, 'sfx-manifest.js'), 'utf8');
const sfx = JSON.parse(sfxSource.split(' = ')[1].trim().replace(/;$/, ''));
const assets = [...new Set([...Object.values(manifest).flatMap(Object.values), ...Object.values(music.cues).flatMap(c=>[c.ogg,c.mp3]), ...Object.values(sfx.cues).flatMap(c=>[c.ogg,c.mp3])])];
// Fail before replacing a valid build if generated artwork is missing.
for (const asset of assets) await stat(path.join(root, asset));
await rm(output, {recursive: true, force: true});
await mkdir(output, {recursive: true});
const entry = await readFile(path.join(root, 'index.html'), 'utf8');
const files = ['index.html', 'music-credits.html', 'music/licenses/GeneralUser-GS.txt', 'music/licenses/Salamander-FreePats.txt', ...new Set([...entry.matchAll(/(?:src|href)="([^"?#]+\.(?:js|css))"/g)].map(match => match[1]))];
for (const name of files) {await mkdir(path.dirname(path.join(output,name)),{recursive:true});await cp(path.join(root, name), path.join(output, name));}
await writeFile(path.join(output, 'game-config.js'), `window.RDFZGameConfig = Object.freeze(${JSON.stringify(config)});\n`);
await mkdir(path.join(output, 'assets/web'), {recursive: true});
await mkdir(path.join(output, 'assets/music'), {recursive: true});
await mkdir(path.join(output, 'assets/sfx'), {recursive: true});
for (const asset of assets) await cp(path.join(root, asset), path.join(output, asset));
const sizes = await Promise.all([...files, ...assets].map(async name => (await stat(path.join(output, name))).size));
console.log(`Built ${files.length} entry files and ${assets.length} image/audio assets (${(sizes.reduce((a,b)=>a+b,0)/1024/1024).toFixed(2)} MiB) into ${output}`);
