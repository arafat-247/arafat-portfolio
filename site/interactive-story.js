(()=>{
  const root=document.querySelector('[data-interactive-story]');
  if(!root)return;
  const parse=el=>{
    const node=el.querySelector('[data-ix-config]');
    if(!node)return {};
    try{return JSON.parse(node.textContent)}catch(error){return {}}
  };
  const fmt=(value,decimals)=>{
    const n=Number(value);
    if(!Number.isFinite(n))return String(value??'');
    if(decimals!==undefined&&decimals!==null)return n.toLocaleString('en-GB',{minimumFractionDigits:Number(decimals),maximumFractionDigits:Number(decimals)});
    return Number.isInteger(n)?n.toLocaleString('en-GB'):n.toLocaleString('en-GB',{maximumFractionDigits:2});
  };
  const suffix=(value)=>String(value??'');

  root.querySelectorAll('[data-ix-module="ratio"]').forEach(el=>{
    const c=parse(el), buttons=[...el.querySelectorAll('[data-ratio-choice]')];
    const value=el.querySelector('[data-ratio-value]'),fill=el.querySelector('[data-ratio-fill]'),sentence=el.querySelector('[data-ratio-sentence]');
    const render=choice=>{
      const primary=choice==='primary';
      const n=Number(primary?c.numerator:c.secondary_value)||0,d=Number(c.denominator)||0,p=d?n/d*100:0,label=primary?(c.primary_label||'Part'):(c.secondary_label||'Remainder');
      if(value)value.textContent=fmt(n);
      if(fill)fill.style.width=Math.max(0,Math.min(100,p))+'%';
      if(sentence)sentence.textContent=label+': '+fmt(n)+' of '+fmt(d)+' ('+p.toFixed(1)+'%).';
      buttons.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.ratioChoice===choice)));
    };
    buttons.forEach(b=>b.addEventListener('click',()=>render(b.dataset.ratioChoice)));
  });

  root.querySelectorAll('[data-ix-module="scenario"]').forEach(el=>{
    const c=parse(el),range=el.querySelector('[data-scenario-range]'),input=el.querySelector('[data-scenario-input]'),output=el.querySelector('[data-scenario-output]'),visual=el.querySelector('[data-scenario-visual]');
    const render=v=>{
      const count=Math.max(1,Number(v)||1),result=(Number(c.total)||0)/count;
      if(input)input.textContent=fmt(count);
      if(output)output.textContent=fmt(result,c.decimals??1);
      if(range)range.value=String(count);
      if(visual){
        const dots=Math.min(70,Math.max(1,Math.round(result)));
        visual.replaceChildren(...Array.from({length:dots},()=>{const i=document.createElement('i');return i}));
      }
    };
    if(range)range.addEventListener('input',()=>render(range.value));
    el.querySelectorAll('[data-scenario-preset]').forEach(b=>b.addEventListener('click',()=>render(b.dataset.scenarioPreset)));
    render(range?.value||c.start||1);
  });

  root.querySelectorAll('[data-ix-module="bar_chart"]').forEach(el=>{
    const c=parse(el),list=el.querySelector('[data-bar-list]'),detail=el.querySelector('[data-bar-detail]');
    let order=(c.data||[]).map((_,i)=>i);
    const rows=()=>[...list.querySelectorAll('[data-bar-index]')];
    const select=index=>{
      rows().forEach(r=>r.setAttribute('aria-pressed',String(Number(r.dataset.barIndex)===index)));
      const item=(c.data||[])[index]||{};
      if(detail)detail.textContent=item.note||item.label+': '+fmt(item.value,c.decimals)+suffix(c.suffix);
    };
    rows().forEach(r=>r.addEventListener('click',()=>select(Number(r.dataset.barIndex))));
    el.querySelectorAll('[data-bar-sort]').forEach(button=>button.addEventListener('click',()=>{
      const mode=button.dataset.barSort;
      el.querySelectorAll('[data-bar-sort]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
      order=mode==='rank'?(c.data||[]).map((_,i)=>i).sort((a,b)=>Number(c.data[b].value)-Number(c.data[a].value)):(c.data||[]).map((_,i)=>i);
      const map=new Map(rows().map(r=>[Number(r.dataset.barIndex),r]));
      order.forEach(i=>list.appendChild(map.get(i)));
    }));
    if((c.data||[]).length)select(0);
  });

  root.querySelectorAll('[data-ix-module="compare"]').forEach(el=>{
    const c=parse(el),buttons=[...el.querySelectorAll('[data-compare-index]')];
    const l=el.querySelector('[data-compare-left]'),r=el.querySelector('[data-compare-right]'),lu=el.querySelector('[data-compare-unit-left]'),ru=el.querySelector('[data-compare-unit-right]'),lb=el.querySelector('[data-compare-bar-left]'),rb=el.querySelector('[data-compare-bar-right]'),delta=el.querySelector('[data-compare-delta]');
    const render=index=>{
      const m=(c.metrics||[])[index]||{},left=Number(m.left)||0,right=Number(m.right)||0,max=Math.max(Math.abs(left),Math.abs(right),1),unit=m.unit||'';
      if(l)l.textContent=fmt(left,m.decimals); if(r)r.textContent=fmt(right,m.decimals); if(lu)lu.textContent=unit;if(ru)ru.textContent=unit;
      if(lb)lb.style.height=(Math.abs(left)/max*52+8)+'%'; if(rb)rb.style.height=(Math.abs(right)/max*52+8)+'%';
      const gap=Math.abs(left-right),leader=left===right?'Neither':left>right?(c.left_label||'Left'):(c.right_label||'Right');
      if(delta)delta.textContent=left===right?'No difference on this measure.':leader+' leads by '+fmt(gap,m.decimals)+unit+'.';
      buttons.forEach((b,i)=>b.setAttribute('aria-pressed',String(i===index)));
    };
    buttons.forEach((b,i)=>b.addEventListener('click',()=>render(i)));
    if(buttons.length)render(0);
  });

  root.querySelectorAll('[data-ix-module="explorer"]').forEach(el=>{
    const c=parse(el),buttons=[...el.querySelectorAll('[data-explorer-index]')],title=el.querySelector('[data-explorer-title]'),text=el.querySelector('[data-explorer-text]'),metrics=el.querySelector('[data-explorer-metrics]');
    const render=index=>{
      const option=(c.options||[])[index]||{};
      if(title)title.textContent=option.title||option.label||'';
      if(text)text.textContent=option.text||'';
      if(metrics){
        metrics.replaceChildren(...(option.metrics||[]).map(m=>{
          const card=document.createElement('article'),label=document.createElement('span'),value=document.createElement('strong');
          label.textContent=m.label||'';value.textContent=fmt(m.value,m.decimals)+suffix(m.suffix);
          card.append(label,value);
          if(m.note){const small=document.createElement('small');small.textContent=m.note;card.appendChild(small)}
          return card;
        }));
      }
      buttons.forEach((b,i)=>b.setAttribute('aria-pressed',String(i===index)));
    };
    buttons.forEach((b,i)=>b.addEventListener('click',()=>render(i)));
    if(buttons.length)render(0);
  });

  root.querySelectorAll('[data-ix-module="timeline"]').forEach(el=>{
    const c=parse(el),buttons=[...el.querySelectorAll('[data-timeline-index]')],date=el.querySelector('[data-timeline-date]'),title=el.querySelector('[data-timeline-title]'),text=el.querySelector('[data-timeline-text]');
    const render=index=>{
      const event=(c.events||[])[index]||{};
      if(date)date.textContent=event.date||'';if(title)title.textContent=event.label||'';if(text)text.textContent=event.text||'';
      buttons.forEach((b,i)=>b.setAttribute('aria-pressed',String(i===index)));
    };
    buttons.forEach((b,i)=>b.addEventListener('click',()=>render(i)));
    if(buttons.length)render(0);
  });

  const modules=[...root.querySelectorAll('.ix-module')],nav=[...root.querySelectorAll('[data-module-nav] a')];
  const setActive=id=>nav.forEach(a=>a.classList.toggle('is-active',a.getAttribute('href')==='#'+id));
  if('IntersectionObserver'in window){
    const io=new IntersectionObserver(entries=>{
      const visible=entries.filter(e=>e.isIntersecting).sort((a,b)=>b.intersectionRatio-a.intersectionRatio);
      if(visible[0])setActive(visible[0].target.id);
    },{rootMargin:'-18% 0px -58% 0px',threshold:[0,.2,.5]});
    modules.forEach(m=>io.observe(m));
  }
  const updateProgress=()=>{
    const shell=root.querySelector('.ix-shell');if(!shell)return;
    const top=shell.getBoundingClientRect().top+scrollY,total=Math.max(1,shell.offsetHeight-innerHeight*.6),travel=scrollY-top+innerHeight*.2;
    document.documentElement.style.setProperty('--progress',(Math.max(0,Math.min(1,travel/total))*100).toFixed(2)+'%');
  };
  addEventListener('scroll',updateProgress,{passive:true});addEventListener('resize',updateProgress,{passive:true});updateProgress();
})();