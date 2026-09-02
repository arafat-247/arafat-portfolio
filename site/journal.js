(()=>{
 const host=document.querySelector('#journal-list'),empty=document.querySelector('#journal-empty');
 AR.optionalJson('data/journal-index.json',{articles:[]}).then(data=>{
   const items=(data.articles||[]).filter(a=>a.status!=='draft'&&a.local_url).sort((a,b)=>Number(b.published_sort||0)-Number(a.published_sort||0));
   if(!items.length)return;
   empty.hidden=true;host.hidden=false;
   host.innerHTML=items.map(a=>`<article class="journal-item"><time>${AR.esc(AR.fmtDate(a.date_published||a.date))}</time><h3><a href="${AR.esc(a.local_url)}">${AR.esc(a.title)}</a></h3><a href="${AR.esc(a.local_url)}">↗</a></article>`).join('');
 }).catch(()=>{});
})();
