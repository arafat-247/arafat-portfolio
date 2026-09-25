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
ASSET_VERSION = "20.9.0"

HOME_CSS = r"""
/* Homepage v20.3 — photographic journalist's desk */
body.home{
  background:#111715;
  overflow-x:hidden;
}
body.home .identity,
body.home .desktophead,
body.home .mobilehead,
body.home .mobilemenu,
body.home .menubackdrop,
body.home .right>footer{
  display:none!important;
}
body.home .right,
body.home main{
  width:100%!important;
  max-width:none!important;
  margin:0!important;
  padding:0!important;
  background:#111715;
}
.deskhome{
  width:100%;
  min-height:100vh;
  padding:18px;
  background:#111715;
}
.deskstage{
  position:relative;
  width:min(100%,1600px);
  aspect-ratio:1447/1087;
  margin:0 auto;
  overflow:hidden;
  border:1px solid rgb(255 255 255 / 20%);
  border-radius:25px;
  background:#2b160b;
  box-shadow:0 22px 65px rgb(0 0 0 / 42%);
}
.deskvisual{
  position:absolute;
  inset:0;
  display:block;
}
.deskvisual img{
  display:block;
  width:100%;
  height:100%;
  object-fit:cover;
  object-position:center;
  user-select:none;
  -webkit-user-drag:none;
}
.mobilefresh{display:none}
.desksemantics{
  position:absolute!important;
  width:1px!important;
  height:1px!important;
  padding:0!important;
  margin:-1px!important;
  overflow:hidden!important;
  clip:rect(0,0,0,0)!important;
  white-space:nowrap!important;
  border:0!important;
}
.deskhotspots{
  position:absolute;
  inset:0;
  z-index:5;
}
.deskhotspot{
  position:absolute;
  display:block;
  border-radius:4px;
  color:transparent;
  text-decoration:none;
  background:transparent;
}
.deskhotspot span,
.deskemail span{
  position:absolute!important;
  width:1px!important;
  height:1px!important;
  padding:0!important;
  margin:-1px!important;
  overflow:hidden!important;
  clip:rect(0,0,0,0)!important;
  white-space:nowrap!important;
  border:0!important;
}
.deskhotspot:focus-visible{
  outline:3px solid #f0d5aa;
  outline-offset:3px;
  background:rgb(255 255 255 / 5%);
}
.deskhotspots-desktop{display:block}
.deskhotspots-mobile{display:none}

/* Desktop navigation — positions match the approved composition. */
.desknav-home{left:49.7%;top:1.2%;width:5.9%;height:5.3%}
.desknav-about{left:56.2%;top:1.2%;width:6.0%;height:5.3%}
.desknav-work{left:63.0%;top:1.2%;width:5.7%;height:5.3%}
.desknav-writing{left:69.1%;top:1.2%;width:7.2%;height:5.3%}
.desknav-contact{left:76.5%;top:1.2%;width:7.2%;height:5.3%}

/* Portrait and work objects. */
.deskprofile-hotspot{left:34.6%;top:4.2%;width:22.7%;height:24.5%}
.deskreporting-hotspot{left:6.0%;top:36.4%;width:25.0%;height:31.8%}
.deskopinion-hotspot{left:31.3%;top:36.8%;width:26.5%;height:31.4%}
.deskthoughts-hotspot{left:57.7%;top:36.5%;width:26.1%;height:31.5%}
.deskphoto-hotspot{left:39.1%;top:68.0%;width:25.4%;height:23.0%}
.deskemail{
  position:absolute;
  z-index:6;
  right:27%;
  bottom:1.3%;
  width:15%;
  height:3.5%;
  text-decoration:none;
}

/* Mobile and tablet — responsive translation of the desktop design */
@media(max-width:800px){
  body.home,
  body.home .right,
  body.home main{background:#f4ecdf}

  .deskhome{
    min-height:0;
    padding:0;
    background:#f4ecdf;
  }
  .deskstage{
    width:100%;
    max-width:none;
    min-height:100vh;
    aspect-ratio:auto;
    border:0;
    border-radius:0;
    box-shadow:none;
    background:#f4ecdf;
  }
  .deskvisual,
  .deskhotspots-desktop,
  .deskhotspots-mobile,
  .deskemail{display:none!important}

  .mobilefresh{
    display:block;
    min-height:100vh;
    color:#1c1814;
    background:#f4ecdf;
  }

  /* Masthead */
  .mf-head{
    display:flex;
    min-height:58px;
    align-items:center;
    justify-content:space-between;
    gap:16px;
    padding:11px clamp(15px,4vw,24px) 10px;
    border-bottom:1px solid #ddd2c1;
    background:#f7f1e7;
  }
  .mf-brand{
    display:grid;
    min-width:0;
    gap:2px;
    color:#17130f;
    text-decoration:none;
  }
  .mf-brand strong{
    font:400 clamp(19px,5.3vw,22px)/.98 var(--serif);
    letter-spacing:-.03em;
    white-space:nowrap;
  }
  .mf-brand small{
    color:#756654;
    font:800 6px/1 var(--sans);
    letter-spacing:.19em;
    text-transform:uppercase;
  }
  .mf-quicknav{
    display:flex;
    flex:0 0 auto;
    align-items:center;
    gap:13px;
  }
  .mf-quicknav a{
    position:relative;
    padding-bottom:3px;
    color:#1e1813;
    font:800 8px/1 var(--sans);
    letter-spacing:.08em;
    text-decoration:none;
    text-transform:uppercase;
  }
  .mf-quicknav a:after{
    content:"";
    position:absolute;
    left:0;
    right:100%;
    bottom:0;
    height:1px;
    background:#0b5b50;
    transition:right .18s ease;
  }
  .mf-quicknav a:hover:after,
  .mf-quicknav a:focus-visible:after{right:0}

  /* Hero */
  .mf-hero{
    display:grid;
    gap:19px;
    padding:24px clamp(15px,4vw,24px) 30px;
    border-bottom:1px solid #ddd2c1;
  }
  .mf-copy{min-width:0}
  .mf-kicker{
    display:block;
    margin-bottom:8px;
    color:#9c3224;
    font:850 8px/1 var(--sans);
    letter-spacing:.18em;
    text-transform:uppercase;
  }
  .mf-copy h1{
    margin:0 0 11px;
    color:#0b4f45;
    font:400 clamp(46px,13vw,61px)/.86 var(--serif);
    letter-spacing:-.05em;
  }
  .mf-copy h1 em{display:block;font-style:italic}
  .mf-deck{
    max-width:590px;
    margin:0;
    color:#332c24;
    font:400 clamp(13.7px,3.8vw,15px)/1.48 var(--serif);
  }
  .mf-script{
    margin:14px 0 0;
    color:#b06e3d;
    font:600 clamp(20px,5.8vw,23px)/1.04 "Caveat",cursive;
  }
  .mf-actions{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:8px;
    margin-top:15px;
  }
  .mf-actions a{
    display:flex;
    min-height:42px;
    min-width:0;
    align-items:center;
    justify-content:space-between;
    gap:10px;
    padding:0 12px;
    border:1px solid #16473f;
    color:#1b1713;
    font:750 9.5px/1 var(--sans);
    text-decoration:none;
  }
  .mf-actions .mf-primary{
    color:#fff;
    border-color:#0b5b50;
    background:#0b5b50;
  }
  .mf-email-link{
    display:inline-block;
    margin-top:11px;
    padding-bottom:3px;
    border-bottom:1px solid #9f8f7c;
    color:#5f5141;
    font:750 8px/1 var(--sans);
    letter-spacing:.07em;
    text-decoration:none;
    text-transform:uppercase;
  }

  .mf-visual{
    display:grid;
    grid-template-columns:minmax(0,1fr) clamp(70px,20vw,94px);
    gap:9px;
    align-items:stretch;
    min-width:0;
  }
  .mf-photo{
    position:relative;
    min-width:0;
    margin:0;
    padding:7px 7px 28px;
    border:1px solid #d0c1ad;
    background:#eadbc5;
    box-shadow:0 7px 18px rgb(55 38 23 / 10%);
  }
  .mf-photo picture,
  .mf-photo img{display:block;width:100%;height:100%}
  .mf-photo picture{aspect-ratio:4/5}
  .mf-photo img{
    object-fit:cover;
    object-position:center 39%;
    filter:grayscale(1) contrast(1.03);
  }
  .mf-photo figcaption{
    position:absolute;
    left:10px;
    bottom:8px;
    color:#5c4a39;
    font:800 7px/1 var(--sans);
    letter-spacing:.12em;
    text-transform:uppercase;
  }
  .mf-green-note{
    display:flex;
    min-width:0;
    flex-direction:column;
    justify-content:flex-end;
    gap:5px;
    padding:12px 9px;
    overflow:hidden;
    color:#f4eee5;
    background:#0b5b50;
  }
  .mf-green-note span{
    font:italic 400 clamp(13px,4vw,16px)/1.02 var(--serif);
    overflow-wrap:anywhere;
  }

  /* Work */
  .mf-work{
    padding:27px clamp(14px,4vw,24px) 34px;
    background:#eee3d2;
  }
  .mf-work-head{
    display:flex;
    align-items:end;
    justify-content:space-between;
    gap:14px;
    margin-bottom:13px;
  }
  .mf-work-head span{
    display:block;
    margin-bottom:4px;
    color:#a33b2c;
    font:850 7px/1 var(--sans);
    letter-spacing:.16em;
    text-transform:uppercase;
  }
  .mf-work-head h2{
    margin:0;
    font:400 clamp(35px,9vw,40px)/.95 var(--serif);
    letter-spacing:-.04em;
  }
  .mf-work-head>a{
    margin-bottom:3px;
    color:#0b5b50;
    font:800 8.5px/1 var(--sans);
    text-decoration:none;
    text-transform:uppercase;
    white-space:nowrap;
  }
  .mf-track{
    display:grid;
    grid-template-columns:1fr;
    gap:10px;
  }
  .mf-card{
    position:relative;
    isolation:isolate;
    display:flex;
    min-height:clamp(132px,37vw,150px);
    overflow:hidden;
    align-items:flex-end;
    padding:17px;
    color:#fff;
    text-decoration:none;
    background:#0d564b;
    box-shadow:0 7px 18px rgb(66 45 28 / 10%);
  }
  .mf-card:after{
    content:"";
    position:absolute;
    inset:0;
    z-index:-1;
    background:linear-gradient(90deg,rgb(7 15 13 / 74%) 0 48%,rgb(7 15 13 / 12%) 100%);
  }
  .mf-card-num{
    position:absolute;
    z-index:3;
    left:16px;
    top:14px;
    color:#efc47c;
    font:850 8px/1 var(--sans);
    letter-spacing:.12em;
  }
  .mf-card-copy{
    position:relative;
    z-index:3;
    max-width:70%;
  }
  .mf-card-copy strong{
    display:block;
    font:400 clamp(23px,6.7vw,27px)/.98 var(--serif);
    letter-spacing:-.035em;
  }
  .mf-card-copy small{
    display:block;
    margin-top:5px;
    color:rgb(255 255 255 / 82%);
    font:400 clamp(10px,2.9vw,11px)/1.35 var(--serif);
  }
  .mf-card>i{
    position:absolute;
    z-index:4;
    right:14px;
    top:14px;
    font:400 18px/1 var(--serif);
    font-style:normal;
  }
  .mf-art,
  .mf-card>img{
    position:absolute;
    inset:0;
    z-index:-2;
    width:100%;
    height:100%;
    object-fit:cover;
  }
  .mf-reporting .mf-art{
    background:
      linear-gradient(90deg,rgb(255 255 255 / 7%) 1px,transparent 1px) 0 0/30px 30px,
      linear-gradient(0deg,rgb(255 255 255 / 7%) 1px,transparent 1px) 0 0/30px 30px,
      linear-gradient(135deg,#0e564c,#163f39);
  }
  .mf-reporting .mf-art:after{
    content:"";
    position:absolute;
    right:10%;
    top:20%;
    width:30%;
    height:58%;
    border:1px solid rgb(255 255 255 / 28%);
    background:repeating-linear-gradient(180deg,rgb(255 255 255 / 24%) 0 1px,transparent 1px 10px);
  }
  .mf-opinion .mf-art{
    background:
      repeating-linear-gradient(0deg,transparent 0 24px,rgb(255 255 255 / 7%) 25px 26px),
      linear-gradient(120deg,#774336,#50302a);
  }
  .mf-opinion .mf-art:after{
    content:"“";
    position:absolute;
    right:7%;
    top:-15px;
    color:rgb(255 255 255 / 16%);
    font:400 120px/.9 Georgia,serif;
  }
  .mf-thoughts .mf-art{
    background:
      radial-gradient(circle at 78% 38%,transparent 0 26px,rgb(255 255 255 / 12%) 27px 28px,transparent 29px 47px,rgb(255 255 255 / 7%) 48px 49px,transparent 50px),
      linear-gradient(140deg,#52675a,#33483f);
  }
  .mf-photography>img{filter:brightness(.68) saturate(.78)}

  /* Scroll-entry motion */
  .mf-reveal-ready{
    opacity:0;
    transform:translateY(20px) scale(.985);
    transition:
      opacity .5s ease var(--mf-delay,0ms),
      transform .5s cubic-bezier(.2,.7,.2,1) var(--mf-delay,0ms);
    will-change:opacity,transform;
  }
  .mf-reveal-ready.mf-reveal-visible{
    opacity:1;
    transform:none;
  }

  .mf-footer{
    display:grid;
    grid-template-columns:1fr auto;
    gap:5px 18px;
    padding:22px clamp(15px,4vw,24px) calc(24px + env(safe-area-inset-bottom));
    color:#eee7dc;
    background:#0b5b50;
  }
  .mf-footer strong{font:400 21px/1 var(--serif)}
  .mf-footer>span{
    grid-column:1;
    color:rgb(255 255 255 / 65%);
    font:700 7px/1 var(--sans);
    letter-spacing:.11em;
    text-transform:uppercase;
  }
  .mf-footer nav{
    grid-column:2;
    grid-row:1/3;
    display:grid;
    align-content:center;
    gap:5px;
  }
  .mf-footer a{
    color:#fff;
    font:750 8px/1.2 var(--sans);
    text-decoration:none;
    text-transform:uppercase;
  }
}

/* Mid-size phones and landscape phones */
@media(min-width:480px) and (max-width:599px){
  .mf-hero{padding-inline:24px}
  .mf-visual{grid-template-columns:minmax(0,1fr) 94px}
  .mf-actions{max-width:390px}
  .mf-track{grid-template-columns:1fr 1fr}
  .mf-card{min-height:164px}
  .mf-card-copy{max-width:76%}
  .mf-work{padding-inline:24px}
}

/* Tablets */
@media(min-width:600px) and (max-width:800px){
  .mf-head{padding-inline:28px}
  .mf-hero{
    grid-template-columns:minmax(0,.92fr) minmax(260px,1.08fr);
    align-items:center;
    gap:28px;
    padding:34px 28px 36px;
  }
  .mf-copy h1{font-size:58px}
  .mf-copy{grid-column:1}
  .mf-visual{
    grid-column:2;
    grid-row:1;
    grid-template-columns:minmax(0,1fr) 78px;
  }
  .mf-actions{max-width:360px}
  .mf-email-link{margin-top:12px}
  .mf-work{padding-inline:28px}
  .mf-track{grid-template-columns:1fr 1fr}
  .mf-card{min-height:176px}
  .mf-card-copy{max-width:75%}
}

/* Very narrow phones */
@media(max-width:360px){
  .mf-head{padding-inline:13px}
  .mf-brand strong{font-size:18px}
  .mf-brand small{letter-spacing:.15em}
  .mf-quicknav{gap:9px}
  .mf-quicknav a{font-size:7px}
  .mf-hero{padding-inline:13px}
  .mf-copy h1{font-size:44px}
  .mf-deck{font-size:13.3px}
  .mf-actions a{padding-inline:10px;font-size:9px}
  .mf-visual{grid-template-columns:minmax(0,1fr) 64px}
  .mf-green-note{padding-inline:7px}
  .mf-green-note span{font-size:12px}
  .mf-work{padding-inline:12px}
  .mf-card{padding:15px}
  .mf-card-copy{max-width:74%}
  .mf-card-copy strong{font-size:22px}
  .mf-footer{padding-inline:14px}
}

@media(prefers-reduced-motion:reduce){
  .mf-reveal-ready{
    opacity:1!important;
    transform:none!important;
    transition:none!important;
  }
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
    print(f"Homepage polish: photographic_desktop=1, live_mobile=1, mobile_cards=4, asset_version={ASSET_VERSION}, versioned_pages={versioned_pages}, css_isolated=1, inline_critical=1")


if __name__ == "__main__":
    main()
