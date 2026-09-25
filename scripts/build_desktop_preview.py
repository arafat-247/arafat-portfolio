"""Build a full-canvas desktop prototype from the approved desk as a visual atlas.

The live homepage is never changed. The approved image is not rendered as a full-page
background; photographed objects are cropped from it into independent layers over a
new responsive desk surface.
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
<title>Desktop prototype - Arafat Rahaman</title>
<link rel="stylesheet" href="../portfolio.css?v=21.2.3">
<style>
:root{--desk:#321a0e;--cream:#f2e5cf;--ink:#17120e;--accent:#8f2e25;--green:#123e35}
*{box-sizing:border-box}
html,body{margin:0;min-height:100%;background:#101413;color:#fff}
body{font-family:Georgia,"Times New Roman",serif;overflow-x:hidden}
a{color:inherit}
.preview-shell{min-height:100vh;padding:16px;display:grid;place-items:center;background:#101413}
.desk-canvas{container-type:inline-size;position:relative;width:min(100%,1600px);aspect-ratio:1447/1087;min-height:660px;overflow:hidden;border:1px solid rgb(255 255 255 / .15);border-radius:24px;isolation:isolate;box-shadow:0 28px 70px rgb(0 0 0 / .48);background:#3b1f11}
.desk-surface{position:absolute;inset:0;z-index:-20;overflow:hidden;background:linear-gradient(105deg,#2f160c,#5a2f18 34%,#3c1e10 61%,#673719)}
.desk-surface:before{content:"";position:absolute;inset:-18%;background:url('../assets/home/approved-desk-desktop.webp') 27% 25%/175% auto no-repeat;filter:blur(24px) brightness(.7) saturate(.8);transform:scale(1.08);opacity:.9}
.desk-surface:after{content:"";position:absolute;inset:0;background:repeating-linear-gradient(91deg,transparent 0 11%,rgb(15 5 2 / .13) 11.2% 11.5%,transparent 11.7% 22%),linear-gradient(180deg,rgb(255 222 175 / .035),rgb(0 0 0 / .15));mix-blend-mode:multiply}

.brand{position:absolute;z-index:40;left:7.8%;top:2.3%;display:grid;gap:.3cqw;text-decoration:none}.brand strong{font:400 clamp(25px,2.4cqw,39px)/.9 Georgia,serif;letter-spacing:-.04em}.brand small{font:800 clamp(6px,.55cqw,9px)/1 Arial,sans-serif;letter-spacing:.24em;text-transform:uppercase;color:#e7d8c6}
.topnav{position:absolute;z-index:40;left:50%;top:2.2%;display:flex;gap:clamp(18px,2.5cqw,40px);transform:translateX(-4%)}.topnav a{position:relative;padding:.55cqw .15cqw;color:#f2e6d5;text-decoration:none;font:400 clamp(12px,1.15cqw,18px)/1 Georgia,serif}.topnav a:after{content:"";position:absolute;left:50%;right:50%;bottom:0;height:1px;background:#f0d0a0;transition:left .2s ease,right .2s ease}.topnav a:hover:after,.topnav a:focus-visible:after,.topnav a[aria-current="page"]:after{left:0;right:0}.topnav a:hover{transform:translateY(-1px)}

.object{position:absolute;z-index:8;overflow:hidden;pointer-events:none}.object img{position:absolute;display:block;max-width:none!important;user-select:none;-webkit-user-drag:none}
.object.soft{filter:drop-shadow(0 9px 9px rgb(13 5 1 / .22));mask-image:radial-gradient(ellipse at center,#000 58%,transparent 100%);-webkit-mask-image:radial-gradient(ellipse at center,#000 58%,transparent 100%)}
.obj-laptop{left:-1.4%;top:0;width:11.5%;height:35%}.obj-laptop img{width:869.57%;height:285.71%;left:12.2%;top:0}
.obj-coffee{left:58.6%;top:5.2%;width:18.8%;height:24.5%}.obj-coffee img{width:531.91%;height:408.16%;left:-311.7%;top:-21.22%}
.obj-books{left:73.2%;top:-1%;width:27%;height:31%}.obj-books img{width:370.37%;height:322.58%;left:-271.11%;top:3.23%}
.obj-camera{left:17.4%;top:67.2%;width:23.5%;height:27.4%}.obj-camera img{width:425.53%;height:364.96%;left:-74.04%;top:-245.26%}
.obj-glasses{left:-.5%;top:66.5%;width:16.5%;height:17%}.obj-glasses img{width:606.06%;height:588.24%;left:3.03%;top:-391.18%}
.obj-bottomright{left:64.6%;top:63.6%;width:36%;height:36.4%}.obj-bottomright img{width:277.78%;height:274.73%;left:-179.44%;top:-174.73%}
.obj-plantleft{left:-2.2%;top:80.5%;width:14.5%;height:20.5%}.obj-plantleft img{width:689.66%;height:487.8%;left:15.17%;top:-392.68%}

.paper{position:absolute;z-index:18;display:block;overflow:hidden;text-decoration:none;filter:drop-shadow(0 9px 8px rgb(16 6 2 / .22));transform-origin:50% 50%;transition:transform .28s cubic-bezier(.2,.72,.2,1),filter .28s ease;will-change:transform}.paper img{position:absolute;display:block;max-width:none!important;user-select:none;-webkit-user-drag:none}.paper:focus-visible{outline:3px solid #f0d0a0;outline-offset:5px}
.profile{left:34.6%;top:4.2%;width:22.7%;height:24.5%;clip-path:polygon(4% 3%,92% 0,100% 91%,8% 100%,0 11%);transform:rotate(.1deg)}.profile img{width:440.53%;height:408.17%;left:-152.43%;top:-17.15%}
.reporting{left:6%;top:36.4%;width:25%;height:31.8%;clip-path:polygon(2% 4%,93% 0,100% 96%,11% 100%,0 11%);transform:rotate(-.25deg)}.reporting img{width:400%;height:314.47%;left:-24%;top:-114.47%}
.opinion{left:31.3%;top:36.8%;width:26.5%;height:31.4%;clip-path:polygon(1% 3%,94% 0,100% 94%,7% 100%,0 8%);transform:rotate(.2deg)}.opinion img{width:377.36%;height:318.48%;left:-118.12%;top:-117.20%}
.thoughts{left:57.7%;top:36.5%;width:26.1%;height:31.5%;clip-path:polygon(3% 1%,96% 2%,100% 93%,7% 100%,0 8%);transform:rotate(-.15deg)}.thoughts img{width:383.15%;height:317.47%;left:-221.08%;top:-115.88%}
.photography{left:39.1%;top:68%;width:25.4%;height:23%;clip-path:polygon(2% 3%,96% 0,100% 93%,7% 100%,0 8%);transform:rotate(.15deg)}.photography img{width:393.71%;height:434.79%;left:-153.94%;top:-295.66%}
.paper:hover,.paper:focus-visible{z-index:31;transform:translate3d(0,-7px,0) rotate(0deg) scale(1.012);filter:drop-shadow(0 16px 12px rgb(16 6 2 / .36))}
@keyframes breezeA{0%,100%{translate:0 0}48%{translate:.6px -1px}65%{translate:-.4px .4px}}
@keyframes breezeB{0%,100%{translate:0 0}52%{translate:-.6px -.8px}}
.reporting,.thoughts{animation:breezeA 8.8s ease-in-out infinite}.opinion,.photography{animation:breezeB 10.4s ease-in-out infinite}.profile{animation:breezeA 12s ease-in-out infinite}.paper:hover,.paper:focus-visible{animation-play-state:paused}

.clock{position:absolute;z-index:20;right:7.2%;top:24.4%;display:grid;width:9.2%;justify-items:center;gap:.45cqw;color:#eadcc8;filter:drop-shadow(0 9px 8px rgb(15 5 2 / .35));transform:rotate(1deg)}
.clock-face{position:relative;width:100%;aspect-ratio:1;border:clamp(4px,.45cqw,7px) solid #3b2b1d;border-radius:50%;background:radial-gradient(circle at 40% 35%,#f2eadc,#d5c3a7 68%,#a58c6b);box-shadow:inset 0 0 0 1px #7b654a,0 3px 0 #24160e}.clock-face i{position:absolute;color:#3a2c21;font:700 clamp(7px,.68cqw,11px)/1 Georgia,serif;font-style:normal}.c12{top:7%;left:50%;transform:translateX(-50%)}.c3{right:8%;top:50%;transform:translateY(-50%)}.c6{bottom:7%;left:50%;transform:translateX(-50%)}.c9{left:8%;top:50%;transform:translateY(-50%)}.hand{position:absolute;z-index:3;left:50%;bottom:50%;display:block;border-radius:99px;background:#30231a;transform-origin:50% 100%}.hour{width:3px;height:24%}.minute{width:2px;height:34%}.second{width:1px;height:39%;background:#a12621}.pin{position:absolute;z-index:5;left:50%;top:50%;width:7px;height:7px;border-radius:50%;background:#312219;transform:translate(-50%,-50%)}.clock small{font:800 clamp(5px,.46cqw,8px)/1 Arial,sans-serif;letter-spacing:.13em;text-transform:uppercase;text-shadow:0 1px 4px #2b160b}

.deskcloth{position:absolute;z-index:4;right:-6%;bottom:-9%;width:29%;height:25%;opacity:.16;transform:rotate(-7deg);background:repeating-linear-gradient(0deg,#eadfc9 0 10px,#183d36 10px 20px),repeating-linear-gradient(90deg,transparent 0 10px,#8c3129 10px 20px);background-blend-mode:multiply;clip-path:polygon(16% 7%,100% 0,100% 100%,0 100%);box-shadow:0 -5px 20px rgb(13 5 1 / .28)}

@media(max-width:1100px){.desk-canvas{min-height:610px}.topnav{gap:18px}.clock{right:6.4%;width:9.5%}}
@media(max-width:850px){.preview-shell{padding:0}.desk-canvas{width:100vw;min-width:820px;border-radius:0}}
@media(prefers-reduced-motion:reduce){.paper{animation:none!important;transition:none!important}}
</style>
</head>
<body>
<div class="preview-shell">
<main class="desk-canvas" aria-label="Interactive desktop portfolio prototype">
  <div class="desk-surface" aria-hidden="true"></div>
  <div class="deskcloth" aria-hidden="true"></div>

  <a class="brand" href="../" aria-label="Arafat Rahaman homepage"><strong>Arafat Rahaman</strong><small>Journalist - Bangladesh</small></a>
  <nav class="topnav" aria-label="Prototype navigation"><a href="../" aria-current="page">Home</a><a href="../about/">About</a><a href="../all-work/">Work</a><a href="../thoughts/">Writing</a><a href="../contact/">Contact</a></nav>

  <span class="object soft obj-laptop" aria-hidden="true"><img src="../assets/home/approved-desk-desktop.webp" alt=""></span>
  <span class="object soft obj-coffee" aria-hidden="true"><img src="../assets/home/approved-desk-desktop.webp" alt=""></span>
  <span class="object soft obj-books" aria-hidden="true"><img src="../assets/home/approved-desk-desktop.webp" alt=""></span>
  <span class="object soft obj-camera" aria-hidden="true"><img src="../assets/home/approved-desk-desktop.webp" alt=""></span>
  <span class="object soft obj-glasses" aria-hidden="true"><img src="../assets/home/approved-desk-desktop.webp" alt=""></span>
  <span class="object soft obj-bottomright" aria-hidden="true"><img src="../assets/home/approved-desk-desktop.webp" alt=""></span>
  <span class="object soft obj-plantleft" aria-hidden="true"><img src="../assets/home/approved-desk-desktop.webp" alt=""></span>

  <a class="paper profile" href="../about/" aria-label="About Arafat Rahaman"><img src="../assets/home/approved-desk-desktop.webp" alt=""></a>
  <a class="paper reporting" href="../reporting/" aria-label="Reporting"><img src="../assets/home/approved-desk-desktop.webp" alt=""></a>
  <a class="paper opinion" href="../opinion/" aria-label="Opinion and Analysis"><img src="../assets/home/approved-desk-desktop.webp" alt=""></a>
  <a class="paper thoughts" href="../thoughts/" aria-label="Thoughts"><img src="../assets/home/approved-desk-desktop.webp" alt=""></a>
  <a class="paper photography" href="../photography/" aria-label="Photography"><img src="../assets/home/approved-desk-desktop.webp" alt=""></a>

  <div class="clock" aria-label="Current time in Dhaka">
    <span class="clock-face"><i class="c12">12</i><i class="c3">3</i><i class="c6">6</i><i class="c9">9</i><b class="hand hour" data-hour></b><b class="hand minute" data-minute></b><b class="hand second" data-second></b><em class="pin"></em></span>
    <small data-clock-label>Dhaka</small>
  </div>
</main>
</div>
<script>
(()=>{const root=document.querySelector('.clock');if(!root)return;const h=root.querySelector('[data-hour]'),m=root.querySelector('[data-minute]'),s=root.querySelector('[data-second]'),label=root.querySelector('[data-clock-label]');const tick=()=>{const parts=new Intl.DateTimeFormat('en-GB',{timeZone:'Asia/Dhaka',hour:'2-digit',minute:'2-digit',second:'2-digit',hour12:false}).formatToParts(new Date());const n=t=>Number(parts.find(p=>p.type===t)?.value||0);const hh=n('hour'),mm=n('minute'),ss=n('second');h.style.transform=`rotate(${(hh%12)*30+mm*.5}deg)`;m.style.transform=`rotate(${mm*6+ss*.1}deg)`;s.style.transform=`rotate(${ss*6}deg)`;label.textContent=`Dhaka - ${String(hh).padStart(2,'0')}:${String(mm).padStart(2,'0')}`};tick();setInterval(tick,1000)})();
</script>
</body>
</html>'''


def main() -> None:
    PREVIEW.parent.mkdir(parents=True, exist_ok=True)
    PREVIEW.write_text(HTML, encoding="utf-8")
    print("Desktop preview rebuilt from independent canvas layers; live homepage untouched")


if __name__ == "__main__":
    main()
