window.AR = (() => {
  const root = () => document.body?.dataset?.root || "";
  const esc = (v = "") => String(v)
    .replaceAll("&", "&amp;").replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;").replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");

  const fmtDate = value => {
    if (!value) return "";
    const raw = String(value);
    const isoDay = raw.match(/^(\d{4}-\d{2}-\d{2})/)?.[1];
    if (!isoDay) return raw;
    const [y,m,d] = isoDay.split("-").map(Number);
    const dt = new Date(Date.UTC(y, m - 1, d));
    return new Intl.DateTimeFormat("en-GB", {day:"numeric", month:"long", year:"numeric", timeZone:"UTC"}).format(dt);
  };

  const category = story => story.story_type || "Reporting";
  const topic = story => story.topic || "Public Affairs";
  const storyDate = story => story.date_published || story.date || "";
  const categoryURL = story => `${root()}archive.html?type=${encodeURIComponent(category(story))}`;
  const topicURL = story => `${root()}archive.html?topic=${encodeURIComponent(topic(story))}`;

  const excerpt = (text, max = 190) => {
    const v = String(text || "").trim();
    return v.length > max ? v.slice(0, max).trimEnd() + "…" : v;
  };

  async function json(path) {
    const r = await fetch(`${root()}${path}`, {cache:"no-store"});
    if (!r.ok) throw new Error(`${path}: ${r.status}`);
    return r.json();
  }

  async function load() {
    const [data, config, enhancements] = await Promise.all([
      json("data/articles.json"),
      json("data/site_config.json"),
      json("data/story_enhancements.json").catch(() => ({}))
    ]);
    const articles = (data.articles || [])
      .filter(a => a.verified_author === true && a.local_url)
      .sort((a,b) => Number(b.published_sort || 0) - Number(a.published_sort || 0) || String(b.date_published || b.date || "").localeCompare(String(a.date_published || a.date || "")));
    return {data, config, enhancements, articles};
  }

  function picture(base, alt, cls = "", loading = "lazy") {
    if (!base) return "";
    const prefix = root();
    return `<picture class="${esc(cls)}">
      <source srcset="${prefix}${esc(base)}.avif" type="image/avif">
      <source srcset="${prefix}${esc(base)}.webp" type="image/webp">
      <img src="${prefix}${esc(base)}.webp" alt="${esc(alt || "")}" loading="${loading}" decoding="async">
    </picture>`;
  }

  function socialLinks(config, compact = false) {
    const s = config.social || {};
    const items = [
      ["The Daily Star", s.daily_star], ["Muck Rack", s.muck_rack], ["LinkedIn", s.linkedin],
      ["Facebook", s.facebook], ["Instagram", s.instagram], ["Flickr", s.flickr]
    ].filter(([,u]) => u);
    return items.map(([name,url]) => `<a ${compact ? 'class="social-chip"' : ''} href="${esc(url)}" target="_blank" rel="me noopener">${esc(name)} <span aria-hidden="true">↗</span></a>`).join("");
  }

  function initTheme() {
    const buttons = [...document.querySelectorAll("[data-theme-toggle]")];
    if (!buttons.length) return;
    const setLabel = () => {
      const dark = document.documentElement.dataset.theme === "dark" || (!document.documentElement.dataset.theme && matchMedia("(prefers-color-scheme: dark)").matches);
      buttons.forEach(btn => { btn.setAttribute("aria-label", dark ? "Use light theme" : "Use dark theme"); btn.textContent = dark ? "☀" : "☾"; });
    };
    setLabel();
    buttons.forEach(btn => btn.addEventListener("click", () => {
      const current = document.documentElement.dataset.theme;
      const systemDark = matchMedia("(prefers-color-scheme: dark)").matches;
      const next = current ? (current === "dark" ? "light" : "dark") : (systemDark ? "light" : "dark");
      document.documentElement.dataset.theme = next;
      localStorage.setItem("ar-theme", next);
      setLabel();
    }));
  }

  function initNav() {
    const btn = document.querySelector("[data-menu-toggle]");
    const nav = document.querySelector("[data-mobile-nav]");
    if (!btn || !nav) return;
    btn.addEventListener("click", () => {
      const open = btn.getAttribute("aria-expanded") === "true";
      btn.setAttribute("aria-expanded", String(!open));
      nav.hidden = open;
    });
    nav.querySelectorAll("a").forEach(a => a.addEventListener("click", () => {
      btn.setAttribute("aria-expanded", "false"); nav.hidden = true;
    }));
  }

  async function initAnalytics() {
    try {
      const config = await json("data/site_config.json");
      const a = config.analytics || {};
      if (a.provider !== "goatcounter" || !a.site_code) return;
      const s = document.createElement("script");
      s.async = true;
      s.src = "https://gc.zgo.at/count.js";
      s.dataset.goatcounter = `https://${a.site_code}.goatcounter.com/count`;
      document.head.appendChild(s);
    } catch (_) {}
  }

  document.addEventListener("DOMContentLoaded", () => { initTheme(); initNav(); initAnalytics(); });
  return {root, esc, fmtDate, category, topic, storyDate, categoryURL, topicURL, excerpt, load, picture, socialLinks, json};
})();
