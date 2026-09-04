# Arafat Rahaman — V13

A complete personal journalism archive and publishing site for GitHub Pages.

## Included

- Distinct desktop and mobile home designs.
- Published Work, Journal, Photography, About and Contact pages.
- Permanent local reading pages for verified work from The Daily Star.
- Automatic archive refresh every six hours.
- Default, Light and Dark appearance controls.
- Editorial display type for story headlines and a reading serif for body copy.
- Search, topic, type, year and chronology controls.
- Source labels, original links, RSS, sitemap, print/PDF and sharing tools.
- A browser-based publishing studio at `/admin/` for Journal stories and photography.
- Responsive layouts, keyboard navigation and reduced-motion support.

## Deploy the complete site

1. Open the `arafat-247/arafat-portfolio` repository on GitHub.
2. Back up the current repository or create a release before replacing files.
3. Upload everything inside this package to the repository root. Keep the supplied folder structure and allow GitHub to replace matching files.
4. In **Settings → Pages**, set **Source** to **GitHub Actions**.
5. Open **Actions → Refresh portfolio and deploy → Run workflow**.
6. The workflow optimises photographs, refreshes the verified archive, checks the build and deploys the `site/` folder.

The public site is configured for `https://arafat-247.github.io/arafat-portfolio/`.

## Use the private publishing studio

Open `https://arafat-247.github.io/arafat-portfolio/admin/`.

Create a fine-grained GitHub personal access token restricted to this repository with **Contents: Read and write** permission. Paste it into the studio when you need to publish. The token is kept only in the browser tab when the checkbox is selected; it is never committed to the repository.

The studio can:

- create and edit Journal stories;
- save drafts or publish;
- add a cover photograph;
- upload multiple gallery photographs;
- compress uploads to WebP;
- update the underlying JSON through GitHub commits.

Every studio commit triggers the deployment workflow. GitHub Pages updates after that workflow completes.

## Local preview

Run from the repository root:

```bash
python -m pip install -r requirements.txt
python scripts/optimise_images.py
python -m http.server 8000 --directory site
```

Then open `http://localhost:8000`. Do not open `site/index.html` directly because browsers can block JSON loading from `file://` URLs.

## Content locations

- `site/data/journal-index.json` — original Journal stories.
- `site/data/photography.json` — photography gallery.
- `site/data/articles.json` — full verified Published Work archive after refresh.
- `site/data/archive-index.json` — lightweight catalogue generated from the archive.
- `site/assets/uploads/` — images sent through the studio.
- `site/assets/photography-src/` — original gallery source photographs added manually.
- `site/data/story_enhancements.json` — optional story modules and source documents.

## Archive behaviour

The archive script verifies Arafat Rahaman's byline before saving a story. It generates a permanent local reading page, preserves the source URL and publication date, and marks the copy as `noindex` with the original article as canonical. Review publication rights and newsroom policy before publicly reproducing full articles.

## Security

- Never commit a GitHub token, password or private key.
- Use a fine-grained token limited to this repository.
- Revoke the token if a shared device was used.
- The `/admin/` page contains no credentials; publishing access depends on GitHub authentication.

## Main files

- `site/index.html` and `site/styles.css` — V13 design.
- `site/common.js` — theme, navigation and shared data handling.
- `site/admin/` — publishing studio.
- `scripts/update_articles.py` — verified Daily Star archive builder.
- `scripts/optimise_images.py` — photograph optimisation.
- `.github/workflows/deploy.yml` — refresh, checks and deployment.
