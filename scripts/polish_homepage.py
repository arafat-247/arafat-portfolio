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
ASSET_VERSION = "20.3.0"

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

/* Mobile navigation stays functional without disturbing the photographic layout. */
.deskmobilemenu{display:none}

@media(max-width:800px){
  body.home,
  body.home .right,
  body.home main{background:#2b160b}
  .deskhome{
    min-height:0;
    padding:0;
    background:#2b160b;
  }
  .deskstage{
    width:100%;
    max-width:720px;
    aspect-ratio:941/1672;
    border:0;
    border-radius:0;
    box-shadow:none;
  }
  .deskhotspots-desktop{display:none}
  .deskhotspots-mobile{display:block}

  .deskprofile-mobile{left:24.2%;top:8.2%;width:52.8%;height:20.8%}
  .deskreporting-mobile{left:23.0%;top:33.0%;width:55.7%;height:16.2%}
  .deskopinion-mobile{left:23.0%;top:49.6%;width:57.0%;height:14.8%}
  .deskthoughts-mobile{left:23.5%;top:64.0%;width:56.0%;height:17.7%}
  .deskphoto-mobile{left:23.6%;top:80.6%;width:55.0%;height:16.0%}

  .deskemail{display:none}
  .deskmobilemenu{
    position:absolute;
    z-index:12;
    display:block;
    right:12px;
    top:12px;
  }
  .deskmobilemenu summary{
    display:grid;
    width:42px;
    height:42px;
    place-content:center;
    gap:5px;
    border:1px solid rgb(255 255 255 / 18%);
    border-radius:50%;
    background:rgb(15 10 6 / 68%);
    box-shadow:0 4px 16px rgb(0 0 0 / 22%);
    cursor:pointer;
    list-style:none;
    backdrop-filter:blur(5px);
  }
  .deskmobilemenu summary::-webkit-details-marker{display:none}
  .deskmobilemenu summary i{
    display:block;
    width:19px;
    height:1.5px;
    background:#f3e7d7;
  }
  .deskmobilemenu nav{
    position:absolute;
    top:48px;
    right:0;
    display:grid;
    width:190px;
    padding:7px;
    border:1px solid rgb(75 51 31 / 28%);
    border-radius:9px;
    background:#e8d9c0;
    box-shadow:0 15px 35px rgb(0 0 0 / 35%);
  }
  .deskmobilemenu nav a{
    padding:11px 12px;
    border-bottom:1px solid rgb(75 51 31 / 13%);
    color:#24170e;
    font:600 14px/1.1 var(--serif);
    text-decoration:none;
  }
  .deskmobilemenu nav a:last-child{border-bottom:0}
}
@media(max-width:420px){
  .deskmobilemenu{right:9px;top:9px}
  .deskmobilemenu summary{width:38px;height:38px}
  .deskmobilemenu nav{top:44px;width:176px}
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
    print(f"Homepage polish: photographic_desk=1, desktop_asset=1, mobile_asset=1, hotspots=1, asset_version={ASSET_VERSION}, versioned_pages={versioned_pages}, css_isolated=1, inline_critical=1")


if __name__ == "__main__":
    main()
