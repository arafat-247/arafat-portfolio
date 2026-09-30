const portfolioFonts=document.getElementById('portfolio-fonts');
if(portfolioFonts)portfolioFonts.media='all';
(()=>{'use strict';
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)],root=document.body.dataset.root||'';
if(document.body.classList.contains('home')&&!location.hash){history.scrollRestoration='manual';window.scrollTo(0,0)}

const menu=$('#mobile-menu'),toggle=$('.menutoggle'),backdrop=$('.menubackdrop'),drawerClose=$('.drawerclose'),themeToggle=$('.themetoggle');
let closeTimer,lastFocused;
function openMenu(){
 if(!menu)return;
 clearTimeout(closeTimer);lastFocused=document.activeElement;menu.hidden=false;backdrop.hidden=false;
 void menu.offsetWidth;menu.classList.add('is-open');backdrop.classList.add('is-open');
 toggle?.setAttribute('aria-expanded','true');document.body.classList.add('menu-open');drawerClose?.focus();
}
function closeMenu(refocus=false){
 if(!menu||menu.hidden)return;
 menu.classList.remove('is-open');backdrop.classList.remove('is-open');toggle?.setAttribute('aria-expanded','false');document.body.classList.remove('menu-open');
 closeTimer=setTimeout(()=>{menu.hidden=true;backdrop.hidden=true},260);
 if(refocus&&(lastFocused||toggle))setTimeout(()=>{(lastFocused||toggle)?.focus()},0);
}
toggle?.addEventListener('click',()=>toggle.getAttribute('aria-expanded')==='true'?closeMenu(true):openMenu());
drawerClose?.addEventListener('click',()=>closeMenu(true));
backdrop?.addEventListener('click',()=>closeMenu(true));
menu?.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>closeMenu()));
document.addEventListener('keydown',event=>{
 if(event.key==='Escape')closeMenu(true);
 if(event.key!=='Tab'||!menu?.classList.contains('is-open'))return;
 const focusable=[...menu.querySelectorAll('a[href],button:not([disabled])')],first=focusable[0],last=focusable.at(-1);
 if(event.shiftKey&&document.activeElement===first){event.preventDefault();last.focus()}
 if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first.focus()}
});

$$('.identity nav a,.drawernav a,.desktopnav a').forEach(a=>{
 if(a.dataset.nav===document.body.dataset.section)a.setAttribute('aria-current','page');
});

function updateTheme(){
 if(!themeToggle)return;
 const dark=document.documentElement.dataset.theme==='dark';
 themeToggle.setAttribute('aria-pressed',String(dark));themeToggle.setAttribute('aria-label',`Switch to ${dark?'light':'dark'} mode`);
 $('.themelabel').textContent=dark?'Light':'Dark';
 $('meta[name="theme-color"]').content=dark?'#101715':'#102d2a';
}
themeToggle?.addEventListener('click',()=>{
 const next=document.documentElement.dataset.theme==='dark'?'light':'dark';
 document.documentElement.dataset.theme=next;localStorage.setItem('portfolio-theme',next);updateTheme();
});
updateTheme();

function observeReveals(scope=document){
 const items=[...scope.querySelectorAll('.homeprofile,.homeintro,.tile,.homecontact,.workitem,.aboutlead,.aboutfacts>*,.coverage,.profiledetails>div,.membership,.recognition li,.contactgrid>*,.photogrid figure')];
 items.forEach(item=>item.classList.add('in'));
}
observeReveals();

if(document.body.classList.contains('home')&&!matchMedia('(prefers-reduced-motion: reduce)').matches){
 document.body.classList.add('home-motion');
 const revealTargets=$$('.homeprofile,.homeintro,.home .tile,.homecontact');
 if('IntersectionObserver' in window){
  const revealObserver=new IntersectionObserver(entries=>entries.forEach(entry=>{
   if(!entry.isIntersecting)return;
   entry.target.classList.add('is-visible');
   revealObserver.unobserve(entry.target);
  }),{threshold:.12,rootMargin:'0px 0px -4% 0px'});
  revealTargets.forEach((item,index)=>{item.style.transitionDelay=Math.min(index*.045,.18)+'s';revealObserver.observe(item)});
 }else revealTargets.forEach(item=>item.classList.add('is-visible'));
}

