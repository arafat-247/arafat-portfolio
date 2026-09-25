"""Add tactile interaction to the approved photographic desktop homepage.

This is a prototype pass. It keeps the approved desk image and the existing
semantic/clickable hotspots, then overlays aligned image slices, subtle motion,
reactive navigation, a live Dhaka analogue clock and restrained physical detail.
Mobile is untouched.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "dist" / "index.html"
PREVIEW = ROOT / "dist" / "desktop-preview" / "index.html"
STYLE_ID = "desktop-tactile-preview-v1"
SCRIPT_ID = "desktop-tactile-preview-clock-v1"
DESK_IMAGE = "assets/home/approved-desk-desktop.webp"

LAYER = r"""
<div class="desktactile" aria-hidden="true">
  <span class="deskpatch patch-stories"></span>
  <span class="deskpatch patch-centre"></span>
  <span class="deskpatch patch-rightnote"></span>
  <span class="deskpatch patch-leftnote"></span>

  <span class="deskpiece piece-profile"><img src="assets/home/approved-desk-desktop.webp" alt=""></span>
  <span class="deskpiece piece-reporting"><img src="assets/home/approved-desk-desktop.webp" alt=""></span>
  <span class="deskpiece piece-opinion"><img src="assets/home/approved-desk-desktop.webp" alt=""></span>
  <span class="deskpiece piece-thoughts"><img src="assets/home/approved-desk-desktop.webp" alt=""></span>
  <span class="deskpiece piece-photo"><img src="assets/home/approved-desk-desktop.webp" alt=""></span>

  <span class="deskcloth"></span>

  <span class="deskclock-live">
    <span class="deskclock-face">
      <i class="tick t12">12</i><i class="tick t3">3</i><i class="tick t6">6</i><i class="tick t9">9</i>
      <b class="hand hour" data-desk-hour></b>
      <b class="hand minute" data-desk-minute></b>
      <b class="hand second" data-desk-second></b>
      <em></em>
    </span>
    <small data-desk-clock-label>Dhaka</small>
  </span>
