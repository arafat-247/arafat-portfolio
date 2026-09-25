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
ASSET_VERSION = "20.6.0"

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

/* Mobile — independent mobile homepage, not a desktop collage adaptation */
@media(max-width:800px){
  body.home,
  body.home .right,
  body.home main{
    background:#f3ecdf;
  }
  .deskhome{
    min-height:0;
    padding:0;
    background:#f3ecdf;
  }
  .deskstage{
    width:100%;
    max-width:none;
    min-height:100vh;
    aspect-ratio:auto;
    border:0;
    border-radius:0;
    box-shadow:none;
    background:#f3ecdf;
  }
  .deskvisual,
  .deskhotspots-desktop,
  .deskhotspots-mobile,
  .deskemail{
    display:none!important;
  }
  .mobilefresh{
    position:relative;
    z-index:5;
    display:block;
    min-height:100vh;
    overflow:hidden;
    color:#17130f;
    background:
      radial-gradient(circle at 88% 6%,rgb(17 95 80 / 10%),transparent 22%),
      linear-gradient(180deg,#f6f0e5 0,#f1e7d8 100%);
  }

  /* Mobile header */
  .mf-head{
    position:sticky;
    top:0;
    z-index:80;
    display:flex;
    min-height:62px;
    align-items:center;
    justify-content:space-between;
    gap:14px;
    padding:10px 17px 9px;
    border-bottom:1px solid rgb(52 39 28 / 11%);
    background:rgb(247 241 231 / 94%);
    backdrop-filter:blur(14px);
    -webkit-backdrop-filter:blur(14px);
  }
  .mf-brand{
    display:grid;
    gap:2px;
    color:#17130f;
    text-decoration:none;
  }
  .mf-brand strong{
    font:400 23px/.96 var(--serif);
    letter-spacing:-.035em;
  }
  .mf-brand small{
    color:#6d5e4d;
    font:800 6px/1 var(--sans);
    letter-spacing:.23em;
    text-transform:uppercase;
  }
  .mf-menu{position:relative}
  .mf-menu summary{
    display:flex;
    min-width:64px;
    height:42px;
    align-items:center;
    justify-content:flex-end;
    gap:5px;
    color:#17130f;
    cursor:pointer;
    list-style:none;
  }
  .mf-menu summary::-webkit-details-marker{display:none}
  .mf-menu-word{
    margin-right:5px;
    font:700 9px/1 var(--sans);
    letter-spacing:.12em;
    text-transform:uppercase;
  }
  .mf-menu summary i{
    display:block;
    width:19px;
    height:1.5px;
    background:currentColor;
  }
  .mf-menu summary i+ i{margin-left:-24px;transform:translateY(6px)}
  .mf-menu[open] summary{
    position:fixed;
    z-index:104;
    top:10px;
    right:15px;
    width:44px;
    min-width:44px;
  }
  .mf-menu[open] .mf-menu-word{display:none}
  .mf-menu[open] summary i{position:absolute}
  .mf-menu[open] summary i:first-of-type{transform:rotate(45deg)}
  .mf-menu[open] summary i:last-of-type{margin-left:0;transform:rotate(-45deg)}
  .mf-menu[open]:before{
    content:"";
    position:fixed;
    z-index:100;
    inset:0;
    background:rgb(20 16 12 / 48%);
    backdrop-filter:blur(3px);
  }
  .mf-menu-sheet{
    position:fixed;
    z-index:102;
    inset:0 0 0 auto;
    width:min(88vw,360px);
    overflow:auto;
    padding:76px 24px 28px;
    border-left:1px solid rgb(58 42 29 / 12%);
    background:
      linear-gradient(180deg,#faf5ea,#efe2cf);
    box-shadow:-22px 0 56px rgb(38 24 13 / 24%);
    transform:translateX(103%);
    transition:transform .28s ease;
  }
  .mf-menu[open] .mf-menu-sheet{transform:none}
  .mf-menu-kicker{
    display:block;
    margin-bottom:8px;
    color:#aa3324;
    font:850 8px/1 var(--sans);
    letter-spacing:.18em;
    text-transform:uppercase;
  }
  .mf-menu-sheet>strong{
    display:block;
    margin-bottom:24px;
    color:#0b5b50;
    font:400 30px/.96 var(--serif);
  }
  .mf-menu-sheet nav{display:grid}
  .mf-menu-sheet nav a{
    display:grid;
    grid-template-columns:1fr auto;
    align-items:center;
    gap:14px;
    padding:15px 0;
    border-bottom:1px solid rgb(73 52 34 / 13%);
    color:#211811;
    font:600 23px/1 var(--serif);
    text-decoration:none;
  }
  .mf-menu-sheet nav a b{
    color:#9b2b20;
    font:800 8px/1 var(--sans);
  }
  .mf-menu-sheet p{
    margin:26px 0 0;
    color:#b46f3d;
    font:600 22px/1.05 "Caveat",cursive;
  }

  /* Hero */
  .mf-hero{
    position:relative;
    display:grid;
    grid-template-columns:1fr;
    gap:20px;
    padding:30px 18px 26px;
    overflow:hidden;
  }
  .mf-copy{position:relative;z-index:3}
  .mf-kicker{
    display:block;
    margin-bottom:9px;
    color:#9f3022;
    font:850 8px/1 var(--sans);
    letter-spacing:.19em;
    text-transform:uppercase;
  }
  .mf-copy h1{
    margin:0 0 12px;
    color:#0b4f45;
    font:400 clamp(50px,15vw,66px)/.82 var(--serif);
    letter-spacing:-.055em;
  }
  .mf-copy h1 em{display:block;font-style:italic}
  .mf-deck{
    max-width:590px;
    margin:0;
    color:#30291f;
    font:400 14.5px/1.48 var(--serif);
  }
  .mf-script{
    margin:16px 0 0;
    color:#b26f3f;
    font:600 23px/1.05 "Caveat",cursive;
  }
  .mf-actions{
    display:flex;
    gap:9px;
    margin-top:18px;
  }
  .mf-actions a{
    display:flex;
    min-height:44px;
    min-width:0;
    flex:1;
    align-items:center;
    justify-content:space-between;
    gap:15px;
    padding:0 14px;
    border:1px solid #123f38;
    border-radius:999px;
    color:#17130f;
    font:750 10.5px/1 var(--sans);
    text-decoration:none;
  }
  .mf-actions .mf-primary{
    color:#fff;
    background:#0a5d51;
    border-color:#0a5d51;
  }

  .mf-visual{
    position:relative;
    min-height:350px;
  }
  .mf-green-note{
    position:absolute;
    z-index:1;
    right:-18px;
    top:26px;
    width:49%;
    height:78%;
    padding:28px 18px;
    color:#f6eee3;
    background:linear-gradient(180deg,#0d6a5f,#075147);
    clip-path:polygon(8% 0,100% 7%,100% 93%,0 100%);
  }
  .mf-green-note i{
    display:block;
    margin-bottom:18px;
    font:850 7px/1 var(--sans);
    letter-spacing:.22em;
    text-transform:uppercase;
    font-style:normal;
  }
  .mf-green-note b{
    display:block;
    font:italic 400 23px/1.02 var(--serif);
  }
  .mf-photo{
    position:absolute;
    z-index:2;
    left:0;
    top:0;
    width:74%;
    margin:0;
    padding:8px 8px 37px;
    background:#f1e4d1;
    border:1px solid rgb(67 48 30 / 20%);
    box-shadow:0 16px 30px rgb(49 31 17 / 18%);
    transform:rotate(-1.5deg);
  }
  .mf-photo:before{
    content:"";
    position:absolute;
    z-index:-1;
    inset:-9px 16px 13px -10px;
    background:#dfd0ba;
    transform:rotate(1.1deg);
  }
  .mf-photo picture,
  .mf-photo img{display:block;width:100%}
  .mf-photo img{
    aspect-ratio:1/1.08;
    object-fit:cover;
    object-position:center 39%;
    filter:grayscale(1) contrast(1.04);
  }
  .mf-photo figcaption{
    position:absolute;
    left:12px;
    bottom:10px;
    color:#4d3b2c;
    font:700 9px/1 var(--sans);
    letter-spacing:.1em;
    text-transform:uppercase;
  }

  /* Work carousel */
  .mf-work{
    padding:24px 0 28px;
    border-top:1px solid rgb(63 45 29 / 11%);
    background:#efe4d3;
  }
  .mf-work-head{
    display:flex;
    align-items:end;
    justify-content:space-between;
    gap:16px;
    padding:0 18px 14px;
  }
  .mf-work-head span{
    display:block;
    margin-bottom:4px;
    color:#a63224;
    font:850 8px/1 var(--sans);
    letter-spacing:.18em;
    text-transform:uppercase;
  }
  .mf-work-head h2{
    margin:0;
    font:400 42px/.95 var(--serif);
    letter-spacing:-.045em;
  }
  .mf-work-head p{
    margin:0 0 4px;
    color:#6d5f4f;
    font:700 9px/1 var(--sans);
    letter-spacing:.1em;
    text-transform:uppercase;
  }
  .mf-track{
    display:flex;
    gap:12px;
    overflow-x:auto;
    overscroll-behavior-inline:contain;
    scroll-snap-type:x mandatory;
    scrollbar-width:none;
    padding:0 18px 8px;
  }
  .mf-track::-webkit-scrollbar{display:none}
  .mf-card{
    position:relative;
    isolation:isolate;
    display:flex;
    width:min(79vw,310px);
    min-width:min(79vw,310px);
    min-height:330px;
    overflow:hidden;
    flex-direction:column;
    justify-content:flex-end;
    scroll-snap-align:start;
    padding:18px;
    color:#fff;
    text-decoration:none;
    background:#0f5147;
    box-shadow:0 12px 26px rgb(59 40 24 / 14%);
  }
  .mf-card:after{
    content:"";
    position:absolute;
    inset:0;
    z-index:-1;
    background:linear-gradient(180deg,transparent 20%,rgb(15 18 15 / 18%) 50%,rgb(7 14 12 / 76%) 100%);
  }
  .mf-card-num{
    position:absolute;
    z-index:3;
    left:17px;
    top:16px;
    color:#f0c47b;
    font:850 9px/1 var(--sans);
    letter-spacing:.12em;
  }
  .mf-card-copy{position:relative;z-index:3;max-width:84%}
  .mf-card-copy strong{
    display:block;
    font:400 34px/.95 var(--serif);
    letter-spacing:-.04em;
  }
  .mf-card-copy small{
    display:block;
    margin-top:7px;
    color:rgb(255 255 255 / 82%);
    font:400 12px/1.4 var(--serif);
  }
  .mf-card>i{
    position:absolute;
    z-index:4;
    right:14px;
    bottom:14px;
    display:grid;
    width:34px;
    height:34px;
    place-items:center;
    border:1px solid rgb(255 255 255 / 70%);
    border-radius:50%;
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
      linear-gradient(90deg,rgb(255 255 255 / 6%) 1px,transparent 1px) 0 0/34px 34px,
      linear-gradient(0deg,rgb(255 255 255 / 6%) 1px,transparent 1px) 0 0/34px 34px,
      radial-gradient(circle at 72% 24%,rgb(244 196 116 / 26%) 0 8%,transparent 8.5%),
      linear-gradient(145deg,#0a4038,#15594f 58%,#0b3932);
  }
  .mf-reporting .mf-art:before{
    content:"";
    position:absolute;
    right:11%;
    top:20%;
    width:42%;
    height:40%;
    border:1px solid rgb(255 255 255 / 28%);
    background:repeating-linear-gradient(180deg,rgb(255 255 255 / 22%) 0 1px,transparent 1px 11px);
    transform:rotate(5deg);
  }
  .mf-opinion{background:#703b30}
  .mf-opinion .mf-art{
    background:
      repeating-linear-gradient(0deg,transparent 0 25px,rgb(255 255 255 / 7%) 26px 27px),
      linear-gradient(125deg,#80483a,#58322b 62%,#402825);
  }
  .mf-opinion .mf-art:before{
    content:"“";
    position:absolute;
    right:5%;
    top:0;
    color:rgb(255 255 255 / 13%);
    font:400 180px/.8 Georgia,serif;
  }
  .mf-thoughts{background:#405447}
  .mf-thoughts .mf-art{
    background:
      radial-gradient(circle at 74% 28%,transparent 0 34px,rgb(255 255 255 / 12%) 35px 36px,transparent 37px 58px,rgb(255 255 255 / 8%) 59px 60px,transparent 61px),
      repeating-linear-gradient(135deg,transparent 0 24px,rgb(255 255 255 / 5%) 25px 26px),
      linear-gradient(140deg,#53675a,#34493f 68%,#283d35);
  }
  .mf-photography>img{filter:brightness(.66) saturate(.8)}
  .mf-work-links{
    display:flex;
    justify-content:space-between;
    gap:16px;
    padding:10px 18px 0;
  }
  .mf-work-links a{
    color:#0b564b;
    font:800 9px/1 var(--sans);
    letter-spacing:.08em;
    text-decoration:none;
    text-transform:uppercase;
  }
  .mf-footer{
    display:grid;
    gap:5px;
    padding:22px 18px calc(24px + env(safe-area-inset-bottom));
    color:#efe8dc;
    background:#0b564b;
  }
  .mf-footer strong{font:400 22px/1 var(--serif)}
  .mf-footer span{
    color:rgb(255 255 255 / 66%);
    font:700 8px/1 var(--sans);
    letter-spacing:.12em;
    text-transform:uppercase;
  }
  .mf-footer a{
    width:max-content;
    margin-top:10px;
    padding-bottom:4px;
    border-bottom:1px solid currentColor;
    color:#fff;
    font:800 9px/1 var(--sans);
    text-decoration:none;
    text-transform:uppercase;
  }

  @media(prefers-reduced-motion:no-preference){
    .mf-photo{animation:mfFloat 5.5s ease-in-out infinite alternate}
    .mf-green-note{animation:mfFloat 7s ease-in-out .4s infinite alternate-reverse}
    @keyframes mfFloat{
      from{translate:0 0}
      to{translate:0 -5px}
    }
  }
}
@media(max-width:420px){
  .mf-head{padding-inline:15px}
  .mf-brand strong{font-size:21px}
  .mf-hero{padding:27px 16px 24px}
  .mf-copy h1{font-size:52px}
  .mf-deck{font-size:14px}
  .mf-visual{min-height:326px}
  .mf-photo{width:76%}
  .mf-green-note{width:50%;right:-22px}
  .mf-green-note b{font-size:21px}
  .mf-track{padding-inline:16px}
  .mf-card{width:82vw;min-width:82vw;min-height:312px}
  .mf-work-head,.mf-work-links{padding-inline:16px}
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
