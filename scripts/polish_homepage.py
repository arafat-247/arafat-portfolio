"""Apply the approved clean editorial homepage after final build processing."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
HOME = DIST / "index.html"
CSS = DIST / "portfolio.css"
CSS_MARKER = "/* Editorial homepage polish v18 */"
ASSET_VERSION_RE = re.compile(r"portfolio\.css\?v=[0-9.]+", re.I)
SCRIPT_VERSION_RE = re.compile(r"portfolio\.js\?v=[0-9.]+", re.I)
ASSET_VERSION = "18.0.1"

HOME_CSS = r"""
/* Editorial homepage polish v18 */
body.home main{background:var(--paper)}
body.home .heroquote{margin:0}

body.home .tile-reporting:after{background:linear-gradient(90deg,rgb(5 43 37 / 91%) 0%,rgb(5 43 37 / 66%) 52%,rgb(5 43 37 / 28%) 100%)}
body.home .tile-opinion:after{background:linear-gradient(90deg,rgb(120 47 30 / 91%) 0%,rgb(120 47 30 / 66%) 53%,rgb(120 47 30 / 28%) 100%)}
body.home .tile-thoughts:after{background:linear-gradient(90deg,rgb(37 48 28 / 90%) 0%,rgb(37 48 28 / 63%) 55%,rgb(37 48 28 / 28%) 100%)}
body.home .tile-photos:after{background:linear-gradient(90deg,rgb(9 25 23 / 88%) 0%,rgb(9 25 23 / 58%) 54%,rgb(9 25 23 / 20%) 100%)}

body.home .tileno{
  position:absolute;z-index:3;left:22px;top:18px;color:#f0b07f;
  font:800 10px/1 var(--sans);letter-spacing:.12em
}
body.home .tileexplore{
  display:block;width:max-content;margin-top:15px;padding-bottom:3px;
  border-bottom:1px solid rgb(255 255 255 / 78%);
  color:#fff;font:700 11px/1.2 var(--sans);font-style:normal
}

