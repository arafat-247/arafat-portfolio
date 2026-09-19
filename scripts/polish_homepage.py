"""Apply the simplified editorial homepage after final build processing."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
HOME = DIST / "index.html"
CSS = DIST / "portfolio.css"
CSS_MARKER = "/* Simplified editorial homepage v18.6 */"
ASSET_VERSION_RE = re.compile(r"portfolio\\.css\\?v=[0-9.]+", re.I)
SCRIPT_VERSION_RE = re.compile(r"portfolio\\.js\\?v=[0-9.]+", re.I)
ASSET_VERSION = "18.6.1"

HOME_CSS = r"""
/* Simplified editorial homepage v18.6 */
body.home main{background:var(--paper)}
body.home .homecontent{width:min(100%,1050px);margin:auto;padding:34px 34px 54px}

/* Keep the header consistent with the rest of the site. */
@media(max-width:800px){
  body.home .mobilehead{height:64px;padding:0 18px}
  body.home .mobilebrand{gap:10px}
  body.home .mark{width:39px;height:39px}
  body.home .themetoggle{display:none}
  body.home .menutoggle{display:inline-flex}
  body.home .mobilemenu[hidden],
  body.home .menubackdrop[hidden]{display:none!important}
}

/* Hero */
body.home .homehero{
  position:relative;
  display:block;
  min-height:460px;
  margin:0 0 28px;
  overflow:hidden;
  color:#fff;
  background:#102f2a;
  box-shadow:0 16px 36px rgb(19 40 34 / 10%);
}
body.home .homeheroimage{
  position:absolute;
  inset:0;
  width:100%;
  height:100%;
  object-fit:cover;
  object-position:center 32%;
  filter:grayscale(1) contrast(1.03);
}
body.home .homehero:after{
  pointer-events:none;
  content:"";
  position:absolute;
  inset:0;
  z-index:1;
  background:
    linear-gradient(90deg,rgb(6 27 24 / 76%) 0%,rgb(6 27 24 / 42%) 42%,rgb(6 27 24 / 8%) 68%,transparent 100%),
    linear-gradient(0deg,rgb(6 27 24 / 36%),transparent 50%);
}
body.home .homeherooverlay{
  position:absolute;
  z-index:2;
  left:36px;
  bottom:34px;
  width:min(48%,470px);
  padding:26px 28px;
  background:rgb(7 55 48 / 88%);
  backdrop-filter:blur(2px);
}
body.home .homeherooverlay>span{
  color:#f2aa91;
  font-size:10px;
  font-weight:850;
  letter-spacing:.16em;
  text-transform:uppercase;
}
body.home .homeherooverlay h2{
  margin:8px 0 0;
  color:#fff;
  font:700 clamp(44px,5vw,68px)/.92 var(--serif);
  letter-spacing:-.04em;
}
body.home .homeherooverlay p{
  margin:14px 0 0;
  color:rgb(255 255 255 / 82%);
  font-size:15px;
  line-height:1.5;
}
body.home .homeherooverlay nav{
  display:flex;
  flex-wrap:wrap;
  gap:16px;
  margin-top:18px;
}
body.home .homeherooverlay a{
  padding-bottom:3px;
  border-bottom:1px solid currentColor;
  color:#fff;
  font-size:12px;
  font-weight:800;
  text-decoration:none;
}

