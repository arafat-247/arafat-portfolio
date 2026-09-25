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
ASSET_VERSION = "21.1.0"

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

.portalhome-mobile{display:none!important}

@media(max-width:800px){
  html,body{max-width:100%;overflow-x:clip}
  body.home,
  body.home .right,
  body.home main{background:#f4eee4}
  body.home .deskhome{display:none!important}
  body.home .portalhome-mobile{
    display:block!important;
    width:100%!important;
    max-width:100vw!important;
    margin:0!important;
    overflow:visible!important;
    border-radius:0!important;
    box-shadow:none!important;
    background:#f4eee4;
    color:#171512;
  }
  body.home .portalhome-mobile,
  body.home .portalhome-mobile *{box-sizing:border-box}

  /* mobile masthead */
  .portalnav{
    position:sticky;
    top:0;
    z-index:80;
    display:flex;
    min-height:62px;
    width:100%;
    align-items:center;
    justify-content:space-between;
    gap:14px;
    padding:10px 16px 9px;
    border-bottom:1px solid rgb(39 29 20 / 13%);
    color:#171512;
    background:rgb(247 241 231 / 97%);
    backdrop-filter:blur(12px);
    -webkit-backdrop-filter:blur(12px);
  }
  .portalbrand{display:grid;min-width:0;gap:2px;text-decoration:none;color:inherit}
  .portalbrand strong{font:400 clamp(20px,5.4vw,23px)/.98 var(--serif);letter-spacing:-.035em}
  .portalbrand small{font:800 6px/1 var(--sans);letter-spacing:.22em;text-transform:uppercase;color:#746654}
  .portalnavlinks{display:none}
  .portalmenu{display:block;position:relative;flex:0 0 auto}
  .portalmenu summary{
    display:grid;width:42px;height:42px;place-content:center;gap:5px;
    cursor:pointer;list-style:none;border:0;background:transparent
  }
  .portalmenu summary::-webkit-details-marker{display:none}
  .portalmenu summary i{display:block;width:26px;height:1.5px;background:#171512;transition:transform .2s ease,opacity .2s ease}
  .portalmenu[open] summary{position:fixed;z-index:103;top:10px;right:14px}
  .portalmenu[open] summary i{position:absolute}
  .portalmenu[open] summary i:nth-child(1){transform:rotate(45deg)}
  .portalmenu[open] summary i:nth-child(2){opacity:0}
  .portalmenu[open] summary i:nth-child(3){transform:rotate(-45deg)}
  .portalmenu[open]:before{
    content:"";position:fixed;z-index:100;inset:0;
    background:rgb(17 13 10 / 46%);backdrop-filter:blur(2px)
  }
  .portalmenu>nav{
    position:fixed;z-index:102;inset:0 0 0 auto;
    display:grid;width:min(86vw,350px);align-content:start;
    padding:80px 26px 28px;
    background:linear-gradient(180deg,#faf5ea,#efe2cf);
    border-left:1px solid rgb(65 46 30 / 12%);
    box-shadow:-20px 0 45px rgb(28 18 10 / 22%);
    transform:translateX(104%);
    transition:transform .26s ease;
  }
  .portalmenu[open]>nav{transform:none}
  .portalmenu>nav:before{
    content:"Arafat Rahaman";display:block;margin-bottom:16px;
    color:#0b5b50;font:400 29px/.96 var(--serif);letter-spacing:-.035em
  }
  .portalmenu>nav a{
    position:relative;padding:14px 0;border-bottom:1px solid rgb(73 52 34 / 13%);
    color:#211811;font:600 20px/1.05 var(--serif);text-decoration:none
  }
  .portalmenu>nav a:after{content:"→";position:absolute;right:0;color:#9d2e21}

  /* hero: fully contained on every phone width */
  .portalhero{
    position:relative;
    display:block;
    width:100%;
    min-height:clamp(620px,158vw,720px);
    overflow:hidden;
    padding:0;
    background:
      radial-gradient(circle at 86% 13%,rgb(218 178 95 / 42%) 0 42px,transparent 43px),
      #f4eee4;
  }
  .portalhero-copy{
    position:relative;
    z-index:5;
    width:64%;
    min-height:clamp(520px,132vw,600px);
    padding:48px 16px 84px 20px;
    color:#fff;
    background:
      radial-gradient(circle at 16% 18%,rgb(255 255 255 / 4%) 0 1px,transparent 2px) 0 0/14px 14px,
      linear-gradient(145deg,#073f38,#052e2a);
    clip-path:polygon(0 0,100% 8%,94% 78%,66% 100%,0 100%);
  }
  .portalkicker{
    display:block;margin-bottom:11px;color:#e3b46d;
    font:850 7px/1 var(--sans);letter-spacing:.19em;text-transform:uppercase
  }
  .portalhero h1{
    margin:0 0 14px;
    color:#fff;
    font:400 clamp(39px,10.8vw,49px)/.9 var(--serif);
    letter-spacing:-.05em;
  }
  .portalhero h1 em{display:block;font-style:normal}
  .portalhero-deck{
    max-width:100%;
    margin:0;
    color:#f3ede4;
    font:400 clamp(11.5px,3.2vw,13.2px)/1.42 var(--serif);
  }
  .portalhero-script{
    margin:14px 0 0;
    color:#e3b47d;
    font:600 clamp(19px,5.4vw,22px)/1 "Caveat",cursive;
  }
  .portalhero-actions{display:block;margin-top:16px}
  .portalhero-actions .portalhero-primary{display:none}
  .portalhero-actions a{
    display:inline-flex;
    min-width:0;
    min-height:42px;
    align-items:center;
    justify-content:space-between;
    gap:16px;
    padding:0 15px;
    border:1px solid rgb(255 255 255 / 66%);
    border-radius:999px;
    color:#fff;
    font:750 9px/1 var(--sans);
    text-decoration:none;
  }
  .portalhero-visual{position:absolute;z-index:3;inset:0;min-height:0}
  .portalhero-photo{
    position:absolute;
    z-index:3;
    top:18px;
    right:0;
    width:56%;
    height:clamp(430px,112vw,520px);
    margin:0;
    overflow:hidden;
    clip-path:polygon(14% 0,100% 0,100% 92%,0 100%,7% 20%);
  }
  .portalhero-photo picture,
  .portalhero-photo img{display:block;width:100%;height:100%}
  .portalhero-photo img{
    object-fit:cover;
    object-position:48% 38%;
    filter:grayscale(1) contrast(1.04);
  }
  .portalhero-photo:after{
    content:"";position:absolute;inset:0;
    background:linear-gradient(90deg,rgb(244 238 228 / 18%),transparent 20%);
    pointer-events:none;
  }
  .portalhero-panel{
    position:absolute;
    z-index:6;
    right:0;
    bottom:26px;
    width:48%;
    min-height:140px;
    background:transparent;
  }
  .portalhero-panel p{
    position:absolute;
    right:15px;
    top:16px;
    width:min(135px,82%);
    margin:0;
    color:#735d49;
    font:600 clamp(18px,5vw,22px)/1.02 "Caveat",cursive;
    transform:rotate(-7deg);
  }
  .portalhero-panel span{display:none}

  /* continuous editorial panels */
  .portalwork{position:relative;margin:0;overflow:hidden;background:#f4eee4}
  .portalgrid{display:block;width:100%;min-height:0;background:#f4eee4}
  .portalpanel{
    position:relative!important;
    left:auto!important;right:auto!important;top:auto!important;bottom:auto!important;
    display:block;width:100%!important;height:auto!important;
    margin:0!important;
    overflow:hidden;
    isolation:isolate;
    text-decoration:none;
  }
  .portalpanel:before{content:"";position:absolute;inset:0;z-index:-1;pointer-events:none}
  .portalimage{position:absolute;inset:0;z-index:-3;width:100%;height:100%;object-fit:cover}
  .portalart{
    position:absolute;inset:0;z-index:-3;
    background-image:url("assets/home/portal-reference-sprite.webp");
    background-repeat:no-repeat;background-size:100% 300%;
  }
  .portalart-opinion{background-position:center 50%}
  .portalart-thoughts{background-position:center bottom}

  .portal-reporting{
    min-height:clamp(310px,84vw,380px);
    color:#15120f;
    background:#eee8df;
    clip-path:polygon(0 0,100% 0,100% 91%,80% 86%,61% 92%,40% 100%,0 96%);
  }
  .portal-reporting .portalimage{filter:saturate(.76) brightness(1.03) contrast(.96)}
  .portal-reporting:before{
    background:linear-gradient(90deg,rgb(244 238 228 / 96%) 0 34%,rgb(244 238 228 / 44%) 60%,transparent 100%)
  }

  .portal-opinion{
    min-height:clamp(285px,76vw,340px);
    margin-top:-14px!important;
    color:#fff;
    background:#8c170e;
    clip-path:polygon(0 10%,22% 3%,46% 11%,64% 6%,84% 18%,100% 30%,100% 90%,78% 84%,57% 94%,30% 100%,0 92%);
  }
  .portal-opinion:before{background:linear-gradient(180deg,rgb(142 21 13 / 77%),rgb(104 13 8 / 90%))}
  .portal-opinion .portalart{opacity:.72;mix-blend-mode:multiply}

  .portal-thoughts{
    min-height:clamp(285px,76vw,340px);
    margin-top:-12px!important;
    color:#16130f;
    background:#f2ece2;
    clip-path:polygon(0 4%,55% 0,70% 8%,84% 27%,100% 58%,100% 100%,0 100%);
  }
  .portal-thoughts .portalart{opacity:.95;background-position:center bottom}

  .portal-photography{
    min-height:clamp(300px,80vw,360px);
    margin-top:-9px!important;
    color:#fff;
    background:#07100f;
    clip-path:polygon(0 9%,22% 0,50% 5%,72% 0,100% 5%,100% 100%,0 100%);
  }
  .portal-photography .portalimage{filter:saturate(.9) brightness(.78) contrast(1.04)}
  .portal-photography:before{background:linear-gradient(180deg,transparent 12%,rgb(3 6 6 / 35%) 56%,rgb(3 6 6 / 82%) 100%)}

  .portalnumber{
    position:absolute;z-index:5;left:21px;top:36px;
    color:currentColor;font:800 9px/1 var(--sans);letter-spacing:.08em
  }
  .portalnumber:after{
    content:"";display:inline-block;width:34px;height:1px;margin-left:9px;
    vertical-align:middle;background:currentColor;opacity:.5
  }
  .portalcopy{
    position:absolute;z-index:5;left:21px;display:block;max-width:66%
  }
  .portalcopy strong{
    display:block;margin-bottom:7px;
    color:currentColor;
    font:400 clamp(31px,8.8vw,39px)/.93 var(--serif);
    letter-spacing:-.04em
  }
  .portalcopy small{
    display:block;color:currentColor;opacity:.92;
    font:400 clamp(11px,3.1vw,13px)/1.32 var(--serif)
  }
  .portalarrow{
    position:absolute;z-index:5;left:21px;bottom:28px;
    display:grid;width:40px;height:40px;place-items:center;
    border:1px solid currentColor;border-radius:50%;
    color:currentColor;font-size:15px;font-style:normal
  }
  .portal-reporting .portalcopy{top:78px}
  .portal-reporting .portalarrow{color:#15120f}
  .portal-opinion .portalcopy{top:84px;max-width:72%}
  .portal-opinion .portalnumber{top:50px}
  .portal-thoughts .portalcopy{top:88px;max-width:64%}
  .portal-thoughts .portalnumber{top:42px}
  .portal-thoughts .portalarrow{color:#16130f}
  .portalnote{
    position:absolute;z-index:4;right:17px;top:35px;
    max-width:110px;color:#725e44;
    font:600 clamp(18px,5vw,22px)/1 "Caveat",cursive;
    transform:rotate(-7deg)
  }
  .portal-thoughts:after{
    content:"";position:absolute;z-index:1;right:11%;top:16%;
    width:90px;height:90px;border-radius:50%;
    background:rgb(220 181 87 / 45%)
  }
  .portal-photography .portalcopy{bottom:82px;top:auto;max-width:72%}
  .portal-photography .portalnumber{top:46px}

  .portal-reveal{
    opacity:0;
    transform:translateY(18px);
    transition:opacity .48s ease var(--portal-delay,0ms),transform .56s cubic-bezier(.2,.72,.2,1) var(--portal-delay,0ms)
  }
  .portal-reveal.is-visible{opacity:1;transform:none}

  .portalfooter{
    display:grid!important;
    grid-template-columns:1fr 1fr;
    gap:18px 24px;
    width:100%;
    padding:28px 20px calc(30px + env(safe-area-inset-bottom));
    color:#f2ede3;
    background:#07594e;
  }
  .portalfooter-brand{grid-column:1/-1;display:grid;gap:5px;padding-bottom:17px;border-bottom:1px solid rgb(255 255 255 / 18%)}
  .portalfooter-brand strong{font:400 24px/1 var(--serif)}
  .portalfooter-brand span{font:700 7px/1.2 var(--sans);letter-spacing:.13em;text-transform:uppercase}
  .portalfooter-brand em{margin-top:5px;color:#efc173;font:600 23px/1 "Caveat",cursive}
  .portalfooter-brand small{margin-top:7px;color:#d4dfda;font-size:9px}
  .portalfooter nav,.portalfooter-meta{display:grid;align-content:start;gap:6px}
  .portalfooter b{color:#f1c45e;font:800 8px/1 var(--sans);letter-spacing:.18em;text-transform:uppercase}
  .portalfooter a{color:#fff;font:600 10px/1.25 var(--sans);text-decoration:none}
  .portalfooter-meta{grid-column:1/-1;padding-top:2px;border-top:1px solid rgb(255 255 255 / 12%)}
  .portalfooter-meta small{color:#e1ebe6;font:800 7px/1.35 var(--sans);letter-spacing:.12em;text-transform:uppercase}
  .portalfooter-mark{display:none}
}

@media(max-width:360px){
  .portalnav{padding-inline:13px}
  .portalbrand strong{font-size:19px}
  .portalhero{min-height:620px}
  .portalhero-copy{width:66%;padding-left:16px;padding-right:12px}
  .portalhero h1{font-size:38px}
  .portalhero-deck{font-size:11.3px}
  .portalhero-photo{width:54%;height:430px}
  .portalcopy{max-width:70%}
  .portalcopy strong{font-size:30px}
}

@media(min-width:600px) and (max-width:800px){
  .portalhero{min-height:620px}
  .portalhero-copy{width:55%;min-height:560px;padding:54px 28px 90px}
  .portalhero h1{font-size:54px}
  .portalhero-deck{font-size:14px}
  .portalhero-photo{width:54%;height:560px}
  .portalhero-panel{width:42%}
  .portalcopy{max-width:52%}
}

@media(prefers-reduced-motion:reduce){
  .portal-reveal{opacity:1!important;transform:none!important;transition:none!important}
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
    print(f"Homepage polish: photographic_desktop=1, flowing_mobile=1, mobile_menu=1, mobile_contained=1, asset_version={ASSET_VERSION}, versioned_pages={versioned_pages}, css_isolated=1, inline_critical=1")


if __name__ == "__main__":
    main()
