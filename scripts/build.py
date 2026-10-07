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

MONTHS_EN=['January','February','March','April','May','June','July','August','September','October','November','December']

def spinfront_wordmark():
 return 'SpinFr<span class="gold-o">o</span>nt'

def issue_href(date,standalone=False):
 if not date:return ''
 return ('https://plastocyanin.org/spinfront/'+date+'/' if standalone else '../'+date+'/')

def archive_href(standalone=False):
 return 'https://plastocyanin.org/spinfront/' if standalone else '../'

def cutoff_label(note):
 m=re.search(r'检索截至(\\d{4}-\\d{2}-\\d{2})\\s+([0-9:]+)（([^）]+)）',note or '')
 return (m.group(2)+' · '+m.group(3)) if m else 'SEE EDITORIAL NOTE'

def issue_header(d,standalone=False):
 date=d['report_date'];day=datetime.date.fromisoformat(date)
 archive=archive_href(standalone);nmr=sum('nmr' in a['direction_ids'] for a in d['items']);epr=sum('epr' in a['direction_ids'] for a in d['items'])
 scopes={a['time_scope'] for a in d['items']}
 scope='7-DAY EXTENSION' if scopes=={'7d_extension'} else ('24H' if scopes=={'24h'} else '24H + 7D')
 return '<header class="issue-topbar"><a class="plastocyanin-link" href="https://plastocyanin.org/">plastocyanin<span>.</span></a><a class="archive-link" href="'+archive+'">Daily archive →</a></header><section class="cover"><div class="cover-main"><div class="eyebrow">NMR / EPR Daily Brief</div><a class="hero-title" href="'+archive+'"><h1>'+spinfront_wordmark()+'</h1></a><p class="deck">追踪自旋、谱学与应用进展。每日筛选磁共振研究、方法、仪器与应用信息。</p><div class="issue-stats"><span>'+str(len(d['items']))+' reports</span><span>NMR '+str(nmr)+'</span><span>EPR '+str(epr)+'</span><span>'+scope+'</span></div></div><div class="cover-date"><strong>'+date[8:]+'</strong><div class="month">'+MONTHS_EN[day.month-1]+'</div><div class="year">'+date[:4]+' · DAILY ISSUE</div><div class="scope-chip">Search cutoff<br>'+esc(cutoff_label(d.get('scope_note','')))+'</div></div></section>'

def scope_block(note):
 return '<details class="scope"><summary>本期检索范围与筛选说明</summary><div class="scope-copy"><span>EDITORIAL NOTE</span><p>'+esc(note)+'</p></div></details>'

def issue_nav(prev_date,next_date,standalone=False):
 prev=('<a class="prev" href="'+issue_href(prev_date,standalone)+'"><small>PREVIOUS ISSUE</small><strong>← '+esc(prev_date)+'</strong></a>' if prev_date else '<span></span>')
 nxt=('<a class="next" href="'+issue_href(next_date,standalone)+'"><small>NEXT ISSUE</small><strong>'+esc(next_date)+' →</strong></a>' if next_date else '<span></span>')
 return '<nav class="issue-nav" aria-label="相邻日报">'+prev+nxt+'</nav>'

def footer(date,standalone=False):
 archive=archive_href(standalone)
 return '<footer class="footer"><div><a class="footer-brand" href="'+archive+'">'+spinfront_wordmark()+'</a><br>NMR / EPR Daily Brief · '+esc(date)+'</div><div class="footer-right">© '+date[:4]+' wuhaifeng@ustc.edu.cn. All rights reserved.<br>本报告版权归作者所有，未经许可不得复制、转载或用于商业用途。</div></footer>'

def issue_html(d,labels,prev_date='',next_date='',standalone=False):
 date=d['report_date'];body=issue_header(d,standalone)+scope_block(d.get('scope_note',''))+'<section class="issue">'
 for a in d['items']:
  time='近7天扩展' if a['time_scope']=='7d_extension' else '近24小时'
  tags=[labels[(f,t)] for f in FIELDS for t in a[f]]
  side=[str(t).replace('_',' ').upper() for f in FIELDS for t in a[f]]
  source=link(a['url'],a['source'])+''.join(' · '+link(s['url'],s['name']) for s in a['alternative_sources'])
  doi=('<a href="https://doi.org/'+html.escape(a['doi'],quote=True)+'" rel="noopener noreferrer">'+esc(a['doi'])+'</a>' if a['doi'] else '—')
  body+='<article class="story" id="'+a['item_id']+'"><div class="story-index">'+f'{a["item_no"]:02d}'+'<span>/</span></div><div class="story-main"><div class="story-type">'+esc(labels[('information_type',a['information_type'])])+' · '+time+'</div><h2>'+esc(a['title_cn'])+'</h2><div class="story-tags-inline">'+''.join('<span>'+esc(t)+'</span>' for t in tags)+'</div><p class="summary">'+esc(a['summary_cn']).replace('\n','<br>')+'</p><aside class="commentary"><div class="commentary-label">TECHNICAL COMMENTARY</div><p>'+esc(a['meaning_cn']).replace('\n','<br>')+'</p></aside><div class="story-meta"><span>Published</span><strong>'+esc(a['publication_date'] or '待核实')+'</strong><span>Source</span><div>'+source+'</div><span>DOI</span><div class="doi">'+doi+'</div></div></div><div class="story-side">'+('<br>'.join(esc(t) for t in side) if side else esc(labels[('information_type',a['information_type'])]))+'</div></article>'
 body+='</section>'+issue_nav(prev_date,next_date,standalone)+footer(date,standalone)
 return shell('SpinFront · '+date,body,'../',standalone)
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

