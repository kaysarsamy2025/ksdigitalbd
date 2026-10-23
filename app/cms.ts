import pages from './site-content.json';
type Config={DB?:D1Database;BUCKET?:R2Bucket};
const basePages=pages as Record<string,string>;
const escape=(s:unknown)=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]!));
const result=(d:unknown,status=200)=>Response.json(d,{status,headers:{'Cache-Control':'no-store'}});
function mapText(source:string,visit:(text:string,index:number,tag:string)=>string){let body=false,skip='',index=0;const stack:string[]=[];return source.replace(/<!--[\s\S]*?-->|<[^>]+>|[^<]+/g,chunk=>{if(chunk.startsWith('<!--'))return chunk;if(chunk.startsWith('<')){const m=/^<\s*(\/?)([a-z0-9]+)/i.exec(chunk);if(!m)return chunk;const tag=m[2].toLowerCase();if(tag==='body')body=!m[1];if(['script','style','svg'].includes(tag))skip=m[1]?'':tag;if(m[1]){const i=stack.lastIndexOf(tag);if(i>=0)stack.splice(i)}else if(!['img','input','meta','link','br','hr','source','wbr'].includes(tag)&&!chunk.endsWith('/>'))stack.push(tag);return chunk}if(!body||skip||!chunk.trim()||chunk.includes('{{CONTACT_DETAILS}}'))return chunk;return visit(chunk,index++,stack[stack.length-1]||'text')})}
const imagePattern=/<img\b[^>]*>/gi;
const decode=(s:string)=>s.replace(/&(#x[0-9a-f]+|#\d+|amp|lt|gt|quot|apos|nbsp);/gi,(_,c)=>c[0]==='#'?String.fromCodePoint(c[1].toLowerCase()==='x'?parseInt(c.slice(2),16):parseInt(c.slice(1))):(({amp:'&',lt:'<',gt:'>',quot:'"',apos:"'",nbsp:' '} as Record<string,string>)[c.toLowerCase()]||_));
function imageAttr(tag:string,key:string){return decode(new RegExp('\\b'+key+'=["\']([^"\']*)["\']','i').exec(tag)?.[1]||'')}
export function fields(path:string){const source=basePages[path];if(!source)return null;return {texts:(()=>{const items:{id:string;tag:string;value:string}[]=[];mapText(source,(text,i,tag)=>{items.push({id:String(i),tag,value:decode(text)});return text});return items})(),images:[...source.matchAll(imagePattern)].map((m,i)=>({id:String(i),src:imageAttr(m[0],'src'),alt:imageAttr(m[0],'alt')}))}}
function safeMedia(v:unknown){const s=String(v||'');return s===''||/^\/(?:media\/|assets\/)[a-zA-Z0-9/_ .-]+$/.test(s)||(/^https:\/\//.test(s)&&(()=>{try{return !new URL(s).username&&!new URL(s).password}catch{return false}})())}
async function readPage(cfg:Config,path:string){const row=await cfg.DB!.prepare('SELECT value FROM site_settings WHERE key=?').bind('cms:page:'+path).first<{value:string}>();return row?JSON.parse(row.value):{texts:{},images:{},gallery:[]}}
export async function cmsApi(request:Request,cfg:Config,owner:boolean):Promise<Response>{try{return await cmsApiImpl(request,cfg,owner)}catch{return result({error:"The change could not be completed. Please try again."},503)}}
async function cmsApiImpl(request:Request,cfg:Config,owner:boolean):Promise<Response>{
 if(!owner)return result({error:'Owner access required.'},403);
 if(!cfg.DB)return result({error:'Database unavailable.'},503);
 const url=new URL(request.url),action=url.pathname.split('/').pop();
 if(request.method==='GET'){
 if(action==='pages')return result({pages:Object.keys(basePages).filter(p=>p!=='/404')});
 if(action==='page'){const path=url.searchParams.get('path')||'/';const f=fields(path);return f?result({...f,overrides:await readPage(cfg,path)}):result({error:'Page not found.'},404)}
 if(action==='entries')return result({entries:(await cfg.DB.prepare('SELECT * FROM cms_entries ORDER BY updated_at DESC').all()).results});
 if(action==='media')return result({media:(await cfg.DB.prepare('SELECT * FROM cms_media ORDER BY created_at DESC').all()).results});
 return result({error:'Not found.'},404);
 }
 if(request.headers.get('origin')!==url.origin)return result({error:'Invalid origin.'},403);
 if(action==='upload'){
 if(!cfg.BUCKET)return result({error:'Media storage unavailable.'},503);
 const limit=25*1024*1024;
 if(Number(request.headers.get('content-length')||0)>limit+10000)return result({error:'Maximum file size is 25 MB.'},413);
 const reader=request.body?.getReader();if(!reader)return result({error:'No file supplied.'},400);const chunks:Uint8Array[]=[];let total=0;
 while(true){const {done,value}=await reader.read();if(done)break;total+=value.length;if(total>limit+10000){await reader.cancel();return result({error:'Maximum file size is 25 MB.'},413)}chunks.push(value)}
 const body=new Uint8Array(total);let offset=0;for(const chunk of chunks){body.set(chunk,offset);offset+=chunk.length}
 const form=await new Response(body,{headers:{'Content-Type':request.headers.get('content-type')||''}}).formData();const file=form.get('file');if(!file||typeof file==='string')return result({error:'Choose an image or video.'},400);
 const bytes=new Uint8Array(await file.arrayBuffer());const head=[...bytes.slice(0,12)];const ascii=new TextDecoder().decode(bytes.slice(0,16));
 const type=head[0]===255&&head[1]===216&&head[2]===255?'image/jpeg':head.slice(0,8).join(',')==='137,80,78,71,13,10,26,10'?'image/png':ascii.startsWith('GIF87a')||ascii.startsWith('GIF89a')?'image/gif':ascii.startsWith('RIFF')&&ascii.slice(8,12)==='WEBP'?'image/webp':ascii.slice(4,8)==='ftyp'&&file.type==='video/mp4'?'video/mp4':head.slice(0,4).join(',')==='26,69,223,163'&&file.type==='video/webm'?'video/webm':'';
 if(!type||!bytes.length||bytes.length>limit)return result({error:'Use JPG, PNG, GIF, WebP, MP4 or WebM, up to 25 MB.'},400);
 const id=crypto.randomUUID()+'.'+({'image/jpeg':'jpg','image/png':'png','image/gif':'gif','image/webp':'webp','video/mp4':'mp4','video/webm':'webm'}[type]);
 await cfg.BUCKET.put(id,bytes,{httpMetadata:{contentType:type}});try{await cfg.DB.prepare('INSERT INTO cms_media (id,name,type,size,created_at) VALUES (?,?,?,?,?)').bind(id,file.name.slice(0,180),type,bytes.length,Date.now()).run()}catch(e){await cfg.BUCKET.delete(id);throw e}return result({url:'/media/'+id},201);
 }
 if(!request.headers.get('content-type')?.startsWith('application/json'))return result({error:'JSON required.'},415);
 const raw=await request.text();if(raw.length>250000)return result({error:'Content too large.'},413);let d;try{d=JSON.parse(raw)}catch{return result({error:'Invalid JSON.'},400)}if(!d||Array.isArray(d)||typeof d!=='object')return result({error:'Invalid data.'},400);
 if(action==='page'){
 const f=fields(d.path);if(!f)return result({error:'Page not found.'},404);
 if(d.reset){await cfg.DB.prepare('DELETE FROM site_settings WHERE key=?').bind('cms:page:'+d.path).run();return result({ok:true})}
 const texts:Record<string,string>={},images:Record<string,{src:string;alt:string}>={};for(const [k,v] of Object.entries(d.texts||{})){if(!f.texts[Number(k)]||typeof v!=='string'||v.length>5000)return result({error:'Invalid text field.'},400);texts[k]=v}
 for(const [k,v] of Object.entries(d.images||{})){const im=v as {src:string;alt:string};if(!f.images[Number(k)]||!im||!safeMedia(im.src)||typeof im.alt!=='string'||im.alt.length>300)return result({error:'Invalid image.'},400);images[k]=im}
 const gallery=Array.isArray(d.gallery)?d.gallery:[];if(gallery.length>30||gallery.some((g:{url:string;type:string;caption:string})=>!g||!g.url||!safeMedia(g.url)||!['image','video'].includes(g.type)||typeof g.caption!=='string'||g.caption.length>300))return result({error:'Invalid page media.'},400);
 await cfg.DB.prepare('INSERT INTO site_settings (key,value) VALUES (?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value').bind('cms:page:'+d.path,JSON.stringify({texts,images,gallery})).run();return result({ok:true});
 }
 if(action==='entry'){
 if(d.delete){await cfg.DB.prepare('DELETE FROM cms_entries WHERE id=?').bind(String(d.id)).run();return result({ok:true})}
 const v:Record<string,string>={};for(const k of ['title','summary','body','price','image','video','slug','kind','status'])v[k]=String(d[k]||'').trim();
 if(!v.title||v.title.length>180||v.summary.length>500||v.body.length>50000||v.price.length>100||!safeMedia(v.image)||!safeMedia(v.video)||!['blog','portfolio','product'].includes(v.kind)||!['draft','published'].includes(v.status)||!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(v.slug)||v.slug.length>100)return result({error:'Check title, slug, media URLs and content lengths.'},400);
 const publicPath=(v.kind==='blog'?'/insights/':v.kind==='portfolio'?'/portfolio/':'/products/')+v.slug;if(basePages[publicPath])return result({error:'That address belongs to an existing page. Edit it under Pages.'},409);
 const id=d.id?String(d.id):crypto.randomUUID();const conflict=await cfg.DB.prepare('SELECT id FROM cms_entries WHERE slug=? AND id<>?').bind(v.slug,id).first();if(conflict)return result({error:'Slug already in use.'},409);
 await cfg.DB.prepare('INSERT INTO cms_entries (id,kind,slug,title,summary,body,price,image,video,status,updated_at) VALUES (?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT(id) DO UPDATE SET kind=excluded.kind,slug=excluded.slug,title=excluded.title,summary=excluded.summary,body=excluded.body,price=excluded.price,image=excluded.image,video=excluded.video,status=excluded.status,updated_at=excluded.updated_at').bind(id,v.kind,v.slug,v.title,v.summary,v.body,v.price,v.image,v.video,v.status,Date.now()).run();return result({ok:true,id});
 }
 if(action==='delete-media'){
 const id=String(d.id||'');if(!/^[0-9a-f-]{36}\.(jpg|png|gif|webp|mp4|webm)$/.test(id))return result({error:'Invalid media.'},400);
 const needle='/media/'+id;const used=await cfg.DB.prepare('SELECT id FROM cms_entries WHERE image=? OR video=? LIMIT 1').bind(needle,needle).first();const pageUsed=await cfg.DB.prepare("SELECT key FROM site_settings WHERE key LIKE 'cms:page:%' AND instr(value,?)>0 LIMIT 1").bind(needle).first();if(used||pageUsed)return result({error:'Remove this file from its pages or entries before deleting it.'},409);
 if(!cfg.BUCKET)return result({error:'Storage unavailable.'},503);await cfg.BUCKET.delete(id);await cfg.DB.prepare('DELETE FROM cms_media WHERE id=?').bind(id).run();return result({ok:true});
 }
 return result({error:'Not found.'},404);
}
export async function mediaResponse(request:Request,cfg:Config){const id=new URL(request.url).pathname.slice(7);if(!/^[0-9a-f-]{36}\.(jpg|png|gif|webp|mp4|webm)$/.test(id)||!cfg.BUCKET)return new Response('Not found',{status:404});const obj=await cfg.BUCKET.get(id,{range:request.headers});if(!obj)return new Response('Not found',{status:404});const h=new Headers({'Cache-Control':'public, max-age=3600','X-Content-Type-Options':'nosniff','Accept-Ranges':'bytes'});obj.writeHttpMetadata(h);h.set('ETag',obj.httpEtag);if(obj.range&&'offset' in obj.range&&'length' in obj.range&&typeof obj.range.offset==='number'&&typeof obj.range.length==='number'){h.set('Content-Range',`bytes ${obj.range.offset}-${obj.range.offset+obj.range.length-1}/${obj.size}`);h.set('Content-Length',String(obj.range.length));return new Response(obj.body,{status:206,headers:h})}return new Response(obj.body,{headers:h})}
function mediaBlock(g:{url:string;type:string;caption:string}){return '<figure style="margin:0">'+(g.type==='video'?'<video controls preload="metadata" style="width:100%;border-radius:16px" src="'+escape(g.url)+'"></video>':'<img loading="lazy" style="width:100%;border-radius:16px" src="'+escape(g.url)+'" alt="'+escape(g.caption)+'">')+(g.caption?'<figcaption>'+escape(g.caption)+'</figcaption>':'')+'</figure>'}
export async function renderCms(path:string,source:string|undefined,cfg:Config){if(!cfg.DB)return source;try{
 let out=source;const entry=await cfg.DB.prepare("SELECT * FROM cms_entries WHERE status='published' AND (CASE kind WHEN 'blog' THEN '/insights/' WHEN 'portfolio' THEN '/portfolio/' ELSE '/products/' END)||slug=?").bind(path).first<Record<string,string>>();
 if(!out&&entry){const template=basePages['/about'];const content='<section class="wrap section"><a class="textlink" href="'+(entry.kind==='blog'?'/insights':entry.kind==='portfolio'?'/portfolio':'/products')+'">← Back</a><h1 style="font-size:clamp(32px,5vw,58px)">'+escape(entry.title)+'</h1><p>'+escape(entry.summary)+'</p>'+(entry.price?'<p class="textlink">'+escape(entry.price)+'</p>':'')+(entry.image?mediaBlock({url:entry.image,type:'image',caption:entry.title}):'')+'<div style="white-space:pre-wrap;margin:28px 0;line-height:1.85">'+escape(entry.body)+'</div>'+(entry.video?mediaBlock({url:entry.video,type:'video',caption:''}):'')+'</section>';out=template.replace(/<main\b[^>]*>[\s\S]*?<\/main>/, '<main>'+content+'</main>').replace(/<title>[\s\S]*?<\/title>/,'<title>'+escape(entry.title)+' | KS Digital BD</title>').replace(/<link rel="canonical"[^>]*>/,'<link rel="canonical" href="https://ks-digital-bd.cleanbell512.chatgpt.site'+path+'">').replace(/<meta (?:name="description"|property="og:[^"]+"|name="twitter:[^"]+")[^>]*>/g,'');}
 if(!out)return undefined;
 const overrides=await readPage(cfg,path);let ii=0;out=mapText(out,(text,index)=>{const replacement=overrides.texts?.[String(index)];return replacement===undefined?text:escape(replacement)});out=out.replace(imagePattern,(full)=>{const im=overrides.images?.[String(ii++)];if(!im)return full;if(!im.src)return '';return full.replace(/\s(?:src|alt)=["'][^"']*["']/gi,'').replace(/\s*\/?>(?=$)/,' src="'+escape(im.src)+'" alt="'+escape(im.alt)+'">')});
 let addition='';if(overrides.gallery?.length)addition+='<section class="wrap section"><div class="grid3">'+overrides.gallery.map(mediaBlock).join('')+'</div></section>';
 const kind=path==='/insights'?'blog':path==='/portfolio'?'portfolio':path==='/products'?'product':null;
 if(kind){const rows=await cfg.DB.prepare("SELECT * FROM cms_entries WHERE status='published' AND kind=? ORDER BY updated_at DESC").bind(kind).all<Record<string,string>>();if(rows.results.length)addition+='<section class="wrap section"><h2>'+(kind==='blog'?'Latest articles':kind==='portfolio'?'More projects':'More products')+'</h2><div class="grid3">'+rows.results.map(e=>'<article class="card" style="padding:24px">'+(e.image?mediaBlock({url:e.image,type:'image',caption:''}):'')+'<h3><a href="'+path+'/'+escape(e.slug)+'">'+escape(e.title)+'</a></h3><p>'+escape(e.summary)+'</p>'+(e.price?'<p class="textlink">'+escape(e.price)+'</p>':'')+'<a class="textlink" href="'+path+'/'+escape(e.slug)+'">View details →</a></article>').join('')+'</div></section>'}
 return out.replace('</main>',addition+'</main>');
 }catch{return source}}
export function cmsPanel(){return '<link rel="stylesheet" href="/cms.css"><div id="cms"><div class="cms-heading"><div><span class="badge">KS DIGITAL BD · CONTENT STUDIO</span><h1>Make it yours.</h1><p>Manage your pages, products, stories and media from one workspace.</p></div><a class="btn outline" href="/" target="_blank">View website ↗</a></div><nav class="cms-tabs" aria-label="Content sections"><button data-tab="pages">Pages &amp; pricing</button><button data-tab="blog">Blog</button><button data-tab="portfolio">Portfolio</button><button data-tab="product">Products</button><button data-tab="media">Media library</button><a href="/admin?view=inbox">Inquiries</a><a href="/admin?view=settings">Business details</a><a href="/signout-with-chatgpt?return_to=%2F" target="_top">Sign out</a></nav><p id="cms-status" role="status" aria-live="polite"></p><div id="cms-workspace">Loading your workspace…</div></div><script src="/cms.js" defer></script>'}
