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
ASSET_VERSION = "18.11.0"

HOME_CSS = r"""
/* Editorial homepage v18.10 — isolated from legacy homepage selectors */
body.home main{background:var(--paper)}
body.home .homecontent{width:100%;max-width:none;margin:0;padding:0 0 56px}

/* HERO — reference 4 */
.editorialhero{
  position:relative;
  display:grid;
  grid-template-columns:minmax(350px,.92fr) minmax(430px,1fr) minmax(300px,.72fr);
  min-height:560px;
  overflow:hidden;
  border-bottom:1px solid var(--line);
  background:#f4efe6;
}
.editorialhero-copy{
  display:flex;
  flex-direction:column;
  justify-content:center;
  padding:58px 36px 42px max(56px,calc((100vw - 1400px)/2 + 34px));
}
.editorialhero-copy>span{
  color:#0d554a;
  font-size:10px;
  font-weight:850;
  letter-spacing:.24em;
  text-transform:uppercase;
}
.editorialhero-copy h1{
  margin:13px 0 15px;
  color:#0c4b42;
  font:400 clamp(68px,6.45vw,106px)/.79 var(--serif);
  letter-spacing:-.055em;
}
.editorialhero-copy h1 em{display:block;font-style:italic;font-weight:400}
.editorialhero-copy>p:not(.editorialhero-tagline){
  max-width:520px;
  margin:0;
  color:#2f332f;
  font:400 19px/1.48 var(--serif);
}
.editorialhero-copy nav{display:flex;gap:38px;margin-top:18px}
.editorialhero-copy nav a{
  padding-bottom:5px;
  border-bottom:1px solid #0c4b42;
  color:#0c4b42;
  font:700 13px/1 var(--serif);
  text-decoration:none;
}
.editorialhero-tagline{
  margin:24px 0 0;
  color:#b17149;
  font:italic 25px/1.18 var(--serif);
}
.editorialhero-portrait{
  position:relative;
  align-self:center;
  width:min(100%,480px);
  margin:0 auto;
  padding:12px;
  background:#faf7f0;
  box-shadow:0 14px 34px rgb(18 38 32 / 12%);
  transform:rotate(-1deg);
  z-index:3;
}
.editorialhero-portrait:before{
  content:"";
  position:absolute;
  z-index:-1;
  inset:-12px 28px 14px -18px;
  background:#e7e0d5;
  transform:rotate(1.5deg);
}
.editorialhero-portrait img{
  display:block;
  width:100%;
  aspect-ratio:1/1;
  object-fit:cover;
  object-position:center 48%;
  filter:grayscale(1) contrast(1.02);
}
.editorialhero-panel{
  position:relative;
  overflow:hidden;
  min-height:560px;
  background:#f1ede5;
}
.editorialhero-panel img{
  position:absolute;
  inset:0;
  width:100%;
  height:100%;
  object-fit:cover;
  filter:grayscale(1) sepia(.08) saturate(.25) brightness(1.42);
  opacity:.30;
}
.editorialhero-panel:after{
  content:"";
  position:absolute;
  inset:0;
  background:linear-gradient(180deg,rgb(245 241 232 / 62%),rgb(245 241 232 / 28%));
  pointer-events:none;
}
.editorialhero-panel p{
  position:absolute;
  z-index:2;
  left:44px;
  top:74px;
  width:188px;
  margin:0;
  padding-top:16px;
  border-top:2px solid #315f57;
  color:#0d4f45;
  font:italic 27px/1.08 var(--serif);
}
.editorialhero-panel>span{
  position:absolute;
  z-index:2;
  right:34px;
  bottom:42px;
  color:#6b756f;
  font:italic 17px/1.18 var(--serif);
  text-align:right;
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

/* WORK GRID — reference 5 */
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
  background:linear-gradient(0deg,rgb(6 24 20 / 78%),rgb(6 24 20 / 8%) 72%);
}
.worktile-reporting{grid-column:1;grid-row:1/3}
.worktile-opinion{grid-column:2/4;grid-row:1}
.worktile-thoughts{grid-column:2;grid-row:2}
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
  z-index:2;
  left:18px;
  top:16px;
  color:#efc37a;
  font:800 10px/1 var(--sans);
  letter-spacing:.12em;
  font-style:normal;
}
.worktile-copy{position:relative;z-index:2;width:64%}
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
  z-index:2;
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
  z-index:3;
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
    linear-gradient(0deg,rgb(5 47 40 / 36%),rgb(5 47 40 / 15%)),
    url("assets/photography/Rajshahi University-nightscape-Journalist-Arafat-Rahaman (2).webp") center/cover;
}
.worktile-opinion .worktile-art{
  background:
    linear-gradient(0deg,rgb(111 44 31 / 50%),rgb(111 44 31 / 36%)),
    url("assets/photography/Rajshahi University-nightscape-Journalist-Arafat-Rahaman (4).webp") center/cover;
}
.worktile-thoughts .worktile-art{
  background:
    linear-gradient(0deg,rgb(47 70 43 / 42%),rgb(47 70 43 / 24%)),
    url("assets/photography/Rajshahi University-nightscape-Journalist-Arafat-Rahaman (1).webp") center/cover;
}
.worktile-photos .worktile-image{filter:brightness(.66) saturate(.72)}
body.home .homecontact{
  width:min(100% - 72px,1400px);
  margin:20px auto 0;
  padding:26px 30px;
}
body.home .homecontact strong{font-size:30px}

/* MOBILE */
@media(max-width:800px){
  body.home .mobilehead{height:64px;padding:0 18px}
  body.home .mobilebrand{gap:10px}
  body.home .mark{width:39px;height:39px}
  body.home .themetoggle{display:none}
  body.home .menutoggle{display:inline-flex}
  body.home .mobilemenu[hidden],
  body.home .menubackdrop[hidden]{display:none!important}

  body.home .homecontent{padding:16px 14px 42px}

  .editorialhero{
    display:block;
    min-height:0;
    border:0;
    background:transparent;
  }
  .editorialhero-portrait{
    position:relative;
    width:100%;
    margin:0;
    padding:0;
    transform:none;
    box-shadow:none;
    background:#d8d3ca;
  }
  .editorialhero-portrait:before{display:none}
  .editorialhero-portrait img{
    width:100%;
    height:auto;
    aspect-ratio:1/1;
    object-fit:cover;
    object-position:center;
  }
  .editorialhero-copy{
    position:absolute;
    z-index:4;
    left:18px;
    right:18px;
    bottom:18px;
    display:block;
    padding:18px;
    color:#fff;
    background:rgb(8 55 48 / 92%);
    backdrop-filter:blur(3px);
  }
  .editorialhero-copy>span{color:#efb29d;font-size:8px;letter-spacing:.15em}
  .editorialhero-copy h1{
    margin:6px 0 8px;
    color:#fff;
    font:400 35px/.95 var(--serif);
    letter-spacing:-.035em;
  }
  .editorialhero-copy h1 em{display:inline;font-style:normal}
  .editorialhero-copy>p:not(.editorialhero-tagline){
    color:rgb(255 255 255 / 84%);
    font:400 12px/1.42 var(--sans);
  }
  .editorialhero-copy nav{gap:22px;margin-top:12px}
  .editorialhero-copy nav a{color:#fff;border-color:#fff;font-size:10px}
  .editorialhero-tagline{display:none}
  .editorialhero-panel{display:none}

  .workintro{
    width:100%;
    grid-template-columns:1fr;
    gap:7px;
    padding:24px 0 17px;
  }
  .workintro h2{font-size:46px}
  .workintro>div:last-child{justify-self:start}
  .workintro p{font-size:14px}

  .workgrid{
    width:100%;
    grid-template-columns:1fr 1fr;
    grid-template-rows:auto;
    gap:8px;
  }
  .worktile{padding:16px;min-height:150px}
  .worktile-reporting{grid-column:1/-1;grid-row:auto;min-height:196px}
  .worktile-opinion{grid-column:1/-1;grid-row:auto;min-height:170px}
  .worktile-thoughts{grid-column:1;grid-row:auto;min-height:152px}
  .worktile-photos{grid-column:2;grid-row:auto;min-height:152px}
  .worktile-copy,
  .worktile-reporting .worktile-copy,
  .worktile-opinion .worktile-copy,
  .worktile-thoughts .worktile-copy,
  .worktile-photos .worktile-copy{width:auto}
  .worktile-copy strong{font-size:22px}
  .worktile-copy small{font-size:10.5px}
  .worktile-number,.worktile-keywords,.worktile-explore{display:none}
  .worktile-arrow{
    right:12px;
    top:12px;
    bottom:auto;
    width:auto;
    height:auto;
    border:0;
  }

  body.home .homecontact{width:100%;margin-top:18px;padding:23px}
  body.home .homecontact strong{font-size:28px}
}

@media(max-width:420px){
  .editorialhero-copy{left:14px;right:14px;bottom:14px;padding:16px}
  .editorialhero-copy h1{font-size:32px}
  .workintro h2{font-size:43px}
  .worktile-reporting{min-height:184px}
  .worktile-opinion{min-height:164px}
  .worktile-thoughts,.worktile-photos{min-height:146px}
}

/* Final homepage composition v18.11 */
@media(min-width:801px){
  .editorialhero{
    grid-template-columns:minmax(330px,.88fr) minmax(390px,.94fr) minmax(250px,.58fr);
    min-height:500px;
  }
  .editorialhero-copy{
    justify-content:flex-start;
    padding:58px 34px 34px max(54px,calc((100vw - 1400px)/2 + 34px));
  }
  .editorialhero-copy h1{
    margin-top:10px;
    font-size:clamp(60px,5.7vw,90px);
    line-height:.82;
  }
  .editorialhero-copy>p:not(.editorialhero-tagline){
    max-width:470px;
    font-size:17px;
    line-height:1.45;
  }
  .editorialhero-copy nav{margin-top:16px}
  .editorialhero-tagline{margin-top:20px;font-size:22px}
  .editorialhero-portrait{width:min(100%,425px)}
  .editorialhero-panel{min-height:500px}
  .editorialhero-panel p{left:34px;top:62px;width:165px;font-size:23px}
  .editorialhero-panel>span{right:26px;bottom:28px;font-size:14px}
  .workintro{padding-top:26px}
  .workgrid{grid-template-rows:178px 178px}
  body.home .homecontact{margin-top:16px}
}
@media(max-width:800px){
  body.home .homecontent{padding:12px 14px 36px}
  .editorialhero-portrait img{
    aspect-ratio:4/5;
    object-fit:cover;
    object-position:50% 46%;
  }
  .editorialhero-copy{
    left:14px;
    right:52px;
    bottom:14px;
    padding:13px 14px 14px;
  }
  .editorialhero-copy h1{
    margin:5px 0 7px;
    font-size:29px;
    line-height:.96;
  }
  .editorialhero-copy>p:not(.editorialhero-tagline){
    font-size:11px;
    line-height:1.38;
  }
  .editorialhero-copy nav{gap:18px;margin-top:9px}
  .editorialhero-copy nav a{font-size:9.5px}
  .workintro{gap:5px;padding:19px 0 14px}
  .workintro h2{font-size:43px}
  .workintro p{font-size:13px}
  .worktile-reporting{min-height:174px}
  .worktile-opinion{min-height:150px}
  .worktile-thoughts,.worktile-photos{min-height:134px}
  .worktile-copy strong{font-size:20px}
  .worktile-copy small{font-size:10px;line-height:1.34}
  body.home .homecontact{margin-top:15px;padding:20px}
  body.home .homecontact strong{font-size:25px}
}
@media(max-width:420px){
  .editorialhero-copy{left:12px;right:44px;bottom:12px;padding:12px 13px}
  .editorialhero-copy h1{font-size:27px}
  .workintro h2{font-size:41px}
  .worktile-reporting{min-height:166px}
  .worktile-opinion{min-height:144px}
  .worktile-thoughts,.worktile-photos{min-height:128px}
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
    CSS.write_text(css_text + "\n\n" + HOME_CSS + "\n", encoding="utf-8")
    print(f"Homepage polish: isolated_classes=1, hero_reference_4=1, work_reference_5=1, asset_version={ASSET_VERSION}, css_isolated=1, inline_critical=1, final_composition=18.11")


if __name__ == "__main__":
    main()
