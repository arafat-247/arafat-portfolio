(()=>{'use strict';
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)],root=document.body.dataset.root||'';
if(document.body.classList.contains('home')&&!location.hash){history.scrollRestoration='manual';window.scrollTo(0,0)}

const menu=$('#mobile-menu'),toggle=$('.menutoggle'),backdrop=$('.menubackdrop'),drawerClose=$('.drawerclose'),themeToggle=$('.themetoggle');
let closeTimer,lastFocused,touchStartX=null,touchDistance=0;
function openMenu(){
 if(!menu||document.body.classList.contains('home'))return;
 clearTimeout(closeTimer);lastFocused=document.activeElement;menu.hidden=false;backdrop.hidden=false;
 requestAnimationFrame(()=>{menu.classList.add('is-open');backdrop.classList.add('is-open')});
 toggle.setAttribute('aria-expanded','true');document.body.classList.add('menu-open');drawerClose.focus();
}
function closeMenu(refocus=false){
 if(!menu||menu.hidden)return;
 menu.classList.remove('is-open');backdrop.classList.remove('is-open');toggle?.setAttribute('aria-expanded','false');document.body.classList.remove('menu-open');
 closeTimer=setTimeout(()=>{menu.hidden=true;backdrop.hidden=true},340);
 if(refocus&&(lastFocused||toggle))setTimeout(()=>{(lastFocused||toggle)?.focus()},0);
}
toggle?.addEventListener('click',()=>toggle.getAttribute('aria-expanded')==='true'?closeMenu(true):openMenu());
drawerClose?.addEventListener('click',()=>closeMenu(true));
backdrop?.addEventListener('click',()=>closeMenu(true));
menu?.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>closeMenu()));
menu?.addEventListener('pointermove',event=>{const box=menu.getBoundingClientRect();menu.style.setProperty('--menu-x',`${event.clientX-box.left}px`);menu.style.setProperty('--menu-y',`${event.clientY-box.top}px`)});
menu?.addEventListener('touchstart',event=>{if(event.touches.length!==1)return;touchStartX=event.touches[0].clientX;touchDistance=0},{passive:true});
menu?.addEventListener('touchmove',event=>{if(touchStartX===null)return;touchDistance=Math.max(0,event.touches[0].clientX-touchStartX);menu.style.transform=`translateX(${touchDistance}px)`},{passive:true});
menu?.addEventListener('touchend',()=>{menu.style.transform='';if(touchDistance>72)closeMenu();touchStartX=null;touchDistance=0});
document.addEventListener('keydown',event=>{
 if(event.key==='Escape')closeMenu(true);
 if(event.key!=='Tab'||!menu?.classList.contains('is-open'))return;
 const focusable=[...menu.querySelectorAll('a[href],button:not([disabled])')],first=focusable[0],last=focusable.at(-1);
 if(event.shiftKey&&document.activeElement===first){event.preventDefault();last.focus()}
 if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first.focus()}
});

const page=document.body.dataset.page;
$$('.identity nav a,.drawernav a').forEach(a=>{
 const href=(a.getAttribute('href')||'').split('#')[0].split('/').pop();
 if((page==='index-html'&&href==='index.html')||(page==='about-html'&&href==='about.html')||(page==='contact-html'&&href==='contact.html'))a.setAttribute('aria-current','page');
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

let revealObserver;
function observeReveals(scope=document){
 const items=[...scope.querySelectorAll('.homeprofile,.homeintro,.tile,.homecontact,.workitem,.aboutlead,.aboutfacts>*,.coverage,.profiledetails>div,.membership,.recognition li,.contactgrid>*,.photogrid figure')];
 if(matchMedia('(prefers-reduced-motion:reduce)').matches||!('IntersectionObserver'in window)){items.forEach(x=>x.classList.add('in'));return}
 revealObserver||=(new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('in');revealObserver.unobserve(entry.target)}}),{threshold:.12,rootMargin:'0px 0px -24px'}));
 items.forEach((item,index)=>{if(item.classList.contains('reveal'))return;item.classList.add('reveal');item.style.setProperty('--reveal-delay',`${Math.min(index%4,3)*55}ms`);revealObserver.observe(item)});
}
observeReveals();

window.addEventListener('scroll',()=>{
 $('.mobilehead')?.classList.toggle('scrolled',window.scrollY>24);
 const portrait=$('.homeprofile>img');
 if(portrait&&!matchMedia('(prefers-reduced-motion:reduce)').matches)portrait.style.setProperty('--portrait-shift',`${Math.min(window.scrollY*.035,12)}px`);
},{passive:true});

