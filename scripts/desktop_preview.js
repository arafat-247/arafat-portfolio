(function(){
  const button=document.querySelector('.desk-menu-button');
  const menu=document.querySelector('.desk-mobile-nav');
  if(button&&menu){
    button.addEventListener('click',()=>{const open=button.getAttribute('aria-expanded')==='true';button.setAttribute('aria-expanded',String(!open));button.setAttribute('aria-label',open?'Open navigation':'Close navigation');menu.hidden=open;});
    menu.addEventListener('click',e=>{if(e.target.closest('a')){menu.hidden=true;button.setAttribute('aria-expanded','false');button.setAttribute('aria-label','Open navigation');}});
    document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!menu.hidden){menu.hidden=true;button.setAttribute('aria-expanded','false');button.focus();}});
  }
  const time=document.getElementById('desk-dhaka-time');
  if(time){const label=time.querySelector('.desk-clock-label');const clock=time.querySelector('.desk-clock');const formatter=new Intl.DateTimeFormat('en-GB',{timeZone:'Asia/Dhaka',hour:'2-digit',minute:'2-digit',second:'2-digit',hour12:false});const update=()=>{const now=new Date();const parts=Object.fromEntries(formatter.formatToParts(now).map(p=>[p.type,p.value]));const hour=Number(parts.hour)%12,minute=Number(parts.minute),second=Number(parts.second);time.dateTime=now.toISOString();label.textContent='Dhaka · '+parts.hour+':'+parts.minute;clock.style.setProperty('--hour-angle',(hour*30+minute*.5)+'deg');clock.style.setProperty('--minute-angle',(minute*6+second*.1)+'deg');};update();setInterval(update,1000);}
})();
