# Arafat Rahaman Portfolio V16.4

Start with [START-HERE.md](START-HERE.md) for installation, GitHub Pages setup, admin access, publishing and archive operation.

This release provides a compact, responsive portfolio; a GitHub-backed publishing studio; separately organised Reporting, Opinion & Analysis and Thoughts; uploaded photography; durable Daily Star article storage; scheduled full-author-page discovery; and categorised manual URL imports.

The admin is protected by GitHub repository permissions. It is not a separate username/password server. The public site is static; GitHub Actions performs imports and publication.

## Build

```bash
python scripts/migrate.py
python scripts/build.py
python scripts/validate.py
```

## Test

```bash
python -m unittest discover -s tests -p 'test_*.py'
node --test tests/github.test.mjs
```

Python 3.12+ is sufficient for build/import. Node is only needed to run the JavaScript unit tests. No external Python packages are required by the V15 scripts.

## Durable files

- `content/articles/`: full accepted imported text and metadata, one file per URL-derived ID.
- `content/revisions/`: previous accepted content when a source changes.
- `content/posts.json`: authored stories and drafts.
- `content/photos.json`: uploaded photograph metadata.
- `content/imports.json`: manually queued source links and contribution declarations.
- `content/overrides.json`: optional corrections to publication state, dates and categories.
- `content/settings.json`: site identity, address, contact and recognition.
- `content/sync-state.json`: discovery progress, timestamps and per-source errors.
- `site/assets/`: user photographs and identity imagery. Publisher article covers are not used by public work indexes.
- `dist/`: generated public output only.

Do not treat Actions cache as an archive, overwrite `content/` with an old release, or force-push over editorial changes. Keep offline backups. Public-repository drafts are not confidential.

See [VALIDATION.md](VALIDATION.md) for what has and has not been tested. Original publisher attribution is preserved for manual imports; verify republication permission before use.
