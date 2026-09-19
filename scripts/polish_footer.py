"""Render the reference-led editorial site footer after build post-processing.\nNever rewrite asset cache versions; the final asset pass owns cache busting.\n"""
from __future__ import annotations

import html
import json
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
CONTENT = ROOT / "content"
FOOTER_RE = re.compile(r"<footer(?:\s[^>]*)?>.*?</footer>", re.I | re.S)
CSS_MARKER = "/* Reference editorial site footer v18.1 */"
ASSET_VERSION_RE = re.compile(r"portfolio\.css\?v=[0-9.]+", re.I)
ASSET_VERSION = "18.5.0"

FOOTER_CSS = r"""
/* Reference editorial site footer v18.1 */
.sitefooter{
  position:relative;isolation:isolate;overflow:hidden;display:block;
  min-height:0;padding:20px 30px 12px;color:#f4f0e7;
  background:#073e36;font-size:11px
}
.footergrid{
  position:relative;z-index:2;display:grid;
  grid-template-columns:1.25fr .78fr .62fr .8fr 1.18fr;
  gap:0;align-items:start;max-width:1080px;margin:0 auto
}
.footeridentity,.footergroup,.footerart{
  min-width:0;min-height:83px;padding:0 22px;
  border-left:1px solid rgb(244 240 231 / 18%)
}
.footeridentity{padding-left:0;border-left:0}
.footername{display:block;color:#fff;font:400 19px/1.05 var(--serif);text-decoration:none}
.footerrole{display:block;margin-top:5px;color:rgb(244 240 231 / 72%);font-size:10px}
.footertagline{
  max-width:230px;margin:14px 0 0;color:#d7b187;
  font:500 18px/1 "Caveat",cursive;transform:rotate(-1deg)
}
.footerlabel{
  display:block;margin:0 0 7px;color:#d9ad6f;
  font:800 8px/1.2 var(--sans);letter-spacing:.18em;text-transform:uppercase
}
.footerlinks{display:grid;gap:3px}
.footerlinks a{
  width:max-content;max-width:100%;color:rgb(244 240 231 / 82%);
  font:400 10.5px/1.32 var(--sans);text-decoration:none;
  transition:color .18s ease,transform .18s ease
}
.footerlinks a:hover{color:#fff;transform:translateX(2px)}
.footerconnect a{display:inline-flex;align-items:center;gap:6px}
.footerconnect a:before{
  display:grid;width:15px;height:15px;place-items:center;
  color:#d8e0db;font-size:8px;font-weight:800;line-height:1
}
.footerconnect a[href^="mailto:"]:before{content:"✉";font-size:10px}
.footerconnect a[href*="linkedin"]:before{content:"in";font-family:Arial,sans-serif}
.footerconnect a[href*="thedailystar"]:before{content:"★";font-size:8px}
.footerart{
  position:relative;display:flex;min-height:83px;align-items:flex-end;
  justify-content:flex-end;padding-right:0
}
.footerlandmark{width:270px;height:auto;color:#92b2a8;opacity:.82;pointer-events:none}
.footerlandmark .land{fill:none;stroke:currentColor;stroke-width:1.15;vector-effect:non-scaling-stroke}
.footerlandmark .soft{fill:#d5ad75;stroke:none;opacity:.9}
.footerartline{
  position:absolute;right:0;bottom:0;color:rgb(244 240 231 / 68%);
  font:700 7.5px/1 var(--sans);letter-spacing:.14em
}
.footerbase{
  position:relative;z-index:2;display:flex;justify-content:space-between;gap:24px;
  max-width:1080px;margin:10px auto 0;padding-top:8px;
  border-top:1px solid rgb(244 240 231 / 20%);
  color:rgb(244 240 231 / 62%);font-size:9px;line-height:1.2
}
.footerbase em{color:rgb(244 240 231 / 75%);font:italic 11px/1.2 var(--serif)}
body.home .homecontent{padding-bottom:0}
html[data-theme="dark"] .sitefooter{background:#052f29}

@media(max-width:980px){
  .footergrid{grid-template-columns:1.2fr .8fr .7fr .8fr}
  .footerart{grid-column:1/-1;min-height:70px;margin-top:12px;padding:12px 0 0;border-left:0;border-top:1px solid rgb(244 240 231 / 14%)}
  .footerlandmark{width:250px}
}
@media(max-width:800px){
  .sitefooter{padding:19px 20px calc(14px + env(safe-area-inset-bottom))}
  .footergrid{grid-template-columns:1fr 1fr;gap:0 16px}
  .footeridentity{grid-column:1/-1;min-height:0;padding:0 0 13px;border-bottom:1px solid rgb(244 240 231 / 17%)}
  .footergroup{min-height:0;margin-top:13px;padding:0;border-left:0}
  .footerabout,.footerconnect{padding-left:14px;border-left:1px solid rgb(244 240 231 / 15%)}
  .footerconnect{grid-column:2}
  .footerart{grid-column:1/-1}
  .footerbase{flex-wrap:wrap;gap:5px 14px}
}
@media(max-width:460px){
  .footergrid{grid-template-columns:1fr 1fr}
  .footerart{display:none}
  .footerlinks a{font-size:10px}
  .footerbase em{font-size:10px}
}
@media print{.sitefooter{display:none!important}}
""".strip()


