# Sortie 2: Fix Existing Code

**Sprint**: 1 - Pre-commit & Code Quality  
**Sortie**: 2 of 4  
**Estimated Time**: 2-3 hours  
**Dependencies**: Sortie 1 (pre-commit configured)  
**Status**: 📋 Ready to Start (after Sortie 1)

---

## Overview

Run pre-commit hooks on the entire codebase to identify and fix existing formatting/linting issues. This sortie ensures all code meets quality standards before enforcing them on new commits.

**What this achieves**: Clean baseline for code quality enforcement.

**Why it's a logical unit**: Must fix existing issues before enforcing standards going forward. All fixes can be reviewed in a single commit.

---

## Scope and Non-Goals

### Included
- ✅ Run `pre-commit run --all-files`
- ✅ Review and commit auto-fixes from Black/isort
- ✅ Review Ruff warnings and fix where appropriate
- ✅ Test suite passes after changes
- ✅ Coverage remains ≥ 68%
- ✅ Single commit with all formatting fixes

### Explicitly Excluded
- ❌ Refactoring code logic
- ❌ Adding new features
- ❌ Changing behavior (only formatting)
- ❌ Fixing all Ruff warnings (only critical ones)
- ❌ Adding type hints (deferred to Sprint 3)

---

## Requirements

### Functional Requirements
1. All files pass Black formatting
2. All imports sorted by isort
3. No trailing whitespace
4. All files end with newline
5. Critical Ruff warnings resolved
6. All 90 tests still pass
7. Coverage ≥ 68%

### Non-functional Requirements
- **Safety**: No behavior changes (formatting only)
- **Testability**: Full test suite validates no regressions
- **Reviewability**: Single commit with clear description

---

## Design

### Execution Strategy

```
Phase 1: Auto-fixes
├── Run: pre-commit run --all-files
├── Review: Git diff for Black changes
├── Review: Git diff for isort changes
└── Commit: Auto-formatting changes

Phase 2: Manual fixes (if needed)
├── Review: Ruff warnings
├── Fix: Critical issues only
├── Test: Run full test suite
└── Commit: Manual fixes (separate commit)
```

### Expected Changes

**Black**: Likely changes
- Line length adjustments (to 100 chars)
- Quote normalization (single → double)
- Whitespace adjustments
- Trailing comma additions

**isort**: Likely changes
- Import grouping (stdlib, third-party, local)
- Import sorting within groups
- Multi-line import formatting

**Ruff**: Likely warnings
- Unused imports (F401)
- Unused variables (F841)
- Line too long (E501) - should be fixed by Black
- Shadowed builtins (A001)

---

## Implementation Plan

### Step 1: Run pre-commit on all files
**Command**:
```powershell
pre-commit run --all-files
```

**Expected Output**: List of modified files and any failures

### Step 2: Review auto-fixes
**Command**:
```powershell
git diff
```

**Review**:
- Ensure only formatting changed
- No logic modifications
- No accidental deletions
- All changes are safe

### Step 3: Stage and test auto-fixes
**Commands**:
```powershell
git add .
python -m pytest -q
python -m coverage run -m pytest
python -m coverage report
```

**Verification**:
- All 90 tests pass
- Coverage ≥ 68%
- No new errors

### Step 4: Commit auto-fixes
**Command**:
```powershell
git commit -m "[Sortie 2]: Apply Black and isort formatting to codebase

- Ran pre-commit run --all-files
- Black formatted all Python files (line length 100)
- isort sorted all imports (black profile)
- Fixed trailing whitespace and EOF newlines
- All tests pass (90/90)
- Coverage maintained at 68%

Implements: SPEC-Sortie-2-fix-existing-code.md
Related: PRD-pre-commit-hooks.md
Tests: Full test suite validates no regressions"
```

### Step 5: Review Ruff warnings
**Command**:
```powershell
pre-commit run ruff --all-files
```

**Action**: Document warnings for future sprints (not all need immediate fix)

### Step 6: Fix critical Ruff issues (if any)
**Criteria for "critical"**:
- Actual bugs (undefined names, etc.)
- Security issues
- Unused imports in production code (not tests)

**Non-critical** (defer):
- Style preferences
- Complexity warnings
- All warnings in test files (if not breaking)

---

## Testing Strategy

### Unit Tests
- Run existing test suite (no new tests needed)

### Integration Tests
- Full test suite validates no behavior changes

### Manual Testing Checklist
- [ ] Application starts without errors
- [ ] TUI displays correctly
- [ ] Theme loading works
- [ ] Bot connects to server (if test server available)
- [ ] All commands work as expected

### Performance Benchmarks
- No performance impact expected (formatting only)

### Regression Prevention
```powershell
# Before committing, verify:
1. All 90 tests pass
2. Coverage ≥ 68%
3. Application runs
4. No new exceptions in logs
```

---

## Acceptance Criteria

- [x] `pre-commit run --all-files` executed
- [x] All auto-fixes reviewed in git diff
- [x] All Python files formatted with Black
- [x] All imports sorted with isort
- [x] No trailing whitespace in any file
- [x] All files end with single newline
- [x] All 90 tests pass
- [x] Coverage ≥ 68% (no decrease)
- [x] Application starts and runs correctly
- [x] Changes committed with sortie-format message
- [x] Critical Ruff issues resolved (if any found)

---

## Rollout

### Deployment Steps
1. Run pre-commit on all files
2. Review all changes
3. Test thoroughly
4. Commit auto-fixes
5. Push to branch
6. Verify CI passes

### Database Migrations
- None required

### Configuration Updates
- None required (Sortie 1 handled configuration)

---

## Documentation

### Code Comments Needed
- None (formatting-only changes)

### User-facing Docs to Update
- None (no user-visible changes)

### Architecture Docs to Revise
- None (no architecture changes)

---

## Risk Mitigation

### Risk 1: Black changes break something
**Probability**: LOW  
**Impact**: MEDIUM  
**Mitigation**: Full test suite catches regressions  
**Contingency**: Revert commit and investigate failing tests

### Risk 2: Import reordering causes issues
**Probability**: VERY LOW  
**Impact**: MEDIUM  
**Mitigation**: isort black-compatible profile prevents issues  
**Contingency**: Fix import order manually if needed

### Risk 3: Large diff makes review difficult
**Probability**: MEDIUM  
**Impact**: LOW  
**Mitigation**: Single commit, clear message, tests validate safety  
**Contingency**: Reviewers trust test coverage

---

**Status**: ✅ Ready to Implement (after Sortie 1)  
**Blocked By**: Sortie 1 (needs pre-commit configured)  
**Blocks**: None (independent)  
**Estimated Completion**: 2-3 hours  

**Next**: After this sortie, integrate with CI in Sortie 3
