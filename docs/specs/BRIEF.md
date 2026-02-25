# BRIEF — Coverage 100% and Codecov Badge
Date: 2026-02-25
Slug: coverage-and-badge

---

## What I want
Reach 100% test coverage by adding `# pragma: no cover` to main.py line 26,
integrate Codecov into the GitHub Actions CI pipeline, and display the
Codecov badge in README.md.

---

## Why it matters
The project sits at 99% coverage due to a single untestable line
(`if __name__ == "__main__"`). Closing this gap makes the coverage
contract explicit, adds a visible quality signal to the repository,
and establishes the Codecov integration before more complex features
are added. A coverage badge is also a strong portfolio signal.

---

## Context
- `phd_progress_tracker/main.py` line 26 has `if __name__ == "__main__"` —
  the only uncovered line
- CI/CD is configured at `.github/workflows/ci.yml` with pytest, flake8,
  black and mypy — currently missing `--cov` flags in the pytest step
- The pytest step does not generate `coverage.xml` yet — must be added
- README.md exists but has no badges
- `coverage.xml` is already in `.gitignore` — correct, it is generated
  at runtime by pytest in the CI runner
- Codecov account needs to be created at codecov.io and connected
  to the GitHub repository

---

## Constraints
- Must not modify any test logic or source behavior
- `# pragma: no cover` must be used only on the `if __name__ == "__main__"` line
- CI/CD pipeline must remain green after all changes
- No new runtime dependencies — Codecov is CI-only (codecov-action)
- pytest step in ci.yml must generate coverage.xml for the Codecov upload
  step that already exists in the workflow

---

## Expected behavior
- Running `poetry run pytest --cov=phd_progress_tracker --cov-report=term-missing`
  locally reports 100% coverage with no missing lines
- Every push to GitHub triggers CI, which runs tests, generates coverage.xml
  and uploads to Codecov automatically
- README.md displays a Codecov badge reflecting current coverage
- Clicking the badge opens the Codecov dashboard for this repository

---

## Out of scope
- Enforcing minimum coverage threshold in CI (e.g. fail if below 100%)
- Adding any other badges beyond Codecov
- Modifying any existing tests or source logic beyond the pragma comment
- Creating a Codecov account — this must be done manually before running /code

---

## Success criteria
- [ ] `poetry run pytest --cov=phd_progress_tracker` reports 100% locally
- [ ] ci.yml pytest step includes `--cov=phd_progress_tracker --cov-report=xml`
- [ ] CI/CD pipeline passes end-to-end on GitHub after push
- [ ] Codecov dashboard shows 100% for the repository
- [ ] README.md displays the Codecov badge with correct repo link
- [ ] Commit follows `ci(config):` or `docs(readme):` convention

---

## Open questions
- Does Codecov require a CODECOV_TOKEN secret in GitHub Actions for
  public repositories, or is the upload automatic?
