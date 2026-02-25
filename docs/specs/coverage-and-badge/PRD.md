# PRD — Coverage 100% and Codecov Badge

## Overview

This feature achieves 100% test coverage by marking the untestable `if __name__ == "__main__"` entry point with a pragma comment, creates the GitHub Actions CI pipeline with coverage reporting, and displays a Codecov badge in the README.

**Project Phase:** CI/CD and quality infrastructure  
**Feature Slug:** coverage-and-badge

---

## Affected Files

| File | Action | Notes |
|------|--------|-------|
| `phd_progress_tracker/main.py` | Modify | Add `# pragma: no cover` to line 25 |
| `.github/workflows/ci.yml` | Modify | Add --cov flags to pytest step only |
| `README.md` | Modify | Update Codecov badge URL with correct repo path |
| `.gitignore` | No change | Already contains `coverage.xml` |
| `pyproject.toml` | No change | pytest-cov already in dev dependencies |

---

## Implementation Plan

1. **Add pragma comment to main.py** — Insert `# pragma: no cover` on the `if __name__ == "__main__":` line (line 25) to exclude it from coverage.

2. Modify pytest step in ci.yml — add --cov=phd_progress_tracker
   and --cov-report=xml flags to the existing pytest command
   - Python setup (3.12)
   - Poetry installation
   - pytest with `--cov=phd_progress_tracker --cov-report=xml` flags
   - flake8, black, mypy checks
   - Codecov upload step using `codecov/codecov-action`

3. **Update README badge** — Replace the placeholder badge URL on line 5 with the correct format: `https://codecov.io/gh/<owner>/<repo>/branch/main/graph/badge.svg`

4. **Verify locally** — Run `poetry run pytest --cov=phd_progress_tracker` to confirm 100% coverage.

5. **Push and validate CI** — Push to a branch, verify CI passes end-to-end, and confirm Codecov dashboard shows the repository.

---

## API / Schema Design

Not applicable. This is a CI/CD and tooling feature, not an API change.

---

## Functional Requirements

- The `if __name__ == "__main__"` line in `main.py` must be excluded from coverage using the `# pragma: no cover` comment.
- The local pytest command `poetry run pytest --cov=phd_progress_tracker` must report 100% coverage.
- The GitHub Actions workflow must run on every push and pull request.
- The pytest step must generate `coverage.xml` and upload it to Codecov.
- The README.md must display a clickable Codecov badge linking to the project dashboard.

---

## Non-Functional Requirements

- **Test coverage:** Must reach 100% after the pragma comment is added.
- **CI reliability:** Pipeline must remain green after changes; no modifications to test logic or source behavior.
- **Dependencies:** No new runtime dependencies; Codecov integration uses `codecov/codecov-action` (CI-only).
- **Code style:** Must follow existing conventions (black formatting, flake8 compliance).

---

## Out of Scope

- Enforcing minimum coverage thresholds in CI (e.g., failing builds below 100%).
- Adding badges other than Codecov.
- Modifying any test files or business logic.
- Creating a Codecov account — this must be done manually by the user.
- Adding mypy strict rules or other linter enhancements.

---

## Risks & Side Effects

- **Risk:** The `# pragma: no cover` comment is specific to coverage.py. If pytest-cov configuration changes, the exclusion may not work. *Mitigation:* The pragma is the standard approach and is already configured in `pyproject.toml`.
- **Risk:** Codecov upload may fail if the repository is not connected to Codecov. *Mitigation:* The BRIEF notes this must be done manually; the PR should include a note reminding the user to connect the repo.
- **Risk:** The README already contains a badge (line 7) with a token. If the token is revoked, the badge breaks. *Mitigation:* Use the token-free badge format (line 5) which is the recommended approach for public repos.

---

## Open Questions

- **Codecov token:** Does Codecov require a `CODECOV_TOKEN` secret in GitHub Actions for public repositories, or is the upload automatic? The `codecov/codecov-action` typically works without a token for public repos, but a token may be needed for private repos.

---

## Success Criteria

- [ ] `poetry run pytest --cov=phd_progress_tracker` reports 100% coverage locally
- [ ] `.github/workflows/ci.yml` includes `--cov=phd_progress_tracker --cov-report=xml` in the pytest step
- [ ] CI/CD pipeline passes end-to-end on GitHub after push
- [ ] Codecov dashboard shows the repository with coverage data
- [ ] README.md displays the correct Codecov badge with proper repo link
- [ ] Commit follows the `ci(config):` or `docs(readme):` convention

