(()=>{
  const scene=document.querySelector('.cinematic-home');
  if(!scene||matchMedia('(max-width:800px)').matches||matchMedia('(prefers-reduced-motion:reduce)').matches)return;
  const image=scene.querySelector('.cinematic-photo img');
  let frame=0;
  scene.querySelector('.cinematic-hero').addEventListener('pointermove',event=>{
    if(event.pointerType==='touch')return;
    cancelAnimationFrame(frame);
    frame=requestAnimationFrame(()=>{
      const box=scene.getBoundingClientRect();
      const move=(event.clientX-box.left)/box.width-.5;
      image.style.transform=`scale(1.055) translateX(${(move*7).toFixed(2)}px)`;
    });
  },{passive:true});
  scene.querySelector('.cinematic-hero').addEventListener('pointerleave',()=>{image.style.transform='';});
})();
