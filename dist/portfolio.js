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

$$('.identity nav a,.drawernav a').forEach(a=>{
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

window.addEventListener('scroll',()=>{
 $('.mobilehead')?.classList.toggle('scrolled',window.scrollY>24);
},{passive:true});

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
