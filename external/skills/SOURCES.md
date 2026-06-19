# External Skill Sources

These external Skills were downloaded after user approval and are vendored as source snapshots for project-autopilot integration.

## nuwa-skill

- Source: https://github.com/alchaincyf/nuwa-skill
- Downloaded commit: `f4c9bc3f8df2cc036f9bed47ac2fecf56c366555`
- Local path: `external/skills/nuwa-skill`
- Notes: `.git` metadata, `promo/`, `examples/`, QR-code image, and large promotional images were removed before publishing to avoid nested Git history, promotional bulk assets, sample-data false-positive secrets/local paths, QR-code privacy risk, and repository bloat.

## darwin-skill

- Source: https://github.com/alchaincyf/darwin-skill
- Downloaded commit: `7c7b7909b630dc3b5cbb91bd4bcb1b10bfb1f894`
- Local path: `external/skills/darwin-skill`
- Notes: `.git` metadata was removed before publishing to avoid nested Git history. One script was adjusted to load `playwright-core` from the active environment instead of an upstream author-local absolute path.
