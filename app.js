(() => {
  const grid = document.querySelector("#story-grid");
  const featuredSlot = document.querySelector("#featured");
  const filters = document.querySelector("#filters");
  const searchInput = document.querySelector("#search-input");
  const emptyState = document.querySelector("#empty-state");

  let articles = [];
  let activeSection = "All";

  const esc = (value = "") => String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");

  const prettyDate = (dateString) => {
    if (!dateString) return "";
    const d = new Date(dateString + (dateString.length === 10 ? "T00:00:00Z" : ""));
    if (Number.isNaN(d.getTime())) return dateString;
    return new Intl.DateTimeFormat("en-GB", {
      day: "numeric", month: "short", year: "numeric", timeZone: "UTC"
    }).format(d);
  };

  const monthYear = (dateString) => {
    if (!dateString) return "—";
    const d = new Date(dateString + (dateString.length === 10 ? "T00:00:00Z" : ""));
    if (Number.isNaN(d.getTime())) return "—";
    return new Intl.DateTimeFormat("en-GB", {
      month: "short", year: "numeric", timeZone: "UTC"
    }).format(d);
  };

  function storyLink(article) {
    const href = article.local_url || article.url || "#";
    const external = !article.local_url;
    return {
      href,
      attrs: external ? ' target="_blank" rel="noopener"' : ""
    };
  }

  function renderFilters() {
    const sections = ["All", ...new Set(articles.map(a => a.section || "Other"))];
    filters.innerHTML = sections.map(section =>
      `<button type="button" class="filter-btn ${section === activeSection ? "active" : ""}" data-section="${esc(section)}">${esc(section)}</button>`
    ).join("");

    filters.querySelectorAll("button").forEach(btn => {
      btn.addEventListener("click", () => {
        activeSection = btn.dataset.section;
        renderFilters();
        renderStories();
      });
    });
  }

  function matches(article) {
    const q = searchInput.value.trim().toLowerCase();
    const sectionOk = activeSection === "All" || (article.section || "Other") === activeSection;
    if (!sectionOk) return false;
    if (!q) return true;
    return [article.title, article.excerpt, article.section, ...(article.authors || [])]
      .some(v => String(v || "").toLowerCase().includes(q));
  }

  function renderFeatured(article) {
    if (!article) {
      featuredSlot.innerHTML = "";
      return;
    }
    const link = storyLink(article);
    featuredSlot.innerHTML = `
      <a class="featured-card" href="${esc(link.href)}"${link.attrs}>
        <div class="featured-number">01</div>
        <div>
          <div class="story-meta">
            <span>${esc(article.section || "Reporting")}</span>
            ${article.date ? `<span>•</span><time>${esc(prettyDate(article.date))}</time>` : ""}
          </div>
          <h3>${esc(article.title)}</h3>
          ${article.excerpt ? `<p>${esc(article.excerpt)}</p>` : ""}
        </div>
        <div class="read-arrow" aria-hidden="true">→</div>
      </a>`;
  }

  function renderStories() {
    const visible = articles.filter(matches);
    const featured = activeSection === "All" && !searchInput.value.trim() ? visible[0] : null;
    renderFeatured(featured);

    const rest = featured ? visible.slice(1) : visible;
    grid.innerHTML = rest.map((article) => {
      const link = storyLink(article);
      return `
        <a class="story-card" href="${esc(link.href)}"${link.attrs}>
          <div class="story-meta">
            <span>${esc(article.section || "Reporting")}</span>
            ${article.date ? `<span>•</span><time>${esc(prettyDate(article.date))}</time>` : ""}
          </div>
          <h3>${esc(article.title)}</h3>
          ${article.excerpt ? `<p>${esc(article.excerpt)}</p>` : ""}
          <div class="card-footer">
            <span>${article.local_url ? "Read story" : "Original story"}</span>
            <span class="arrow" aria-hidden="true">↗</span>
          </div>
        </a>
      `;
    }).join("");

    emptyState.hidden = visible.length !== 0;
  }

  async function init() {
    try {
      const response = await fetch("data/articles.json", { cache: "no-store" });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const payload = await response.json();
      articles = Array.isArray(payload.articles) ? payload.articles : [];
      articles.sort((a, b) => String(b.date || "").localeCompare(String(a.date || "")));

      const sections = new Set(articles.map(a => a.section || "Other"));
      document.querySelector("#stat-count").textContent = articles.length;
      document.querySelector("#stat-sections").textContent = sections.size;
      document.querySelector("#stat-latest").textContent =
        articles.length ? monthYear(articles[0].date) : "—";

      if (payload.updated_at) {
        const updated = new Date(payload.updated_at);
        if (!Number.isNaN(updated.getTime())) {
          document.querySelector("#last-updated").textContent =
            "UPDATED " + new Intl.DateTimeFormat("en-GB", {
              day:"numeric", month:"short", year:"numeric", timeZone:"UTC"
            }).format(updated).toUpperCase();
        }
      }

      renderFilters();
      renderStories();
      searchInput.addEventListener("input", renderStories);
    } catch (err) {
      grid.innerHTML = `<p class="empty-state">The archive could not be loaded. Please use the Daily Star author-page link above.</p>`;
      console.error(err);
    }
  }

  init();
})();
