const assert=require('node:assert/strict'),fs=require('node:fs'),C=require('../assets/search-core.js');
const path=require('node:path'),root=path.resolve(__dirname,'..');
const tax=JSON.parse(fs.readFileSync(path.join(root,'taxonomy/taxonomy.json')));
const data=JSON.parse(fs.readFileSync(path.join(root,'_site/search-index.json')));
const items=C.prepare(data.items,tax);const state=()=>({q:'',date:'',direction_match:'any',...Object.fromEntries(C.fields.map(f=>[f,[]]))});
assert.equal(items.length,381);assert.equal(C.filter(items,{...state(),date:'2026-10-05'},tax).length,10);
assert.equal(C.filter(items,{...state(),date:'2026-08-28'},tax).length,9);
assert.equal(C.filter(items,{...state(),date:'2026-10-06'},tax).length,0);
const mixed=items.find(a=>a.direction_ids.includes('nmr')&&a.direction_ids.includes('epr'));assert(mixed);for(const dir of ['nmr','epr'])assert(C.filter([mixed],{...state(),direction_ids:[dir]},tax).length===1);
const q=C.filter(items,{...state(),q:'DEER'},tax);assert(q.length>0);
assert(C.filter(items,{...state(),q:'10.1021/acs.analchem.6c02571'},tax).length>=1);
const parent=C.filter(items,{...state(),application_ids:['life_science']},tax),child=C.filter(items,{...state(),application_ids:['structural_biology']},tax);assert(child.length>0);assert(child.every(a=>parent.includes(a)));
const both=C.filter(items,{...state(),direction_ids:['nmr','epr']},tax),nmr=C.filter(items,{...state(),direction_ids:['nmr']},tax),epr=C.filter(items,{...state(),direction_ids:['epr']},tax);assert.equal(both.length,new Set([...nmr,...epr]).size);
const combo=C.filter(items,{...state(),direction_ids:['epr'],method_ids:['pds']},tax);assert(combo.length>0);assert(combo.every(a=>C.filter([a],{...state(),direction_ids:['epr']},tax).length));
const s={...state(),q:'顺磁 NMR',direction_ids:['nmr'],application_ids:['structural_biology']};assert.deepEqual(C.parse(C.serialize(s),tax,'2026-10-05',true),s);
assert.equal(C.parse('',tax,'2026-10-05',true).date,'2026-10-05');assert.equal(C.parse('?view=all',tax,'2026-10-05',true).date,'');assert.deepEqual(C.parse('?method_ids=unknown',tax,'2026-10-05',false).method_ids,[]);
assert(C.descendants(tax,'method_ids','mas').has('fast_mas'));assert(C.descendants(tax,'method_ids','pds').has('deer_peldor'));
console.log('PASS: date selection, missing days, DOI and method search, mixed direction, parent expansion, OR/AND, URL restore, invalid IDs');

assert.deepEqual(tax.tags.filter(t=>t.dimension==='direction_ids').map(t=>t.id),['nmr','epr']);
const intersection=C.filter(items,{...state(),direction_ids:['nmr','epr'],direction_match:'all'},tax);assert.equal(intersection.length,30);assert(intersection.every(a=>a.direction_ids.includes('nmr')&&a.direction_ids.includes('epr')));
const legacy=C.parse('?direction_ids=nmr_epr',tax,'2026-10-05',false);assert.equal(legacy.direction_match,'all');assert.deepEqual(legacy.direction_ids,['nmr','epr']);assert.equal(C.filter(items,legacy,tax).length,30);
for(const [old,exp] of [['mrs','in_vivo_mrs'],['mrv','mr_velocimetry']]){const migrated=C.parse('?direction_ids='+old,tax,'2026-10-05',false);assert.deepEqual(migrated.direction_ids,['nmr']);assert.deepEqual(migrated.experiment_type_ids,[exp]);assert(C.filter(items,migrated,tax).length>0);}
assert.deepEqual(C.parse(C.serialize(legacy),tax,'2026-10-05',false),legacy);
assert(items.every(a=>a.direction_ids.length>0&&a.direction_ids.every(id=>['nmr','epr'].includes(id))));
console.log('PASS: two canonical directions, 30 mixed entries, explicit AND, legacy mixed/MRS/MRV URLs');
