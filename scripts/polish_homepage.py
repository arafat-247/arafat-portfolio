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
ASSET_VERSION = "20.4.0"

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
.mobilelive{display:none}
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

/* Mobile is a real interface; desktop remains the approved photographic composition. */
@media(max-width:800px){
  body.home,
  body.home .right,
  body.home main{
    background:#2b160b;
  }
  .deskhome{
    min-height:0;
    padding:0;
    background:#2b160b;
  }
  .deskstage{
    width:100%;
    max-width:720px;
    min-height:100vh;
    aspect-ratio:auto;
    border:0;
    border-radius:0;
    box-shadow:none;
    background:
      linear-gradient(rgb(49 24 10 / 88%),rgb(35 16 7 / 92%)),
      url("assets/home/approved-desk-desktop.webp") 68% 46%/250% auto;
  }
  .deskvisual,
  .deskhotspots-desktop,
  .deskhotspots-mobile,
  .deskemail{
    display:none!important;
  }
  .mobilelive{
    position:relative;
    z-index:6;
    display:block;
    min-height:100vh;
    padding:0 14px 34px;
    color:#f4eadc;
  }
  .mobilelive-head{
    position:sticky;
    z-index:30;
    top:0;
    display:flex;
    min-height:68px;
    align-items:center;
    justify-content:space-between;
    gap:18px;
    margin:0 -14px;
    padding:11px 17px 10px;
    border-bottom:1px solid rgb(245 229 207 / 12%);
    background:rgb(34 16 8 / 82%);
    backdrop-filter:blur(12px);
    -webkit-backdrop-filter:blur(12px);
  }
  .mobilelive-brand{
    display:grid;
    gap:3px;
    color:#f4eadc;
    text-decoration:none;
  }
  .mobilelive-brand strong{
    font:400 24px/.95 var(--serif);
    letter-spacing:-.025em;
  }
  .mobilelive-brand small{
    color:#c6aa83;
    font:800 6px/1 var(--sans);
    letter-spacing:.25em;
    text-transform:uppercase;
  }
  .mobilelive-menu{
    position:relative;
  }
  .mobilelive-menu summary{
    display:grid;
    width:40px;
    height:40px;
    place-content:center;
    gap:5px;
    border:1px solid rgb(245 229 207 / 20%);
    border-radius:50%;
    background:rgb(12 8 5 / 35%);
    cursor:pointer;
    list-style:none;
  }
  .mobilelive-menu summary::-webkit-details-marker{display:none}
  .mobilelive-menu summary i{
    display:block;
    width:18px;
    height:1.5px;
    background:#f4eadc;
  }
  .mobilelive-menu nav{
    position:absolute;
    top:46px;
    right:0;
    display:grid;
    width:188px;
    overflow:hidden;
    border:1px solid rgb(79 55 35 / 30%);
    border-radius:10px;
    background:#e9dcc5;
    box-shadow:0 18px 40px rgb(0 0 0 / 40%);
  }
  .mobilelive-menu nav a{
    padding:12px 14px;
    border-bottom:1px solid rgb(75 51 31 / 13%);
    color:#25170e;
    font:600 14px/1.1 var(--serif);
    text-decoration:none;
  }
  .mobilelive-menu nav a:last-child{border-bottom:0}

  .mobilelive-hero{
    display:grid;
    grid-template-columns:minmax(118px,39%) 1fr;
    gap:14px;
    align-items:end;
    padding:22px 2px 24px;
  }
  .mobilelive-profile{
    position:relative;
    display:block;
    padding:7px 7px 58px;
    color:#24170f;
    text-decoration:none;
    transform:rotate(-1.8deg);
    background:
      repeating-linear-gradient(0deg,rgb(89 61 34 / 3%) 0 1px,transparent 1px 3px),
      #e5d7c0;
    border:1px solid rgb(70 48 30 / 28%);
    box-shadow:0 11px 23px rgb(0 0 0 / 34%);
  }
  .mobilelive-profile picture,
  .mobilelive-profile img{
    display:block;
    width:100%;
  }
  .mobilelive-profile img{
    aspect-ratio:1/1.02;
    object-fit:cover;
    object-position:center 34%;
    filter:grayscale(1) contrast(1.04);
  }
  .mobilelive-profile>span{
    position:absolute;
    left:11px;
    right:9px;
    bottom:9px;
    display:grid;
    gap:3px;
  }
  .mobilelive-profile strong{
    font:700 14px/1 var(--serif);
  }
  .mobilelive-profile small{
    color:#4c3929;
    font:400 9.5px/1.22 var(--serif);
  }
  .mobilelive-intro{
    padding:0 2px 4px;
    text-shadow:0 2px 8px rgb(0 0 0 / 38%);
  }
  .mobilelive-intro>span{
    display:block;
    margin-bottom:8px;
    color:#d0aa74;
    font:800 7px/1 var(--sans);
    letter-spacing:.18em;
    text-transform:uppercase;
  }
  .mobilelive-intro h2{
    margin:0 0 8px;
    color:#f5ebdd;
    font:400 clamp(32px,9vw,43px)/.9 var(--serif);
    letter-spacing:-.04em;
  }
  .mobilelive-intro p{
    margin:0;
    color:#dfd0be;
    font:400 13px/1.4 var(--serif);
  }

  .mobilelive-work{
    display:grid;
    gap:18px;
    padding:2px 1px 8px;
  }
  .mobilelive-card{
    position:relative;
    display:block;
    color:#24170f;
    text-decoration:none;
    filter:drop-shadow(0 12px 17px rgb(0 0 0 / 31%));
  }
  .mobilelive-card:nth-child(odd){transform:rotate(-.55deg)}
  .mobilelive-card:nth-child(even){transform:rotate(.45deg)}
  .mobilelive-card:active{transform:translateY(2px) rotate(0)}
  .mobilelive-media{
    position:relative;
    display:block;
    min-height:180px;
    overflow:hidden;
    border:1px solid rgb(70 47 27 / 24%);
    background:#ddccb0;
  }
  .mobilelive-media:before{
    content:"";
    position:absolute;
    z-index:-1;
    inset:8px -6px -8px 7px;
    border:1px solid rgb(70 47 27 / 18%);
    background:#bda98b;
  }
  .mobilelive-reporting .mobilelive-media img,
  .mobilelive-photo img{
    display:block;
    width:100%;
    height:195px;
    object-fit:cover;
  }
  .mobilelive-reporting .mobilelive-media img{
    object-position:center;
    filter:sepia(.24) saturate(.72) contrast(.95);
  }
  .mobilelive-copy{
    position:relative;
    z-index:4;
    display:grid;
    grid-template-columns:auto 1fr auto;
    align-items:center;
    gap:9px;
    width:91%;
    margin:-33px 0 0 7%;
    padding:14px 15px 14px 20px;
    border:1px solid rgb(70 47 27 / 24%);
    background:
      repeating-linear-gradient(0deg,rgb(83 58 34 / 3%) 0 1px,transparent 1px 3px),
      #eadcc4;
    box-shadow:0 5px 10px rgb(0 0 0 / 12%);
  }
  .mobilelive-copy>b{
    display:grid;
    width:38px;
    aspect-ratio:1;
    place-items:center;
    margin-left:-29px;
    border:2px solid #a4291d;
    border-radius:50%;
    color:#a4291d;
    background:#f0e3cf;
    font:600 20px/1 var(--serif);
    transform:rotate(-8deg);
  }
  .mobilelive-copy>span{
    display:grid;
    gap:3px;
  }
  .mobilelive-copy strong{
    font:600 22px/.98 var(--serif);
    letter-spacing:-.025em;
  }
  .mobilelive-copy small{
    color:#4a392a;
    font:400 11.5px/1.3 var(--serif);
  }
  .mobilelive-copy em{
    font:400 23px/1 var(--serif);
    font-style:normal;
  }

  .mobilelive-paper{
    min-height:190px;
    padding:29px 30px 23px;
    background:
      linear-gradient(90deg,transparent 0 8%,rgb(167 81 52 / 11%) 8.2% 8.6%,transparent 8.8%),
      repeating-linear-gradient(0deg,#e4d6bb 0 23px,#c6b9a4 24px 25px);
  }
  .mobilelive-paper i{
    display:block;
    max-width:74%;
    color:#4a3a2d;
    font:400 13px/1.35 var(--serif);
    font-style:normal;
  }
  .mobilelive-paper mark{
    display:inline-block;
    margin-top:16px;
    padding:2px 4px;
    color:#5b3d1d;
    background:#d8aa51;
    font:400 10px/1.2 var(--serif);
    transform:rotate(-1deg);
  }
  .mobilelive-paper u{
    position:absolute;
    right:19px;
    bottom:26px;
    color:#ad2a20;
    font:600 20px/.9 "Caveat",cursive;
    text-decoration:none;
    transform:rotate(-8deg);
  }
  .mobilelive-paper:after{
    content:"";
    position:absolute;
    left:20px;
    right:22px;
    bottom:30px;
    height:1px;
    background:#a93428;
    transform:rotate(-2deg);
    opacity:.65;
  }

  .mobilelive-notebook{
    min-height:205px;
    padding:27px 62px 24px 38px;
    border-radius:7px;
    background:
      linear-gradient(90deg,transparent 0 8%,rgb(176 95 67 / 17%) 8.2% 8.6%,transparent 8.8%),
      repeating-linear-gradient(0deg,#e8ddc7 0 25px,#b8b1a4 26px 27px);
  }
  .mobilelive-notebook:after{
    content:"";
    position:absolute;
    right:11%;
    top:6%;
    width:8%;
    height:88%;
    border-radius:10px;
    background:linear-gradient(90deg,#0c0b09,#b79a5d 20%,#111 34% 78%,#c5a466 82%,#090806);
    transform:rotate(-8deg);
    box-shadow:3px 4px 7px rgb(0 0 0 / 30%);
  }
  .mobilelive-notebook i{
    display:block;
    color:#4b3929;
    font:600 23px/.9 "Caveat",cursive;
  }
  .mobilelive-notebook>span{
    display:block;
    margin-top:18px;
    color:#4a392b;
    font:500 16px/1.18 "Caveat",cursive;
  }
  .mobilelive-photo{
    min-height:190px;
    padding:8px 8px 14px;
    background:#e7d8bf;
  }
  .mobilelive-photo img{
    height:190px;
    object-position:center;
    border:1px solid rgb(65 45 26 / 15%);
  }

  .mobilelive-foot{
    display:flex;
    justify-content:space-between;
    gap:14px;
    margin-top:24px;
    padding:17px 4px 3px;
    border-top:1px solid rgb(241 220 193 / 20%);
  }
  .mobilelive-foot a{
    color:#e3c79f;
    font:800 8px/1.2 var(--sans);
    letter-spacing:.12em;
    text-decoration:none;
    text-transform:uppercase;
  }
}
@media(max-width:420px){
  .mobilelive{padding-inline:11px}
  .mobilelive-head{margin-inline:-11px;padding-inline:14px}
  .mobilelive-brand strong{font-size:22px}
  .mobilelive-hero{
    grid-template-columns:42% 1fr;
    gap:11px;
    padding-top:18px;
  }
  .mobilelive-profile{padding:6px 6px 54px}
  .mobilelive-profile small{font-size:9px}
  .mobilelive-intro h2{font-size:34px}
  .mobilelive-intro p{font-size:12.5px}
  .mobilelive-copy{width:93%;margin-left:5%}
  .mobilelive-copy strong{font-size:20px}
  .mobilelive-copy small{font-size:11px}
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
