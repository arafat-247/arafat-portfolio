(()=>{
  const host=document.querySelector('#photo-grid'),empty=document.querySelector('#photo-empty');
  const src=p=>p?.src||p?.webp||p?.image||'';
  AR.optionalJson('data/photography.json',{photos:[]}).then(data=>{
    const photos=(data.photos||[]).filter(p=>src(p));
    if(!photos.length){empty.hidden=false;return}
    host.innerHTML=photos.map((p,i)=>`<figure class="photo-card ${p.wide?'wide':''}" data-reveal><div class="photo-card-media"><img src="${AR.esc(src(p))}" alt="${AR.esc(p.alt||p.caption||'Photograph by Arafat Rahaman')}" loading="${i<2?'eager':'lazy'}"></div><figcaption><span>${AR.esc(p.caption||'Untitled')}</span><span>${AR.esc([p.location,p.year].filter(Boolean).join(' · '))}</span></figcaption></figure>`).join('');
    host.querySelectorAll('[data-reveal]').forEach(el=>{el.classList.add('is-visible')});
  }).catch(()=>{empty.hidden=false});
})();
