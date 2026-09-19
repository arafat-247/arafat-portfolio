"""Apply the approved hybrid editorial homepage after final build processing."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
HOME = DIST / "index.html"
CSS = DIST / "portfolio.css"
CSS_MARKER = "/* Hybrid editorial homepage v18.4 */"
ASSET_VERSION_RE = re.compile(r"portfolio\.css\?v=[0-9.]+", re.I)
SCRIPT_VERSION_RE = re.compile(r"portfolio\.js\?v=[0-9.]+", re.I)
ASSET_VERSION = "18.4.1"

HOME_CSS = r"""
/* Hybrid editorial homepage v18.4 */
body.home main{background:#f7f3ea}
body.home .homecontent{position:relative}
body.home .herotagline{font-family:"Caveat",cursive}
body.home .heroquote{margin:0}
body.home .tile-reporting:after{background:linear-gradient(90deg,rgb(6 43 38 / 91%) 0%,rgb(6 43 38 / 56%) 58%,rgb(6 43 38 / 14%) 100%)}
body.home .tile-opinion:after{background:linear-gradient(90deg,rgb(126 52 33 / 90%) 0%,rgb(126 52 33 / 54%) 58%,rgb(126 52 33 / 14%) 100%)}
body.home .tile-thoughts:after{background:linear-gradient(90deg,rgb(43 54 32 / 90%) 0%,rgb(43 54 32 / 55%) 58%,rgb(43 54 32 / 14%) 100%)}
body.home .tile-photos:after{background:linear-gradient(90deg,rgb(11 37 35 / 90%) 0%,rgb(11 37 35 / 52%) 58%,rgb(11 37 35 / 12%) 100%)}

body.home .tileno{
  position:absolute;z-index:3;left:20px;top:16px;
  color:#efb56f;font:800 10px/1 var(--sans);letter-spacing:.13em
}
body.home .tileexplore{
  display:block;width:max-content;margin-top:14px;padding-bottom:3px;
  border-bottom:1px solid rgb(255 255 255 / 78%);
  color:#fff;font:700 11px/1.2 var(--sans);font-style:normal
}
body.home .tilewords{display:none}

@media(min-width:801px){
  body.home .homecontent{
    width:min(100% - 48px,1180px);
    margin:0 auto;
    padding:16px 0 26px;
  }

  /* Hero: paper field + framed portrait + editorial scene */
  body.home .homeprofile{
    position:relative;
    isolation:isolate;
    display:grid;
    grid-template-columns:repeat(12,minmax(0,1fr));
    min-height:430px;
    margin:0 0 18px;
    overflow:hidden;
    border:1px solid #e4ded1;
    background:
      radial-gradient(circle at 22% 22%,rgb(255 255 255 / 72%),transparent 36%),
      #f8f4eb;
    box-shadow:0 18px 48px rgb(20 35 30 / 7%);
  }
  body.home .homeprofile:before{
    content:"";
    position:absolute;
    inset:0;
    z-index:0;
    opacity:.28;
    pointer-events:none;
    background:
      linear-gradient(90deg,transparent 0 49%,rgb(20 65 57 / 7%) 49.2% 49.45%,transparent 49.7%),
      repeating-linear-gradient(0deg,transparent 0 28px,rgb(34 43 39 / 2.5%) 29px 30px);
  }

  body.home .herocopy{
    position:relative;
    z-index:5;
    grid-column:1/6;
    grid-row:1;
    align-self:center;
    padding:44px 10px 40px 42px;
  }
  body.home .herocopy>span{
    color:#0f5a50;
    font:800 10px/1.25 var(--sans);
    letter-spacing:.23em;
    text-transform:uppercase;
  }
  body.home .homeprofile h2{
    margin:14px 0 0;
    color:#073e36;
    font:400 clamp(60px,6.1vw,86px)/.84 var(--serif);
    letter-spacing:-.045em;
  }
  body.home .homeprofile h2 span,
  body.home .homeprofile h2 em{display:block}
  body.home .homeprofile h2 em{font-weight:400;font-style:italic}
  body.home .herocopy>p:not(.herotagline){
    max-width:430px;
    margin:20px 0 0;
    color:#242622;
    font:400 17px/1.42 var(--serif);
    text-wrap:pretty;
  }
  body.home .homeprofile .herotagline{
    margin:18px 0 0;
    color:#b87439;
    font:500 25px/1 "Caveat",cursive;
    transform:rotate(-1deg);
  }
  body.home .homeprofile nav{
    display:flex;
    flex-wrap:wrap;
    gap:12px;
    margin-top:22px;
  }
  body.home .homeprofile nav a{
    display:inline-flex;
    min-width:145px;
    min-height:47px;
    align-items:center;
    justify-content:center;
    padding:10px 18px;
    border:1px solid #315b54;
    color:#123e37;
    background:rgb(248 244 235 / 76%);
    font:400 14px/1 var(--serif);
    text-decoration:none;
    transition:transform .2s ease,background .2s ease,color .2s ease,box-shadow .2s ease;
  }
  body.home .homeprofile nav a.heroprimary{
    color:#fff;
    background:#0b4b43;
    border-color:#0b4b43;
  }
  body.home .homeprofile nav a:hover{
    transform:translateY(-2px);
    box-shadow:0 8px 18px rgb(11 75 67 / 10%);
  }
  body.home .heromicro{
    display:block;
    margin-top:24px;
    color:#85877f;
    font:italic 11px/1.4 var(--serif);
  }

  body.home .herolayers{
    position:absolute;
    inset:0;
    z-index:1;
    pointer-events:none;
  }
  body.home .heropaper{
    position:absolute;
    display:block;
    border:1px solid rgb(112 104 90 / 16%);
    background:#efe9dd;
    box-shadow:0 8px 22px rgb(62 50 35 / 9%);
  }
  body.home .heropaper-one{
    width:230px;
    height:330px;
    left:43%;
    top:54px;
    transform:rotate(-4deg);
    background:
      repeating-linear-gradient(0deg,transparent 0 11px,rgb(102 89 67 / 10%) 12px 13px),
      #efe9dd;
  }
  body.home .heropaper-two{
    width:128px;
    min-height:225px;
    left:68%;
    top:104px;
    padding:90px 13px 16px;
    transform:rotate(3deg);
    color:#6e675c;
    background:#f3ede1;
    font:700 10px/1.6 var(--sans);
    letter-spacing:.13em;
    text-transform:uppercase;
  }
  body.home .heropaper-two:before{
    content:"The Daily Star";
    position:absolute;
    top:18px;
    left:13px;
    color:#3c3b36;
    font:400 14px/1 var(--serif);
    letter-spacing:0;
    text-transform:none;
  }

  body.home .heroportrait{
    position:relative;
    z-index:4;
    grid-column:5/10;
    grid-row:1;
    align-self:center;
    justify-self:center;
    width:min(100%,430px);
    margin:0;
    padding:13px;
    transform:translate3d(var(--hero-x,0),var(--hero-y,0),0) rotate(-1.8deg);
    background:#faf7f0;
    box-shadow:0 18px 42px rgb(22 35 31 / 18%);
    transition:transform .45s cubic-bezier(.2,.65,.25,1),box-shadow .3s ease;
  }
  body.home .homeprofile:hover .heroportrait{
    box-shadow:0 23px 50px rgb(22 35 31 / 22%);
  }
  body.home .heroportrait img{
    display:block;
    width:100%;
    aspect-ratio:1/1.02;
    object-fit:cover;
    object-position:center 26%;
    filter:grayscale(1) contrast(1.02);
  }
  body.home .heroportrait figcaption{
    position:absolute;
    left:34px;
    bottom:28px;
    max-width:135px;
    color:#f7f2e8;
    font:500 19px/.95 "Caveat",cursive;
    transform:rotate(-4deg);
    text-shadow:0 1px 4px rgb(0 0 0 / 35%);
  }

  body.home .heroscene{
    position:relative;
    z-index:2;
    grid-column:8/13;
    grid-row:1;
    min-height:430px;
    overflow:hidden;
    background:#0b4b43;
  }
  body.home .heroscene:after{
    content:"";
    position:absolute;
    inset:0;
    background:
      linear-gradient(90deg,#0b4b43 0%,rgb(11 75 67 / 78%) 26%,rgb(11 75 67 / 15%) 66%,rgb(11 75 67 / 36%) 100%),
      linear-gradient(0deg,rgb(4 40 35 / 42%),transparent 55%);
  }
  body.home .heroscene>img{
    position:absolute;
    inset:0;
    width:100%;
    height:100%;
    object-fit:cover;
    object-position:center;
    filter:saturate(.72) contrast(.96) brightness(.82);
    transform:scale(1.04);
    transition:transform .8s cubic-bezier(.2,.65,.25,1),filter .35s ease;
  }
  body.home .homeprofile:hover .heroscene>img{transform:scale(1.075);filter:saturate(.82) contrast(1) brightness(.86)}
  body.home .heroquote{
    position:absolute;
    z-index:3;
    top:72px;
    right:34px;
    width:146px;
    padding-top:14px;
    border-top:2px solid rgb(243 241 231 / 78%);
    color:#f8f4ea;
    font:italic 21px/1.1 var(--serif);
  }
  body.home .herolocation{
    position:absolute;
    z-index:3;
    right:34px;
    bottom:30px;
    color:#fff;
    font:800 9px/1.55 var(--sans);
    letter-spacing:.2em;
    text-transform:uppercase;
  }

  /* Work header */
  body.home .homeintro{
    display:grid;
    grid-template-columns:minmax(280px,.8fr) minmax(0,1.2fr);
    align-items:end;
    gap:34px;
    margin:0 0 8px;
    padding:0;
  }
  body.home .homeintro>div>span{
    display:block;
    margin-bottom:2px;
    color:#b8563f;
    font:800 10px/1.2 var(--sans);
    letter-spacing:.2em;
    text-transform:uppercase;
  }
  body.home .homeintro h1{
    margin:0;
    color:#12130f;
    font:400 clamp(44px,4vw,55px)/.92 var(--serif);
    letter-spacing:-.035em;
  }
  body.home .homeintrocopy{
    display:flex;
    align-items:flex-end;
    justify-content:flex-end;
    gap:24px;
    padding-bottom:5px;
  }
  body.home .homeintrocopy p{
    margin:0;
    color:#30322d;
    font:400 14px/1.4 var(--serif);
    text-align:right;
  }
  body.home .homeintrocopy a{
    flex:0 0 auto;
    padding-bottom:3px;
    border-bottom:1px solid #315b54;
    color:#12473f;
    font:400 12px/1.2 var(--serif);
    text-decoration:none;
  }

  /* Work grid: large reporting + opinion top right + two lower cards */
  body.home .tiles{
    display:grid;
    grid-template-columns:1.08fr .56fr .82fr;
    grid-template-areas:
      "reporting opinion opinion"
      "reporting thoughts photos";
    gap:5px;
  }
  body.home .tile{
    position:relative;
    min-height:180px;
    overflow:hidden;
    padding:42px 20px 18px;
    transform:translateZ(0);
    box-shadow:none;
    transition:transform .24s cubic-bezier(.2,.7,.25,1),box-shadow .24s ease;
  }
  body.home .tile-reporting{grid-area:reporting;min-height:376px}
  body.home .tile-opinion{grid-area:opinion;min-height:188px}
  body.home .tile-thoughts{grid-area:thoughts;min-height:183px}
  body.home .tile-photos{grid-area:photos;min-height:183px}
  body.home .tile:before{
    content:"";
    position:absolute;
    inset:0;
    z-index:1;
    pointer-events:none;
    background:radial-gradient(circle at var(--mx,50%) var(--my,50%),rgb(255 255 255 / 14%),transparent 34%);
    opacity:0;
    transition:opacity .2s ease;
  }
  body.home .tile:hover:before{opacity:1}
  body.home .tile:hover{
    z-index:4;
    transform:translateY(-3px);
    box-shadow:0 16px 32px rgb(10 35 30 / 16%);
  }
  body.home .tile img{
    position:absolute;
    inset:-5px;
    width:calc(100% + 10px);
    height:calc(100% + 10px);
    object-fit:cover;
    filter:saturate(.72) contrast(.98) brightness(.85);
    transform:translate3d(var(--ix,0),var(--iy,0),0) scale(1.035);
    transition:transform .6s cubic-bezier(.2,.65,.25,1),filter .3s ease;
  }
  body.home .tile:hover img{
    transform:translate3d(var(--ix,0),var(--iy,0),0) scale(1.07);
    filter:saturate(.9) contrast(1) brightness(.9);
  }
  body.home .tile .tilecopy{
    position:relative;
    z-index:3;
    display:block;
    width:min(70%,370px);
  }
  body.home .tile strong{
    display:block;
    font:400 clamp(27px,2.7vw,39px)/.97 var(--serif);
    letter-spacing:-.025em;
  }
  body.home .tile-reporting strong{font-size:clamp(36px,3.6vw,50px)}
  body.home .tile small{
    display:block;
    max-width:315px;
    margin-top:8px;
    color:rgb(255 255 255 / 88%);
    font:400 12px/1.33 var(--serif);
  }
  body.home .tile-reporting small{font-size:14px;max-width:335px}
  body.home .tilewords{
    position:absolute;
    right:18px;
    bottom:18px;
    z-index:3;
    display:block;
    width:96px;
    padding-top:11px;
    border-top:1px solid rgb(255 255 255 / 58%);
    color:rgb(255 255 255 / 88%);
    font:700 9px/1.45 var(--sans);
    letter-spacing:.05em;
    transition:transform .2s ease,opacity .2s ease;
  }
  body.home .tile:hover .tilewords{transform:translateX(-4px)}
  body.home .tile>i{
    position:absolute;
    z-index:3;
    left:120px;
    bottom:15px;
    display:grid;
    width:34px;
    height:34px;
    place-items:center;
    border:1px solid rgb(255 255 255 / 72%);
    border-radius:50%;
    font-style:normal;
    transition:transform .2s ease,background .2s ease;
  }
  body.home .tile:hover>i{transform:translateX(3px);background:rgb(255 255 255 / 10%)}
  body.home .tile-reporting>i{left:128px}

  body.home .homecontact{
    grid-template-columns:minmax(0,1fr) auto;
    min-height:62px;
    gap:24px;
    margin:10px 0 12px;
    padding:14px 24px;
    background:#b9533d;
  }
  body.home .homecontact strong{font:400 25px/1 var(--serif)}
  body.home .homecontact a{
    padding-bottom:3px;
    border-bottom:1px solid currentColor;
    font:400 13px/1.2 var(--serif);
  }

  body.home.home-motion .homeprofile,
  body.home.home-motion .homeintro,
  body.home.home-motion .tile,
  body.home.home-motion .homecontact{opacity:0;transform:translateY(10px)}
  body.home.home-motion .homeprofile.is-visible,
  body.home.home-motion .homeintro.is-visible,
  body.home.home-motion .tile.is-visible,
  body.home.home-motion .homecontact.is-visible{
    opacity:1;
    transform:none;
    transition:opacity .5s ease,transform .5s cubic-bezier(.2,.7,.25,1),box-shadow .24s ease;
  }
  body.home.home-motion .tile.is-visible:hover{transform:translateY(-3px)}
}

@media(min-width:801px) and (max-width:1080px){
  body.home .homecontent{width:min(100% - 36px,980px)}
  body.home .homeprofile{min-height:390px}
  body.home .herocopy{grid-column:1/6;padding-left:28px}
  body.home .homeprofile h2{font-size:clamp(52px,6vw,67px)}
  body.home .heroportrait{grid-column:5/10;width:min(100%,370px)}
  body.home .heroscene{grid-column:8/13;min-height:390px}
  body.home .heroquote{right:22px;font-size:18px;width:122px}
  body.home .homeprofile nav a{min-width:120px}
  body.home .tiles{
    grid-template-columns:1fr 1fr;
    grid-template-areas:
      "reporting opinion"
      "thoughts photos";
  }
  body.home .tile-reporting,
  body.home .tile-opinion,
  body.home .tile-thoughts,
  body.home .tile-photos{min-height:190px}
  body.home .tile-reporting strong{font-size:35px}
  body.home .tile-reporting small{font-size:12px}
  body.home .tilewords{display:none}
}

@media(max-width:800px){
  body.home .homecontent{padding:12px 16px 18px}
  body.home .homeprofile{
    display:grid;
    grid-template-columns:1fr;
    margin:0 -16px 24px;
    overflow:hidden;
    border:0;
    background:#f8f4eb;
  }
  body.home .herocopy{
    order:1;
    padding:27px 20px 24px;
  }
  body.home .herocopy>span{
    color:#0b554c;
    font-size:9px;
    font-weight:800;
    letter-spacing:.18em;
    text-transform:uppercase;
  }
  body.home .homeprofile h2{
    margin:8px 0 0;
    color:#073e36;
    font:400 clamp(44px,13vw,62px)/.9 var(--serif);
    letter-spacing:-.04em;
  }
  body.home .homeprofile h2 span,
  body.home .homeprofile h2 em{display:inline}
  body.home .homeprofile h2 em{font-style:italic}
  body.home .herocopy>p:not(.herotagline){
    margin:13px 0 0;
    color:#33352f;
    font:400 15px/1.45 var(--serif);
  }
  body.home .homeprofile .herotagline{
    margin:13px 0 0;
    color:#b87439;
    font:500 22px/1 "Caveat",cursive;
  }
  body.home .homeprofile nav{display:flex;gap:9px;margin-top:17px}
  body.home .homeprofile nav a{
    min-width:0;
    padding:10px 14px;
    border:1px solid #315b54;
    color:#16463f;
    background:#f8f4eb;
    font:400 12px/1 var(--serif);
    text-decoration:none;
  }
  body.home .homeprofile nav a.heroprimary{color:#fff;background:#0b4b43}
  body.home .heromicro{display:none}
  body.home .herolayers{display:none}
  body.home .heroportrait{
    order:2;
    position:relative;
    z-index:2;
    width:calc(100% - 34px);
    margin:0 auto 18px;
    padding:10px;
    background:#faf7f0;
    box-shadow:0 14px 30px rgb(20 35 31 / 15%);
    transform:rotate(-1deg);
  }
  body.home .heroportrait img{
    width:100%;
    aspect-ratio:1/1;
    object-fit:cover;
    object-position:center 24%;
    filter:grayscale(1);
  }
  body.home .heroportrait figcaption{
    position:absolute;
    left:28px;
    bottom:24px;
    color:#fff;
    font:500 18px/.95 "Caveat",cursive;
    transform:rotate(-4deg);
  }
  body.home .heroscene{
    order:3;
    position:relative;
    min-height:180px;
    overflow:hidden;
    background:#0b4b43;
  }
  body.home .heroscene>img{
    position:absolute;
    inset:0;
    width:100%;
    height:100%;
    object-fit:cover;
    filter:saturate(.7) brightness(.72);
  }
  body.home .heroscene:after{
    content:"";
    position:absolute;
    inset:0;
    background:linear-gradient(90deg,rgb(8 61 54 / 74%),rgb(8 61 54 / 24%));
  }
  body.home .heroquote{
    position:absolute;
    z-index:2;
    top:28px;
    right:22px;
    width:142px;
    padding-top:10px;
    border-top:1px solid rgb(255 255 255 / 72%);
    color:#fff;
    font:italic 18px/1.12 var(--serif);
  }
  body.home .herolocation{
    position:absolute;
    z-index:2;
    right:22px;
    bottom:19px;
    color:#fff;
    font:800 8px/1.45 var(--sans);
    letter-spacing:.17em;
    text-transform:uppercase;
  }

  body.home .homeintro{display:grid;grid-template-columns:1fr;gap:8px;margin-bottom:10px}
  body.home .homeintro>div>span{color:#b8563f;font-size:9px;font-weight:800;letter-spacing:.15em;text-transform:uppercase}
  body.home .homeintro h1{margin:2px 0 0;font:400 41px/.95 var(--serif)}
  body.home .homeintrocopy{display:block}
  body.home .homeintrocopy p{margin:0;color:#595b54;font:400 13px/1.4 var(--serif);text-align:left}
  body.home .homeintrocopy a{display:inline-block;margin-top:6px;color:#16483f;font:400 12px/1.2 var(--serif)}

  body.home .tiles{display:grid;grid-template-columns:1fr;gap:6px}
  body.home .tile,
  body.home .tile-reporting,
  body.home .tile-opinion,
  body.home .tile-thoughts,
  body.home .tile-photos{
    grid-area:auto;
    min-height:165px;
    padding:36px 18px 17px;
  }
  body.home .tile img{filter:brightness(.74) saturate(.72)}
  body.home .tile .tilecopy{width:72%}
  body.home .tile strong{font-size:28px}
  body.home .tile small{font-size:11.5px}
  body.home .tilewords{display:none}
  body.home .tileexplore{display:none}
  body.home .tile>i{right:16px;left:auto;bottom:15px}
  body.home .tileno{left:16px;top:14px;font-size:9px}
  body.home .homecontact{margin-top:8px}
}

@media(max-width:470px){
  body.home .homeprofile h2{font-size:44px}
  body.home .homeprofile nav{flex-wrap:wrap}
  body.home .homeprofile nav a{flex:1}
  body.home .heroscene{min-height:155px}
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


/* Hero composition lock: matches the approved framed-reference proportions. */
@media(min-width:801px){
  body.home .homeprofile{
    position:relative;
    display:block;
    height:clamp(430px,40vw,500px);
    min-height:0;
    overflow:hidden;
  }
  body.home .herocopy{
    position:absolute;
    z-index:5;
    left:36px;
    top:50%;
    width:38%;
    padding:0;
    transform:translateY(-50%);
  }
  body.home .herocopy>span{font-size:10px}
  body.home .homeprofile h2{
    margin-top:13px;
    font-size:clamp(58px,6vw,82px);
    line-height:.86;
  }
  body.home .herocopy>p:not(.herotagline){
    max-width:405px;
    margin-top:18px;
    font-size:16px;
    line-height:1.43;
  }
  body.home .homeprofile .herotagline{
    margin-top:16px;
    font-size:24px;
  }
  body.home .homeprofile nav{margin-top:20px}
  body.home .homeprofile nav a{
    min-width:138px;
    min-height:45px;
    padding:9px 17px;
  }
  body.home .heromicro{margin-top:21px}

  body.home .herolayers{
    position:absolute;
    inset:0;
    z-index:1;
    display:block;
    pointer-events:none;
  }
  body.home .heropaper-one{
    left:50%;
    top:12%;
    width:180px;
    height:315px;
    transform:rotate(-4deg);
  }
  body.home .heropaper-two{
    left:67%;
    top:20%;
    width:112px;
    min-height:220px;
    transform:rotate(3deg);
  }

  body.home .heroscene{
    position:absolute;
    z-index:2;
    top:0;
    right:0;
    width:34%;
    height:100%;
    min-height:0;
  }
  body.home .heroscene>img{
    width:100%;
    height:100%;
    object-fit:cover;
    object-position:center;
  }
  body.home .heroquote{
    top:58px;
    right:28px;
    width:140px;
    font-size:20px;
  }
  body.home .herolocation{
    right:28px;
    bottom:26px;
  }

  body.home .heroportrait{
    position:absolute;
    z-index:4;
    left:57.5%;
    top:50%;
    width:min(35%,410px);
    max-width:410px;
    margin:0;
    padding:12px;
    transform:translate(-50%,-50%) rotate(-1.6deg);
  }
  body.home .homeprofile:hover .heroportrait{
    transform:translate(calc(-50% + var(--hero-x,0)),calc(-50% + var(--hero-y,0))) rotate(-1.6deg);
  }
  body.home .heroportrait img{
    display:block;
    width:100%;
    height:auto;
    max-height:none;
    aspect-ratio:auto;
    object-fit:contain;
    object-position:center;
  }
  body.home .heroportrait figcaption{
    left:30px;
    bottom:28px;
    max-width:132px;
  }
}

@media(min-width:801px) and (max-width:1080px){
  body.home .homeprofile{height:430px}
  body.home .herocopy{left:28px;width:40%}
  body.home .homeprofile h2{font-size:clamp(52px,6.2vw,67px)}
  body.home .herocopy>p:not(.herotagline){font-size:14px}
  body.home .homeprofile .herotagline{font-size:21px}
  body.home .homeprofile nav a{min-width:116px}
  body.home .heroportrait{left:58%;width:min(35%,350px)}
  body.home .heroscene{width:33%}
  body.home .heroquote{right:20px;width:118px;font-size:17px}
  body.home .heropaper-one{left:49%;width:150px;height:285px}
  body.home .heropaper-two{left:67%;width:96px}
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
    print(f"Homepage polish: hybrid_hero=1, asymmetric_work=1, responsive=1, asset_version={ASSET_VERSION}")


if __name__ == "__main__":
    main()
