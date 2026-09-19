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
ASSET_VERSION = "18.9.0"

HOME_CSS = r"""
/* Approved editorial homepage v18.9 */
body.home main{background:var(--paper)}
body.home .homecontent{width:100%;margin:0;padding:0 0 54px}

/* Desktop hero: approved reference no. 4 */
@media(min-width:801px){
  body.home .homeprofile{display:grid!important}
  body.home .homehero-reference{
    position:relative;
    grid-template-columns:minmax(350px,.93fr) minmax(420px,1fr) minmax(280px,.72fr);
    min-height:565px;
    overflow:hidden;
    border-bottom:1px solid var(--line);
    background:#f4f0e7;
  }

  body.home .homehero-copy{
    display:flex;
    flex-direction:column;
    justify-content:center;
    padding:58px 34px 42px max(56px,calc((100vw - 1400px)/2 + 34px));
  }
  body.home .homehero-copy>span{
    color:var(--forest);
    font-size:10px;
    font-weight:850;
    letter-spacing:.24em;
    text-transform:uppercase;
  }
  body.home .homehero-copy h1{
    margin:14px 0 13px;
    color:#0e4a41;
    font:400 clamp(66px,6.5vw,106px)/.78 var(--serif);
    letter-spacing:-.055em;
  }
  body.home .homehero-copy h1 em{display:block;font-style:italic;font-weight:400}
  body.home .homehero-copy>p:not(.homehero-tagline){
    max-width:500px;
    margin:0;
    color:#2f322e;
    font:400 18px/1.48 var(--serif);
  }
  body.home .homehero-rule{width:52px;height:2px;margin:18px 0 13px;background:var(--forest)}
  body.home .homehero-tagline{
    margin:0;
    color:#b2764e;
    font:italic 24px/1.18 var(--serif);
  }
  body.home .homehero-copy nav{display:flex;gap:38px;margin-top:20px}
  body.home .homehero-copy nav a{
    display:inline-flex;
    min-width:0;
    min-height:0;
    align-items:center;
    padding:0 0 5px;
    border:0;
    border-bottom:1px solid var(--forest);
    color:var(--forest);
    background:transparent;
    font:700 13px/1 var(--serif);
    text-decoration:none;
  }
  body.home .homehero-copy nav .hero-primary{color:var(--forest);background:transparent}
  body.home .homehero-copy blockquote{
    margin:auto 0 0;
    padding-top:17px;
    border-top:1px solid #d6cfc2;
    color:#7d7a71;
    font:italic 12px/1.45 var(--serif);
  }

  body.home .homehero-portrait{
    position:relative;
    align-self:center;
    width:min(100%,475px);
    margin:0 auto;
    padding:12px;
    background:#f8f5ef;
    box-shadow:0 13px 30px rgb(18 38 32 / 11%);
    transform:rotate(-1deg);
    z-index:3;
  }
  body.home .homehero-portrait:before{
    content:"";
    position:absolute;
    z-index:-1;
    inset:-12px 26px 14px -18px;
    background:#e7e1d5;
    transform:rotate(1.5deg);
  }
  body.home .homehero-portrait img{
    display:block;
    width:100%;
    aspect-ratio:1/1;
    object-fit:cover;
    object-position:center 48%;
    filter:grayscale(1) contrast(1.02);
  }
  body.home .homehero-portrait figcaption{
    position:absolute;
    left:42px;
    bottom:31px;
    max-width:150px;
    color:#fff;
    font:italic 21px/1.08 var(--serif);
    transform:rotate(-4deg);
    text-shadow:0 1px 12px rgb(0 0 0 / 45%);
  }

  body.home .homehero-panel{
    position:relative;
    overflow:hidden;
    min-height:565px;
    color:#0e4a41;
    background:#f3efe6;
  }
  body.home .homehero-panel:after{
    content:"";
    position:absolute;
    inset:0;
    background:linear-gradient(180deg,rgb(244 240 231 / 72%),rgb(244 240 231 / 46%));
    pointer-events:none;
  }
  body.home .homehero-panel img{
    position:absolute;
    inset:0;
    width:100%;
    height:100%;
    object-fit:cover;
    filter:grayscale(1) sepia(.08) saturate(.25) brightness(1.35);
    opacity:.34;
  }
  body.home .homehero-panel p{
    position:absolute;
    z-index:2;
    left:42px;
    top:72px;
    width:176px;
    margin:0;
    padding-top:16px;
    border-top:2px solid #315e57;
    color:#0d4d43;
    font:italic 26px/1.1 var(--serif);
  }
  body.home .homehero-panel>span{
    position:absolute;
    z-index:2;
    right:34px;
    bottom:38px;
    padding-top:13px;
    border-top:2px solid #6d8b85;
    color:#315e57;
    font-size:9px;
    font-weight:850;
    letter-spacing:.2em;
    line-height:1.55;
    text-transform:uppercase;
  }

  body.home .homeintro{
    display:grid;
    width:min(100% - 72px,1400px);
    margin:0 auto;
    padding:30px 0 18px;
    grid-template-columns:1fr 1fr;
    gap:32px;
    align-items:end;
  }
  body.home .homeintro>div:first-child span{
    display:block;
    margin-bottom:4px;
    color:var(--accent);
    font-size:10px;
    font-weight:850;
    letter-spacing:.18em;
    text-transform:uppercase;
  }
  body.home .homeintro h2{margin:0;font:400 58px/.94 var(--serif);letter-spacing:-.045em}
  body.home .homeintro>div:last-child{justify-self:end;max-width:620px}
  body.home .homeintro p{margin:0 0 8px;color:#474a45;font:400 15px/1.5 var(--serif)}
  body.home .homeintro a{
    color:var(--forest);
    font-size:12px;
    font-weight:750;
    text-decoration:none;
    border-bottom:1px solid currentColor;
  }

  /* Work grid: approved reference no. 5 */
  body.home .tiles{
    display:grid;
    width:min(100% - 72px,1400px);
    margin:0 auto;
    grid-template-columns:1.08fr .52fr .52fr;
    grid-template-rows:190px 190px;
    gap:10px;
  }
  body.home .tile{
    position:relative;
    min-height:0;
    padding:22px 22px 20px;
    align-items:flex-end;
    overflow:hidden;
    color:#fff;
    border:0;
    box-shadow:none;
    transform:none;
  }
  body.home .tile:hover{transform:translateY(-2px)}
  body.home .tile:after{
    content:"";
    position:absolute;
    inset:0;
    z-index:-1;
    background:linear-gradient(0deg,rgb(7 25 21 / 77%),rgb(7 25 21 / 6%) 74%);
  }
  body.home .tile-reporting{grid-column:1;grid-row:1/3}
  body.home .tile-opinion{grid-column:2/4;grid-row:1}
  body.home .tile-thoughts{grid-column:2;grid-row:2}
  body.home .tile-photos{grid-column:3;grid-row:2}

  body.home .tile-number{
    position:absolute;
    z-index:2;
    left:18px;
    top:16px;
    color:#efc37a;
    font:800 10px/1 var(--sans);
    letter-spacing:.12em;
    font-style:normal;
  }
  body.home .tile-copy{position:relative;z-index:2;width:64%}
  body.home .tile-reporting .tile-copy{width:56%}
  body.home .tile-opinion .tile-copy{width:58%}
  body.home .tile-thoughts .tile-copy,
  body.home .tile-photos .tile-copy{width:78%}
  body.home .tile strong{
    font:400 clamp(25px,2.35vw,36px)/1 var(--serif);
    letter-spacing:-.035em;
  }
  body.home .tile-reporting strong{font-size:clamp(36px,3.1vw,50px)}
  body.home .tile small{
    display:block;
    margin-top:7px;
    color:rgb(255 255 255 / 82%);
    font:400 12px/1.38 var(--serif);
  }
  body.home .tile-explore{
    display:inline-block;
    margin-top:18px;
    padding-bottom:4px;
    border-bottom:1px solid rgb(255 255 255 / 75%);
    font:700 10px/1 var(--sans);
  }
  body.home .tile-keywords{
    position:absolute;
    z-index:2;
    right:18px;
    bottom:20px;
    width:92px;
    padding-top:12px;
    border-top:1px solid rgb(255 255 255 / 64%);
    color:rgb(255 255 255 / 86%);
    font:800 9px/1.5 var(--sans);
    letter-spacing:.08em;
    text-transform:uppercase;
  }
  body.home .tile-keywords span{display:block}
  body.home .tile>i{
    position:absolute;
    z-index:3;
    right:16px;
    top:auto;
    bottom:16px;
    display:grid;
    width:34px;
    height:34px;
    place-items:center;
    border:1px solid rgb(255 255 255 / 65%);
    border-radius:50%;
    font-size:14px;
    transform:none;
  }

  body.home .tile-reporting .tile-art{
    background:
      linear-gradient(0deg,rgb(5 47 40 / 42%),rgb(5 47 40 / 24%)),
      url("assets/photography/Rajshahi University-nightscape-Journalist-Arafat-Rahaman (2).webp") center/cover;
  }
  body.home .tile-opinion .tile-art{
    background:
      linear-gradient(0deg,rgb(111 44 31 / 46%),rgb(111 44 31 / 42%)),
      url("assets/photography/Rajshahi University-nightscape-Journalist-Arafat-Rahaman (4).webp") center/cover;
  }
  body.home .tile-thoughts .tile-art{
    background:
      linear-gradient(0deg,rgb(47 70 43 / 43%),rgb(47 70 43 / 30%)),
      url("assets/photography/Rajshahi University-nightscape-Journalist-Arafat-Rahaman (1).webp") center/cover;
  }
  body.home .tile-photos img{filter:brightness(.64) saturate(.72)}
  body.home .homecontact{
    width:min(100% - 72px,1400px);
    margin:20px auto 0;
    padding:26px 30px;
  }
  body.home .homecontact strong{font-size:30px}
}

/* Mobile: no floating copy over the work cards, no overlap */
@media(max-width:800px){
  body.home .mobilehead{height:64px;padding:0 18px}
  body.home .mobilebrand{gap:10px}
  body.home .mark{width:39px;height:39px}
  body.home .themetoggle{display:none}
  body.home .menutoggle{display:inline-flex}
  body.home .mobilemenu[hidden],
  body.home .menubackdrop[hidden]{display:none!important}

  body.home .homecontent{padding:16px 14px 42px}
  body.home .homehero-reference{
    position:relative;
    display:flex!important;
    flex-direction:column;
    min-height:0;
    margin:0 0 22px;
    overflow:hidden;
    background:#f2ede4;
  }
  body.home .homehero-portrait{
    order:1;
    position:relative;
    display:block;
    width:100%;
    height:auto;
    margin:0;
    padding:0;
    overflow:hidden;
    background:#ddd7cc;
  }
  body.home .homehero-portrait img{
    display:block;
    width:100%;
    height:auto;
    aspect-ratio:1/1;
    object-fit:cover;
    object-position:center;
    filter:grayscale(1);
  }
  body.home .homehero-portrait figcaption{display:none}
  body.home .homehero-copy{
    order:2;
    position:static;
    padding:20px 18px 21px;
    color:var(--ink);
    background:#f2ede4;
  }
  body.home .homehero-copy>span{
    color:var(--accent);
    font-size:8px;
    font-weight:850;
    letter-spacing:.15em;
    text-transform:uppercase;
  }
  body.home .homehero-copy h1{
    margin:7px 0 9px;
    color:var(--forest);
    font:400 38px/.95 var(--serif);
    letter-spacing:-.035em;
  }
  body.home .homehero-copy h1 em{display:inline;font-style:italic}
  body.home .homehero-copy>p:not(.homehero-tagline){
    margin:0;
    color:#454944;
    font:400 13px/1.45 var(--serif);
  }
  body.home .homehero-rule{width:42px;height:1px;margin:14px 0 10px;background:var(--forest)}
  body.home .homehero-tagline{margin:0;color:#b2764e;font:italic 18px/1.2 var(--serif)}
  body.home .homehero-copy nav{display:flex;gap:24px;margin-top:14px}
  body.home .homehero-copy nav a{
    color:var(--forest);
    padding-bottom:3px;
    border-bottom:1px solid currentColor;
    font-size:10px;
    font-weight:800;
    text-decoration:none;
  }
  body.home .homehero-copy blockquote{display:none}
  body.home .homehero-panel{display:none}

  body.home .homeintro{
    display:grid;
    grid-template-columns:1fr;
    gap:7px;
    margin:0 0 17px;
    padding:14px 0 0;
  }
  body.home .homeintro>div:first-child span{display:block;color:var(--accent);font-size:9px;font-weight:850;letter-spacing:.14em;text-transform:uppercase}
  body.home .homeintro h2{margin:2px 0 0;font:400 48px/.95 var(--serif);letter-spacing:-.04em}
  body.home .homeintro p{margin:0;color:var(--muted);font-size:14px;line-height:1.45}
  body.home .homeintro a{display:inline-block;margin-top:4px;color:var(--forest);font-size:11px;text-decoration:none}

  body.home .tiles{display:grid;grid-template-columns:1fr 1fr;grid-template-rows:auto;gap:8px}
  body.home .tile{min-height:156px;padding:16px}
  body.home .tile-reporting{grid-column:1/-1;grid-row:auto;min-height:196px}
  body.home .tile-opinion{grid-column:1/-1;grid-row:auto;min-height:172px}
  body.home .tile-thoughts{grid-column:1;grid-row:auto}
  body.home .tile-photos{grid-column:2;grid-row:auto}
  body.home .tile-number,
  body.home .tile-keywords,
  body.home .tile-explore{display:none}
  body.home .tile-copy,
  body.home .tile-reporting .tile-copy,
  body.home .tile-opinion .tile-copy,
  body.home .tile-thoughts .tile-copy,
  body.home .tile-photos .tile-copy{width:auto}
  body.home .tile strong{font-size:22px}
  body.home .tile small{font-size:10.5px}
  body.home .homecontact{margin-top:18px;padding:23px}
  body.home .homecontact strong{font-size:28px}
}

@media(max-width:420px){
  body.home .homehero-copy h1{font-size:35px}
  body.home .homeintro h2{font-size:44px}
  body.home .tile{min-height:148px}
  body.home .tile-reporting{min-height:184px}
  body.home .tile-opinion{min-height:164px}
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
    markers = (
        "/* Hybrid editorial homepage v18.4 */",
        "/* Simplified editorial homepage v18.6 */",
        "/* Reference editorial homepage v18.8 */",
        "/* Approved editorial homepage v18.9 */",
    )
    cut = len(css_text)
    for marker in markers:
        index = css_text.find(marker)
        if index >= 0:
            cut = min(cut, index)
    if cut < len(css_text):
        css_text = css_text[:cut].rstrip()
    CSS.write_text(css_text + "\n\n" + HOME_CSS + "\n", encoding="utf-8")
    print(f"Homepage polish: hero_reference_4=1, work_reference_5=1, asset_version={ASSET_VERSION}")


if __name__ == "__main__":
    main()
