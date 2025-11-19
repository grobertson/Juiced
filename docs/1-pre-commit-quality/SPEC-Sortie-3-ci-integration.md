# Sortie 3: CI Integration

**Sprint**: 1 - Pre-commit & Code Quality  
**Sortie**: 3 of 4  
**Estimated Time**: 1-2 hours  
**Dependencies**: Sortie 1 (pre-commit configured)  
**Status**: 📋 Ready to Start (after Sortie 1)

---

## Overview

Integrate pre-commit checks into the CI pipeline to ensure all merged code meets quality standards. This creates consistency between local development and CI validation.

**What this achieves**: Automated enforcement of code quality in CI, preventing non-compliant code from being merged.

**Why it's a logical unit**: CI changes are independent from local setup and documentation.

---

## Scope and Non-Goals

### Included

- ✅ Create/update GitHub Actions workflow
- ✅ Add pre-commit step to CI
- ✅ Configure CI to fail on quality violations
- ✅ Test CI with intentionally broken code
- ✅ Ensure CI mirrors local pre-commit hooks

### Explicitly Excluded

- ❌ Changing existing CI steps (tests, coverage)
- ❌ Adding new quality tools beyond pre-commit
- ❌ Documentation (handled in Sortie 4)
- ❌ Branch protection rules (manual GitHub settings)

---

## Requirements

### Functional Requirements

1. CI runs pre-commit on all files in PR
2. CI fails if any pre-commit hook fails
3. CI success guarantees code meets quality standards
4. CI runs same hooks as local development
5. CI provides clear error messages on failure

### Non-functional Requirements

- **Performance**: CI completes in < 2 minutes for pre-commit step
- **Reliability**: No flaky failures
- **Maintainability**: Single source of truth (.pre-commit-config.yaml)

---

## Design

### GitHub Actions Workflow Structure

```yaml
# .github/workflows/quality.yml
name: Code Quality

on:
  pull_request:
    branches: [main]
  push:
    branches: [main, wip/*]

jobs:
  pre-commit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pre-commit
      
      - name: Cache pre-commit hooks
        uses: actions/cache@v3
        with:
          path: ~/.cache/pre-commit
          key: pre-commit-${{ hashFiles('.pre-commit-config.yaml') }}
      
      - name: Run pre-commit
        run: pre-commit run --all-files --show-diff-on-failure
```

### Integration with Existing CI

If existing workflow exists, add pre-commit as a job:

```yaml
jobs:
  quality:
    name: Code Quality
    runs-on: ubuntu-latest
    steps:
      # ... pre-commit steps ...
  
  tests:
    name: Run Tests
    needs: quality  # Run tests only if quality passes
    runs-on: ubuntu-latest
    steps:
      # ... existing test steps ...
```

---

## Implementation Plan

### Step 1: Check for existing GitHub Actions

**Command**:
```powershell
ls .github/workflows/
```

**Action**:
- If workflows exist: Review and plan integration
- If no workflows: Create new quality.yml

### Step 2: Create/update workflow file

**File**: `.github/workflows/quality.yml` (new or updated)

**Content**: See Design section above

### Step 3: Test CI locally (optional)

**Tool**: [act](https://github.com/nektos/act) - runs GitHub Actions locally

**Command**:
```powershell
# If act is installed
act pull_request
```

### Step 4: Commit and push workflow

**Command**:
```powershell
git add .github/workflows/quality.yml
git commit -m "[Sortie 3]: Add pre-commit CI validation

- Created GitHub Actions workflow for code quality
- Runs pre-commit on all files in PR
- Fails CI if quality checks fail
- Cached pre-commit hooks for performance
- Provides diff on failure for easy debugging

Implements: SPEC-Sortie-3-ci-integration.md
Related: PRD-pre-commit-hooks.md"

git push
```

### Step 5: Verify CI runs

**Actions**:
1. Open GitHub PR page
2. Check Actions tab
3. Verify "Code Quality" workflow runs
4. Confirm it passes with current code

### Step 6: Test CI failure scenario

**Create test branch**:
```powershell
git checkout -b test/ci-quality
echo "import os,sys" > test_bad_format.py
git add test_bad_format.py
git commit -m "Test: Intentionally bad formatting" --no-verify
git push
```

**Expected**: CI fails with clear error showing formatting issue

**Cleanup**:
```powershell
git checkout wip/ruff-fixes
git branch -D test/ci-quality
git push origin --delete test/ci-quality
```

---

## Testing Strategy

### Unit Tests

- None required (CI configuration)

### Integration Tests

1. **Test CI Success**
   - Push clean code
   - Verify CI passes
   - Check execution time

2. **Test CI Failure - Formatting**
   - Push code with bad formatting
   - Verify CI fails
   - Check error message clarity

3. **Test CI Failure - Linting**
   - Push code with linting errors
   - Verify CI fails
   - Check error message shows specific issue

4. **Test Cache Performance**
   - Run CI twice on same commit
   - Verify second run is faster (cache hit)

### Manual Testing Checklist

- [ ] Workflow file is valid YAML
- [ ] CI runs on pull requests
- [ ] CI runs on pushes to main/wip/*
- [ ] Pre-commit hooks execute in CI
- [ ] Failed hooks fail the CI build
- [ ] CI shows diff for failed checks
- [ ] Cache improves performance
- [ ] Error messages are actionable

---

## Acceptance Criteria

- [x] GitHub Actions workflow created/updated
- [x] Pre-commit runs on all files in CI
- [x] CI fails if pre-commit checks fail
- [x] CI shows clear error messages and diffs
- [x] Pre-commit hooks cached for performance
- [x] CI tested with success scenario
- [x] CI tested with failure scenario
- [x] Workflow committed to repository
- [x] CI execution time < 2 minutes

---

## Rollout

### Deployment Steps

1. Create/update `.github/workflows/quality.yml`
2. Commit workflow file
3. Push to remote
4. Verify workflow appears in Actions tab
5. Test with clean code (should pass)
6. Test with bad code (should fail)
7. Document CI behavior in Sortie 4

### Configuration Updates

- GitHub Actions workflow configuration
- Optional: Branch protection rules (manual)

---

## Documentation

### Code Comments Needed

- None (workflow file is self-documenting with name fields)

### User-facing Docs to Update

- Defer to Sortie 4 (comprehensive documentation)

### Architecture Docs to Revise

- Defer to Sortie 4

---

## Risk Mitigation

### Risk 1: CI cache invalidation issues

**Probability**: LOW  
**Impact**: LOW (slower builds)  
**Mitigation**: Cache key uses hash of .pre-commit-config.yaml  
**Contingency**: Remove cache if issues occur

### Risk 2: CI timeout on large PRs

**Probability**: LOW  
**Impact**: MEDIUM  
**Mitigation**: Pre-commit is fast, typically < 1 minute  
**Contingency**: Increase timeout or split checks

### Risk 3: Different behavior between local and CI

**Probability**: VERY LOW  
**Impact**: HIGH  
**Mitigation**: Both use same .pre-commit-config.yaml  
**Contingency**: Pin pre-commit version in CI

---

**Status**: ✅ Ready to Implement (after Sortie 1)  
**Blocked By**: Sortie 1 (needs .pre-commit-config.yaml)  
**Blocks**: None  
**Estimated Completion**: 1-2 hours  

**Next**: After this sortie, document everything in Sortie 4
