/* Shared, dependency-free search rules; also used by Node verification. */
(function(root){'use strict';
const fields=['direction_ids','experiment_type_ids','method_ids','application_ids','instrument_component_ids','information_type'];
const norm=s=>String(s||'').normalize('NFKC').toLowerCase().replace(/\s+/g,' ').trim();
function descendants(tax,dim,id){const out=new Set([id]);let changed=true;while(changed){changed=false;for(const t of tax.tags)if(t.dimension===dim&&t.parent_ids.some(p=>out.has(p))&&!out.has(t.id)){out.add(t.id);changed=true;}}return out;}
function matcher(tax,dim,id){const out=descendants(tax,dim,id);if(dim==='direction_ids'&&(id==='nmr'||id==='epr'))out.add('nmr_epr');return out;}
function filter(items,state,tax,skip){const words=norm(state.q).split(' ').filter(Boolean);return items.filter(a=>{if(state.date&&a.report_date!==state.date)return false;if(words.some(w=>!a._search.includes(w)))return false;for(const f of fields){if(f===skip||!state[f]?.length)continue;const vals=f==='information_type'?[a[f]]:a[f];if(!state[f].some(id=>{const matches=matcher(tax,f,id);return vals.some(v=>matches.has(v));}))return false;}return true;});}
function prepare(items,tax){const labels=new Map(tax.tags.map(t=>[t.id,[t.label_cn,t.label_en,...t.aliases].join(' ')]));return items.map(a=>({...a,_search:norm([a.title_cn,a.summary_cn,a.meaning_cn,a.doi,a.source,a.url,...a.sample_systems,...fields.flatMap(f=>Array.isArray(a[f])?a[f]:[a[f]]).map(id=>labels.get(id)||id)].join(' '))}));}
function parse(search,tax,latest,initial){const p=new URLSearchParams(search);const s={q:p.get('q')||'',date:p.get('date')||''};if(s.date&&!/^\d{4}-\d{2}-\d{2}$/.test(s.date))s.date='';if(initial&&!search)s.date=latest;for(const f of fields){const valid=new Set(tax.tags.filter(t=>t.dimension===f).map(t=>t.id));s[f]=[...new Set((p.get(f)||'').split(',').filter(id=>valid.has(id)))];}return s;}
function serialize(s){const p=new URLSearchParams();if(s.date)p.set('date',s.date);else p.set('view','all');if(s.q)p.set('q',s.q);for(const f of fields)if(s[f]?.length)p.set(f,s[f].join(','));return '?'+p.toString();}
const api={fields,norm,descendants,filter,prepare,parse,serialize};if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.SpinSearch=api;
})(typeof globalThis!=='undefined'?globalThis:this);
