# Arafat Rahaman — reporting portfolio

A free, static reporting portfolio designed for GitHub Pages.

## What is included

- Responsive one-page portfolio.
- Search and section filters.
- Seed archive based on Arafat Rahaman's public Daily Star author page.
- Automatic index refresh every six hours through GitHub Actions.
- GitHub Pages deployment workflow.
- No database and no paid server required.

The automated index stores only discovery metadata: headline, date, section,
short description, optional Open Graph image URL and the original Daily Star link.
Full stories remain on the publisher's website.

## Free deployment

1. Create a new **public** GitHub repository, for example `arafat-portfolio`.
2. Upload the contents of this folder to the repository root.
3. Open **Settings → Pages**.
4. Under **Build and deployment → Source**, choose **GitHub Actions**.
5. Open **Actions** and run `Refresh portfolio and deploy`, or push any commit.
6. When the workflow finishes, GitHub shows the public Pages URL.

For a repository called `arafat-portfolio`, the usual project-site form is:

    https://YOUR-GITHUB-USERNAME.github.io/arafat-portfolio/

If you later create a repository named exactly `YOUR-GITHUB-USERNAME.github.io`,
the site can instead live at the account root.

## Local preview

From the repository root:

    python -m http.server 8000 --directory site

Then open:

    http://localhost:8000

## Refresh locally

    python -m pip install -r requirements.txt
    python scripts/update_articles.py --limit 40

## Files

- `site/index.html` — page structure
- `site/styles.css` — visual design
- `site/app.js` — archive rendering, search and filters
- `site/data/articles.json` — portfolio data
- `scripts/update_articles.py` — Daily Star indexer
- `.github/workflows/deploy.yml` — automatic refresh and Pages deployment

## Important

The Daily Star author page carries a notice against unauthorised commercial
reproduction. This build therefore functions as a portfolio index and sends
readers to the original story rather than mirroring full article text.
