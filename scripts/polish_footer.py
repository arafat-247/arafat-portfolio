"""Render a compact, organised site footer after all build post-processing."""
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
CSS_MARKER = "/* Compact editorial site footer */"
ASSET_VERSION_RE = re.compile(r"portfolio\.css\?v=[0-9.]+", re.I)
ASSET_VERSION = "18.0.1"

FOOTER_CSS = r"""
/* Compact editorial site footer */
.sitefooter{position:relative;isolation:isolate;overflow:hidden;display:block;min-height:0;padding:21px 34px 13px;color:#f4f0e7;background:linear-gradient(135deg,#082e29 0%,#0a3731 55%,#072722 100%);font-size:12px}
.sitefooter:before{content:"";position:absolute;inset:0;z-index:-2;background:radial-gradient(circle at 92% 15%,rgb(210 176 130 / 13%) 0 12px,transparent 13px),linear-gradient(90deg,transparent 0 67%,rgb(255 255 255 / 2.5%) 100%)}
.footergrid{position:relative;z-index:2;display:grid;grid-template-columns:minmax(185px,1.08fr) minmax(125px,.66fr) minmax(330px,1.55fr) minmax(125px,.63fr);gap:0;align-items:start;max-width:1120px;margin:0 auto}
.footeridentity,.footergroup{min-width:0;min-height:98px;padding:0 24px;border-left:1px solid rgb(244 240 231 / 16%)}
.footeridentity{padding-left:0;border-left:0}
.footername{display:block;color:#fff;font:700 18px/1.05 var(--serif);letter-spacing:.02em;text-decoration:none}
.footerrole{display:block;margin-top:5px;color:rgb(244 240 231 / 68%);font-size:10.5px;line-height:1.35}
.footertagline{max-width:225px;margin:13px 0 0;color:rgb(244 240 231 / 78%);font:italic 12.5px/1.35 var(--serif)}
.footertagline:before{content:"";display:block;width:30px;margin-bottom:8px;border-top:1px solid rgb(244 240 231 / 38%)}
.footerlabel{display:block;margin:0 0 8px;color:#faf6ef;font:700 12.5px/1.2 var(--serif)}
.footerlinks{display:grid;gap:5px}
.footerlinks a{width:max-content;max-width:100%;color:rgb(244 240 231 / 76%);font-size:10.5px;line-height:1.35;text-decoration:none;transition:color .18s ease,transform .18s ease}
.footerlinks a:hover{color:#fff;transform:translateX(2px)}
.footerlinks a:focus-visible{outline-color:#e69a84}
.footerexplore .footerlinks{grid-template-columns:minmax(0,1.18fr) minmax(0,.82fr);grid-template-rows:repeat(3,auto);grid-auto-flow:column;column-gap:20px;row-gap:5px}
.footerconnect .footerlinks{gap:7px}
.footerconnect a{display:inline-flex;align-items:center;gap:7px}
.footerconnect a:before{display:grid;width:17px;height:17px;place-items:center;border:1px solid rgb(244 240 231 / 24%);border-radius:50%;color:#fff;font-size:8px;font-weight:850;line-height:1}
.footerconnect a[href^="mailto:"]:before{content:"@"}
.footerconnect a[href*="linkedin"]:before{content:"in";font-family:Arial,sans-serif;font-size:7.5px}
.footerlandmark{position:absolute;right:-8px;bottom:20px;z-index:0;width:min(29vw,330px);height:auto;color:#8fb8ac;opacity:.24;pointer-events:none}
.footerlandmark .land{fill:none;stroke:currentColor;stroke-width:1.35;vector-effect:non-scaling-stroke}
.footerlandmark .soft{fill:currentColor;stroke:none;opacity:.46}
.footerbase{position:relative;z-index:2;display:flex;align-items:center;gap:12px;max-width:1120px;margin:11px auto 0;padding-top:9px;border-top:1px solid rgb(244 240 231 / 17%);color:rgb(244 240 231 / 58%);font-size:9.5px;line-height:1.2}
.footerbase span+span:before{content:"";display:inline-block;height:9px;margin-right:12px;border-left:1px solid rgb(244 240 231 / 24%);vertical-align:-1px}
.sitefooter .top{margin:0;color:rgb(244 240 231 / 78%)}
body.home .homecontent{padding-bottom:32px}
body.home .homecontact{background:#aa4e38}
html[data-theme="dark"] .sitefooter{color:#f4f0e7;background:linear-gradient(135deg,#062620 0%,#092f29 58%,#061f1b 100%)}
@media(max-width:980px){
  .sitefooter{padding-inline:25px}
  .footergrid{grid-template-columns:1fr .72fr 1.35fr;gap:0}
  .footerconnect{grid-column:2;grid-row:2;min-height:0;margin-top:13px;padding-top:11px;border-top:1px solid rgb(244 240 231 / 13%)}
  .footerexplore{grid-column:3;grid-row:1/3}
  .footerlandmark{width:275px;opacity:.16}
}
@media(max-width:800px){
  .sitefooter{padding:20px 20px calc(15px + env(safe-area-inset-bottom))}
  .sitefooter span{display:inline}
  .footergrid{grid-template-columns:1fr 1fr;gap:0 17px}
  .footeridentity{grid-column:1/-1;min-height:0;padding:0 0 14px;border-bottom:1px solid rgb(244 240 231 / 17%)}
  .footername{font-size:17px}
  .footerrole{display:block;margin-top:3px}
  .footertagline{max-width:none;margin-top:10px;font-size:12px}
  .footertagline:before{display:none}
  .footergroup{min-height:0;margin-top:14px;padding:0;border-left:0}
  .footernavigate{padding-right:13px;border-right:1px solid rgb(244 240 231 / 15%)}
  .footerconnect{grid-column:2;grid-row:2;margin-top:14px;padding:0;border-top:0}
  .footerexplore{grid-column:1/-1;grid-row:auto;margin-top:15px;padding-top:13px;border-top:1px solid rgb(244 240 231 / 15%)}
  .footerexplore .footerlinks{grid-template-columns:1fr 1fr;grid-template-rows:none;grid-auto-flow:row;gap:5px 13px}
  .footerlandmark{right:-18px;bottom:22px;width:235px;opacity:.23}
  .footerbase{flex-wrap:wrap;gap:4px 11px;margin-top:15px;padding-top:9px}
  .footerbase span+span:before{height:8px;margin-right:9px}
}
@media(max-width:460px){
  .sitefooter{padding-inline:18px}
  .footergrid{column-gap:13px}
  .footerexplore .footerlinks{grid-template-columns:1fr 1fr;column-gap:9px}
  .footerlinks a{font-size:10px}
  .footerlandmark{right:-12px;bottom:18px;width:220px;opacity:.26}
  body.home .homecontent{padding-bottom:24px}
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
    location = settings.get("location") or "Dhaka, Bangladesh"
    email = str(settings.get("email") or "").strip()
    linkedin = str(settings.get("social", {}).get("linkedin") or "").strip()
    daily_star = str(settings.get("social", {}).get("daily_star") or "").strip()

    connect = []
    if email:
        connect.append(f'<a href="mailto:{esc(email)}">Email</a>')
    if urlsplit(linkedin).scheme == "https":
        connect.append(f'<a href="{esc(linkedin)}" rel="me noopener">LinkedIn</a>')
    if urlsplit(daily_star).scheme == "https":
        connect.append(f'<a href="{esc(daily_star)}" rel="me noopener">Daily Star profile</a>')

    monument = '''<svg class="footerlandmark" viewBox="0 0 360 150" aria-hidden="true" focusable="false">
      <circle class="soft" cx="316" cy="24" r="13"/>
      <path class="land" d="M4 141 C48 123 86 126 126 111 C170 94 206 103 247 91 C286 80 322 87 356 76"/>
      <path class="land" d="M12 139 C35 126 49 115 64 120 C78 103 96 105 104 119 C119 104 137 106 144 119 C159 105 178 107 185 119"/>
      <path class="land" d="M233 130 L274 42 L284 130 M244 130 L274 59 L296 130 M255 130 L274 77 L308 130 M265 130 L274 96 L320 130"/>
      <path class="land" d="M226 130 H326 M240 135 H312"/>
    </svg>'''

    return f'''<footer class="sitefooter">
      <div class="footergrid">
        <section class="footeridentity" aria-label="Portfolio identity">
          <a class="footername" href="/">{esc(name)}</a>
          <span class="footerrole">Journalist · {esc(location)}</span>
          <p class="footertagline">Stories for a more thoughtful Bangladesh.</p>
        </section>
        <nav class="footergroup footernavigate" aria-label="Footer navigation">
          <strong class="footerlabel">Navigate</strong>
          <div class="footerlinks"><a class="archiveindex" href="/all-work/">Complete index</a><a class="top" href="#top">Back to top ↑</a></div>
        </nav>
        <nav class="footergroup footerexplore" data-seo-topics="1" aria-label="Explore reporting topics">
          <strong class="footerlabel">Explore</strong>
          <div class="footerlinks"><a href="/education/">Education</a><a href="/public-universities/">Public universities</a><a href="/governance-accountability/">Governance &amp; accountability</a><a href="/data-evidence/">Data &amp; evidence</a><a href="/case-studies/">Case studies</a></div>
        </nav>
        <section class="footergroup footerconnect" aria-label="Connect">
          <strong class="footerlabel">Connect</strong>
          <div class="footerlinks">{''.join(connect)}</div>
        </section>
      </div>
      {monument}
      <div class="footerbase"><span>© {datetime.now().year} {esc(name)}</span><span>Independent portfolio · Dhaka</span></div>
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
        updated = ASSET_VERSION_RE.sub(f"portfolio.css?v={ASSET_VERSION}", updated)
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

    print(f"Footer polish: pages={changed}, asset_version={ASSET_VERSION}")


if __name__ == "__main__":
    main()
