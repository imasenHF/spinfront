"""Build the SpinFront static archive from canonical issue JSON (Python stdlib)."""
import argparse,datetime,html,json,re,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FIELDS=['direction_ids','experiment_type_ids','method_ids','application_ids','instrument_component_ids']
REQUIRED=['item_id','report_date','item_no','title_cn',*FIELDS,'sample_systems','information_type','summary_cn','meaning_cn','publication_date','time_scope','source','url','doi','alternative_sources','related_to','review_status','first_seen','last_updated','report_file']
def read(path):return json.loads(path.read_text(encoding='utf-8'))
def esc(s):return html.escape(str(s or ''))
def link(url,label):
 if not re.match(r'^https?://',url or '',re.I):raise ValueError('Unsupported source URL')
 return '<a href="'+html.escape(url,quote=True)+'" rel="noopener noreferrer">'+esc(label)+'</a>'
def load():
 tax=read(ROOT/'taxonomy/taxonomy.json');labels={(t['dimension'],t['id']):t['label_cn'] for t in tax['tags']};issues=[];seen=set()
 for p in sorted((ROOT/'data').glob('*/SpinFront_*.json')):
  d=read(p);date=d['report_date'];datetime.date.fromisoformat(date)
  assert p.stem=='SpinFront_'+date and d['taxonomy_version']==tax['taxonomy_version'],p
  for n,a in enumerate(d['items'],1):
   assert all(k in a for k in REQUIRED),(p,n,'missing field')
   assert a['item_no']==n and a['report_date']==date and a['item_id']==f'SF-{date.replace("-", "")}-{n:02d}',(p,n,'identity/order')
   assert a['item_id'] not in seen;seen.add(a['item_id'])
   assert a['time_scope'] in ['24h','7d_extension']
   assert all(a[k] for k in ['title_cn','summary_cn','meaning_cn','source','url'])
   for f in FIELDS:assert isinstance(a[f],list) and all((f,t) in labels for t in a[f]),(p,n,f)
   assert a.get('publication_status','unknown') in ['unknown','preprint','early_access','published']
   assert ('information_type',a['information_type']) in labels
   link(a['url'],a['source'])
   for src in a['alternative_sources']:link(src['url'],src['name'])
   assert not any(k.lower() in ['image','images','image_url','image_data','image_keywords'] for k in a)
  issues.append(d)
 for dim,groups in tax.get('ui_groups',{}).items():
  roots={t['id'] for t in tax['tags'] if t['dimension']==dim and not t['parent_ids']}
  ids=[id for g in groups for id in g['ids']]
  assert len(ids)==len(set(ids)) and set(ids)==roots,(dim,'UI group coverage')
 app_roots={t['id'] for t in tax['tags'] if t['dimension']=='application_ids' and not t['parent_ids']}
 domain_ids=[id for g in tax['application_domains'] for id in g['ids']]
 assert len(domain_ids)==len(set(domain_ids)) and set(domain_ids)==app_roots,'Application domain coverage'
 assert {t['id'] for t in tax['tags'] if t['dimension']=='direction_ids'}=={'nmr','epr'}
 assert all(a['direction_ids'] for d in issues for a in d['items'])
 assert len({d['report_date'] for d in issues})==len(issues)
 return tax,labels,issues

def shell(title,body,prefix,standalone=False):
 template=(ROOT/'templates/issue.html').read_text(encoding='utf-8')
 styles=('<style>'+(ROOT/'assets/style.css').read_text(encoding='utf-8')+'</style>') if standalone else '<link rel="stylesheet" href="'+prefix+'assets/style.css">'
 return template.replace('{{TITLE}}',esc(title)).replace('{{STYLES}}',styles).replace('{{BODY}}',body)

def hero(date=''):return '<header class="hero"><h1>自旋前沿｜SpinFront</h1><p class="en">NMR / EPR Daily Brief</p><p>追踪自旋、谱学与应用进展</p>'+('<p>'+esc(date)+'</p>' if date else '')+'</header>'
def footer(date):return '<footer class="footer"><div>SpinFront · NMR / EPR Daily Brief · '+esc(date)+'</div><div>© '+date[:4]+' wuhaifeng@ustc.edu.cn. All rights reserved.</div><div>本报告版权归作者所有，未经许可不得复制、转载或用于商业用途。</div></footer>'
def issue_html(d,labels,standalone=False):
 date=d['report_date'];body=('<a class="archive-link" href="https://plastocyanin.org/spinfront/">← SpinFront归档</a>' if standalone else '<a class="archive-link" href="../">← SpinFront归档</a>')+hero(date)+'<div class="note"><p>'+esc(d['scope_note'])+'</p></div>'
 for a in d['items']:
  time='近7天扩展' if a['time_scope']=='7d_extension' else '近24小时'
  tags=[labels[(f,t)] for f in FIELDS for t in a[f]]
  body+='<article class="card" id="'+a['item_id']+'"><div class="top"><span class="num">'+f'{a["item_no"]:02d}'+'</span><span class="type">'+esc(labels[('information_type',a['information_type'])])+'</span><span class="tag">'+time+'</span></div><div class="content"><h2>'+esc(a['title_cn'])+'</h2><div class="labels">'+''.join('<span>'+esc(t)+'</span>' for t in tags)+'</div><p>'+esc(a['summary_cn']).replace('\n','<br>')+'</p><p><span class="label">具体意义：</span>'+esc(a['meaning_cn']).replace('\n','<br>')+'</p><div class="meta">发布日期：'+esc(a['publication_date'] or '待核实')+'｜'+time+'<br>原始来源：'+link(a['url'],a['source'])+''.join(' · '+link(s['url'],s['name']) for s in a['alternative_sources'])+('<br>DOI：'+esc(a['doi']) if a['doi'] else '')+'</div></div></article>'
 return shell('自旋前沿｜SpinFront｜'+date,body+footer(date),'../',standalone)