def latest_feature(d):
 date=d['report_date'];day=datetime.date.fromisoformat(date);nmr=sum('nmr' in a['direction_ids'] for a in d['items']);epr=sum('epr' in a['direction_ids'] for a in d['items'])
 stories=''.join('<article class="latest-story"><span>'+f'{a["item_no"]:02d}'+' /</span><h2><a href="'+date+'/#'+a['item_id']+'">'+esc(a['title_cn'])+'</a></h2><small>'+esc(a['source'])+'</small></article>' for a in d['items'][:4])
 return '<section class="mag-front"><div class="mag-front-main"><div class="mag-eyebrow">NMR / EPR Daily Brief</div><h1>'+spinfront_wordmark()+'</h1><p>追踪自旋、谱学与应用进展。每日筛选磁共振研究、方法、仪器与应用信息。</p><div class="mag-stats"><span>'+str(len(d['items']))+' reports</span><span>NMR '+str(nmr)+'</span><span>EPR '+str(epr)+'</span></div></div><aside class="mag-latest-date"><small>LATEST ISSUE</small><strong>'+date[8:]+'</strong><span>'+MONTHS_EN[day.month-1]+'</span><em>'+date[:4]+'</em><a href="'+date+'/">Read full issue →</a></aside></section><section class="latest-issue"><header><div><span>LATEST ISSUE</span><h2>'+esc(date)+'</h2></div><a href="'+date+'/">READ FULL ISSUE →</a></header><div class="latest-stories">'+stories+'</div></section>'

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',default='_site');args=ap.parse_args();tax,labels,issues=load()
 if args.check:print(f'Validated {len(issues)} issues / {sum(len(d["items"]) for d in issues)} items');return
 out=(ROOT/args.output).resolve();assert out!=ROOT and ROOT in out.parents,'Output must be a child directory of this repo'
 out.mkdir(parents=True,exist_ok=True);shutil.copytree(ROOT/'assets',out/'assets',dirs_exist_ok=True);shutil.copytree(ROOT/'data',out/'data',dirs_exist_ok=True);shutil.copytree(ROOT/'taxonomy',out/'taxonomy',dirs_exist_ok=True)
 downloads=out/'downloads';downloads.mkdir(exist_ok=True)
 listings=[]
 for i,d in enumerate(issues):
  date=d['report_date'];prev_date=issues[i-1]['report_date'] if i>0 else '';next_date=issues[i+1]['report_date'] if i+1<len(issues) else ''
  p=out/date;p.mkdir(exist_ok=True);s=issue_html(d,labels,prev_date,next_date);(p/'index.html').write_text(s,encoding='utf-8');(downloads/f'SpinFront_{date}.html').write_text(issue_html(d,labels,prev_date,next_date,standalone=True),encoding='utf-8')
  assert s.count('<article ')==len(d['items']) and '<img' not in s
  for a in d['items']:
   for k in ['title_cn','summary_cn','meaning_cn']:assert esc(a[k]).replace('\n','<br>') in s
  listings.append('<li><a href="'+date+'/">'+date+'</a><span>'+str(len(d['items']))+'条</span></li>')
 template=(ROOT/'templates/home.html').read_text(encoding='utf-8')
 facet_html='<section class="facet primary-facet"><h3>谱学方向 <small id="facet-count-0"></small></h3><div id="facet-0"></div></section><section class="facet primary-facet"><h3>应用领域 <small id="facet-count-3"></small></h3><div id="facet-3"></div></section><details class="advanced-filters"><summary>高级筛选 <small id="advanced-count"></small></summary><label class="joint-option"><input type="checkbox" id="joint-only">仅同时涉及 NMR 与 EPR</label>'
 for i,name in [(2,'方法'),(1,'实验类型'),(5,'信息类型'),(4,'仪器部件')]:
  facet_html+='<details class="facet"><summary>'+name+'<small id="facet-count-'+str(i)+'"></small></summary><div class="facet-options" id="facet-'+str(i)+'"></div></details>'
 facet_html+='</details>'
 for key,value in {'{{TOTAL}}':f'{len(issues)}期 · {sum(len(d["items"]) for d in issues)}条','{{RANGE}}':issues[0]['report_date']+' — '+issues[-1]['report_date'],'{{YEAR}}':str(datetime.date.today().year),'{{FACETS}}':facet_html,'{{ARCHIVE}}':archive_html(issues),'{{LATEST_FEATURE}}':latest_feature(issues[-1])}.items():template=template.replace(key,value)
 (out/'index.html').write_text(template,encoding='utf-8')
 compact_fields=['item_id','item_no','report_date','title_cn','summary_cn','meaning_cn','publication_date','source','url','doi','sample_systems',*FIELDS,'information_type']
 compact={'taxonomy_version':tax['taxonomy_version'],'issues':[{'report_date':d['report_date'],'item_count':len(d['items'])} for d in issues],'items':[{**{k:a[k] for k in compact_fields},'publication_status':a.get('publication_status','unknown')} for d in issues for a in d['items']]}
 (out/'search-index.json').write_text(json.dumps(compact,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
 (out/'.nojekyll').write_text('');(out/'index.json').write_text(json.dumps({'schema_version':'1.4-tag-reviewed','taxonomy_version':tax['taxonomy_version'],'issues':[{'report_date':d['report_date'],'item_count':len(d['items']),'url':d['report_date']+'/','data_url':f'data/{d["report_date"][:4]}/SpinFront_{d["report_date"]}.json'} for d in issues],'items':[a for d in issues for a in d['items']]},ensure_ascii=False),encoding='utf-8');print(f'Built {len(issues)} issues')
if __name__=='__main__':main()