def esc(value: str) -> str:
    return html.escape(str(value), quote=True)


def load_settings() -> dict:
    path = CONTENT / "settings.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def footer_markup(settings: dict) -> str:
    name = settings.get("site_name") or "Arafat Rahaman"
    email = str(settings.get("email") or "").strip()
    social = settings.get("social", {})
    linkedin = str(social.get("linkedin") or "").strip()
    daily_star = str(social.get("daily_star") or "").strip()

    connect = []
    if email:
        connect.append(f'<a href="mailto:{esc(email)}">Email</a>')
    if urlsplit(linkedin).scheme == "https":
        connect.append(f'<a href="{esc(linkedin)}" rel="me noopener">LinkedIn</a>')
    if urlsplit(daily_star).scheme == "https":
        connect.append(f'<a href="{esc(daily_star)}" rel="me noopener">The Daily Star</a>')

    monument = """<svg class="footerlandmark" viewBox="0 0 360 112" aria-hidden="true" focusable="false">
      <circle class="soft" cx="316" cy="17" r="10"/>
      <path class="land" d="M5 92 C45 77 78 80 111 69 C151 55 190 63 226 53 C270 41 316 49 356 39"/>
      <path class="land" d="M9 91 C30 78 47 70 61 76 C73 63 89 65 98 76 C111 64 129 66 137 77 C151 65 168 67 178 76"/>
      <path class="land" d="M231 88 L270 23 L278 88 M241 88 L270 36 L291 88 M251 88 L270 51 L303 88 M261 88 L270 66 L317 88"/>
      <path class="land" d="M225 88 H323 M238 94 H311"/>
      <path class="land" d="M122 85 q7-7 14 0 q7-7 14 0 M151 79 q7-7 14 0 q7-7 14 0"/>
    </svg>"""

    return f'''<footer class="sitefooter">
      <div class="footergrid">
        <section class="footeridentity" aria-label="Portfolio identity">
          <a class="footername" href="/">{esc(name)}</a>
          <span class="footerrole">Journalist · The Daily Star</span>
          <p class="footertagline">Stories for a more thoughtful Bangladesh.</p>
        </section>
        <nav class="footergroup footerexplore" aria-label="Explore portfolio">
          <strong class="footerlabel">Explore</strong>
          <div class="footerlinks"><a href="/">Portfolio</a><a href="/reporting/">Reporting</a><a href="/opinion/">Opinion &amp; Analysis</a><a href="/thoughts/">Thoughts</a><a href="/photography/">Photography</a></div>
        </nav>
        <nav class="footergroup footerabout" aria-label="About">
          <strong class="footerlabel">About</strong>
          <div class="footerlinks"><a href="/about/">About me</a><a href="/contact/">Contact</a><a href="/all-work/">Complete index</a></div>
        </nav>
        <section class="footergroup footerconnect" aria-label="Connect">
          <strong class="footerlabel">Connect</strong>
          <div class="footerlinks">{''.join(connect)}</div>
        </section>
        <section class="footerart" aria-hidden="true">{monument}<span class="footerartline">DHAKA / PEOPLE / POLICY / A FAIRER TOMORROW</span></section>
      </div>
      <div class="footerbase"><span>© {datetime.now().year} {esc(name)}. All rights reserved.</span><em>Journalism for a more equal Bangladesh.</em></div>
    </footer>'''


def main() -> None:
    if not DIST.is_dir():
        raise FileNotFoundError("dist/ does not exist; run scripts/build.py first")
    settings = load_settings()
    footer = footer_markup(settings)
    changed = 0
    for page in DIST.rglob("*.html"):
        if "admin" in page.parts:
            continue
        source = page.read_text(encoding="utf-8")
        if not FOOTER_RE.search(source):
            continue
        updated = FOOTER_RE.sub(footer, source, count=1)
        if updated != source:
            page.write_text(updated, encoding="utf-8")
            changed += 1

    css = DIST / "portfolio.css"
    if not css.is_file():
        raise FileNotFoundError("dist/portfolio.css was not generated")
    source = css.read_text(encoding="utf-8")
    marker_index = source.find(CSS_MARKER)
    if marker_index >= 0:
        source = source[:marker_index].rstrip()
    css.write_text(source + "\n\n" + FOOTER_CSS + "\n", encoding="utf-8")

    print(f"Footer polish: reference_layout=1, pages={changed}, asset_version=unchanged")


if __name__ == "__main__":
    main()
