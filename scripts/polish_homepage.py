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
ASSET_VERSION = "19.1.0"

HOME_CSS = r"""
/* Homepage v19.1 — portrait hero + approved reference-art portals + full footer */
body.home{background:#0b0c0b}
body.home .identity,
body.home .desktophead,
body.home .mobilehead,
body.home .mobilemenu,
body.home .menubackdrop,
body.home .right>footer{display:none!important}
body.home .right{margin-left:0;min-height:100vh;background:#0b0c0b}
body.home main{min-height:100vh;background:#0b0c0b}
body.home .portalhome{width:100%;overflow:hidden;background:#0b0c0b;color:#f6f0e6}

/* top navigation */
.portalnav{
  position:absolute;
  z-index:50;
  inset:0 0 auto 0;
  display:flex;
  height:72px;
  align-items:center;
  justify-content:space-between;
  padding:0 clamp(24px,5vw,78px);
  color:#161816;
  background:rgb(244 239 230 / 94%);
  border-bottom:1px solid rgb(19 23 21 / 12%);
  backdrop-filter:blur(12px);
}
.portalbrand{display:grid;gap:2px;text-decoration:none}
.portalbrand strong{font:400 26px/1 var(--serif);letter-spacing:-.03em}
.portalbrand small{font:800 7px/1.2 var(--sans);letter-spacing:.22em;text-transform:uppercase;opacity:.62}
.portalnavlinks{display:flex;align-items:center;gap:clamp(14px,1.65vw,26px)}
.portalnavlinks a{
  position:relative;
  padding:28px 0 22px;
  color:inherit;
  font:750 9px/1 var(--sans);
  letter-spacing:.08em;
  text-transform:uppercase;
  text-decoration:none;
  opacity:.66;
}
.portalnavlinks a:hover,.portalnavlinks a[aria-current=page]{opacity:1}
.portalnavlinks a[aria-current=page]:after{
  content:"";position:absolute;left:0;right:0;bottom:16px;height:2px;background:#151816
}

/* hero */
.portalhero{
  display:grid;
  min-height:610px;
  grid-template-columns:minmax(0,43%) minmax(0,57%);
  padding-top:72px;
  color:#151816;
  background:#f1ebe1;
}
.portalhero-copy{
  display:flex;
  min-width:0;
  flex-direction:column;
  justify-content:center;
  padding:54px clamp(34px,5.2vw,82px) 54px;
}
.portalkicker{
  display:block;
  margin-bottom:14px;
  color:#7c1e16;
  font:850 9px/1 var(--sans);
  letter-spacing:.3em;
  text-transform:uppercase;
}
.portalhero h1{
  max-width:620px;
  margin:0;
  font:400 clamp(70px,7.2vw,118px)/.82 var(--serif);
  letter-spacing:-.065em;
}
.portalhero-deck{
  max-width:620px;
  margin:24px 0 0;
  color:#353833;
  font:400 clamp(17px,1.45vw,21px)/1.48 var(--serif);
}
.portalhero-actions{
  display:flex;
  flex-wrap:wrap;
  gap:12px 24px;
  margin-top:28px;
}
.portalhero-actions a{
  display:inline-flex;
  min-height:46px;
  align-items:center;
  justify-content:space-between;
  gap:24px;
  padding:0 20px;
  border:1px solid #1d211f;
  color:#161816;
  font:750 12px/1 var(--sans);
  text-decoration:none;
}
.portalhero-actions a b{font-weight:400}
.portalhero-actions .portalhero-primary{color:#fff;background:#101312}
.portalhero-actions a:hover{transform:translateY(-1px)}
.portalhero-photo{
  position:relative;
  min-width:0;
  min-height:538px;
  margin:0;
  overflow:hidden;
  background:#161817;
}
.portalhero-photo picture,.portalhero-photo img{display:block;width:100%;height:100%}
.portalhero-photo img{object-fit:cover;object-position:center 42%;filter:grayscale(1) contrast(1.04)}
.portalhero-photo:after{
  content:"";position:absolute;inset:0;
  background:linear-gradient(90deg,rgb(17 19 18 / 8%),transparent 38%,rgb(17 19 18 / 8%));
  pointer-events:none
}
.portalhero-photo figcaption{
  position:absolute;
  z-index:2;
  right:28px;
  bottom:24px;
  color:#fff;
  font:750 8px/1 var(--sans);
  letter-spacing:.2em;
  text-transform:uppercase;
}

/* work section */
.portalwork{position:relative;background:#0b0c0b}
.portalintro{
  display:grid;
  width:min(100% - 72px,1420px);
  margin:0 auto;
  padding:44px 0 32px;
  grid-template-columns:minmax(0,1.25fr) minmax(280px,.75fr);
  gap:20px 52px;
  align-items:end;
  color:#f4eee3;
}
.portalintro .portalkicker{grid-column:1/-1;margin:0;color:#e6b39e}
.portalintro h2{
  margin:0;
  font:400 clamp(48px,5.4vw,82px)/.9 var(--serif);
  letter-spacing:-.055em;
}
.portalintro p{
  margin:0 0 9px;
  color:rgb(255 255 255 / 72%);
  font:400 16px/1.48 var(--serif);
}
.portalintro-link{
  display:inline-flex;
  width:max-content;
  gap:12px;
  padding-bottom:5px;
  border-bottom:1px solid currentColor;
  color:#fff;
  font:750 11px/1 var(--sans);
  text-decoration:none;
}
.portalintro-link b{font-weight:400}

.portalgrid{
  position:relative;
  display:grid;
  min-height:1050px;
  grid-template-columns:52% 48%;
  grid-template-rows:420px 330px 300px;
  overflow:hidden;
  background:#0b0c0b;
}
.portalpanel{
  position:relative;
  isolation:isolate;
  overflow:hidden;
  display:flex;
  min-width:0;
  align-items:flex-end;
  padding:30px clamp(24px,3.4vw,52px) 34px;
  color:#fff;
  text-decoration:none;
}
.portalpanel:after{
  content:"";position:absolute;inset:0;z-index:-1;pointer-events:none
}
.portalart,.portalimage{
  position:absolute;inset:0;z-index:-3;width:100%;height:100%;
}
.portalart{
  background-image:url("assets/home/portal-reference-sprite.webp");
  background-repeat:no-repeat;
  background-size:100% 300%;
}
.portalart-reporting{background-position:center top}
.portalart-opinion{background-position:center 50%}
.portalart-thoughts{background-position:center bottom}
.portalimage{object-fit:cover;transition:transform .45s ease}
.portalpanel:hover .portalimage{transform:scale(1.018)}

.portal-reporting{
  grid-column:1/3;
  grid-row:1;
  color:#111;
  clip-path:polygon(0 0,100% 0,100% 85%,78% 100%,39% 91%,0 100%);
  padding-left:clamp(34px,6vw,96px);
}
.portal-reporting:after{
  background:linear-gradient(90deg,rgb(241 235 225 / 96%) 0 34%,rgb(241 235 225 / 60%) 51%,rgb(241 235 225 / 2%) 76%);
}
.portal-reporting .portalcopy{max-width:420px}
.portal-reporting .portalcopy strong{font-size:clamp(48px,5vw,78px)}
.portal-reporting .portalnumber,.portal-reporting .portalarrow{color:#111}
.portal-reporting .portalarrow{border-color:rgb(17 17 17 / 48%)}

.portal-opinion{
  grid-column:1;
  grid-row:2;
  z-index:5;
  margin-top:-44px;
  background:#7e1e16;
  clip-path:polygon(0 8%,100% 0,100% 86%,0 100%);
}
.portal-opinion:after{
  background:linear-gradient(90deg,rgb(112 24 17 / 92%) 0 48%,rgb(112 24 17 / 45%) 100%);
}
.portalquote{
  position:absolute;right:8%;top:1%;z-index:0;
  color:rgb(255 226 211 / 16%);
  font:400 190px/.8 Georgia,serif
}

.portal-thoughts{
  grid-column:1;
  grid-row:3;
  z-index:6;
  margin-top:-36px;
  color:#111;
  background:#eee7dc;
  clip-path:polygon(0 16%,100% 0,100% 100%,0 100%);
}
.portal-thoughts:after{
  background:linear-gradient(90deg,rgb(239 233 223 / 98%) 0 54%,rgb(239 233 223 / 56%) 100%);
}
.portal-thoughts .portalnumber,.portal-thoughts .portalcopy,.portal-thoughts .portalarrow{color:#111}
.portal-thoughts .portalarrow{border-color:rgb(17 17 17 / 45%)}
.portalnote{
  position:absolute;right:8%;top:22%;z-index:2;
  color:#6c5f50;
  font:600 clamp(22px,2.2vw,32px)/1.02 "Caveat",cursive;
  transform:rotate(-7deg)
}

.portal-photography{
  grid-column:2;
  grid-row:2/4;
  min-height:630px;
  margin-top:-72px;
  clip-path:polygon(0 15%,100% 0,100% 100%,13% 100%,0 78%);
}
.portal-photography:after{
  background:linear-gradient(180deg,rgb(5 8 7 / 7%) 12%,rgb(5 8 7 / 58%) 76%,rgb(5 8 7 / 86%) 100%)
}
.portal-photography .portalimage{filter:saturate(.82) brightness(.82)}

.portalnumber{
  position:absolute;z-index:3;left:clamp(24px,3vw,46px);top:clamp(22px,3vw,40px);
  font:800 9px/1 var(--sans);letter-spacing:.18em
}
.portalcopy{position:relative;z-index:3;display:block;max-width:430px}
.portalcopy strong{
  display:block;
  font:400 clamp(38px,4.1vw,66px)/.92 var(--serif);
  letter-spacing:-.045em
}
.portalcopy small{
  display:block;
  max-width:390px;
  margin-top:10px;
  color:currentColor;
  opacity:.85;
  font:400 14px/1.4 var(--serif)
}
.portalarrow{
  position:absolute;z-index:4;right:clamp(20px,3vw,42px);bottom:clamp(20px,3vw,38px);
  display:grid;width:42px;height:42px;place-items:center;
  border:1px solid rgb(255 255 255 / 65%);border-radius:50%;
  font-size:17px;font-style:normal;transition:transform .2s ease
}
.portalpanel:hover .portalarrow{transform:translateX(4px)}

/* footer */
.portalfooter{
  display:grid!important;
  min-height:0;
  grid-template-columns:1fr 1.2fr auto;
  gap:28px 56px;
  align-items:start;
  padding:44px clamp(28px,5vw,78px) 38px;
  color:#e7e2d9;
  background:#101312;
  border-top:1px solid rgb(255 255 255 / 12%);
}
.portalfooter-brand{display:grid;gap:7px}
.portalfooter-brand strong{font:400 27px/1 var(--serif)}
.portalfooter-brand span{color:rgb(255 255 255 / 56%);font-size:11px}
.portalfooter nav{display:flex;flex-wrap:wrap;gap:10px 24px}
.portalfooter nav a,.portalfooter-meta a{
  color:#fff;font-size:10px;font-weight:750;text-decoration:none
}
.portalfooter-meta{display:flex;flex-wrap:wrap;justify-content:flex-end;gap:10px 16px;color:rgb(255 255 255 / 52%);font-size:9px}

/* tablet */
@media(max-width:1100px) and (min-width:801px){
  .portalnav{padding-inline:28px}
  .portalnavlinks{gap:13px}
  .portalnavlinks a{font-size:8px}
  .portalhero{grid-template-columns:46% 54%;min-height:560px}
  .portalhero h1{font-size:72px}
  .portalhero-copy{padding-inline:36px}
  .portalgrid{min-height:940px;grid-template-rows:380px 300px 260px}
  .portalcopy small{font-size:12px}
}

/* mobile */
@media(max-width:800px){
  body.home .portalhome{background:#0b0c0b}
  .portalnav{
    position:relative;
    height:58px;
    padding:0 16px;
    color:#f4eee3;
    background:#0b0c0b;
    border-bottom-color:rgb(255 255 255 / 10%);
  }
  .portalbrand strong{font-size:20px}
  .portalbrand small{font-size:6px;color:rgb(255 255 255 / 60%)}
  .portalnavlinks{display:none}
  .portalnav:after{
    content:"";display:block;width:24px;height:15px;
    border-top:2px solid currentColor;border-bottom:2px solid currentColor
  }

  .portalhero{
    display:flex;
    min-height:0;
    padding:0;
    flex-direction:column;
    background:#f1ebe1
  }
  .portalhero-photo{
    order:1;
    width:100%;
    min-height:0;
    height:min(92vw,420px)
  }
  .portalhero-photo figcaption{right:16px;bottom:14px;font-size:6px}
  .portalhero-copy{
    order:2;
    padding:26px 20px 30px
  }
  .portalhero h1{
    max-width:none;
    font-size:clamp(48px,15vw,66px);
    line-height:.86
  }
  .portalhero-deck{margin-top:16px;font-size:14px;line-height:1.45}
  .portalhero-actions{margin-top:20px;gap:8px}
  .portalhero-actions a{min-height:42px;flex:1;padding-inline:13px;font-size:10px}

  .portalintro{
    display:block;
    width:auto;
    margin:0 18px;
    padding:30px 0 22px
  }
  .portalintro .portalkicker{margin-bottom:8px}
  .portalintro h2{font-size:42px;line-height:.92}
  .portalintro p{margin-top:12px;font-size:13px}
  .portalintro-link{margin-top:12px;font-size:10px}

  .portalgrid{
    display:block;
    min-height:0;
    overflow:hidden
  }
  .portalpanel,
  .portal-reporting,
  .portal-opinion,
  .portal-thoughts,
  .portal-photography{
    display:flex;
    min-height:220px;
    margin:0;
    padding:24px 20px 22px;
    clip-path:none
  }
  .portal-reporting{min-height:280px}
  .portal-reporting:after{
    background:linear-gradient(90deg,rgb(241 235 225 / 97%) 0 52%,rgb(241 235 225 / 55%) 74%,rgb(241 235 225 / 7%) 100%)
  }
  .portal-opinion{min-height:220px}
  .portal-thoughts{min-height:230px}
  .portal-photography{min-height:270px}
  .portalnumber{left:19px;top:17px;font-size:8px}
  .portalcopy{max-width:72%}
  .portal-reporting .portalcopy{max-width:66%}
  .portalcopy strong{font-size:32px}
  .portal-reporting .portalcopy strong{font-size:38px}
  .portalcopy small{font-size:11px;line-height:1.34}
  .portalarrow{right:17px;bottom:17px;width:34px;height:34px;font-size:14px}
  .portalquote{font-size:130px}
  .portalnote{right:7%;top:19%;font-size:19px}

  .portalfooter{
    grid-template-columns:1fr;
    gap:22px;
    padding:30px 20px
  }
  .portalfooter nav{gap:9px 18px}
  .portalfooter-meta{justify-content:flex-start}
}

@media(max-width:420px){
  .portalhero-photo{height:88vw;max-height:370px}
  .portalhero-copy{padding-inline:17px}
  .portalhero h1{font-size:48px}
  .portalintro{margin-inline:16px}
  .portalintro h2{font-size:38px}
  .portalpanel,
  .portal-reporting,
  .portal-opinion,
  .portal-thoughts,
  .portal-photography{padding-inline:18px}
  .portal-reporting{min-height:250px}
  .portalcopy strong{font-size:29px}
  .portal-reporting .portalcopy strong{font-size:35px}
  .portalcopy small{font-size:10.5px}
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
    print(f"Homepage polish: hero=1, reference_portals=1, footer=1, asset_version={ASSET_VERSION}, versioned_pages={versioned_pages}, css_isolated=1, inline_critical=1")


if __name__ == "__main__":
    main()
