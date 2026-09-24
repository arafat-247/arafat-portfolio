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
ASSET_VERSION = "19.0.0"

HOME_CSS = r"""
/* Four-portal homepage v19.0 */
body.home{background:#111}
body.home .identity,
body.home .desktophead,
body.home .mobilehead,
body.home .mobilemenu,
body.home .menubackdrop,
body.home footer{display:none!important}
body.home .right{margin-left:0;min-height:100vh;background:#111}
body.home main{min-height:100vh;background:#111}
body.home .portalhome{
  position:relative;
  display:grid;
  width:100%;
  min-height:100vh;
  overflow:hidden;
  grid-template-columns:38% 62%;
  grid-template-rows:74px minmax(360px,48vh) minmax(300px,42vh);
  color:#f7f1e7;
  background:#0b0c0b;
}
.portalnav{
  position:absolute;
  z-index:20;
  inset:0 0 auto 0;
  display:flex;
  height:74px;
  align-items:center;
  justify-content:space-between;
  padding:0 clamp(28px,5vw,78px);
  color:#f3eee5;
  background:linear-gradient(180deg,rgb(4 5 5 / 80%),rgb(4 5 5 / 22%),transparent);
}
.portalbrand{display:grid;gap:1px;text-decoration:none}
.portalbrand strong{font:400 26px/1 var(--serif);letter-spacing:-.025em}
.portalbrand small{font:700 8px/1.2 var(--sans);letter-spacing:.22em;text-transform:uppercase;opacity:.72}
.portalnavlinks{display:flex;align-items:center;gap:clamp(16px,2vw,30px)}
.portalnavlinks a{
  position:relative;
  padding:27px 0 21px;
  color:inherit;
  font:700 10px/1 var(--sans);
  letter-spacing:.08em;
  text-transform:uppercase;
  text-decoration:none;
  opacity:.76;
}
.portalnavlinks a:hover,.portalnavlinks a[aria-current=page]{opacity:1}
.portalnavlinks a[aria-current=page]:after{
  content:"";
  position:absolute;
  left:0;right:0;bottom:15px;height:2px;
  background:#f3eee5;
}
.portalintro{
  position:relative;
  z-index:8;
  grid-column:1;
  grid-row:1/3;
  display:flex;
  min-width:0;
  flex-direction:column;
  justify-content:center;
  padding:110px clamp(30px,5vw,76px) 54px;
  background:
    radial-gradient(circle at 100% 6%,rgb(255 255 255 / 6%),transparent 24%),
    linear-gradient(165deg,#090b0b 0%,#111615 60%,#141311 100%);
}
.portalintro:after{
  content:"";
  position:absolute;
  z-index:-1;
  right:-18%;
  bottom:-18%;
  width:74%;
  aspect-ratio:1;
  border-radius:48% 52% 42% 58%/54% 38% 62% 46%;
  background:#8f271c;
  opacity:.88;
  transform:rotate(-12deg);
}
.portalkicker{
  margin-bottom:14px;
  font:800 10px/1 var(--sans);
  letter-spacing:.34em;
  text-transform:uppercase;
}
.portalintro h1{
  max-width:520px;
  margin:0;
  font:400 clamp(58px,6vw,102px)/.88 var(--serif);
  letter-spacing:-.055em;
}
.portalintro p{
  max-width:410px;
  margin:24px 0 0;
  color:rgb(255 255 255 / 82%);
  font:400 17px/1.48 var(--serif);
}
.portalintro-link{
  width:max-content;
  margin-top:28px;
  padding:11px 0 6px;
  border-bottom:1px solid currentColor;
  font:700 11px/1 var(--sans);
  text-decoration:none;
}
.portalintro-link b{margin-left:12px;font-weight:400}

.portalpanel{
  position:relative;
  isolation:isolate;
  overflow:hidden;
  display:flex;
  min-width:0;
  align-items:flex-end;
  padding:30px clamp(26px,3.4vw,52px) 30px;
  color:#fff;
  text-decoration:none;
}
.portalpanel:before{
  content:"";
  position:absolute;
  inset:0;
  z-index:-1;
  pointer-events:none;
}
.portalpanel .portalimage{
  position:absolute;
  inset:0;
  z-index:-3;
  width:100%;
  height:100%;
  object-fit:cover;
}
.portal-reporting{
  grid-column:2;
  grid-row:1/3;
  padding-top:110px;
  align-items:center;
}
.portal-reporting:before{
  background:
    linear-gradient(90deg,rgb(247 241 231 / 95%) 0 48%,rgb(247 241 231 / 64%) 66%,rgb(247 241 231 / 5%) 100%);
}
.portal-reporting .portalimage{filter:grayscale(.95) contrast(1.02) brightness(.9)}
.portal-reporting .portalcopy,
.portal-reporting .portalnumber,
.portal-reporting .portalarrow{color:#111}
.portal-reporting .portalcopy{max-width:360px;margin-left:5%}
.portal-reporting .portalcopy strong{font-size:clamp(42px,4.3vw,72px)}
.portal-reporting .portalarrow{border-color:rgb(17 17 17 / 45%)}

.portal-opinion{
  grid-column:1;
  grid-row:3;
  z-index:6;
  background:#8b281d;
  border-top-right-radius:52% 42%;
}
.portal-opinion:before{
  background:
    linear-gradient(180deg,rgb(121 28 18 / 32%),rgb(92 17 12 / 82%)),
    linear-gradient(90deg,#8b281d 0%,rgb(139 40 29 / 86%) 56%,rgb(139 40 29 / 28%) 100%);
}
.portal-opinion .portalimage{
  filter:grayscale(1) sepia(.7) hue-rotate(330deg) saturate(2.1) contrast(1.05) brightness(.58);
  mix-blend-mode:multiply;
}
.portalquote{
  position:absolute;
  right:8%;
  top:3%;
  color:rgb(255 228 210 / 12%);
  font:400 220px/.8 Georgia,serif;
}
.portal-thoughts{
  grid-column:1;
  grid-row:4;
  min-height:300px;
  color:#111;
  background:#efe9df;
  border-top-right-radius:48% 36%;
}
.portal-thoughts:before{
  background:
    linear-gradient(90deg,#f0e9df 0%,rgb(240 233 223 / 93%) 62%,rgb(240 233 223 / 62%) 100%);
}
.portal-thoughts .portalimage{
  filter:grayscale(1) sepia(.18) opacity(.28) contrast(.9);
  mix-blend-mode:multiply;
}
.portal-thoughts .portalcopy,.portal-thoughts .portalnumber,.portal-thoughts .portalarrow{color:#111}
.portal-thoughts .portalarrow{border-color:rgb(17 17 17 / 45%)}
.portalnote{
  position:absolute;
  right:10%;
  top:20%;
  color:#6e6152;
  font:600 clamp(20px,2vw,30px)/1.05 "Caveat",cursive;
  transform:rotate(-8deg);
}
.portal-photography{
  grid-column:2;
  grid-row:3/5;
  min-height:600px;
  align-items:flex-end;
}
.portal-photography:before{
  background:linear-gradient(180deg,rgb(4 7 6 / 6%) 15%,rgb(4 7 6 / 66%) 78%,rgb(4 7 6 / 88%) 100%);
}
.portal-photography .portalimage{filter:saturate(.78) brightness(.82)}

.portalnumber{
  position:absolute;
  left:clamp(24px,3vw,46px);
  top:clamp(22px,3vw,42px);
  z-index:2;
  font:700 10px/1 var(--sans);
  letter-spacing:.16em;
}
.portalcopy{position:relative;z-index:2;display:block;max-width:440px}
.portalcopy strong{
  display:block;
  font:400 clamp(38px,4vw,68px)/.94 var(--serif);
  letter-spacing:-.04em;
}
.portalcopy small{
  display:block;
  max-width:390px;
  margin-top:11px;
  color:currentColor;
  opacity:.82;
  font:400 15px/1.38 var(--serif);
}
.portalarrow{
  position:absolute;
  right:clamp(22px,3vw,44px);
  bottom:clamp(22px,3vw,40px);
  z-index:3;
  display:grid;
  width:42px;height:42px;
  place-items:center;
  border:1px solid rgb(255 255 255 / 66%);
  border-radius:50%;
  font-size:18px;
  font-style:normal;
  transition:transform .2s ease,background .2s ease;
}
.portalpanel:hover .portalarrow{transform:translateX(4px);background:rgb(255 255 255 / 10%)}
.portalpanel:hover .portalimage{transform:scale(1.015)}
.portalimage{transition:transform .5s ease}

/* create the broad asymmetric overlaps seen in the reference */
.portal-reporting{clip-path:polygon(0 0,100% 0,100% 78%,76% 87%,43% 92%,0 79%)}
.portal-opinion{margin-top:-13vh;min-height:350px;clip-path:polygon(0 8%,100% 0,100% 84%,0 100%)}
.portal-thoughts{margin-top:-4vh;min-height:360px;clip-path:polygon(0 20%,100% 0,100% 100%,0 100%)}
.portal-photography{margin-top:-10vh;clip-path:polygon(0 18%,100% 0,100% 100%,22% 100%,0 76%)}

@media(min-width:801px){
  body.home .portalhome{grid-template-rows:74px minmax(440px,54vh) minmax(340px,42vh) minmax(330px,40vh)}
}

@media(max-width:1100px) and (min-width:801px){
  .portalnav{padding-inline:30px}
  .portalnavlinks{gap:15px}
  .portalnavlinks a{font-size:9px}
  .portalintro{padding-left:36px;padding-right:26px}
  .portalintro h1{font-size:clamp(54px,6vw,76px)}
  .portalintro p{font-size:15px}
  .portal-reporting .portalcopy{margin-left:0}
  .portalcopy small{font-size:13px}
}

/* mobile: same identity, rebuilt as a stacked flowing sequence */
@media(max-width:800px){
  body.home .right,body.home main{min-height:100vh}
  body.home .portalhome{
    display:block;
    min-height:100vh;
    overflow:hidden;
    background:#090b0b;
  }
  .portalnav{
    position:relative;
    height:58px;
    padding:0 16px;
    background:#090b0b;
  }
  .portalbrand strong{font-size:20px}
  .portalbrand small{font-size:6.5px}
  .portalnavlinks{display:none}
  .portalnav:after{
    content:"";
    width:25px;height:16px;
    border-top:2px solid #fff;border-bottom:2px solid #fff;
  }
  .portalintro{
    min-height:280px;
    padding:44px 22px 72px;
    justify-content:flex-start;
  }
  .portalintro:after{
    right:-34%;
    bottom:-25%;
    width:105%;
    opacity:.88;
  }
  .portalkicker{font-size:8px;letter-spacing:.28em}
  .portalintro h1{
    max-width:320px;
    font-size:clamp(44px,13vw,62px);
    line-height:.9;
  }
  .portalintro p{max-width:300px;margin-top:16px;font-size:14px;line-height:1.4}
  .portalintro-link{margin-top:18px;font-size:10px}

  .portalpanel,
  .portal-reporting,
  .portal-opinion,
  .portal-thoughts,
  .portal-photography{
    display:flex;
    min-height:230px;
    margin:0;
    padding:28px 22px 24px;
    align-items:flex-end;
    clip-path:none;
    border-radius:0;
  }
  .portal-reporting{min-height:290px}
  .portal-reporting:before{
    background:linear-gradient(90deg,rgb(247 241 231 / 94%) 0 52%,rgb(247 241 231 / 50%) 75%,rgb(247 241 231 / 8%) 100%);
  }
  .portal-reporting .portalcopy{margin-left:0;max-width:67%}
  .portal-reporting .portalcopy strong{font-size:40px}
  .portal-opinion{min-height:230px;background:#8b281d}
  .portal-opinion:before{
    background:linear-gradient(90deg,rgb(126 31 20 / 96%) 0 58%,rgb(126 31 20 / 58%) 100%);
  }
  .portal-thoughts{
    min-height:240px;
    background:#efe9df;
  }
  .portal-thoughts:before{
    background:linear-gradient(90deg,#efe9df 0 62%,rgb(239 233 223 / 64%) 100%);
  }
  .portal-photography{min-height:270px}
  .portalnumber{left:20px;top:19px;font-size:8px}
  .portalcopy{max-width:72%}
  .portalcopy strong{font-size:34px}
  .portalcopy small{margin-top:8px;font-size:12px;line-height:1.34}
  .portalarrow{right:18px;bottom:19px;width:36px;height:36px;font-size:15px}
  .portalquote{font-size:145px;right:5%;top:4%}
  .portalnote{right:8%;top:18%;font-size:20px}
}

@media(max-width:420px){
  .portalintro{min-height:260px;padding-inline:18px}
  .portalintro h1{font-size:43px}
  .portalintro p{font-size:13px}
  .portalpanel,
  .portal-reporting,
  .portal-opinion,
  .portal-thoughts,
  .portal-photography{padding-inline:18px}
  .portal-reporting{min-height:260px}
  .portalcopy strong{font-size:31px}
  .portal-reporting .portalcopy strong{font-size:36px}
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
    print(f"Homepage polish: four_portal_home=1, asset_version={ASSET_VERSION}, versioned_pages={versioned_pages}, css_isolated=1, inline_critical=1")


if __name__ == "__main__":
    main()
