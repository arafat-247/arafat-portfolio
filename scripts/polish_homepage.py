"""Give the homepage a denser editorial treatment after the main build."""
from __future__ import annotations

import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
HOME = DIST / "index.html"
INDEX = DIST / "data" / "index.json"
CSS = DIST / "portfolio.css"
CSS_MARKER = "/* Editorial homepage polish */"
ASSET_VERSION_RE = re.compile(r"portfolio\.css\?v=[0-9.]+", re.I)
ASSET_VERSION = "17.4.0"

HOME_CSS = r"""
/* Editorial homepage polish */
body.home main{background:
  radial-gradient(circle at 8% 7%,rgb(166 75 54 / 7%) 0 86px,transparent 87px),
  linear-gradient(180deg,#e8e1d5 0%,#eee9df 38%,#e5ddd0 100%)}
body.home .homecontent{padding-top:34px;padding-bottom:38px}
body.home .homeprofile{box-shadow:0 18px 44px rgb(20 43 38 / 12%)}
body.home .homeintro{margin-bottom:18px;padding:20px 0 22px;border-top:1px solid #c9c0b2;border-bottom:1px solid #c9c0b2}
.homefocus{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:0 0 22px;padding:11px 12px;border:1px solid #c9c0b2;background:#ddd4c6}
.homefocus>span{margin-right:3px;color:#6e655b;font-size:9.5px;font-weight:850;letter-spacing:.12em;text-transform:uppercase}
.homefocus a{padding:6px 9px;border:1px solid rgb(65 61 54 / 14%);background:rgb(255 255 255 / 28%);font-size:10.5px;font-weight:760;line-height:1.2;text-decoration:none}
.homefocus a:hover{background:rgb(255 255 255 / 55%)}
body.home .tiles{gap:11px}
body.home .tile{box-shadow:0 10px 28px rgb(11 48 43 / 8%)}
.homelatest{margin-top:28px;padding:26px 26px 22px;color:#f4f0e7;background:linear-gradient(135deg,#153b35,#0b2e29)}
.homelatest>header{display:flex;align-items:end;justify-content:space-between;gap:20px;margin-bottom:15px}
.homelatest-kicker{display:block;color:#e99a82;font-size:9.5px;font-weight:850;letter-spacing:.13em;text-transform:uppercase}
.homelatest h2{margin:4px 0 0;font:700 30px/1 var(--serif)}
.homelatest-all{color:rgb(244 240 231 / 76%);font-size:10.5px;font-weight:800;text-decoration:none}
.homelatest-all:hover{color:#fff}
.homelatest-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));border-top:1px solid rgb(244 240 231 / 18%)}
.homelatest article{min-width:0;padding:18px 18px 6px 0}
.homelatest article+article{padding-left:18px;border-left:1px solid rgb(244 240 231 / 16%)}
.homelatest-meta{display:flex;flex-wrap:wrap;gap:5px 9px;color:rgb(244 240 231 / 58%);font-size:9px;line-height:1.3;text-transform:uppercase;letter-spacing:.06em}
.homelatest h3{margin:10px 0 0;font:700 19px/1.12 var(--serif)}
.homelatest h3 a{text-decoration:none}
.homelatest h3 a:hover{text-decoration:underline}
body.home .homecontact{margin-top:22px}
html[data-theme="dark"] body.home main{background:linear-gradient(180deg,#101715,#141d1a 45%,#0f1715)}
html[data-theme="dark"] body.home .homeintro{border-color:#34403c}
html[data-theme="dark"] .homefocus{border-color:#34403c;background:#19231f}
html[data-theme="dark"] .homefocus>span{color:#aeb6b0}
html[data-theme="dark"] .homefocus a{border-color:#34403c;background:#202b27}
@media(max-width:800px){
  body.home .homecontent{padding-top:24px;padding-bottom:28px}
  body.home .homeprofile{margin-bottom:26px}
  body.home .homeintro{margin-bottom:15px;padding:16px 0 18px}
  .homefocus{margin-bottom:18px;padding:10px}
  .homelatest{margin-top:20px;padding:22px 18px 18px}
  .homelatest>header{align-items:start;margin-bottom:12px}
  .homelatest h2{font-size:27px}
  .homelatest-grid{grid-template-columns:1fr}
  .homelatest article{padding:15px 0}
  .homelatest article+article{padding-left:0;border-top:1px solid rgb(244 240 231 / 16%);border-left:0}
  .homelatest h3{font-size:20px}
  body.home .homecontact{margin-top:18px}
}
@media(max-width:460px){
  body.home .homecontent{padding-inline:16px}
  .homefocus{gap:6px}
  .homefocus>span{width:100%;margin-bottom:2px}
  .homefocus a{font-size:10px}
}
""".strip()


def esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def date_label(value: str) -> str:
    try:
        dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return ""
    return f"{dt.day} {dt.strftime('%B %Y')}"


def latest_markup() -> str:
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    articles = list(data.get("articles") or [])[:3]
    cards = []
    for item in articles:
        stream = str(item.get("stream") or "reporting")
        if stream == "opinion":
            label = "Opinion & Analysis"
        elif stream == "thoughts":
            label = "Thoughts"
        else:
            label = str(item.get("category") or "Reporting")
        href = "/" + str(item.get("local_url") or "").lstrip("/")
        cards.append(
            '<article>'
            f'<div class="homelatest-meta"><span>{esc(label)}</span><span>{esc(date_label(item.get("date_published", "")))}</span></div>'
            f'<h3><a href="{esc(href)}">{esc(item.get("title"))}</a></h3>'
            '</article>'
        )
    return (
        '<section class="homelatest" aria-labelledby="homelatest-title">'
        '<header><div><span class="homelatest-kicker">New from the archive</span>'
        '<h2 id="homelatest-title">Latest work</h2></div>'
        '<a class="homelatest-all" href="/all-work/">Complete index →</a></header>'
        f'<div class="homelatest-grid">{"".join(cards)}</div></section>'
    )


def main() -> None:
    if not HOME.is_file() or not INDEX.is_file() or not CSS.is_file():
        raise FileNotFoundError("Build output is incomplete; run scripts/build.py first")

    source = HOME.read_text(encoding="utf-8")
    focus = (
        '<nav class="homefocus" aria-label="Reporting focus">'
        '<span>Reporting focus</span>'
        '<a href="/education/">Education</a>'
        '<a href="/public-universities/">Public universities</a>'
        '<a href="/governance-accountability/">Governance &amp; accountability</a>'
        '<a href="/data-evidence/">Data &amp; evidence</a>'
        '</nav>'
    )
    if 'class="homefocus"' not in source:
        marker = '</header><div class="tiles">'
        if marker not in source:
            raise ValueError("Homepage intro marker not found")
        source = source.replace(marker, '</header>' + focus + '<div class="tiles">', 1)

    if 'class="homelatest"' not in source:
        marker = '</div><aside class="homecontact">'
        if marker not in source:
            raise ValueError("Homepage contact marker not found")
        source = source.replace(marker, '</div>' + latest_markup() + '<aside class="homecontact">', 1)

    source = ASSET_VERSION_RE.sub(f"portfolio.css?v={ASSET_VERSION}", source)
    HOME.write_text(source, encoding="utf-8")

    css = CSS.read_text(encoding="utf-8")
    marker_index = css.find(CSS_MARKER)
    if marker_index >= 0:
        css = css[:marker_index].rstrip()
    CSS.write_text(css + "\n\n" + HOME_CSS + "\n", encoding="utf-8")
    print(f"Homepage polish: latest=3, focus=4, asset_version={ASSET_VERSION}")


if __name__ == "__main__":
    main()
