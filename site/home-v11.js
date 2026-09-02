(()=>{
  const root=document.documentElement;
  const a=document.querySelector('.hero-image-a');
  const b=document.querySelector('.hero-image-b');
  const second=document.querySelector('.photo-window-image');
  const previewLinks=[...document.querySelectorAll('[data-preview]')];
  const prefersReduced=window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let photos=[];
  let active=0;
  let front=a;
  let back=b;
  let timer=null;

  const escURL=v=>String(v||'').replace(/["\\\n\r]/g,'');
  function setBg(el,src){if(el&&src)el.style.backgroundImage=`url("${escURL(src)}")`}
  function show(index,immediate=false){
    if(!photos.length)return;
    active=((index%photos.length)+photos.length)%photos.length;
    const src=photos[active].src;
    setBg(back,src);
    if(immediate){front.classList.remove('is-visible');back.classList.add('is-visible')}
    else requestAnimationFrame(()=>{back.classList.add('is-visible');front.classList.remove('is-visible')});
    const old=front;front=back;back=old;
    if(second&&photos.length>1)setBg(second,photos[(active+1)%photos.length].src);
  }
  function startRotation(){
    if(prefersReduced||photos.length<2)return;
    clearInterval(timer);
    timer=setInterval(()=>show(active+1),9000);
  }
  async function loadPhotos(){
    try{
      const res=await fetch('data/photography.json',{cache:'no-store'});
      if(!res.ok)throw new Error('Photography data unavailable');
      const data=await res.json();
      photos=(data.photos||[]).filter(p=>p&&p.src).slice(0,6);
    }catch(err){console.warn(err)}
    if(!photos.length){
      photos=[{src:'assets/portraits/home.webp'}];
    }
    setBg(front,photos[0].src);front.classList.add('is-visible');
    if(second)setBg(second,photos[Math.min(1,photos.length-1)].src);
    startRotation();
  }
  previewLinks.forEach((link,i)=>{
    link.addEventListener('mouseenter',()=>{if(photos.length){clearInterval(timer);show(i%photos.length)}});
    link.addEventListener('focus',()=>{if(photos.length){clearInterval(timer);show(i%photos.length)}});
    link.addEventListener('mouseleave',startRotation);
    link.addEventListener('blur',startRotation);
  });

  const drawer=document.querySelector('#mobile-drawer');
  const openBtn=document.querySelector('.mobile-menu-button');
  const closeBtn=document.querySelector('.drawer-close');
  let lastFocus=null;
  function openDrawer(){
    if(!drawer)return;lastFocus=document.activeElement;drawer.hidden=false;document.body.style.overflow='hidden';openBtn?.setAttribute('aria-expanded','true');closeBtn?.focus();
  }
  function closeDrawer(){
    if(!drawer)return;drawer.hidden=true;document.body.style.overflow='';openBtn?.setAttribute('aria-expanded','false');lastFocus?.focus?.();
  }
  openBtn?.addEventListener('click',openDrawer);
  closeBtn?.addEventListener('click',closeDrawer);
  drawer?.querySelectorAll('a').forEach(x=>x.addEventListener('click',closeDrawer));
  document.addEventListener('keydown',e=>{if(e.key==='Escape'&&drawer&&!drawer.hidden)closeDrawer()});

  loadPhotos();
})();
