(()=>{'use strict';
const root=document.body.dataset.root||'';
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
