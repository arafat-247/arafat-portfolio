"""Apply the approved portrait hero without redesigning the rest of the homepage."""
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
    r'<section class="homeprofile"[^>]*>.*?</section>',
    re.S,
)
ASSET_VERSION = "17.8.0"
HERO_IMAGE = "assets/portraits/byline.webp"

# The existing byline asset is the supplied black-and-white portrait.
# Keep this a normal image and real text; do not rasterise the whole hero.
HOME_PROFILE = """<section class="homeprofile" data-hero-version="17.8.0" aria-labelledby="home-profile-title"><img src="assets/portraits/byline.webp" alt="Black-and-white portrait of Arafat Rahaman" width="900" height="892" loading="eager" fetchpriority="high" decoding="async"><div><span>Journalist \u00b7 Dhaka</span><h2 id="home-profile-title"><span>Arafat</span> <em>Rahaman</em></h2><p>Reporting on education, governance, public accountability and social issues for The Daily Star.</p><nav aria-label="About and contact"><a href="about/">About me \u2192</a><a href="mailto:arafat.mcj@yahoo.com">Email</a></nav></div></section>"""

HOME_CSS = r"""
/* Editorial homepage polish */

/* Existing mobile masthead and page padding: intentionally unchanged. */
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
}

@media(max-width:380px){
  body.home .mobilebrand{font-size:15px}
  body.home .menutoggle>span:last-child{display:none}
}

/* Approved portrait hero only. Other homepage sections retain their styles. */
body.home .homeprofile{
  position:relative;
  isolation:isolate;
  display:grid;
  grid-template-columns:minmax(0,1fr);
  align-items:center;
  min-height:480px;
  margin:0 0 34px;
  padding:44px;
  overflow:hidden;
  color:#f4f2eb;
  background:var(--forest);
}
body.home .homeprofile>img{
  position:absolute;
  inset:0 0 0 auto;
  z-index:0;
  display:block;
  width:68%;
  height:100%;
  min-height:0;
  max-width:none;
  object-fit:cover;
  object-position:56% 30%;
  filter:grayscale(1);
}
body.home .homeprofile:after{
  content:"";
  position:absolute;
  inset:0;
  z-index:1;
  pointer-events:none;
  background:linear-gradient(90deg,#0b302b 0%,#0b302b 34%,rgb(11 48 43 / 94%) 39%,rgb(11 48 43 / 58%) 47%,rgb(11 48 43 / 8%) 63%,transparent 78%),linear-gradient(0deg,#0b302b 0%,rgb(11 48 43 / 42%) 20%,transparent 52%);
}
body.home .homeprofile>div{
  position:relative;
  z-index:2;
  display:flex;
  width:48%;
  min-width:0;
  flex-direction:column;
  align-items:flex-start;
  justify-content:center;
  padding:0;
  background:transparent;
}
body.home .homeprofile>div>span{
  display:block;
  color:#efaa96;
  font:750 10px/1.5 var(--sans);
  letter-spacing:.16em;
  text-transform:uppercase;
}
body.home .homeprofile h2{
  margin:24px 0 0;
  color:#f4f2eb;
  font:400 clamp(52px,6.2vw,86px)/.99 var(--serif);
  letter-spacing:-.05em;
}
body.home .homeprofile h2 span,body.home .homeprofile h2 em{display:block}
body.home .homeprofile h2 em{font-weight:400}
body.home .homeprofile p{
  display:block;
  max-width:335px;
  margin:23px 0 0;
  overflow:visible;
  color:#e3e8e3;
  font:400 14px/1.6 var(--sans);
  -webkit-line-clamp:unset;
}
body.home .homeprofile nav{display:flex;flex-wrap:wrap;gap:24px;margin-top:22px}
body.home .homeprofile a{
  display:inline-flex;
  min-height:44px;
  align-items:center;
  padding:3px 0;
  border-bottom:1px solid #8ca79f;
  color:#f4f2eb;
  font:750 12px/1.3 var(--sans);
  text-decoration:none;
}
body.home .homeprofile a:hover{border-color:#efaa96;color:#efaa96}
body.home .homeprofile a:focus-visible{outline:2px solid #efaa96;outline-offset:5px}
@media(min-width:1001px) and (max-width:1200px){
  body.home .homeprofile{min-height:420px;padding:30px}
  body.home .homeprofile h2{font-size:60px}
  body.home .homeprofile p{font-size:13px}
}
@media(max-width:1000px){
  body.home .homeprofile{
    display:block;
    min-height:0;
    padding:0;
  }
  body.home .homeprofile>img{
    inset:0 0 auto;
    width:100%;
    height:auto;
    min-height:0;
    object-position:center top;
  }
  body.home .homeprofile:after{
    background:linear-gradient(180deg,rgb(11 48 43 / 8%) 0%,rgb(11 48 43 / 2%) 28%,rgb(11 48 43 / 60%) 47%,#0b302b 67%,#0b302b 100%);
  }
  body.home .homeprofile>div{
    width:100%;
    padding:66% 26px 26px;
    justify-content:flex-end;
  }
  body.home .homeprofile>div>span{
    position:absolute;
    top:22px;
    left:26px;
    width:85px;
    color:#eaf0e9;
    font-size:9px;
    text-shadow:0 1px 5px #102d28;
  }
  body.home .homeprofile h2{margin:0;font-size:clamp(43px,8.5vw,66px);line-height:1;letter-spacing:-.05em}
  body.home .homeprofile h2 em{font-style:normal}
  body.home .homeprofile p{max-width:430px;margin-top:16px;font-size:13px;line-height:1.55}
  body.home .homeprofile nav{margin-top:15px;gap:25px}
}
@media(max-width:520px){
  body.home .homeprofile{margin-bottom:30px}
  body.home .homeprofile>div{padding:66% 22px 24px}
  body.home .homeprofile>div>span{left:22px;top:20px}
  body.home .homeprofile h2{font-size:clamp(43px,11.5vw,59px)}
  body.home .homeprofile p{font-size:12px}
  body.home .homeprofile nav{gap:24px;margin-top:13px}
  body.home .homeprofile a{font-size:11px}
}
@media(max-width:380px){
  body.home .homeprofile>div{padding-inline:19px}
  body.home .homeprofile>div>span{left:19px}
  body.home .homeprofile h2{font-size:42px}
}
""".strip()


def main() -> None:
    if not HOME.is_file() or not CSS.is_file():
        raise FileNotFoundError("Build output is incomplete; run scripts/build.py first")
    if not (DIST / HERO_IMAGE).is_file():
        raise FileNotFoundError(f"The approved hero portrait is missing: {HERO_IMAGE}")

    source = HOME.read_text(encoding="utf-8")
    source = ASSET_VERSION_RE.sub(f"portfolio.css?v={ASSET_VERSION}", source)
    source, replaced = HOME_PROFILE_RE.subn(lambda _: HOME_PROFILE, source, count=1)
    if replaced != 1:
        raise RuntimeError("Could not locate the homepage profile block")

    css = CSS.read_text(encoding="utf-8")
    marker_index = css.find(CSS_MARKER)
    if marker_index >= 0:
        css = css[:marker_index].rstrip()
    CSS.write_text(css + "\n\n" + HOME_CSS + "\n", encoding="utf-8")
    HOME.write_text(source, encoding="utf-8")
    print(f"Homepage hero: approved_portrait=1, foreground_text=1, other_sections=unchanged, asset_version={ASSET_VERSION}")


if __name__ == "__main__":
    main()
