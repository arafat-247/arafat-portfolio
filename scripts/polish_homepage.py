"""Polish the homepage with restrained motion and a purposeful mobile header."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
HOME = DIST / "index.html"
CSS = DIST / "portfolio.css"
CSS_MARKER = "/* Editorial homepage polish */"
ASSET_VERSION_RE = re.compile(r"portfolio\.css\?v=[0-9.]+", re.I)
ASSET_VERSION = "17.5.0"

HOME_CSS = r"""
/* Editorial homepage polish */
body.home main{
  background:
    radial-gradient(circle at 9% 8%,rgb(166 75 54 / 6%) 0 68px,transparent 69px),
    linear-gradient(180deg,#e2d9cb 0%,#e8e0d4 45%,#ddd2c4 100%);
}
body.home .homecontent{padding-top:24px;padding-bottom:30px}
body.home .homeprofile{margin-bottom:22px;box-shadow:0 15px 36px rgb(20 43 38 / 11%)}
body.home .homeintro{margin:0 0 16px;padding:13px 0 15px;border-top:1px solid #c3b7a6;border-bottom:1px solid #c3b7a6}
body.home .homeintro p{max-width:610px}
body.home .tiles{gap:9px}
body.home .tile{box-shadow:0 8px 20px rgb(11 48 43 / 8%);transition:transform .22s ease,box-shadow .22s ease,filter .22s ease}
body.home .tile:hover{transform:translateY(-3px);box-shadow:0 14px 30px rgb(11 48 43 / 13%)}
body.home .tile:active{transform:scale(.985);filter:brightness(.97)}
body.home .tile:active>i{transform:translateX(3px)}
body.home .homecontact{margin-top:16px}
html[data-theme="dark"] body.home main{background:linear-gradient(180deg,#101715,#141d1a 45%,#0f1715)}
html[data-theme="dark"] body.home .homeintro{border-color:#34403c}

/* Motion only becomes active when the homepage script runs. */
body.home.home-motion .tile,body.home.home-motion .homecontact{opacity:0;transform:translateY(15px)}
body.home.home-motion .tile.home-visible,body.home.home-motion .homecontact.home-visible{opacity:1;transform:none;transition:opacity .55s cubic-bezier(.2,.7,.25,1),transform .55s cubic-bezier(.2,.7,.25,1),box-shadow .22s ease,filter .22s ease}
body.home.home-motion .tile.home-visible:hover{transform:translateY(-3px)}

@media(max-width:800px){
  body.home .mobilehead{height:64px;padding-inline:16px;background:color-mix(in srgb,var(--paper) 96%,transparent)}
  body.home .mobilehead:after{content:"";position:absolute;left:0;bottom:-1px;width:var(--home-scroll,0%);height:2px;background:var(--accent);transition:width .08s linear;pointer-events:none}
  body.home .mobilehead.scrolled{box-shadow:0 5px 18px rgb(12 30 27 / 10%)}
  body.home .mobilebrand{display:grid;grid-template-columns:38px minmax(0,1fr);grid-template-rows:auto auto;column-gap:10px;align-items:center;min-width:0;font-weight:800}
  body.home .mobilebrand .mark{grid-row:1/3;width:38px;height:38px}
  body.home .mobilebrand>span:nth-child(2){align-self:end;overflow:hidden;white-space:nowrap;text-overflow:ellipsis;font-size:14px;line-height:1.08}
  body.home .homeheadrole{align-self:start;margin-top:2px;color:var(--muted);font-size:8.5px;font-weight:750;line-height:1.1;letter-spacing:.07em;text-transform:uppercase}
  body.home .mobileactions:before{content:"Portfolio";display:inline-flex;align-items:center;height:24px;padding:0 8px;border:1px solid var(--line);border-radius:999px;color:var(--muted);font-size:8px;font-weight:850;letter-spacing:.11em;text-transform:uppercase}
  body.home .homecontent{padding-top:8px;padding-bottom:22px}
  body.home .homeprofile{grid-template-columns:39% 61%;min-height:184px;margin-bottom:14px}
  body.home .homeprofile>div{padding:15px}
  body.home .homeprofile>div>span{font-size:9px}
  body.home .homeprofile h2{margin-top:5px;font-size:23px}
  body.home .homeprofile p{display:-webkit-box;overflow:hidden;margin-top:9px;font-size:11px;line-height:1.38;-webkit-line-clamp:3;-webkit-box-orient:vertical}
  body.home .homeprofile nav{gap:13px;margin-top:11px}
  body.home .homeprofile a{font-size:10px}
  body.home .homeintro{margin-bottom:12px;padding:11px 0 12px}
  body.home .homeintro>span{margin-bottom:1px;font-size:10px}
  body.home .homeintro h1{font-size:clamp(39px,10vw,52px)}
  body.home .homeintro p{margin-top:7px;font-size:14px;line-height:1.4}
  body.home .tiles{grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}
  body.home .tile{min-height:142px;padding:15px}
  body.home .tile-reporting,body.home .tile-photos{grid-column:1/-1;min-height:154px}
  body.home .tile strong{font-size:20px}
  body.home .tile small{margin-top:6px;font-size:10px;line-height:1.35}
  body.home .tile>i{right:14px;top:11px;font-size:16px}
  body.home .homecontact{margin-top:14px;padding:22px}
  body.home .homecontact strong{font-size:27px}
}

@media(max-width:520px){
  body.home .homecontent{padding-inline:14px}
  body.home .homeprofile{min-height:176px}
  body.home .homeprofile>div{padding:13px}
  body.home .homeprofile h2{font-size:21px}
  body.home .tile{min-height:132px;padding:14px}
  body.home .tile-reporting,body.home .tile-photos{min-height:144px}
  body.home .tile strong{font-size:19px}
  body.home .mobileactions:before{display:none}
}

@media(max-width:360px){
  body.home .tiles{grid-template-columns:1fr}
  body.home .tile,body.home .tile-reporting,body.home .tile-photos{grid-column:auto;min-height:128px}
}

@media(prefers-reduced-motion:no-preference){
  body.home .homeprofile{animation:home-profile-in .65s cubic-bezier(.2,.7,.25,1) both}
  body.home .homeintro{animation:home-intro-in .6s .08s cubic-bezier(.2,.7,.25,1) both}
  body.home .tile-art{animation:home-pattern-drift 14s ease-in-out infinite alternate}
  body.home .tile:nth-child(2) .tile-art{animation-duration:17s;animation-direction:alternate-reverse}
  body.home .tile:nth-child(3) .tile-art{animation-duration:19s}
  body.home .tile-photos img{animation:home-photo-breathe 16s ease-in-out infinite alternate}
  body.home .tile>i{animation:home-arrow 2.8s ease-in-out infinite}
  @keyframes home-profile-in{from{opacity:.01;transform:translateY(9px) scale(.995)}to{opacity:1;transform:none}}
  @keyframes home-intro-in{from{opacity:.01;transform:translateY(8px)}to{opacity:1;transform:none}}
  @keyframes home-pattern-drift{from{background-position:0 0}to{background-position:28px 16px}}
  @keyframes home-photo-breathe{from{transform:scale(1.01)}to{transform:scale(1.045)}}
  @keyframes home-arrow{0%,75%,100%{transform:translateX(0)}86%{transform:translateX(4px)}}
}

@media(prefers-reduced-motion:reduce){
  body.home.home-motion .tile,body.home.home-motion .homecontact{opacity:1;transform:none}
  body.home .mobilehead:after{transition:none}
}
""".strip()

HOME_SCRIPT = r"""
<script id="home-motion-script">
(()=>{
  const body=document.body;
  if(!body.classList.contains('home'))return;
  const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  const header=document.querySelector('.mobilehead');
  const updateProgress=()=>{
    const max=Math.max(1,document.documentElement.scrollHeight-innerHeight);
    const progress=Math.min(100,Math.max(0,(scrollY/max)*100));
    header?.style.setProperty('--home-scroll',progress.toFixed(2)+'%');
  };
  updateProgress();
  addEventListener('scroll',updateProgress,{passive:true});
  if(reduce)return;
  body.classList.add('home-motion');
  const targets=[...document.querySelectorAll('.tile,.homecontact')];
  if(!('IntersectionObserver' in window)){
    targets.forEach(el=>el.classList.add('home-visible'));
    return;
  }
  const observer=new IntersectionObserver(entries=>{
    for(const entry of entries){
      if(!entry.isIntersecting)continue;
      entry.target.classList.add('home-visible');
      observer.unobserve(entry.target);
    }
  },{threshold:.16,rootMargin:'0px 0px -5% 0px'});
  targets.forEach(el=>observer.observe(el));
})();
</script>
""".strip()


def main() -> None:
    if not HOME.is_file() or not CSS.is_file():
        raise FileNotFoundError("Build output is incomplete; run scripts/build.py first")

    source = HOME.read_text(encoding="utf-8")
    source = ASSET_VERSION_RE.sub(f"portfolio.css?v={ASSET_VERSION}", source)

    if 'class="homeheadrole"' not in source:
        source = re.sub(
            r'(<a class="mobilebrand"[^>]*>.*?<span>Arafat Rahaman</span>)(</a>)',
            r'\1<span class="homeheadrole">Journalist · The Daily Star</span>\2',
            source,
            count=1,
            flags=re.S,
        )

    if 'id="home-motion-script"' not in source:
        source = source.replace('</body>', HOME_SCRIPT + '</body>', 1)

    HOME.write_text(source, encoding="utf-8")

    css = CSS.read_text(encoding="utf-8")
    marker_index = css.find(CSS_MARKER)
    if marker_index >= 0:
        css = css[:marker_index].rstrip()
    CSS.write_text(css + "\n\n" + HOME_CSS + "\n", encoding="utf-8")
    print(f"Homepage polish: motion=1, header=1, asset_version={ASSET_VERSION}")


if __name__ == "__main__":
    main()
