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
ASSET_VERSION = "17.4.1"

HOME_CSS = r"""
/* Editorial homepage polish */
body.home main{
  background:
    radial-gradient(circle at 9% 8%,rgb(166 75 54 / 7%) 0 74px,transparent 75px),
    linear-gradient(180deg,#e4dccf 0%,#e9e2d7 44%,#ddd4c7 100%);
}
body.home .homecontent{padding-top:28px;padding-bottom:34px}
body.home .homeprofile{margin-bottom:26px;box-shadow:0 16px 40px rgb(20 43 38 / 11%)}
body.home .homeintro{margin:0 0 20px;padding:16px 0 18px;border-top:1px solid #c5baaa;border-bottom:1px solid #c5baaa}
body.home .homeintro p{max-width:610px}
body.home .tiles{gap:10px}
body.home .tile{box-shadow:0 9px 24px rgb(11 48 43 / 8%)}
body.home .homecontact{margin-top:22px}
html[data-theme="dark"] body.home main{background:linear-gradient(180deg,#101715,#141d1a 45%,#0f1715)}
html[data-theme="dark"] body.home .homeintro{border-color:#34403c}
@media(max-width:800px){
  body.home .homecontent{padding-top:22px;padding-bottom:26px}
  body.home .homeprofile{margin-bottom:22px}
  body.home .homeintro{margin-bottom:16px;padding:14px 0 16px}
  body.home .homeintro>span{margin-bottom:2px}
  body.home .homeintro h1{font-size:clamp(41px,11vw,56px)}
  body.home .homeintro p{margin-top:9px;font-size:15px;line-height:1.45}
  body.home .tiles{gap:9px}
  body.home .homecontact{margin-top:18px}
}
@media(max-width:460px){
  body.home .homecontent{padding-inline:16px}
  body.home .homeprofile{min-height:208px}
  body.home .tile{min-height:158px}
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
    print(f"Homepage polish: structure=original, asset_version={ASSET_VERSION}")


if __name__ == "__main__":
    main()
