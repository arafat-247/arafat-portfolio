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
ASSET_VERSION = "20.5.0"

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

/* Mobile — faithful responsive adaptation of the approved desktop composition. */
@media(max-width:800px){
  body.home,
  body.home .right,
  body.home main{
    background:#ede3d1;
  }
  .deskhome{
    min-height:0;
    padding:0;
    background:
      linear-gradient(rgb(246 239 226 / 95%),rgb(237 226 207 / 96%)),
      url("assets/home/approved-desk-desktop.webp") 50% 42%/220% auto;
  }
  .deskstage{
    width:100%;
    max-width:720px;
    min-height:100vh;
    aspect-ratio:auto;
    border:0;
    border-radius:0;
    box-shadow:none;
    background:transparent;
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
    overflow:hidden;
    padding:0 16px 36px;
    color:#1e1a16;
    background:
      radial-gradient(circle at 82% 9%,rgb(18 81 69 / 12%),transparent 19%),
      linear-gradient(180deg,#f3eadc 0,#efe3d1 52%,#eadac4 100%);
  }
  .mobilelive:before{
    content:"";
    position:absolute;
    inset:0;
    pointer-events:none;
    opacity:.26;
    background:
      repeating-linear-gradient(0deg,rgb(74 52 32 / 3%) 0 1px,transparent 1px 4px),
      repeating-linear-gradient(90deg,rgb(74 52 32 / 2%) 0 1px,transparent 1px 5px);
    mix-blend-mode:multiply;
  }

  /* Header: same restrained identity as desktop, no dark app bar. */
  .mobilelive-head{
    position:sticky;
    z-index:50;
    top:0;
    display:flex;
    min-height:64px;
    align-items:center;
    justify-content:space-between;
    gap:18px;
    margin:0 -16px;
    padding:10px 18px 9px;
    border-bottom:1px solid rgb(51 38 26 / 13%);
    background:rgb(244 237 224 / 93%);
    backdrop-filter:blur(14px);
    -webkit-backdrop-filter:blur(14px);
  }
  .mobilelive-brand{
    display:grid;
    gap:2px;
    color:#1d1814;
    text-decoration:none;
  }
  .mobilelive-brand strong{
    font:400 24px/.96 var(--serif);
    letter-spacing:-.035em;
  }
  .mobilelive-brand small{
    color:#756652;
    font:800 6px/1 var(--sans);
    letter-spacing:.25em;
    text-transform:uppercase;
  }
  .mobilelive-menu summary{
    display:grid;
    width:42px;
    height:42px;
    place-content:center;
    gap:6px;
    border:0;
    border-radius:50%;
    background:transparent;
    cursor:pointer;
    list-style:none;
  }
  .mobilelive-menu summary::-webkit-details-marker{display:none}
  .mobilelive-menu summary i{
    display:block;
    width:25px;
    height:1.5px;
    background:#1f1a16;
    transition:transform .24s ease,opacity .24s ease;
  }
  .mobilelive-menu[open] summary{
    position:fixed;
    z-index:103;
    top:11px;
    right:14px;
  }
  .mobilelive-menu[open] summary i:nth-child(1){transform:translateY(7.5px) rotate(45deg)}
  .mobilelive-menu[open] summary i:nth-child(2){opacity:0}
  .mobilelive-menu[open] summary i:nth-child(3){transform:translateY(-7.5px) rotate(-45deg)}
  .mobilelive-menu[open]:before{
    content:"";
    position:fixed;
    z-index:100;
    inset:0;
    background:rgb(23 17 12 / 42%);
    backdrop-filter:blur(2px);
  }
  .mobilelive-menu nav{
    position:fixed;
    z-index:101;
    top:0;
    right:0;
    bottom:0;
    display:grid;
    width:min(84vw,340px);
    align-content:start;
    overflow:auto;
    padding:88px 26px 30px;
    border:0;
    border-left:1px solid rgb(72 52 34 / 14%);
    border-radius:0;
    background:
      linear-gradient(180deg,rgb(248 242 231 / 98%),rgb(239 226 207 / 99%)),
      repeating-linear-gradient(0deg,rgb(91 64 38 / 3%) 0 1px,transparent 1px 4px);
    box-shadow:-20px 0 46px rgb(38 24 12 / 22%);
    transform:translateX(105%);
    transition:transform .26s ease;
  }
  .mobilelive-menu[open] nav{transform:translateX(0)}
  .mobilelive-menu nav:before{
    content:"Arafat Rahaman";
    display:block;
    margin-bottom:20px;
    color:#0b5b50;
    font:400 28px/.95 var(--serif);
    letter-spacing:-.035em;
  }
  .mobilelive-menu nav a{
    position:relative;
    padding:15px 0;
    border-bottom:1px solid rgb(74 53 34 / 14%);
    color:#231a14;
    font:600 22px/1 var(--serif);
    text-decoration:none;
  }
  .mobilelive-menu nav a:after{
    content:"→";
    position:absolute;
    right:0;
    color:#0c5b50;
    font-weight:400;
  }

  /* Hero: same cream + portrait + green panel language as desktop. */
  .mobilelive-hero{
    position:relative;
    display:block;
    min-height:560px;
    margin:0 -16px;
    padding:34px 22px 24px;
    overflow:hidden;
    background:#f4ecdf;
    border-bottom:1px solid rgb(59 43 28 / 12%);
  }
  .mobilelive-hero:before{
    content:"";
    position:absolute;
    z-index:0;
    right:-18%;
    top:33%;
    width:68%;
    height:54%;
    background:linear-gradient(180deg,#0d6a5f 0,#075248 100%);
    clip-path:polygon(10% 0,100% 8%,100% 93%,0 100%);
    opacity:.96;
  }
  .mobilelive-hero:after{
    content:"People, policy\A and a more equal\A Bangladesh.";
    white-space:pre;
    position:absolute;
    z-index:1;
    right:6%;
    top:47%;
    width:31%;
    color:#f8f0e4;
    font:italic 400 20px/.98 var(--serif);
    transform:rotate(-1deg);
  }
  .mobilelive-intro{
    position:relative;
    z-index:3;
    width:76%;
    padding:0 0 18px;
    text-shadow:none;
  }
  .mobilelive-intro>span{
    display:block;
    margin-bottom:9px;
    color:#9f2d20;
    font:850 8px/1 var(--sans);
    letter-spacing:.2em;
    text-transform:uppercase;
  }
  .mobilelive-intro h2{
    margin:0 0 12px;
    color:#0d4e45;
    font:400 clamp(42px,12vw,58px)/.88 var(--serif);
    letter-spacing:-.05em;
  }
  .mobilelive-intro p{
    margin:0;
    max-width:94%;
    color:#3a322a;
    font:400 14px/1.42 var(--serif);
  }

  .mobilelive-profile{
    position:absolute;
    z-index:4;
    left:5%;
    bottom:18px;
    width:68%;
    padding:9px 9px 66px;
    color:#24170f;
    text-decoration:none;
    transform:rotate(-2.2deg);
    background:
      repeating-linear-gradient(0deg,rgb(89 61 34 / 3%) 0 1px,transparent 1px 3px),
      #f0e4d2;
    border:1px solid rgb(70 48 30 / 22%);
    box-shadow:0 16px 28px rgb(48 31 17 / 22%);
  }
  .mobilelive-profile:before{
    content:"";
    position:absolute;
    z-index:-1;
    inset:-10px 18px 16px -12px;
    background:#ded0bb;
    transform:rotate(1.3deg);
  }
  .mobilelive-profile picture,
  .mobilelive-profile img{
    display:block;
    width:100%;
  }
  .mobilelive-profile img{
    aspect-ratio:1/1.03;
    object-fit:cover;
    object-position:center 36%;
    filter:grayscale(1) contrast(1.04);
  }
  .mobilelive-profile>span{
    position:absolute;
    left:13px;
    right:11px;
    bottom:11px;
    display:grid;
    gap:3px;
  }
  .mobilelive-profile strong{
    font:600 16px/1 var(--serif);
  }
  .mobilelive-profile small{
    color:#554333;
    font:400 10.5px/1.2 var(--serif);
  }

  /* Work area: desk collage rhythm, stacked rather than flattened. */
  .mobilelive-work{
    position:relative;
    display:grid;
    gap:18px;
    margin:0 -16px;
    padding:28px 18px 12px;
    background:
      linear-gradient(rgb(51 27 13 / 89%),rgb(38 19 9 / 92%)),
      url("assets/home/approved-desk-desktop.webp") 63% 60%/230% auto;
  }
  .mobilelive-work:before{
    content:"Work";
    position:absolute;
    left:20px;
    top:7px;
    color:rgb(244 232 214 / 70%);
    font:400 12px/1 var(--serif);
    letter-spacing:.12em;
    text-transform:uppercase;
  }
  .mobilelive-card{
    position:relative;
    display:block;
    color:#24170f;
    text-decoration:none;
    filter:drop-shadow(0 12px 18px rgb(0 0 0 / 24%));
    transition:transform .2s ease,filter .2s ease;
  }
  .mobilelive-card:nth-child(odd){transform:rotate(-.7deg)}
  .mobilelive-card:nth-child(even){transform:rotate(.55deg)}
  .mobilelive-card:active{transform:translateY(2px) rotate(0)}
  .mobilelive-media{
    position:relative;
    display:block;
    min-height:168px;
    overflow:hidden;
    border:1px solid rgb(70 47 27 / 22%);
    background:#ddccb0;
  }
  .mobilelive-reporting .mobilelive-media img,
  .mobilelive-photo img{
    display:block;
    width:100%;
    height:184px;
    object-fit:cover;
  }
  .mobilelive-reporting .mobilelive-media img{
    object-position:center;
    filter:sepia(.15) saturate(.78) contrast(.97);
  }
  .mobilelive-copy{
    position:relative;
    z-index:4;
    display:grid;
    grid-template-columns:auto 1fr auto;
    align-items:center;
    gap:9px;
    width:92%;
    margin:-29px 0 0 6%;
    padding:13px 14px 13px 18px;
    border:1px solid rgb(70 47 27 / 22%);
    background:
      repeating-linear-gradient(0deg,rgb(83 58 34 / 3%) 0 1px,transparent 1px 3px),
      #efe1ca;
    box-shadow:0 5px 10px rgb(0 0 0 / 12%);
  }
  .mobilelive-copy>b{
    display:grid;
    width:38px;
    aspect-ratio:1;
    place-items:center;
    margin-left:-27px;
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
    font:600 23px/.98 var(--serif);
    letter-spacing:-.025em;
  }
  .mobilelive-copy small{
    color:#4a392a;
    font:400 11.5px/1.28 var(--serif);
  }
  .mobilelive-copy em{
    color:#0d5a4f;
    font:400 23px/1 var(--serif);
    font-style:normal;
  }

  .mobilelive-paper{
    min-height:182px;
    padding:27px 30px 23px;
    background:
      linear-gradient(90deg,transparent 0 8%,rgb(167 81 52 / 11%) 8.2% 8.6%,transparent 8.8%),
      repeating-linear-gradient(0deg,#e5d8bd 0 23px,#c8bba6 24px 25px);
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
    margin-top:15px;
    padding:2px 4px;
    color:#5b3d1d;
    background:#d9ad56;
    font:400 10px/1.2 var(--serif);
    transform:rotate(-1deg);
  }
  .mobilelive-paper u{
    position:absolute;
    right:18px;
    bottom:24px;
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
    bottom:28px;
    height:1px;
    background:#a93428;
    transform:rotate(-2deg);
    opacity:.6;
  }

  .mobilelive-notebook{
    min-height:194px;
    padding:25px 60px 23px 36px;
    border-radius:6px;
    background:
      linear-gradient(90deg,transparent 0 8%,rgb(176 95 67 / 17%) 8.2% 8.6%,transparent 8.8%),
      repeating-linear-gradient(0deg,#e8ddc7 0 25px,#b8b1a4 26px 27px);
  }
  .mobilelive-notebook:after{
    content:"";
    position:absolute;
    right:11%;
    top:5%;
    width:8%;
    height:89%;
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
    min-height:184px;
    padding:8px 8px 13px;
    background:#e7d8bf;
  }
  .mobilelive-photo img{
    height:184px;
    object-position:center;
    border:1px solid rgb(65 45 26 / 15%);
  }

  .mobilelive-foot{
    display:flex;
    justify-content:space-between;
    gap:14px;
    margin:0 -16px;
    padding:18px 20px 5px;
    border-top:1px solid rgb(75 54 35 / 13%);
    background:#0d5a4f;
  }
  .mobilelive-foot a{
    color:#f3e8d8;
    font:800 8px/1.2 var(--sans);
    letter-spacing:.12em;
    text-decoration:none;
    text-transform:uppercase;
  }

  @media(prefers-reduced-motion:no-preference){
    .mobilelive-card{animation:mobileDeskIn .55s ease both}
    .mobilelive-card:nth-child(2){animation-delay:.05s}
    .mobilelive-card:nth-child(3){animation-delay:.1s}
    .mobilelive-card:nth-child(4){animation-delay:.15s}
    @keyframes mobileDeskIn{
      from{opacity:0;transform:translateY(18px) rotate(0)}
      to{opacity:1}
    }
  }
}
@media(max-width:420px){
  .mobilelive{padding-inline:12px}
  .mobilelive-head{margin-inline:-12px;padding-inline:14px}
  .mobilelive-brand strong{font-size:22px}
  .mobilelive-hero{margin-inline:-12px;padding:30px 18px 22px;min-height:520px}
  .mobilelive-intro{width:78%}
  .mobilelive-intro h2{font-size:44px}
  .mobilelive-intro p{font-size:13.5px}
  .mobilelive-profile{left:4%;width:70%;bottom:16px}
  .mobilelive-hero:after{font-size:18px;right:5%;width:30%}
  .mobilelive-work{margin-inline:-12px;padding-inline:14px}
  .mobilelive-copy{width:93%;margin-left:5%}
  .mobilelive-copy strong{font-size:21px}
  .mobilelive-copy small{font-size:11px}
  .mobilelive-foot{margin-inline:-12px}
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
