(()=>{
  const safeHTML=input=>{const t=document.createElement('template');t.innerHTML=String(input||'');t.content.querySelectorAll('script,style,iframe,object,embed,form,input,button').forEach(n=>n.remove());t.content.querySelectorAll('*').forEach(n=>[...n.attributes].forEach(a=>{if(/^on/i.test(a.name)||(a.name==='href'&&/^javascript:/i.test(a.value)))n.removeAttribute(a.name)}));return t.innerHTML};
  async function init(){
    const slug=new URL(location.href).searchParams.get('slug')||'';
    const data=await AR.optionalJson('data/journal-index.json',{articles:[]});
    const item=(data.articles||[]).find(a=>a.slug===slug&&a.status!=='draft');
    const host=document.querySelector('#article');
    if(!item){host.innerHTML='<p class="micro-label">Journal</p><header><h1>Piece not found.</h1><p class="journal-deck">This entry may be unpublished or the link may be incorrect.</p></header><a href="journal.html">Return to the Journal ↗</a>';document.title='Piece not found — Arafat Rahaman';return}
    document.title=`${item.title} — Arafat Rahaman`;
    document.querySelector('meta[name="description"]')?.setAttribute('content',item.deck||item.excerpt||'Independent writing by Arafat Rahaman.');
    host.innerHTML=`<nav class="story-breadcrumb"><a href="journal.html">Journal</a> / ${AR.esc(item.category||'Essay')}</nav><header><div class="journal-story-meta"><span>First published here</span><span>${AR.esc(item.category||'Journal')}</span><time>${AR.esc(AR.fmtDate(item.date_published||item.date))}</time></div><h1>${AR.esc(item.title)}</h1>${item.deck?`<p class="journal-deck">${AR.esc(item.deck)}</p>`:''}</header>${item.cover_image?`<img class="journal-cover" src="${AR.esc(item.cover_image)}" alt="${AR.esc(item.cover_alt||item.title)}">`:''}<article class="journal-story-body">${safeHTML(item.body_html||'')}</article><section class="source-note"><div><span>Publication</span><strong>First published on this website</strong></div><a href="journal.html">More from the Journal ↗</a></section>`;
  }
  init().catch(e=>{console.error(e);document.querySelector('#article').innerHTML='<h1>The Journal could not be loaded.</h1>'});
})();
