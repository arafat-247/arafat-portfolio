window.AR=(()=>{
  const root=()=>document.body?.dataset?.root||"";
  const esc=(v="")=>String(v).replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;").replaceAll('"',"&quot;").replaceAll("'","&#039;");
  const fmtDate=value=>{if(!value)return"";const m=String(value).match(/^(\d{4})-(\d{2})-(\d{2})/);if(!m)return String(value);const d=new Date(Date.UTC(+m[1],+m[2]-1,+m[3]));return new Intl.DateTimeFormat("en-GB",{day:"numeric",month:"long",year:"numeric",timeZone:"UTC"}).format(d)};
  const category=s=>s.story_type||"Reporting",topic=s=>s.topic||"",storyDate=s=>s.date_published||s.date||"";
  const categoryURL=s=>`${root()}archive.html?type=${encodeURIComponent(category(s))}`,topicURL=s=>`${root()}archive.html?topic=${encodeURIComponent(topic(s))}`;
  const excerpt=(t,max=190)=>{const v=String(t||"").trim();return v.length>max?v.slice(0,max).trimEnd()+"…":v};
  async function json(path){const r=await fetch(`${root()}${path}`,{cache:"no-store"});if(!r.ok)throw new Error(`${path}: ${r.status}`);return r.json()}
  async function optionalJson(path,fallback={}){try{return await json(path)}catch{return fallback}}
  async function loadConfig(){return json("data/site_config.json")}
  async function load(){const[data,config,enhancements]=await Promise.all([json("data/archive-index.json"),loadConfig(),optionalJson("data/story_enhancements.json",{})]);const articles=(data.articles||[]).filter(a=>a.verified_author===true&&a.local_url&&Number(a.published_sort||0)>0).sort((a,b)=>Number(b.published_sort||0)-Number(a.published_sort||0));return{data,config,enhancements,articles}}
  function setMenu(state){const open=document.querySelector('[data-menu-toggle]'),nav=document.querySelector('[data-mobile-nav]');if(!nav)return;nav.hidden=!state;open?.setAttribute('aria-expanded',String(state));document.documentElement.classList.toggle('menu-open',state);document.body.style.overflow=state?'hidden':'';if(state)nav.querySelector('a,button')?.focus()}
  function initNav(){const open=document.querySelector('[data-menu-toggle]'),close=document.querySelector('[data-menu-close]'),nav=document.querySelector('[data-mobile-nav]');if(!open||!nav)return;open.addEventListener('click',()=>setMenu(true));close?.addEventListener('click',()=>setMenu(false));nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>setMenu(false)));addEventListener('keydown',e=>{if(e.key==='Escape')setMenu(false)})}
  function initPageMotion(){if(matchMedia('(prefers-reduced-motion: reduce)').matches)return;document.querySelectorAll('[data-reveal]').forEach((el,i)=>{el.style.setProperty('--reveal-delay',`${Math.min(i*55,330)}ms`)});const io=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('is-visible');io.unobserve(e.target)}}),{threshold:.08});document.querySelectorAll('[data-reveal]').forEach(el=>io.observe(el))}
  async function initAnalytics(){try{const c=await loadConfig(),a=c.analytics||{};if(a.provider!=="goatcounter"||!a.site_code)return;const s=document.createElement('script');s.async=true;s.src='https://gc.zgo.at/count.js';s.dataset.goatcounter=`https://${a.site_code}.goatcounter.com/count`;document.head.appendChild(s)}catch(_){}}
  document.addEventListener('DOMContentLoaded',()=>{initNav();initPageMotion();initAnalytics()});
  return{root,esc,fmtDate,category,topic,storyDate,categoryURL,topicURL,excerpt,load,loadConfig,json,optionalJson};
})();
