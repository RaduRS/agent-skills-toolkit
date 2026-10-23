# Taste assessment — not installed

Reviewed candidate: `Leonxlnx/taste-skill`, revision `6010f91a9935f1c167dfc500fb1a475681892e6b`, skill `design-taste-frontend`. MIT, copyright (c) 2026 Leonxlnx. No upstream Taste payload is included in this toolkit or installed user-wide.

## Recommendation

Leave Taste out of the global default toolkit. Its subject inventory, claims-with-proof approach and screenshot critique are useful ideas, but its broad auto-trigger overlaps the existing Frontend Design plugin and UI/UX Pro Max. Its default gates enforce a specific house style, which can conflict with a client's established identity. It is a potential explicit, per-project art-direction reference after adapting the browser workflow and treating style findings as advisory.

## Bounded local trial

Only the complete, reviewed `scripts/lint.mjs` was executed, using the existing Node 24 runtime with a 64 MB heap cap and 10-second timeout, against two synthetic HTML files in an isolated temporary directory. No real project/customer files were scanned. The linter has only Node filesystem-read and path imports; it did not mutate either fixture or create history/artifact files.

- `clean.html`: exit 0, one file, zero findings.
- `brand.html`: exit 1, two FAIL findings: `font-family:monospace` and `#6366f1`. The fixture explicitly describes a synthetic type foundry whose brand requires those choices. The linter cannot determine that contextual requirement from its regex checks.

See `taste-trial-results.json` for exact findings. This establishes linter behavior, not comparative visual quality or end-to-end browser compatibility. It is not an A/B website design evaluation.

## Reviewed side effects and limits

The review covered the SKILL run/house-rule sections, the full static linter, browser/profile-management code and asset-helper network/write call sites. It was not a complete security audit of every library asset or script.

- `draw.mjs` writes project direction files and user-level history at `~/.taste-skill/history.json` by default; `TASTE_SKILL_HISTORY` can relocate history.
- `inspect.mjs` starts its own browser via a custom CDP client, writes screenshots/report data, and removes matching screenshots from the chosen output directory before running. Its CDP helper creates/cleans temporary browser profiles and terminates its launched browser process. This environment requires browser work through its provided CUA browser tools, so that inspector was not executed through an alternate automation route.
- `assets.mjs` sends search queries to external open-collection services and can download image/video assets and write credit records. It was not executed. No queries, private data, credentials or customer content were sent through it.
- The style gate bans or flags choices including monospace, violet/indigo, gradients, small section labels and dividers. Those are editorial defaults, not universal accessibility or engineering requirements. The source does provide exception mechanisms; no exceptions were configured in this trial.

No Taste dependency installation, remote CLI, browser automation, asset fetching, drawing/history mutation or global installation occurred. No approval denial is outstanding. A future full integration needs an explicit project scope and a host-compatible inspection path; it should preserve user brand/content constraints and keep external asset lookup separately authorized.
