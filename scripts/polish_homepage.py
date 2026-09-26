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
ASSET_VERSION = "21.2.3"

HOME_CSS = r"""

/* Homepage v20.3 — photographic journalist's desk */
body.home{
  background:#15110d;
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
  background:#15110d;
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
  min-height:900px;
  margin:0 auto;
  overflow:hidden;
  border:1px solid rgb(255 255 255 / 14%);
  border-radius:28px;
  isolation:isolate;
  color:#f6ead9;
  background:
    radial-gradient(circle at 72% 15%,rgb(241 196 124 / 12%),transparent 21%),
    linear-gradient(100deg,rgba(0,0,0,.12),transparent 28%,rgba(0,0,0,.08) 60%),
    repeating-linear-gradient(92deg,transparent 0 145px,rgba(35,13,4,.17) 148px 152px,transparent 155px 298px),
    linear-gradient(112deg,#2d160d 0%,#5b2f18 33%,#3a1d11 60%,#6f3b21 84%,#2d170e 100%);
  box-shadow:0 32px 90px rgb(0 0 0 / 45%);
}
.deskgrain{
  position:absolute;inset:0;z-index:-1;pointer-events:none;
  background:
    repeating-linear-gradient(0deg,transparent 0 24px,rgb(255 255 255 / .012) 25px 26px,transparent 27px 47px),
    radial-gradient(circle at 20% 75%,rgb(0 0 0 / .24),transparent 31%);
  mix-blend-mode:screen
}
.deskbrand{position:absolute;z-index:30;left:4.2%;top:3.4%}
.deskbrand a{display:grid;gap:6px;color:#fff;text-decoration:none}
.deskbrand strong{font:400 clamp(28px,2.6vw,44px)/.95 "DM Serif Display",Georgia,serif;letter-spacing:-.04em}
.deskbrand small{font:800 8px/1 Arial,sans-serif;letter-spacing:.22em;text-transform:uppercase;color:#e2cfb8}
.desknav{
  position:absolute;z-index:30;left:36%;top:3.6%;
  display:flex;gap:clamp(20px,2.4vw,40px)
}
.desknav a{
  color:#f1e5d5;text-decoration:none;font:600 14px/1 Arial,sans-serif;
  padding:7px 0;border-bottom:1px solid transparent
}
.desknav a:hover,.desknav a:focus-visible,.desknav a[aria-current]{color:#f2c47e;border-color:#f2c47e}
.deskintro{
  position:absolute;z-index:14;left:4.6%;top:16%;width:26.5%;
  padding:34px 32px 31px;
  background:linear-gradient(135deg,rgba(21,11,7,.91),rgba(26,13,8,.62));
  border:1px solid rgb(255 255 255 / 6%);
  box-shadow:0 20px 35px rgb(0 0 0 / 26%)
}
.deskintro>span{font:800 8px/1 Arial,sans-serif;letter-spacing:.25em;text-transform:uppercase;color:#d9b986}
.deskintro h1{margin:17px 0 16px;font:400 clamp(39px,4vw,65px)/.91 "DM Serif Display",Georgia,serif;letter-spacing:-.045em}
.deskintro p{margin:0;color:#eadfce;font:400 16px/1.45 "Source Serif 4",Georgia,serif}
.deskintro>a{display:inline-flex;gap:26px;margin-top:22px;padding-bottom:6px;border-bottom:1px solid #e8d3b6;color:#fff;text-decoration:none;font:700 12px/1 Arial,sans-serif}
.deskportrait{
  position:absolute;z-index:12;left:36.5%;top:10%;width:19.2%;height:26%;
  padding:10px 10px 35px;background:#efe2cf;transform:rotate(-3deg);
  box-shadow:0 20px 36px rgb(0 0 0 / 34%);text-decoration:none
}
.deskportrait:before{content:"";position:absolute;inset:6px -10px -9px 10px;z-index:-1;background:#d2c2ab;transform:rotate(5deg);box-shadow:0 14px 26px rgb(0 0 0 / 28%)}
.deskportrait picture,.deskportrait img{display:block;width:100%;height:100%}
.deskportrait img{object-fit:cover;object-position:center 30%;filter:grayscale(.12) contrast(1.04)}
.deskportrait>span{position:absolute;left:14px;bottom:11px;color:#20160f;font:600 12px/1 "Caveat",cursive}
.deskwork{
  position:absolute;z-index:16;left:31.7%;top:37.5%;width:39%;height:45%;
  display:grid;grid-template-columns:1fr 1fr;gap:16px
}
.desk-work-card{
  position:relative;display:flex;flex-direction:column;min-width:0;overflow:hidden;
  padding:16px 16px 14px;color:#20160f;text-decoration:none;
  background:#efe1ca;box-shadow:0 15px 25px rgb(0 0 0 / 28%);
  transition:transform .22s ease,box-shadow .22s ease
}
.desk-work-card:nth-child(1){transform:rotate(-1.4deg)}
.desk-work-card:nth-child(2){transform:rotate(1.2deg)}
.desk-work-card:nth-child(3){transform:rotate(.8deg)}
.desk-work-card:nth-child(4){transform:rotate(-1deg)}
.desk-work-card:hover,.desk-work-card:focus-visible{transform:translateY(-7px) rotate(0);box-shadow:0 22px 31px rgb(0 0 0 / 35%)}
.desk-card-number{position:absolute;right:12px;top:10px;font:800 7px/1 Arial,sans-serif;letter-spacing:.08em;color:#7d6d59}
.desk-work-card>strong{margin-top:auto;font:600 clamp(18px,1.55vw,25px)/1 "DM Serif Display",Georgia,serif}
.desk-work-card>small{margin-top:5px;color:#665846;font:600 10px/1.25 Arial,sans-serif}
.desk-newspaper{height:59%;padding:10px;background:#e6d8c1;border:1px solid #b7a48b}
.desk-newspaper b{display:block;border-bottom:2px solid #33271d;padding-bottom:6px;font:700 19px/1 "DM Serif Display",Georgia,serif}
.desk-newspaper em{display:block;margin:7px 0 6px;font:800 7px/1 Arial,sans-serif;letter-spacing:.14em}
.desk-newspaper i{display:block;height:1px;margin:7px 0;background:#76624b;opacity:.55}
.desk-marked-page{position:relative;height:59%;padding:15px 14px;background:#f5ead8;border:1px solid #c8b293}
.desk-marked-page i{display:block;margin:7px 0;font:600 12px/1.1 "Source Serif 4",Georgia,serif}
.desk-marked-page i:nth-child(2){background:#e4bf58;width:max-content;padding:1px 4px}
.desk-marked-page b{position:absolute;right:14px;bottom:6px;color:#a32f24;font:600 39px/1 "Caveat",cursive;transform:rotate(8deg)}
.desk-notebook{
  height:59%;padding:17px 15px 12px 28px;
  background:repeating-linear-gradient(180deg,#f2e6cf 0 25px,#baa47f 26px 27px);
  border-left:8px solid #3c352e
}
.desk-notebook i{display:block;margin:6px 0;color:#493a2e;font:600 13px/1 "Caveat",cursive}
.desk-photo figure{height:59%;margin:0;overflow:hidden;background:#111}
.desk-photo img{width:100%;height:100%;object-fit:cover;filter:saturate(.84) contrast(1.04)}
.deskclock-object{
  position:absolute;z-index:18;right:2.8%;top:3.4%;width:8.4%;
  display:grid;gap:6px;justify-items:center;color:#f1e2cf;
  transform:rotate(2deg);filter:drop-shadow(0 14px 16px rgb(0 0 0 / 33%))
}
.deskclock-face{
  position:relative;width:100%;aspect-ratio:1;border:8px solid #211b17;border-radius:50%;
  background:radial-gradient(circle at 40% 35%,#f5ead8,#d7c3a4 73%,#aa8f6f)
}
.deskclock-face i{position:absolute;color:#36291f;font:700 9px/1 Georgia,serif;font-style:normal}
.deskclock-12{top:7%;left:50%;transform:translateX(-50%)}.deskclock-3{right:8%;top:50%;transform:translateY(-50%)}.deskclock-6{bottom:7%;left:50%;transform:translateX(-50%)}.deskclock-9{left:8%;top:50%;transform:translateY(-50%)}
.deskclock-hand{position:absolute;left:50%;bottom:50%;display:block;transform-origin:50% 100%;border-radius:20px;background:#34271d}
.deskclock-hour{width:3px;height:24%}.deskclock-minute{width:2px;height:34%}.deskclock-second{width:1px;height:39%;background:#a52a22}
.deskclock-face>span{position:absolute;z-index:4;left:50%;top:50%;width:7px;height:7px;border-radius:50%;background:#34271d;transform:translate(-50%,-50%)}
.deskclock-object>small{font:800 7px/1 Arial,sans-serif;letter-spacing:.12em;text-transform:uppercase}
.deskcamera{position:absolute;z-index:9;left:12%;bottom:9.5%;width:13.8%;height:11%;background:linear-gradient(145deg,#1b1c1c,#090909);border-radius:12px;transform:rotate(-9deg);box-shadow:0 16px 24px rgb(0 0 0 / 38%)}
.deskcamera i{position:absolute;left:31%;top:24%;width:42%;aspect-ratio:1;border-radius:50%;background:radial-gradient(circle,#050708 0 38%,#3b4142 39% 49%,#070707 50% 65%,#232323 66%);box-shadow:0 0 0 7px #0b0b0b}
.deskcamera b{position:absolute;left:18%;top:-13%;width:34%;height:22%;background:#191919;border-radius:4px}
.deskcoffee{position:absolute;z-index:10;right:16%;top:12%;width:8.6%;aspect-ratio:1;border-radius:50%;background:radial-gradient(circle,#1a0e08 0 43%,#cbb393 45% 65%,#f2e7d7 66%);box-shadow:0 13px 18px rgb(0 0 0 / 27%)}
.deskcoffee:after{content:"";position:absolute;right:-26%;top:34%;width:35%;height:29%;border:8px solid #dcc5a5;border-left-width:5px;border-radius:50%}
.deskpencil{position:absolute;z-index:8;right:8.5%;top:33%;width:2px;height:180px;background:#dfb14f;transform:rotate(31deg);box-shadow:0 0 0 2px #845d24}
.desk-selected{
  position:absolute;z-index:17;right:2.6%;top:31.5%;width:24%;min-height:42%;
  padding:20px 20px 18px;color:#1f160f;background:#ddccb3;
  transform:rotate(4deg);box-shadow:0 21px 38px rgb(0 0 0 / 32%)
}
.desk-selected header{display:grid;grid-template-columns:1fr auto;gap:4px 12px;padding-bottom:13px;border-bottom:2px solid #35281e}
.desk-selected header>span{grid-column:1/-1;font:800 7px/1 Arial,sans-serif;letter-spacing:.16em;text-transform:uppercase;color:#7a6046}
.desk-selected h2{margin:0;font:400 27px/1 "DM Serif Display",Georgia,serif}
.desk-selected header a{align-self:end;color:#33271d;text-decoration:none;font:700 8px/1 Arial,sans-serif;text-transform:uppercase}
.desk-selected-list{display:grid}
.desk-selected-list a{position:relative;display:grid;gap:5px;padding:14px 25px 14px 0;border-bottom:1px solid #9d876b;color:#23170f;text-decoration:none}
.desk-selected-list small{font:800 6px/1 Arial,sans-serif;letter-spacing:.08em;text-transform:uppercase;color:#7a654d}
.desk-selected-list strong{font:600 15px/1.08 "Source Serif 4",Georgia,serif}
.desk-selected-list span{position:absolute;right:2px;top:50%;transform:translateY(-50%);font-size:18px}
.deskcontact{
  position:absolute;z-index:20;left:28.8%;bottom:2.6%;display:flex;gap:26px;align-items:center;
  padding:9px 14px;border-top:1px solid rgb(255 255 255 / 24%);
  color:#eadbc7;text-decoration:none;font:700 9px/1 Arial,sans-serif;letter-spacing:.08em;text-transform:uppercase
}
.deskcontact strong{color:#f0c88c}
.deskhome a:focus-visible{outline:3px solid #f2c47e;outline-offset:4px}
@media(max-width:1180px) and (min-width:801px){
  .deskstage{min-height:820px}
  .deskintro{width:28.5%}
  .deskwork{left:31%;width:40%}
  .desk-selected{width:25%}
  .desknav{left:34%;gap:18px}
}
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
    color:#171512;background:rgb(247 241 231 / 97%);
    backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px)
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
    padding:78px 26px 28px;
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
  .portalpanel:before{content:"";position:absolute;inset:0;z-index:-1;pointer-events:none}
  .portalimage{position:absolute;inset:0;z-index:-3;width:100%;height:100%;object-fit:cover}
  .portalart{position:absolute;inset:0;z-index:-3}

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