if(document.body.classList.contains('home')&&!matchMedia('(prefers-reduced-motion: reduce)').matches){
 const portalPanels=$$('.portalpanel');
 if(portalPanels.length){
  portalPanels.forEach((item,index)=>{
   item.classList.add('portal-reveal');
   item.style.setProperty('--portal-delay',Math.min(index*.055,.18)+'s');
  });
  if('IntersectionObserver' in window){
   const portalObserver=new IntersectionObserver(entries=>entries.forEach(entry=>{
    if(!entry.isIntersecting)return;
    entry.target.classList.add('is-visible');
    portalObserver.unobserve(entry.target);
   }),{threshold:.14,rootMargin:'0px 0px -6% 0px'});
   portalPanels.forEach(item=>portalObserver.observe(item));
  }else portalPanels.forEach(item=>item.classList.add('is-visible'));
 }
}

const desktopHead=$('.desktophead'),hero=$('.homeprofile'),desktopMenuToggle=$('.desktopmenutoggle'),desktopNav=$('.desktopnav');
function closeDesktopNav(){
 if(!desktopHead)return;
 desktopHead.classList.remove('nav-open');
 desktopMenuToggle?.setAttribute('aria-expanded','false');
}
desktopMenuToggle?.addEventListener('click',()=>{
 if(!desktopHead)return;
 const open=desktopHead.classList.toggle('nav-open');
 desktopMenuToggle.setAttribute('aria-expanded',String(open));
});
desktopNav?.querySelectorAll('a').forEach(a=>a.addEventListener('click',closeDesktopNav));
document.addEventListener('click',event=>{
 if(!desktopHead?.classList.contains('nav-open'))return;
 if(!desktopHead.contains(event.target))closeDesktopNav();
});
document.addEventListener('keydown',event=>{if(event.key==='Escape')closeDesktopNav()});
function updateShellMotion(){
 const y=window.scrollY;
 $('.mobilehead')?.classList.toggle('scrolled',y>24);
 const compact=y>90;
 desktopHead?.classList.toggle('scrolled',compact);
 if(!compact)closeDesktopNav();
 if(hero&&innerWidth>800)hero.style.setProperty('--hero-shift',Math.min(12,y*.035).toFixed(1)+'px');
 if(desktopHead&&document.body.classList.contains('home')){
  const max=Math.max(1,document.documentElement.scrollHeight-innerHeight);
  desktopHead.style.setProperty('--page-progress',Math.min(100,y/max*100).toFixed(2)+'%');
 }
}
updateShellMotion();
window.addEventListener('scroll',updateShellMotion,{passive:true});

if(matchMedia('(pointer:fine)').matches){
 if(hero){
  hero.addEventListener('pointermove',event=>{
   const box=hero.getBoundingClientRect();
   const x=(event.clientX-box.left)/box.width-.5;
   const y=(event.clientY-box.top)/box.height-.5;
   hero.style.setProperty('--hero-x',(x*8).toFixed(2)+'px');
   hero.style.setProperty('--hero-y',(y*5).toFixed(2)+'px');
   hero.style.setProperty('--hero-hx',((x+.5)*100).toFixed(1)+'%');
   hero.style.setProperty('--hero-hy',((y+.5)*100).toFixed(1)+'%');
  });
  hero.addEventListener('pointerleave',()=>{
   ['--hero-x','--hero-y','--hero-hx','--hero-hy'].forEach(name=>hero.style.removeProperty(name));
  });
 }
 $$('.home .tile').forEach(tile=>{
  tile.addEventListener('pointermove',event=>{
   const box=tile.getBoundingClientRect();
   const x=(event.clientX-box.left)/box.width;
   const y=(event.clientY-box.top)/box.height;
   tile.style.setProperty('--mx',(x*100).toFixed(1)+'%');
   tile.style.setProperty('--my',(y*100).toFixed(1)+'%');
   tile.style.setProperty('--ix',((x-.5)*7).toFixed(2)+'px');
   tile.style.setProperty('--iy',((y-.5)*5).toFixed(2)+'px');
  });
  tile.addEventListener('pointerleave',()=>{
   ['--mx','--my','--ix','--iy'].forEach(name=>tile.style.removeProperty(name));
  });
 });
}

