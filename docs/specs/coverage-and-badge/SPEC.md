# SPEC — Coverage 100% and Codecov Badge

## Overview

This spec defines the implementation to achieve 100% test coverage by adding a pragma comment to exclude the untestable `if __name__ == "__main__"` entry point, configure GitHub Actions CI to generate coverage reports, and display a Codecov badge in the README.

---

## Files to Create

None. This feature modifies only existing files.

---

## Files to Modify

### 1. `phd_progress_tracker/main.py`

| Line | Change |
|------|--------|
| 25 | Add `# pragma: no cover` comment to the `if __name__ == "__main__":` line |

**Reason:** Exclude the entry point from coverage as it cannot be tested in the normal test flow.

**After change (lines 24-26):**
```python
if __name__ == "__main__":  # pragma: no cover
    app()
```

---

### 2. `.github/workflows/ci.yml`

| Line | Change |
|------|--------|
| 57 | Add `--cov=phd_progress_tracker --cov-report=xml` flags to the pytest command |

**Reason:** Generate coverage.xml file for Codecov upload.

**Current line 57:**
```yaml
      - name: Pytest + Coverage
        run: poetry run pytest tests/ -v --tb=short
```

**After change:**
```yaml
      - name: Pytest + Coverage
        run: poetry run pytest tests/ -v --tb=short --cov=phd_progress_tracker --cov-report=xml
```

---

### 3. `README.md`

| Line | Change |
|------|--------|
| 5 | Replace placeholder badge URL `<user>/<repo>` with actual repo path `williamceccon/phd-progress-tracker` |

**Reason:** Display correct clickable Codecov badge.

**Current line 5:**
```markdown
![Coverage](https://codecov.io/gh/<user>/<repo>/badge.svg)
```

**After change:**
```markdown
![Coverage](https://codecov.io/gh/williamceccon/phd-progress-tracker/badge.svg)
```

---

## Implementation Tasks

1. **Modify `phd_progress_tracker/main.py`** — Add `# pragma: no cover` to line 25
2. **Modify `.github/workflows/ci.yml`** — Add `--cov=phd_progress_tracker --cov-report=xml` to pytest command on line 57
3. **Modify `README.md`** — Replace `<user>/<repo>` placeholder with `williamceccon/phd-progress-tracker` on line 5
4. **Verify locally** — Run `poetry run pytest --cov=phd_progress_tracker --cov-report=term-missing` to confirm 100% coverage
5. **Commit and push** — Create a branch and push changes (commit message: `ci(config): add coverage reporting and Codecov badge`)

---

## Test Plan

No test files need to be created or modified. The implementation is verified by:

1. **Local coverage check:**
   - Run: `poetry run pytest --cov=phd_progress_tracker --cov-report=term-missing`
   - Expected: 100% coverage reported

2. **CI pipeline validation:**
   - After pushing to a branch, verify GitHub Actions runs successfully
   - Check Codecov dashboard shows the repository with coverage data

3. **README badge validation:**
   - Verify the badge URL on line 5 is properly formatted and clickable
   - Badge should link to `https://codecov.io/gh/williamceccon/phd-progress-tracker`

---

## Risks & Side Effects

- **Low Risk:** The `# pragma: no cover` is the standard approach for coverage.py and is already configured in `pyproject.toml` (line 38-39).
- **Note:** User must manually connect the repository to Codecov by logging into Codecov and adding the repo.
- **Note:** For public repositories, no CODECOV_TOKEN is required. The CI workflow is already configured to use `codecov/codecov-action@v5`.

---

## Open Questions

None. All necessary information is available in the PRD and codebase.
