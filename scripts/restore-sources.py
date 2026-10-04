"""Restore pinned originals using committed SHA-256 manifests; no API key needed."""
from pathlib import Path
import json,urllib.request,hashlib,concurrent.futures
R=Path(__file__).resolve().parents[1]
rows={q['file']:q for f in ['manifest.json','curated-manifest.json'] for q in json.loads((R/'sources'/f).read_text())}
def restore(q):
 p=R/q['file'];p.parent.mkdir(parents=True,exist_ok=True)
 if not p.exists():p.write_bytes(urllib.request.urlopen(q['url'],timeout=90).read())
 assert hashlib.sha256(p.read_bytes()).hexdigest()==q['sha256'],q['file']
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:list(pool.map(restore,rows.values()))
print('Verified source files:',len(rows))