const html=v=>String(v||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function formatDate(v){if(!v)return'Date not recorded';const d=new Date(v);return Number.isNaN(+d)?'Date not recorded':d.toLocaleDateString('en-GB',{day:'numeric',month:'long',year:'numeric',timeZone:'Asia/Dhaka'})}
const archive=$('[data-archive]');
if(archive){const filterToggle=$('.filtertoggle');filterToggle?.addEventListener('click',()=>{const open=archive.classList.toggle('filters-open');filterToggle.setAttribute('aria-expanded',String(open))});(async()=>{try{
 const r=await fetch(root+'data/index.json');if(!r.ok)throw Error('Archive could not be loaded. Please reload.');
 const all=(await r.json()).articles.filter(a=>a.stream===archive.dataset.archive),q=$('[name=q]'),cat=$('[name=category]'),year=$('[name=year]'),creditViews=$$('[data-credit-view]');let page=1,selectedCredit='';
 $('.archive-total strong')?.replaceChildren(document.createTextNode(String(all.length)));
 $$('[data-total]').forEach(total=>{total.textContent=all.filter(a=>a.credit_type===total.dataset.total).length});
 [...new Set(all.map(a=>a.category).filter(Boolean))].sort().forEach(v=>cat.add(new Option(v,v)));[...new Set(all.map(a=>a.date_published?.slice(0,4)).filter(Boolean))].sort().reverse().forEach(v=>year.add(new Option(v,v)));
 const params=new URLSearchParams(location.search);q.value=params.get('q')||'';cat.value=params.get('category')||'';year.value=params.get('year')||'';if(creditViews.length)selectedCredit=params.get('credit')==='contribution'?'contribution':'byline';
 function draw(){const term=q.value.trim().toLocaleLowerCase();const found=all.filter(a=>(!cat.value||a.category===cat.value)&&(!year.value||a.date_published.startsWith(year.value))&&(!selectedCredit||a.credit_type===selectedCredit)&&[a.title,a.excerpt,a.category,a.source_name].join(' ').toLocaleLowerCase().includes(term));const pages=Math.max(1,Math.ceil(found.length/12));page=Math.min(page,pages);$('.count').textContent=found.length+' '+(found.length===1?'entry':'entries');
 $('.work-list').innerHTML=found.slice((page-1)*12,page*12).map(a=>{const url=/^(stories|thoughts)\/[a-zA-Z0-9_-]+\/$/.test(a.local_url)?root+a.local_url:root+'reporting/';const badge=a.credit_type==='contribution'?'<span class="creditbadge">Non-byline contribution</span>':'';return `<article class="workitem" data-credit="${html(a.credit_type)}"><div class="workmeta"><span>${html(formatDate(a.date_published))}</span><span>${html(a.category||'Reporting')}</span><span>${html(a.source_name||'Arafat Rahaman')}</span>${badge}</div><div class="workcopy"><h2><a href="${html(url)}">${html(a.title)}</a></h2><p>${html(a.excerpt)}</p></div><a class="read" href="${html(url)}" aria-label="Read ${html(a.title)}"><span>Read</span> →</a></article>`}).join('')||'<p class="empty">No matches. Try another search or category.</p>';
 $('.pagination [data-page]').textContent=`Page ${page} of ${pages}`;$('[data-prev]').disabled=page<=1;$('[data-next]').disabled=page>=pages;creditViews.forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.creditView===selectedCredit)));const state=new URLSearchParams();if(q.value)state.set('q',q.value);if(cat.value)state.set('category',cat.value);if(year.value)state.set('year',year.value);if(selectedCredit==='contribution')state.set('credit',selectedCredit);history.replaceState(null,'',location.pathname+(state.size?'?'+state:''));observeReveals($('.work-list'));
 }
 $('.tools').onsubmit=e=>{e.preventDefault();page=1;draw()};q.oninput=()=>{page=1;draw()};cat.onchange=year.onchange=()=>{page=1;draw()};creditViews.forEach(button=>button.onclick=()=>{selectedCredit=button.dataset.creditView;page=1;draw()});$('[data-prev]').onclick=()=>{page--;draw();archive.scrollIntoView({behavior:'smooth'})};$('[data-next]').onclick=()=>{page++;draw();archive.scrollIntoView({behavior:'smooth'})};draw();
 }catch(e){$('.count').textContent=e.message;$('[data-next]').disabled=true}})()}


