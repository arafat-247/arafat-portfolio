(() => {
  const latestSlot = document.querySelector("#latest-story");
  const focusGrid = document.querySelector("#focus-grid");
  const leadSlot = document.querySelector("#lead-story");
  const selectedGrid = document.querySelector("#selected-grid");

  const esc = (v = "") => String(v)
    .replaceAll("&", "&amp;").replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;").replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");

  const storyHref = a => a.local_url || a.url || "#";
  const externalAttrs = a => a.local_url ? "" : ' target="_blank" rel="noopener"';

  const fmtDate = value => {
    if (!value) return "";
    const d = new Date(value + (value.length === 10 ? "T00:00:00Z" : ""));
    if (Number.isNaN(d.getTime())) return "";
    return new Intl.DateTimeFormat("en-GB", {
      day: "numeric", month: "short", year: "numeric", timeZone: "UTC"
    }).format(d);
  };

  const fmtMonthYear = value => {
    if (!value) return "—";
    const d = new Date(value + (value.length === 10 ? "T00:00:00Z" : ""));
    if (Number.isNaN(d.getTime())) return "—";
    return new Intl.DateTimeFormat("en-GB", {
      month: "short", year: "numeric", timeZone: "UTC"
    }).format(d);
  };

  function latestStory(a) {
    if (!a) return;
    latestSlot.innerHTML = `
      <a class="latest-link" href="${esc(storyHref(a))}"${externalAttrs(a)}>
        <div class="latest-meta"><span>${esc(a.section || "Reporting")}</span>${a.date ? `<span>·</span><time>${esc(fmtDate(a.date))}</time>` : ""}</div>
        <h2>${esc(a.title)}</h2>
        ${a.excerpt ? `<p>${esc(a.excerpt)}</p>` : ""}
        <span class="latest-read">Read story <strong>→</strong></span>
      </a>`;
  }

  function focusCards(articles) {
    const counts = new Map();
    articles.forEach(a => {
      const section = a.section || "Other";
      counts.set(section, (counts.get(section) || 0) + 1);
    });

    const top = [...counts.entries()]
      .sort((a, b) => b[1] - a[1])
      .slice(0, 4);

    focusGrid.innerHTML = top.map(([section, count], i) => `
      <a class="focus-card" href="archive.html?section=${encodeURIComponent(section)}">
        <span class="focus-number">0${i + 1}</span>
        <div>
          <h3>${esc(section)}</h3>
          <p>${count} ${count === 1 ? "story" : "stories"} in the archive</p>
        </div>
        <span class="focus-arrow">↗</span>
      </a>
    `).join("");
  }

  function selectedWork(articles) {
    const lead = articles[0];
    const selected = articles.slice(1, 5);

    if (lead) {
      leadSlot.innerHTML = `
        <a class="front-lead" href="${esc(storyHref(lead))}"${externalAttrs(lead)}>
          <div class="front-lead-label">
            <span>FEATURED</span>
            <strong>01</strong>
          </div>
          <div class="front-lead-copy">
            <div class="story-meta">
              <span>${esc(lead.section || "Reporting")}</span>
              ${lead.date ? `<span>•</span><time>${esc(fmtDate(lead.date))}</time>` : ""}
            </div>
            <h3>${esc(lead.title)}</h3>
            ${lead.excerpt ? `<p>${esc(lead.excerpt)}</p>` : ""}
          </div>
          <span class="front-lead-arrow">→</span>
        </a>`;
    }

    selectedGrid.innerHTML = selected.map((a, idx) => `
      <a class="selected-card" href="${esc(storyHref(a))}"${externalAttrs(a)}>
        <div class="selected-card-top">
          <span class="card-index">0${idx + 2}</span>
          <span class="selected-arrow">↗</span>
        </div>
        <div class="story-meta">
          <span>${esc(a.section || "Reporting")}</span>
          ${a.date ? `<span>•</span><time>${esc(fmtDate(a.date))}</time>` : ""}
        </div>
        <h3>${esc(a.title)}</h3>
        ${a.excerpt ? `<p>${esc(a.excerpt)}</p>` : ""}
      </a>
    `).join("");
  }

  function stats(articles) {
    const sections = new Set(articles.map(a => a.section || "Other"));
    const dated = articles.filter(a => /^\d{4}-\d{2}-\d{2}$/.test(a.date || ""));
    const newest = dated[0]?.date || "";
    const oldest = dated[dated.length - 1]?.date || "";
    const newYear = newest ? newest.slice(0, 4) : "";
    const oldYear = oldest ? oldest.slice(0, 4) : "";

    document.querySelector("#stat-count").textContent = articles.length;
    document.querySelector("#stat-sections").textContent = sections.size;
    document.querySelector("#stat-range").textContent =
      oldYear && newYear ? (oldYear === newYear ? newYear : `${oldYear}–${newYear}`) : "Growing";

    document.querySelector("#archive-description").textContent =
      `Search ${articles.length} indexed stories by headline or coverage area, then open each story inside the portfolio.`;
  }

  async function init() {
    try {
      const r = await fetch("data/articles.json", { cache: "no-store" });
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      const payload = await r.json();
      const articles = Array.isArray(payload.articles) ? payload.articles : [];
      articles.sort((a, b) => String(b.date || "").localeCompare(String(a.date || "")));

      latestStory(articles[0]);
      focusCards(articles);
      selectedWork(articles);
      stats(articles);
    } catch (err) {
      latestSlot.innerHTML = `<p class="loading-copy">The latest story could not be loaded. <a href="archive.html">Open the archive →</a></p>`;
      console.error(err);
    }
  }

  init();
})();
