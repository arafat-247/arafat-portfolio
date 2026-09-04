(()=>{
  const src=p=>p?.src||p?.webp||p?.image||'';
  async function init(){
    const data=await AR.optionalJson('data/photography.json',{photos:[]});
    const photos=(data.photos||[]).filter(p=>src(p));
    const landscape=photos.find(p=>!p.src?.includes('(1)')&&!p.src?.includes('(2)'))||photos[0];
    const portrait=photos.find(p=>p.src?.includes('(1)'))||photos.find(p=>p.src?.includes('(2)'))||photos[0];
    const band=photos.find((p,i)=>i>2&&!p.src?.includes('(1)'))||landscape;
    const desktop=document.querySelector('#desktop-hero-image'),mobile=document.querySelector('#mobile-hero-image'),bandHost=document.querySelector('#home-photo-band-image');
    if(desktop&&landscape)desktop.style.backgroundImage=`url("${src(landscape).replaceAll('"','%22')}")`;
    if(mobile&&portrait){mobile.src=src(portrait);mobile.alt=portrait.alt||portrait.caption||'Documentary photograph by Arafat Rahaman'}
    if(bandHost&&band)bandHost.style.backgroundImage=`url("${src(band).replaceAll('"','%22')}")`;
  }
  init().catch(console.error);
})();