const allWork=$('[data-all-work]');
if(allWork){const form=$('#all-work-tools'),box=$('[data-all-results]'),count=$('[data-all-count]'),more=$('[data-all-more]');let rows=[],shown=24;
 const escText=v=>String(v||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const localUrl=a=>/^(stories|thoughts)\/[a-zA-Z0-9_-]+\/$/.test(a.local_url)?root+a.local_url:root+'all-work/';
 const card=a=>{const img=a.cover_image?'<figure><img src="'+root+escText(a.cover_image)+'" alt="" loading="lazy" decoding="async"></figure>':'<figure></figure>';const badge=a.credit_type==='contribution'?'Non-byline':a.stream==='opinion'?'Opinion':a.stream==='thoughts'?'Thoughts':'Reporting';return '<article class="featurecard">'+img+'<div><div class="featuremeta"><span>'+escText((a.date_published||'').slice(0,10))+'</span><b>'+escText(badge)+'</b><span>'+escText(a.beat_title||'Other')+'</span></div><h2><a href="'+escText(localUrl(a))+'">'+escText(a.title)+'</a></h2><p>'+escText(a.excerpt)+'</p></div></article>'};
 const filtered=()=>{const data=new FormData(form),q=String(data.get('q')||'').trim().toLowerCase(),stream=data.get('stream'),beat=data.get('beat'),year=data.get('year'),credit=data.get('credit');return rows.filter(a=>(!stream||a.stream===stream)&&(!beat||a.beat===beat)&&(!year||String(a.date_published||'').startsWith(year))&&(!credit||a.credit_type===credit)&&(!q||[a.title,a.excerpt,a.category,a.beat_title,(a.series||[]).join(' ')].join(' ').toLowerCase().includes(q)))};
 const draw=reset=>{if(reset)shown=24;const found=filtered();box.innerHTML=found.slice(0,shown).map(card).join('')||'<p class="empty">No matches. Try another search or filter.</p>';count.textContent=found.length+' '+(found.length===1?'result':'results');more.hidden=shown>=found.length};
 form?.addEventListener('input',()=>draw(true));form?.addEventListener('change',()=>draw(true));$('[data-all-reset]')?.addEventListener('click',()=>{form.reset();draw(true)});more?.addEventListener('click',()=>{shown+=24;draw(false)});
 fetch(root+'data/portfolio-features.json').then(r=>{if(!r.ok)throw Error('Archive data unavailable');return r.json()}).then(data=>{rows=data.articles||[];const years=[...new Set(rows.map(a=>String(a.date_published||'').slice(0,4)).filter(Boolean))].sort().reverse();years.forEach(v=>form.elements.year.add(new Option(v,v)));draw(true)}).catch(()=>{if(more)more.hidden=true});
}

const epaperButton=$('[data-epaper-view]'),epaperDialog=$('#epaper-dialog'),epaperSheet=$('.epaper-sheet'),epaperStage=$('.epaper-stage'),epaperStatus=$('[data-epaper-status]');
let epaperScale=1,epaperNatural={width:920,height:1260};
function setEpaperStatus(message){if(epaperStatus)epaperStatus.textContent=message||''}
function measureEpaper(){
 if(!epaperSheet)return epaperNatural;
 const previous=epaperSheet.style.getPropertyValue('--epaper-scale');
 epaperSheet.style.setProperty('--epaper-scale','1');
 epaperNatural={width:epaperSheet.offsetWidth||920,height:epaperSheet.scrollHeight||1260};
 if(previous)epaperSheet.style.setProperty('--epaper-scale',previous);else epaperSheet.style.removeProperty('--epaper-scale');
 return epaperNatural;
}
function setEpaperScale(value){
 if(!epaperSheet)return;
 const natural=measureEpaper();
 epaperScale=Math.max(.25,Math.min(1.5,value));
 epaperSheet.style.setProperty('--epaper-scale',epaperScale.toFixed(3));
 if(epaperStage){
  epaperStage.style.width=Math.ceil(natural.width*epaperScale)+'px';
  epaperStage.style.height=Math.ceil(natural.height*epaperScale)+'px';
 }
}
function fitEpaper(){
 if(!epaperDialog||!epaperSheet)return;
 const viewport=epaperDialog.querySelector('.epaper-viewport');
 const natural=measureEpaper();
 const compact=window.matchMedia('(max-width:800px)').matches;
 const availableWidth=Math.max(240,viewport.clientWidth-(compact?8:28));
 const availableHeight=Math.max(320,viewport.clientHeight-(compact?8:28));
 const scale=Math.min(1,availableWidth/natural.width,availableHeight/natural.height);
 setEpaperScale(scale);
 if(epaperStage){
  epaperStage.style.marginLeft='auto';
  epaperStage.style.marginRight='auto';
 }
 viewport.scrollTo({top:0,left:0});
 setEpaperStatus('Fit to screen');
}
function loadExternalScript(src,test){
 if(test())return Promise.resolve();
 return new Promise((resolve,reject)=>{
  const existing=document.querySelector(`script[src="${src}"]`);
  if(existing){
   existing.addEventListener('load',resolve,{once:true});
   existing.addEventListener('error',reject,{once:true});
   return;
  }
  const script=document.createElement('script');
  script.src=src;script.async=true;script.crossOrigin='anonymous';
  script.onload=resolve;script.onerror=()=>reject(new Error('Could not load export library'));
  document.head.appendChild(script);
 });
}
async function ensureEpaperExportLibraries(){
 await loadExternalScript('https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js',()=>typeof window.html2canvas==='function');
 await loadExternalScript('https://cdn.jsdelivr.net/npm/jspdf@2.5.1/dist/jspdf.umd.min.js',()=>!!window.jspdf?.jsPDF);
}
function epaperFilename(extension){
 const title=$('.reading h1')?.textContent.trim()||'article';
 const slug=title.toLowerCase().normalize('NFKD').replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'').slice(0,80)||'article';
 return `${slug}-epaper.${extension}`;
}
async function renderEpaperCanvas(){
 if(!epaperSheet)throw new Error('E-paper sheet is unavailable');
 await ensureEpaperExportLibraries();
 setEpaperStatus('Preparing HD export…');
 const oldScale=epaperScale;
 const oldTransition=epaperSheet.style.transition;
 epaperSheet.style.transition='none';
 setEpaperScale(1);
 await new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)));
 try{
  return await window.html2canvas(epaperSheet,{
   scale:3,
   useCORS:true,
   backgroundColor:'#f4f0e7',
   logging:false,
   imageTimeout:15000,
   width:epaperSheet.scrollWidth,
   height:epaperSheet.scrollHeight,
   windowWidth:epaperSheet.scrollWidth,
   windowHeight:epaperSheet.scrollHeight
  });
 }finally{
  epaperSheet.style.transition=oldTransition;
  setEpaperScale(oldScale);
 }
}
async function downloadEpaperImage(){
 const button=$('[data-download-epaper-image]');
 try{
  if(button)button.disabled=true;
  const canvas=await renderEpaperCanvas();
  const blob=await new Promise((resolve,reject)=>canvas.toBlob(value=>value?resolve(value):reject(new Error('Image export failed')),'image/png'));
  const filename=epaperFilename('png');
  const url=URL.createObjectURL(blob),link=document.createElement('a');
  link.href=url;
  link.download=filename;
  link.rel='noopener';
  link.style.display='none';
  document.body.appendChild(link);
  link.click();
  link.remove();
  setTimeout(()=>URL.revokeObjectURL(url),5000);
  setEpaperStatus(`PNG downloaded · ${canvas.width} × ${canvas.height}px`);
 }catch(error){
  console.error(error);setEpaperStatus('Image download failed. Please try again.');
 }finally{if(button)button.disabled=false}
}
async function downloadEpaperPdf(){
 const button=$('[data-download-epaper-pdf]');
 try{
  if(button)button.disabled=true;
  const canvas=await renderEpaperCanvas();
  const {jsPDF}=window.jspdf;
  const widthPt=canvas.width*.24,heightPt=canvas.height*.24;
  const pdf=new jsPDF({orientation:widthPt>heightPt?'landscape':'portrait',unit:'pt',format:[widthPt,heightPt],compress:true});
  pdf.addImage(canvas.toDataURL('image/png'),'PNG',0,0,widthPt,heightPt,undefined,'FAST');
  pdf.save(epaperFilename('pdf'));
  setEpaperStatus('HD PDF saved');
 }catch(error){
  console.error(error);setEpaperStatus('PDF download failed. Please try again.');
 }finally{if(button)button.disabled=false}
}
epaperButton?.addEventListener('click',()=>{
 if(!epaperDialog)return;
 epaperDialog.showModal();
 setEpaperStatus('');
 requestAnimationFrame(()=>requestAnimationFrame(fitEpaper));
});
$('[data-close-epaper]')?.addEventListener('click',()=>epaperDialog?.close());
$('[data-epaper-zoom-in]')?.addEventListener('click',()=>{setEpaperScale(epaperScale+.1);setEpaperStatus(Math.round(epaperScale*100)+'%')});
$('[data-epaper-zoom-out]')?.addEventListener('click',()=>{setEpaperScale(epaperScale-.1);setEpaperStatus(Math.round(epaperScale*100)+'%')});
$('[data-epaper-fit]')?.addEventListener('click',fitEpaper);
$('[data-download-epaper-image]')?.addEventListener('click',downloadEpaperImage);
$('[data-download-epaper-pdf]')?.addEventListener('click',downloadEpaperPdf);
epaperDialog?.addEventListener('click',event=>{if(event.target===epaperDialog)epaperDialog.close()});
epaperDialog?.addEventListener('close',()=>{setEpaperScale(1);setEpaperStatus('')});
window.addEventListener('resize',()=>{if(epaperDialog?.open)fitEpaper()},{passive:true});

