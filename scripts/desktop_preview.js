(function(){
  const button=document.querySelector('.desk-menu-button');
  const menu=document.querySelector('.desk-mobile-nav');
  if(button&&menu){
    button.addEventListener('click',()=>{const open=button.getAttribute('aria-expanded')==='true';button.setAttribute('aria-expanded',String(!open));button.setAttribute('aria-label',open?'Open navigation':'Close navigation');menu.hidden=open;});
    menu.addEventListener('click',e=>{if(e.target.closest('a')){menu.hidden=true;button.setAttribute('aria-expanded','false');button.setAttribute('aria-label','Open navigation');}});
    document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!menu.hidden){menu.hidden=true;button.setAttribute('aria-expanded','false');button.focus();}});
  }
  const time=document.getElementById('desk-dhaka-time');
  if(time){const update=()=>{const now=new Date();time.dateTime=now.toISOString();time.textContent='Dhaka · '+new Intl.DateTimeFormat('en-GB',{timeZone:'Asia/Dhaka',hour:'2-digit',minute:'2-digit',hour12:false}).format(now);};update();setInterval(update,30000);}
})();
