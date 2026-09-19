"""Apply the editorial reference homepage after final build processing."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
HOME = DIST / "index.html"
CSS = DIST / "portfolio.css"
ASSET_VERSION_RE = re.compile(r"portfolio\\.css\\?v=[0-9.]+", re.I)
SCRIPT_VERSION_RE = re.compile(r"portfolio\\.js\\?v=[0-9.]+", re.I)
ASSET_VERSION = "18.8.0"

HOME_CSS = r"""
/* Reference editorial homepage v18.8 */
body.home main{background:var(--paper)}
body.home .homecontent{width:100%;margin:0;padding:0 0 64px}

/* Desktop: match the approved editorial reference composition */
@media(min-width:801px){
  body.home .homeprofile{display:grid!important}
  body.home .homehero-reference{
    grid-template-columns:minmax(320px,.95fr) minmax(360px,.92fr) minmax(250px,.64fr);
    min-height:590px;
    overflow:hidden;
    border-bottom:1px solid var(--line);
    background:#f4f0e7;
  }

  body.home .homehero-copy{
    display:flex;
    flex-direction:column;
    justify-content:center;
    padding:70px 38px 54px max(48px,calc((100vw - 1320px)/2 + 34px));
  }
  body.home .homehero-copy>span{
    color:var(--forest);
    font-size:11px;
    font-weight:850;
    letter-spacing:.24em;
    text-transform:uppercase;
  }
  body.home .homehero-copy h1{
    margin:14px 0 14px;
    color:#0f3731;
    font:400 clamp(64px,6vw,102px)/.78 var(--serif);
    letter-spacing:-.055em;
  }
  body.home .homehero-copy h1 em{
    display:block;
    font-style:italic;
    font-weight:400;
  }
  body.home .homehero-copy>p:not(.homehero-tagline){
    max-width:520px;
    margin:0;
    color:#2f322f;
    font:400 18px/1.5 var(--serif);
  }
  body.home .homehero-rule{
    width:56px;
    height:2px;
    margin:20px 0 14px;
    background:var(--forest);
  }
  body.home .homehero-tagline{
    margin:0;
    color:#b57449;
    font:italic 24px/1.2 var(--serif);
    letter-spacing:.01em;
  }
  body.home .homehero-copy nav{
    display:flex;
    gap:12px;
    margin-top:26px;
  }
  body.home .homehero-copy nav a{
    display:inline-flex;
    min-width:145px;
    min-height:50px;
    align-items:center;
    justify-content:space-between;
    padding:0 20px;
    border:1px solid var(--forest);
    color:var(--forest);
    background:transparent;
    font:700 13px/1 var(--serif);
    text-decoration:none;
  }
  body.home .homehero-copy nav .hero-primary{
    color:#fff;
    background:var(--forest);
  }
  body.home .homehero-copy blockquote{
    margin:auto 0 0;
    padding-top:22px;
    border-top:1px solid color-mix(in srgb,var(--line) 80%,transparent);
    color:#79776f;
    font:italic 13px/1.45 var(--serif);
  }

  body.home .homehero-portrait{
    position:relative;
    align-self:center;
    width:min(100%,470px);
    margin:0 auto;
    padding:14px;
    background:#f8f5ee;
    box-shadow:0 15px 40px rgb(18 38 32 / 13%);
    transform:rotate(-1.5deg);
    z-index:2;
  }
  body.home .homehero-portrait:before{
    content:"";
    position:absolute;
    z-index:-1;
    inset:-16px 32px 16px -18px;
    background:#ece6da;
    transform:rotate(2deg);
  }
  body.home .homehero-portrait img{
    display:block;
    width:100%;
    aspect-ratio:1/1;
    object-fit:cover;
    object-position:center;
    filter:grayscale(1) contrast(1.03);
  }
  body.home .homehero-portrait figcaption{
    position:absolute;
    left:46px;
    bottom:34px;
    max-width:170px;
    color:#fff;
    font:italic 22px/1.08 var(--serif);
    transform:rotate(-4deg);
    text-shadow:0 1px 14px rgb(0 0 0 / 45%);
  }

  body.home .homehero-panel{
    position:relative;
    overflow:hidden;
    min-height:590px;
    color:#fff;
    background:#0e4d44;
  }
  body.home .homehero-panel:after{
    content:"";
    position:absolute;
    inset:0;
    background:linear-gradient(180deg,rgb(9 69 60 / 12%),rgb(5 55 48 / 58%));
    pointer-events:none;
  }
  body.home .homehero-panel img{
    position:absolute;
    inset:0;
    width:100%;
    height:100%;
    object-fit:cover;
    filter:grayscale(.25) sepia(.12) saturate(.75) brightness(.52);
  }
  body.home .homehero-panel p{
    position:absolute;
    z-index:2;
    right:36px;
    top:82px;
    width:150px;
    margin:0;
    padding-top:16px;
    border-top:2px solid rgb(255 255 255 / 70%);
    font:italic 24px/1.12 var(--serif);
  }
  body.home .homehero-panel>span{
    position:absolute;
    z-index:2;
    right:36px;
    bottom:44px;
    padding-top:14px;
    border-top:2px solid rgb(255 255 255 / 70%);
    font-size:9px;
    font-weight:850;
    letter-spacing:.22em;
    line-height:1.6;
    text-transform:uppercase;
  }

  body.home .homeintro{
    display:grid;
    width:min(100% - 64px,1320px);
    margin:0 auto;
    padding:34px 0 22px;
    grid-template-columns:1fr 1fr;
    gap:30px;
    align-items:end;
  }
  body.home .homeintro>div:first-child span{
    display:block;
    margin-bottom:5px;
    color:var(--accent);
    font-size:10px;
    font-weight:850;
    letter-spacing:.18em;
    text-transform:uppercase;
  }
  body.home .homeintro h2{
    margin:0;
    font:400 56px/.95 var(--serif);
    letter-spacing:-.045em;
  }
  body.home .homeintro>div:last-child{
    justify-self:end;
    text-align:left;
  }
  body.home .homeintro p{
    margin:0 0 8px;
    color:#4d504b;
    font:400 15px/1.5 var(--serif);
  }
  body.home .homeintro a{
    color:var(--forest);
    font-size:12px;
    font-weight:750;
    text-decoration:none;
    border-bottom:1px solid currentColor;
  }

  body.home .tiles{
    display:grid;
    width:min(100% - 48px,1360px);
    margin:0 auto;
    grid-template-columns:repeat(4,minmax(0,1fr));
    gap:10px;
  }
  body.home .tile{
    position:relative;
    min-height:300px;
    padding:24px 22px 22px;
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
    background:linear-gradient(0deg,rgb(7 25 21 / 76%),rgb(7 25 21 / 5%) 72%);
  }
  body.home .tile-number{
    position:absolute;
    z-index:2;
    left:20px;
    top:18px;
    color:#efc37a;
    font:800 10px/1 var(--sans);
    letter-spacing:.12em;
    font-style:normal;
  }
  body.home .tile-copy{
    position:relative;
    z-index:2;
    width:66%;
  }
  body.home .tile strong{
    font:400 clamp(26px,2.25vw,34px)/1 var(--serif);
    letter-spacing:-.035em;
  }
  body.home .tile small{
    display:block;
    margin-top:8px;
    color:rgb(255 255 255 / 78%);
    font:400 12px/1.4 var(--serif);
  }
  body.home .tile-explore{
    display:inline-block;
    margin-top:22px;
    padding-bottom:4px;
    border-bottom:1px solid rgb(255 255 255 / 75%);
    font:700 10px/1 var(--sans);
  }
  body.home .tile-keywords{
    position:absolute;
    z-index:2;
    right:18px;
    bottom:22px;
    width:86px;
    padding-top:13px;
    border-top:1px solid rgb(255 255 255 / 65%);
    color:rgb(255 255 255 / 86%);
    font:800 9px/1.5 var(--sans);
    letter-spacing:.09em;
    text-transform:uppercase;
  }
  body.home .tile-keywords span{display:block}
  body.home .tile>i{
    position:absolute;
    z-index:3;
    right:17px;
    top:auto;
    bottom:18px;
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
      linear-gradient(0deg,rgb(7 50 44 / 58%),rgb(7 50 44 / 58%)),
      url("assets/photography/Rajshahi University-nightscape-Journalist-Arafat-Rahaman (2).webp") center/cover;
  }
  body.home .tile-opinion .tile-art{
    background:
      linear-gradient(0deg,rgb(128 58 44 / 62%),rgb(128 58 44 / 62%)),
      url("assets/photography/Rajshahi University-nightscape-Journalist-Arafat-Rahaman (4).webp") center/cover;
  }
  body.home .tile-thoughts .tile-art{
    background:
      linear-gradient(0deg,rgb(45 73 48 / 58%),rgb(45 73 48 / 58%)),
      url("assets/photography/Rajshahi University-nightscape-Journalist-Arafat-Rahaman (1).webp") center/cover;
  }
  body.home .tile-photos img{filter:brightness(.62) saturate(.72)}
  body.home .homecontact{
    width:min(100% - 48px,1360px);
    margin:26px auto 0;
  }
}

