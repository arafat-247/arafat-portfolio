(() => {
  let articles = [], config = {}, enhancements = {};

  function meta(story) {
    return `<div class="story-meta-line">
      <a href="${AR.categoryURL(story)}">${AR.esc(AR.category(story))}</a>
      <time datetime="${AR.esc(AR.storyDate(story))}">${AR.esc(AR.fmtDate(AR.storyDate(story)))}</time>
    </div>`;
  }

  function heroFor(story) {
    const e = enhancements[story.url] || {};
    if (!e.hero?.base) return "";
    return AR.picture(e.hero.base, e.hero.alt || `Editorial illustration for ${story.title}`, "latest-lead-media", "eager");
  }

  function renderLatest() {
    const host = document.querySelector("#latest-work");
    if (!host) return;
    const latest = articles.slice(0, 7);
    if (!latest.length) {
      host.innerHTML = `<p class="empty-state">The verified archive is being refreshed.</p>`;
      return;
    }
    const lead = latest[0], rest = latest.slice(1);
    const image = heroFor(lead);
    host.innerHTML = `
      <article class="latest-lead ${image ? "has-media" : "text-only"}">
        <div class="latest-lead-copy">
          ${meta(lead)}
          <h3><a href="${AR.esc(lead.local_url)}">${AR.esc(lead.title)}</a></h3>
          ${lead.excerpt ? `<p>${AR.esc(AR.excerpt(lead.excerpt, 260))}</p>` : ""}
          <a class="text-link" href="${AR.esc(lead.local_url)}">Read article <span>→</span></a>
        </div>
        ${image}
      </article>
      <div class="latest-list">
        ${rest.map(story => `<article class="latest-row">
          <div class="latest-row-meta">${meta(story)}</div>
          <h3><a href="${AR.esc(story.local_url)}">${AR.esc(story.title)}</a></h3>
          <a class="row-go" aria-label="Read ${AR.esc(story.title)}" href="${AR.esc(story.local_url)}">↗</a>
        </article>`).join("")}
      </div>`;
  }

  function renderPinned() {
    const wrap = document.querySelector("#notable-section");
    const host = document.querySelector("#notable-work");
    const pins = new Set(config.pinned_story_urls || []);
    const pinned = articles.filter(a => pins.has(a.url)).slice(0, 4);
    if (!wrap || !host || !pinned.length) { if (wrap) wrap.hidden = true; return; }
    wrap.hidden = false;
    host.innerHTML = pinned.map((story, i) => `<article class="notable-item">
      <span class="notable-no">0${i+1}</span>
      <div>${meta(story)}<h3><a href="${AR.esc(story.local_url)}">${AR.esc(story.title)}</a></h3></div>
    </article>`).join("");
  }

  async function init() {
    try {
      ({articles, config, enhancements} = await AR.load());
      renderLatest(); renderPinned();
      const social = document.querySelector("#home-social");
      if (social) social.innerHTML = AR.socialLinks(config, true);
    } catch (e) {
      console.error(e);
      document.querySelector("#latest-work").innerHTML = `<p class="empty-state">The archive could not be loaded.</p>`;
    }
  }
  init();
})();
