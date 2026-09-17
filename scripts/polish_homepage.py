"""Tighten the homepage without adding extra editorial sections."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
HOME = DIST / "index.html"
CSS = DIST / "portfolio.css"
CSS_MARKER = "/* Editorial homepage polish */"
ASSET_VERSION_RE = re.compile(r"portfolio\.css\?v=[0-9.]+", re.I)
ASSET_VERSION = "17.4.2"

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
body.home .tile{box-shadow:0 8px 20px rgb(11 48 43 / 8%);transition:transform .18s ease,box-shadow .18s ease,filter .18s ease}
body.home .tile:active{transform:scale(.985);filter:brightness(.97)}
body.home .tile:active>i{transform:translateX(3px)}
body.home .homecontact{margin-top:16px}
html[data-theme="dark"] body.home main{background:linear-gradient(180deg,#101715,#141d1a 45%,#0f1715)}
html[data-theme="dark"] body.home .homeintro{border-color:#34403c}

@media(max-width:800px){
  body.home .mobilehead{height:60px}
  body.home .mobilehead.scrolled{box-shadow:0 5px 18px rgb(12 30 27 / 10%)}
  body.home .homecontent{padding-top:10px;padding-bottom:22px}
  body.home .homeprofile{grid-template-columns:39% 61%;min-height:184px;margin-bottom:14px}
  body.home .homeprofile>div{padding:15px 15px}
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
}

@media(max-width:360px){
  body.home .tiles{grid-template-columns:1fr}
  body.home .tile,body.home .tile-reporting,body.home .tile-photos{grid-column:auto;min-height:128px}
}

@media(prefers-reduced-motion:no-preference){
  body.home .homeprofile,body.home .homeintro,body.home .tile,body.home .homecontact{animation:home-rise .42s cubic-bezier(.2,.65,.3,1) both}
  body.home .homeintro{animation-delay:.04s}
  body.home .tile:nth-child(1){animation-delay:.08s}
  body.home .tile:nth-child(2){animation-delay:.11s}
  body.home .tile:nth-child(3){animation-delay:.14s}
  body.home .tile:nth-child(4){animation-delay:.17s}
  body.home .homecontact{animation-delay:.20s}
  @keyframes home-rise{from{opacity:.01;transform:translateY(8px)}to{opacity:1;transform:none}}
}
""".strip()


def main() -> None:
    if not HOME.is_file() or not CSS.is_file():
        raise FileNotFoundError("Build output is incomplete; run scripts/build.py first")

    source = HOME.read_text(encoding="utf-8")
    source = ASSET_VERSION_RE.sub(f"portfolio.css?v={ASSET_VERSION}", source)
    HOME.write_text(source, encoding="utf-8")

    css = CSS.read_text(encoding="utf-8")
    marker_index = css.find(CSS_MARKER)
    if marker_index >= 0:
        css = css[:marker_index].rstrip()
    CSS.write_text(css + "\n\n" + HOME_CSS + "\n", encoding="utf-8")
    print(f"Homepage polish: responsive=1, compact=1, asset_version={ASSET_VERSION}")


if __name__ == "__main__":
    main()
