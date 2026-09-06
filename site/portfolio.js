(()=>{'use strict';
const $=s=>document.querySelector(s),root=document.body.dataset.root||'';
const menu=$('#mobile-menu'),toggle=$('.menutoggle');
function closeMenu(){if(menu)menu.hidden=true;if(toggle){toggle.setAttribute('aria-expanded','false');toggle.textContent='☰ Menu'}}
if(toggle)toggle.onclick=()=>{menu.hidden=!menu.hidden;toggle.setAttribute('aria-expanded',String(!menu.hidden));toggle.textContent=menu.hidden?'☰ Menu':'× Close'};
document.addEventListener('keydown',e=>{if(e.key==='Escape'){closeMenu();toggle?.focus()}});
document.addEventListener('click',e=>{if(menu&&!menu.hidden&&!menu.contains(e.target)&&!toggle?.contains(e.target))closeMenu()});
const current=location.pathname.split('/').pop()||'index.html';document.querySelectorAll('.identity nav a').forEach(a=>{if(a.getAttribute('href')===root+current)a.setAttribute('aria-current','page')});
const html=v=>String(v||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const local=v=>/^assets\//.test(v||'')&&!String(v).split('/').includes('..')?v:'';
function formatDate(v){if(!v)return 'Date not recorded';const d=new Date(v);return Number.isNaN(+d)?'Date not recorded':d.toLocaleDateString('en-GB',{day:'numeric',month:'long',year:'numeric',timeZone:'Asia/Dhaka'})}
function activateMotion(scope=document){const items=[...scope.querySelectorAll('.tile,.card,.photogrid figure,.recognition li,.bio,.contactrow')];items.forEach(el=>el.classList.add('motion-item'));if('IntersectionObserver'in window&&!matchMedia('(prefers-reduced-motion: reduce)').matches){const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('is-visible');observer.unobserve(entry.target)}}),{threshold:.08,rootMargin:'0px 0px -24px'});items.forEach(el=>observer.observe(el))}else items.forEach(el=>el.classList.add('is-visible'))}
const archive=$('[data-archive]');
if(archive){(async()=>{try{
 const r=await fetch(root+'data/index.json');if(!r.ok)throw Error('Archive could not be loaded. Please reload.');
 const all=(await r.json()).articles.filter(a=>a.stream===archive.dataset.archive),q=$('[name=q]'),cat=$('[name=category]'),year=$('[name=year]');let page=1;
 for(const value of [...new Set(all.map(a=>a.category).filter(Boolean))].sort()){const o=new Option(value,value);cat.add(o)}
 for(const value of [...new Set(all.map(a=>a.date_published?.slice(0,4)).filter(Boolean))].sort().reverse())year.add(new Option(value,value));
 const params=new URLSearchParams(location.search);q.value=params.get('q')||'';cat.value=params.get('category')||'';year.value=params.get('year')||'';
 function draw(){const term=q.value.trim().toLocaleLowerCase();const found=all.filter(a=>(!cat.value||a.category===cat.value)&&(!year.value||a.date_published.startsWith(year.value))&&[a.title,a.excerpt,a.category,a.source_name].join(' ').toLocaleLowerCase().includes(term));const pages=Math.max(1,Math.ceil(found.length/12));page=Math.min(page,pages);
 $('.count').textContent=found.length+' '+(found.length===1?'entry':'entries');
 $('.cards').innerHTML=found.slice((page-1)*12,page*12).map(a=>{const url=/^(stories|thoughts)\/[a-zA-Z0-9_-]+\/$/.test(a.local_url)?root+a.local_url:root+'reporting.html';return `<article class="card">${local(a.cover_image)?`<img class="cardimage" loading="lazy" src="${html(root+a.cover_image)}" alt="${html(a.cover_alt)}">`:''}<div class="copy"><div class="meta">${html(a.source_name||'Arafat Rahaman')} · ${html(formatDate(a.date_published))}</div><h2><a href="${html(url)}">${html(a.title)}</a></h2><p>${html(a.excerpt)}</p><a class="read" href="${html(url)}">Read story →</a></div></article>`}).join('')||'<p class="empty">No matches. Try another search or category.</p>';
 $('[data-page]').textContent=`Page ${page} of ${pages}`;$('[data-prev]').disabled=page<=1;$('[data-next]').disabled=page>=pages;
 activateMotion($('.cards'));const state=new URLSearchParams();if(q.value)state.set('q',q.value);if(cat.value)state.set('category',cat.value);if(year.value)state.set('year',year.value);history.replaceState(null,'',location.pathname+(state.size?'?'+state:''));
 }
 $('.tools').onsubmit=e=>{e.preventDefault();page=1;draw()};q.oninput=()=>{page=1;draw()};cat.onchange=year.onchange=()=>{page=1;draw()};
 $('[data-prev]').onclick=()=>{page--;draw();archive.scrollIntoView({block:'start'})};$('[data-next]').onclick=()=>{page++;draw();archive.scrollIntoView({block:'start'})};draw();
 }catch(e){$('.count').textContent=e.message;$('[data-next]').disabled=true}})()}
document.querySelector('[data-print]')?.addEventListener('click',()=>window.print());
document.querySelector('[data-share]')?.addEventListener('click',async()=>{try{if(navigator.share)await navigator.share({title:document.title,url:location.href});else{await navigator.clipboard.writeText(location.href);$('[data-share-status]').textContent='Link copied.'}}catch(e){if(e.name!=='AbortError')$('[data-share-status]').textContent='Copy the address from your browser to share this story.'}});
let opener;const dialog=$('#photo-dialog');document.querySelectorAll('[data-photo]').forEach(b=>b.onclick=()=>{opener=b;dialog.querySelector('img').src=root+b.dataset.photo;dialog.querySelector('img').alt=b.querySelector('img').alt;dialog.showModal()});$('[data-close-photo]')?.addEventListener('click',()=>dialog.close());dialog?.addEventListener('close',()=>opener?.focus());
activateMotion();
if(matchMedia('(hover: hover) and (pointer: fine)').matches){document.querySelectorAll('.tile').forEach(tile=>{tile.addEventListener('pointermove',e=>{const r=tile.getBoundingClientRect();tile.style.setProperty('--shift-x',((e.clientX-r.left)/r.width-.5)*8+'px');tile.style.setProperty('--shift-y',((e.clientY-r.top)/r.height-.5)*8+'px')});tile.addEventListener('pointerleave',()=>{tile.style.setProperty('--shift-x','0px');tile.style.setProperty('--shift-y','0px')})})}
const reading=$('.reading');if(reading){const bar=document.createElement('div');bar.className='reading-progress';bar.setAttribute('aria-hidden','true');document.body.append(bar);let scheduled=false;const updateProgress=()=>{const start=reading.offsetTop,end=start+reading.offsetHeight-innerHeight,progress=end<=start?1:Math.max(0,Math.min(1,(scrollY-start)/(end-start)));bar.style.transform=`scaleX(${progress})`;scheduled=false};addEventListener('scroll',()=>{if(!scheduled){scheduled=true;requestAnimationFrame(updateProgress)}},{passive:true});addEventListener('resize',updateProgress);updateProgress()}
})();