$('[data-print]')?.addEventListener('click',()=>window.print());
const shareButton=$('[data-share]'),shareDialog=$('#share-dialog'),shareStatus=$('[data-share-status]');
function shareDetails(){
 const url=new URL($('link[rel="canonical"]')?.href||location.href);url.search='';url.hash='';
 return{title:$('.reading h1')?.textContent.trim()||document.title,url:url.href};
}
function setShareLinks(){
 if(!shareDialog)return;
 const{title,url}=shareDetails(),encodedUrl=encodeURIComponent(url),encodedTitle=encodeURIComponent(title);
 const destinations={
  facebook:`https://www.facebook.com/sharer/sharer.php?u=${encodedUrl}`,
  whatsapp:`https://api.whatsapp.com/send?text=${encodeURIComponent(title+' '+url)}`,
  x:`https://twitter.com/intent/tweet?text=${encodedTitle}&url=${encodedUrl}`,
  linkedin:`https://www.linkedin.com/sharing/share-offsite/?url=${encodedUrl}`
 };
 shareDialog.querySelectorAll('[data-share-service]').forEach(link=>link.href=destinations[link.dataset.shareService]);
}
function openShareDialog(){
 if(!shareDialog)return;
 setShareLinks();shareStatus.textContent='';
 if(typeof shareDialog.showModal==='function')shareDialog.showModal();else shareDialog.setAttribute('open','');
}
shareButton?.addEventListener('click',async()=>{
 const details=shareDetails();
 if(navigator.share&&window.isSecureContext){
  try{await navigator.share(details);return}catch(error){if(error.name==='AbortError')return}
 }
 openShareDialog();
});
$('[data-close-share]')?.addEventListener('click',()=>shareDialog.close());
shareDialog?.addEventListener('click',event=>{
 if(event.target===shareDialog){shareDialog.close();return}
 const link=event.target.closest('[data-share-service]');if(!link)return;
 event.preventDefault();
 const popup=window.open(link.href,'share-story','popup=yes,width=680,height=680');
 if(popup)popup.opener=null;else location.href=link.href;
});
$('[data-copy-share]')?.addEventListener('click',async()=>{
 const{url}=shareDetails();
 try{
  if(navigator.clipboard&&window.isSecureContext)await navigator.clipboard.writeText(url);
  else{const field=document.createElement('textarea');field.value=url;field.setAttribute('readonly','');field.style.position='fixed';field.style.opacity='0';document.body.append(field);field.select();document.execCommand('copy');field.remove()}
  shareStatus.textContent='Link copied.';
 }catch(error){shareStatus.textContent='Could not copy automatically. Select the address in your browser.'}
});
const dialog=$('#photo-dialog'),photoButtons=$$('[data-photo]');
let photoIndex=-1,opener;
const photoGrid=$('.photogrid'),viewButtons=$$('[data-photo-view]');
viewButtons.forEach(button=>button.addEventListener('click',()=>{
 const view=button.dataset.photoView;photoGrid.dataset.view=view;
 viewButtons.forEach(item=>item.setAttribute('aria-pressed',String(item===button)));
 try{localStorage.setItem('photo-view',view)}catch(error){}
}));
try{const saved=localStorage.getItem('photo-view');if(saved&&viewButtons.some(button=>button.dataset.photoView===saved))viewButtons.find(button=>button.dataset.photoView===saved).click()}catch(error){}
function showPhoto(index){
 if(!dialog||!photoButtons.length)return;
 photoIndex=(index+photoButtons.length)%photoButtons.length;
 const button=photoButtons[photoIndex],photo=dialog.querySelector('img');
 photo.src=root+button.dataset.photo;photo.alt=button.querySelector('img')?.alt||'';
 $('[data-dialog-caption]').textContent=button.dataset.caption||photo.alt;
 $('[data-dialog-location]').textContent=button.dataset.location||'';
 $('[data-dialog-position]').textContent=`${String(photoIndex+1).padStart(2,'0')} / ${String(photoButtons.length).padStart(2,'0')}`;
 if(!dialog.open)dialog.showModal();
}
photoButtons.forEach((button,index)=>button.addEventListener('click',()=>{opener=button;showPhoto(index)}));
$('[data-prev-photo]')?.addEventListener('click',()=>showPhoto(photoIndex-1));
$('[data-next-photo]')?.addEventListener('click',()=>showPhoto(photoIndex+1));
$('[data-close-photo]')?.addEventListener('click',()=>dialog.close());
dialog?.addEventListener('click',event=>{if(event.target===dialog)dialog.close()});
document.addEventListener('keydown',event=>{
 if(!dialog?.open)return;
 if(event.key==='ArrowLeft')showPhoto(photoIndex-1);
 if(event.key==='ArrowRight')showPhoto(photoIndex+1);
});
dialog?.addEventListener('close',()=>{dialog.querySelector('img').removeAttribute('src');opener?.focus()});
})();