const html=v=>String(v||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function formatDate(v){if(!v)return'Date not recorded';const d=new Date(v);return Number.isNaN(+d)?'Date not recorded':d.toLocaleDateString('en-GB',{day:'numeric',month:'long',year:'numeric',timeZone:'Asia/Dhaka'})}
const archive=$('[data-archive]');
if(archive){const filterToggle=$('.filtertoggle');filterToggle?.addEventListener('click',()=>{const open=archive.classList.toggle('filters-open');filterToggle.setAttribute('aria-expanded',String(open))});(async()=>{try{
 const r=await fetch(root+'data/index.json');if(!r.ok)throw Error('Archive could not be loaded. Please reload.');
 const all=(await r.json()).articles.filter(a=>a.stream===archive.dataset.archive),q=$('[name=q]'),cat=$('[name=category]'),year=$('[name=year]'),credit=$('[name=credit]');let page=1;
 [...new Set(all.map(a=>a.category).filter(Boolean))].sort().forEach(v=>cat.add(new Option(v,v)));[...new Set(all.map(a=>a.date_published?.slice(0,4)).filter(Boolean))].sort().reverse().forEach(v=>year.add(new Option(v,v)));
 const params=new URLSearchParams(location.search);q.value=params.get('q')||'';cat.value=params.get('category')||'';year.value=params.get('year')||'';if(credit)credit.value=params.get('credit')||'';
 function draw(){const term=q.value.trim().toLocaleLowerCase();const found=all.filter(a=>(!cat.value||a.category===cat.value)&&(!year.value||a.date_published.startsWith(year.value))&&(!credit||!credit.value||a.credit_type===credit.value)&&[a.title,a.excerpt,a.category,a.source_name,a.contribution].join(' ').toLocaleLowerCase().includes(term));const pages=Math.max(1,Math.ceil(found.length/12));page=Math.min(page,pages);$('.count').textContent=found.length+' '+(found.length===1?'entry':'entries');
 $('.work-list').innerHTML=found.slice((page-1)*12,page*12).map(a=>{const url=/^(stories|thoughts)\/[a-zA-Z0-9_-]+\/$/.test(a.local_url)?root+a.local_url:root+'reporting.html',creditLabel=a.credit_type==='contribution'?'Non-byline contribution':'Bylined story';return `<article class="workitem"><div class="workmeta"><span>${html(formatDate(a.date_published))}</span><span>${html(a.category||'Reporting')}</span><span>${html(a.source_name||'Arafat Rahaman')}</span><span class="credit credit-${html(a.credit_type||'author-page')}">${creditLabel}</span></div><div class="workcopy"><h2><a href="${html(url)}">${html(a.title)}</a></h2><p>${html(a.excerpt)}</p></div><a class="read" href="${html(url)}" aria-label="Read ${html(a.title)}"><span>Read</span> →</a></article>`}).join('')||'<p class="empty">No matches. Try another search or filter.</p>';
 $('.pagination [data-page]').textContent=`Page ${page} of ${pages}`;$('[data-prev]').disabled=page<=1;$('[data-next]').disabled=page>=pages;const state=new URLSearchParams();if(q.value)state.set('q',q.value);if(cat.value)state.set('category',cat.value);if(year.value)state.set('year',year.value);if(credit?.value)state.set('credit',credit.value);history.replaceState(null,'',location.pathname+(state.size?'?'+state:''));observeReveals($('.work-list'));
 }
 $('.tools').onsubmit=e=>{e.preventDefault();page=1;draw()};q.oninput=()=>{page=1;draw()};cat.onchange=year.onchange=()=>{page=1;draw()};if(credit)credit.onchange=()=>{page=1;draw()};$('[data-prev]').onclick=()=>{page--;draw();archive.scrollIntoView({behavior:'smooth'})};$('[data-next]').onclick=()=>{page++;draw();archive.scrollIntoView({behavior:'smooth'})};draw();
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
let opener;const dialog=$('#photo-dialog');$$('[data-photo]').forEach(button=>button.onclick=()=>{opener=button;dialog.querySelector('img').src=root+button.dataset.photo;dialog.querySelector('img').alt=button.querySelector('img').alt;dialog.showModal()});$('[data-close-photo]')?.addEventListener('click',()=>dialog.close());dialog?.addEventListener('close',()=>opener?.focus());
})();
