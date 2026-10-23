import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ICONS={
 'retail':'<path d="M3 9h18l-2-6H5L3 9Z"/><path d="M4 9v12h16V9M9 21v-7h6v7"/><path d="M3 9a3 3 0 0 0 6 0 3 3 0 0 0 6 0 3 3 0 0 0 6 0"/>',
 'pharmacy':'<path d="M9 3h6v6h6v6h-6v6H9v-6H3V9h6V3Z"/>',
 'restaurant':'<path d="M4 3v6a3 3 0 0 0 6 0V3M7 3v18M20 3c-4 0-5 8-5 10h5M20 3v18"/>',
 'e-commerce':'<path d="m3 3 2 2 2 11h12l2-8H6"/><circle cx="9" cy="21" r="1"/><circle cx="18" cy="21" r="1"/>',
 'healthcare':'<path d="M5 3v5a4 4 0 0 0 8 0V3M3 3h4M11 3h4M9 12v3a5 5 0 0 0 10 0v-2"/><circle cx="19" cy="10" r="3"/>',
 'service-businesses':'<rect x="3" y="7" width="18" height="14" rx="2"/><path d="M8 7V3h8v4M3 12a22 22 0 0 0 18 0M10 13h4"/>',
 'web':'<rect x="2" y="4" width="20" height="16" rx="2"/><path d="M2 9h20M6 6.5h.01M9 6.5h.01m0 6-3 2 3 2m6-4 3 2-3 2"/>',
 'mobile':'<rect x="6" y="2" width="12" height="20" rx="3"/><path d="M10 5h4M11 19h2"/>',
 'custom':'<path d="m8 4-6 8 6 8m8-16 6 8-6 8m-3-18-2 20"/>',
 'erp':'<rect x="9" y="2" width="6" height="6" rx="1"/><rect x="2" y="16" width="6" height="6" rx="1"/><rect x="16" y="16" width="6" height="6" rx="1"/><path d="M12 8v4M5 16v-4h14v4"/>',
 'ai':'<path d="m12 2 2.5 7.5L22 12l-7.5 2.5L12 22l-2.5-7.5L2 12l7.5-2.5L12 2Z"/>',
 'marketing':'<path d="m3 15 5-5 4 3 8-9M15 4h5v5M3 21h18"/>',
 'plan':'<path d="M8 4h8M9 2h6v4H9z"/><rect x="4" y="4" width="16" height="18" rx="2"/><path d="m8 12 2 2 5-5M8 18h8"/>',
 'chat':'<path d="M21 11a8 8 0 0 1-8 8H8l-5 3V7a5 5 0 0 1 5-5h5a8 8 0 0 1 8 9Z"/><path d="M7 8h10M7 12h7"/>',
 'shield':'<path d="m12 2 9 4v6c0 6-9 10-9 10S3 18 3 12V6l9-4Z"/><path d="m8 12 3 3 5-6"/>',
 'support':'<path d="M3 13v-2a9 9 0 0 1 18 0v2M3 12H2v7h4v-7H3Zm18 0h1v7h-4v-7h3ZM18 19c0 3-3 3-6 3"/>',
 'search':'<circle cx="10" cy="10" r="7"/><path d="m15 15 7 7"/>',
 'design':'<path d="m15 3 6 6-12 12H3v-6L15 3Z"/><path d="m12 6 6 6"/>',
 'test':'<path d="M9 3h6M10 3v6L4 19a2 2 0 0 0 2 3h12a2 2 0 0 0 2-3L14 9V3M8 15h8"/>',
 'launch':'<path d="M14 3c4-1 7-1 7-1s0 3-1 7l-8 8-5-5 7-9ZM7 12H2l6-6h4m0 11v5l6-6v-4M6 18l-3 3"/><circle cx="16" cy="7" r="1"/>',
}
def icon(name,cls=''):
 return '<svg class="glyph '+cls+'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.65" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+ICONS.get(name,ICONS['custom'])+'</svg>'
def replace_div(s,start,new):
 depth=0
 for m in re.finditer(r'<div\b[^>]*>|</div>',s[start:]):
  depth+=-1 if m.group().startswith('</') else 1
  if depth==0:return s[:start]+new+s[start+m.end():]
 return s
PRODUCTS={'KS Business Manager':'business','KS Pharmacy Manager':'pharmacy','KS Restaurant Manager':'restaurant','KS CRM':'crm'}
def product_art(key,large=False):
 return '<figure class="product-art'+(' large' if large else '')+'"><img src="/assets/products/'+key+'.webp" alt="AI concept illustration of '+key+' management software" width="1200" height="800" loading="lazy" decoding="async"><figcaption>AI concept illustration</figcaption></figure>'
