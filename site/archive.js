(() => {
  const PER_PAGE = 20;
  let articles = [], page = 1, activeType = "All", activeTopic = "", activeYear = "", order = "new";

  const input = () => document.querySelector("#archive-search");
  const terms = () => input().value.trim().toLowerCase().split(/\s+/).filter(Boolean);

  function score(story, q) {
    if (!q.length) return 1;
    const fields = {
      title: String(story.title || "").toLowerCase(),
      excerpt: String(story.excerpt || "").toLowerCase(),
      topic: String(AR.topic(story)).toLowerCase(),
      type: String(AR.category(story)).toLowerCase(),
      date: String(AR.storyDate(story)).toLowerCase()
    };
    return q.reduce((sum,t) => sum + (fields.title.includes(t)?10:0) + (fields.topic.includes(t)?6:0) + (fields.type.includes(t)?5:0) + (fields.excerpt.includes(t)?2:0) + (fields.date.includes(t)?1:0), 0);
  }

  function filtered() {
    const q = terms();
    const list = articles.filter(a => activeType === "All" || AR.category(a) === activeType)
      .filter(a => !activeTopic || AR.topic(a) === activeTopic)
      .filter(a => !activeYear || String(AR.storyDate(a)).startsWith(activeYear))
      .map(a => ({a, score:score(a,q)})).filter(x => !q.length || x.score > 0);
    list.sort((x,y) => q.length ? (y.score - x.score || Number(y.a.published_sort||0)-Number(x.a.published_sort||0)) : (order === "new" ? Number(y.a.published_sort||0)-Number(x.a.published_sort||0) : Number(x.a.published_sort||0)-Number(y.a.published_sort||0)));
    return list.map(x=>x.a);
  }

  function meta(story) {
    return `<div class="story-meta-line"><a href="?type=${encodeURIComponent(AR.category(story))}">${AR.esc(AR.category(story))}</a><a href="?topic=${encodeURIComponent(AR.topic(story))}">${AR.esc(AR.topic(story))}</a><time>${AR.esc(AR.fmtDate(AR.storyDate(story)))}</time></div>`;
  }

  function render() {
    const list = filtered(), pages = Math.max(1, Math.ceil(list.length/PER_PAGE)); page = Math.min(page,pages);
    const start = (page-1)*PER_PAGE, visible = list.slice(start,start+PER_PAGE);
    document.querySelector("#result-count").textContent = `${list.length} ${list.length===1?"article":"articles"}`;
    document.querySelector("#archive-results").innerHTML = visible.map((story,i)=>`<article class="archive-item">
      <span class="archive-index">${String(start+i+1).padStart(2,"0")}</span>
      <div class="archive-copy">${meta(story)}<h2><a href="${AR.esc(story.local_url)}">${AR.esc(story.title)}</a></h2>${story.excerpt?`<p>${AR.esc(AR.excerpt(story.excerpt,175))}</p>`:""}</div>
      <a class="archive-arrow" href="${AR.esc(story.local_url)}" aria-label="Read ${AR.esc(story.title)}">↗</a>
    </article>`).join("");
    document.querySelector("#archive-empty").hidden = !!list.length;
    renderPagination(pages); updateURL();
  }

  function renderPagination(pages) {
    const host = document.querySelector("#pagination");
    if (pages <= 1) { host.innerHTML = ""; return; }
    const nums = new Set([1,pages,page-1,page,page+1].filter(n=>n>=1&&n<=pages));
    let last=0, html=`<button ${page===1?"disabled":""} data-page="${page-1}">←</button>`;
    [...nums].sort((a,b)=>a-b).forEach(n=>{ if(last && n-last>1) html += `<span>…</span>`; html += `<button class="${n===page?"active":""}" data-page="${n}">${n}</button>`; last=n; });
    html += `<button ${page===pages?"disabled":""} data-page="${page+1}">→</button>`;
    host.innerHTML=html;
    host.querySelectorAll("button[data-page]").forEach(b=>b.addEventListener("click",()=>{const n=Number(b.dataset.page); if(n<1||n>pages)return; page=n; render(); scrollTo({top:document.querySelector(".archive-controls").offsetTop-90, behavior:"smooth"});}));
  }

  function populateFilters() {
    const topics=[...new Set(articles.map(AR.topic))].sort();
    const years=[...new Set(articles.map(a=>String(AR.storyDate(a)).slice(0,4)).filter(Boolean))].sort().reverse();
    document.querySelector("#topic-filter").innerHTML=`<option value="">All topics</option>`+topics.map(t=>`<option value="${AR.esc(t)}">${AR.esc(t)}</option>`).join("");
    document.querySelector("#year-filter").innerHTML=`<option value="">All years</option>`+years.map(y=>`<option value="${y}">${y}</option>`).join("");
  }

  function readURL() {
    const u=new URL(location.href); activeType=u.searchParams.get("type")||"All"; activeTopic=u.searchParams.get("topic")||""; activeYear=u.searchParams.get("year")||""; order=u.searchParams.get("order")==="old"?"old":"new"; input().value=u.searchParams.get("q")||"";
  }
  function updateURL() {
    const u=new URL(location.href); const q=input().value.trim();
    activeType==="All"?u.searchParams.delete("type"):u.searchParams.set("type",activeType);
    activeTopic?u.searchParams.set("topic",activeTopic):u.searchParams.delete("topic"); activeYear?u.searchParams.set("year",activeYear):u.searchParams.delete("year"); order==="old"?u.searchParams.set("order","old"):u.searchParams.delete("order"); q?u.searchParams.set("q",q):u.searchParams.delete("q"); history.replaceState(null,"",u);
  }

  async function init(){
    ({articles}=await AR.load()); readURL(); populateFilters();
    document.querySelector("#topic-filter").value=activeTopic; document.querySelector("#year-filter").value=activeYear; document.querySelector("#sort-filter").value=order;
    document.querySelectorAll("[data-type]").forEach(b=>{b.classList.toggle("active",b.dataset.type===activeType); b.addEventListener("click",()=>{activeType=b.dataset.type; page=1; document.querySelectorAll("[data-type]").forEach(x=>x.classList.toggle("active",x===b)); render();});});
    input().addEventListener("input",()=>{page=1;render();});
    document.querySelector("#topic-filter").addEventListener("change",e=>{activeTopic=e.target.value;page=1;render();});
    document.querySelector("#year-filter").addEventListener("change",e=>{activeYear=e.target.value;page=1;render();});
    document.querySelector("#sort-filter").addEventListener("change",e=>{order=e.target.value;page=1;render();});
    addEventListener("keydown",e=>{if(e.key==="/"&&!/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)){e.preventDefault();input().focus();}});
    render();
  }
  init().catch(console.error);
})();
