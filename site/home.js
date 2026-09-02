(()=>{
  const framesHost=document.querySelector('#home-frames');
  const grid=document.querySelector('#home-photo-grid');
  const links=[...document.querySelectorAll('[data-home-photo]')];
  const label=document.querySelector('#home-frame-label');
  const visual=document.querySelector('#home-visual');
  let active=0,timer=null,photos=[];
  const fallback=[
    {src:'assets/portraits/home.webp',alt:'Arafat Rahaman'},
    {src:'assets/portraits/about.webp',alt:'Arafat Rahaman'},
    {src:'assets/portraits/contact.webp',alt:'Arafat Rahaman'},
    {src:'assets/portraits/home.webp',alt:'Arafat Rahaman'}
  ];
  function source(p){return p?.src||p?.webp||p?.image||''}
  function activate(i){if(!photos.length)return;active=((i%photos.length)+photos.length)%photos.length;framesHost.querySelectorAll('.home-frame').forEach((f,n)=>f.classList.toggle('is-active',n===active));label.textContent=`Field frame ${String(active+1).padStart(2,'0')}`;const p=photos[active];document.querySelector('.home-rail')?.style.setProperty('--home-mobile-image',`url("${source(p).replaceAll('"','%22')}")`)}
  function start(){clearInterval(timer);if(matchMedia('(prefers-reduced-motion: reduce)').matches)return;timer=setInterval(()=>activate(active+1),7000)}
  async function init(){
    const data=await AR.optionalJson('data/photography.json',{photos:[]});
    photos=(data.photos||[]).filter(p=>source(p));
    if(!photos.length)photos=fallback;
    while(photos.length<4)photos.push(photos[photos.length%Math.max(1,photos.length)]||fallback[0]);
    framesHost.innerHTML=photos.slice(0,6).map((p,i)=>`<figure class="home-frame ${i===0?'is-active':''}"><img src="${AR.esc(source(p))}" alt="${AR.esc(p.alt||p.caption||'Photograph by Arafat Rahaman')}" ${i===0?'fetchpriority="high"':'loading="lazy"'}></figure>`).join('');
    const previews=photos.slice(0,3);grid.innerHTML=previews.map(p=>`<figure><img src="${AR.esc(source(p))}" alt="${AR.esc(p.alt||p.caption||'Photograph by Arafat Rahaman')}" loading="lazy"></figure>`).join('');
    activate(0);start();
    links.forEach(a=>{const i=Number(a.dataset.homePhoto)||0;a.addEventListener('mouseenter',()=>{activate(i);start()});a.addEventListener('focus',()=>{activate(i);start()})});
    if(visual&&!matchMedia('(prefers-reduced-motion: reduce)').matches){visual.addEventListener('pointermove',e=>{const r=visual.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;const img=framesHost.querySelector('.home-frame.is-active img');if(img)img.style.transform=`translate(${x*8}px,${y*6}px) scale(1.02)`});visual.addEventListener('pointerleave',()=>{const img=framesHost.querySelector('.home-frame.is-active img');if(img)img.style.transform=''})}
  }
  init().catch(console.error);
})();
