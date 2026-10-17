(()=>{'use strict';
const root=document.body.dataset.root||'';
const css=`
.discovery{margin:0 0 34px;padding:24px;border:1px solid var(--line);background:var(--surface)}
.discovery-head{display:grid;grid-template-columns:minmax(0,1fr) minmax(280px,.9fr);gap:32px;align-items:end;padding-bottom:20px;border-bottom:1px solid var(--line)}
.discovery-head h2{margin:5px 0 0;font:700 clamp(31px,3.6vw,43px)/1 var(--serif);letter-spacing:-.035em}
.discovery-head p{margin:0;color:var(--muted);font-size:13px;line-height:1.55}
.discovery-switch{display:inline-flex;margin:18px 0;border:1px solid var(--line);background:var(--paper)}
.discovery-switch button{min-height:42px;padding:9px 16px;border:0;background:transparent;color:var(--muted);font-size:12px;font-weight:800;cursor:pointer}
.discovery-switch button+button{border-left:1px solid var(--line)}
.discovery-switch button[aria-pressed="true"]{color:#fff;background:var(--forest)}
.discovery-panel{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0;border-top:1px solid var(--line);border-left:1px solid var(--line)}
.selected-story{display:flex;min-height:205px;flex-direction:column;padding:19px;border-right:1px solid var(--line);border-bottom:1px solid var(--line);background:var(--paper)}
.selected-story-meta{display:flex;justify-content:space-between;gap:12px;color:var(--muted);font-size:10px;text-transform:uppercase;letter-spacing:.06em}
.selected-story-meta span{color:var(--accent);font-weight:850}
.selected-story h3{margin:12px 0 0;font:700 clamp(21px,2vw,27px)/1.08 var(--serif);letter-spacing:-.025em}
.selected-story h3 a{text-decoration:none}
.selected-story h3 a:hover{text-decoration:underline}
.selected-story p{display:-webkit-box;overflow:hidden;margin:9px 0 16px;color:var(--muted);font-size:12px;line-height:1.5;-webkit-line-clamp:3;-webkit-box-orient:vertical}
.selected-story-link{margin-top:auto;color:var(--accent);font-size:11px;font-weight:850;text-decoration:none}
.topic-links{grid-template-columns:repeat(2,minmax(0,1fr))}
.topic-links>a{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:14px;align-items:center;min-height:68px;padding:14px 16px;border-right:1px solid var(--line);border-bottom:1px solid var(--line);background:var(--paper);text-decoration:none}
.topic-links>a:hover{background:var(--surface)}
.topic-links span{font:700 17px/1.2 var(--serif)}
.topic-links strong{color:var(--accent);font-size:11px}
.topic-all{color:var(--accent)}
.reporting-topics{margin:-4px 0 22px;padding:16px 0 20px;border-bottom:1px solid var(--line)}
.reporting-topics-head{display:flex;align-items:center;justify-content:space-between;gap:20px;margin-bottom:12px}
.reporting-topics-head>a{color:var(--accent);font-size:11px;font-weight:850;text-decoration:none}
.reporting-topics-head>a[aria-current="page"]{text-decoration:underline}
.reporting-topic-links{display:flex;flex-wrap:wrap;gap:7px}
.reporting-topic-links>a{display:flex;gap:9px;align-items:center;padding:7px 10px;border:1px solid var(--line);background:var(--surface);font-size:12px;text-decoration:none}
.reporting-topic-links>a:hover,.reporting-topic-links>a[aria-current="page"]{border-color:var(--forest);color:#fff;background:var(--forest)}
.reporting-topic-links strong{color:var(--accent);font-size:9px}
.reporting-topic-links>a[aria-current="page"] strong,.reporting-topic-links>a:hover strong{color:#fff}
html[data-theme="dark"] .discovery-switch,html[data-theme="dark"] .selected-story,html[data-theme="dark"] .topic-links>a{background:var(--surface)}
@media(max-width:800px){
 .discovery{margin-bottom:28px;padding:18px}
 .discovery-head{grid-template-columns:1fr;gap:10px}
 .discovery-head p{font-size:12px}
 .discovery-panel{grid-template-columns:1fr}
 .topic-links{grid-template-columns:1fr 1fr}
 .selected-story{min-height:0}
 .reporting-topics{margin-top:-2px}
 .reporting-topic-links{flex-wrap:nowrap;overflow-x:auto;padding-bottom:4px;scrollbar-width:thin}
 .reporting-topic-links>a{flex:0 0 auto;white-space:nowrap}
}
@media(max-width:460px){
 .discovery{margin-inline:-2px;padding:16px}
 .discovery-head h2{font-size:31px}
 .discovery-switch{display:grid;grid-template-columns:1fr 1fr;width:100%}
 .topic-links{grid-template-columns:1fr}
}
`;
const style=document.createElement('style');style.dataset.discoveryStyles='17.2';style.textContent=css;document.head.append(style);
const html=value=>String(value||'').replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
const formatDate=value=>{if(!value)return'';const d=new Date(value);return Number.isNaN(+d)?'':d.toLocaleDateString('en-GB',{day:'numeric',month:'short',year:'numeric',timeZone:'Asia/Dhaka'})};
const safeUrl=value=>/^(stories|thoughts)\/[a-zA-Z0-9_-]+\/$/.test(value||'')?root+value:root+'reporting/';

function topicCounts(articles){
 const counts=new Map();
 articles.filter(article=>article.stream==='reporting'&&article.credit_type==='byline'&&article.category).forEach(article=>counts.set(article.category,(counts.get(article.category)||0)+1));
 return [...counts.entries()].sort((a,b)=>b[1]-a[1]||a[0].localeCompare(b[0]));
}

function selectedStories(articles,limit=4){
 const pool=articles.filter(article=>article.credit_type==='byline'&&(article.stream==='reporting'||article.stream==='opinion'));
 const selected=[],seenCategories=new Set();
 for(const article of pool){
  const key=article.category||article.stream;
  if(seenCategories.has(key))continue;
  selected.push(article);seenCategories.add(key);
  if(selected.length===limit)break;
 }
 if(selected.length<limit){
  for(const article of pool){
   if(selected.includes(article))continue;
   selected.push(article);
   if(selected.length===limit)break;
  }
 }
 return selected;
}

function buildHomeDiscovery(articles){
 const home=document.querySelector('.homecontent'),intro=home?.querySelector('.homeintro');
 if(!home||!intro)return;
 const selected=selectedStories(articles),topics=topicCounts(articles).slice(0,10);
 if(!selected.length&&!topics.length)return;
 const section=document.createElement('section');
 section.className='discovery';section.setAttribute('aria-labelledby','discovery-title');
 const selectedMarkup=selected.map(article=>`<article class="selected-story"><div class="selected-story-meta"><span>${html(article.category||article.stream)}</span><time datetime="${html(article.date_published)}">${html(formatDate(article.date_published))}</time></div><h3><a href="${html(safeUrl(article.local_url))}">${html(article.title)}</a></h3><p>${html(article.excerpt)}</p><a class="selected-story-link" href="${html(safeUrl(article.local_url))}">Read story →</a></article>`).join('');
 const topicMarkup=topics.map(([topic,count])=>`<a href="${html(root+'reporting/?category='+encodeURIComponent(topic))}"><span>${html(topic)}</span><strong>${count}</strong></a>`).join('');
 section.innerHTML=`<div class="discovery-head"><div><span class="eyebrow">Start here</span><h2 id="discovery-title">Find the work that matters</h2></div><p>Move between a compact selection of recent bylined work and the subjects that define the reporting archive.</p></div><div class="discovery-switch" role="group" aria-label="Choose how to browse"><button type="button" data-discovery-mode="selected" aria-pressed="true" aria-controls="discovery-selected">Selected work</button><button type="button" data-discovery-mode="topics" aria-pressed="false" aria-controls="discovery-topics">Topics</button></div><div class="discovery-panel" id="discovery-selected">${selectedMarkup||'<p class="empty">No selected work is available yet.</p>'}</div><div class="discovery-panel topic-links" id="discovery-topics" hidden>${topicMarkup}<a class="topic-all" href="${html(root+'reporting/')}"><span>All reporting</span><strong>→</strong></a></div>`;
 intro.insertAdjacentElement('afterend',section);
 const buttons=[...section.querySelectorAll('[data-discovery-mode]')],panels={selected:section.querySelector('#discovery-selected'),topics:section.querySelector('#discovery-topics')};
 buttons.forEach(button=>button.addEventListener('click',()=>{
  const mode=button.dataset.discoveryMode;
  buttons.forEach(item=>item.setAttribute('aria-pressed',String(item===button)));
  Object.entries(panels).forEach(([key,panel])=>panel.hidden=key!==mode);
 }));
}

function buildReportingTopics(articles){
 const archive=document.querySelector('[data-archive="reporting"]'),intro=archive?.querySelector('.pageintro');
 if(!archive||!intro)return;
 const topics=topicCounts(articles).slice(0,10);if(!topics.length)return;
 const active=new URLSearchParams(location.search).get('category')||'';
 const nav=document.createElement('nav');nav.className='reporting-topics';nav.setAttribute('aria-label','Browse reporting by topic');
 const allClass=active?'':' aria-current="page"';
 nav.innerHTML=`<div class="reporting-topics-head"><span class="eyebrow">Browse by topic</span><a href="${html(root+'reporting/')}"${allClass}>All reporting</a></div><div class="reporting-topic-links">${topics.map(([topic,count])=>`<a href="${html(root+'reporting/?category='+encodeURIComponent(topic))}"${active===topic?' aria-current="page"':''}><span>${html(topic)}</span><strong>${count}</strong></a>`).join('')}</div>`;
 intro.insertAdjacentElement('afterend',nav);
}

(async()=>{
 if(!document.body.classList.contains('home')&&!document.querySelector('[data-archive="reporting"]'))return;
 try{
  const response=await fetch(root+'data/index.json');if(!response.ok)return;
  const data=await response.json(),articles=Array.isArray(data.articles)?data.articles:[];
  buildHomeDiscovery(articles);buildReportingTopics(articles);
 }catch(error){/* The core portfolio remains fully usable if discovery cannot load. */}
})();
})();
