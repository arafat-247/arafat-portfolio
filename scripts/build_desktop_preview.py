"""Mirror the finished homepage at /desktop-preview/ for visual review.

The preview must never carry its own desktop renderer. It is intentionally the
same built homepage, with only a root base URL and noindex metadata added.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "dist" / "index.html"
PREVIEW = ROOT / "dist" / "desktop-preview" / "index.html"


def main() -> None:
    if not HOME.is_file():
        raise FileNotFoundError("dist/index.html does not exist; run the site build first")

    source = HOME.read_text(encoding="utf-8")

    # Guard against the rejected baked desktop poster returning to the rendered
    # homepage. The source asset may remain in the repository archive, but it
    # must not be referenced by the built homepage or its preview.
    if "assets/home/approved-desk-desktop.webp" in source:
        raise RuntimeError("Desktop preview refused: rejected static desk poster is referenced")

    preview = source.replace(
        "<head>",
        '<head><base href="/"><meta name="robots" content="noindex,nofollow">',
        1,
    )
    preview = preview.replace('href="#main"', 'href="desktop-preview/#main"', 1)

    PREVIEW.parent.mkdir(parents=True, exist_ok=True)
    PREVIEW.write_text(preview, encoding="utf-8")
    print("Desktop preview mirrors the rebuilt homepage exactly; no preview overlay renderer")


if __name__ == "__main__":
    main()