def service_art(key):
 if key=='web':inner='<div class="ui-browser"><div class="ui-browserbar"><i></i><i></i><i></i><span>yourbusiness.com</span></div><div class="ui-browserbody"><div><b>Your next<br>digital chapter.</b><em></em><small></small></div><div class="ui-orb">'+icon('web')+'</div></div><div class="ui-tiles"><i></i><i></i><i></i></div></div><div class="responsive-tag">Responsive by design</div>'
 elif key=='mobile':inner='<div class="ui-phone phone-back"><div class="phone-notch"></div><span class="phone-title">Explore</span><div class="phone-photo"></div><div class="phone-lines"></div></div><div class="ui-phone phone-front"><div class="phone-notch"></div><span class="phone-title">Your workspace</span><div class="phone-ministats"><i></i><i></i></div><div class="phone-list"><i></i><i></i><i></i></div><div class="phone-nav">● &nbsp; ◇ &nbsp; ▦</div></div>'
 elif key=='custom':inner='<div class="code-window"><div class="ui-browserbar"><i></i><i></i><i></i><span>Built around your workflow</span></div><div class="code-row"><span>01</span><b>discover</b><i>your goals</i></div><div class="code-row"><span>02</span><b>design</b><i>the solution</i></div><div class="code-row"><span>03</span><b>build</b><i>with purpose</i></div></div><div class="code-badge">'+icon('custom')+'</div>'
 elif key=='erp':inner='<div class="module-map"><div class="module-core">'+icon('erp')+'<b>One workspace</b></div><div class="module-leaves">'+''.join('<span>'+icon(i)+'<b>'+t+'</b></span>' for i,t in [('retail','Sales'),('plan','Stock'),('chat','CRM')])+'</div></div>'
 elif key=='ai':inner='<div class="automation-map"><div class="auto-node">'+icon('chat')+'<span>Input</span></div><div class="auto-line"></div><div class="auto-brain">'+icon('ai')+'</div><div class="auto-line"></div><div class="auto-node">'+icon('shield')+'<span>Review</span></div></div><div class="automation-caption">Less repetition. More focus.</div>'
 else:inner='<div class="growth-panel"><div class="growth-top">Campaign overview '+icon('marketing')+'</div><div class="growth-bars">'+''.join('<i style="height:'+str(x)+'%"></i>' for x in [25,38,32,57,49,72,88])+'</div><div class="growth-bottom"><span>Reach</span><span>Engagement</span><span>Leads</span></div></div>'
 return '<div class="service-art art-'+key+'" role="img" aria-label="'+{'web':'Illustrative responsive website interface','mobile':'Illustrative mobile application interfaces','custom':'Custom development workflow illustration','erp':'Connected business modules illustration','ai':'Automation with human review illustration','marketing':'Illustrative campaign reporting interface'}[key]+'">'+inner+'</div>'
SERVICES={'Website Development':'web','Mobile App Development':'mobile','Custom Software':'custom','ERP, CRM and POS':'erp','AI Automation':'ai','Digital Marketing':'marketing'}

def workflow():
 labels=[('search','Discovery','Understand your goals.'),('plan','Planning','Agree scope and priorities.'),('design','Design','Shape the experience.'),('custom','Development','Build the agreed solution.'),('test','Testing','Review and refine together.'),('launch','Launch & Support','Handover and next steps.')]
 return '<div class="workflow" aria-label="Six-stage project workflow">'+''.join('<div class="workflow-step"><div class="workflow-rail"><span class="workflow-node">'+icon(key)+'</span><span class="workflow-count">0'+str(i+1)+'</span></div><h3>'+title+'</h3><p>'+desc+'</p></div>' for i,(key,title,desc) in enumerate(labels))+'</div><div class="feedback-loop">'+icon('chat')+'<span>Your feedback connects every stage.</span><a href="/contact">Start a conversation ↗</a></div>'
def why_graphic():
 return '<div class="why-map"><div class="why-heading"><span class="why-mark">'+icon('shield')+'</span><div><span class="eyebrow">One connected approach</span><h3>Clarity from first conversation to launch.</h3></div></div><div class="why-points">'+''.join('<article><span class="why-icon">'+icon(key)+'</span><h3>'+title+'</h3><p>'+desc+'</p></article>' for key,title,desc in [('plan','Structured process','Defined scope, milestones and updates.'),('chat','Clear communication','A shared understanding at every step.'),('shield','Quality assurance','Review and testing before release.'),('support','Ongoing support','A handover and support plan on agreed terms.')])+'</div><div class="why-bottom"><span>Discover</span><i></i><span>Design</span><i></i><span>Build</span><i></i><span>Support</span></div></div>'

