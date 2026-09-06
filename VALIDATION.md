# V15 release validation

Prepared on 6 September 2026.

## Passed locally

- 16 Python automated tests covering exact byline verification, manually supplied non-byline attribution, executable-HTML removal, private-network URL rejection, tracker deduplication, missing publication dates, revised article preservation, suspiciously short extraction rejection, current Drupal body/date parsing, paywall metadata refusal, failed-source preservation, draft-text exclusion and draft-cover exclusion.
- 3 JavaScript automated tests covering atomic multi-file saves, non-force branch updates, conflict handling, token clearing and refresh-dispatch payloads.
- Python build and public-output validation: 16 HTML files, including redirects and admin; all local page and asset references resolve.
- Public and admin JavaScript syntax checks.
- The footer contains no duplicate section navigation or social links. Mobile inner pages use the compact menu header; the full portrait/identity block appears only on the mobile homepage. Responsive CSS breakpoints are included.
- ZIP integrity and per-file SHA-256 manifest verification are performed during packaging.

## Included content

- Six existing user photographs, with their captions and locations.
- The identity and category imagery used by the approved prototype.
- One public full-text Daily Star article with a successfully downloaded local cover: “Why girls continue to outpace boys in SSC results”, dated 5 September 2026.
- One additional imported full-text article retained for review: “3 Public Universities: VCs’ greetings to BNP leaders raise ethical questions”. Its publication date must be checked before publication. It is excluded from the public archive.
- The prior package's eight article metadata records are retained as migration/discovery seeds, not misrepresented as full archived copies.
- Thoughts begins empty; there are no invented essays or sample articles published as genuine work.

## Live verification and limitations

The extractor was checked against real Daily Star article HTML. Live discovery, one accepted archive save and cover download completed. A further live run was interrupted by an environment approval cancellation. The included discovery state is partial. It does not establish the complete author-archive count or prove all historical pages are reachable.

The current date parser was tightened after detecting that a sidebar date could be mistaken for an article date. The regression test now includes that exact structural case. The additional uncertain record remains unpublished for review.

No GitHub account token was supplied or used. Admin writes and workflow dispatch were tested with simulated API responses, not against the user's repository. No production repository was changed, no workflow was activated, and no public deployment was performed. These must be verified after the setup steps in START-HERE.md.

Browser screenshots, browser interaction tests and real-device visual testing were not performed in this turn. The responsive styling is implemented, but this report does not claim visual approval or device-tested behaviour.

Automatic refresh is scheduled polling, subject to GitHub delays and publisher caching. Arbitrary external URLs are supported on a best-effort basis; a source may require an additional extractor. Restricted pages are not bypassed. Full-text storage and accessible cover images are implemented; inline multimedia and publisher-side interactive graphics are not mirrored.

Drafts are excluded from the public output, not hidden from a public repository's source and history. Use a private editorial service for confidential drafts.

## Checks to perform after setup

1. Confirm the first deployment succeeds and the expected public address opens.
2. Connect the studio with a repository-scoped token. Publish a short test draft, change it, then return it to draft status.
3. Upload one photograph; confirm its caption and mobile display.
4. Queue an authorised non-byline article, review its retained original byline and contribution line, then publish it.
5. Run Refresh now and a deep scan. Check timestamps, per-source warnings and discovery progress.
6. Check a saved article's local page independently of its source link. Back up the repository, including content and assets.