@media(min-width:801px){
  body.home .homecontent{
    width:min(100% - 48px,1200px);
    margin:0 auto;
    padding:24px 0 30px;
  }
  body.home .homeprofile{
    position:relative;isolation:isolate;display:block;min-height:365px;
    margin:0 0 7px;padding:0;overflow:hidden;color:#f4f2eb;background:#0b3a33
  }
  body.home .homeprofile>img{
    position:absolute;inset:calc(var(--hero-shift,0px) * -1) 0 auto auto;z-index:0;
    width:66%;height:calc(100% + 24px);max-width:none;min-height:0;
    object-fit:cover;object-position:58% 31%;filter:grayscale(1);
    -webkit-mask-image:linear-gradient(90deg,transparent 0%,#000 29%);
    mask-image:linear-gradient(90deg,transparent 0%,#000 29%);
    transition:transform .6s cubic-bezier(.2,.65,.25,1)
  }
  body.home .homeprofile:after{
    content:"";position:absolute;inset:0;z-index:1;pointer-events:none;
    background:
      linear-gradient(90deg,#0b3a33 0%,#0b3a33 35%,rgb(11 58 51 / 90%) 45%,rgb(11 58 51 / 20%) 70%,transparent 86%),
      linear-gradient(0deg,rgb(7 37 32 / 42%),transparent 42%)
  }
  body.home .homeprofile>div{
    position:relative;z-index:3;display:flex;width:45%;min-height:365px;
    flex-direction:column;align-items:flex-start;justify-content:center;padding:38px 40px
  }
  body.home .homeprofile>div>span{
    color:#efaa82;font:800 10px/1.3 var(--sans);letter-spacing:.17em;text-transform:uppercase
  }
  body.home .homeprofile h2{
    margin:13px 0 0;color:#fff;font:400 clamp(55px,5.8vw,78px)/.88 var(--serif);
    letter-spacing:-.035em
  }
  body.home .homeprofile h2 span,body.home .homeprofile h2 em{display:block}
  body.home .homeprofile h2 em{font-weight:400;font-style:italic}
  body.home .homeprofile p{
    display:block;max-width:390px;margin:20px 0 0;overflow:visible;color:rgb(255 255 255 / 83%);
    font:400 15px/1.55 var(--sans);-webkit-line-clamp:unset;text-wrap:pretty
  }
  body.home .homeprofile nav{display:flex;gap:25px;margin-top:17px}
  body.home .homeprofile a{
    min-height:0;padding:0 0 5px;border-bottom:1px solid rgb(255 255 255 / 74%);
    color:#fff;font:700 12px/1.3 var(--sans);text-decoration:none;
    transition:color .18s ease,border-color .18s ease,transform .18s ease
  }
  body.home .homeprofile a:hover{color:#efb398;border-color:#efb398;transform:translateX(2px)}
  body.home .heroquote{
    position:absolute;z-index:3;right:24px;top:44%;width:150px;transform:translateY(-50%);
    padding-top:16px;border-top:1px solid #315c56;color:#173f39;
    font:italic 20px/1.12 var(--serif);text-align:left
  }

  body.home .tiles{grid-template-columns:repeat(2,minmax(0,1fr));gap:3px}
  body.home .tile{
    min-height:214px;padding:46px 24px 21px;transform:translateZ(0);
    box-shadow:none;transition:transform .24s ease,box-shadow .24s ease,filter .24s ease
  }
  body.home .tile:before{
    content:"";position:absolute;inset:0;z-index:0;pointer-events:none;
    background:radial-gradient(circle at var(--mx,50%) var(--my,50%),rgb(255 255 255 / 13%),transparent 34%);
    opacity:0;transition:opacity .22s ease
  }
  body.home .tile:hover:before{opacity:1}
  body.home .tile:hover{transform:translateY(-3px);box-shadow:0 17px 38px rgb(10 35 30 / 16%)}
  body.home .tile img{
    inset:-5px;width:calc(100% + 10px);height:calc(100% + 10px);
    filter:saturate(.72) contrast(.97);transition:transform .65s cubic-bezier(.2,.65,.25,1),filter .3s ease
  }
  body.home .tile:hover img{transform:scale(1.045);filter:saturate(.9) contrast(1)}
  body.home .tile span{z-index:2}
  body.home .tile strong{font:400 clamp(29px,2.8vw,39px)/.98 var(--serif);letter-spacing:-.025em}
  body.home .tile small{max-width:310px;margin-top:8px;color:rgb(255 255 255 / 79%);font-size:12px;line-height:1.35}
  body.home .tile>i{
    right:22px;top:auto;bottom:20px;display:grid;width:34px;height:34px;place-items:center;
    border:1px solid rgb(255 255 255 / 65%);border-radius:50%;font-size:15px;
    transition:transform .22s ease,background .22s ease
  }
  body.home .tile:hover>i{transform:translateX(3px);background:rgb(255 255 255 / 10%)}

  body.home .homecontact{
    grid-template-columns:minmax(0,1fr) auto;min-height:76px;gap:24px;
    margin:8px 0 0;padding:18px 28px;background:#ad513b
  }
  body.home .homecontact strong{font:400 clamp(28px,3vw,38px)/1 var(--serif)}
  body.home .homecontact a{
    transition:transform .18s ease,border-color .18s ease;
    font-family:var(--serif);font-weight:400
  }
  body.home .homecontact a:hover{transform:translateX(3px)}

  body.home.home-motion .homeprofile,
  body.home.home-motion .tile,
  body.home.home-motion .homecontact{opacity:0;transform:translateY(12px)}
  body.home.home-motion .homeprofile.is-visible,
  body.home.home-motion .tile.is-visible,
  body.home.home-motion .homecontact.is-visible{
    opacity:1;transform:none;transition:opacity .52s ease,transform .52s cubic-bezier(.2,.7,.25,1),box-shadow .24s ease
  }
  body.home.home-motion .tile.is-visible:hover{transform:translateY(-3px)}
}

@media(max-width:800px){
  body.home .heroquote{display:none}
  body.home .tileno{left:16px;top:14px;font-size:9px}
  body.home .tileexplore{display:none}
  body.home .tile{padding-top:34px}
  body.home .tile img{filter:brightness(.74) saturate(.74)}
}

@media(prefers-reduced-motion:reduce){
  body.home.home-motion .homeprofile,
  body.home.home-motion .tile,
  body.home.home-motion .homecontact{opacity:1;transform:none}
}
""".strip()


def main() -> None:
    if not HOME.is_file() or not CSS.is_file():
        raise FileNotFoundError("Build output is incomplete; run scripts/build.py first")

    source = HOME.read_text(encoding="utf-8")
    source = ASSET_VERSION_RE.sub(f"portfolio.css?v={ASSET_VERSION}", source)
    source = SCRIPT_VERSION_RE.sub(f"portfolio.js?v={ASSET_VERSION}", source)
    HOME.write_text(source, encoding="utf-8")

    css = CSS.read_text(encoding="utf-8")
    marker_index = css.find(CSS_MARKER)
    if marker_index >= 0:
        css = css[:marker_index].rstrip()
    css.write_text(css + "\n\n" + HOME_CSS + "\n", encoding="utf-8")
    print(f"Homepage polish: editorial_desktop=1, interactions=1, asset_version={ASSET_VERSION}")


if __name__ == "__main__":
    main()
