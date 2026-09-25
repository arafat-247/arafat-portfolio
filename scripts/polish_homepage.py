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
ASSET_VERSION = "20.0.2"

HOME_CSS = r"""
/* Homepage v20.0.2 — approved flowing editorial composition */
body.home{background:#111}
body.home .identity,
body.home .desktophead,
body.home .mobilehead,
body.home .mobilemenu,
body.home .menubackdrop,
body.home .right>footer{display:none!important}
body.home .right{width:100%!important;max-width:none!important;margin-left:0!important;min-height:100vh;background:#111}
body.home main{width:100%!important;max-width:none!important;min-height:100vh;background:#111}
body.home .portalhome{
  width:calc(100% - 28px);
  margin:14px auto 22px;
  overflow:hidden;
  border-radius:28px;
  background:#f4eee4;
  color:#111;
  box-shadow:0 14px 50px rgb(0 0 0 / 22%);
}

/* Header */
.portalnav{
  display:flex;min-height:62px;align-items:center;justify-content:space-between;
  padding:0 clamp(24px,5vw,70px);
  color:#171512;background:#f4eee4;
  border-bottom:1px solid rgb(17 17 17 / 11%)
}
.portalbrand{display:grid;gap:2px;text-decoration:none}
.portalbrand strong{font:400 23px/1 var(--serif);letter-spacing:-.03em}
.portalbrand small{font:800 7px/1.1 var(--sans);letter-spacing:.25em;text-transform:uppercase;opacity:.62}
.portalnavlinks{display:flex;align-items:center;gap:30px}
.portalmobilemenu{display:none}
.portalnavlinks a{
  position:relative;padding:23px 0 18px;
  color:inherit;font:750 9px/1 var(--sans);
  letter-spacing:.14em;text-transform:uppercase;text-decoration:none;opacity:.72
}
.portalnavlinks a:hover,.portalnavlinks a[aria-current=page]{opacity:1}
.portalnavlinks a[aria-current=page]:after{content:"";position:absolute;left:0;right:0;bottom:12px;height:1.5px;background:#171512}

/* Hero */
.portalhero{
  position:relative;
  display:grid;
  min-height:470px;
  grid-template-columns:minmax(0,1fr) minmax(520px,48%);
  align-items:center;
  padding:22px clamp(24px,5vw,70px) 28px;
  background:#f4eee4
}
.portalhero-copy{position:relative;z-index:3;padding:10px 0}
.portalkicker{
  display:block;margin-bottom:12px;color:#a52918;
  font:850 9px/1 var(--sans);letter-spacing:.25em;text-transform:uppercase
}
.portalhero h1{
  margin:0 0 14px;
  font:400 clamp(66px,6.2vw,96px)/.83 var(--serif);
  letter-spacing:-.055em
}
.portalhero h1 em{display:block;font-style:italic}
.portalhero-deck{
  max-width:620px;margin:0;color:#302d28;
  font:400 clamp(16px,1.25vw,19px)/1.42 var(--serif)
}
.portalhero-script{
  margin:15px 0 0;color:#b87b46;
  font:600 clamp(24px,2vw,31px)/1 "Caveat",cursive
}
.portalhero-actions{display:flex;gap:12px;flex-wrap:wrap;margin-top:20px}
.portalhero-actions a{
  display:inline-flex;min-width:174px;min-height:42px;
  align-items:center;justify-content:space-between;gap:20px;
  padding:0 18px;border:1px solid #153d38;border-radius:999px;
  color:#171512;font:750 11px/1 var(--sans);text-decoration:none
}
.portalhero-actions .portalhero-primary{color:#fff;background:#0b5b50;border-color:#0b5b50}
.portalhero-actions a b{font-weight:400}
.portalhero-visual{position:relative;min-height:410px}
.portalhero-panel{
  position:absolute;z-index:1;inset:42px 0 36px 42%;
  overflow:hidden;border-radius:0 34px 34px 0;
  background:linear-gradient(180deg,#0d6a5f 0,#075248 100%);
  clip-path:polygon(0 0,100% 11%,100% 88%,0 100%)
}
.portalhero-panel p{
  position:absolute;right:12%;top:19%;width:220px;margin:0;
  color:#fff;font:italic 400 clamp(30px,2.7vw,42px)/.97 var(--serif)
}
.portalhero-panel span{
  position:absolute;right:12%;bottom:13%;
  color:#fff;font:800 7px/1 var(--sans);
  letter-spacing:.28em;text-transform:uppercase
}
.portalhero-photo{
  position:absolute;z-index:2;inset:0 23% 0 0;margin:0
}
.portalhero-photo picture,.portalhero-photo img{display:block;width:100%;height:100%}
.portalhero-photo img{
  object-fit:cover;object-position:center 42%;
  filter:grayscale(1) contrast(1.04)
}
.portalhero-photo:after{
  content:"";position:absolute;inset:0;
  background:linear-gradient(90deg,#f4eee4 0%,transparent 24%,transparent 100%);
  pointer-events:none
}

/* Work: single continuous composition */
.portalwork{
  position:relative;
  margin:0;
  background:#09100e;
  overflow:hidden
}
.portalgrid{
  position:relative;
  width:100%;
  height:clamp(860px,72vw,1040px);
  min-height:860px;
  background:
    radial-gradient(circle at 26% 14%,#1b211f 0,#0c1210 54%,#050807 100%)
}
.portalpanel{
  position:absolute;
  isolation:isolate;
  overflow:hidden;
  color:#fff;text-decoration:none
}
.portalpanel:before{
  content:"";position:absolute;inset:0;z-index:1;pointer-events:none
}
.portalimage{
  position:absolute;inset:0;z-index:0;
  width:100%;height:100%;object-fit:cover
}
.portalart{
  position:absolute;inset:0;z-index:0;
  background-image:url("assets/home/portal-reference-sprite.webp");
  background-repeat:no-repeat;background-size:100% 300%
}
.portalart-opinion{background-position:center 50%}
.portalart-thoughts{background-position:center bottom}

/* reporting top-right */
.portal-reporting{
  z-index:2;
  top:0;right:0;
  width:63%;height:58%;
  color:#111;
  background:#efe9df;
  clip-path:polygon(0 0,100% 0,100% 100%,82% 99%,70% 91%,57% 87%,45% 91%,28% 100%,0 100%)
}
.portal-reporting .portalimage{filter:saturate(.72) brightness(1.04) contrast(.94)}
.portal-reporting:before{
  background:linear-gradient(90deg,rgb(244 238 228 / 96%) 0 22%,rgb(244 238 228 / 58%) 44%,rgb(244 238 228 / 3%) 72%)
}
.portal-reporting .portalcopy{left:15%;top:17%;max-width:360px}
.portal-reporting .portalnumber{left:15%;top:11%}
.portal-reporting .portalarrow{left:15%;bottom:18%;right:auto;color:#111;border-color:rgb(17 17 17 / 55%)}

/* opinion wave */
.portal-opinion{
  z-index:4;
  left:0;top:18%;
  width:59%;height:54%;
  background:#8d150e;
  clip-path:polygon(0 15%,18% 8%,34% 12%,48% 22%,59% 20%,70% 12%,79% 14%,88% 27%,100% 44%,100% 100%,74% 96%,58% 91%,43% 93%,28% 100%,13% 97%,0 88%)
}
.portal-opinion:before{
  background:linear-gradient(180deg,rgb(142 21 13 / 80%),rgb(104 13 8 / 90%))
}
.portal-opinion .portalart{opacity:.74;mix-blend-mode:multiply}
.portal-opinion:after{
  content:"“";position:absolute;right:19%;top:27%;z-index:1;
  color:rgb(255 255 255 / 10%);
  font:400 190px/.7 var(--serif)
}
.portal-opinion .portalcopy{left:8%;top:38%;max-width:310px}
.portal-opinion .portalnumber{left:8%;top:30%}
.portal-opinion .portalarrow{left:8%;bottom:12%;right:auto}

/* thoughts paper */
.portal-thoughts{
  z-index:5;
  left:0;bottom:0;
  width:54%;height:41%;
  color:#12110f;
  background:#f3eee4;
  clip-path:polygon(0 0,54% 0,63% 6%,72% 18%,79% 33%,86% 52%,95% 76%,100% 100%,0 100%)
}
.portal-thoughts:before{
  background:linear-gradient(180deg,rgb(245 240 232 / 8%),rgb(245 240 232 / 5%))
}
.portal-thoughts .portalart{opacity:.96;background-size:100% 300%;background-position:center bottom}
.portal-thoughts .portalcopy{left:6%;bottom:14%;max-width:330px}
.portal-thoughts .portalnumber{left:6%;top:16%}
.portal-thoughts .portalarrow{left:6%;bottom:5%;right:auto;color:#111;border-color:rgb(17 17 17 / 55%)}
.portalnote{
  position:absolute;z-index:4;left:42%;top:20%;
  max-width:180px;color:#705c42;
  font:600 29px/1.02 "Caveat",cursive;
  transform:rotate(-8deg)
}
.portal-thoughts:after{
  content:"";position:absolute;z-index:1;
  width:120px;height:120px;border-radius:50%;
  right:9%;top:15%;background:rgb(220 181 87 / 52%)
}

/* photography lower-right */
.portal-photography{
  z-index:3;
  right:0;bottom:0;
  width:54%;height:43%;
  background:#07100f;
  clip-path:polygon(0 14%,19% 1%,39% 7%,55% 12%,70% 8%,84% 1%,100% 0,100% 100%,0 100%)
}
.portal-photography .portalimage{filter:saturate(.9) brightness(.82) contrast(1.04)}
.portal-photography:before{
  background:linear-gradient(180deg,rgb(3 6 6 / 3%) 8%,rgb(3 6 6 / 32%) 48%,rgb(3 6 6 / 78%) 100%)
}
.portal-photography .portalcopy{left:18%;bottom:16%;max-width:330px}
.portal-photography .portalnumber{left:18%;top:33%}
.portal-photography .portalarrow{left:18%;bottom:5%;right:auto}

/* shared text */
.portalnumber{
  position:absolute;z-index:5;
  color:currentColor;font:800 10px/1 var(--sans);letter-spacing:.06em
}
.portalnumber:after{
  content:"";display:inline-block;width:38px;height:1px;
  margin-left:10px;vertical-align:middle;background:currentColor;opacity:.5
}
.portalcopy{
  position:absolute;z-index:5;display:block
}
.portalcopy strong{
  display:block;margin-bottom:9px;
  font:400 clamp(38px,3.8vw,62px)/.92 var(--serif);
  letter-spacing:-.04em
}
.portalcopy small{
  display:block;color:currentColor;opacity:.92;
  font:400 14px/1.32 var(--serif)
}
.portalarrow{
  position:absolute;z-index:5;
  display:grid;width:42px;height:42px;place-items:center;
  border:1px solid currentColor;border-radius:50%;
  font-size:16px;font-style:normal;transition:transform .2s ease
}
.portalpanel:hover .portalarrow{transform:translateX(3px)}

/* footer */
.portalfooter{
  display:grid!important;
  grid-template-columns:1.18fr .8fr .7fr 1.1fr;
  gap:24px 34px;
  padding:22px clamp(24px,5vw,70px) 20px;
  color:#f2ede3;background:#07594e;
  border-top:1px solid rgb(255 255 255 / 10%)
}
.portalfooter-brand{display:grid;gap:5px}
.portalfooter-brand strong{font:400 21px/1 var(--serif)}
.portalfooter-brand span{font:700 8px/1.2 var(--sans);letter-spacing:.12em;text-transform:uppercase}
.portalfooter-brand em{margin-top:7px;color:#f1c272;font:600 21px/1 "Caveat",cursive}
.portalfooter-brand small{margin-top:8px;color:#d4dfda;font-size:9px}
.portalfooter nav,.portalfooter-meta{display:grid;align-content:start;gap:6px}
.portalfooter b{color:#f1c45e;font:800 8px/1 var(--sans);letter-spacing:.2em;text-transform:uppercase}
.portalfooter a{color:#fff;font:600 10px/1.25 var(--sans);text-decoration:none}
.portalfooter-meta small{color:#e1ebe6;font:800 7px/1.35 var(--sans);letter-spacing:.13em;text-transform:uppercase}
.portalfooter-mark{margin-top:8px;color:#d6c28a;font:400 27px/1 monospace;letter-spacing:-.15em}

/* Mobile keeps same flow, stacked with curved seams */
@media(max-width:800px){
  body.home{background:#090b0a}
  body.home .portalhome{width:100%;margin:0;border-radius:0;box-shadow:none}
  .portalnav{
    min-height:58px;padding:0 16px;
    color:#fff;background:#0a0d0c;border-color:rgb(255 255 255 / 9%)
  }
  .portalbrand strong{font-size:20px}
  .portalbrand small{font-size:6px;color:rgb(255 255 255 / 60%)}
  .portalnavlinks{display:none}
  .portalmobilemenu{display:block;position:relative;margin-left:auto}
  .portalmobilemenu summary{
    display:grid;width:34px;height:34px;place-content:center;gap:6px;
    list-style:none;cursor:pointer
  }
  .portalmobilemenu summary::-webkit-details-marker{display:none}
  .portalmobilemenu summary span{display:block;width:24px;height:2px;background:currentColor}
  .portalmobilemenu-panel{
    position:absolute;z-index:90;right:0;top:38px;
    display:grid;width:min(76vw,270px);padding:8px 0;
    border:1px solid rgb(255 255 255 / 12%);
    background:#0a0d0c;box-shadow:0 18px 40px rgb(0 0 0 / 36%)
  }
  .portalmobilemenu-panel a{
    padding:12px 16px;border-bottom:1px solid rgb(255 255 255 / 8%);
    color:#fff;font:750 10px/1 var(--sans);letter-spacing:.14em;
    text-transform:uppercase;text-decoration:none
  }
  .portalmobilemenu-panel a:last-child{border-bottom:0}
  .portalmobilemenu-panel a[aria-current=page]{color:#e2bb73}

  .portalhero{display:block;min-height:0;padding:22px 18px 18px}
  .portalhero h1{font-size:50px}
  .portalhero-deck{font-size:15px}
  .portalhero-script{font-size:26px}
  .portalhero-actions a{min-width:0;flex:1;font-size:10px;padding-inline:13px}
  .portalhero-visual{min-height:320px;margin-top:18px}
  .portalhero-photo{inset:0 20% 0 0}
  .portalhero-panel{inset:44px 0 28px 44%}
  .portalhero-panel p{right:10%;top:16%;width:125px;font-size:21px}
  .portalhero-panel span{right:10%;font-size:6px}

  .portalgrid{height:auto;min-height:0;background:#09100e}
  .portalpanel{
    position:relative;left:auto!important;right:auto!important;top:auto!important;bottom:auto!important;
    width:100%!important;height:auto!important;margin:0!important
  }
  .portal-reporting{
    min-height:300px;
    clip-path:polygon(0 0,100% 0,100% 91%,78% 86%,61% 92%,40% 100%,0 96%)
  }
  .portal-reporting .portalcopy{left:24px;top:20%;max-width:52%}
  .portal-reporting .portalnumber{left:24px;top:10%}
  .portal-reporting .portalarrow{left:24px;bottom:12%}

  .portal-opinion{
    min-height:255px;margin-top:-12px!important;
    clip-path:polygon(0 9%,22% 3%,46% 12%,64% 6%,83% 18%,100% 31%,100% 88%,77% 84%,56% 94%,31% 100%,0 91%)
  }
  .portal-opinion .portalcopy{left:24px;top:26%;max-width:68%}
  .portal-opinion .portalnumber{left:24px;top:16%}
  .portal-opinion .portalarrow{left:24px;bottom:11%}

  .portal-thoughts{
    min-height:245px;margin-top:-9px!important;
    clip-path:polygon(0 4%,55% 0,70% 8%,84% 27%,100% 58%,100% 100%,0 100%)
  }
  .portal-thoughts .portalcopy{left:24px;bottom:17%;max-width:65%}
  .portal-thoughts .portalnumber{left:24px;top:14%}
  .portal-thoughts .portalarrow{left:24px;bottom:4%}
  .portalnote{left:auto;right:18px;top:13%;max-width:115px;font-size:22px}

  .portal-photography{
    min-height:285px;margin-top:-7px!important;
    clip-path:polygon(0 9%,22% 0,50% 5%,72% 0,100% 5%,100% 100%,0 100%)
  }
  .portal-photography .portalcopy{left:24px;bottom:17%;max-width:72%}
  .portal-photography .portalnumber{left:24px;top:16%}
  .portal-photography .portalarrow{left:24px;bottom:4%}

  .portalcopy strong{font-size:34px}
  .portalcopy small{font-size:12px}

  .portalfooter{grid-template-columns:1fr;gap:20px;padding:27px 20px}
  .portalfooter-brand em{font-size:24px}
}

@media(max-width:420px){
  .portalhero h1{font-size:46px}
  .portalhero-deck{font-size:14px}
  .portalhero-visual{min-height:300px}
  .portal-reporting{min-height:275px}
  .portal-opinion{min-height:240px}
  .portal-thoughts{min-height:230px}
  .portal-photography{min-height:260px}
  .portalcopy strong{font-size:31px}
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
    print(f"Homepage polish: approved_flowing_composition=1, reference_photography=1, asset_version={ASSET_VERSION}, versioned_pages={versioned_pages}, css_isolated=1, inline_critical=1")


if __name__ == "__main__":
    main()