/* Tablet and mobile retain a separate, compact composition */
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
    display:block!important;
    min-height:0;
    margin:0 0 22px;
    background:transparent;
  }
  body.home .homehero-copy{
    position:absolute;
    z-index:3;
    left:26px;
    right:26px;
    bottom:36px;
    padding:18px;
    color:#fff;
    background:rgb(7 55 48 / 91%);
  }
  body.home .homehero-copy>span{color:#efb39d;font-size:8px;font-weight:850;letter-spacing:.16em;text-transform:uppercase}
  body.home .homehero-copy h1{margin:7px 0 8px;color:#fff;font:400 34px/.95 var(--serif);letter-spacing:-.03em}
  body.home .homehero-copy h1 em{display:inline;font-style:normal}
  body.home .homehero-copy>p:not(.homehero-tagline){margin:0;color:rgb(255 255 255 / 80%);font-size:12px;line-height:1.4}
  body.home .homehero-rule,
  body.home .homehero-tagline,
  body.home .homehero-copy blockquote{display:none}
  body.home .homehero-copy nav{display:flex;gap:14px;margin-top:12px}
  body.home .homehero-copy nav a{color:#fff;font-size:10px;font-weight:800;text-decoration:none;border-bottom:1px solid currentColor}

  body.home .homehero-portrait{
    position:relative;
    display:block;
    height:410px;
    margin:0;
    overflow:hidden;
    background:#111;
  }
  body.home .homehero-portrait img{
    width:100%;
    height:100%;
    object-fit:cover;
    object-position:center 30%;
    filter:grayscale(1) brightness(.7);
  }
  body.home .homehero-portrait figcaption{display:none}
  body.home .homehero-panel{display:none}

  body.home .homeintro{
    display:grid;
    grid-template-columns:1fr;
    gap:8px;
    margin:0 0 18px;
    padding:18px 0 0;
  }
  body.home .homeintro>div:first-child span{display:block;color:var(--accent);font-size:9px;font-weight:850;letter-spacing:.14em;text-transform:uppercase}
  body.home .homeintro h2{margin:2px 0 0;font:400 48px/.95 var(--serif);letter-spacing:-.04em}
  body.home .homeintro p{margin:0;color:var(--muted);font-size:14px;line-height:1.45}
  body.home .homeintro a{display:inline-block;margin-top:4px;color:var(--forest);font-size:11px;text-decoration:none}

  body.home .tiles{display:grid;grid-template-columns:1fr 1fr;gap:8px}
  body.home .tile{min-height:158px;padding:16px}
  body.home .tile-reporting,
  body.home .tile-photos{grid-column:1/-1}
  body.home .tile-number,
  body.home .tile-keywords,
  body.home .tile-explore{display:none}
  body.home .tile-copy{width:auto}
  body.home .tile strong{font-size:22px}
  body.home .tile small{font-size:10.5px}
  body.home .homecontact{margin-top:18px;padding:24px}
}

@media(max-width:420px){
  body.home .homehero-portrait{height:380px}
  body.home .homehero-copy{left:22px;right:22px;bottom:28px}
  body.home .homehero-copy h1{font-size:31px}
  body.home .homeintro h2{font-size:44px}
  body.home .tile{min-height:148px}
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
    )
    cut = len(css_text)
    for marker in markers:
        index = css_text.find(marker)
        if index >= 0:
            cut = min(cut, index)
    if cut < len(css_text):
        css_text = css_text[:cut].rstrip()
    CSS.write_text(css_text + "\n\n" + HOME_CSS + "\n", encoding="utf-8")
    print(f"Homepage polish: reference_layout=1, desktop_four_cards=1, asset_version={ASSET_VERSION}")


if __name__ == "__main__":
    main()
