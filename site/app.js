(() => {
  const esc = (v = "") => String(v)
    .replaceAll("&", "&amp;").replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;").replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");

  const localHref = a => a.local_url || "#";

  const fmtDate = value => {
    if (!value) return "";
    const d = new Date(value + (value.length === 10 ? "T00:00:00Z" : ""));
    if (Number.isNaN(d.getTime())) return "";
    return new Intl.DateTimeFormat("en-GB", {
      day: "numeric", month: "short", year: "numeric", timeZone: "UTC"
    }).format(d);
  };

  function excerpt(text, max = 180) {
    const value = String(text || "").trim();
    if (!value) return "";
    return value.length > max ? value.slice(0, max).trimEnd() + "…" : value;
  }

  function renderFeatured(articles) {
    const slot = document.querySelector("#featured-layout");
    const picks = articles.slice(0, 5);
    if (!picks.length) {
      slot.innerHTML = `<div class="loading-card">No verified stories are available yet.</div>`;
      return;
    }

    const lead = picks[0];
    const side = picks.slice(1);

    slot.innerHTML = `
      <a class="feature-main" href="${esc(localHref(lead))}">
        <div class="feature-number">01</div>
        <div class="feature-meta">
          <span>${esc(lead.section || "Reporting")}</span>
          ${lead.date ? `<time>${esc(fmtDate(lead.date))}</time>` : ""}
        </div>
        <h3>${esc(lead.title)}</h3>
        ${lead.excerpt ? `<p>${esc(excerpt(lead.excerpt, 260))}</p>` : ""}
        <div class="feature-footer"><span>Read in portfolio</span><strong>→</strong></div>
      </a>

      <div class="feature-side">
        ${side.map((a, i) => `
          <a class="feature-mini" href="${esc(localHref(a))}">
            <div class="feature-mini-index">0${i + 2}</div>
            <div>
              <div class="feature-meta">
                <span>${esc(a.section || "Reporting")}</span>
                ${a.date ? `<time>${esc(fmtDate(a.date))}</time>` : ""}
              </div>
              <h3>${esc(a.title)}</h3>
              ${a.excerpt ? `<p>${esc(excerpt(a.excerpt, 115))}</p>` : ""}
            </div>
            <span class="mini-arrow">↗</span>
          </a>
        `).join("")}
      </div>
    `;
  }

  function renderBeats(articles) {
    const counts = new Map();
    articles.forEach(a => {
      const section = a.section || "Other";
      counts.set(section, (counts.get(section) || 0) + 1);
    });

    const beats = [...counts.entries()]
      .sort((a, b) => b[1] - a[1])
      .slice(0, 6);

    document.querySelector("#beat-grid").innerHTML = beats.map(([name, count], i) => `
      <a class="beat-card beat-${(i % 3) + 1}" href="archive.html?section=${encodeURIComponent(name)}">
        <span class="beat-count">${count}</span>
        <h3>${esc(name)}</h3>
        <span class="beat-note">${count === 1 ? "story" : "stories"} →</span>
      </a>
    `).join("");
  }

  function renderStats(articles, updatedAt) {
    document.querySelector("#story-count").textContent = articles.length;

    const years = articles
      .map(a => String(a.date || "").slice(0, 4))
      .filter(y => /^\d{4}$/.test(y))
      .map(Number);

    document.querySelector("#year-span").textContent = years.length
      ? `${Math.min(...years)}–${Math.max(...years)}`
      : "Growing";

    if (updatedAt) {
      const d = new Date(updatedAt);
      if (!Number.isNaN(d.getTime())) {
        document.querySelector("#last-updated").textContent =
          "UPDATED " + new Intl.DateTimeFormat("en-GB", {
            day: "numeric", month: "short", year: "numeric", timeZone: "UTC"
          }).format(d).toUpperCase();
      }
    }
  }

  async function init() {
    try {
      const response = await fetch("data/articles.json", { cache: "no-store" });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const payload = await response.json();

      const articles = (Array.isArray(payload.articles) ? payload.articles : [])
        .filter(a => a.verified_author === true && a.local_url)
        .sort((a, b) => String(b.date || "").localeCompare(String(a.date || "")));

      renderFeatured(articles);
      renderBeats(articles);
      renderStats(articles, payload.updated_at);
    } catch (error) {
      document.querySelector("#featured-layout").innerHTML =
        `<div class="loading-card">The verified archive could not be loaded.</div>`;
      console.error(error);
    }
  }

  init();
})();
