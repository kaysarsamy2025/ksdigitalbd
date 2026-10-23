from pathlib import Path
from html.parser import HTMLParser
import json
pages=json.loads(Path('app/site-content.json').read_text())
class Check(HTMLParser):
 def __init__(self):super().__init__();self.h1=0;self.links=[];self.images=[];self.title=False;self.meta=False
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='h1':self.h1+=1
  if tag=='title':self.title=True
  if tag=='meta' and a.get('name')=='description':self.meta=True
  if tag=='a':self.links.append(a.get('href',''))
  if tag=='img':self.images.append(a.get('src',''))
for path,doc in pages.items():
 c=Check();c.feed(doc);assert c.h1==1 and c.title and c.meta,path
 for link in c.links:
  href=link.split('?')[0].split('#')[0]
  assert not href.startswith('/') or href in pages or href=='/admin',(path,href)
 for src in c.images:assert (Path('public')/src.lstrip('/')).exists(),(path,src)
print('Page structure, metadata, assets and internal links passed across',len(pages),'routes.')
