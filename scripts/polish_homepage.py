"""Keep the original homepage structure while refining its mobile masthead and portrait lead."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
HOME = DIST / "index.html"
CSS = DIST / "portfolio.css"
CSS_MARKER = "/* Editorial homepage polish */"
ASSET_VERSION_RE = re.compile(r"portfolio\.css\?v=[0-9.]+", re.I)
HOME_PROFILE_RE = re.compile(
    r'<section class="homeprofile" aria-labelledby="home-profile-title">.*?</section>',
    re.S,
)
ASSET_VERSION = "17.6.0"

HOME_PROFILE = """<section class="homeprofile" aria-labelledby="home-profile-title"><img src="assets/portraits/home.webp" alt="Arafat Rahaman" width="640" height="760"><div><span>Journalist · The Daily Star</span><h2 id="home-profile-title">Arafat Rahaman</h2><p>Reporting on education, governance, rights and public accountability.</p><nav><a href="about/">About me →</a><a href="mailto:arafat.mcj@yahoo.com">Email</a></nav></div></section>"""

HOME_CSS = r"""
/* Editorial homepage polish */
/* The homepage otherwise uses the original site layout and palette. */
@media(max-width:800px){
  body.home .mobilehead{
    height:60px;
    padding:0 16px;
    border-bottom:1px solid var(--line);
    background:color-mix(in srgb,var(--paper) 97%,transparent);
    backdrop-filter:blur(12px);
  }
  body.home .mobilehead.scrolled{box-shadow:0 5px 18px rgb(12 30 27 / 9%)}
  body.home .mobilebrand{gap:10px;font-size:14px;letter-spacing:-.01em}
  body.home .mark{width:36px;height:36px;font-size:22px}
  body.home .mobileactions{gap:2px}
  body.home .themetoggle,body.home .menutoggle{min-width:40px;min-height:40px;padding:5px}
  body.home .menutoggle{display:inline-flex}
  body.home .menutoggle>span:last-child{font-size:12px;font-weight:750}
  body.home .mobilemenu:not([hidden]){display:flex!important;inset:60px 0 auto auto;max-height:calc(100dvh - 60px)}
  body.home .menubackdrop:not([hidden]){display:block!important}
  body.home .mobilemenu[hidden],body.home .menubackdrop[hidden]{display:none!important}

  body.home .homecontent{padding-top:18px}
  body.home .homeprofile{
    position:relative;
    isolation:isolate;
    display:block;
    min-height:clamp(300px,70vw,410px);
    margin-bottom:36px;
    overflow:hidden;
    color:#fff;
    background:var(--forest);
  }
  body.home .homeprofile:before{
    content:"";
    position:absolute;
    inset:0;
    z-index:0;
    background:
      linear-gradient(90deg,rgb(4 24 21 / 84%) 0%,rgb(4 24 21 / 68%) 38%,rgb(4 24 21 / 18%) 72%,transparent 100%),
      linear-gradient(0deg,rgb(4 24 21 / 42%) 0%,transparent 54%);
    pointer-events:none;
  }
  body.home .homeprofile>img{
    position:absolute;
    inset:0;
    width:100%;
    height:100%;
    object-fit:cover;
    object-position:center 28%;
  }
  body.home .homeprofile>div{
    position:relative;
    z-index:1;
    display:flex;
    width:min(66%,390px);
    min-height:clamp(300px,70vw,410px);
    flex-direction:column;
    justify-content:flex-end;
    padding:28px 24px;
    background:transparent;
  }
  body.home .homeprofile>div>span{color:#efaa96;font-size:10px;font-weight:850;letter-spacing:.13em;text-transform:uppercase}
  body.home .homeprofile h2{margin:6px 0 0;font:700 clamp(30px,8vw,42px)/.98 var(--serif);letter-spacing:-.035em}
  body.home .homeprofile p{max-width:330px;margin:12px 0 0;color:rgb(255 255 255 / 82%);font-size:12px;line-height:1.5}
  body.home .homeprofile nav{display:flex;flex-wrap:wrap;gap:17px;margin-top:17px}
  body.home .homeprofile a{padding-bottom:2px;border-bottom:1px solid rgb(255 255 255 / 72%);font-size:11px;font-weight:800;text-decoration:none}
}

@media(max-width:460px){
  body.home .mobilehead{padding-inline:14px}
  body.home .mobilebrand{gap:8px;font-size:13px}
  body.home .mark{width:34px;height:34px;font-size:21px}
  body.home .themesymbol{width:28px;height:28px}
  body.home .menutoggle{gap:5px}
  body.home .menulines{width:19px}
  body.home .homecontent{padding-top:14px}
  body.home .homeprofile{min-height:292px;margin-bottom:32px}
  body.home .homeprofile>div{width:72%;min-height:292px;padding:24px 20px}
  body.home .homeprofile h2{font-size:31px}
  body.home .homeprofile p{font-size:11.5px}
}
""".strip()


def main() -> None:
    if not HOME.is_file() or not CSS.is_file():
        raise FileNotFoundError("Build output is incomplete; run scripts/build.py first")

    source = HOME.read_text(encoding="utf-8")
    source = ASSET_VERSION_RE.sub(f"portfolio.css?v={ASSET_VERSION}", source)
    source, replaced = HOME_PROFILE_RE.subn(HOME_PROFILE, source, count=1)
    if replaced != 1:
        raise RuntimeError("Could not locate the homepage profile block")
    HOME.write_text(source, encoding="utf-8")

    css = CSS.read_text(encoding="utf-8")
    marker_index = css.find(CSS_MARKER)
    if marker_index >= 0:
        css = css[:marker_index].rstrip()
    CSS.write_text(css + "\n\n" + HOME_CSS + "\n", encoding="utf-8")
    print(f"Homepage concept: original_structure=1, overlay_hero=1, mobile_menu=1, asset_version={ASSET_VERSION}")


if __name__ == "__main__":
    main()
