# Arafat Rahaman Portfolio V15.2

This is the complete GitHub Pages repository package, not a CSS patch or a concept board. The approved monochrome identity panel, photographic home categories, compact mobile menu and minimal footer are carried into the public pages.

## 1. Before uploading

Download a backup of your current GitHub repository. Keep it until the new version has deployed successfully. This package has a new `content/` directory: it is the permanent source of stories, photographs, settings and import history. Never replace it with an older package after you start publishing.

The packaged archive is only the starting point. The first and subsequent refreshes collect every valid article listed across the configured Daily Star author pages, with no publication-review queue. The process saves its position and continues automatically until the listing is complete.

## 2. Upload the whole repository structure

Unzip the package. Upload the contents of `arafat-portfolio-v15/` into the root of `arafat-247/arafat-portfolio`, keeping the folders intact. Do not upload the ZIP itself as your website. Do not put another `arafat-portfolio-v15` folder inside the repository.

The root should contain:

```text
.github/workflows/deploy.yml
content/
scripts/
site/
tests/
START-HERE.md
README.md
```

The `site/` directory contains editable presentation files and images. `content/` stores permanent editorial records. `dist/` is the ready-built public site and is regenerated during deployment. The workflow deploys **dist**, not the source repository.

If uploading through GitHub's website loses the `.github` folder, open Add file → Create new file, name it `.github/workflows/deploy.yml`, and paste the complete workflow from this package. For the other folders, upload into each matching folder, or use GitHub Desktop to copy the complete directory structure.

Do not retain a second active deployment workflow from an old version. Replace `.github/workflows/deploy.yml` with this version. Preserve existing custom-domain settings and any CNAME you already use; set the matching URL below.

## 3. Set the public address and enable deployment

1. Open `content/settings.json`. Check `site_url`. The supplied default is `https://arafat-247.github.io/arafat-portfolio`. If using your own domain, replace it with that HTTPS address. Also check your email, LinkedIn link, biography and award details.
2. In the repository, open Settings → Pages. Choose **GitHub Actions** as the build/deployment source.
3. Open Settings → Actions → General → Workflow permissions. Allow **Read and write permissions**. If an organisation or branch rule prevents direct writes, do not weaken it blindly: ask the administrator for an approved publishing route.
4. Open Actions → **Refresh portfolio and deploy** → Run workflow. Select `main`. Use the deep-scan option for the first archive discovery run.
5. Wait for the complete run to turn green. Its deployment step provides the website address.

Scheduled runs use the default branch. This package assumes `main`; if your repository uses another branch, update the workflow, `scripts/persist.py`, and the publishing setting together.

## 4. Connect the admin studio

Open your website address followed by `/admin/`.

Create a **fine-grained GitHub personal access token**, restricted to this repository only:

- Contents: Read and write
- Actions: Read and write, for the Refresh now and Deep archive scan buttons
- Metadata: Read, normally included automatically

Use an expiry date. The token does not need permission to edit workflows because the studio writes only content and image files. Paste it into the studio, along with `arafat-247/arafat-portfolio` and `main`. GitHub enforces access; there is no hard-coded admin password. The token stays only in the current page's memory. Reloading or disconnecting clears it.

Never send your token in chat, commit it into a file, put it in the public settings, or use a broad account-wide token. If connecting fails, check repository selection, token expiry and required permissions. Do not disable branch protections to work around a rejection without understanding the implications.

## 5. Publish your own stories

Choose Write a story. Add the title, description, section, category, original publication date and text. Upload an optional cover, description and credit. Plain text supports paragraphs separated by blank lines, `## Heading`, `### Subheading`, and `> Quote`. Basic HTML is also supported; executable HTML is removed at build time.

Choose Save draft or Publish story. The studio commits the content and any cover in one update. Publication completes after the deployment run. Manage stories lets you reopen a story and edit it; save a published story as a draft to unpublish it. Its source remains in repository history. Download draft saves a local recovery copy of your text.

