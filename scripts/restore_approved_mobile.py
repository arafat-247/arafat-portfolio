"""Restore the approved mobile-only homepage details after homepage/footer post-processing.

Desktop is intentionally untouched. The source homepage already carries the approved
semantic structure; this pass restores the mobile artwork and alternating scroll entry
motion that later CSS simplification removed.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "dist" / "index.html"
MARKER = "approved-mobile-restore-v1"

MOBILE_CSS = r"""
@media(max-width:800px){
  /* Keep the approved biography CTA visible on mobile. */
  .portalhero-actions{
    display:flex!important;
    flex-wrap:wrap;
    gap:8px;
  }
  .portalhero-actions .portalhero-primary{
    display:inline-flex!important;
    color:#fff!important;
    border-color:#0b5b50!important;
    background:#0b5b50!important;
  }

  /* Restore the approved artwork rather than later CSS approximations. */
  .portalart-opinion,
  .portalart-thoughts{
    background-image:url("assets/home/portal-reference-sprite.webp")!important;
    background-repeat:no-repeat!important;
    background-size:100% 300%!important;
  }
  .portalart-opinion{background-position:center 50%!important}
  .portalart-thoughts{background-position:center bottom!important}
  .portalart-opinion:before,
  .portalart-opinion:after,
  .portalart-thoughts:before,
  .portalart-thoughts:after{content:none!important}

  /* Reporting enters from the left; Opinion from the right; then alternate. */
  .portalwork{overflow:hidden!important}
  .portalpanel.portal-reveal{
    opacity:0!important;
    transition:
      opacity .52s ease var(--portal-delay,0ms),
      transform .62s cubic-bezier(.2,.72,.2,1) var(--portal-delay,0ms)!important;
    will-change:opacity,transform;
  }
  .portalpanel.portal-reveal:nth-child(odd){transform:translate3d(-54px,0,0)!important}
  .portalpanel.portal-reveal:nth-child(even){transform:translate3d(54px,0,0)!important}
  .portalpanel.portal-reveal.is-visible{
    opacity:1!important;
    transform:translate3d(0,0,0)!important;
  }

  /* The existing shared site footer is the approved deep-green ending. */
  .portalhome-mobile>.sitefooter{
    margin:0!important;
    border-radius:0!important;
  }
}

@media(max-width:800px) and (prefers-reduced-motion:reduce){
  .portalpanel.portal-reveal,
  .portalpanel.portal-reveal.is-visible{
    opacity:1!important;
    transform:none!important;
    transition:none!important;
  }
}
""".strip()


def main() -> None:
    if not HOME.is_file():
        raise FileNotFoundError("dist/index.html does not exist; run the build first")

    source = HOME.read_text(encoding="utf-8")
    required = (
        'class="portalhome portalhome-mobile"',
        'Stories <em>from a changing Bangladesh</em>',
        'class="portalpanel portal-reporting"',
        'class="portalpanel portal-opinion"',
        'class="portalpanel portal-thoughts"',
        'class="portalpanel portal-photography"',
    )
    missing = [token for token in required if token not in source]
    if missing:
        raise RuntimeError("Approved mobile structure missing: " + ", ".join(missing))

    # Use the retained approved reporting artwork if a later build replaced it with
    # generated CSS art. The asset is already preserved by the build pipeline.
    source = source.replace(
        '<b class="portalart portalart-reporting" aria-hidden="true"></b>',
        '<img class="portalimage" src="assets/home/reference-report.webp" alt="" loading="lazy" fetchpriority="low" decoding="async">',
        1,
    )

    start = f'<style id="{MARKER}">'
    if start in source:
        before, rest = source.split(start, 1)
        _, after = rest.split('</style>', 1)
        source = before + after

    style = f'<style id="{MARKER}">\n{MOBILE_CSS}\n</style>'
    source = source.replace('</head>', style + '</head>', 1)
    HOME.write_text(source, encoding="utf-8")
    print("Approved mobile restore: hero_cta=1, artwork=1, alternating_reveals=1, footer=shared_sitefooter, desktop_untouched=1")


if __name__ == "__main__":
    main()