def decorate(path,body):
 def product(m):
  s=m.group();name=re.search(r'<h3>(.*?)</h3>',s).group(1);key=PRODUCTS.get(name)
  if key:
   pos=s.find('<div class="dashboard');s=replace_div(s,pos,product_art(key)) if pos>=0 else s
  return s
 body=re.sub(r'<article class="product">.*?</article>',product,body,flags=re.S)
 def service(m):
  s=m.group();name=re.search(r'<h3>(.*?)</h3>',s).group(1);key=SERVICES.get(name)
  if key:s=re.sub(r'<div class="icon">.*?</div>',service_art(key)+'<div class="service-title"><span class="service-icon">'+icon(key)+'</span>',s,count=1,flags=re.S).replace('</h3>','</h3></div>',1)
  return s
 body=re.sub(r'<article class="service">.*?</article>',service,body,flags=re.S)
 def project(m):
  s=m.group();name=re.search(r'<h3>(.*?)</h3>',s).group(1);key={'FastSheba':'fastsheba','RT Destination':'rt-destination','IMAS':'imas'}.get(name)
  if key:s=re.sub(r'<div class="project-art">.*?</div>','<a class="project-preview" href="/portfolio/'+key+'" aria-label="Explore '+name+' concept preview"><img src="/assets/projects/'+key+'.svg" alt="Illustrative '+name+' interface concept, not a live project screenshot" width="900" height="560" loading="lazy"><span>Concept UI preview</span></a>',s,count=1,flags=re.S)
  return s
 body=re.sub(r'<article class="project">.*?</article>',project,body,flags=re.S)
 body=re.sub(r'<a class="industry"\s+href="([^"]+)">([^<]+)</a>',lambda m:'<a class="industry" href="'+m[1]+'"><span class="industry-icon">'+icon(m[1].split('/')[-1])+'</span><b>'+m[2]+'</b><span class="industry-arrow">↗</span></a>',body)
 body=re.sub(r'<div class="reasons">.*?</div></div></div></section>',lambda m:why_graphic()+'</div></section>',body,flags=re.S) if False else body
 pos=body.find('<div class="reasons">')
 if pos>=0:body=replace_div(body,pos,why_graphic())
 pos=body.find('<div class="steps">')
 if pos>=0:body=replace_div(body,pos,workflow())
 if path.startswith('/products/'):
  key={'business-manager':'business','pharmacy-manager':'pharmacy','restaurant-manager':'restaurant','crm':'crm'}.get(path.split('/')[-1]);
  if key:body=body.replace('<div class="rich">','<div class="rich">'+product_art(key,True),1)
 if path.startswith('/services/'):
  key={'website-development':'web','mobile-apps':'mobile','custom-software':'custom','erp-crm-pos':'erp','ai-automation':'ai','digital-marketing':'marketing'}.get(path.split('/')[-1]);
  if key:body=body.replace('<div class="rich">','<div class="rich"><div class="service-detail-art">'+service_art(key)+'</div>',1)
 if path.startswith('/portfolio/'):
  key=path.split('/')[-1]
  if key in ['fastsheba','rt-destination','imas']:body=body.replace('<div class="rich">','<div class="rich"><figure class="portfolio-detail-preview"><img src="/assets/projects/'+key+'.svg" alt="'+key+' illustrative UI concept" width="900" height="560"><figcaption>Illustrative UI concept · Not a live project screenshot</figcaption></figure>',1)
 if path.startswith('/industries/'):
  key=path.split('/')[-1];body=body.replace('<div class="rich">','<div class="rich"><div class="industry-detail-art"><span>'+icon(key)+'</span><div><small>BUILT AROUND YOUR OPERATIONS</small><strong>People. Processes. Possibilities.</strong></div></div>',1)
 if path=='/contact':body=body.replace('<div class="eyebrow">KS Digital BD</div>','<div class="contact-map" role="img" aria-label="Office in Rajshahi, Bangladesh">'+icon('service-businesses')+'<div class="map-dot"></div><b>Rajshahi</b><span>Bangladesh</span></div><div class="eyebrow">KS Digital BD</div>',1)
 return body
