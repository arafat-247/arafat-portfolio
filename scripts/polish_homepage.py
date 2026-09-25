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
ASSET_VERSION = "19.2.0"

HOME_CSS = r"""
/* Homepage v19.2 — compact portrait hero + balanced reference work grid */
body.home{background:#f3eee6}
body.home .identity,
body.home .desktophead,
body.home .mobilehead,
body.home .mobilemenu,
body.home .menubackdrop,
body.home .right>footer{display:none!important}
body.home .right{margin-left:0;min-height:100vh;background:#f3eee6}
body.home main{min-height:100vh;background:#f3eee6}
body.home .portalhome{width:100%;overflow:hidden;background:#f3eee6;color:#171513}

.portalnav{
  position:sticky;top:0;z-index:50;
  display:flex;height:68px;align-items:center;justify-content:space-between;
  padding:0 clamp(22px,5vw,72px);
  color:#181614;background:rgb(243 238 230 / 94%);
  border-bottom:1px solid #d9d0c4;backdrop-filter:blur(10px)
}
.portalbrand{display:grid;gap:2px;text-decoration:none}
.portalbrand strong{font:400 24px/1 var(--serif);letter-spacing:-.03em}
.portalbrand small{font:800 7px/1.2 var(--sans);letter-spacing:.22em;text-transform:uppercase;opacity:.6}
.portalnavlinks{display:flex;gap:24px}
.portalnavlinks a{font:750 9px/1 var(--sans);letter-spacing:.11em;text-transform:uppercase;text-decoration:none;opacity:.7}
.portalnavlinks a:hover,.portalnavlinks a[aria-current=page]{opacity:1}

.portalhero{
  display:grid;
  min-height:500px;
  grid-template-columns:minmax(0,1fr) minmax(390px,46%);
  gap:34px;
  align-items:center;
  padding:34px clamp(22px,5vw,72px) 22px;
  color:#171513;background:#f3eee6
}
.portalhero-copy{padding:8px 0 12px}
.portalkicker{
  display:block;margin-bottom:16px;color:#9a2b1f;
  font:850 9px/1 var(--sans);letter-spacing:.24em;text-transform:uppercase
}
.portalhero h1{
  max-width:6ch;margin:0 0 18px;
  font:400 clamp(60px,6.2vw,82px)/.88 var(--serif);
  letter-spacing:-.055em
}
.portalhero h1 em{display:block;font-style:italic}
.portalhero-deck{
  max-width:600px;margin:0;color:#2d2925;
  font:400 clamp(17px,1.35vw,21px)/1.48 var(--serif)
}
.portalhero-script{
  margin:17px 0 0;color:#ad7a4e;
  font:600 clamp(26px,2.2vw,32px)/1.05 "Caveat",cursive
}
.portalhero-actions{display:flex;gap:12px;flex-wrap:wrap;margin-top:26px}
.portalhero-actions a{
  display:inline-flex;min-width:168px;min-height:46px;
  align-items:center;justify-content:space-between;gap:22px;
  padding:0 18px;border:1px solid #29423d;border-radius:999px;
  color:#171513;font:750 11px/1 var(--sans);text-decoration:none
}
.portalhero-actions .portalhero-primary{color:#fff;background:#0b4a42;border-color:#0b4a42}
.portalhero-actions a b{font-weight:400}

.portalhero-visual{position:relative;min-height:440px}
.portalhero-panel{
  position:absolute;inset:38px 0 0 21%;
  overflow:hidden;border-radius:30px;
  background:linear-gradient(180deg,#0f5a50,#073f38);
  box-shadow:0 16px 40px rgb(20 18 13 / 8%)
}
.portalhero-panel:before{
  content:"";position:absolute;inset:0;
  background:radial-gradient(circle at 88% 12%,rgb(255 255 255 / 14%),transparent 34%),
             linear-gradient(90deg,rgb(255 255 255 / 5%),transparent 26%)
}
.portalhero-panel p{
  position:absolute;z-index:2;right:28px;top:26px;
  width:170px;margin:0;color:#fff;
  font:italic 28px/1.02 var(--serif)
}
.portalhero-panel span{
  position:absolute;z-index:2;right:28px;bottom:26px;
  color:#eef4f1;font:800 8px/1.5 var(--sans);
  letter-spacing:.22em;text-transform:uppercase
}
.portalhero-photo{
  position:absolute;left:0;top:0;width:min(420px,76%);
  margin:0;padding:12px;border-radius:22px;
  background:#f8f4ec;box-shadow:0 16px 40px rgb(20 18 13 / 10%);
  transform:rotate(-1deg)
}
.portalhero-photo:before{
  content:"";position:absolute;z-index:-1;inset:10px -14px -12px 20px;
  border-radius:22px;background:#e6ddd0;transform:rotate(2.5deg)
}
.portalhero-photo picture{display:block;overflow:hidden;border-radius:16px}
.portalhero-photo img{
  display:block;width:100%;height:auto;aspect-ratio:3/3.25;
  object-fit:cover;object-position:center 46%;
  filter:grayscale(1) contrast(1.03)
}
.portalhero-photo figcaption{
  position:absolute;left:24px;bottom:24px;color:#fff;
  font:600 25px/1 "Caveat",cursive;
  transform:rotate(-5deg);text-shadow:0 2px 9px rgb(0 0 0 / 34%)
}

.portalwork{padding:14px clamp(22px,5vw,72px) 44px;background:#f3eee6}
.portalintro{
  display:grid;grid-template-columns:minmax(0,1.25fr) minmax(280px,.75fr);
  gap:24px 46px;align-items:end;
  width:min(100%,1320px);margin:0 auto;padding:12px 0 24px
}
.portalintro .portalkicker{margin:0 0 9px}
.portalintro h2{
  margin:0;font:400 clamp(46px,4.8vw,64px)/.91 var(--serif);
  letter-spacing:-.05em
}
.portalintro p{
  margin:0 0 10px;color:#514a42;
  font:400 16px/1.5 var(--serif)
}
.portalintro-link{
  display:inline-flex;gap:10px;padding-bottom:4px;
  border-bottom:1px solid currentColor;color:#0b4a42;
  font:750 10px/1 var(--sans);text-decoration:none
}
.portalintro-link b{font-weight:400}

.portalgrid{
  display:grid;width:min(100%,1320px);margin:0 auto;gap:16px;
  grid-template-columns:1.12fr .88fr .96fr;
  grid-template-areas:"report report opinion" "thoughts photo photo";
  grid-auto-rows:minmax(250px,auto)
}
.portalpanel{
  position:relative;isolation:isolate;overflow:hidden;
  display:flex;min-height:250px;align-items:flex-end;
  padding:22px 24px 24px;border-radius:30px;
  box-shadow:0 16px 38px rgb(20 18 13 / 8%);
  color:#fff;text-decoration:none
}
.portalpanel:after{
  content:"";position:absolute;inset:0;z-index:-1;pointer-events:none
}
.portalart,.portalimage{position:absolute;inset:0;z-index:-3;width:100%;height:100%}
.portalart{
  background-image:url("assets/home/portal-reference-sprite.webp");
  background-repeat:no-repeat;background-size:100% 300%
}
.portalart-reporting{background-position:center top}
.portalart-opinion{background-position:center 50%}
.portalart-thoughts{background-position:center bottom}
.portalimage{object-fit:cover;transition:transform .35s ease}
.portalpanel:hover .portalimage{transform:scale(1.015)}

.portal-reporting{grid-area:report;min-height:330px}
.portal-reporting:after{background:linear-gradient(180deg,rgb(0 0 0 / 8%),rgb(0 0 0 / 46%))}
.portal-opinion{grid-area:opinion;min-height:330px;background:#8f190f}
.portal-opinion:after{background:linear-gradient(180deg,rgb(94 12 8 / 6%),rgb(62 7 5 / 30%))}
.portal-thoughts{grid-area:thoughts;color:#171513;background:#f5f0e7}
.portal-thoughts:after{background:linear-gradient(180deg,rgb(255 255 255 / 4%),rgb(255 255 255 / 25%))}
.portal-photography{grid-area:photo}
.portal-photography:after{background:linear-gradient(180deg,rgb(0 0 0 / 4%),rgb(0 0 0 / 56%))}
.portal-photography .portalimage{filter:saturate(.82) brightness(.85)}

.portalnumber{
  position:absolute;left:22px;top:20px;z-index:3;
  display:grid;width:34px;height:34px;place-items:center;
  border-radius:50%;background:rgb(255 255 255 / 78%);
  color:#171513;font:800 9px/1 var(--sans)
}
.portalcopy{position:relative;z-index:3;display:block;max-width:72%}
.portal-reporting .portalcopy{max-width:55%}
.portal-opinion .portalcopy{max-width:84%}
.portal-photography .portalcopy{max-width:56%}
.portalcopy strong{
  display:block;font:400 clamp(34px,3.4vw,48px)/.94 var(--serif);
  letter-spacing:-.045em
}
.portalcopy small{
  display:block;margin-top:8px;color:currentColor;opacity:.9;
  font:400 15px/1.42 var(--serif)
}
.portalarrow{
  position:absolute;right:20px;bottom:20px;z-index:4;
  display:grid;width:44px;height:44px;place-items:center;
  border:1px solid currentColor;border-radius:50%;
  font-size:16px;font-style:normal;transition:transform .2s ease
}
.portalpanel:hover .portalarrow{transform:translateX(3px)}
.portalnote{
  position:absolute;right:22px;top:26px;z-index:3;
  max-width:170px;color:#846b50;
  font:600 26px/1.02 "Caveat",cursive;
  transform:rotate(-5deg)
}

.portalcontact{
  display:flex;width:min(100%,1320px);margin:20px auto 0;
  align-items:center;justify-content:space-between;gap:20px;
  padding:18px 0 4px;color:#3a352e
}
.portalcontact strong{font:400 28px/1.05 var(--serif)}
.portalcontact a{
  color:#0b4a42;font:800 10px/1 var(--sans);
  letter-spacing:.12em;text-transform:uppercase;text-decoration:none
}
.portalcontact b{font-weight:400}

.portalfooter{
  display:grid!important;grid-template-columns:1.3fr 1fr .8fr;
  gap:28px 44px;align-items:start;
  padding:34px clamp(22px,5vw,72px) 30px;
  color:#edf3ef;background:#071f1d;
  border-top:1px solid rgb(255 255 255 / 10%)
}
.portalfooter-brand{display:grid;gap:6px}
.portalfooter-brand strong{font:400 27px/1 var(--serif)}
.portalfooter-brand span{color:#c0d5ce;font:700 9px/1.2 var(--sans);letter-spacing:.16em;text-transform:uppercase}
.portalfooter-brand em{margin-top:10px;color:#d7e5df;font:600 25px/1 "Caveat",cursive}
.portalfooter nav,.portalfooter-meta{display:grid;gap:8px}
.portalfooter b{color:#d6b06d;font:800 9px/1 var(--sans);letter-spacing:.16em;text-transform:uppercase}
.portalfooter a{color:#fff;font:600 11px/1.35 var(--sans);text-decoration:none}
.portalfooter-meta span{margin-top:5px;color:#b9cbc5;font-size:9px}

@media(max-width:1050px) and (min-width:801px){
  .portalhero{grid-template-columns:1fr 44%;gap:24px}
  .portalhero h1{font-size:64px}
  .portalhero-copy{padding-right:10px}
  .portalgrid{grid-template-columns:1fr 1fr;grid-template-areas:"report report" "opinion opinion" "thoughts photo"}
  .portalcopy,.portal-reporting .portalcopy,.portal-opinion .portalcopy,.portal-photography .portalcopy{max-width:78%}
}

@media(max-width:800px){
  .portalnav{height:58px;padding:0 16px;color:#f2ece2;background:#0b0d0c;border-bottom-color:rgb(255 255 255 / 9%)}
  .portalbrand strong{font-size:20px}
  .portalbrand small{font-size:6px;color:rgb(255 255 255 / 62%)}
  .portalnavlinks{display:none}
  .portalnav:after{content:"";width:24px;height:15px;border-top:2px solid currentColor;border-bottom:2px solid currentColor}

  .portalhero{display:block;min-height:0;padding:20px 16px 8px}
  .portalhero-copy{padding:0}
  .portalhero h1{max-width:none;font-size:52px}
  .portalhero-deck{font-size:16px}
  .portalhero-script{font-size:28px}
  .portalhero-actions{gap:8px;margin-top:20px}
  .portalhero-actions a{min-width:0;flex:1;font-size:10px;padding-inline:13px}
  .portalhero-visual{min-height:360px;margin-top:18px}
  .portalhero-panel{inset:72px 0 0 23%;border-radius:24px}
  .portalhero-panel p{right:18px;top:20px;width:130px;font-size:20px}
  .portalhero-panel span{right:18px;bottom:18px;font-size:6.5px}
  .portalhero-photo{width:min(320px,78vw);padding:9px;border-radius:18px}
  .portalhero-photo:before{border-radius:18px}
  .portalhero-photo picture{border-radius:13px}
  .portalhero-photo figcaption{left:17px;bottom:17px;font-size:21px}

  .portalwork{padding:14px 14px 30px}
  .portalintro{display:block;width:100%;padding:10px 2px 18px}
  .portalintro h2{font-size:40px}
  .portalintro p{margin-top:10px;font-size:14px}
  .portalintro-link{margin-top:9px}

  .portalgrid{grid-template-columns:1fr;grid-template-areas:"report" "opinion" "thoughts" "photo";gap:12px}
  .portalpanel,.portal-reporting,.portal-opinion,.portal-thoughts,.portal-photography{min-height:230px;border-radius:22px;padding:18px}
  .portal-reporting,.portal-opinion{min-height:260px}
  .portalcopy,.portal-reporting .portalcopy,.portal-opinion .portalcopy,.portal-photography .portalcopy{max-width:none;padding-right:45px}
  .portalcopy strong{font-size:33px}
  .portalcopy small{font-size:12px}
  .portalnumber{left:16px;top:15px;width:30px;height:30px;font-size:8px}
  .portalarrow{right:16px;bottom:16px;width:36px;height:36px;font-size:14px}
  .portalnote{top:18px;right:16px;max-width:120px;font-size:21px}

  .portalcontact{display:block;margin-top:16px}
  .portalcontact strong{display:block;margin-bottom:10px;font-size:24px}
  .portalfooter{grid-template-columns:1fr;gap:22px;padding:28px 18px}
}

@media(max-width:420px){
  .portalhero h1{font-size:46px}
  .portalhero-deck{font-size:15px}
  .portalhero-visual{min-height:330px}
  .portalhero-photo{width:min(292px,80vw)}
  .portalintro h2{font-size:36px}
  .portalpanel,.portal-reporting,.portal-opinion,.portal-thoughts,.portal-photography{min-height:220px}
  .portal-reporting,.portal-opinion{min-height:245px}
  .portalcopy strong{font-size:30px}
  .portalcopy small{font-size:11px}
}
""".strip()


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
    print(f"Homepage polish: compact_hero=1, balanced_work_grid=1, compact_footer=1, asset_version={ASSET_VERSION}, versioned_pages={versioned_pages}, css_isolated=1, inline_critical=1")


if __name__ == "__main__":
    main()
