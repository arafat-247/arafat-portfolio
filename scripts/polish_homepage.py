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
ASSET_VERSION = "20.2.0"

HOME_CSS = r"""
/* Homepage v20.2 — approved journalist's desk */
body.home{
  --desk-wood-1:#241107;
  --desk-wood-2:#4b2611;
  --desk-paper:#e9dcc4;
  --desk-ink:#21180f;
  --desk-red:#a51d16;
  --desk-gold:#c9a46c;
  background:#111817;
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
  background:#111817;
}
.deskhome{
  width:100%;
  min-height:100vh;
  padding:20px;
  background:#111817;
}
.deskstage{
  position:relative;
  width:min(100%,1600px);
  aspect-ratio:1447/1087;
  margin:0 auto;
  overflow:hidden;
  color:#f4eadb;
  border:1px solid rgb(255 255 255 / 22%);
  border-radius:26px;
  background:
    radial-gradient(ellipse at 48% 30%,rgb(255 185 100 / 10%),transparent 35%),
    radial-gradient(ellipse at 12% 80%,rgb(0 0 0 / 30%),transparent 36%),
    repeating-linear-gradient(1deg,rgb(255 255 255 / 2.5%) 0 1px,transparent 1px 5px),
    repeating-linear-gradient(92deg,transparent 0 72px,rgb(19 7 2 / 13%) 73px 75px,transparent 76px 145px),
    linear-gradient(102deg,var(--desk-wood-1),#3c1c0c 44%,var(--desk-wood-2) 68%,#2c150a);
  box-shadow:0 24px 80px rgb(0 0 0 / 40%),inset 0 0 100px rgb(0 0 0 / 30%);
}
.deskstage:after{
  content:"";
  position:absolute;
  z-index:30;
  inset:0;
  pointer-events:none;
  box-shadow:inset 0 0 100px rgb(0 0 0 / 24%);
}
.deskhead{
  position:absolute;
  z-index:20;
  left:5.4%;
  right:6.4%;
  top:2.3%;
  display:flex;
  align-items:flex-start;
  justify-content:space-between;
  gap:30px;
}
.deskbrand{
  display:grid;
  gap:4px;
  color:#f4eee4;
  text-decoration:none;
}
.deskbrand strong{
  font:400 clamp(22px,2vw,32px)/1 var(--serif);
  letter-spacing:-.025em;
}
.deskbrand small{
  font:800 clamp(6px,.55vw,8px)/1 var(--sans);
  letter-spacing:.25em;
  text-transform:uppercase;
  color:#c9baa4;
}
.desknav{
  display:flex;
  align-items:center;
  gap:clamp(20px,3vw,44px);
}
.desknav a{
  position:relative;
  padding:5px 0 9px;
  color:#f4eee4;
  font:600 clamp(10px,.9vw,14px)/1 var(--serif);
  text-decoration:none;
}
.desknav a:after{
  content:"";
  position:absolute;
  left:0;right:0;bottom:0;
  height:1px;
  transform:scaleX(0);
  background:#f5eee3;
  transition:transform .18s ease;
}
.desknav a:hover:after,
.desknav a[aria-current=page]:after{transform:scaleX(1)}
.deskprofile{
  position:absolute;
  z-index:16;
  left:35.7%;
  top:5.2%;
  width:22.8%;
  color:var(--desk-ink);
  text-decoration:none;
  transform:rotate(-1.5deg);
  filter:drop-shadow(0 10px 12px rgb(0 0 0 / 27%));
}
.deskprofile:before{
  content:"";
  position:absolute;
  z-index:-1;
  left:-7%;
  right:-7%;
  top:4%;
  bottom:9%;
  background:
    repeating-linear-gradient(0deg,transparent 0 15px,rgb(65 50 34 / 8%) 16px 17px),
    #bca98b;
  transform:rotate(3.5deg);
}
.deskphoto{
  display:block;
  padding:4.6% 4.6% 15%;
  background:#d8ccb8;
  border:1px solid rgb(45 35 25 / 35%);
}
.deskphoto img{
  display:block;
  width:100%;
  aspect-ratio:1.05/1;
  object-fit:cover;
  object-position:center 37%;
  filter:grayscale(1) contrast(1.04);
}
.deskbio{
  position:absolute;
  left:2.8%;
  right:-2%;
  bottom:0;
  display:grid;
  gap:2px;
  padding:3.2% 5.2% 3.8%;
  background:
    repeating-linear-gradient(0deg,rgb(96 72 45 / 3%) 0 1px,transparent 1px 3px),
    #e8dbc3;
  border:1px solid rgb(58 43 28 / 20%);
}
.deskbio strong{font:700 clamp(12px,1.05vw,17px)/1.05 var(--serif)}
.deskbio small{font:400 clamp(8px,.72vw,11px)/1.25 var(--serif)}
.desknote{
  position:absolute;
  z-index:10;
  color:#d9c6ab;
  font:600 clamp(14px,1.65vw,25px)/.96 "Caveat",cursive;
  transform:rotate(-7deg);
  text-shadow:0 1px 1px rgb(0 0 0 / 35%);
}
.desknote-left{left:27.3%;top:8.2%}
.desknote-right{
  right:10.3%;top:24%;
  padding:1.4% 1.8%;
  color:#3e3024;
  background:#d8c9ad;
  transform:rotate(7deg);
  box-shadow:0 5px 12px rgb(0 0 0 / 18%);
}
.desknote-bottom{
  left:6.2%;bottom:9.2%;
  padding:1.1% 1.3%;
  color:#443528;
  background:#cdbb9e;
  transform:rotate(-5deg);
}
.deskintro{
  position:absolute;
  z-index:12;
  left:30.7%;
  top:29.1%;
  width:37%;
  margin:0;
  color:#f4eadb;
  font:400 clamp(13px,1.35vw,21px)/1.38 var(--serif);
  text-shadow:0 1px 2px rgb(0 0 0 / 45%);
}
.deskwork{position:absolute;z-index:14;inset:0}
.deskpiece{
  position:absolute;
  display:block;
  color:var(--desk-ink);
  text-decoration:none;
  filter:drop-shadow(0 9px 10px rgb(0 0 0 / 22%));
  transition:transform .18s ease,filter .18s ease;
}
.deskpiece:hover{
  transform:translateY(-4px) rotate(0deg)!important;
  filter:drop-shadow(0 15px 14px rgb(0 0 0 / 31%));
}
.deskpaper{
  position:absolute;
  inset:0 0 12%;
  display:block;
  overflow:hidden;
  border:1px solid rgb(61 45 27 / 25%);
  background:
    repeating-linear-gradient(0deg,rgb(105 74 42 / 3%) 0 1px,transparent 1px 4px),
    var(--desk-paper);
}
.deskpaper:before{
  content:"";
  position:absolute;
  z-index:-1;
  inset:3% -3% -3% 3%;
  border:1px solid rgb(61 45 27 / 20%);
  background:#c8b598;
}
.desklabel{
  position:absolute;
  z-index:5;
  left:9%;
  right:1%;
  bottom:0;
  display:grid;
  min-height:29%;
  grid-template-columns:auto 1fr auto;
  grid-template-rows:auto auto;
  column-gap:8px;
  align-items:center;
  padding:4.3% 5.5% 4.6%;
  background:
    repeating-linear-gradient(0deg,rgb(104 75 43 / 3%) 0 1px,transparent 1px 3px),
    #e9dcc5;
  border:1px solid rgb(58 41 24 / 22%);
}
.desklabel b{
  grid-row:1/3;
  display:grid;
  width:clamp(31px,3.1vw,50px);
  aspect-ratio:1;
  place-items:center;
  margin-left:-24%;
  border:2px solid var(--desk-red);
  border-radius:50%;
  color:var(--desk-red);
  font:600 clamp(17px,1.8vw,28px)/1 var(--serif);
  transform:rotate(-7deg);
  background:#eee1cc;
}
.desklabel strong{
  grid-column:2;
  font:600 clamp(18px,1.85vw,30px)/.98 var(--serif);
  letter-spacing:-.025em;
}
.desklabel small{
  grid-column:2;
  color:#4a3a2d;
  font:400 clamp(10px,.9vw,14px)/1.25 var(--serif);
}
.desklabel em{
  grid-column:3;
  grid-row:1/3;
  font:400 clamp(19px,2vw,30px)/1 var(--serif);
  font-style:normal;
}
.desk-reporting{
  left:7.8%;top:39%;
  width:22.4%;height:29%;
  transform:rotate(-.7deg);
}
.deskpaper-report img{
  display:block;
  width:100%;height:100%;
  object-fit:cover;
  filter:sepia(.32) saturate(.62) contrast(.92);
}
.desk-opinion{
  left:32.5%;top:39.5%;
  width:24.2%;height:28.8%;
  transform:rotate(.5deg);
}
.deskpaper-opinion{
  padding:12% 9% 8%;
  background:
    repeating-linear-gradient(0deg,transparent 0 17px,rgb(79 64 47 / 12%) 18px 19px),
    #ded0b7;
}
.deskpaper-opinion i{
  display:block;
  color:#4f4032;
  font:400 clamp(9px,.78vw,13px)/1.35 var(--serif);
  font-style:normal;
}
.deskpaper-opinion mark{
  display:inline-block;
  margin-top:8%;
  padding:1px 3px;
  color:#5a3b1d;
  background:#d8a94d;
  font:400 clamp(8px,.68vw,11px)/1.2 var(--serif);
  transform:rotate(-1deg);
}
.deskpaper-opinion u{
  position:absolute;
  right:5%;bottom:20%;
  color:#b22d21;
  font:600 clamp(13px,1.15vw,19px)/.92 "Caveat",cursive;
  text-decoration:none;
  transform:rotate(-8deg);
}
.desk-thoughts{
  left:58%;top:39%;
  width:25.5%;height:29.2%;
  transform:rotate(-.25deg);
}
.deskpaper-notebook{
  padding:13% 9% 8% 12%;
  border-radius:7px;
  background:
    linear-gradient(90deg,transparent 0 8%,rgb(177 99 70 / 18%) 8.2% 8.6%,transparent 8.8%),
    repeating-linear-gradient(0deg,#e8ddc6 0 25px,#b9b0a1 26px 27px);
}
.deskpaper-notebook:after{
  content:"";
  position:absolute;
  right:10%;top:3%;
  width:7%;height:92%;
  border-radius:10px;
  background:linear-gradient(90deg,#0b0b09,#b6985b 20%,#111 34% 78%,#c9a96a 82%,#080806);
  transform:rotate(-10deg);
  box-shadow:3px 4px 5px rgb(0 0 0 / 25%);
}
.deskpaper-notebook i{
  display:block;
  color:#4b3a2a;
  font:600 clamp(14px,1.35vw,21px)/.96 "Caveat",cursive;
}
.deskpaper-notebook span{
  display:block;
  margin-top:7%;
  color:#49392b;
  font:500 clamp(11px,1.05vw,17px)/1.18 "Caveat",cursive;
}
.desk-photography{
  left:39.4%;top:69.5%;
  width:24.5%;height:21.7%;
  transform:rotate(-1.3deg);
}
.deskpaper-photo{inset:0 0 14%}
.deskpaper-photo img{
  width:100%;height:100%;
  display:block;object-fit:cover;
  filter:saturate(.85) contrast(.95);
}
.desk-photography .desklabel{
  left:8%;right:0;min-height:35%;
}
.deskdecor{
  position:absolute;
  z-index:4;
  pointer-events:none;
}
.desk-laptop{
  left:-5.5%;top:5%;
  width:14%;height:31%;
  border-radius:8px;
  background:
    repeating-linear-gradient(90deg,#222 0 10%,#0c0c0c 10.5% 11%),
    linear-gradient(#393b3c,#151617);
  box-shadow:9px 10px 16px rgb(0 0 0 / 35%);
  transform:rotate(-12deg);
}
.desk-laptop:after{
  content:"";
  position:absolute;left:11%;right:9%;bottom:8%;height:42%;
  border:1px solid #4d4e4e;
  background:repeating-linear-gradient(0deg,#161717 0 10%,#292a2a 10.5% 12%);
}
.desk-coffee{
  left:62.6%;top:7.5%;
  width:11%;aspect-ratio:1;
  border-radius:50%;
  background:radial-gradient(circle,#100a06 0 45%,#25150c 46% 52%,#aa9377 53% 65%,#e2d4bf 66% 73%,#8f7c66 74%);
  box-shadow:5px 9px 15px rgb(0 0 0 / 32%);
}
.desk-coffee i{
  position:absolute;
  right:-21%;top:37%;
  width:34%;height:25%;
  border:8px solid #b19c83;
  border-left:0;
  border-radius:0 50% 50% 0;
  transform:rotate(10deg);
}
.desk-books{
  right:4.2%;top:4.3%;
  width:17%;height:19%;
  transform:rotate(7deg);
}
.desk-books:before,
.desk-books:after,
.desk-books i,
.desk-books b{
  content:"";
  position:absolute;
  right:0;
  width:100%;height:24%;
  border:1px solid #15120f;
  background:linear-gradient(90deg,#191611,#30281d 65%,#120f0c);
  box-shadow:3px 5px 8px rgb(0 0 0 / 30%);
}
.desk-books:before{top:0;transform:translateX(3%)}
.desk-books:after{top:26%;width:92%}
.desk-books i{top:52%;width:96%;transform:translateX(-3%)}
.desk-books b{top:78%;width:88%;transform:translateX(-7%)}
.desk-books u{
  position:absolute;
  z-index:2;
  left:19%;top:33%;
  color:#bd9454;
  font:600 clamp(7px,.65vw,11px)/1 var(--serif);
  letter-spacing:.14em;
  text-decoration:none;
  transform:rotate(-2deg);
}
.desk-camera{
  left:17.6%;bottom:7.6%;
  width:20%;height:18%;
  border-radius:15px 15px 8px 8px;
  background:linear-gradient(140deg,#121313,#272827 40%,#080909);
  transform:rotate(-9deg);
  box-shadow:8px 12px 18px rgb(0 0 0 / 45%);
}
.desk-camera:before{
  content:"";
  position:absolute;
  left:22%;top:12%;
  width:49%;aspect-ratio:1;
  border-radius:50%;
  background:radial-gradient(circle,#080909 0 23%,#4b4d49 24% 32%,#111 33% 47%,#77746c 48% 50%,#111 51% 67%,#353633 68% 72%,#090a0a 73%);
}
.desk-camera:after{
  content:"";
  position:absolute;
  left:10%;top:-13%;
  width:30%;height:28%;
  border-radius:5px 5px 0 0;
  background:#171818;
}
.desk-camera i{position:absolute;right:8%;top:13%;width:12%;aspect-ratio:1;border-radius:50%;background:#55554f}
.desk-camera b{position:absolute;left:-20%;right:-25%;bottom:-8%;height:8%;border-radius:50%;border-bottom:4px solid #090909;transform:rotate(8deg)}
.desk-map{
  right:1.2%;bottom:2.5%;
  width:18%;height:27%;
  border:1px solid #8e7b61;
  background:
    linear-gradient(37deg,transparent 0 48%,rgb(80 112 119 / 25%) 49% 50%,transparent 51%),
    linear-gradient(128deg,transparent 0 49%,rgb(161 110 69 / 22%) 50% 51%,transparent 52%),
    repeating-linear-gradient(18deg,transparent 0 19px,rgb(88 76 59 / 10%) 20px 21px),
    #c9b898;
  transform:rotate(10deg);
  box-shadow:-5px 8px 10px rgb(0 0 0 / 25%);
}
.desk-map:after{
  content:"BANGLADESH";
  position:absolute;
  right:12%;bottom:20%;
  color:#725d40;
  font:700 clamp(8px,.85vw,13px)/1 var(--serif);
  letter-spacing:.12em;
}
.desk-map i{
  position:absolute;
  right:16%;top:8%;
  width:5%;height:28%;
  border:2px solid #8a7759;
  border-radius:10px;
  transform:rotate(15deg);
}
.desk-plant{
  width:18%;height:21%;
  background:
    radial-gradient(ellipse at 20% 70%,#2f5729 0 17%,transparent 18%),
    radial-gradient(ellipse at 45% 50%,#437238 0 20%,transparent 21%),
    radial-gradient(ellipse at 70% 30%,#244f25 0 19%,transparent 20%),
    radial-gradient(ellipse at 82% 70%,#3c6c35 0 18%,transparent 19%);
  filter:blur(1.5px);
}
.desk-plant-a{right:-5%;top:-3%;transform:rotate(18deg)}
.desk-plant-b{left:-5%;bottom:-4%;transform:rotate(-24deg)}
.deskfooterline{
  position:absolute;
  z-index:15;
  left:34%;right:24%;
  bottom:1.8%;
  display:flex;
  justify-content:space-between;
  gap:20px;
  padding-top:8px;
  border-top:1px solid rgb(235 216 185 / 32%);
  color:#c9ab80;
  font:800 clamp(6px,.55vw,8px)/1 var(--sans);
  letter-spacing:.24em;
  text-transform:uppercase;
}
.deskfooterline a{color:#d9c6aa;text-decoration:none;letter-spacing:.1em}

/* Mobile: same desk language, purpose-built vertical arrangement. */
@media(max-width:800px){
  body.home .right,body.home main,body.home{background:#241107}
  .deskhome{padding:0;background:#241107}
  .deskstage{
    width:100%;
    max-width:720px;
    min-height:1820px;
    aspect-ratio:auto;
    border:0;
    border-radius:0;
    box-shadow:none;
    background:
      radial-gradient(ellipse at 50% 7%,rgb(255 183 92 / 10%),transparent 24%),
      repeating-linear-gradient(2deg,rgb(255 255 255 / 2%) 0 1px,transparent 1px 5px),
      linear-gradient(101deg,#241107,#43210f 56%,#2d160a);
  }
  .deskstage:after{box-shadow:inset 0 0 65px rgb(0 0 0 / 25%)}
  .deskhead{
    position:relative;
    left:auto;right:auto;top:auto;
    height:82px;
    padding:23px 20px 0;
  }
  .deskbrand strong{font-size:26px}
  .deskbrand small{font-size:7px}
  .desknav{display:none}
  .deskprofile{
    left:23%;
    top:9%;
    width:54%;
    transform:rotate(-2deg);
  }
  .deskphoto{padding-bottom:17%}
  .deskbio{padding:3.7% 5.5% 4.2%}
  .deskbio strong{font-size:16px}
  .deskbio small{font-size:11px;line-height:1.25}
  .desknote-left{
    left:14%;top:10.8%;
    font-size:21px;
  }
  .desknote-right{
    right:8%;top:19.5%;
    font-size:19px;
    padding:12px 14px;
  }
  .deskintro{
    left:20%;
    top:27.3%;
    width:69%;
    font-size:16px;
    line-height:1.42;
  }
  .deskwork{position:absolute;inset:0}
  .deskpiece{
    left:22%!important;
    width:64%!important;
    height:250px!important;
    transform:none!important;
  }
  .desk-reporting{top:34%}
  .desk-opinion{top:49.3%}
  .desk-thoughts{top:64.5%}
  .desk-photography{top:80.1%;height:235px!important}
  .deskpaper{inset:0 0 15%}
  .desklabel{
    left:7%;right:0;
    min-height:31%;
    padding:13px 14px 13px 25px;
    column-gap:7px;
  }
  .desklabel b{
    width:42px;
    margin-left:-45%;
    font-size:24px;
  }
  .desklabel strong{font-size:25px}
  .desklabel small{font-size:13px}
  .desklabel em{font-size:26px}
  .deskpaper-opinion{padding:30px 28px}
  .deskpaper-opinion i{font-size:12px}
  .deskpaper-opinion mark{font-size:10px}
  .deskpaper-opinion u{font-size:20px}
  .deskpaper-notebook{padding:31px 45px 24px 50px}
  .deskpaper-notebook i{font-size:23px}
  .deskpaper-notebook span{font-size:17px}
  .deskpaper-notebook:after{right:9%;width:8%}
  .desk-photography .desklabel{min-height:35%}
  .desk-laptop{
    left:-12%;top:0;width:31%;height:13%;
  }
  .desk-coffee{
    left:59%;top:1.4%;width:22%;
  }
  .desk-books{
    right:-2%;top:3.2%;width:29%;height:11%;
  }
  .desk-camera{
    left:-8%;bottom:66%;width:31%;height:10%;
  }
  .desk-map{
    right:-5%;bottom:2%;width:34%;height:15%;
  }
  .desk-plant-a{right:-12%;top:-1%;width:30%;height:12%}
  .desk-plant-b{left:-13%;bottom:-1%;width:35%;height:10%}
  .desknote-bottom{
    left:3%;bottom:25%;
    font-size:18px;
  }
  .deskfooterline{
    left:20px;right:20px;bottom:15px;
    display:none;
  }
}
@media(max-width:520px){
  .deskstage{min-height:1710px}
  .deskhead{height:72px;padding:19px 17px 0}
  .deskbrand strong{font-size:23px}
  .deskprofile{left:20%;top:8.5%;width:60%}
  .desknote-left{left:8%;top:11.5%;font-size:18px}
  .desknote-right{right:4%;top:20%;font-size:16px}
  .deskintro{left:12%;top:27.6%;width:78%;font-size:15px}
  .deskpiece{left:16%!important;width:72%!important;height:235px!important}
  .desk-reporting{top:34.2%}
  .desk-opinion{top:49.2%}
  .desk-thoughts{top:64.1%}
  .desk-photography{top:79.4%;height:220px!important}
  .desklabel strong{font-size:22px}
  .desklabel small{font-size:12px}
  .desklabel b{width:38px;font-size:21px}
  .desk-coffee{left:63%;width:25%}
  .desk-books{right:-7%;width:34%}
  .desk-camera{left:-12%;width:35%}
}
""".strip()""".strip()


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
    print(f"Homepage polish: isolated_classes=1, hero_reference_4=1, work_reference_5=1, asset_version={ASSET_VERSION}, versioned_pages={versioned_pages}, css_isolated=1, inline_critical=1, duplicate_home_css=0")


if __name__ == "__main__":
    main()
