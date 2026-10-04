(()=>{
 const root=document.querySelector('[data-immersive-story]');if(!root)return;
 const field=root.querySelector('[data-school-field]');
 if(field){
   const frag=document.createDocumentFragment();
   for(let i=0;i<100;i++){const dot=document.createElement('i');frag.appendChild(dot)}
   field.appendChild(frag);
 }
 const steps=[...root.querySelectorAll('[data-step]')],dots=field?[...field.children]:[];
 const big=root.querySelector('[data-big-number]'),label=root.querySelector('[data-big-label]'),fill=root.querySelector('[data-share-fill]'),caption=root.querySelector('[data-visual-caption]');
 const renderStep=i=>{
   steps.forEach((s,n)=>s.classList.toggle('is-active',n===i));
   if(i===0){if(big)big.textContent='65,567';if(label)label.textContent='government primary schools';if(fill)fill.style.width='100%';if(caption)caption.textContent='Start with the full system.';dots.forEach(d=>d.className='')}
   if(i===1){if(big)big.textContent='36,235';if(label)label.textContent='vacant headteacher posts';if(fill)fill.style.width='55.3%';if(caption)caption.textContent='About 55.3% of headteacher posts were vacant.';dots.forEach((d,n)=>d.className=n<55?'hot':'dim')}
   if(i===2){if(big)big.textContent='1';if(label)label.textContent='assistant teacher may carry both teaching and administration';if(fill)fill.style.width='55.3%';if(caption)caption.textContent='A vacancy is not just an empty office; the work moves to someone already teaching.';dots.forEach((d,n)=>d.className=n<55?'hot':'dim')}
 };
 if('IntersectionObserver'in window){
   const io=new IntersectionObserver(entries=>{
     const active=entries.filter(e=>e.isIntersecting).sort((a,b)=>b.intersectionRatio-a.intersectionRatio)[0];
     if(active)renderStep(Number(active.target.dataset.step));
   },{rootMargin:'-25% 0px -45% 0px',threshold:[0,.2,.5,.8]});
   steps.forEach(s=>io.observe(s));
 } else renderStep(0);

 const range=root.querySelector('[data-teacher-range]'),teachers=root.querySelector('[data-teachers]'),plural=root.querySelector('[data-plural]'),per=root.querySelector('[data-students-per]'),teacherDots=root.querySelector('[data-teacher-dots]');
 const renderTeachers=value=>{
   const n=Math.max(1,Math.min(5,Number(value)||1));
   if(teachers)teachers.textContent=String(n);if(plural)plural.textContent=n===1?'':'s';if(per)per.textContent=(70/n).toFixed(n===1?0:1);
   if(teacherDots){teacherDots.replaceChildren(...Array.from({length:n},()=>document.createElement('i')))}
 };
 if(range){range.addEventListener('input',()=>renderTeachers(range.value));renderTeachers(range.value)}

 const cases=[
  {location:'Jamalpur',title:'West Nangla Government Primary School',text:'Five posts were sanctioned, but the school was operating with one teacher for 70 students.',metrics:[['Sanctioned posts','5'],['Teachers serving','1'],['Students','70'],['Vacant posts','4']],quote:'“The shortage of teachers has made many guardians reluctant to admit their children to this school.”'},
  {location:'Gazipur',title:'Sonarua Government Primary School',text:'Four teachers were serving against six sanctioned posts. Around three classes were cancelled every day.',metrics:[['Sanctioned posts','6'],['Teachers serving','4'],['Vacant posts','2'],['Classes cancelled','~3/day']],quote:'“A teacher has to take two to three additional classes every day.”'},
  {location:'Faridpur',title:'No. 24 Purba Aliabad Government Primary School',text:'Three teachers were working against five sanctioned posts.',metrics:[['Sanctioned posts','5'],['Teachers serving','3'],['Vacant posts','2'],['Reported effect','Split classes']],quote:'“One teacher often teaches two classes at the same time and sometimes leaves one class before finishing the lesson.”'}
 ];
 const caseButtons=[...root.querySelectorAll('[data-case]')],caseLocation=root.querySelector('[data-case-location]'),caseTitle=root.querySelector('[data-case-title]'),caseText=root.querySelector('[data-case-text]'),caseMetrics=root.querySelector('[data-case-metrics]'),caseQuote=root.querySelector('[data-case-quote]'),caseGraphic=root.querySelector('[data-case-graphic]');
 const renderCase=i=>{
   const c=cases[i];if(!c)return;
   caseButtons.forEach((b,n)=>b.setAttribute('aria-pressed',String(n===i)));
   if(caseLocation)caseLocation.textContent=c.location;if(caseTitle)caseTitle.textContent=c.title;if(caseText)caseText.textContent=c.text;if(caseQuote)caseQuote.textContent=c.quote;
   if(caseMetrics){caseMetrics.replaceChildren(...c.metrics.map(([l,v])=>{const d=document.createElement('div'),s=document.createElement('span'),b=document.createElement('strong');s.textContent=l;b.textContent=v;d.append(s,b);return d}))}
   if(caseGraphic)caseGraphic.style.setProperty('--case-index',i);
 };
 caseButtons.forEach((b,i)=>b.addEventListener('click',()=>renderCase(i)));renderCase(0);

 const regional=[['Chattogram',6.65],['Dhaka',6.52],['Rajshahi',6.46],['Barishal',5.89],['Sylhet',5.59]];
 const bars=root.querySelector('[data-rank-bars]'),rankButtons=[...root.querySelectorAll('[data-rank-order]')];
 const renderRanks=mode=>{
   const data=[...regional];if(mode==='low')data.sort((a,b)=>a[1]-b[1]);
   rankButtons.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.rankOrder===mode)));
   if(bars){bars.replaceChildren(...data.map(([name,value])=>{const row=document.createElement('div');row.className='rank-row';const l=document.createElement('span'),track=document.createElement('div'),bar=document.createElement('i'),v=document.createElement('strong');l.textContent=name;bar.style.width=(value/6.65*100)+'%';track.appendChild(bar);v.textContent=value.toFixed(2);row.append(l,track,v);return row}))}
 };
 rankButtons.forEach(b=>b.addEventListener('click',()=>renderRanks(b.dataset.rankOrder)));renderRanks('reported');

 const learning={math:{a:61,b:70,copy:'61% of Class III students and 70% of Class V students lacked grade-appropriate proficiency in mathematics.'},bangla:{a:51,b:50,copy:'51% of Class III students and 50% of Class V students lacked the required competency in Bangla.'}};
 const subjectButtons=[...root.querySelectorAll('[data-subject]')],class3=root.querySelector('[data-class3]'),class5=root.querySelector('[data-class5]'),f3=root.querySelector('[data-class3-fill]'),f5=root.querySelector('[data-class5-fill]'),learnCopy=root.querySelector('[data-learning-copy]');
 const renderLearning=key=>{const d=learning[key];subjectButtons.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.subject===key)));if(class3)class3.textContent=d.a+'%';if(class5)class5.textContent=d.b+'%';if(f3)f3.style.height=d.a+'%';if(f5)f5.style.height=d.b+'%';if(learnCopy)learnCopy.textContent=d.copy};
 subjectButtons.forEach(b=>b.addEventListener('click',()=>renderLearning(b.dataset.subject)));renderLearning('math');

 const times=[
  {date:'2013',title:'Recruitment rules set the route',text:'Under the existing rules, 20 percent of headteacher posts are filled through direct recruitment and 80 percent through promotion from assistant teachers.'},
  {date:'2017',title:'A writ petition stalls the process',text:'A writ petition challenged a provision of the 2013 Recruitment Rules relating to seniority, stalling the filling of many headteacher posts.'},
  {date:'2 July 2026',title:'The Appellate Division removes a major obstacle',text:'The Appellate Division overturned a High Court verdict that had struck down part of the rules governing seniority and promotion.'},
  {date:'Next',title:'Recruitment is expected to restart',text:'Primary and mass education ministry officials said a formal requisition would soon be sent to the Public Service Commission for direct recruitment and promotion under special arrangements.'}
 ];
 const timeButtons=[...root.querySelectorAll('[data-time]')],td=root.querySelector('[data-time-date]'),tt=root.querySelector('[data-time-title]'),tx=root.querySelector('[data-time-text]');
 const renderTime=i=>{const d=times[i];timeButtons.forEach((b,n)=>b.setAttribute('aria-pressed',String(n===i)));if(td)td.textContent=d.date;if(tt)tt.textContent=d.title;if(tx)tx.textContent=d.text};
 timeButtons.forEach((b,i)=>b.addEventListener('click',()=>renderTime(i)));renderTime(0);
})();