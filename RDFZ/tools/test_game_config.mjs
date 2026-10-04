import assert from 'node:assert/strict';
import {gameConfig} from './game_config.mjs';
assert.deepEqual(gameConfig({}), {initialGems:3000,unlimitedGems:false});
assert.deepEqual(gameConfig({RDFZ_INITIAL_GEMS:'9000',RDFZ_UNLIMITED_GEMS:'true'}), {initialGems:9000,unlimitedGems:true});
assert.equal(gameConfig({RDFZ_INITIAL_GEMS:'0'}).initialGems,0);
for (const value of ['-1','NaN','3.5','','9007199254740992']) assert.throws(()=>gameConfig({RDFZ_INITIAL_GEMS:value}));
for (const value of ['1','yes','','TRUE']) assert.throws(()=>gameConfig({RDFZ_UNLIMITED_GEMS:value}));
console.log('Config defaults, overrides and invalid values passed');
