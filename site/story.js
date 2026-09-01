(() => {
  const sourceURL = document.body.dataset.sourceUrl || "";
  const wordCount = Number(document.body.dataset.wordCount || 0);

  function shareURL(platform) {
    const url = encodeURIComponent(location.href), title = encodeURIComponent(document.title.replace(/ — Arafat Rahaman$/, ""));
    if (platform === "facebook") return `https://www.facebook.com/sharer/sharer.php?u=${url}`;
    if (platform === "x") return `https://twitter.com/intent/tweet?url=${url}&text=${title}`;
    if (platform === "linkedin") return `https://www.linkedin.com/sharing/share-offsite/?url=${url}`;
    if (platform === "whatsapp") return `https://wa.me/?text=${title}%20${url}`;
    return "";
  }

  function initShare() {
    document.querySelectorAll("[data-share]").forEach(btn => btn.addEventListener("click", async () => {
      const type = btn.dataset.share;
      if (type === "copy") {
        try { await navigator.clipboard.writeText(location.href); btn.dataset.old = btn.textContent; btn.textContent = "Copied"; setTimeout(()=>btn.textContent=btn.dataset.old||"Copy",1400); }
        catch { prompt("Copy this link:", location.href); }
        return;
      }
      const url = shareURL(type); if (url) window.open(url, "_blank", "noopener,noreferrer,width=720,height=620");
    }));
    document.querySelectorAll("[data-print]").forEach(btn => btn.addEventListener("click",()=>window.print()));
  }


  function initMobileShare() {
    const bar = document.querySelector(".mobile-share-bar");
    if (!bar) return;
    const update = () => {
      const mobile = matchMedia("(max-width: 760px)").matches;
      const footer = document.querySelector(".site-footer");
      const nearFooter = footer && footer.getBoundingClientRect().top < innerHeight + 80;
      bar.hidden = !mobile || scrollY < 420 || nearFooter;
    };
    addEventListener("scroll", update, {passive:true}); addEventListener("resize", update); update();
  }

  function initProgress() {
    if (wordCount < 1100) return;
    const bar = document.querySelector("#reading-progress"); if (!bar) return;
    bar.hidden = false;
    const update = () => {
      const article = document.querySelector(".story-prose"); if (!article) return;
      const rect = article.getBoundingClientRect(), start = scrollY + rect.top, height = article.offsetHeight - innerHeight * .45;
      const p = Math.max(0, Math.min(1, (scrollY - start + 120) / Math.max(1,height)));
      bar.firstElementChild.style.transform = `scaleX(${p})`;
    };
    addEventListener("scroll", update, {passive:true}); update();
  }

  function tableToCSV(table) {
    return [...table.rows].map(row => [...row.cells].map(cell => `"${cell.innerText.replaceAll('"','""').trim()}"`).join(",")).join("\n");
  }

  function enhanceTables() {
    document.querySelectorAll(".story-prose table").forEach((table, index) => {
      if (table.closest(".interactive-table")) return;
      const wrapper=document.createElement("section"); wrapper.className="interactive-table"; wrapper.setAttribute("aria-label",`Interactive data table ${index+1}`);
      table.parentNode.insertBefore(wrapper, table); wrapper.appendChild(table);
      const controls=document.createElement("div"); controls.className="table-tools";
      controls.innerHTML=`<label><span class="sr-only">Search this table</span><input type="search" placeholder="Search table"></label><button type="button" data-csv>Download CSV</button>`;
      wrapper.insertBefore(controls, table);
      const search=controls.querySelector("input"); search.addEventListener("input",()=>{const q=search.value.trim().toLowerCase(); [...table.tBodies].flatMap(b=>[...b.rows]).forEach(row=>row.hidden=q && !row.innerText.toLowerCase().includes(q));});
      controls.querySelector("[data-csv]").addEventListener("click",()=>{const blob=new Blob([tableToCSV(table)],{type:"text/csv;charset=utf-8"}); const a=document.createElement("a"); a.href=URL.createObjectURL(blob); a.download=`arafat-rahaman-data-${index+1}.csv`; a.click(); setTimeout(()=>URL.revokeObjectURL(a.href),1000);});
      const head=table.tHead?.rows?.[0];
      if (head) [...head.cells].forEach((cell,col)=>{cell.tabIndex=0; cell.setAttribute("role","button"); cell.setAttribute("aria-label",`Sort by ${cell.innerText.trim()}`); let asc=true; const sort=()=>{const body=table.tBodies[0]; if(!body)return; const rows=[...body.rows]; rows.sort((a,b)=>{const av=a.cells[col]?.innerText.trim()||"", bv=b.cells[col]?.innerText.trim()||""; const an=Number(av.replace(/[^0-9.-]/g,"")), bn=Number(bv.replace(/[^0-9.-]/g,"")); const cmp=Number.isFinite(an)&&Number.isFinite(bn)&&av.match(/\d/)&&bv.match(/\d/)?an-bn:av.localeCompare(bv,undefined,{numeric:true}); return asc?cmp:-cmp;}); rows.forEach(r=>body.appendChild(r)); asc=!asc;}; cell.addEventListener("click",sort); cell.addEventListener("keydown",e=>{if(e.key==="Enter"||e.key===" "){e.preventDefault();sort();}});});
    });
  }

  function renderInlineModule(mod) {
    if (mod.type === "pullquote") return `<aside class="inline-pullquote"><span aria-hidden="true">“</span><blockquote>${AR.esc(mod.text||"")}</blockquote>${mod.attribution?`<cite>${AR.esc(mod.attribution)}</cite>`:""}</aside>`;
    if (mod.type === "explainer") return `<aside class="inline-explainer"><p class="module-kicker">${AR.esc(mod.eyebrow||"CONTEXT")}</p><h3>${AR.esc(mod.title||"At a glance")}</h3><div>${(mod.items||[]).map(x=>`<p><strong>${AR.esc(x.label||"")}</strong> ${AR.esc(x.text||"")}</p>`).join("")}</div></aside>`;
    if (mod.type === "timeline") return `<section class="inline-module"><p class="module-kicker">TIMELINE</p><h3>${AR.esc(mod.title||"Timeline")}</h3><ol class="story-timeline">${(mod.items||[]).map(x=>`<li><time>${AR.esc(x.date||"")}</time><div><strong>${AR.esc(x.title||"")}</strong><p>${AR.esc(x.text||"")}</p></div></li>`).join("")}</ol></section>`;
    if (mod.type === "chart") { const vals=mod.values||[], max=Math.max(1,...vals.map(v=>Number(v.value)||0)); return `<section class="inline-module"><p class="module-kicker">DATA</p><h3>${AR.esc(mod.title||"Comparison")}</h3><div class="story-bars">${vals.map(v=>`<div><span>${AR.esc(v.label||"")}</span><i><b style="width:${Math.max(2,(Number(v.value)||0)/max*100)}%"></b></i><strong>${AR.esc(v.display??v.value)}</strong></div>`).join("")}</div>${mod.source?`<p class="module-source">${AR.esc(mod.source)}</p>`:""}</section>`; }
    if (mod.type === "table") { const cols=mod.columns||[], rows=mod.rows||[]; return `<section class="inline-module"><p class="module-kicker">DATA</p><h3>${AR.esc(mod.title||"Data table")}</h3><table><thead><tr>${cols.map(c=>`<th>${AR.esc(c)}</th>`).join("")}</tr></thead><tbody>${rows.map(r=>`<tr>${r.map(c=>`<td>${AR.esc(c)}</td>`).join("")}</tr>`).join("")}</tbody></table>${mod.source?`<p class="module-source">${AR.esc(mod.source)}</p>`:""}</section>`; }
    if (mod.type === "map" && mod.embed_url) return `<section class="inline-module"><p class="module-kicker">MAP</p><h3>${AR.esc(mod.title||"Locations")}</h3><iframe class="story-map" src="${AR.esc(mod.embed_url)}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="${AR.esc(mod.title||"Story map")}"></iframe>${mod.note?`<p class="module-source">${AR.esc(mod.note)}</p>`:""}</section>`;
    return "";
  }

  async function enhancements() {
    try {
      const data=await AR.json("data/story_enhancements.json"), e=data[sourceURL]||{};
      const prose=document.querySelector(".story-prose");
      const paragraphs=[...prose.querySelectorAll(":scope > p")];
      (e.inline||[]).sort((a,b)=>(b.after_paragraph||0)-(a.after_paragraph||0)).forEach(mod=>{const html=renderInlineModule(mod); if(!html)return; const wrap=document.createElement("div"); wrap.innerHTML=html; const node=wrap.firstElementChild; const n=Math.max(1,Math.min(paragraphs.length,Number(mod.after_paragraph)||3)); paragraphs[n-1]?.insertAdjacentElement("afterend",node);});
      const docs=e.documents||[]; const host=document.querySelector("#evidence-card");
      if(host&&docs.length){host.hidden=false; host.querySelector(".evidence-links").innerHTML=docs.map(d=>`<a href="${AR.esc(d.url)}" target="_blank" rel="noopener"><span>${AR.esc(d.label||"Document")}</span><b>↗</b></a>`).join("");}
      enhanceTables();
    } catch(e) { enhanceTables(); }
  }

  async function relatedAndNavigation() {
    try {
      const {articles}=await AR.load(); const idx=articles.findIndex(a=>a.url===sourceURL); if(idx<0)return; const current=articles[idx];
      const related=articles.filter(a=>a.url!==sourceURL).map(a=>({a,score:(AR.topic(a)===AR.topic(current)?7:0)+(AR.category(a)===AR.category(current)?2:0)})).filter(x=>x.score>0).sort((x,y)=>y.score-x.score||Number(y.a.published_sort||0)-Number(x.a.published_sort||0)).slice(0,3).map(x=>x.a);
      const host=document.querySelector("#related-stories"); if(host&&related.length) host.innerHTML=`<div class="section-heading small"><p>RELATED</p><h2>More on this subject</h2></div><div class="related-grid">${related.map(a=>`<article><div class="story-meta-line"><a href="${AR.topicURL(a)}">${AR.esc(AR.topic(a))}</a><time>${AR.esc(AR.fmtDate(AR.storyDate(a)))}</time></div><h3><a href="${AR.root()}${AR.esc(a.local_url)}">${AR.esc(a.title)}</a></h3></article>`).join("")}</div>`;
      const nav=document.querySelector("#story-sequence"); if(nav){const newer=idx>0?articles[idx-1]:null, older=idx<articles.length-1?articles[idx+1]:null; nav.innerHTML=`${newer?`<a href="${AR.root()}${AR.esc(newer.local_url)}"><span>Newer</span><strong>${AR.esc(newer.title)}</strong></a>`:"<span></span>"}${older?`<a class="next" href="${AR.root()}${AR.esc(older.local_url)}"><span>Older</span><strong>${AR.esc(older.title)}</strong></a>`:""}`;}
    } catch(e){console.error(e)}
  }

  initShare(); initMobileShare(); initProgress(); enhancements(); relatedAndNavigation();
})();
