# Public Release Checklist — CDP v0.1.0

Use this checklist before making the repository public or tagging a release.

## Repository Hygiene

- [x] `.idea/` and other IDE artifacts removed from version control
- [x] `.gitignore` covers common local artifacts (`.idea/`, `.vscode/`, `.env`, `__pycache__/`, etc.)
- [x] No secrets, credentials, or internal URLs in source files
- [x] `.env.example` contains only safe placeholder values
- [x] `NOTICE` file is up to date

## Documentation

- [x] `README.md` includes status line, quickstart, architecture, and contribution guidance
- [x] `CHANGELOG.md` is present and up to date
- [x] `CONTRIBUTING.md` references correct repository URL
- [x] `CODE_OF_CONDUCT.md` is present
- [x] `SECURITY.md` describes vulnerability reporting process
- [x] `LICENSE` (Apache 2.0) is present
- [x] `docs/known-limitations.md` documents current limitations
- [x] `docs/releases/v0.1.0.md` is ready to copy into GitHub Release description

## Code Quality

- [x] `ruff check adp/ tests/ examples/` passes with no errors
- [x] All unit tests pass: `pytest tests/unit/ -v`
- [x] All functional tests pass: `pytest tests/functional/ -v`
- [x] Schema validation passes: `pytest tests/schema_validation/ -v`
- [x] Protocol vector validation passes: `pytest tests/protocol_vectors/ -v`
- [x] Interoperability tests pass: `pytest tests/interoperability/ -v`

## CI / GitHub Configuration

- [x] `.github/workflows/ci.yml` is present and runs on push and PR
- [x] `CODEOWNERS` is present
- [x] Issue templates exist for bug reports, feature requests, and protocol changes
- [x] Pull request template is present

## GitHub UI Steps (manual — cannot be automated via code)

- [ ] Set repository description to the suggested value in `docs/github-repo-metadata.md`
- [ ] Add repository topics from `docs/github-repo-metadata.md`
- [ ] Set repository website URL if applicable
- [ ] Make repository public (Settings → Danger Zone → Change visibility)
- [ ] Create the `v0.1.0` tag and publish a GitHub Release using `docs/releases/v0.1.0.md`
- [ ] Enable GitHub Discussions if community Q&A is desired
- [ ] Pin the repository to your GitHub profile if desired
- [ ] Review branch protection rules for `main`
