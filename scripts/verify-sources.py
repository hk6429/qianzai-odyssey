"""Audit shipped work text against pinned, locally cached source records."""
from pathlib import Path
import json,hashlib,re,subprocess
R=Path(__file__).resolve().parents[1]
works=json.loads((R/'data/works.json').read_text());bank=json.loads((R/'data/questions.json').read_text())
manifest={r['file']:r for f in ['manifest.json','curated-manifest.json'] for r in json.loads((R/'sources'/f).read_text())}
cache={};originals={}
for key,w in works.items():
 f=w['sourceFile']
 if f not in cache:
  raw=(R/f).read_bytes()
  assert hashlib.sha256(raw).hexdigest()==manifest[f]['sha256'],f
  try:cache[f]=json.loads(raw)
  except json.JSONDecodeError:cache[f]=[json.loads(line) for line in raw.decode().splitlines() if line.strip()]
 row=cache[f][w['sourceIndex']];content=row['content']
 originals[key]='\n'.join(content) if isinstance(content,list) else content
converted=json.loads(subprocess.run(['opencc','-c','s2tw.json'],input=json.dumps(originals,ensure_ascii=False),text=True,capture_output=True,check=True).stdout)
for key,content in converted.items():
 content=content.replace('\\n','\n').replace('\\u3000',' ').replace('\\r','')
 content=re.sub(r'<[^>]+>','',content)
 content=re.sub(r'\([^)]*\)|（[^）]*）|\[[^]]*\]|【[^】]*】','',content)
 content=re.sub(r'[ \t\u3000]+','',content).replace('“','「').replace('”','」').replace('‘','『').replace('’','』').strip()
 assert works[key]['content']==content,key
canon=lambda s:re.sub(r'[^\u3400-\u9fff]','',s)
for q in bank:assert canon(q['left']+q['answer']) in canon(works[q['workId']]['content']),q['id']
report={'questionsCompared':len(bank),'worksCompared':len(works),'pinnedSourceFilesHashMatched':len(cache),'failures':0,'scope':'Text fidelity and excerpt continuity; not historical attribution or critical-edition review.'}
(R/'docs/source-verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False))
