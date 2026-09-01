(() => {
  const grid = document.querySelector("#archive-grid");
  const filters = document.querySelector("#archive-filters");
  const search = document.querySelector("#archive-search");
  const resultsCount = document.querySelector("#results-count");
  const empty = document.querySelector("#archive-empty");
  const pagination = document.querySelector("#pagination");
  const clearBtn = document.querySelector("#clear-filters");

  const PER_PAGE = 18;
  let articles = [];
  let activeSection = "All";
  let currentPage = 1;

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

  function filtered() {
    const q = search.value.trim().toLowerCase();
    return articles.filter(a => {
      const sectionOk = activeSection === "All" || (a.section || "Other") === activeSection;
      if (!sectionOk) return false;
      if (!q) return true;
      return [a.title, a.excerpt, a.section, ...(a.authors || [])]
        .some(v => String(v || "").toLowerCase().includes(q));
    });
  }

  function renderFilters() {
    const counts = new Map();
    articles.forEach(a => {
      const s = a.section || "Other";
      counts.set(s, (counts.get(s) || 0) + 1);
    });
    const sections = [...counts.keys()].sort((a, b) => a.localeCompare(b));
    const buttons = ["All", ...sections];

    filters.innerHTML = buttons.map(s => {
      const count = s === "All" ? articles.length : counts.get(s);
      return `<button type="button" class="archive-filter ${s === activeSection ? "active" : ""}" data-section="${esc(s)}"><span>${esc(s)}</span><small>${count}</small></button>`;
    }).join("");

    filters.querySelectorAll("button").forEach(btn => {
      btn.addEventListener("click", () => {
        activeSection = btn.dataset.section;
        currentPage = 1;
        updateUrl();
        renderFilters();
        render();
      });
    });
  }

  function updateUrl() {
    const url = new URL(window.location.href);
    if (activeSection === "All") url.searchParams.delete("section");
    else url.searchParams.set("section", activeSection);
    if (search.value.trim()) url.searchParams.set("q", search.value.trim());
    else url.searchParams.delete("q");
    history.replaceState(null, "", url);
  }

  function renderPagination(totalPages) {
    if (totalPages <= 1) {
      pagination.innerHTML = "";
      return;
    }

    const start = Math.max(1, currentPage - 2);
    const end = Math.min(totalPages, currentPage + 2);
    const items = [];

    items.push(`<button type="button" ${currentPage === 1 ? "disabled" : ""} data-page="${currentPage - 1}" aria-label="Previous page">←</button>`);
    if (start > 1) {
      items.push(`<button type="button" data-page="1">1</button>`);
      if (start > 2) items.push(`<span>…</span>`);
    }
    for (let i = start; i <= end; i++) {
      items.push(`<button type="button" class="${i === currentPage ? "active" : ""}" data-page="${i}" ${i === currentPage ? 'aria-current="page"' : ""}>${i}</button>`);
    }
    if (end < totalPages) {
      if (end < totalPages - 1) items.push(`<span>…</span>`);
      items.push(`<button type="button" data-page="${totalPages}">${totalPages}</button>`);
    }
    items.push(`<button type="button" ${currentPage === totalPages ? "disabled" : ""} data-page="${currentPage + 1}" aria-label="Next page">→</button>`);

    pagination.innerHTML = items.join("");
    pagination.querySelectorAll("button[data-page]").forEach(btn => {
      btn.addEventListener("click", () => {
        const p = Number(btn.dataset.page);
        if (!Number.isFinite(p) || p < 1 || p > totalPages || p === currentPage) return;
        currentPage = p;
        render();
        document.querySelector(".archive-results").scrollIntoView({ behavior: "smooth", block: "start" });
      });
    });
  }

  function render() {
    const list = filtered();
    const totalPages = Math.max(1, Math.ceil(list.length / PER_PAGE));
    currentPage = Math.min(currentPage, totalPages);

    const start = (currentPage - 1) * PER_PAGE;
    const visible = list.slice(start, start + PER_PAGE);

    resultsCount.textContent = `${list.length} ${list.length === 1 ? "story" : "stories"}${activeSection !== "All" ? ` · ${activeSection}` : ""}`;
    clearBtn.hidden = activeSection === "All" && !search.value.trim();
    empty.hidden = list.length !== 0;

    grid.innerHTML = visible.map(a => `
      <a class="archive-card" href="${esc(storyHref(a))}"${externalAttrs(a)}>
        <div class="archive-card-top">
          <div class="story-meta">
            <span>${esc(a.section || "Reporting")}</span>
            ${a.date ? `<span>•</span><time>${esc(fmtDate(a.date))}</time>` : ""}
          </div>
          <span class="archive-card-arrow">↗</span>
        </div>
        <h2>${esc(a.title)}</h2>
        ${a.excerpt ? `<p>${esc(a.excerpt)}</p>` : ""}
        <span class="archive-read">${a.local_url ? "Read in portfolio" : "Original story"}</span>
      </a>
    `).join("");

    renderPagination(list.length ? Math.ceil(list.length / PER_PAGE) : 0);
  }

  function setTopMeta() {
    document.querySelector("#archive-total").textContent = articles.length;
    const dated = articles.filter(a => /^\d{4}-\d{2}-\d{2}$/.test(a.date || ""));
    const years = dated.map(a => Number(a.date.slice(0, 4))).filter(Number.isFinite);
    document.querySelector("#archive-range").textContent = years.length
      ? `${Math.min(...years)}–${Math.max(...years)}`
      : "Reporting archive";
  }

  async function init() {
    try {
      const r = await fetch("data/articles.json", { cache: "no-store" });
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      const payload = await r.json();
      articles = Array.isArray(payload.articles) ? payload.articles : [];
      articles.sort((a, b) => String(b.date || "").localeCompare(String(a.date || "")));

      const params = new URLSearchParams(window.location.search);
      const requestedSection = params.get("section");
      const requestedQuery = params.get("q");
      if (requestedSection) activeSection = requestedSection;
      if (requestedQuery) search.value = requestedQuery;

      setTopMeta();
      renderFilters();

      // If URL carries an outdated/non-existent section, fall back cleanly.
      const known = new Set(articles.map(a => a.section || "Other"));
      if (activeSection !== "All" && !known.has(activeSection)) {
        activeSection = "All";
        renderFilters();
      }

      render();

      search.addEventListener("input", () => {
        currentPage = 1;
        updateUrl();
        render();
      });

      clearBtn.addEventListener("click", () => {
        activeSection = "All";
        search.value = "";
        currentPage = 1;
        updateUrl();
        renderFilters();
        render();
      });
    } catch (err) {
      resultsCount.textContent = "Archive unavailable";
      grid.innerHTML = `<p class="archive-empty">The reporting archive could not be loaded.</p>`;
      console.error(err);
    }
  }

  init();
})();
