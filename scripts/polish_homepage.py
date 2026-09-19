"""Apply the approved reference-led editorial homepage after final build processing."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
HOME = DIST / "index.html"
CSS = DIST / "portfolio.css"
CSS_MARKER = "/* Editorial homepage responsive v18.3 */"
ASSET_VERSION_RE = re.compile(r"portfolio\.css\?v=[0-9.]+", re.I)
SCRIPT_VERSION_RE = re.compile(r"portfolio\.js\?v=[0-9.]+", re.I)
ASSET_VERSION = "18.3.0"

HOME_CSS = r"""
/* Editorial homepage responsive v18.3 */
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


/* Responsive editorial rhythm */
@media(min-width:981px){
  body.home .homeprofile{
    min-height:338px;
    box-shadow:0 12px 34px rgb(9 42 36 / 8%);
  }
  body.home .homeprofile:before{
    content:"";
    position:absolute;
    inset:0;
    z-index:2;
    pointer-events:none;
    background:radial-gradient(circle at var(--hero-hx,66%) var(--hero-hy,42%),rgb(255 255 255 / 10%),transparent 24%);
    opacity:.45;
    transition:opacity .25s ease;
  }
  body.home .homeprofile:hover:before{opacity:.72}
  body.home .homeprofile>img{
    transform:translate3d(var(--hero-x,0),calc(var(--hero-y,0) - var(--hero-shift,0px)),0) scale(1.015);
    transition:transform .5s cubic-bezier(.2,.65,.25,1),filter .3s ease;
  }

  body.home .tiles{
    display:grid;
    grid-template-columns:1.18fr .82fr;
    grid-template-areas:
      "reporting opinion"
      "thoughts photos";
    gap:4px;
  }
  body.home .tile-reporting{grid-area:reporting;min-height:205px}
  body.home .tile-opinion{grid-area:opinion;min-height:205px}
  body.home .tile-thoughts{grid-area:thoughts;min-height:185px}
  body.home .tile-photos{grid-area:photos;min-height:185px}
  body.home .tile{
    transform:translate3d(0,0,0);
    transition:transform .25s cubic-bezier(.2,.7,.25,1),box-shadow .25s ease,filter .25s ease;
  }
  body.home .tile img{
    transform:translate3d(var(--ix,0),var(--iy,0),0) scale(1.035);
  }
  body.home .tile:hover img{
    transform:translate3d(var(--ix,0),var(--iy,0),0) scale(1.07);
  }
  body.home .tile-reporting:hover,
  body.home .tile-thoughts:hover{transform:translate3d(-2px,-3px,0)}
  body.home .tile-opinion:hover,
  body.home .tile-photos:hover{transform:translate3d(2px,-3px,0)}
  body.home .tile .tilecopy{width:min(68%,360px)}
  body.home .tilewords{transition:transform .22s ease,opacity .22s ease}
  body.home .tile:hover .tilewords{transform:translateX(-4px);opacity:1}
  body.home .tileexplore{transition:letter-spacing .18s ease,border-color .18s ease}
  body.home .tile:hover .tileexplore{letter-spacing:.025em;border-color:#efb398}
}

@media(min-width:1180px){
  body.home .homecontent{width:min(100% - 64px,1120px)}
  body.home .homeprofile{min-height:352px}
  body.home .tile-reporting,
  body.home .tile-opinion{min-height:215px}
  body.home .tile-thoughts,
  body.home .tile-photos{min-height:195px}
}

@media(min-width:801px) and (max-width:980px){
  body.home .homecontent{width:min(100% - 36px,920px)}
  body.home .homeprofile{min-height:300px}
  body.home .homeprofile>div{width:52%;min-height:300px;padding:24px 28px}
  body.home .homeprofile h2{font-size:clamp(48px,6vw,60px)}
  body.home .heroquote{display:none}
  body.home .homeintro{grid-template-columns:1fr;gap:7px}
  body.home .homeintro p{text-align:left}
  body.home .tiles{grid-template-columns:1fr 1fr;gap:4px}
  body.home .tile{min-height:176px}
  body.home .tilewords{display:none}
}

@media(max-width:800px){
  body.home .homecontent{padding-top:12px}
  body.home .homeprofile{
    position:relative;
    display:block;
    min-height:0;
    margin:0 -22px 26px;
    border-radius:0;
    overflow:hidden;
  }
  body.home .homeprofile>img{
    width:100%;
    height:auto;
    aspect-ratio:1.12/1;
    object-fit:cover;
    object-position:center 18%;
    filter:grayscale(1) contrast(1.02);
  }
  body.home .homeprofile:after{
    content:"";
    position:absolute;
    inset:0;
    z-index:1;
    background:linear-gradient(180deg,transparent 26%,rgb(7 48 42 / 15%) 42%,rgb(7 48 42 / 91%) 69%,#073e36 100%);
    pointer-events:none;
  }
  body.home .homeprofile>div{
    position:absolute;
    inset:auto 0 0;
    z-index:2;
    width:100%;
    padding:22px;
    color:#fff;
  }
  body.home .homeprofile>div>span{font-size:9px}
  body.home .homeprofile h2{
    margin-top:5px;
    color:#fff;
    font:400 clamp(38px,12vw,54px)/.91 var(--serif);
    letter-spacing:-.035em;
  }
  body.home .homeprofile h2 span,
  body.home .homeprofile h2 em{display:inline}
  body.home .homeprofile h2 em{font-style:italic}
  body.home .homeprofile p{
    max-width:31rem;
    margin-top:10px;
    color:rgb(255 255 255 / 86%);
    font:400 13px/1.42 var(--sans);
  }
  body.home .homeprofile nav{margin-top:10px}
  body.home .homeprofile a{font-size:11px}
  body.home .homeintro{margin-bottom:10px}
  body.home .homeintro h1{font-size:40px}
  body.home .tiles{
    display:grid;
    grid-template-columns:1fr;
    gap:6px;
  }
  body.home .tile,
  body.home .tile-reporting,
  body.home .tile-opinion,
  body.home .tile-thoughts,
  body.home .tile-photos{
    grid-column:auto;
    min-height:164px;
    padding:34px 18px 17px;
  }
  body.home .tile strong{font-size:27px}
  body.home .tile small{max-width:78%;font-size:11.5px}
  body.home .tile>i{right:16px;left:auto;bottom:15px}
  body.home .homecontact{margin-top:8px}
}

@media(max-width:520px){
  body.home .homecontent{padding-inline:16px}
  body.home .homeprofile{margin-inline:-16px}
  body.home .homeprofile>div{padding:18px 17px}
  body.home .homeprofile p{font-size:12px}
  body.home .tile{min-height:154px}
  body.home .tile strong{font-size:25px}
}

body.home .desktophead:after{
  content:"";
  position:absolute;
  left:0;
  bottom:-1px;
  width:var(--page-progress,0%);
  height:2px;
  background:linear-gradient(90deg,#0b4b43,#b9563e,#b18c42);
  opacity:.82;
  pointer-events:none;
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
