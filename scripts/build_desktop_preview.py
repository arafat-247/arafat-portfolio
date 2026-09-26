"""Build the fresh desktop portfolio prototype approved in chat.

This preview is independent of the live homepage. It uses real HTML/CSS/JS,
real portfolio imagery, a responsive layered desk composition, animated paper,
interactive navigation, and a live Dhaka analogue clock.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREVIEW = ROOT / "dist" / "desktop-preview" / "index.html"

HTML = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>Desktop prototype — Arafat Rahaman</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@500;600&family=DM+Serif+Display&family=Source+Serif+4:wght@400;600;700&display=swap" rel="stylesheet">
<style>
:root{
  --wood-1:#2a140b;
  --wood-2:#4a2513;
  --wood-3:#61351d;
  --paper:#efe3cf;
  --paper-2:#e3d2b7;
  --ink:#17110c;
  --muted:#7d6a58;
  --cream:#f5ead9;
  --red:#8f2a22;
  --green:#0b4d42;
  --gold:#cf9e5b;
  --shadow:0 22px 40px rgb(8 3 1 / .34);
}
*{box-sizing:border-box}
html,body{margin:0;min-height:100%;background:#0d1210;color:#fff}
body{font-family:"Source Serif 4",Georgia,serif;overflow-x:hidden}
a{color:inherit}
button,input,a{font:inherit}
.preview{
  min-height:100vh;
  padding:18px;
  background:
    radial-gradient(circle at 50% -10%,rgb(255 255 255 / .035),transparent 38%),
    #0d1210;
}
.desk{
  container-type:inline-size;
  position:relative;
  width:min(100%,1600px);
  min-height:760px;
  aspect-ratio:16/9;
  margin:0 auto;
  overflow:hidden;
  border:1px solid rgb(255 255 255 / .14);
  border-radius:28px;
  isolation:isolate;
  background:
    radial-gradient(circle at 65% 21%,rgb(248 194 115 / .12),transparent 22%),
    radial-gradient(circle at 15% 78%,rgb(0 0 0 / .22),transparent 30%),
    repeating-linear-gradient(91deg,transparent 0 12%,rgb(24 9 4 / .14) 12.2% 12.5%,transparent 12.8% 24%),
    linear-gradient(105deg,var(--wood-1),var(--wood-3) 32%,#3c1e10 58%,#6c3a20 82%,#2e170d);
  box-shadow:0 30px 80px rgb(0 0 0 / .46);
}
.desk:before{
  content:"";
  position:absolute;
  inset:0;
  z-index:-3;
  background:
    repeating-linear-gradient(0deg,transparent 0 24px,rgb(255 255 255 / .012) 25px 26px,transparent 27px 46px),
    linear-gradient(180deg,rgb(255 225 178 / .035),rgb(0 0 0 / .15));
  mix-blend-mode:screen;
}
.desk:after{
  content:"";
  position:absolute;
  inset:0;
  z-index:60;
  pointer-events:none;
  box-shadow:inset 0 0 95px rgb(0 0 0 / .35);
}
.masthead{
  position:absolute;
  z-index:50;
  left:4.4%;
  top:3.2%;
  display:grid;
  gap:.25cqw;
  text-decoration:none;
}
.masthead strong{
  font:400 clamp(26px,2.45cqw,40px)/.95 "DM Serif Display",Georgia,serif;
  letter-spacing:-.03em;
}
.masthead small{
  color:#efe4d5;
  font:800 clamp(6px,.55cqw,9px)/1 Arial,sans-serif;
  letter-spacing:.24em;
  text-transform:uppercase;
}
.nav{
  position:absolute;
  z-index:50;
  left:36.5%;
  top:3.1%;
  display:flex;
  gap:clamp(18px,2.2cqw,36px);
}
.nav a{
  position:relative;
  padding:.45cqw 0;
  color:#f4e7d7;
  text-decoration:none;
  font:400 clamp(13px,1.08cqw,18px)/1 "Source Serif 4",Georgia,serif;
  transition:transform .18s ease,color .18s ease;
}
.nav a:after{
  content:"";
  position:absolute;
  left:50%;
  right:50%;
  bottom:0;
  height:1px;
  background:#f1c984;
  transition:left .18s ease,right .18s ease;
}
.nav a:hover,.nav a:focus-visible{color:#f7d79e;transform:translateY(-2px)}
.nav a:hover:after,.nav a:focus-visible:after,.nav a[aria-current="page"]:after{left:0;right:0}

.social{
  position:absolute;
  z-index:50;
  right:13.4%;
  top:3.1%;
  display:flex;
  gap:.55cqw;
}
.social a{
  display:grid;
  width:clamp(24px,2cqw,34px);
  aspect-ratio:1;
  place-items:center;
  border:1px solid rgb(255 255 255 / .34);
  border-radius:50%;
  color:#fff;
  text-decoration:none;
  font:800 clamp(8px,.6cqw,10px)/1 Arial,sans-serif;
  transition:transform .18s ease,background .18s ease;
}
.social a:hover{transform:translateY(-2px);background:rgb(255 255 255 / .1)}

.location{
  position:absolute;
  z-index:45;
  right:2.3%;
  top:2.3%;
  color:#eadbc7;
  font:700 clamp(6px,.54cqw,9px)/1.3 Arial,sans-serif;
  letter-spacing:.06em;
  text-align:right;
  text-transform:uppercase;
}

.hero-copy{
  position:absolute;
  z-index:26;
  left:5.1%;
  top:31.2%;
  width:24.5%;
  padding:1.8cqw 1.9cqw 1.7cqw;
  background:linear-gradient(110deg,rgb(26 13 8 / .88),rgb(34 16 10 / .58));
  border:1px solid rgb(255 255 255 / .06);
  box-shadow:0 18px 34px rgb(0 0 0 / .26);
  backdrop-filter:blur(2px);
}
.hero-copy .eyebrow{
  display:block;
  margin-bottom:.9cqw;
  color:#eadfcf;
  font:800 clamp(7px,.72cqw,11px)/1 Arial,sans-serif;
  letter-spacing:.34em;
  text-transform:uppercase;
}
.hero-copy h1{
  margin:0;
  color:#fff8ee;
  font:400 clamp(38px,4.3cqw,70px)/.9 "DM Serif Display",Georgia,serif;
  letter-spacing:-.045em;
}
.hero-copy p{
  max-width:31ch;
  margin:1.05cqw 0 0;
  color:#eadfce;
  font-size:clamp(12px,1cqw,17px);
  line-height:1.45;
}
.cta{
  display:inline-flex;
  align-items:center;
  gap:1.15cqw;
  margin-top:1.35cqw;
  padding:.9cqw 1.15cqw;
  border-radius:4px;
  background:#f7eddd;
  color:#1e160f;
  text-decoration:none;
  font:700 clamp(10px,.8cqw,13px)/1 Arial,sans-serif;
  box-shadow:0 8px 20px rgb(0 0 0 / .22);
  transition:transform .2s ease,box-shadow .2s ease;
}
.cta:hover{transform:translateY(-3px);box-shadow:0 14px 25px rgb(0 0 0 / .3)}
.cta:after{content:"→";font-size:1.25em}

.portrait-stack{
  position:absolute;
  z-index:18;
  left:35.8%;
  top:8.2%;
  width:19.5%;
  height:25.5%;
  transform:rotate(-3deg);
  filter:drop-shadow(0 14px 14px rgb(12 5 2 / .28));
}
.portrait-stack:before,.portrait-stack:after{
  content:"";
  position:absolute;
  inset:4% 1% -4% 4%;
  background:#d8c9b3;
  transform:rotate(6deg);
  box-shadow:var(--shadow);
}
.portrait-stack:after{inset:2% -2% -2% 3%;transform:rotate(2deg);background:#eadcc7}
.polaroid{
  position:absolute;
  z-index:2;
  inset:0;
  padding:5.5% 5.5% 17%;
  background:#f3e8d8;
  box-shadow:var(--shadow);
}
.polaroid img{width:100%;height:100%;object-fit:cover;object-position:center 24%;filter:grayscale(.07) contrast(1.03)}
.polaroid:after{
  content:"Arafat Rahaman";
  position:absolute;
  left:7%;
  bottom:5.2%;
  color:#221811;
  font:600 clamp(10px,.9cqw,15px)/1.1 "Source Serif 4",Georgia,serif;
}

.camera{
  position:absolute;
  z-index:12;
  left:17.4%;
  top:8.5%;
  width:17.2%;
  height:20.2%;
  transform:rotate(-6deg);
  filter:drop-shadow(0 14px 13px rgb(0 0 0 / .38));
}
.camera-body{
  position:absolute;
  left:9%;top:18%;
  width:73%;height:58%;
  border-radius:16% 14% 12% 14%;
  background:linear-gradient(150deg,#1c1d1d,#070808 63%,#242424);
  border:1px solid #343434;
}
.camera-grip{
  position:absolute;
  right:4%;top:24%;
  width:28%;height:53%;
  border-radius:30% 48% 32% 27%;
  background:linear-gradient(130deg,#171818,#070707);
}
.camera-prism{
  position:absolute;
  left:29%;top:4%;
  width:34%;height:28%;
  clip-path:polygon(16% 100%,0 40%,30% 0,75% 0,100% 58%,88% 100%);
  background:#161717;
  border:1px solid #303030;
}
.camera-lens{
  position:absolute;
  z-index:3;
  left:21%;top:35%;
  width:42%;aspect-ratio:1;
  border-radius:50%;
  background:
    radial-gradient(circle at 43% 40%,#4c5c62 0 8%,#112027 9% 18%,#050708 19% 48%,#222 49% 57%,#080808 58% 70%,#1f1f1f 71%);
  box-shadow:0 0 0 7px #151515,0 0 0 11px #050505;
}
.camera:after{
  content:"";
  position:absolute;
  left:3%;top:4%;
  width:88%;height:16%;
  border-top:5px solid #811f1b;
  border-radius:50%;
  transform:rotate(-13deg);
  opacity:.95;
}

.coffee{
  position:absolute;
  z-index:15;
  left:60.8%;
  top:12%;
  width:10.5%;
  aspect-ratio:1;
  border-radius:50%;
  background:
    radial-gradient(circle at 48% 47%,#160e09 0 45%,#432717 47% 51%,#d3bd9c 52% 68%,#f2e7d5 69% 100%);
  box-shadow:0 13px 18px rgb(0 0 0 / .28);
  transform:rotate(5deg);
}
.coffee:after{
  content:"";
  position:absolute;
  right:-28%;top:34%;
  width:34%;height:29%;
  border:9px solid #ddc8a8;
  border-left-width:6px;
  border-radius:50%;
}

.books{
  position:absolute;
  z-index:10;
  right:2.6%;
  top:8%;
  width:17.5%;
  height:23%;
  transform:rotate(8deg);
}
.book{position:absolute;right:0;width:94%;height:18%;border-radius:3px;box-shadow:0 6px 10px rgb(0 0 0 / .25);background:linear-gradient(180deg,#132726,#071615)}
.book:nth-child(1){top:0;right:4%;background:#252323}
.book:nth-child(2){top:18%;background:#12312d}
.book:nth-child(3){top:36%;right:2%;background:#1b2725}
.book:nth-child(4){top:54%;right:5%;background:#101d1b}
.book:nth-child(5){top:72%;background:#29251f}
.book span{position:absolute;right:6%;top:50%;transform:translateY(-50%);color:#d6b170;font:700 clamp(7px,.7cqw,11px)/1 Georgia,serif;letter-spacing:.08em;text-transform:uppercase}

.clock{
  position:absolute;
  z-index:22;
  right:1.3%;
  top:0.8%;
  width:8%;
  display:grid;
  gap:.3cqw;
  justify-items:center;
  color:#f0e4d2;
}
.clock-face{
  position:relative;
  width:100%;
  aspect-ratio:1;
  border:clamp(5px,.55cqw,9px) solid #211b17;
  border-radius:50%;
  background:radial-gradient(circle at 42% 36%,#f5ead9,#d6c3a3 73%,#a48766);
  box-shadow:0 12px 18px rgb(0 0 0 / .35),inset 0 0 0 1px #7a654b;
}
.clock-face i{position:absolute;color:#36281e;font:700 clamp(7px,.68cqw,11px)/1 Georgia,serif;font-style:normal}
.n12{top:7%;left:50%;transform:translateX(-50%)}.n3{right:8%;top:50%;transform:translateY(-50%)}.n6{bottom:7%;left:50%;transform:translateX(-50%)}.n9{left:8%;top:50%;transform:translateY(-50%)}
.hand{position:absolute;z-index:3;left:50%;bottom:50%;display:block;border-radius:99px;background:#34271d;transform-origin:50% 100%}
.hour{width:3px;height:24%}.minute{width:2px;height:34%}.second{width:1px;height:39%;background:#a42821}
.pin{position:absolute;z-index:4;left:50%;top:50%;width:7px;height:7px;border-radius:50%;background:#34271d;transform:translate(-50%,-50%)}
.clock small{font:800 clamp(5px,.45cqw,8px)/1 Arial,sans-serif;letter-spacing:.12em;text-transform:uppercase}

.cards{
  position:absolute;
  z-index:24;
  left:31.8%;
  top:34.2%;
  width:37.2%;
  height:48.6%;
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:2.2%;
}
.work-card{
  position:relative;
  display:block;
  overflow:visible;
  text-decoration:none;
  transform-origin:50% 50%;
  animation:paperfloat 8.8s ease-in-out infinite;
}
.work-card:nth-child(2){animation-duration:10.2s;animation-delay:-2.1s}
.work-card:nth-child(3){animation-duration:9.6s;animation-delay:-3.7s}
.work-card:nth-child(4){animation-duration:11.3s;animation-delay:-1.2s}
.work-card:before,.work-card:after{
  content:"";
  position:absolute;
  inset:3% -1% -4% 2%;
  z-index:-2;
  background:#cdbda7;
  transform:rotate(2.3deg);
  box-shadow:0 13px 22px rgb(0 0 0 / .23);
}
.work-card:after{inset:1% 1% -2% -1%;z-index:-1;background:#dfd0b8;transform:rotate(-1.8deg)}
.paper-card{
  position:absolute;
  inset:0;
  display:grid;
  grid-template-rows:1fr auto;
  padding:5% 5% 6%;
  background:#efe1cb;
  color:#22160e;
  box-shadow:0 11px 20px rgb(0 0 0 / .25);
  transition:transform .22s ease,box-shadow .22s ease;
}
.work-card:hover .paper-card,.work-card:focus-visible .paper-card{
  transform:translateY(-7px) rotate(.3deg);
  box-shadow:0 20px 28px rgb(0 0 0 / .34);
}
.work-card:focus-visible{outline:3px solid #f2cb89;outline-offset:5px}
.work-card figure{margin:0;min-height:0;overflow:hidden;background:#c8b99f}
.work-card img{display:block;width:100%;height:100%;object-fit:cover;filter:saturate(.82) contrast(1.04)}
.work-card .label{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:.5cqw;
  padding-top:5%;
  font:600 clamp(13px,1.28cqw,21px)/1 "Caveat",cursive;
}
.work-card .label:after{content:"→";font-family:Georgia,serif;font-size:.9em}
@keyframes paperfloat{
  0%,100%{transform:translate3d(0,0,0) rotate(-.2deg)}
  45%{transform:translate3d(1px,-2px,0) rotate(.45deg)}
  72%{transform:translate3d(-1px,.7px,0) rotate(-.35deg)}
}

.newspaper{
  position:absolute;
  z-index:13;
  right:2.2%;
  top:31.2%;
  width:24.5%;
  height:29.5%;
  padding:1.6cqw 1.7cqw;
  color:#20170f;
  background:#dccbb2;
  transform:rotate(7deg);
  box-shadow:var(--shadow);
  overflow:hidden;
}
.newspaper:before{content:"";position:absolute;inset:0;background:repeating-linear-gradient(0deg,transparent 0 7px,rgb(86 65 43 / .08) 8px 9px);opacity:.55}
.paper-mast{position:relative;border-bottom:2px solid #38291e;padding-bottom:.55cqw;font:700 clamp(18px,2.1cqw,34px)/.9 "DM Serif Display",Georgia,serif}
.newspaper h3{position:relative;margin:.8cqw 0 .7cqw;font:700 clamp(20px,2.15cqw,35px)/.95 "DM Serif Display",Georgia,serif}
.columns{position:relative;display:grid;grid-template-columns:1fr 1fr 1fr;gap:.8cqw;color:#554331;font-size:clamp(6px,.5cqw,8px);line-height:1.25}
.columns span{display:block;height:7.2cqw;background:repeating-linear-gradient(180deg,currentColor 0 1px,transparent 1px 5px);opacity:.42}

.notebook{
  position:absolute;
  z-index:15;
  right:1%;
  bottom:8%;
  width:17%;
  height:25%;
  padding:2cqw 1.5cqw 1cqw 2.4cqw;
  color:#3f3025;
  background:
    repeating-linear-gradient(180deg,#f0e2c8 0 1.3cqw,#c3aa84 1.34cqw 1.38cqw);
  transform:rotate(-7deg);
  box-shadow:var(--shadow);
}
.notebook:before{
  content:"";
  position:absolute;
  left:.75cqw;top:0;bottom:0;
  width:.55cqw;
  background:repeating-linear-gradient(180deg,#392f28 0 .5cqw,transparent .5cqw .92cqw);
}
.notebook strong{display:block;margin-bottom:.8cqw;font:600 clamp(13px,1.2cqw,20px)/1 "Caveat",cursive}
.notebook ul{margin:0;padding-left:1.2em;font:500 clamp(9px,.8cqw,13px)/1.65 "Caveat",cursive}

.map{
  position:absolute;
  z-index:5;
  left:-2%;
  top:20%;
  width:17%;
  height:26%;
  transform:rotate(-9deg);
  opacity:.9;
  background:
    linear-gradient(35deg,transparent 0 19%,#5f755e 20% 22%,transparent 23% 46%,#8b5b48 47% 49%,transparent 50%),
    repeating-linear-gradient(75deg,#c8b994 0 12px,#c3af86 13px 14px);
  border:1px solid #b7a27c;
  box-shadow:0 12px 18px rgb(0 0 0 / .24);
}
.map:after{content:"BANGLADESH";position:absolute;right:12%;bottom:12%;color:#6b5942;font:800 clamp(7px,.64cqw,10px)/1 Arial,sans-serif;letter-spacing:.16em}

.glasses{
  position:absolute;
  z-index:19;
  left:9%;
  bottom:5.5%;
  width:16%;
  height:8%;
  transform:rotate(5deg);
}
.glasses:before,.glasses:after{content:"";position:absolute;top:18%;width:35%;height:60%;border:3px solid #171717;border-radius:48%}
.glasses:before{left:8%}.glasses:after{right:8%}
.glasses i{position:absolute;left:43%;top:43%;width:14%;height:3px;background:#171717}

.recent{
  position:absolute;
  z-index:35;
  left:0;
  right:0;
  bottom:0;
  min-height:17%;
  padding:1.45% 4.2% 1.7%;
  color:#f7ead8;
  background:linear-gradient(90deg,rgb(15 9 6 / .97),rgb(31 16 9 / .94));
  border-top:1px solid rgb(255 255 255 / .08);
  box-shadow:0 -12px 28px rgb(0 0 0 / .24);
}
.recent-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:.9cqw}
.recent-head h2{margin:0;font:400 clamp(20px,2.1cqw,34px)/1 "DM Serif Display",Georgia,serif}
.recent-head a{font:700 clamp(8px,.65cqw,11px)/1 Arial,sans-serif;letter-spacing:.06em;text-decoration:none;text-transform:uppercase}
.story-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:1.2cqw}
.story{
  display:grid;
  grid-template-columns:34% 1fr;
  gap:.9cqw;
  align-items:center;
  color:inherit;
  text-decoration:none;
  min-width:0;
}
.story img{width:100%;aspect-ratio:1.25;object-fit:cover;border-radius:2px}
.story small{display:block;margin-bottom:.35cqw;color:#bca992;font:800 clamp(5px,.48cqw,8px)/1 Arial,sans-serif;letter-spacing:.12em;text-transform:uppercase}
.story strong{display:block;font:600 clamp(10px,.92cqw,15px)/1.15 "Source Serif 4",Georgia,serif}

@media(max-width:1180px){
  .desk{min-height:700px}
  .hero-copy{width:27%;left:4.2%}
  .cards{left:31.3%;width:38.5%}
  .newspaper{width:25.5%}
  .social{display:none}
  .location{top:3.4%}
}
@media(max-width:980px){
  .preview{padding:0}
  .desk{width:100vw;min-width:920px;border-radius:0}
  .books{right:1%}
}
@media(prefers-reduced-motion:reduce){
  .work-card{animation:none!important}
  .work-card .paper-card,.nav a,.cta,.social a{transition:none!important}
}
</style>
</head>
<body>
<div class="preview">
<main class="desk" aria-label="Desktop portfolio prototype">
  <a class="masthead" href="../"><strong>Arafat Rahaman</strong><small>Journalist</small></a>

  <nav class="nav" aria-label="Prototype navigation">
    <a href="../" aria-current="page">Home</a>
    <a href="../about/">About</a>
    <a href="../all-work/">Work</a>
    <a href="../thoughts/">Writing</a>
    <a href="../contact/">Contact</a>
  </nav>

  <div class="social" aria-label="Social links">
    <a href="mailto:arafat.mcj@yahoo.com" aria-label="Email">@</a>
    <a href="../contact/" aria-label="Facebook">f</a>
    <a href="../contact/" aria-label="LinkedIn">in</a>
    <a href="../contact/" aria-label="Instagram">ig</a>
  </div>
  <div class="location">Dhaka, Bangladesh<br>Portfolio prototype</div>

  <div class="map" aria-hidden="true"></div>

  <div class="camera" aria-hidden="true">
    <span class="camera-body"></span><span class="camera-grip"></span><span class="camera-prism"></span><span class="camera-lens"></span>
  </div>

  <a class="portrait-stack" href="../about/" aria-label="About Arafat Rahaman">
    <span class="polaroid"><img src="../assets/identity/asset0.webp" alt="Arafat Rahaman"></span>
  </a>

  <div class="coffee" aria-hidden="true"></div>

  <div class="books" aria-hidden="true">
    <div class="book"><span>Bangladesh</span></div>
    <div class="book"><span>Politics</span></div>
    <div class="book"><span>Development</span></div>
    <div class="book"><span>Journalism</span></div>
    <div class="book"><span>Society</span></div>
  </div>

  <div class="clock" aria-label="Current time in Dhaka">
    <span class="clock-face">
      <i class="n12">12</i><i class="n3">3</i><i class="n6">6</i><i class="n9">9</i>
      <b class="hand hour" data-hour></b>
      <b class="hand minute" data-minute></b>
      <b class="hand second" data-second></b>
      <em class="pin"></em>
    </span>
    <small data-clock-label>Dhaka</small>
  </div>

  <section class="hero-copy">
    <span class="eyebrow">Stories from</span>
    <h1>People,<br>places and<br>possibilities</h1>
    <p>I report on education, governance, labour, politics and the issues that shape everyday life in Bangladesh.</p>
    <a class="cta" href="../all-work/">Explore my work</a>
  </section>

  <section class="cards" aria-label="Portfolio sections">
    <a class="work-card" href="../reporting/">
      <span class="paper-card">
        <figure><img src="../assets/photography/Rajshahi University-nightscape-Journalist-Arafat-Rahaman (2).webp" alt=""></figure>
        <span class="label">Reporting</span>
      </span>
    </a>

    <a class="work-card" href="../opinion/">
      <span class="paper-card">
        <figure><img src="../assets/photography/Rajshahi University-nightscape-Journalist-Arafat-Rahaman (4).webp" alt=""></figure>
        <span class="label">Opinion &amp; Analysis</span>
      </span>
    </a>

    <a class="work-card" href="../photography/">
      <span class="paper-card">
        <figure><img src="../assets/photography/Rajshahi University-nightscape-Journalist-Arafat-Rahaman (6).webp" alt=""></figure>
        <span class="label">Photography</span>
      </span>
    </a>

    <a class="work-card" href="../thoughts/">
      <span class="paper-card">
        <figure><img src="../assets/photography/Rajshahi University-nightscape-Journalist-Arafat-Rahaman (1).webp" alt=""></figure>
        <span class="label">Writing</span>
      </span>
    </a>
  </section>

  <article class="newspaper" aria-hidden="true">
    <div class="paper-mast">The Daily Star</div>
    <h3>A more equal<br>Bangladesh?</h3>
    <div class="columns"><span></span><span></span><span></span></div>
  </article>

  <aside class="notebook" aria-hidden="true">
    <strong>Ideas</strong>
    <ul><li>Interviews</li><li>Field visits</li><li>Data</li><li>Deadlines</li><li>A fairer Bangladesh</li></ul>
  </aside>

  <div class="glasses" aria-hidden="true"><i></i></div>

  <section class="recent" aria-label="Recent stories">
    <div class="recent-head"><h2>Recent stories</h2><a href="../all-work/">View all stories →</a></div>
    <div class="story-grid">
      <a class="story" href="../reporting/"><img src="../assets/photography/Rajshahi University-nightscape-Journalist-Arafat-Rahaman (2).webp" alt=""><span><small>Education</small><strong>Thousands of BCS posts go unfilled as candidate pool narrows</strong></span></a>
      <a class="story" href="../reporting/"><img src="../assets/photography/Rajshahi University-nightscape-Journalist-Arafat-Rahaman (4).webp" alt=""><span><small>Universities</small><strong>Vice-chancellors’ partisan notices renew questions over neutrality</strong></span></a>
      <a class="story" href="../reporting/"><img src="../assets/photography/Rajshahi University-nightscape-Journalist-Arafat-Rahaman (1).webp" alt=""><span><small>Health</small><strong>Dengue cases rise again, putting pressure on hospitals</strong></span></a>
      <a class="story" href="../reporting/"><img src="../assets/photography/Rajshahi University-nightscape-Journalist-Arafat-Rahaman (6).webp" alt=""><span><small>Labour</small><strong>Hundreds of workers terminated at Malaysia factory, face uncertainty</strong></span></a>
    </div>
  </section>
</main>
</div>
<script>
(()=> {
  const root=document.querySelector('.clock');
  if(!root) return;
  const hour=root.querySelector('[data-hour]');
  const minute=root.querySelector('[data-minute]');
  const second=root.querySelector('[data-second]');
  const label=root.querySelector('[data-clock-label]');
  const tick=()=> {
    const parts=new Intl.DateTimeFormat('en-GB',{
      timeZone:'Asia/Dhaka',hour:'2-digit',minute:'2-digit',second:'2-digit',hour12:false
    }).formatToParts(new Date());
    const n=t=>Number(parts.find(p=>p.type===t)?.value||0);
    const h=n('hour'),m=n('minute'),s=n('second');
    hour.style.transform=`rotate(${(h%12)*30+m*.5}deg)`;
    minute.style.transform=`rotate(${m*6+s*.1}deg)`;
    second.style.transform=`rotate(${s*6}deg)`;
    label.textContent=`Dhaka · ${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}`;
  };
  tick();
  setInterval(tick,1000);
})();
</script>
</body>
</html>'''


def main() -> None:
    PREVIEW.parent.mkdir(parents=True,exist_ok=True)
    PREVIEW.write_text(HTML,encoding="utf-8")
    print("Fresh desktop prototype built from scratch; live homepage untouched")


if __name__=="__main__":
    main()
