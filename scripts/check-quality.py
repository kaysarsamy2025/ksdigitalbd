import json,re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit,unquote
pages=json.loads(Path('app/site-content.json').read_text())
class Page(HTMLParser):
 def __init__(self,s):
  super().__init__();self.ids=[];self.links=[];self.images=[];self.labels=[];self.fields=[];self.feed(s)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if a.get('id'):self.ids.append(a['id'])
  if tag=='a':self.links.append(a.get('href',''))
  if tag=='img':self.images.append(a)
  if tag=='label':self.labels.append(a.get('for'))
  if tag in ['input','select','textarea']:self.fields.append(a)
parsed={p:Page(s) for p,s in pages.items()}
titles=[]
for path,doc in pages.items():
 p=parsed[path];assert len(p.ids)==len(set(p.ids)),('duplicate IDs',path)
 title=re.search('<title>(.*?)</title>',doc).group(1);titles.append(title)
 assert 'capability-directory' not in doc,path
 for a in p.images:assert 'alt' in a,(path,a)
 for f in p.fields:assert f.get('aria-label') or f.get('id') in p.labels,(path,f)
 for href in p.links:
  u=urlsplit(href)
  if u.scheme or u.netloc:continue
  dest=unquote(u.path) or path
  if u.fragment and dest in parsed:assert unquote(u.fragment) in parsed[dest].ids,(path,href)
 for schema in re.findall('<script type="application/ld\\+json">(.*?)</script>',doc):json.loads(schema)
 assert '<meta name="description"' in doc and '<link rel="canonical"' in doc,path
assert len(titles)==len(set(titles)),'Duplicate titles'
assert 'noindex,follow' in pages['/404']
assert '/404<' not in Path('public/sitemap.xml').read_text()
print('Quality checks passed: unique titles and IDs, anchor destinations, image alternatives, form labels, structured metadata and noindex 404 across',len(pages),'routes.')
