"""Mirror the finished homepage at the historic desktop preview URL."""
from pathlib import Path

root = Path(__file__).resolve().parents[1] / 'dist'
home = (root / 'index.html').read_text(encoding='utf-8')
home = home.replace('<head>', '<head><base href="/"><meta name="robots" content="noindex,nofollow">', 1)
target = root / 'desktop-preview' / 'index.html'
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(home, encoding='utf-8')
print('Desktop preview mirrors current homepage')
