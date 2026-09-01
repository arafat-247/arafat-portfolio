(async () => {
  try {
    const [{photos=[]}, config] = await Promise.all([AR.json("data/photography.json"), AR.json("data/site_config.json")]);
    const grid=document.querySelector("#photo-grid"), empty=document.querySelector("#photo-empty");
    if (photos.length) {
      empty.hidden=true;
      grid.innerHTML=photos.map((p,i)=>`<figure class="photo-item photo-${(i%5)+1}">${AR.picture(p.base,p.alt||p.caption||"Photograph by Arafat Rahaman","photo-picture")}<figcaption><span>${AR.esc(p.caption||"")}</span><small>${AR.esc([p.location,p.year].filter(Boolean).join(" · "))}</small></figcaption></figure>`).join("");
    }
    const flickr=document.querySelectorAll("[data-flickr]"); flickr.forEach(a=>a.href=config.social.flickr);
  } catch(e){console.error(e)}
})();
