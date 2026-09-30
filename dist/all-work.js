(()=>{'use strict';
const $=s=>document.querySelector(s),root=document.body.dataset.root||'';
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
})();
