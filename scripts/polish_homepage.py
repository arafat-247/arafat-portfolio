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
ASSET_VERSION = "20.1.0"

HOME_CSS = r"""
/* Homepage v20.1 — editorial journey through Bangladesh */
body.home{
  background:#202524;
}
body.home .identity,
body.home .desktophead,
body.home .mobilehead,
body.home .mobilemenu,
body.home .menubackdrop{
  display:none!important;
}
body.home .right{
  width:100%!important;
  max-width:none!important;
  margin:0!important;
  background:#202524;
}
body.home main{
  width:100%!important;
  max-width:none!important;
  background:#202524;
}
body.home .right>footer.sitefooter{
  width:calc(100% - 48px);
  max-width:1700px;
  margin:0 auto 24px;
  border-radius:0 0 24px 24px;
}

/* paper canvas */
.journeyhome{
  width:calc(100% - 48px);
  max-width:1700px;
  margin:24px auto 0;
  overflow:hidden;
  border-radius:26px 26px 0 0;
  color:#171612;
  background:#f2ecdf;
  box-shadow:0 18px 60px rgb(0 0 0 / 26%);
}
.journeyhead{
  position:relative;
  z-index:30;
  display:flex;
  min-height:74px;
  align-items:center;
  justify-content:space-between;
  gap:28px;
  padding:0 clamp(32px,5vw,78px);
  border-bottom:1px solid rgb(35 31 24 / 9%);
  background:rgb(242 236 223 / 96%);
}
.journeybrand{
  display:grid;
  gap:3px;
  color:inherit;
  text-decoration:none;
}
.journeybrand strong{
  font:400 28px/1 var(--serif);
  letter-spacing:-.035em;
}
.journeybrand small{
  font:800 7px/1 var(--sans);
  letter-spacing:.28em;
  text-transform:uppercase;
  opacity:.58;
}
.journeynav{
  display:flex;
  align-items:center;
  gap:30px;
}
.journeynav a{
  position:relative;
  padding:27px 0 23px;
  color:inherit;
  font:700 9px/1 var(--sans);
  letter-spacing:.08em;
  text-decoration:none;
}
.journeynav a:hover,
.journeynav a[aria-current=page]{color:#8f2117}
.journeynav a[aria-current=page]:after{
  content:"";
  position:absolute;
  left:0;right:0;bottom:15px;
  height:1px;
  background:#a12519;
}
.journeymenu{display:none}

.journeycanvas{
  position:relative;
  min-height:clamp(780px,67vw,1010px);
  overflow:hidden;
  background:
    radial-gradient(circle at 12% 10%,rgb(255 255 255 / 55%),transparent 26%),
    radial-gradient(circle at 88% 23%,rgb(174 132 85 / 8%),transparent 28%),
    repeating-linear-gradient(0deg,rgb(77 67 51 / 2.2%) 0 1px,transparent 1px 4px),
    #f2ecdf;
}
.journeycanvas:before{
  content:"";
  position:absolute;
  z-index:0;
  inset:0;
  opacity:.34;
  background:
    linear-gradient(90deg,transparent 49.85%,rgb(93 84 69 / 4%) 50%,transparent 50.15%),
    linear-gradient(0deg,transparent 49.85%,rgb(93 84 69 / 3%) 50%,transparent 50.15%);
  background-size:120px 120px;
  pointer-events:none;
}

/* Bangladesh / river / route layer */
.journeymap{
  position:absolute;
  z-index:1;
  left:20%;
  top:3%;
  width:74%;
  height:91%;
  overflow:visible;
  pointer-events:none;
}
.journeyoutline{
  fill:rgb(91 78 57 / 2%);
  stroke:rgb(88 78 62 / 18%);
  stroke-width:1.4;
}
.journeyriver,
.journeyriver.small{
  fill:none;
  stroke:rgb(83 103 99 / 16%);
  stroke-width:22;
  stroke-linecap:round;
}
.journeyriver.small{stroke-width:12}
.journeyroute{
  fill:none;
  stroke:#4d4b43;
  stroke-width:1.4;
  stroke-dasharray:4 5;
  opacity:.78;
}
.routepoint{
  fill:#f2ecdf;
  stroke:#b12a1b;
  stroke-width:2.6;
}
.routepoint.p1,.routepoint.p2,.routepoint.p3,.routepoint.p4{
  filter:drop-shadow(0 0 0.5px #fff);
}

/* hero */
.journeyhero{
  position:absolute;
  z-index:8;
  left:5.2%;
  top:7.4%;
  width:min(39%,540px);
}
.journeyeyebrow{
  display:flex;
  align-items:center;
  gap:12px;
  color:#5f5b52;
  font:800 9px/1 var(--sans);
  letter-spacing:.28em;
  text-transform:uppercase;
}
.journeyeyebrow:before{
  content:"";
  width:16px;
  height:2px;
  background:#a52018;
}
.journeyhero h1{
  max-width:620px;
  margin:16px 0 18px;
  font:400 clamp(54px,5.3vw,86px)/.91 var(--serif);
  letter-spacing:-.05em;
}
.journeyhero p{
  max-width:520px;
  margin:0;
  color:#4a463e;
  font:400 clamp(16px,1.35vw,20px)/1.42 var(--serif);
}
.journeyhero-links{
  display:flex;
  gap:18px;
  margin-top:21px;
}
.journeyhero-links a{
  color:#201e1a;
  font:750 10px/1 var(--sans);
  text-decoration:none;
  border-bottom:1px solid currentColor;
  padding-bottom:4px;
}
.journeyhero-links a:first-child{color:#8f2117}

/* destinations */
.journeynode{
  position:absolute;
  z-index:7;
  display:block;
  color:#181611;
  text-decoration:none;
}
.journeymarker{
  position:absolute;
  width:18px;
  height:18px;
  border:2px solid #b42618;
  border-radius:50%;
  background:#f2ecdf;
  box-shadow:0 0 0 5px rgb(185 41 27 / 8%);
}
.journeymarker:after{
  content:"";
  position:absolute;
  inset:4px;
  border-radius:50%;
  background:#b42618;
}
.journeynumber{
  position:absolute;
  color:#4c4942;
  font:700 10px/1 var(--sans);
}
.journeycopy{
  position:relative;
  z-index:4;
  display:block;
}
.journeycopy strong{
  display:block;
  margin-bottom:7px;
  font:400 clamp(27px,2.45vw,39px)/.96 var(--serif);
  letter-spacing:-.035em;
}
.journeycopy small{
  display:block;
  max-width:270px;
  color:#4b473f;
  font:400 14px/1.36 var(--serif);
}
.journeycopy em{
  display:block;
  margin-top:12px;
  font:400 22px/1 var(--serif);
  font-style:normal;
}
.journeynode:hover .journeycopy strong{color:#922218}
.journeynode:hover .journeycopy em{transform:translateX(4px)}
.journeycopy em{transition:transform .18s ease}

/* abstract reporting figure */
.journey-reporting{
  left:10.5%;
  top:39%;
  width:28%;
  min-height:220px;
  padding:36px 0 0 12%;
}
.journey-reporting .journeymarker{left:9%;top:22px}
.journey-reporting .journeynumber{left:18%;top:25px}
.journeyart-reporting{
  position:absolute;
  left:0;
  bottom:-18px;
  width:155px;
  height:182px;
  opacity:.72;
}
.journeyart-reporting:before{
  content:"";
  position:absolute;
  left:52px;top:18px;
  width:40px;height:40px;
  border-radius:50%;
  background:#343832;
}
.journeyart-reporting:after{
  content:"";
  position:absolute;
  left:42px;top:55px;
  width:66px;height:105px;
  background:linear-gradient(95deg,#3f433e 0 56%,#202522 57% 100%);
  clip-path:polygon(28% 0,70% 0,83% 26%,100% 67%,76% 72%,68% 100%,32% 100%,28% 73%,0 65%,17% 24%);
}
.journeyart-reporting i{
  position:absolute;
  left:2px;right:6px;bottom:7px;
  height:1px;
  background:#6c685e;
  box-shadow:20px -9px 0 rgb(80 75 66 / 20%),50px -18px 0 rgb(80 75 66 / 16%);
}
.journeyart-reporting b{
  position:absolute;
  left:24px;bottom:0;
  width:58px;height:43px;
  border:1px solid rgb(53 52 47 / 52%);
  transform:skew(-11deg);
}

/* opinion skyline */
.journey-opinion{
  left:65.5%;
  top:45%;
  width:28%;
  min-height:190px;
  padding:44px 0 0 16%;
}
.journey-opinion .journeymarker{left:6%;top:25px}
.journey-opinion .journeynumber{left:15%;top:28px}
.journeyart-opinion{
  position:absolute;
  right:0;
  bottom:-14px;
  width:170px;
  height:98px;
  opacity:.58;
}
.journeyart-opinion:before,
.journeyart-opinion:after,
.journeyart-opinion i,
.journeyart-opinion b,
.journeyart-opinion u{
  content:"";
  position:absolute;
  bottom:0;
  background:#65655f;
  border-top:1px solid #4b4b46;
}
.journeyart-opinion:before{left:0;width:35px;height:49px}
.journeyart-opinion:after{left:39px;width:45px;height:74px}
.journeyart-opinion i{left:87px;width:30px;height:62px}
.journeyart-opinion b{left:120px;width:50px;height:43px}
.journeyart-opinion u{
  left:-10px;right:-10px;height:1px;bottom:-6px;background:#8c8679;
}

/* thoughts tree */
.journey-thoughts{
  left:29%;
  top:69%;
  width:27%;
  min-height:190px;
  padding:38px 0 0 15%;
}
.journey-thoughts .journeymarker{left:4%;top:18px}
.journey-thoughts .journeynumber{left:13%;top:22px}
.journeyart-thoughts{
  position:absolute;
  left:0;
  bottom:-8px;
  width:135px;
  height:145px;
  opacity:.66;
}
.journeyart-thoughts:before{
  content:"";
  position:absolute;
  left:59px;top:58px;
  width:8px;height:81px;
  background:#474a43;
  transform:rotate(3deg);
}
.journeyart-thoughts:after{
  content:"";
  position:absolute;
  left:17px;top:5px;
  width:99px;height:79px;
  background:
    radial-gradient(circle at 28% 48%,#4d5049 0 22%,transparent 23%),
    radial-gradient(circle at 53% 30%,#3f433c 0 28%,transparent 29%),
    radial-gradient(circle at 70% 56%,#52554d 0 24%,transparent 25%),
    radial-gradient(circle at 46% 68%,#454941 0 29%,transparent 30%);
}
.journeyart-thoughts i{
  position:absolute;
  left:0;right:0;bottom:0;
  height:1px;
  background:#858073;
}
.journeyart-thoughts b{
  position:absolute;
  left:64px;top:82px;
  width:50px;height:1px;
  background:#595b54;
  transform:rotate(-32deg);
  transform-origin:left center;
}

/* photography */
.journey-photography{
  left:70%;
  top:72%;
  width:27%;
  min-height:190px;
  padding:22px 0 0 3%;
}
.journey-photography .journeymarker{left:-7%;top:8px}
.journey-photography .journeynumber{left:2%;top:12px}
.journeyphoto{
  position:absolute;
  z-index:1;
  left:-6%;
  right:0;
  bottom:-38px;
  width:112%;
  height:104px;
  object-fit:cover;
  filter:saturate(.82) contrast(.95);
  box-shadow:0 7px 18px rgb(53 43 28 / 12%);
}
.journey-photography .journeycopy{
  position:relative;
  z-index:3;
  padding:24px 14px 17px;
  background:linear-gradient(90deg,#f2ecdf 0 70%,rgb(242 236 223 / 76%) 100%);
}

.journeybottom{
  position:absolute;
  z-index:8;
  left:5%;
  right:5%;
  bottom:3.2%;
  display:flex;
  justify-content:space-between;
  gap:30px;
  padding-top:15px;
  border-top:1px solid rgb(56 50 42 / 18%);
  color:#5b574d;
  font:800 7.5px/1.2 var(--sans);
  letter-spacing:.24em;
  text-transform:uppercase;
}
.journeybottom a{
  color:#6e251d;
  text-decoration:none;
  letter-spacing:.12em;
}

/* laptop adjustment */
@media(min-width:801px) and (max-width:1150px){
  .journeycanvas{min-height:800px}
  .journeyhero{width:42%}
  .journeyhero h1{font-size:58px}
  .journey-reporting{left:8%;top:40%;width:32%}
  .journey-opinion{left:62%;width:32%}
  .journey-thoughts{left:27%;width:30%}
  .journey-photography{left:68%;width:30%}
}

/* mobile: purpose-built vertical journey */
@media(max-width:800px){
  body.home{background:#f2ecdf}
  body.home .right>footer.sitefooter{
    width:100%;
    margin:0;
    border-radius:0;
  }
  .journeyhome{
    width:100%;
    margin:0;
    border-radius:0;
    box-shadow:none;
  }
  .journeyhead{
    min-height:62px;
    padding:0 18px;
  }
  .journeybrand strong{font-size:22px}
  .journeybrand small{font-size:6px}
  .journeynav{display:none}
  .journeymenu{
    display:block;
    position:relative;
    margin-left:auto;
  }
  .journeymenu summary{
    display:grid;
    width:38px;height:38px;
    place-content:center;
    gap:6px;
    list-style:none;
    cursor:pointer;
  }
  .journeymenu summary::-webkit-details-marker{display:none}
  .journeymenu summary span{
    display:block;
    width:25px;height:1.5px;
    background:#171612;
  }
  .journeymenu div{
    position:absolute;
    z-index:80;
    top:43px;right:-4px;
    display:grid;
    width:min(78vw,290px);
    padding:7px 0;
    border:1px solid rgb(41 36 28 / 12%);
    background:#f5efe4;
    box-shadow:0 18px 40px rgb(37 32 25 / 18%);
  }
  .journeymenu div a{
    padding:12px 16px;
    border-bottom:1px solid rgb(41 36 28 / 8%);
    color:#191711;
    font:750 10px/1 var(--sans);
    text-decoration:none;
  }
  .journeymenu div a:last-child{border-bottom:0}

  .journeycanvas{
    min-height:0;
    overflow:hidden;
    padding-bottom:44px;
  }
  .journeycanvas:before{
    background-size:90px 90px;
    opacity:.24;
  }
  .journeycanvas:after{
    content:"";
    position:absolute;
    z-index:2;
    left:67px;
    top:382px;
    bottom:116px;
    border-left:1.5px dashed #6b655b;
    opacity:.72;
    pointer-events:none;
  }
  .journeymap{
    left:34%;
    top:115px;
    width:78%;
    height:330px;
    opacity:.26;
  }
  .journeyroute,.routepoint{display:none}

  .journeyhero{
    position:relative;
    left:auto;top:auto;
    width:auto;
    min-height:300px;
    padding:32px 22px 24px;
  }
  .journeyeyebrow{font-size:8px}
  .journeyhero h1{
    max-width:560px;
    margin:15px 0 15px;
    font-size:clamp(43px,12.5vw,59px);
    line-height:.91;
  }
  .journeyhero p{
    max-width:520px;
    font-size:15px;
    line-height:1.45;
  }
  .journeyhero-links{gap:14px;margin-top:18px;flex-wrap:wrap}
  .journeyhero-links a{font-size:9.5px}

  .journeynode{
    position:relative;
    left:auto!important;right:auto!important;top:auto!important;bottom:auto!important;
    width:auto!important;
    min-height:194px;
    margin:0 18px;
    padding:38px 14px 24px 112px;
    border-top:1px solid rgb(57 51 42 / 12%);
  }
  .journeynode:first-of-type{border-top:0}
  .journeymarker{
    left:41px!important;
    top:45px!important;
    width:17px;height:17px;
    background:#f2ecdf;
  }
  .journeynumber{
    left:71px!important;
    top:49px!important;
    font-size:9px;
  }
  .journeycopy{padding:0!important;background:none!important}
  .journeycopy strong{
    margin-bottom:7px;
    font-size:31px;
  }
  .journeycopy small{
    max-width:270px;
    font-size:12.5px;
    line-height:1.38;
  }
  .journeycopy em{margin-top:10px;font-size:20px}

  .journeyart{
    left:0!important;
    top:48px!important;
    right:auto!important;
    bottom:auto!important;
    transform:scale(.63);
    transform-origin:top left;
  }
  .journeyart-reporting{left:4px!important}
  .journeyart-opinion{left:-3px!important;top:70px!important}
  .journeyart-thoughts{left:4px!important;top:56px!important}

  .journey-photography{
    min-height:244px;
    padding-bottom:120px;
  }
  .journeyphoto{
    left:112px;
    right:0;
    bottom:26px;
    width:calc(100% - 112px);
    height:96px;
  }
  .journey-photography .journeymarker{top:45px!important}
  .journey-photography .journeynumber{top:49px!important}

  .journeybottom{
    position:relative;
    left:auto;right:auto;bottom:auto;
    display:grid;
    gap:9px;
    margin:18px 20px 0;
    padding-top:17px;
    font-size:7px;
    line-height:1.45;
  }
}

@media(max-width:420px){
  .journeyhero{min-height:288px;padding:28px 18px 21px}
  .journeyhero h1{font-size:44px}
  .journeyhero p{font-size:14px}
  .journeycanvas:after{left:58px;top:365px}
  .journeynode{
    margin-inline:14px;
    min-height:186px;
    padding-left:102px;
  }
  .journeymarker{left:35px!important}
  .journeynumber{left:64px!important}
  .journeycopy strong{font-size:28px}
  .journeycopy small{font-size:12px}
  .journeyphoto{left:102px;width:calc(100% - 102px)}
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
    print(f"Homepage polish: editorial_journey=1, responsive_mobile_hero=1, asset_version={ASSET_VERSION}, versioned_pages={versioned_pages}, css_isolated=1, inline_critical=1")


if __name__ == "__main__":
    main()
