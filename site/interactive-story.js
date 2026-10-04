(()=>{
  const root=document.querySelector('[data-interactive-story]');
  if(!root||root.dataset.ready==='1')return;
  root.dataset.ready='1';
  document.documentElement.classList.add('js');

  const copy=root.querySelector('[data-interactive-copy]');
  const chapterNav=root.querySelector('[data-chapter-nav]');
  const currentLabel=root.querySelector('[data-current-part]');
  const totalLabel=root.querySelector('[data-total-parts]');
  const progressBars=[...root.querySelectorAll('[data-progress-fill]')];
  if(!copy)return;

  const children=[...copy.children];
  const sections=[];
  let section=null;
  let proseCount=0;

  const makeSection=()=>{
    section=document.createElement('section');
    section.className='story-beat';
    section.id='part-'+(sections.length+1);
    section.dataset.number=String(sections.length+1).padStart(2,'0');
    sections.push(section);
    proseCount=0;
    return section;
  };

  const fragment=document.createDocumentFragment();
  children.forEach((child,index)=>{
    const tag=child.tagName;
    const heading=tag==='H2'||tag==='H3';
    const longEnough=section&&proseCount>=4&&tag==='P';
    if(!section||heading&&section.children.length||longEnough){
      makeSection();
      fragment.appendChild(section);
    }
    section.appendChild(child);
    if(tag==='P')proseCount+=1;
    if(tag==='BLOCKQUOTE'&&proseCount>=2)proseCount=4;
    if(index===children.length-1&&section&&!section.children.length)section.remove();
  });

  if(!sections.length){
    const fallback=makeSection();
    fallback.innerHTML='<p>This story is not available.</p>';
    fragment.appendChild(fallback);
  }

  copy.replaceChildren(fragment);
  copy.dataset.enhanced='true';
  if(totalLabel)totalLabel.textContent=String(sections.length).padStart(2,'0');

  const labels=sections.map((beat,index)=>{
    const heading=beat.querySelector('h2,h3');
    return heading&&heading.textContent.trim()?heading.textContent.trim():'Part '+(index+1);
  });

  if(chapterNav){
    chapterNav.replaceChildren();
    sections.forEach((beat,index)=>{
      const link=document.createElement('a');
      link.href='#'+beat.id;
      link.dataset.part=String(index);
      const number=document.createElement('span');
      number.textContent=String(index+1).padStart(2,'0');
      const title=document.createElement('span');
      title.textContent=labels[index];
      link.append(number,title);
      chapterNav.appendChild(link);
    });
  }

  const navLinks=chapterNav?[...chapterNav.querySelectorAll('a')]:[];
  let activeIndex=0;
  const setActive=index=>{
    activeIndex=Math.max(0,Math.min(sections.length-1,index));
    sections.forEach((beat,i)=>beat.classList.toggle('is-active',i===activeIndex));
    navLinks.forEach((link,i)=>{
      if(i===activeIndex)link.setAttribute('aria-current','true');
      else link.removeAttribute('aria-current');
    });
    if(currentLabel)currentLabel.textContent=String(activeIndex+1).padStart(2,'0');
  };
  setActive(0);

  if('IntersectionObserver' in window){
    const observer=new IntersectionObserver(entries=>{
      const visible=entries.filter(entry=>entry.isIntersecting).sort((a,b)=>b.intersectionRatio-a.intersectionRatio);
      if(!visible.length)return;
      const index=sections.indexOf(visible[0].target);
      if(index>=0)setActive(index);
    },{rootMargin:'-18% 0px -58% 0px',threshold:[0,.15,.35,.6]});
    sections.forEach(beat=>observer.observe(beat));
  }

  const story=root.querySelector('[data-story-body]')||copy;
  let ticking=false;
  const updateProgress=()=>{
    ticking=false;
    const rect=story.getBoundingClientRect();
    const absoluteTop=window.scrollY+rect.top;
    const total=Math.max(1,story.offsetHeight-window.innerHeight*.55);
    const travelled=window.scrollY-absoluteTop+window.innerHeight*.22;
    const ratio=Math.max(0,Math.min(1,travelled/total));
    const value=(ratio*100).toFixed(2)+'%';
    document.documentElement.style.setProperty('--ix-progress',value);
    progressBars.forEach(bar=>bar.style.width=value);
  };
  const onScroll=()=>{
    if(ticking)return;
    ticking=true;
    requestAnimationFrame(updateProgress);
  };
  window.addEventListener('scroll',onScroll,{passive:true});
  window.addEventListener('resize',onScroll,{passive:true});
  updateProgress();

  root.querySelectorAll('a[href^="#"]').forEach(link=>{
    link.addEventListener('click',event=>{
      const target=document.querySelector(link.getAttribute('href'));
      if(!target)return;
      event.preventDefault();
      const reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      target.scrollIntoView({behavior:reduce?'auto':'smooth',block:'start'});
      target.focus({preventScroll:true});
    });
  });

  sections.forEach(section=>{
    section.setAttribute('tabindex','-1');
  });
})();
