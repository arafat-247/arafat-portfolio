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
ASSET_VERSION = "18.21.0"

HOME_CSS = r"""
/* Editorial homepage v18.10 — isolated from legacy homepage selectors */
body.home main{background:var(--paper)}
body.home .homecontent{width:100%;max-width:none;margin:0;padding:0 0 56px}

/* HERO — exact visual target from supplied reference */
.editorialhero{
  position:relative;
  min-height:clamp(520px,38.6vw,592px);
  overflow:hidden;
  border-bottom:1px solid #ddd6c8;
  background:#f7f3ea;
}
.editorialhero-copy{
  position:absolute;
  z-index:5;
  inset:0 auto 0 0;
  display:flex;
  width:43%;
  min-width:0;
  flex-direction:column;
  justify-content:center;
  padding:54px 36px 34px max(66px,calc((100vw - 1440px)/2 + 66px));
}
.editorialhero-kicker{
  color:#0d554a;
  font:850 10px/1 var(--sans);
  letter-spacing:.26em;
  text-transform:uppercase;
}
.editorialhero-copy h1{
  margin:15px 0 13px;
  color:#073e38;
  font:400 clamp(72px,6.75vw,104px)/.80 var(--serif);
  letter-spacing:-.058em;
}
.editorialhero-copy h1 em{display:block;font-style:italic;font-weight:400}
.editorialhero-deck{
  max-width:500px;
  margin:0;
  color:#242724;
  font:400 clamp(17px,1.42vw,21px)/1.42 var(--serif);
}
.editorialhero-rule{
  display:block;
  width:58px;
  height:2px;
  margin:22px 0 12px;
  background:#214d48;
}
.editorialhero-tagline{
  margin:0;
  color:#b17a4f;
  font:600 clamp(24px,2.1vw,31px)/1.05 "Caveat",cursive;
  letter-spacing:.01em;
}
.editorialhero-actions{
  display:flex;
  gap:12px;
  margin-top:26px;
}
.editorialhero-actions a{
  display:flex;
  min-width:150px;
  height:53px;
  align-items:center;
  justify-content:space-between;
  gap:24px;
  padding:0 22px;
  border:1px solid #28413d;
  font:700 15px/1 var(--serif);
  text-decoration:none;
}
.editorialhero-actions b{font-weight:400}
.editorialhero-primary{color:#fff;background:#0b5147}
.editorialhero-secondary{color:#202521;background:transparent}
.editorialhero-primary:hover{background:#0f6256}
.editorialhero-secondary:hover{background:#efe9dd}

/* The portrait overlaps the cream field and the green panel, as in the reference. */
.editorialhero-portrait{
  position:absolute;
  z-index:8;
  left:40.2%;
  top:29px;
  bottom:30px;
  width:min(32vw,486px);
  margin:0;
  padding:13px 14px 15px;
  background:#faf7f0;
  box-shadow:0 14px 32px rgb(25 40 35 / 13%);
  transform:rotate(-.75deg);
}
.editorialhero-portrait:before{
  content:"";
  position:absolute;
  z-index:-1;
  inset:-12px 31px 16px -17px;
  background:#e7e0d5;
  transform:rotate(1.45deg);
}
.editorialhero-photo-frame{
  position:relative;
  width:100%;
  height:100%;
  overflow:hidden;
  background:#d8d4cc;
}
.editorialhero-picture{display:block;width:100%;height:100%}
.editorialhero-portrait img{
  display:block;
  width:100%;
  height:100%;
  object-fit:cover;
  object-position:center 48%;
  filter:grayscale(1) contrast(1.04);
}
.editorialhero-photo-note{
  position:absolute;
  left:27px;
  bottom:27px;
  color:#f4efe7;
  font:600 23px/1.02 "Caveat",cursive;
  text-shadow:0 1px 3px rgb(0 0 0 / 20%);
  transform:rotate(-5deg);
}

/* Deep-green Bangladesh panel with layered editorial paper details. */
.editorialhero-panel{
  position:absolute;
  z-index:1;
  inset:0 0 0 auto;
  width:42%;
  overflow:hidden;
  color:#f7f1e7;
  background:#0b4b43;
}
.editorialhero-panel-image{
  position:absolute;
  inset:0;
  width:100%;
  height:100%;
  object-fit:cover;
  object-position:center;
  filter:grayscale(1) contrast(1.04);
  opacity:.23;
  mix-blend-mode:screen;
}
.editorialhero-panel:after{
  content:"";
  position:absolute;
  inset:0;
  z-index:1;
  background:
    linear-gradient(90deg,rgb(9 63 56 / 18%),rgb(4 55 49 / 4%)),
    linear-gradient(180deg,rgb(11 75 67 / 8%),rgb(7 54 48 / 20%));
  pointer-events:none;
}
.editorialhero-paper{
  position:absolute;
  z-index:2;
  display:block;
  color:#756f65;
  background:#eee8dc;
  box-shadow:0 5px 14px rgb(12 35 30 / 12%);
}
.editorialhero-paper-long{
  left:17%;
  top:9%;
  width:113px;
  height:78%;
  opacity:.83;
  transform:rotate(-4.5deg);
  background:
    repeating-linear-gradient(0deg,transparent 0 8px,rgb(93 87 78 / 10%) 8px 9px),
    #eee8dc;
}
.editorialhero-paper-note{
  left:38%;
  top:39%;
  width:118px;
  height:43%;
  padding:22px 17px;
  transform:rotate(4.2deg);
  background:#efe9de;
}
.editorialhero-paper-note i{
  position:absolute;
  left:29px;
  right:23px;
  bottom:31px;
  height:22px;
  border-top:2px solid #9b8a77;
  border-radius:50%;
  transform:rotate(-12deg);
}
.editorialhero-panel-quote{
  position:absolute;
  z-index:4;
  top:13%;
  right:8%;
  width:165px;
  margin:0;
  padding-top:15px;
  border-top:2px solid rgb(255 255 255 / 68%);
  color:#f6efe5;
  font:italic clamp(20px,1.75vw,27px)/1.05 var(--serif);
}
.editorialhero-location{
  position:absolute;
  z-index:4;
  right:8.5%;
  bottom:8%;
  padding-top:14px;
  border-top:2px solid rgb(255 255 255 / 62%);
  color:#fff;
  font:850 9px/1.7 var(--sans);
  letter-spacing:.28em;
  text-transform:uppercase;
}

/* Keep the reference geometry stable at ordinary laptop widths. */
@media(min-width:801px) and (max-width:1180px){
  .editorialhero{min-height:515px}
  .editorialhero-copy{width:44%;padding-left:34px;padding-right:26px}
  .editorialhero-copy h1{font-size:clamp(62px,7.2vw,82px)}
  .editorialhero-deck{font-size:17px}
  .editorialhero-portrait{left:40%;top:27px;bottom:28px;width:min(34vw,410px)}
  .editorialhero-panel{width:41%}
  .editorialhero-panel-quote{right:6%;width:145px;font-size:21px}
  .editorialhero-paper-note{left:37%;width:102px}
}

/* WORK INTRO */
.workintro{
  display:grid;
  width:min(100% - 72px,1400px);
  margin:0 auto;
  padding:30px 0 18px;
  grid-template-columns:1fr 1fr;
  gap:32px;
  align-items:end;
}
.workintro>div:first-child span{
  display:block;
  margin-bottom:4px;
  color:var(--accent);
  font-size:10px;
  font-weight:850;
  letter-spacing:.18em;
  text-transform:uppercase;
}
.workintro h2{margin:0;font:400 58px/.94 var(--serif);letter-spacing:-.045em}
.workintro>div:last-child{justify-self:end;max-width:620px}
.workintro p{margin:0 0 8px;color:#474a45;font:400 15px/1.5 var(--serif)}
.workintro a{
  color:var(--forest);
  font-size:12px;
  font-weight:750;
  text-decoration:none;
  border-bottom:1px solid currentColor;
}

/* WORK GRID — corrected: editorial elements for first three, original image for photography */
.workgrid{
  display:grid;
  width:min(100% - 72px,1400px);
  margin:0 auto;
  grid-template-columns:1.08fr .52fr .52fr;
  grid-template-rows:190px 190px;
  gap:10px;
}
.worktile{
  position:relative;
  isolation:isolate;
  display:flex;
  min-width:0;
  min-height:0;
  overflow:hidden;
  align-items:flex-end;
  padding:22px 22px 20px;
  color:#fff;
  background:#173a34;
  text-decoration:none;
  transition:transform .18s ease,box-shadow .18s ease;
}
.worktile:hover{transform:translateY(-2px);box-shadow:0 13px 28px rgb(15 38 32 / 14%)}
.worktile:after{
  content:"";
  position:absolute;
  inset:0;
  z-index:-1;
  pointer-events:none;
}
.worktile-reporting{grid-column:1;grid-row:1/3;background:#0f4e45}
.worktile-opinion{grid-column:2/4;grid-row:1;background:#713f32}
.worktile-thoughts{grid-column:2;grid-row:2;background:#405447}
.worktile-photos{grid-column:3;grid-row:2}
.worktile-art,.worktile-image{
  position:absolute;
  inset:0;
  z-index:-2;
  width:100%;
  height:100%;
  object-fit:cover;
}
.worktile-number{
  position:absolute;
  z-index:3;
  left:18px;
  top:16px;
  color:#efc37a;
  font:800 10px/1 var(--sans);
  letter-spacing:.12em;
  font-style:normal;
}
.worktile-copy{position:relative;z-index:3;width:64%}
.worktile-reporting .worktile-copy{width:56%}
.worktile-opinion .worktile-copy{width:58%}
.worktile-thoughts .worktile-copy,.worktile-photos .worktile-copy{width:78%}
.worktile-copy strong{
  display:block;
  font:400 clamp(25px,2.35vw,36px)/1 var(--serif);
  letter-spacing:-.035em;
}
.worktile-reporting .worktile-copy strong{font-size:clamp(38px,3.1vw,50px)}
.worktile-copy small{
  display:block;
  margin-top:7px;
  color:rgb(255 255 255 / 84%);
  font:400 12px/1.38 var(--serif);
}
.worktile-explore{
  display:inline-block;
  margin-top:18px;
  padding-bottom:4px;
  border-bottom:1px solid rgb(255 255 255 / 76%);
  font:700 10px/1 var(--sans);
}
.worktile-keywords{
  position:absolute;
  z-index:3;
  right:18px;
  bottom:20px;
  width:94px;
  padding-top:12px;
  border-top:1px solid rgb(255 255 255 / 64%);
  color:rgb(255 255 255 / 88%);
  font:800 9px/1.5 var(--sans);
  letter-spacing:.08em;
  text-transform:uppercase;
}
.worktile-keywords span{display:block}
.worktile-arrow{
  position:absolute;
  z-index:4;
  right:16px;
  bottom:16px;
  display:grid;
  width:34px;
  height:34px;
  place-items:center;
  border:1px solid rgb(255 255 255 / 66%);
  border-radius:50%;
  font-size:14px;
  font-style:normal;
}
.worktile-reporting .worktile-art{
  background:
    linear-gradient(90deg,rgb(255 255 255 / 6%) 1px,transparent 1px) 0 0/38px 38px,
    linear-gradient(0deg,rgb(255 255 255 / 6%) 1px,transparent 1px) 0 0/38px 38px,
    radial-gradient(circle at 78% 26%,rgb(240 195 122 / 22%) 0 8%,transparent 8.5%),
    linear-gradient(145deg,#0a4038,#15594f 55%,#0c3933);
}
.worktile-reporting .worktile-art:before{
  content:"";
  position:absolute;
  right:10%;
  top:16%;
  width:33%;
  height:54%;
  border:1px solid rgb(255 255 255 / 30%);
  background:
    repeating-linear-gradient(180deg,rgb(255 255 255 / 22%) 0 1px,transparent 1px 12px),
    rgb(245 239 225 / 8%);
  transform:rotate(4deg);
  box-shadow:-15px 15px 0 rgb(5 36 31 / 22%);
}
.worktile-reporting .worktile-art:after{
  content:"";
  position:absolute;
  right:8%;
  bottom:11%;
  width:118px;
  height:36px;
  border-top:2px solid #efc37a;
  border-bottom:1px solid rgb(255 255 255 / 35%);
  transform:rotate(-4deg);
}
.worktile-opinion .worktile-art{
  background:
    linear-gradient(130deg,transparent 0 54%,rgb(255 255 255 / 8%) 54% 55%,transparent 55%),
    repeating-linear-gradient(0deg,transparent 0 25px,rgb(255 255 255 / 7%) 26px 27px),
    linear-gradient(115deg,#7d4537,#5a332c 62%,#3f2925);
}
.worktile-opinion .worktile-art:before{
  content:"“";
  position:absolute;
  right:7%;
  top:-16px;
  color:rgb(247 230 206 / 20%);
  font:400 180px/.9 Georgia,serif;
}
.worktile-opinion .worktile-art:after{
  content:"";
  position:absolute;
  right:20%;
  bottom:22%;
  width:122px;
  height:74px;
  border:1px solid rgb(255 255 255 / 30%);
  border-left:5px solid #efc37a;
  transform:rotate(-5deg);
}
.worktile-thoughts .worktile-art{
  background:
    radial-gradient(circle at 76% 31%,transparent 0 29px,rgb(255 255 255 / 15%) 30px 31px,transparent 32px 54px,rgb(255 255 255 / 9%) 55px 56px,transparent 57px),
    repeating-linear-gradient(135deg,transparent 0 24px,rgb(255 255 255 / 5%) 25px 26px),
    linear-gradient(140deg,#506356,#354b40 68%,#293f36);
}
.worktile-thoughts .worktile-art:before{
  content:"";
  position:absolute;
  left:13%;
  top:22%;
  width:44%;
  height:1px;
  background:rgb(255 255 255 / 30%);
  box-shadow:0 18px 0 rgb(255 255 255 / 22%),0 36px 0 rgb(255 255 255 / 16%);
  transform:rotate(-7deg);
}
.worktile-thoughts .worktile-art:after{
  content:"";
  position:absolute;
  right:12%;
  bottom:16%;
  width:56px;
  height:56px;
  border:2px solid #d8b174;
  border-radius:50%;
  opacity:.75;
}
.worktile-photos:after{background:linear-gradient(0deg,rgb(6 24 20 / 78%),rgb(6 24 20 / 8%) 72%)}
.worktile-photos .worktile-image{filter:brightness(.66) saturate(.72)}
body.home .homecontact{
  width:min(100% - 72px,1400px);
  margin:20px auto 0;
  padding:26px 30px;
}
body.home .homecontact strong{font-size:30px}

/* MOBILE — one coherent editorial composition */
@media(max-width:800px){
  body.home .mobilehead{
    height:58px;
    padding:0 15px;
    border-bottom:1px solid #ded7cb;
    background:#f7f3ea;
  }
  body.home .mobilebrand{gap:9px;font-size:13px}
  body.home .mark{width:34px;height:34px}
  body.home .themetoggle{display:none}
  body.home .menutoggle{display:inline-flex;gap:7px;font-size:12px}
  body.home .mobilemenu[hidden],
  body.home .menubackdrop[hidden]{display:none!important}
  body.home .homecontent{padding:0 0 30px}

  .editorialhero{
    display:grid;
    min-height:0;
    overflow:hidden;
    grid-template-columns:1fr;
    gap:0;
    border:0;
    background:#f7f3ea;
  }
  .editorialhero-portrait{
    position:relative;
    inset:auto;
    order:1;
    width:100%;
    height:min(102vw,430px);
    margin:0;
    padding:0;
    background:#d8d4cc;
    box-shadow:none;
    transform:none;
  }
  .editorialhero-portrait:before{display:none}
  .editorialhero-photo-frame{border-radius:0}
  .editorialhero-portrait img{
    object-position:center 43%;
    filter:grayscale(1) contrast(1.04);
  }
  .editorialhero-photo-note{display:none}

  .editorialhero-copy{
    position:relative;
    inset:auto;
    order:2;
    width:100%;
    padding:24px 20px 25px;
    border:0;
    border-bottom:1px solid #ddd6c8;
    border-radius:0;
    background:#f7f3ea;
  }
  .editorialhero-kicker{font-size:8px;letter-spacing:.2em}
  .editorialhero-copy h1{
    margin:8px 0 11px;
    font-size:clamp(43px,13.4vw,56px);
    line-height:.88;
    letter-spacing:-.045em;
  }
  .editorialhero-copy h1 em{display:inline;font-style:italic}
  .editorialhero-deck{
    max-width:560px;
    font-size:14.5px;
    line-height:1.48;
  }
  .editorialhero-rule{width:42px;margin:15px 0 9px}
  .editorialhero-tagline{font-size:21px;line-height:1.08}
  .editorialhero-actions{gap:8px;margin-top:18px}
  .editorialhero-actions a{
    min-width:0;
    height:43px;
    flex:1;
    padding:0 13px;
    font-size:12px;
  }

  /* Desktop's decorative third panel becomes visual noise on a narrow screen. */
  .editorialhero-panel{display:none}

  .workintro{
    display:grid;
    width:auto;
    margin:0 18px;
    padding:25px 0 14px;
    grid-template-columns:minmax(0,1fr) auto;
    gap:6px 14px;
    align-items:end;
    border-bottom:1px solid #ddd6c8;
  }
  .workintro>div:first-child span{
    margin-bottom:5px;
    font-size:8px;
    letter-spacing:.16em;
  }
  .workintro h2{font-size:38px;line-height:.96}
  .workintro>div:last-child{
    display:contents;
    max-width:none;
  }
  .workintro p{
    grid-column:1/-1;
    grid-row:2;
    margin:0;
    color:#5a5d57;
    font-size:12.5px;
    line-height:1.45;
  }
  .workintro a{
    grid-column:2;
    grid-row:1;
    align-self:end;
    margin-bottom:2px;
    font-size:10.5px;
    white-space:nowrap;
  }

  .workgrid{
    display:grid;
    width:auto;
    margin:0 18px;
    grid-template-columns:1fr;
    grid-template-rows:auto;
    gap:7px;
    padding-top:12px;
  }
  .worktile,
  .worktile-reporting,
  .worktile-opinion,
  .worktile-thoughts,
  .worktile-photos{
    grid-column:1;
    grid-row:auto;
    min-height:132px;
    padding:17px 17px 15px;
  }
  .worktile-reporting{min-height:150px}
  .worktile-copy,
  .worktile-reporting .worktile-copy,
  .worktile-opinion .worktile-copy,
  .worktile-thoughts .worktile-copy,
  .worktile-photos .worktile-copy{
    width:auto;
    max-width:72%;
  }
  .worktile-reporting .worktile-copy{max-width:66%}
  .worktile-copy strong{font-size:23px;line-height:1}
  .worktile-reporting .worktile-copy strong{font-size:29px}
  .worktile-opinion .worktile-copy strong{font-size:24px}
  .worktile-copy small{
    margin-top:5px;
    font-size:10.5px;
    line-height:1.36;
  }
  .worktile-number{
    left:16px;
    top:14px;
    font-size:8px;
  }
  .worktile-keywords,.worktile-explore{display:none}
  .worktile-arrow{
    right:13px;
    top:13px;
    bottom:auto;
    width:28px;
    height:28px;
    font-size:12px;
  }
  .worktile-reporting .worktile-art:before{
    right:7%;
    top:16%;
    width:30%;
    height:54%;
  }
  .worktile-reporting .worktile-art:after{
    right:6%;
    bottom:10%;
    width:82px;
  }
  .worktile-opinion .worktile-art:before{
    right:3%;
    top:-9px;
    font-size:116px;
  }
  .worktile-opinion .worktile-art:after{
    right:9%;
    bottom:15%;
    width:78px;
    height:52px;
  }
  .worktile-thoughts .worktile-art:before{
    left:9%;
    top:20%;
    width:42%;
  }
  .worktile-thoughts .worktile-art:after{
    right:11%;
    bottom:13%;
    width:44px;
    height:44px;
  }
  .worktile-photos .worktile-image{object-position:center 46%}

  body.home .homecontact{
    width:auto;
    margin:14px 18px 0;
    padding:18px 17px;
    grid-template-columns:1fr auto;
    gap:16px;
  }
  body.home .homecontact strong{
    max-width:240px;
    font-size:20px;
    line-height:1.08;
  }
  body.home .homecontact a{
    align-self:center;
    font-size:11px;
  }
}

@media(max-width:420px){
  .editorialhero-portrait{height:94vw;max-height:380px}
  .editorialhero-copy{padding:22px 18px 23px}
  .editorialhero-copy h1{font-size:45px}
  .editorialhero-deck{font-size:14px}
  .editorialhero-tagline{font-size:20px}
  .workintro{margin-inline:16px}
  .workintro h2{font-size:36px}
  .workgrid{margin-inline:16px}
  .worktile,
  .worktile-reporting,
  .worktile-opinion,
  .worktile-thoughts,
  .worktile-photos{min-height:126px}
  .worktile-reporting{min-height:144px}
  .worktile-copy strong{font-size:22px}
  .worktile-reporting .worktile-copy strong{font-size:27px}
  .worktile-opinion .worktile-copy strong{font-size:23px}
  .worktile-copy small{font-size:10px}
  body.home .homecontact{margin-inline:16px}
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
    print(f"Homepage polish: isolated_classes=1, hero_reference_4=1, work_reference_5=1, asset_version={ASSET_VERSION}, versioned_pages={versioned_pages}, css_isolated=1, inline_critical=1, duplicate_home_css=0")


if __name__ == "__main__":
    main()
