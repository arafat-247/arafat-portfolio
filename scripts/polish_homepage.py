"""Apply the approved reference-led editorial homepage after final build processing."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
HOME = DIST / "index.html"
CSS = DIST / "portfolio.css"
CSS_MARKER = "/* Editorial homepage reference v18.1 */"
ASSET_VERSION_RE = re.compile(r"portfolio\.css\?v=[0-9.]+", re.I)
SCRIPT_VERSION_RE = re.compile(r"portfolio\.js\?v=[0-9.]+", re.I)
ASSET_VERSION = "18.2.0"

HOME_CSS = r"""
/* Editorial homepage reference v18.1 */
body.home main{background:#f7f3ea}
body.home .heroquote{margin:0}
body.home .herotagline{font-family:"Caveat",cursive}

body.home .tile-reporting:after{background:linear-gradient(90deg,rgb(8 50 44 / 92%) 0%,rgb(8 50 44 / 66%) 54%,rgb(8 50 44 / 22%) 100%)}
body.home .tile-opinion:after{background:linear-gradient(90deg,rgb(124 50 31 / 92%) 0%,rgb(124 50 31 / 64%) 54%,rgb(124 50 31 / 20%) 100%)}
body.home .tile-thoughts:after{background:linear-gradient(90deg,rgb(37 48 27 / 91%) 0%,rgb(37 48 27 / 62%) 54%,rgb(37 48 27 / 18%) 100%)}
body.home .tile-photos:after{background:linear-gradient(90deg,rgb(13 34 31 / 91%) 0%,rgb(13 34 31 / 59%) 54%,rgb(13 34 31 / 16%) 100%)}

body.home .tileno{
  position:absolute;z-index:3;left:20px;top:15px;color:#e7a86b;
  font:800 10px/1 var(--sans);letter-spacing:.13em
}
body.home .tileexplore{
  display:block;width:max-content;margin-top:14px;padding-bottom:3px;
  border-bottom:1px solid rgb(255 255 255 / 78%);
  color:#fff;font:700 11px/1.2 var(--sans);font-style:normal
}
body.home .tilewords{display:none}

@media(min-width:801px){
  body.home .homecontent{
    width:min(100% - 48px,1080px);
    margin:0 auto;
    padding:14px 0 22px;
  }

  body.home .homeprofile{
    position:relative;isolation:isolate;display:block;min-height:320px;
    margin:0 0 14px;padding:0;overflow:hidden;color:#f7f2e9;background:#0a443b
  }
  body.home .homeprofile>img{
    position:absolute;inset:calc(var(--hero-shift,0px) * -1) 0 auto auto;z-index:0;
    width:68%;height:calc(100% + 20px);max-width:none;min-height:0;
    object-fit:cover;object-position:54% 30%;filter:grayscale(1) contrast(1.02);
    -webkit-mask-image:linear-gradient(90deg,transparent 0%,#000 26%);
    mask-image:linear-gradient(90deg,transparent 0%,#000 26%);
  }
  body.home .homeprofile:after{
    content:"";position:absolute;inset:0;z-index:1;pointer-events:none;
    background:
      linear-gradient(90deg,#0a443b 0%,#0a443b 35%,rgb(10 68 59 / 93%) 43%,rgb(10 68 59 / 26%) 70%,transparent 88%),
      linear-gradient(0deg,rgb(4 36 31 / 34%),transparent 42%)
  }
  body.home .homeprofile>div{
    position:relative;z-index:3;display:flex;width:47%;min-height:320px;
    flex-direction:column;align-items:flex-start;justify-content:center;padding:26px 36px 22px
  }
  body.home .homeprofile>div>span{
    color:#efad73;font:800 10px/1.3 var(--sans);letter-spacing:.18em;text-transform:uppercase
  }
  body.home .homeprofile h2{
    margin:10px 0 0;color:#fff;font:400 clamp(54px,5.3vw,70px)/.9 var(--serif);
    letter-spacing:-.03em
  }
  body.home .homeprofile h2 span,body.home .homeprofile h2 em{display:block}
  body.home .homeprofile h2 em{font-weight:400;font-style:italic}
  body.home .homeprofile p{
    display:block;max-width:405px;margin:16px 0 0;overflow:visible;color:rgb(255 255 255 / 88%);
    font:400 15px/1.45 var(--serif);-webkit-line-clamp:unset
  }
  body.home .homeprofile nav{display:flex;gap:33px;margin-top:14px}
  body.home .homeprofile a{
    min-height:0;padding:0 0 4px;border-bottom:1px solid rgb(255 255 255 / 77%);
    color:#fff;font:400 14px/1.2 var(--serif);text-decoration:none;
    transition:color .18s ease,border-color .18s ease,transform .18s ease
  }
  body.home .homeprofile a:hover{color:#efb98b;border-color:#efb98b;transform:translateX(2px)}
  body.home .homeprofile .herotagline{
    margin:16px 0 0;color:#d1a171;font:500 23px/1 "Caveat",cursive;
    transform:rotate(-1.2deg)
  }
  body.home .heroquote{
    position:absolute;z-index:3;right:28px;top:47%;width:118px;transform:translateY(-50%);
    padding-top:14px;border-top:2px solid #315d56;color:#124b43;
    font:italic 19px/1.12 var(--serif);text-align:left
  }

  body.home .homeintro{
    display:grid;grid-template-columns:minmax(280px,.9fr) minmax(0,1.1fr);
    align-items:end;gap:34px;margin:0 0 7px;padding:0;
  }
  body.home .homeintro>div>span{
    display:block;margin-bottom:2px;color:#b8563f;font:800 10px/1.2 var(--sans);
    letter-spacing:.2em;text-transform:uppercase
  }
  body.home .homeintro h1{
    margin:0;color:#12130f;font:400 clamp(42px,4vw,52px)/.92 var(--serif);
    letter-spacing:-.035em
  }
  body.home .homeintro p{
    margin:0 0 6px;color:#30322d;font:400 14px/1.4 var(--serif);text-align:right
  }

  body.home .tiles{grid-template-columns:repeat(2,minmax(0,1fr));gap:3px}
  body.home .tile{
    min-height:172px;padding:39px 20px 16px;transform:translateZ(0);
    box-shadow:none;transition:transform .23s ease,box-shadow .23s ease,filter .23s ease
  }
  body.home .tile:before{
    content:"";position:absolute;inset:0;z-index:0;pointer-events:none;
    background:radial-gradient(circle at var(--mx,50%) var(--my,50%),rgb(255 255 255 / 12%),transparent 34%);
    opacity:0;transition:opacity .2s ease
  }
  body.home .tile:hover:before{opacity:1}
  body.home .tile:hover{transform:translateY(-2px);box-shadow:0 12px 28px rgb(10 35 30 / 14%)}
  body.home .tile img{
    inset:-4px;width:calc(100% + 8px);height:calc(100% + 8px);
    filter:saturate(.7) contrast(.96) brightness(.88);
    transition:transform .55s cubic-bezier(.2,.65,.25,1),filter .3s ease
  }
  body.home .tile:hover img{transform:scale(1.035);filter:saturate(.86) contrast(1) brightness(.92)}
  body.home .tile .tilecopy{position:relative;z-index:2;display:block;width:64%}
  body.home .tile strong{font:400 clamp(27px,2.45vw,35px)/.96 var(--serif);letter-spacing:-.02em}
  body.home .tile small{display:block;max-width:290px;margin-top:7px;color:rgb(255 255 255 / 86%);font:400 12px/1.25 var(--serif)}
  body.home .tilewords{
    position:absolute;right:16px;bottom:17px;z-index:2;display:block;width:82px;
    padding-top:11px;border-top:1px solid rgb(255 255 255 / 58%);
    color:rgb(255 255 255 / 86%);font:700 9px/1.45 var(--sans);letter-spacing:.05em
  }
  body.home .tile>i{
    left:112px;right:auto;top:auto;bottom:13px;display:grid;width:32px;height:32px;place-items:center;
    border:1px solid rgb(255 255 255 / 72%);border-radius:50%;font-size:14px;
    transition:transform .2s ease,background .2s ease
  }
  body.home .tile:hover>i{transform:translateX(2px);background:rgb(255 255 255 / 10%)}

  body.home .homecontact{
    grid-template-columns:minmax(0,1fr) auto;min-height:58px;gap:24px;
    margin:8px 0 14px;padding:12px 28px;background:#b9533d
  }
  body.home .homecontact strong{font:400 clamp(25px,2.6vw,32px)/1 var(--serif)}
  body.home .homecontact a{
    padding:4px 0;border-bottom:1px solid currentColor;
    font:400 14px/1.2 var(--serif);transition:transform .18s ease
  }
  body.home .homecontact a:hover{transform:translateX(3px)}

  body.home.home-motion .homeprofile,
  body.home.home-motion .homeintro,
  body.home.home-motion .tile,
  body.home.home-motion .homecontact{opacity:0;transform:translateY(10px)}
  body.home.home-motion .homeprofile.is-visible,
  body.home.home-motion .homeintro.is-visible,
  body.home.home-motion .tile.is-visible,
  body.home.home-motion .homecontact.is-visible{
    opacity:1;transform:none;
    transition:opacity .48s ease,transform .48s cubic-bezier(.2,.7,.25,1),box-shadow .23s ease
  }
  body.home.home-motion .tile.is-visible:hover{transform:translateY(-2px)}
}

@media(max-width:800px){
  body.home .heroquote,body.home .tilewords{display:none}
  body.home .homeprofile .herotagline{display:none}
  body.home .homeintro{display:grid;grid-template-columns:1fr;gap:8px;margin:0 0 18px}
  body.home .homeintro>div>span{display:block;color:var(--accent);font-size:10px;font-weight:800;letter-spacing:.14em;text-transform:uppercase}
  body.home .homeintro h1{margin:2px 0 0;font:400 43px/1 var(--serif)}
  body.home .homeintro p{margin:0;color:var(--muted);font-size:14px}
  body.home .tileno{left:16px;top:14px;font-size:9px}
  body.home .tileexplore{display:none}
  body.home .tile{padding-top:34px}
  body.home .tile img{filter:brightness(.73) saturate(.72)}
}

@media(prefers-reduced-motion:reduce){
  body.home.home-motion .homeprofile,
  body.home.home-motion .homeintro,
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

    css_text = CSS.read_text(encoding="utf-8")
    marker_index = css_text.find(CSS_MARKER)
    if marker_index >= 0:
        css_text = css_text[:marker_index].rstrip()
    CSS.write_text(css_text + "\n\n" + HOME_CSS + "\n", encoding="utf-8")
    print(f"Homepage polish: reference_match=1, compact_cards=1, work_heading=1, asset_version={ASSET_VERSION}")


if __name__ == "__main__":
    main()
