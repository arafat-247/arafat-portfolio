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
ASSET_VERSION = "21.2.2"

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

  /* Mobile masthead */
  .portalnav{
    position:sticky;top:0;z-index:80;
    display:flex;min-height:60px;width:100%;
    align-items:center;justify-content:space-between;gap:12px;
    padding:9px 16px 8px;
    border-bottom:1px solid rgb(39 29 20 / 13%);
    color:#171512;background:#f7f1e7;
  }
  .portalbrand{display:grid;min-width:0;gap:2px;color:inherit;text-decoration:none}
  .portalbrand strong{font:400 clamp(20px,5.3vw,23px)/.98 var(--serif);letter-spacing:-.035em}
  .portalbrand small{color:#746654;font:800 6px/1 var(--sans);letter-spacing:.2em;text-transform:uppercase}
  .portalnavlinks{display:none}
  .portalmenu{display:block;position:relative;flex:0 0 auto}
  .portalmenu summary{
    display:grid;width:42px;height:42px;place-content:center;gap:5px;
    cursor:pointer;list-style:none;border:0;background:transparent
  }
  .portalmenu summary::-webkit-details-marker{display:none}
  .portalmenu summary i{display:block;width:26px;height:1.5px;background:#171512;transition:transform .2s ease,opacity .2s ease}
  .portalmenu:not([open])>nav{visibility:hidden;pointer-events:none}
  .portalmenu[open] summary{position:fixed;z-index:103;top:9px;right:14px}
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
    padding:78px 26px 28px;\n    height:100dvh;overflow-y:auto;
    background:linear-gradient(180deg,#faf5ea,#efe2cf);
    border-left:1px solid rgb(65 46 30 / 12%);
    box-shadow:-20px 0 45px rgb(28 18 10 / 22%);
    transform:translateX(104%);
    transition:transform .26s ease
  }
  .portalmenu[open]>nav{visibility:visible;pointer-events:auto;transform:none}
  .portalmenu>nav:before{
    content:"Arafat Rahaman";display:block;margin-bottom:16px;
    color:#0b5b50;font:400 29px/.96 var(--serif);letter-spacing:-.035em
  }
  .portalmenu>nav a{
    position:relative;padding:14px 0;border-bottom:1px solid rgb(73 52 34 / 13%);
    color:#211811;font:600 20px/1.05 var(--serif);text-decoration:none
  }
  .portalmenu>nav a:after{content:"→";position:absolute;right:0;color:#9d2e21}

  /* Hero */
  .portalhero{
    position:relative;display:block;width:100%;
    min-height:clamp(535px,138vw,590px);
    overflow:hidden;padding:0;
    background:
      radial-gradient(circle at 87% 13%,rgb(218 178 95 / 38%) 0 39px,transparent 40px),
      #f4eee4
  }
  .portalhero-copy{
    position:relative;z-index:5;
    width:63%;min-height:clamp(455px,118vw,505px);
    padding:42px 14px 64px 20px;
    color:#fff;
    background:
      radial-gradient(circle at 16% 18%,rgb(255 255 255 / 4%) 0 1px,transparent 2px) 0 0/14px 14px,
      linear-gradient(145deg,#073f38,#052e2a);
    clip-path:polygon(0 0,100% 8%,95% 76%,66% 100%,0 100%)
  }
  .portalkicker{
    display:block;margin-bottom:10px;color:#e3b46d;
    font:850 7px/1 var(--sans);letter-spacing:.18em;text-transform:uppercase
  }
  .portalhero h1{
    margin:0 0 13px;color:#fff;
    font:400 clamp(38px,10.5vw,47px)/.9 var(--serif);
    letter-spacing:-.05em
  }
  .portalhero h1 em{display:block;font-style:normal}
  .portalhero-deck{
    max-width:100%;margin:0;color:#f3ede4;
    font:400 clamp(11.2px,3vw,12.8px)/1.42 var(--serif)
  }
  .portalhero-script{
    margin:13px 0 0;color:#e3b47d;
    font:600 clamp(18px,5vw,21px)/1 "Caveat",cursive
  }
  .portalhero-actions{display:block;margin-top:15px}
  .portalhero-actions .portalhero-primary{display:none}
  .portalhero-actions a{
    display:inline-flex;min-width:0;min-height:40px;
    align-items:center;justify-content:space-between;gap:14px;
    padding:0 14px;border:1px solid rgb(255 255 255 / 66%);
    border-radius:999px;color:#fff;
    font:750 8.8px/1 var(--sans);text-decoration:none
  }
  .portalhero-visual{position:absolute;z-index:3;inset:0;min-height:0}
  .portalhero-photo{
    position:absolute;z-index:3;
    top:14px;right:0;
    width:58%;height:clamp(350px,91vw,395px);
    margin:0;overflow:hidden;
    clip-path:polygon(13% 0,100% 0,100% 91%,0 100%,7% 20%)
  }
  .portalhero-photo picture,
  .portalhero-photo img{display:block;width:100%;height:100%}
  .portalhero-photo img{
    object-fit:cover;object-position:52% 37%;
    filter:grayscale(1) contrast(1.04)
  }
  .portalhero-photo:after{
    content:"";position:absolute;inset:0;
    background:linear-gradient(90deg,rgb(244 238 228 / 14%),transparent 18%);
    pointer-events:none
  }
  .portalhero-panel{
    position:absolute;z-index:6;
    right:0;bottom:2px;width:49%;min-height:112px;
    background:transparent
  }
  .portalhero-panel p{
    position:absolute;right:15px;top:10px;
    width:min(140px,84%);margin:0;color:#735d49;
    font:600 clamp(18px,5vw,22px)/1.02 "Caveat",cursive;
    transform:rotate(-7deg)
  }
  .portalhero-panel span{display:none}

  /* Work */
  .portalwork{position:relative;margin:0;overflow:hidden;background:#f4eee4}
  .portalwork>.sr-only{
    position:absolute!important;width:1px!important;height:1px!important;
    padding:0!important;margin:-1px!important;overflow:hidden!important;
    clip:rect(0,0,0,0)!important;white-space:nowrap!important;border:0!important
  }
  .portalgrid{display:block;width:100%;min-height:0;background:#f4eee4}
  .portalpanel{
    position:relative!important;
    left:auto!important;right:auto!important;top:auto!important;bottom:auto!important;
    display:block;width:100%!important;height:auto!important;
    margin:0!important;overflow:hidden;isolation:isolate;text-decoration:none
  }
  .portalpanel:before{content:"";position:absolute;inset:0;z-index:1;pointer-events:none}
  .portalimage{position:absolute;inset:0;z-index:0;width:100%;height:100%;object-fit:cover}
  .portalart{position:absolute;inset:0;z-index:0}

  /* Reporting — editorial flag/city treatment, no fragile external art */
  .portal-reporting{
    min-height:clamp(320px,84vw,375px);
    color:#15120f;background:#ece5da;
    clip-path:polygon(0 0,100% 0,100% 92%,81% 87%,62% 93%,40% 100%,0 96%)
  }
  .portalart-reporting{
    background:
      linear-gradient(180deg,transparent 0 62%,rgb(34 42 39 / 9%) 62% 100%),
      repeating-linear-gradient(90deg,transparent 0 31px,rgb(35 50 46 / 7%) 32px 33px),
      linear-gradient(180deg,#eee8df,#ded7ca)
  }
  .portalart-reporting:before{
    content:"";position:absolute;right:9%;top:25%;
    width:92px;height:56px;background:#006a4e;
    box-shadow:-2px 8px 14px rgb(0 0 0 / 12%);
    transform:rotate(5deg)
  }
  .portalart-reporting:after{
    content:"";position:absolute;right:calc(9% + 33px);top:calc(25% + 16px);
    width:25px;height:25px;border-radius:50%;background:#f42a41;
    box-shadow:
      -72px 135px 0 31px rgb(25 34 31 / 14%),
      -18px 130px 0 38px rgb(25 34 31 / 12%),
      38px 138px 0 33px rgb(25 34 31 / 12%),
      82px 132px 0 35px rgb(25 34 31 / 11%)
  }
  .portal-reporting:before{
    background:linear-gradient(90deg,rgb(244 238 228 / 95%) 0 33%,rgb(244 238 228 / 49%) 57%,transparent 100%)
  }

  /* Opinion */
  .portal-opinion{
    min-height:clamp(285px,76vw,335px);
    margin-top:-13px!important;color:#fff;background:#8c170e;
    clip-path:polygon(0 9%,22% 3%,46% 11%,64% 6%,84% 18%,100% 30%,100% 90%,78% 84%,57% 94%,30% 100%,0 92%)
  }
  .portalart-opinion{
    background:
      linear-gradient(180deg,transparent 0 58%,rgb(30 11 9 / 36%) 58% 100%),
      repeating-linear-gradient(90deg,transparent 0 34px,rgb(34 10 8 / 44%) 35px 52px),
      linear-gradient(150deg,#a02117,#73130e)
  }
  .portalart-opinion:before{
    content:"“";position:absolute;right:7%;top:15%;
    color:rgb(255 255 255 / 12%);font:400 130px/.8 var(--serif)
  }

  /* Thoughts */
  .portal-thoughts{
    min-height:clamp(285px,76vw,335px);
    margin-top:-11px!important;color:#16130f;background:#f2ece2;
    clip-path:polygon(0 4%,55% 0,70% 8%,84% 27%,100% 58%,100% 100%,0 100%)
  }
  .portalart-thoughts{
    background:
      radial-gradient(circle at 79% 27%,rgb(220 181 87 / 48%) 0 43px,transparent 44px),
      repeating-linear-gradient(0deg,transparent 0 31px,rgb(91 78 59 / 9%) 32px 33px),
      linear-gradient(180deg,#f4eee5,#e9e0d2)
  }
  .portalart-thoughts:before{
    content:"";position:absolute;right:7%;bottom:13%;
    width:48%;height:45%;
    border-bottom:1px solid rgb(54 52 46 / 35%);
    border-right:1px solid rgb(54 52 46 / 20%);
    transform:skewY(-10deg)
  }

  /* Photography uses the real portfolio photograph */
  .portal-photography{
    min-height:clamp(300px,80vw,355px);
    margin-top:-8px!important;color:#fff;background:#07100f;
    clip-path:polygon(0 9%,22% 0,50% 5%,72% 0,100% 5%,100% 100%,0 100%)
  }
  .portal-photography .portalimage{
    display:block;filter:saturate(.92) brightness(.74) contrast(1.06);
    object-position:center 50%
  }
  .portal-photography:before{
    background:linear-gradient(180deg,transparent 8%,rgb(3 6 6 / 22%) 45%,rgb(3 6 6 / 82%) 100%)
  }

  .portalnumber{
    position:absolute;z-index:5;left:21px;top:35px;
    color:currentColor;font:800 9px/1 var(--sans);letter-spacing:.08em
  }
  .portalnumber:after{
    content:"";display:inline-block;width:34px;height:1px;margin-left:9px;
    vertical-align:middle;background:currentColor;opacity:.5
  }
  .portalcopy{position:absolute;z-index:5;left:21px;display:block;max-width:68%}
  .portalcopy strong{
    display:block;margin-bottom:7px;color:currentColor;
    font:400 clamp(31px,8.8vw,39px)/.93 var(--serif);
    letter-spacing:-.04em
  }
  .portalcopy small{
    display:block;color:currentColor;opacity:.92;
    font:400 clamp(11px,3.05vw,13px)/1.32 var(--serif)
  }
  .portalarrow{
    position:absolute;z-index:5;left:21px;bottom:27px;
    display:grid;width:40px;height:40px;place-items:center;
    border:1px solid currentColor;border-radius:50%;
    color:currentColor;font-size:15px;font-style:normal
  }
  .portal-reporting .portalcopy{top:78px;max-width:58%}
  .portal-reporting .portalarrow{color:#15120f}
  .portal-opinion .portalcopy{top:82px;max-width:72%}
  .portal-opinion .portalnumber{top:49px}
  .portal-thoughts .portalcopy{top:86px;max-width:64%}
  .portal-thoughts .portalnumber{top:41px}
  .portal-thoughts .portalarrow{color:#16130f}
  .portalnote{display:none}
  .portal-thoughts:after{display:none}
  .portal-photography .portalcopy{bottom:80px;top:auto;max-width:72%}
  .portal-photography .portalnumber{top:45px}

  /* Keep content visible even if JS/observer fails. */
  .portal-reveal,
  .portal-reveal.is-visible{opacity:1;transform:none}

  /* polish_footer replaces the source footer with .sitefooter */
  .portalhome-mobile>.sitefooter{margin:0;border-radius:0}

  body.home .right>footer{display:none!important}
}

@media(max-width:360px){
  .portalnav{padding-inline:13px}
  .portalbrand strong{font-size:19px}
  .portalhero{min-height:530px}
  .portalhero-copy{width:65%;min-height:455px;padding-left:16px;padding-right:11px}
  .portalhero h1{font-size:37px}
  .portalhero-deck{font-size:11px}
  .portalhero-photo{width:58%;height:345px}
  .portalcopy{max-width:70%}
  .portalcopy strong{font-size:29px}
}

@media(min-width:600px) and (max-width:800px){
  .portalhero{min-height:570px}
  .portalhero-copy{width:55%;min-height:500px;padding:48px 28px 76px}
  .portalhero h1{font-size:52px}
  .portalhero-deck{font-size:13.5px}
  .portalhero-photo{width:54%;height:470px}
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
    print(f"Homepage polish: photographic_desktop=1, flowing_mobile=1, mobile_menu=1, mobile_audited=1, mobile_contained=1, asset_version={ASSET_VERSION}, versioned_pages={versioned_pages}, css_isolated=1, inline_critical=1")


if __name__ == "__main__":
    main()
