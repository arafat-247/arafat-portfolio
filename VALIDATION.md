# V16.4 release validation

Prepared on 6 September 2026.

## Passed locally

- 20 Python tests, including every-card author-list discovery, clean headline URLs, legacy redirects, author-list provenance, exact bylines, manual contribution attribution, sanitisation, URL safety, draft exclusion, revision preservation and failed-source preservation.
- 3 JavaScript tests covering atomic GitHub saves, branch conflicts and bounded workflow dispatch.
- Public and admin JavaScript syntax checks.
- Build and output validation: local links, assets, safe attributes, JSON indexes, redirects and draft exclusion.
- The release ZIP is integrity-tested and contains a SHA-256 manifest.

## V16.4 behaviour

- Every valid story card found on the configured Daily Star author pages enters the permanent archive and publishes without an editorial review queue.
- Article pages keep the original source byline and original-publication link.
- Opinion and analysis URLs/sections are separated from Reporting automatically.
- Manually pasted contribution links publish within Reporting under the selected contribution category.
- Publisher cover images are not copied or displayed in Reporting and Opinion archives. Homepage identity imagery and the separate Photography gallery remain.
- About contains biography, reporting areas, Awards & Recognition and a contact route. The old awards address redirects to this section.
- Mobile inner pages use a compact sticky header and an overlay drawer instead of repeating the portrait panel above every page.
- Article addresses use readable headline slugs; previous ID-led addresses remain as permanent compatibility redirects.
- Canonical, Open Graph and X metadata use the custom domain and the branded 1200 × 630 sharing card.
- The About page identifies Arafat Rahaman through ProfilePage and Person data, and every matching bylined article links to that same permanent author identity. Non-byline contributions remain unlinked.
- Article sharing uses the device's native sharing sheet where available and a Facebook, WhatsApp, X, LinkedIn and copy-link window elsewhere.

## Operational limits

The Daily Star archive is collected progressively because GitHub Actions and the publisher impose practical run-time limits. A normal run saves up to 60 due stories; a deep run up to 180. Scheduled runs continue until the author listing and pending queue are complete. A failed, restricted or structurally incomplete extraction is logged and is not falsely presented as archived.

The static public site needs no installed software. GitHub Actions runs Python for discovery, validation, rebuilding and deployment. Scheduled execution can be delayed by GitHub, and a source-site markup change can require an extractor update.

No production repository credentials were supplied or used during local validation. After uploading the update, run **Deep archive scan** once, then allow scheduled runs to continue the backlog.
