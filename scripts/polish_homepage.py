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
ASSET_VERSION = "20.7.0"

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

/* Mobile — simple responsive translation of the desktop design */
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

  /* Header */
  .mf-head{
    position:sticky;
    top:0;
    z-index:60;
    display:flex;
    min-height:62px;
    align-items:center;
    justify-content:space-between;
    gap:16px;
    padding:10px 17px;
    border-bottom:1px solid #ddd2c1;
    background:rgb(247 241 231 / 96%);
    backdrop-filter:blur(10px);
    -webkit-backdrop-filter:blur(10px);
  }
  .mf-brand{
    display:grid;
    gap:2px;
    color:#17130f;
    text-decoration:none;
  }
  .mf-brand strong{
    font:400 22px/.98 var(--serif);
    letter-spacing:-.03em;
  }
  .mf-brand small{
    color:#756654;
    font:800 6px/1 var(--sans);
    letter-spacing:.21em;
    text-transform:uppercase;
  }
  .mf-menu{position:relative}
  .mf-menu summary{
    display:grid;
    width:42px;
    height:42px;
    place-content:center;
    gap:5px;
    cursor:pointer;
    list-style:none;
  }
  .mf-menu summary::-webkit-details-marker{display:none}
  .mf-menu summary i{
    display:block;
    width:24px;
    height:1.5px;
    background:#1c1814;
    transition:transform .2s ease,opacity .2s ease;
  }
  .mf-menu[open] summary i:nth-child(1){transform:translateY(6.5px) rotate(45deg)}
  .mf-menu[open] summary i:nth-child(2){opacity:0}
  .mf-menu[open] summary i:nth-child(3){transform:translateY(-6.5px) rotate(-45deg)}
  .mf-menu-sheet{
    position:fixed;
    z-index:59;
    top:62px;
    right:12px;
    display:none;
    width:min(86vw,320px);
    padding:10px 18px 16px;
    border:1px solid #d7c9b7;
    background:#faf5ea;
    box-shadow:0 14px 34px rgb(52 37 23 / 16%);
  }
  .mf-menu[open] .mf-menu-sheet{display:block}
  .mf-menu-sheet nav{display:grid}
  .mf-menu-sheet nav a{
    padding:13px 2px;
    border-bottom:1px solid #e1d7c8;
    color:#1f1914;
    font:500 18px/1 var(--serif);
    text-decoration:none;
  }
  .mf-menu-sheet nav a:last-child{border-bottom:0}
  .mf-menu-sheet nav a[aria-current="page"]{color:#0b5b50}

  /* Hero */
  .mf-hero{
    display:grid;
    gap:24px;
    padding:28px 18px 30px;
    border-bottom:1px solid #ddd2c1;
  }
  .mf-kicker{
    display:block;
    margin-bottom:9px;
    color:#9c3224;
    font:850 8px/1 var(--sans);
    letter-spacing:.18em;
    text-transform:uppercase;
  }
  .mf-copy h1{
    margin:0 0 12px;
    color:#0b4f45;
    font:400 clamp(48px,14vw,62px)/.84 var(--serif);
    letter-spacing:-.05em;
  }
  .mf-copy h1 em{display:block;font-style:italic}
  .mf-deck{
    max-width:600px;
    margin:0;
    color:#332c24;
    font:400 14.5px/1.48 var(--serif);
  }
  .mf-script{
    margin:15px 0 0;
    color:#b06e3d;
    font:600 22px/1.05 "Caveat",cursive;
  }
  .mf-actions{
    display:flex;
    gap:8px;
    margin-top:18px;
  }
  .mf-actions a{
    display:flex;
    min-height:43px;
    min-width:0;
    flex:1;
    align-items:center;
    justify-content:space-between;
    padding:0 14px;
    border:1px solid #16473f;
    color:#1b1713;
    font:750 10px/1 var(--sans);
    text-decoration:none;
  }
  .mf-actions .mf-primary{
    color:#fff;
    border-color:#0b5b50;
    background:#0b5b50;
  }

  .mf-visual{
    display:grid;
    grid-template-columns:minmax(0,1fr) 86px;
    gap:10px;
    align-items:stretch;
  }
  .mf-photo{
    position:relative;
    margin:0;
    padding:8px 8px 30px;
    border:1px solid #d0c1ad;
    background:#eadbc5;
    box-shadow:0 8px 20px rgb(55 38 23 / 12%);
  }
  .mf-photo picture,
  .mf-photo img{display:block;width:100%;height:auto}
  .mf-photo img{filter:grayscale(1) contrast(1.03)}
  .mf-photo figcaption{
    position:absolute;
    left:11px;
    bottom:9px;
    color:#5c4a39;
    font:800 7px/1 var(--sans);
    letter-spacing:.12em;
    text-transform:uppercase;
  }
  .mf-green-note{
    display:flex;
    flex-direction:column;
    justify-content:flex-end;
    gap:5px;
    padding:14px 10px;
    color:#f4eee5;
    background:#0b5b50;
  }
  .mf-green-note span{
    font:italic 400 16px/1.02 var(--serif);
  }

  /* Work */
  .mf-work{
    padding:27px 16px 34px;
    background:#eee3d2;
  }
  .mf-work-head{
    display:flex;
    align-items:end;
    justify-content:space-between;
    gap:14px;
    margin-bottom:14px;
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
    font:400 38px/.95 var(--serif);
    letter-spacing:-.04em;
  }
  .mf-work-head>a{
    margin-bottom:3px;
    color:#0b5b50;
    font:800 9px/1 var(--sans);
    text-decoration:none;
    text-transform:uppercase;
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
    min-height:142px;
    overflow:hidden;
    align-items:flex-end;
    padding:17px;
    color:#fff;
    text-decoration:none;
    background:#0d564b;
  }
  .mf-card:after{
    content:"";
    position:absolute;
    inset:0;
    z-index:-1;
    background:linear-gradient(90deg,rgb(7 15 13 / 72%) 0 48%,rgb(7 15 13 / 14%) 100%);
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
    max-width:67%;
  }
  .mf-card-copy strong{
    display:block;
    font:400 26px/.98 var(--serif);
    letter-spacing:-.035em;
  }
  .mf-card-copy small{
    display:block;
    margin-top:5px;
    color:rgb(255 255 255 / 82%);
    font:400 11px/1.35 var(--serif);
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

  .mf-footer{
    display:grid;
    grid-template-columns:1fr auto;
    gap:5px 18px;
    padding:22px 18px calc(24px + env(safe-area-inset-bottom));
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

@media(min-width:560px) and (max-width:800px){
  .mf-hero{
    grid-template-columns:minmax(0,1fr) minmax(280px,.9fr);
    align-items:center;
    gap:28px;
    padding:34px 28px 36px;
  }
  .mf-copy h1{font-size:58px}
  .mf-work{padding-inline:28px}
  .mf-track{grid-template-columns:1fr 1fr}
  .mf-card{min-height:170px}
  .mf-work-head{margin-bottom:16px}
}

@media(max-width:420px){
  .mf-head{padding-inline:15px}
  .mf-brand strong{font-size:20px}
  .mf-hero{padding:25px 15px 28px}
  .mf-copy h1{font-size:49px}
  .mf-deck{font-size:14px}
  .mf-script{font-size:21px}
  .mf-visual{grid-template-columns:minmax(0,1fr) 76px}
  .mf-green-note span{font-size:14px}
  .mf-work{padding-inline:14px}
  .mf-card{min-height:136px}
  .mf-card-copy strong{font-size:24px}
  .mf-footer{padding-inline:16px}
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
