(()=>{'use strict';
if(!document.body.classList.contains('home'))return;
const root=document.body.dataset.root||'';
const esc=value=>String(value??'').replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
const date=value=>{if(!value)return'';const d=new Date(value);return Number.isNaN(+d)?'':d.toLocaleDateString('en-GB',{day:'numeric',month:'short',year:'numeric',timeZone:'Asia/Dhaka'})};
const safeUrl=value=>/^(stories|thoughts)\/[a-zA-Z0-9_-]+\/$/.test(value||'')?root+value:root+'reporting/';
const css=document.createElement('link');css.rel='stylesheet';css.href=root+'assets/pro-home.css?v=18.0.0';document.head.append(css);
document.body.classList.add('portfolio-pro');

const profile={
 name:'Arafat Rahaman',
 role:'Journalist at The Daily Star',
 location:'Dhaka, Bangladesh',
 email:'arafat.mcj@yahoo.com',
 bio:'I report on education, governance, rights, social policy and public accountability. My work combines field reporting, interviews, public records, data and visual storytelling, with a focus on how policy decisions affect people and institutions.',
 career:[
  ['2022–present','Staff Reporter','The Daily Star · Dhaka'],
  ['2017–2022','Reporter','The Daily Star · Rajshahi']
 ],
 awards:[
  ['2025','AccessFest Fellowship','Investigative Reporters & Editors'],
  ['2024','Youth of the Year Award','The Daily Star'],
  ['2024','Dhaka Road Traffic Safety Project Fellowship','JICA and Dhaka Metropolitan Police'],
  ['2019','Media Tech Challenge Bootcamp winner','DW Akademie'],
  ['2018','Most Talked About Photograph','The Daily Star']
 ],
 focus:[
  ['01','Education','Schools, universities, access, quality and public policy'],
  ['02','Governance','Institutions, accountability and the exercise of public power'],
  ['03','Rights & justice','Human rights, social justice and civic freedoms'],
  ['04','Youth & politics','Civic movements, political participation and generational change'],
  ['05','Data & investigations','Records, datasets and evidence-led reporting']
 ],
 photos:[
  ['assets/photography/Rajshahi University-nightscape-Journalist-Arafat-Rahaman (6).webp','Rajshahi University by night'],
  ['assets/photography/Rajshahi University-nightscape-Journalist-Arafat-Rahaman (3).webp','Nightscape'],
  ['assets/photography/Rajshahi University-nightscape-Journalist-Arafat-Rahaman (4).webp','After sunset']
 ]
};

function distinctStories(articles){
 const pool=articles.filter(a=>a.credit_type==='byline'&&(a.stream==='reporting'||a.stream==='opinion'));
 const result=[],seen=new Set();
 for(const a of pool){const key=a.category||a.stream;if(seen.has(key))continue;seen.add(key);result.push(a);if(result.length===3)break}
 for(const a of pool){if(result.length===3)break;if(!result.includes(a))result.push(a)}
 return result;
}
function storyCard(article,index){
 return `<a class="pro-story" href="${esc(safeUrl(article.local_url))}"><span class="pro-story-number">0${index+1}</span><div><div class="pro-story-meta"><span>${esc(article.category||article.stream||'Journalism')}</span><span>${esc(date(article.date_published))}</span></div><h3>${esc(article.title)}</h3><p>${esc(article.excerpt||'')}</p></div><div class="pro-story-foot"><span>${esc(article.source_name||'The Daily Star')}</span><span>Read story →</span></div></a>`;
}
function focusCard(item){return `<a class="pro-focus" href="${esc(root+'reporting/?category='+encodeURIComponent(item[1]))}"><b>${esc(item[0])}</b><strong>${esc(item[1])}</strong><span>${esc(item[2])}</span></a>`}
function careerRow(item){return `<div class="pro-career-row"><time>${esc(item[0])}</time><strong>${esc(item[1])}</strong><span>${esc(item[2])}</span></div>`}
function awardCard(item){return `<div class="pro-award"><b>${esc(item[0])}</b><strong>${esc(item[1])}</strong><span>${esc(item[2])}</span></div>`}
function photoCard(item){return `<a class="pro-photo" href="${esc(root+'photography/')}" aria-label="Open photography portfolio"><img src="${esc(root+item[0])}" alt="${esc(item[1])}" loading="lazy" decoding="async"><span>${esc(item[1])}</span></a>`}

async function render(){
 let articles=[];
 try{const response=await fetch(root+'data/index.json');if(response.ok){const data=await response.json();articles=Array.isArray(data.articles)?data.articles:[]}}catch(error){}
 const stories=distinctStories(articles);
 const bylined=articles.filter(a=>a.credit_type==='byline').length;
 const reporting=articles.filter(a=>a.stream==='reporting'&&a.credit_type==='byline').length;
 const opinion=articles.filter(a=>a.stream==='opinion').length;
 const content=document.querySelector('.homecontent');if(!content)return;
 content.innerHTML=`<div class="pro-shell">
  <div class="pro-wrap"><nav class="pro-nav" aria-label="Portfolio navigation"><a class="pro-brand" href="${esc(root+'./')}"><strong>ARAFAT RAHAMAN</strong><span>Journalist · Writer · Researcher</span></a><div class="pro-navlinks"><a href="${esc(root+'reporting/')}">Reporting</a><a href="${esc(root+'opinion/')}">Opinion</a><a href="${esc(root+'photography/')}">Photography</a><a href="${esc(root+'about/')}">About</a><a class="pro-nav-cta" href="${esc(root+'contact/')}">Contact</a></div></nav></div>
  <div class="pro-wrap"><section class="pro-hero" aria-labelledby="pro-home-title"><div class="pro-hero-copy"><div class="pro-hero-eyebrow">Independent portfolio · Bangladesh</div><h1 id="pro-home-title">Arafat Rahaman<span>Journalist.</span></h1><p class="pro-hero-lede">${esc(profile.bio)}</p><div class="pro-hero-actions"><a class="pro-button" href="#signature-work">View signature work →</a><a class="pro-button secondary" href="${esc(root+'about/')}">Profile & experience</a></div><p class="pro-hero-note">Based in ${esc(profile.location)} · Reporting since 2017</p></div><figure class="pro-portrait"><img src="${esc(root+'assets/portraits/home.webp')}" alt="Portrait of Arafat Rahaman" decoding="async"><figcaption class="pro-portrait-caption"><strong>${esc(profile.name)}</strong><span>${esc(profile.role)} · ${esc(profile.location)}</span></figcaption></figure></section></div>
  <section class="pro-proof"><div class="pro-wrap pro-proof-grid"><div class="pro-proof-item"><strong>${bylined||'250+'}</strong><span>Bylined pieces in the portfolio</span></div><div class="pro-proof-item"><strong>Since 2017</strong><span>Reporting professionally</span></div><div class="pro-proof-item"><strong>${reporting||'200+'}</strong><span>Reports and features</span></div><div class="pro-proof-item"><strong>${opinion||'20+'}</strong><span>Opinion and analysis</span></div></div></section>
  <section class="pro-section" id="signature-work"><div class="pro-wrap"><div class="pro-section-head"><div><span class="pro-kicker">Selected journalism</span><h2 class="pro-title">Signature work</h2></div><p>A concise selection from the reporting archive. The full body of work remains searchable by topic, year and credit on the reporting page.</p></div><div class="pro-signature">${stories.length?stories.map(storyCard).join(''):'<p>No selected stories are available yet.</p>'}</div><div style="margin-top:28px"><a class="pro-link" href="${esc(root+'reporting/')}">Browse the complete reporting archive →</a></div></div></section>
  <section class="pro-section"><div class="pro-wrap"><div class="pro-section-head"><div><span class="pro-kicker">Reporting agenda</span><h2 class="pro-title">What I cover</h2></div><p>Recurring subjects rather than a generic news feed: institutions, education, rights, politics and evidence-led public-interest reporting.</p></div><div class="pro-focus-grid">${profile.focus.map(focusCard).join('')}</div></div></section>
  <section class="pro-section"><div class="pro-wrap"><div class="pro-career"><div class="pro-career-intro"><span class="pro-kicker">Professional profile</span><h2 class="pro-title">Newsroom work</h2><p>Reporting from Rajshahi and Dhaka for The Daily Star, with field reporting, interviews, public records, data and photography forming the core of the work.</p><a class="pro-link" href="${esc(root+'about/')}">Read full profile →</a></div><div class="pro-career-list">${profile.career.map(careerRow).join('')}</div></div><div class="pro-recognition"><div class="pro-recognition-head"><div><span class="pro-kicker" style="color:#f0aa94">Recognition</span><h3>Awards & fellowships</h3></div><a href="${esc(root+'about/#recognition')}">Full details →</a></div><div class="pro-awards">${profile.awards.map(awardCard).join('')}</div></div></div></section>
  <section class="pro-section"><div class="pro-wrap"><div class="pro-section-head"><div><span class="pro-kicker">Visual work</span><h2 class="pro-title">Photography</h2></div><p>A separate visual practice documenting public spaces, people and everyday life in Bangladesh.</p></div><div class="pro-visual">${profile.photos.map(photoCard).join('')}</div><div style="margin-top:28px"><a class="pro-link" href="${esc(root+'photography/')}">Open photography portfolio →</a></div></div></section>
  <div class="pro-wrap"><section class="pro-contact"><div><span class="pro-kicker">Contact</span><h2>Story lead, reporting enquiry or professional correspondence?</h2></div><div class="pro-contact-actions"><a class="pro-button" href="mailto:${esc(profile.email)}">Email Arafat →</a><a class="pro-button secondary" href="${esc(root+'contact/')}">Contact details</a></div></section></div>
 </div>`;
}
render();
})();