</div>
""".strip()

CSS = r"""
@media(min-width:801px){
  .deskstage{isolation:isolate}
  .deskvisual{z-index:0}
  .desktactile{position:absolute;inset:0;z-index:3;pointer-events:none;overflow:hidden}
  .deskhotspots-desktop{z-index:12!important}

  .deskpiece{
    position:absolute;overflow:hidden;
    transform-origin:50% 50%;
    filter:drop-shadow(0 8px 9px rgb(13 5 1 / 0));
    transition:transform .34s cubic-bezier(.2,.72,.2,1),filter .34s ease;
    will-change:transform;
  }
  .deskpiece img{position:absolute;max-width:none!important;user-select:none;-webkit-user-drag:none}

  .piece-profile{left:34.6%;top:4.2%;width:22.7%;height:24.5%;clip-path:polygon(4% 3%,92% 0,100% 91%,8% 100%,0 11%)}
  .piece-profile img{width:440.53%;height:408.17%;left:-152.43%;top:-17.15%}

  .piece-reporting{left:6%;top:36.4%;width:25%;height:31.8%;clip-path:polygon(2% 4%,93% 0,100% 96%,11% 100%,0 11%)}
  .piece-reporting img{width:400%;height:314.47%;left:-24%;top:-114.47%}

  .piece-opinion{left:31.3%;top:36.8%;width:26.5%;height:31.4%;clip-path:polygon(1% 3%,94% 0,100% 94%,7% 100%,0 8%)}
  .piece-opinion img{width:377.36%;height:318.48%;left:-118.12%;top:-117.20%}

  .piece-thoughts{left:57.7%;top:36.5%;width:26.1%;height:31.5%;clip-path:polygon(3% 1%,96% 2%,100% 93%,7% 100%,0 8%)}
  .piece-thoughts img{width:383.15%;height:317.47%;left:-221.08%;top:-115.88%}

  .piece-photo{left:39.1%;top:68%;width:25.4%;height:23%;clip-path:polygon(2% 3%,96% 0,100% 93%,7% 100%,0 8%)}
  .piece-photo img{width:393.71%;height:434.79%;left:-153.94%;top:-295.66%}

  @keyframes deskBreezeA{0%,100%{transform:translate3d(0,0,0) rotate(0)}48%{transform:translate3d(.8px,-1.1px,0) rotate(.08deg)}}
  @keyframes deskBreezeB{0%,100%{transform:translate3d(0,0,0) rotate(0)}52%{transform:translate3d(-.7px,-.8px,0) rotate(-.07deg)}}
  .piece-reporting,.piece-thoughts{animation:deskBreezeA 8.8s ease-in-out infinite}
  .piece-opinion,.piece-photo{animation:deskBreezeB 10.4s ease-in-out infinite}
  .piece-profile{animation:deskBreezeA 12.2s ease-in-out infinite}

  .deskstage:has(.deskprofile-hotspot:is(:hover,:focus-visible)) .piece-profile,
  .deskstage:has(.deskreporting-hotspot:is(:hover,:focus-visible)) .piece-reporting,
  .deskstage:has(.deskopinion-hotspot:is(:hover,:focus-visible)) .piece-opinion,
  .deskstage:has(.deskthoughts-hotspot:is(:hover,:focus-visible)) .piece-thoughts,
  .deskstage:has(.deskphoto-hotspot:is(:hover,:focus-visible)) .piece-photo{
    animation-play-state:paused;
    transform:translate3d(0,-4px,0) rotate(.18deg);
    filter:drop-shadow(0 11px 9px rgb(13 5 1 / 28%));
  }

  .deskhotspot[class*="desknav-"]:before{
    content:"";position:absolute;left:10%;right:10%;bottom:3%;
    height:1px;background:#ead3ad;
    transform:scaleX(0);transform-origin:center;
    transition:transform .2s ease,box-shadow .2s ease;
  }
  .deskhotspot[class*="desknav-"]:hover:before,
  .deskhotspot[class*="desknav-"]:focus-visible:before{
    transform:scaleX(1);box-shadow:0 0 10px rgb(234 211 173 / 72%)
  }
  .deskhotspot[class*="desknav-"]:hover{background:rgb(255 243 220 / 4%)}

  .deskpatch{
    position:absolute;
    background:
      repeating-linear-gradient(3deg,rgb(255 255 255 / 0) 0 9px,rgb(37 13 4 / 8%) 10px 11px),
      linear-gradient(98deg,#3a1d10,#4b2817 48%,#3b1d10);
    box-shadow:inset 0 0 18px rgb(14 5 2 / 28%);
    opacity:.96;
    mask-image:radial-gradient(ellipse at center,#000 63%,transparent 100%);
    -webkit-mask-image:radial-gradient(ellipse at center,#000 63%,transparent 100%);
  }
  .patch-stories{left:25.6%;top:9.2%;width:12.4%;height:14.8%;transform:rotate(-1deg)}
  .patch-centre{left:29.8%;top:27.2%;width:35.2%;height:10.2%}
  .patch-rightnote{left:76.3%;top:22.8%;width:14.1%;height:15.2%;transform:rotate(2deg)}
  .patch-leftnote{left:3.2%;top:78.6%;width:14.4%;height:15.5%;transform:rotate(-2deg)}

  .deskcloth{
    position:absolute;right:-3%;bottom:-4%;width:28%;height:23%;
    opacity:.18;transform:rotate(-7deg);
    background:
      repeating-linear-gradient(0deg,#e8dfcc 0 9px,#183d36 9px 18px),
      repeating-linear-gradient(90deg,transparent 0 9px,#8c3129 9px 18px);
    background-blend-mode:multiply;
    box-shadow:0 -5px 18px rgb(15 6 2 / 26%);
    clip-path:polygon(17% 8%,100% 0,100% 100%,0 100%);
  }

  .deskclock-live{
    position:absolute;z-index:6;right:4.8%;top:27.8%;width:8.3%;
    display:grid;justify-items:center;gap:5px;color:#eadcc6;
    filter:drop-shadow(0 7px 8px rgb(12 5 2 / 35%));
  }
  .deskclock-face{
    position:relative;display:block;width:100%;aspect-ratio:1;
    border:clamp(3px,.35vw,6px) solid #3a2a1d;border-radius:50%;
    background:radial-gradient(circle at 42% 37%,#f0e6d4,#cdbb9f 72%,#9f896d);
    box-shadow:inset 0 0 0 1px #806a4f,0 3px 0 #2b1b11;
  }
  .deskclock-face .tick{position:absolute;color:#3b2d21;font:700 clamp(6px,.55vw,10px)/1 Georgia,serif;font-style:normal}
  .deskclock-face .t12{top:7%;left:50%;transform:translateX(-50%)}
  .deskclock-face .t3{right:8%;top:50%;transform:translateY(-50%)}
  .deskclock-face .t6{bottom:7%;left:50%;transform:translateX(-50%)}
  .deskclock-face .t9{left:8%;top:50%;transform:translateY(-50%)}
  .deskclock-face .hand{position:absolute;z-index:3;left:50%;bottom:50%;display:block;border-radius:99px;background:#33261d;transform-origin:50% 100%}
  .deskclock-face .hour{width:3px;height:24%}
  .deskclock-face .minute{width:2px;height:34%}
  .deskclock-face .second{width:1px;height:38%;background:#a62d25}
  .deskclock-face em{position:absolute;z-index:5;left:50%;top:50%;width:6px;height:6px;border-radius:50%;background:#35271d;transform:translate(-50%,-50%)}
  .deskclock-live small{font:800 clamp(5px,.43vw,8px)/1 var(--sans);letter-spacing:.13em;text-transform:uppercase;text-shadow:0 1px 4px #2b160b}

  @media(max-width:1080px){
    .deskclock-live{right:3.6%;width:8.8%}
    .patch-centre{width:34.5%}
  }
}
@media(max-width:800px){.desktactile{display:none!important}}
@media(prefers-reduced-motion:reduce){
  .deskpiece{animation:none!important;transition:none!important}
}
""".strip()

JS = r"""
(()=> {
  const root=document.querySelector('.deskclock-live');
  if(!root) return;
  const hour=root.querySelector('[data-desk-hour]');
  const minute=root.querySelector('[data-desk-minute]');
  const second=root.querySelector('[data-desk-second]');
  const label=root.querySelector('[data-desk-clock-label]');
  const tick=()=> {
    const parts=new Intl.DateTimeFormat('en-GB',{
      timeZone:'Asia/Dhaka',hour:'2-digit',minute:'2-digit',second:'2-digit',hour12:false
    }).formatToParts(new Date());
    const n=(type)=>Number(parts.find(p=>p.type===type)?.value||0);
    const h=n('hour'),m=n('minute'),s=n('second');
    hour.style.transform=`rotate(${(h%12)*30+m*.5}deg)`;
    minute.style.transform=`rotate(${m*6+s*.1}deg)`;
    second.style.transform=`rotate(${s*6}deg)`;
    label.textContent=`Dhaka · ${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}`;
  };
  tick();
  setInterval(tick,1000);
})();
""".strip()

def main() -> None:
    if not SOURCE.is_file():
        raise FileNotFoundError("dist/index.html does not exist; run the build first")

    source=SOURCE.read_text(encoding="utf-8")
    if 'class="deskhome deskhome-photo"' not in source or DESK_IMAGE not in source:
        raise RuntimeError("Approved photographic desktop homepage was not found")

    picture=re.compile(r'(<picture class="deskvisual"[^>]*>.*?</picture>)',re.I|re.S)
    source,count=picture.subn(r'\1'+LAYER,source,count=1)
    if count!=1:
        raise RuntimeError("Could not attach tactile layer to approved desk image")

    source=source.replace(
        "<head>",
        '<head><base href="../"><meta name="robots" content="noindex,nofollow">'
        '<meta name="description" content="Desktop interaction prototype for review.">',
        1,
    )
    source=source.replace(
        "</head>",
        f'<style id="{STYLE_ID}">\n{CSS}\n</style></head>',
        1,
    )
    source=source.replace(
        "</body>",
        f'<script id="{SCRIPT_ID}">\n{JS}\n</script></body>',
        1,
    )
    source=source.replace(
        "<title>Arafat Rahaman — Journalist at The Daily Star</title>",
        "<title>Desktop prototype — Arafat Rahaman</title>",
        1,
    )

    PREVIEW.parent.mkdir(parents=True,exist_ok=True)
    PREVIEW.write_text(source,encoding="utf-8")
    print("Desktop preview built: /desktop-preview/; live homepage untouched")

if __name__=="__main__":
    main()
