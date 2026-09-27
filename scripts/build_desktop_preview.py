"""Build /desktop-preview/ from the exact live reference desk composition."""
from pathlib import Path
import re

from reference_desk import DESK

ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / 'dist' / 'index.html'
PREVIEW = ROOT / 'dist' / 'desktop-preview' / 'index.html'


def replace_desk_section(source: str, replacement: str) -> str:
    start_match = re.search(r'<section\s+class="[^"]*\bdeskhome\b[^"]*"[^>]*>', source, flags=re.I)
    if not start_match:
        raise RuntimeError('Desk homepage section not found')
    token_re = re.compile(r'<section\b[^>]*>|</section>', re.I)
    depth = 0
    end = None
    for match in token_re.finditer(source, start_match.start()):
        token = match.group(0).lower()
        if token.startswith('<section'):
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                end = match.end()
                break
    if end is None:
        raise RuntimeError('Desk homepage section is not balanced')
    return source[:start_match.start()] + replacement + source[end:]


def main():
    source = HOME.read_text(encoding='utf-8')
    preview_desk = DESK.replace('href="./"', 'href="desktop-preview/"', 1)
    source = replace_desk_section(source, preview_desk)
    source = source.replace('<head>', '<head><base href="/"><meta name="robots" content="noindex,nofollow">', 1)
    source = source.replace('href="#main"', 'href="desktop-preview/#main"', 1)
    PREVIEW.parent.mkdir(parents=True, exist_ok=True)
    PREVIEW.write_text(source, encoding='utf-8')
    print('Reference desk preview built from the same desktop composition used live')


if __name__ == '__main__':
    main()