**Draft privacy:** drafts do not appear in public website pages, the index, RSS or sitemap. However, a public GitHub repository exposes its source files and history. Drafts and import notes are therefore not confidential in a public repository. Do not store unpublished investigations, confidential source details, credentials or sensitive notes there. A genuinely private editorial backend would require a separately configured private service or a compatible private-repository hosting plan.

## 6. Upload photographs

Choose Photographs. Select up to 12 photographs, add a caption, location, date and image description, then confirm ownership/permission. The studio resizes images to 1,800 pixels and converts them to WebP before uploading. A batch shares the entered caption and description; edit individual details afterwards. Hide removes a photograph from the gallery after deployment without deleting its original repository file. A previously public image can remain accessible by its direct URL or in history; hiding is not secure deletion.

## 7. Add a link that is not on your byline page

Choose Import a link:

1. Paste the article's public HTTPS address.
2. State your contribution, such as reporting, co-reporting, interview or research.
3. Choose a Reporting category: Event & Roundtable Coverage, Collaborative Reporting, Interview & Research Contribution or Other Reporting Contribution.
4. Confirm that you contributed and have permission to republish the text.
5. Queue the link. A deployment run imports it into the permanent archive and publishes it under Reporting. Manage stories can later correct its category, title, date or visibility.

A generic original byline such as Staff Correspondent is retained. Your contribution is displayed separately as “Portfolio contribution: Arafat Rahaman”. Another person's byline is not silently replaced with yours. This is especially important for collaborative and non-byline work.

The importer supports common structured article metadata and article-body markup, not every website. It does not bypass paywalls, logins, blocked requests or anti-bot restrictions. Failed and incomplete imports are reported in the status panel and are not published. Some websites need a source-specific parser. If necessary, use text you are authorised to republish, retaining the source and original attribution.

## 8. Automatic Daily Star updates and permanence

- Scheduled checks are requested at minutes 17, 37 and 57 each hour. This is polling, not a push feed or guaranteed real-time service.
- A deeper discovery scan is requested daily at 02:43 UTC. Refresh now and Deep archive scan are available in the studio.
- Recent listings are examined first. The collector reads every story card on each author-listing page and explores up to 180 pages, stopping on an empty or repeated page. A normal run saves up to 60 due articles; a deep run up to 180. Later scheduled runs continue the backlog automatically.
- Existing successful records are retained if an article disappears, a request fails, a byline changes or extraction becomes suspiciously shorter.
- Article bodies, source metadata and progress are committed to the repository **before** deployment. They are not dependent on an Actions cache. Publisher cover images are deliberately omitted for speed and a cleaner archive.
- Changed saved content creates a revision file; Git history also retains committed versions. The public site uses the current accepted copy.
- Inline source graphics, publisher covers, embeds, video and interactive elements are not mirrored; the archive preserves article text, basic formatting, attribution and the original-source link.

GitHub can delay or drop scheduled jobs during heavy load, and public-repository schedules may be disabled after inactivity. The Daily Star may also serve cached listings. Use the studio's timestamps, queue and deployment status to see what actually happened. Do not interpret a scheduled time as a guaranteed publication deadline.

Keep periodic offline repository backups. “Permanent” here means retained in your repository and rebuilt independently of the source; it does not protect against deleting the repository, losing the account, or removing its history.

## 9. Local preview

Python 3.12 or newer is enough for the V15 build and importer; no npm installation is needed for the public site.

```bash
python scripts/migrate.py
python scripts/build.py
python scripts/validate.py
python -m http.server 8000 --directory dist
```

Visit `http://localhost:8000`. Do not open the HTML with `file://`: archive loading and admin modules need an HTTP server. The public site works without a running Python server after deployment; Python runs only during builds and imports.

## Source documentation

- [GitHub Pages deployment with Actions](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
- [Scheduled workflow limitations](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
- [GitHub's workflow dispatch API](https://docs.github.com/en/rest/actions/workflows#create-a-workflow-dispatch-event)
- [Git trees and atomic multi-file updates](https://docs.github.com/en/rest/git/trees)
- [The Daily Star author page](https://www.thedailystar.net/author/arafat-rahaman)
