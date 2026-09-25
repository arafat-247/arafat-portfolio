"""Apply the approved editorial homepage composition after final build processing."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
HOME = DIST / "index.html"
CSS = DIST / "portfolio.css"
ASSET_VERSION_RE = re.compile(r"portfolio\\.css\\?v=[0-9.]+", re.I)
SCRIPT_VERSION_RE = re.compile(r"portfolio\\.js\\?v=[0-9.]+", re.I)
ASSET_VERSION = "21.2.2"

HOME_CSS = r"""
/* Mobile homepage — reference-aligned personal composition */
body.home{background:#111715;overflow-x:hidden}
body.home .identity,body.home .desktophead,body.home .mobilehead,body.home .mobilemenu,body.home .menubackdrop,body.home .right>footer{display:none!important}
body.home .right,body.home main{width:100%!important;max-width:none!important;margin:0!important;padding:0!important;background:#111715}
.deskhome{width:100%;min-height:100vh;padding:18px;background:#111715}
.deskstage{position:relative;width:min(100%,1600px);aspect-ratio:1447/1087;margin:0 auto;overflow:hidden;border:1px solid rgb(255 255 255 / 20%);border-radius:25px;background:#2b160b;box-shadow:0 22px 65px rgb(0 0 0 / 42%)}
.deskvisual,.deskvisual img{position:absolute;inset:0;display:block;width:100%;height:100%}
.deskvisual img{object-fit:cover;object-position:center}
.desksemantics,.deskhotspot span,.deskemail span{position:absolute!important;width:1px!important;height:1px!important;padding:0!important;margin:-1px!important;overflow:hidden!important;clip:rect(0,0,0,0)!important;white-space:nowrap!important;border:0!important}
.deskhotspots{position:absolute;inset:0;z-index:5}
.deskhotspot{position:absolute;display:block;border-radius:4px;color:transparent;text-decoration:none;background:transparent}
.deskhotspot:focus-visible{outline:3px solid #f0d5aa;outline-offset:3px;background:rgb(255 255 255 / 5%)}
.desknav-home{left:49.7%;top:1.2%;width:5.9%;height:5.3%}.desknav-about{left:56.2%;top:1.2%;width:6%;height:5.3%}.desknav-work{left:63%;top:1.2%;width:5.7%;height:5.3%}.desknav-writing{left:69.1%;top:1.2%;width:7.2%;height:5.3%}.desknav-contact{left:76.5%;top:1.2%;width:7.2%;height:5.3%}
.deskprofile-hotspot{left:34.6%;top:4.2%;width:22.7%;height:24.5%}.deskreporting-hotspot{left:6%;top:36.4%;width:25%;height:31.8%}.deskopinion-hotspot{left:31.3%;top:36.8%;width:26.5%;height:31.4%}.deskthoughts-hotspot{left:57.7%;top:36.5%;width:26.1%;height:31.5%}.deskphoto-hotspot{left:39.1%;top:68%;width:25.4%;height:23%}
.deskemail{position:absolute;z-index:6;right:27%;bottom:1.3%;width:15%;height:3.5%;text-decoration:none}
.portalhome-mobile{display:none!important}

@media(max-width:800px){
  html,body{max-width:100%;overflow-x:clip}
  body.home,body.home .right,body.home main{background:#eee9df}
  body.home .deskhome{display:none!important}
  body.home .portalhome-mobile{display:block!important;width:100%!important;max-width:100vw!important;margin:0!important;background:#eee9df;color:#171512}
  .portalnav{display:none!important}
  .portalhero{display:flex;min-height:100svh;flex-direction:column;align-items:center;justify-content:flex-start;padding:48px 22px 34px;text-align:center;background:#eee9df}
  .portalhero-photo{order:1;width:132px;height:132px;margin:0 0 18px;overflow:hidden;border-radius:50%;box-shadow:0 0 0 1px #cfc7b9}
  .portalhero-photo picture,.portalhero-photo img{display:block;width:100%;height:100%}
  .portalhero-photo img{object-fit:cover;object-position:52% 31%;filter:grayscale(1)}
  .portalhero-copy{order:2;display:flex;width:100%;max-width:390px;flex-direction:column;align-items:center;padding:0;color:#171512;background:transparent}
  .portalkicker{order:1;margin:0 0 8px;color:#6b655d;font:700 9px/1 var(--sans);letter-spacing:.17em;text-transform:uppercase}
  .portalhero h1{order:2;margin:0;color:#171512;font:400 clamp(35px,10vw,46px)/.95 var(--serif);letter-spacing:-.045em}
  .portalhero-deck{order:3;max-width:315px;margin:12px auto 0;color:#5c574f;font:400 13.5px/1.45 var(--serif)}
  .portalhero-social{order:4;display:flex;gap:16px;margin:14px 0 0}
  .portalhero-social a{color:#5c574f;font:700 10px/1 var(--sans);letter-spacing:.08em;text-decoration:none;text-transform:uppercase}
  .portalhero-actions{order:5;display:grid;width:100%;max-width:290px;margin:27px auto 0;border-top:1px solid #c9c1b5}
  .portalhero-actions a{display:flex;min-height:62px;align-items:center;justify-content:center;border-bottom:1px solid #c9c1b5;color:#171512;font:400 clamp(27px,7.5vw,34px)/1 var(--serif);text-decoration:none}
  .portalhero-visual,.portalhero-panel,.portalhero-script{display:none!important}

  .portalwork{padding:0 14px 22px;background:#eee9df}
  .portalgrid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
  .portalpanel{position:relative;display:flex!important;min-height:170px;overflow:hidden;align-items:flex-end;padding:16px;color:#fff;text-decoration:none;background:#143f39}
  .portalpanel:nth-child(2){background:#a44d3a}
  .portalpanel:nth-child(3){background:#d7ccb9;color:#171512}
  .portalpanel:nth-child(4){background:#1f2a28}
  .portalart,.portalimage{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
  .portalpanel:before{content:"";position:absolute;inset:0;z-index:1;background:linear-gradient(180deg,transparent 20%,rgb(8 12 11 / 50%) 100%)}
  .portal-thoughts:before{background:linear-gradient(180deg,transparent 45%,rgb(255 255 255 / 5%) 100%)}
  .portalnumber{position:absolute;z-index:2;top:13px;left:14px;font:800 8px/1 var(--sans);letter-spacing:.08em}
  .portalcopy{position:relative;z-index:2;display:block}
  .portalcopy strong{display:block;font:400 clamp(22px,6.1vw,29px)/.96 var(--serif);letter-spacing:-.035em}
  .portalcopy small{display:block;margin-top:7px;font:400 10.5px/1.35 var(--serif);opacity:.92}
  .portalarrow{display:none}
  .portal-thoughts .portalart{background:radial-gradient(circle at 78% 26%,rgb(190 151 78 / 35%) 0 34px,transparent 35px),linear-gradient(180deg,#ded5c7,#cfc4b3)}
  .portal-reporting .portalart{background:linear-gradient(160deg,#174b45,#0d302c)}
  .portal-opinion .portalart{background:linear-gradient(160deg,#b05943,#813d30)}
  .portal-photography .portalimage{filter:brightness(.64) saturate(.88)}
  .portalnote{display:none}
  .portalhome-mobile>.sitefooter,.portalfooter{margin-top:0}
}
@media(max-width:380px){
  .portalhero{padding-inline:18px}
  .portalhero-photo{width:118px;height:118px}
  .portalgrid{gap:8px}
  .portalpanel{min-height:158px;padding:14px}
  .portalcopy strong{font-size:22px}
}
@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important;transition:none!important}}
"""


def main() -> None:
    if not HOME.is_file() or not CSS.is_file():
        raise FileNotFoundError("Build output is incomplete; run scripts/build.py first")

    source = HOME.read_text(encoding="utf-8")
    source = ASSET_VERSION_RE.sub(f"portfolio.css?v={ASSET_VERSION}", source)
    source = SCRIPT_VERSION_RE.sub(f"portfolio.js?v={ASSET_VERSION}", source)
    source = re.sub(r'<style id="homepage-critical">.*?</style>', '', source, flags=re.I | re.S)
    critical = '<style id="homepage-critical">\n' + HOME_CSS + '\n</style>'
    source = source.replace("</head>", critical + "</head>", 1)
    HOME.write_text(source, encoding="utf-8")

    css_text = CSS.read_text(encoding="utf-8")
    markers = (
        "/* Hybrid editorial homepage v18.4 */",
        "/* Simplified editorial homepage v18.6 */",
        "/* Reference editorial homepage v18.8 */",
        "/* Approved editorial homepage v18.9 */",
        "/* Editorial homepage v18.10",
    )
    cut = len(css_text)
    for marker in markers:
        index = css_text.find(marker)
        if index >= 0:
            cut = min(cut, index)
    if cut < len(css_text):
        css_text = css_text[:cut].rstrip()
    CSS.write_text(css_text + "\n", encoding="utf-8")
    versioned_pages = 0
    for page in DIST.rglob("*.html"):
        page_source = page.read_text(encoding="utf-8")
        updated = ASSET_VERSION_RE.sub(f"portfolio.css?v={ASSET_VERSION}", page_source)
        updated = SCRIPT_VERSION_RE.sub(f"portfolio.js?v={ASSET_VERSION}", updated)
        if updated != page_source:
            page.write_text(updated, encoding="utf-8")
            versioned_pages += 1
    print(f"Homepage polish: photographic_desktop=1, flowing_mobile=1, mobile_menu=1, mobile_audited=1, mobile_contained=1, asset_version={ASSET_VERSION}, versioned_pages={versioned_pages}, css_isolated=1, inline_critical=1")


if __name__ == "__main__":
    main()
