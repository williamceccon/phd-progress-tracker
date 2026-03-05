# Review Report — web-tests-v2-polish

Date: 2026-03-05

## Review Plan

### Code Changes to Review

| Layer | File | Change Type | Priority |
|-------|------|-------------|----------|
| Frontend | `web/lib/api.ts` | Modify - Remove `/api` prefix | Critical |
| Frontend | `web/components/MilestoneList.tsx` | Modify - Fix text | Medium |
| Config | `pyproject.toml` | Modify - Version bump | Low |
| Config | `web/package.json` | Modify - Test deps + version | Medium |
| Tests | `web/tests/*.test.tsx` | Create - 5 test files | High |

### Review Checklist

#### Critical (Must Fix)
- [ ] API endpoints in `web/lib/api.ts` no longer use `/api` prefix
- [ ] Task creation POST returns 201 (test via curl)
- [ ] Milestone creation POST returns 201 (test via curl)

#### High Priority
- [ ] All 5 frontend test files exist and are syntactically valid
- [ ] Vitest configuration is correct (`web/vitest.config.ts`)
- [ ] Test setup file exists (`web/tests/setup.ts`)

#### Medium Priority
- [ ] Text "dias para frente" in MilestoneList.tsx (line ~150)
- [ ] Version 2.0.0 in `pyproject.toml`
- [ ] Version 2.0.0 in `web/package.json`
- [ ] Test dependencies added to `web/package.json`

#### Low Priority
- [ ] `web/README.md` exists and is complete
- [ ] Root `README.md` updated for v2.0
- [ ] `web/tests/TEST_PLAN.md` exists

### Code Quality Standards

Per AGENTS.md:
- Python: black (formatter) + flake8 (linter)
- Frontend: ESLint + Prettier (if configured)
- Coverage: 100% (no new `pragma: no cover`)

### Lint/Format Commands

```bash
# Python backend
poetry run flake8 phd_progress_tracker/ tests/
poetry run black phd_progress_tracker/ tests/

# Frontend (if configured)
cd web && npm run lint
```

### Risk Assessment

| Risk | Impact | Likelihood | Notes |
|------|--------|------------|-------|
| Route fix breaks other integrations | Medium | Low | Test all API endpoints |
| Vitest config conflicts with Next.js | Low | Low | Use jsdom environment |
| Frontend tests fail on CI | Medium | Medium | Ensure jsdom environment |

### Notes

- Focus review on critical bug fix (API route prefix removal)
- Verify test files compile and follow React Testing Library best practices
- Check that version bump is consistent across both pyproject.toml and package.json
