(() => {
  const PER_PAGE = 12;

  const grid = document.querySelector("#archive-grid");
  const filterRow = document.querySelector("#archive-filters");
  const search = document.querySelector("#archive-search");
  const resultCount = document.querySelector("#result-count");
  const clearSearch = document.querySelector("#clear-search");
  const empty = document.querySelector("#archive-empty");
  const pagination = document.querySelector("#pagination");

  let articles = [];
  let activeSection = "All";
  let currentPage = 1;

  const esc = (v = "") => String(v)
    .replaceAll("&", "&amp;").replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;").replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");

  const fmtDate = value => {
    if (!value) return "";
    const d = new Date(value + (value.length === 10 ? "T00:00:00Z" : ""));
    if (Number.isNaN(d.getTime())) return "";
    return new Intl.DateTimeFormat("en-GB", {
      day: "numeric", month: "short", year: "numeric", timeZone: "UTC"
    }).format(d);
  };

  const excerpt = (text, max = 170) => {
    const v = String(text || "").trim();
    return v.length > max ? v.slice(0, max).trimEnd() + "…" : v;
  };

  function matches() {
    const q = search.value.trim().toLowerCase();

    return articles.filter(a => {
      const section = a.section || "Other";
      if (activeSection !== "All" && section !== activeSection) return false;
      if (!q) return true;
      return [a.title, a.excerpt, a.section, ...(a.authors || [])]
        .some(value => String(value || "").toLowerCase().includes(q));
    });
  }

  function renderFilters() {
    const counts = new Map();
    articles.forEach(a => {
      const section = a.section || "Other";
      counts.set(section, (counts.get(section) || 0) + 1);
    });

    const sections = [...counts.keys()].sort((a, b) => a.localeCompare(b));
    const all = ["All", ...sections];

    filterRow.innerHTML = all.map(name => {
      const count = name === "All" ? articles.length : counts.get(name);
      return `<button type="button" class="filter-pill ${name === activeSection ? "active" : ""}" data-section="${esc(name)}">${esc(name)} <small>${count}</small></button>`;
    }).join("");

    filterRow.querySelectorAll("button").forEach(btn => {
      btn.addEventListener("click", () => {
        activeSection = btn.dataset.section;
        currentPage = 1;
        renderFilters();
        updateUrl();
        render();
      });
    });
  }

  function updateUrl() {
    const url = new URL(location.href);
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

    const pages = [];
    pages.push(`<button type="button" data-page="${currentPage - 1}" ${currentPage === 1 ? "disabled" : ""}>←</button>`);

    const start = Math.max(1, currentPage - 2);
    const end = Math.min(totalPages, currentPage + 2);

    if (start > 1) pages.push(`<button type="button" data-page="1">1</button>`);
    if (start > 2) pages.push(`<span>…</span>`);

    for (let p = start; p <= end; p++) {
      pages.push(`<button type="button" data-page="${p}" class="${p === currentPage ? "active" : ""}">${p}</button>`);
    }

    if (end < totalPages - 1) pages.push(`<span>…</span>`);
    if (end < totalPages) pages.push(`<button type="button" data-page="${totalPages}">${totalPages}</button>`);

    pages.push(`<button type="button" data-page="${currentPage + 1}" ${currentPage === totalPages ? "disabled" : ""}>→</button>`);

    pagination.innerHTML = pages.join("");
    pagination.querySelectorAll("button[data-page]").forEach(btn => {
      btn.addEventListener("click", () => {
        const page = Number(btn.dataset.page);
        if (!Number.isFinite(page) || page < 1 || page > totalPages) return;
        currentPage = page;
        render();
        document.querySelector(".archive-list").scrollIntoView({ behavior: "smooth", block: "start" });
      });
    });
  }

  function render() {
    const list = matches();
    const totalPages = Math.max(1, Math.ceil(list.length / PER_PAGE));
    currentPage = Math.min(currentPage, totalPages);

    const start = (currentPage - 1) * PER_PAGE;
    const visible = list.slice(start, start + PER_PAGE);

    resultCount.textContent =
      `${list.length} verified ${list.length === 1 ? "story" : "stories"}${activeSection !== "All" ? ` · ${activeSection}` : ""}`;

    clearSearch.hidden = activeSection === "All" && !search.value.trim();
    empty.hidden = list.length !== 0;

    grid.innerHTML = visible.map((a, index) => `
      <a class="archive-story-card" href="${esc(a.local_url)}">
        <div class="archive-card-number">${String(start + index + 1).padStart(2, "0")}</div>
        <div class="archive-card-content">
          <div class="archive-card-meta">
            <span>${esc(a.section || "Reporting")}</span>
            ${a.date ? `<time>${esc(fmtDate(a.date))}</time>` : ""}
          </div>
          <h2>${esc(a.title)}</h2>
          ${a.excerpt ? `<p>${esc(excerpt(a.excerpt))}</p>` : ""}
          <span class="archive-card-read">Read in portfolio →</span>
        </div>
      </a>
    `).join("");

    renderPagination(list.length ? Math.ceil(list.length / PER_PAGE) : 0);
  }

  function topStats() {
    document.querySelector("#archive-total").textContent = articles.length;

    const years = articles
      .map(a => String(a.date || "").slice(0, 4))
      .filter(y => /^\d{4}$/.test(y))
      .map(Number);

    document.querySelector("#archive-span").textContent = years.length
      ? `${Math.min(...years)}–${Math.max(...years)}`
      : "Archive";
  }

  async function init() {
    try {
      const response = await fetch("data/articles.json", { cache: "no-store" });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const payload = await response.json();

      articles = (Array.isArray(payload.articles) ? payload.articles : [])
        .filter(a => a.verified_author === true && a.local_url)
        .sort((a, b) => String(b.date || "").localeCompare(String(a.date || "")));

      const params = new URLSearchParams(location.search);
      if (params.get("section")) activeSection = params.get("section");
      if (params.get("q")) search.value = params.get("q");

      const known = new Set(articles.map(a => a.section || "Other"));
      if (activeSection !== "All" && !known.has(activeSection)) activeSection = "All";

      topStats();
      renderFilters();
      render();

      search.addEventListener("input", () => {
        currentPage = 1;
        updateUrl();
        render();
      });

      clearSearch.addEventListener("click", () => {
        activeSection = "All";
        search.value = "";
        currentPage = 1;
        updateUrl();
        renderFilters();
        render();
      });
    } catch (error) {
      resultCount.textContent = "Archive unavailable";
      grid.innerHTML = `<div class="loading-card">The verified archive could not be loaded.</div>`;
      console.error(error);
    }
  }

  init();
})();
