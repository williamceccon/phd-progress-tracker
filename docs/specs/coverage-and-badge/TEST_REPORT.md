# Test Report — coverage-and-badge
Date: Wed Feb 25 2026

## Results
============================= test session starts ==============================
platform darwin -- Python 3.12.12, pytest-9.0.2, pluggy-1.6.0
rootdir: /Users/williamfelipeseccon/Documents/Programação/phd-progress-tracker
configfile: pyproject.toml
plugins: cov-7.0.0
collected 72 items

tests/test_basic.py ...                                                  [  4%]
tests/test_commands.py .....................                             [ 33%]
tests/test_database.py .........                                         [ 45%]
tests/test_helpers.py ...........                                        [ 61%]
tests/test_main.py ...                                                   [ 65%]
tests/test_milestone.py .........                                        [ 77%]
tests/test_task.py ................                                      [100%]

================================ tests coverage ================================
______________ coverage: platform darwin, python 3.12.12-final-0 _______________

Name                                        Stmts   Miss  Cover   Missing
-------------------------------------------------------------------------
phd_progress_tracker/__init__.py                2      0   100%
phd_progress_tracker/cli/__init__.py            2      0   100%
phd_progress_tracker/cli/commands.py          143      0   100%
phd_progress_tracker/main.py                   10      0   100%
phd_progress_tracker/models/__init__.py         0      0   100%
phd_progress_tracker/models/milestone.py       17      0   100%
phd_progress_tracker/models/task.py            38      0   100%
phd_progress_tracker/utils/__init__.py          0      0   100%
phd_progress_tracker/utils/database.py         31      0   100%
phd_progress_tracker/utils/date_helper.py      29      0   100%
-------------------------------------------------------------------------
TOTAL                                         272      0   100%
Coverage XML written to file coverage.xml
============================== 72 passed in 3.25s ==============================

## Verdict
- 72 passing / 0 failing
- Coverage per module: 🟢 100% (all modules)

---

## Fix Round 1 — Wed Feb 25 2026

### Issues Fixed
1. **🔴 High** — Removed unused `Progress` import from `phd_progress_tracker/cli/commands.py:12`
2. **🔴 High** — Removed unused `json` and `patch` imports from `tests/test_commands.py:1,3`
3. **🟢 Low** — Removed duplicate Codecov badge from README.md
4. **Security** — Removed exposed Codecov token from README badge URL

### Results
============================= test session starts ==============================
platform darwin -- Python 3.12.12, pytest-9.0.2, pluggy-1.6.0
rootdir: /Users/williamfelipeseccon/Documents/Programação/phd-progress-tracker
configfile: pyproject.toml
plugins: cov-7.0.0
collected 72 items

tests/test_basic.py ...                                                  [  4%]
tests/test_commands.py .....................                             [ 33%]
tests/test_database.py .........                                         [ 45%]
tests/test_helpers.py ...........                                        [ 61%]
tests/test_main.py ...                                                   [ 65%]
tests/test_milestone.py .........                                        [ 77%]
tests/test_task.py ................                                      [100%]

================================ tests coverage ================================
______________ coverage: platform darwin, python 3.12.12-final-0 _______________

Name                                        Stmts   Miss  Cover   Missing
-------------------------------------------------------------------------
phd_progress_tracker/__init__.py                2      0   100%
phd_progress_tracker/cli/__init__.py            2      0   100%
phd_progress_tracker/cli/commands.py          142      0   100%
phd_progress_tracker/main.py                   10      0   100%
phd_progress_tracker/models/__init__.py         0      0   100%
phd_progress_tracker/models/milestone.py       17      0   100%
phd_progress_tracker/models/task.py            38      0   100%
phd_progress_tracker/utils/__init__.py         0      0   100%
phd_progress_tracker/utils/database.py         31      0   100%
phd_progress_tracker/utils/date_helper.py      29      0   100%
-------------------------------------------------------------------------
TOTAL                                         271      0   100%
Coverage XML written to file coverage.xml
============================== 72 passed in 3.54s ==============================

### Flake8 Check
- `phd_progress_tracker/cli/commands.py` — ✅ 0 errors
- `tests/test_commands.py` — ✅ 0 errors

## Verdict
- 72 passing / 0 failing
- Coverage per module: 🟢 100% (all modules)