/* Original portfolio structure */
body.home .homeintro{display:grid;grid-template-columns:1fr 1.6fr;align-items:end;gap:24px;margin:0 0 28px}
body.home .homeintro>span{grid-column:1/-1;color:var(--accent);font-size:11px;font-weight:850;letter-spacing:.15em;text-transform:uppercase}
body.home .homeintro h1{margin:0;font:700 clamp(42px,5vw,62px)/.95 var(--serif);letter-spacing:-.04em}
body.home .homeintro p{margin:0 0 3px;color:var(--muted);font-size:16px;line-height:1.55}
body.home .tiles{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}
body.home .tile{min-height:245px;padding:24px;box-shadow:none}
body.home .tile strong{font:700 clamp(27px,3vw,36px)/1.03 var(--serif)}
body.home .tile small{max-width:330px;margin-top:8px;font-size:12px;line-height:1.4}
body.home .tile-reporting .tile-art{background:radial-gradient(circle at 78% 32%,rgb(190 92 66 / 30%) 0 7%,transparent 7.5%),repeating-linear-gradient(90deg,transparent 0 38px,rgb(255 255 255 / 7%) 39px 40px),repeating-linear-gradient(0deg,transparent 0 38px,rgb(255 255 255 / 6%) 39px 40px),#123a34}
body.home .tile-opinion .tile-art{background:radial-gradient(circle at 82% 20%,transparent 0 34px,rgb(255 255 255 / 12%) 35px 36px,transparent 37px 63px,rgb(255 255 255 / 9%) 64px 65px,transparent 66px),repeating-linear-gradient(135deg,transparent 0 25px,rgb(255 255 255 / 6%) 26px 27px),#203e38}
body.home .tile-thoughts .tile-art{background:repeating-radial-gradient(ellipse at 76% 55%,transparent 0 22px,rgb(255 255 255 / 9%) 23px 24px,transparent 25px 40px),#304a43}
body.home .tile-photos img{filter:brightness(.62) saturate(.78)}
body.home .homecontact{margin-top:42px}

@media(max-width:800px){
  body.home .homecontent{padding:18px 16px 42px}
  body.home .homehero{min-height:390px;margin-bottom:26px}
  body.home .homeheroimage{object-position:center 23%}
  body.home .homehero:after{
    background:linear-gradient(0deg,rgb(5 27 23 / 88%) 0%,rgb(5 27 23 / 46%) 44%,rgb(5 27 23 / 7%) 72%,transparent 100%)
  }
  body.home .homeherooverlay{
    left:16px;
    right:16px;
    bottom:16px;
    width:auto;
    padding:20px 20px 18px;
    background:rgb(7 55 48 / 90%);
  }
  body.home .homeherooverlay h2{font-size:38px}
  body.home .homeherooverlay p{font-size:13px}
  body.home .homeherooverlay nav{margin-top:14px}
  body.home .homeintro{grid-template-columns:1fr;gap:4px;margin-bottom:22px}
  body.home .homeintro h1{font-size:clamp(44px,12vw,60px)}
  body.home .homeintro p{margin-top:10px;font-size:15px}
  body.home .tiles{grid-template-columns:1fr 1fr;gap:8px}
  body.home .tile{min-height:170px;padding:18px}
  body.home .tile-reporting,
  body.home .tile-photos{grid-column:1/-1}
  body.home .tile strong{font-size:22px}
  body.home .tile small{font-size:11px}
  body.home .homecontact{margin-top:20px;padding:26px}
  body.home .homecontact strong{font-size:30px}
}

@media(max-width:420px){
  body.home .homehero{min-height:360px}
  body.home .homeherooverlay h2{font-size:34px}
  body.home .tile{min-height:158px}
}
""".strip()


def main() -> None:
    if not HOME.is_file() or not CSS.is_file():
        raise FileNotFoundError("Build output is incomplete; run scripts/build.py first")

    source = HOME.read_text(encoding="utf-8")
    source = ASSET_VERSION_RE.sub(f"portfolio.css?v={ASSET_VERSION}", source)
    source = SCRIPT_VERSION_RE.sub(f"portfolio.js?v={ASSET_VERSION}", source)
    HOME.write_text(source, encoding="utf-8")

    css_text = CSS.read_text(encoding="utf-8")
    old_markers = (
        "/* Hybrid editorial homepage v18.4 */",
        "/* Simplified editorial homepage v18.6 */",
    )
    cut = len(css_text)
    for marker in old_markers:
        index = css_text.find(marker)
        if index >= 0:
            cut = min(cut, index)
    if cut < len(css_text):
        css_text = css_text[:cut].rstrip()
    CSS.write_text(css_text + "\n\n" + HOME_CSS + "\n", encoding="utf-8")
    print(f"Homepage polish: simplified=1, overlay_hero=1, asset_version={ASSET_VERSION}")


if __name__ == "__main__":
    main()
