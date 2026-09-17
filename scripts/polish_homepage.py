"""Keep the original homepage language while refining the mobile masthead and portrait lead."""
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
ASSET_VERSION = "17.7.0"

HOME_PROFILE = """<section class="homeprofile" aria-labelledby="home-profile-title"><img src="assets/portraits/home.webp" alt="Arafat Rahaman" width="640" height="760"><div><span>Journalist · Dhaka</span><h2 id="home-profile-title">Arafat Rahaman</h2><p>Reporting on education, governance, public accountability and social issues for The Daily Star.</p><nav><a href="about/">About me →</a><a href="mailto:arafat.mcj@yahoo.com">Email</a></nav></div></section>"""

HOME_CSS = r"""
/* Editorial homepage polish */
/* Preserve the site's original palette and structure; only refine the mobile masthead and hero. */
@media(max-width:800px){
  body.home .mobilehead{
    height:62px;
    padding:0 16px;
    border-bottom:1px solid var(--line);
    background:var(--surface);
  }
  body.home .mobilehead.scrolled{box-shadow:0 5px 18px rgb(12 30 27 / 8%)}
  body.home .mobilebrand{gap:10px;font:700 18px/1 var(--serif);letter-spacing:-.02em}
  body.home .mobilebrand .mark{width:37px;height:37px;border-radius:50%;color:#fff;background:var(--forest);font:400 24px/37px var(--serif);text-align:center}
  body.home .mobileactions{gap:7px}
  body.home .themetoggle{min-width:38px;min-height:38px;padding:4px}
  body.home .menutoggle{display:inline-flex;min-width:auto;min-height:38px;gap:7px;padding:5px 2px 5px 6px}
  body.home .menutoggle>span:last-child{display:inline;font-size:12px;font-weight:760}
  body.home .menulines{width:20px}
  body.home .mobilemenu:not([hidden]){display:flex!important;inset:62px 0 auto auto;max-height:calc(100dvh - 62px)}
  body.home .menubackdrop:not([hidden]){display:block!important}
  body.home .mobilemenu[hidden],body.home .menubackdrop[hidden]{display:none!important}

  body.home .homecontent{padding-top:18px}
  body.home .homeprofile{
    display:grid;
    grid-template-columns:minmax(0,56%) minmax(0,44%);
    min-height:252px;
    margin-bottom:34px;
    overflow:hidden;
    color:#fff;
    background:var(--forest);
    box-shadow:0 14px 36px rgb(12 38 33 / 9%);
  }
  body.home .homeprofile>img{
    width:100%;
    height:100%;
    min-height:252px;
    object-fit:cover;
    object-position:61% 45%;
    filter:grayscale(1) contrast(1.02);
  }
  body.home .homeprofile>div{
    display:flex;
    min-width:0;
    flex-direction:column;
    justify-content:center;
    padding:21px 18px;
    background:var(--forest);
  }
  body.home .homeprofile>div>span{color:#efaa96;font-size:9px;font-weight:850;line-height:1.25;letter-spacing:.13em;text-transform:uppercase}
  body.home .homeprofile h2{margin:7px 0 0;font:700 clamp(25px,5.5vw,34px)/.98 var(--serif);letter-spacing:-.035em}
  body.home .homeprofile p{margin:11px 0 0;color:rgb(255 255 255 / 78%);font-size:11px;line-height:1.45}
  body.home .homeprofile nav{display:flex;flex-wrap:wrap;gap:14px;margin-top:15px}
  body.home .homeprofile a{padding-bottom:2px;border-bottom:1px solid rgb(255 255 255 / 70%);font-size:10.5px;font-weight:800;text-decoration:none}
}

@media(max-width:520px){
  body.home .mobilehead{height:58px;padding-inline:14px}
  body.home .mobilebrand{gap:8px;font-size:16px}
  body.home .mobilebrand .mark{width:34px;height:34px;font-size:22px;line-height:34px}
  body.home .mobileactions{gap:4px}
  body.home .themesymbol{width:28px;height:28px}
  body.home .menutoggle{gap:5px}
  body.home .menutoggle>span:last-child{font-size:11px}
  body.home .menulines{width:18px}
  body.home .mobilemenu:not([hidden]){inset:58px 0 auto auto;max-height:calc(100dvh - 58px)}

  body.home .homecontent{padding-top:14px}
  body.home .homeprofile{grid-template-columns:55% 45%;min-height:232px;margin-bottom:30px}
  body.home .homeprofile>img{min-height:232px;object-position:62% 44%}
  body.home .homeprofile>div{padding:17px 14px}
  body.home .homeprofile>div>span{font-size:8px}
  body.home .homeprofile h2{font-size:25px}
  body.home .homeprofile p{margin-top:9px;font-size:10.3px;line-height:1.4}
  body.home .homeprofile nav{gap:11px;margin-top:12px}
  body.home .homeprofile a{font-size:9.5px}
}

@media(max-width:380px){
  body.home .mobilebrand{font-size:15px}
  body.home .menutoggle>span:last-child{display:none}
  body.home .homeprofile{grid-template-columns:54% 46%;min-height:220px}
  body.home .homeprofile>img{min-height:220px}
  body.home .homeprofile>div{padding:15px 12px}
  body.home .homeprofile h2{font-size:23px}
  body.home .homeprofile p{font-size:9.8px}
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
    print(f"Homepage concept: original_structure=1, split_hero=1, refined_header=1, asset_version={ASSET_VERSION}")


if __name__ == "__main__":
    main()