def archive_html(issues):
 groups={}
 for d in reversed(issues):groups.setdefault(d['report_date'][:7],[]).append(d)
 years=sorted({m[:4] for m in groups},reverse=True)
 out=['<div class="archive-controls"><label for="archive-year">年份</label><select id="archive-year">'+''.join('<option>'+y+'</option>' for y in years)+'</select><div id="archive-months" class="month-tabs"></div></div>']
 for month,ds in groups.items():
  out.append('<section class="archive-month-panel" data-month="'+month+'"><h3>'+month+' <small>'+str(len(ds))+'期</small></h3><ul class="archive-date-grid">')
  for d in reversed(ds):
   date=d['report_date'];day=datetime.date.fromisoformat(date)
   out.append('<li><a href="'+date+'/"><strong>'+date[8:]+'</strong><span>周'+"一二三四五六日"[day.weekday()]+'</span><small>'+str(len(d['items']))+'条 ↗</small></a></li>')
  out.append('</ul></section>')
 return ''.join(out)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',default='_site');args=ap.parse_args();tax,labels,issues=load()
 if args.check:print(f'Validated {len(issues)} issues / {sum(len(d["items"]) for d in issues)} items');return
 out=(ROOT/args.output).resolve();assert out!=ROOT and ROOT in out.parents,'Output must be a child directory of this repo'
 out.mkdir(parents=True,exist_ok=True);shutil.copytree(ROOT/'assets',out/'assets',dirs_exist_ok=True);shutil.copytree(ROOT/'data',out/'data',dirs_exist_ok=True);shutil.copytree(ROOT/'taxonomy',out/'taxonomy',dirs_exist_ok=True)
 downloads=out/'downloads';downloads.mkdir(exist_ok=True)
 listings=[]
 for d in reversed(issues):
  date=d['report_date'];p=out/date;p.mkdir(exist_ok=True);s=issue_html(d,labels);(p/'index.html').write_text(s,encoding='utf-8');(downloads/f'SpinFront_{date}.html').write_text(issue_html(d,labels,standalone=True),encoding='utf-8')
  assert s.count('<article ')==len(d['items']) and '<img' not in s
  for a in d['items']:
   for k in ['title_cn','summary_cn','meaning_cn']:assert esc(a[k]).replace('\n','<br>') in s
  listings.append('<li><a href="'+date+'/">'+date+'</a><span>'+str(len(d['items']))+'条</span></li>')
 template=(ROOT/'templates/home.html').read_text(encoding='utf-8')
 facet_html='<section class="facet primary-facet"><h3>谱学方向 <small id="facet-count-0"></small></h3><div id="facet-0"></div></section><section class="facet primary-facet"><h3>应用领域 <small id="facet-count-3"></small></h3><div id="facet-3"></div></section><details class="advanced-filters"><summary>高级筛选 <small id="advanced-count"></small></summary><label class="joint-option"><input type="checkbox" id="joint-only">仅同时涉及 NMR 与 EPR</label>'
 for i,name in [(2,'方法'),(1,'实验类型'),(5,'信息类型'),(4,'仪器部件')]:
  facet_html+='<details class="facet"><summary>'+name+'<small id="facet-count-'+str(i)+'"></small></summary><div class="facet-options" id="facet-'+str(i)+'"></div></details>'
 facet_html+='</details>'
 for key,value in {'{{TOTAL}}':f'{len(issues)}期 · {sum(len(d["items"]) for d in issues)}条','{{RANGE}}':issues[0]['report_date']+' — '+issues[-1]['report_date'],'{{YEAR}}':str(datetime.date.today().year),'{{FACETS}}':facet_html,'{{ARCHIVE}}':archive_html(issues)}.items():template=template.replace(key,value)
 (out/'index.html').write_text(template,encoding='utf-8')
 compact_fields=['item_id','item_no','report_date','title_cn','summary_cn','meaning_cn','publication_date','source','url','doi','sample_systems',*FIELDS,'information_type']
 compact={'taxonomy_version':tax['taxonomy_version'],'issues':[{'report_date':d['report_date'],'item_count':len(d['items'])} for d in issues],'items':[{**{k:a[k] for k in compact_fields},'publication_status':a.get('publication_status','unknown')} for d in issues for a in d['items']]}
 (out/'search-index.json').write_text(json.dumps(compact,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
 (out/'.nojekyll').write_text('');(out/'index.json').write_text(json.dumps({'schema_version':'1.4-tag-reviewed','taxonomy_version':tax['taxonomy_version'],'issues':[{'report_date':d['report_date'],'item_count':len(d['items']),'url':d['report_date']+'/','data_url':f'data/{d["report_date"][:4]}/SpinFront_{d["report_date"]}.json'} for d in issues],'items':[a for d in issues for a in d['items']]},ensure_ascii=False),encoding='utf-8');print(f'Built {len(issues)} issues')
if __name__=='__main__':main()
