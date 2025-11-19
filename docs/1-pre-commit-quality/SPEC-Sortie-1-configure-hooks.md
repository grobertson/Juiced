# Sortie 1: Configure Pre-commit Hooks

**Sprint**: 1 - Pre-commit & Code Quality  
**Sortie**: 1 of 4  
**Estimated Time**: 2-3 hours  
**Dependencies**: None  
**Status**: 📋 Ready to Start

---

## Overview

Set up the pre-commit framework with hooks for Black, isort, Ruff, and basic file hygiene. This sortie focuses on getting the infrastructure in place and configured correctly.

**What this achieves**: Foundation for automated code quality enforcement at commit time.

**Why it's a logical unit**: Configuration setup is independent and must be complete before running on codebase.

---

## Scope and Non-Goals

### Included
- ✅ Install pre-commit package
- ✅ Create `.pre-commit-config.yaml`
- ✅ Configure Black with project settings
- ✅ Configure isort to work with Black
- ✅ Configure Ruff with existing rules
- ✅ Add trailing-whitespace and end-of-file-fixer hooks
- ✅ Install hooks locally: `pre-commit install`
- ✅ Test hooks work correctly

### Explicitly Excluded
- ❌ Running hooks on existing codebase (Sortie 2)
- ❌ CI integration (Sortie 3)
- ❌ Documentation (Sortie 4)
- ❌ Modifying any Python source files

---

## Requirements

### Functional Requirements
1. Pre-commit framework installed and configured
2. Hooks execute on `git commit`
3. Failed hooks prevent commit with clear messages
4. Successful hooks allow commit to proceed
5. Hook execution completes in < 5 seconds for typical commit

### Non-functional Requirements
- **Performance**: Hook execution < 5s for 1-3 files
- **Reliability**: Hooks must not produce false positives
- **Usability**: Error messages must be actionable
- **Compatibility**: Works on Windows, Linux, macOS

---

## Design

### Hook Configuration Structure

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: ["--profile", "black"]

  - repo: https://github.com/psf/black
    rev: 23.11.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
```

### Tool Configuration

**Black Settings** (pyproject.toml):
```toml
[tool.black]
line-length = 100
target-version = ['py311']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.pytest_cache
  | __pycache__
  | build
  | dist
)/
'''
```

**isort Settings** (pyproject.toml):
```toml
[tool.isort]
profile = "black"
line_length = 100
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true
```

**Ruff Settings** (pyproject.toml):
```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # pyflakes
    "I",    # isort
    "B",    # flake8-bugbear
    "C4",   # flake8-comprehensions
    "UP",   # pyupgrade
]
ignore = [
    "E501",  # line too long (handled by black)
]

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401"]  # Allow unused imports
"tests/*" = ["B011"]      # Allow assert False
```

---

## Implementation Plan

### Step 1: Add isort to requirements
**File**: `requirements-dev.txt`
**Action**: Add line
```
isort>=5.12.0
```

### Step 2: Create pre-commit configuration
**File**: `.pre-commit-config.yaml` (new)
**Action**: Create with full configuration (see Design section above)

### Step 3: Add tool configurations to pyproject.toml
**File**: `pyproject.toml`
**Action**: Add `[tool.black]`, `[tool.isort]`, `[tool.ruff]` sections

### Step 4: Update setup scripts
**File**: `setup.bat`
**Action**: Add after pip install:
```batch
echo Installing pre-commit hooks...
pre-commit install
```

**File**: `setup.sh`
**Action**: Add after pip install:
```bash
echo "Installing pre-commit hooks..."
pre-commit install
```

### Step 5: Install and test locally
**Commands**:
```powershell
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Test on a sample file
echo "# test" > test.py
git add test.py
git commit -m "Test pre-commit" --no-verify  # Test without running
git reset HEAD~1
rm test.py
```

---

## Testing Strategy

### Unit Tests
- None required (infrastructure change)

### Integration Tests
1. **Test Hook Execution**
   ```powershell
   # Create test file with bad formatting
   echo "import os,sys" > test_format.py
   git add test_format.py
   git commit -m "Test"
   # Expected: isort and black auto-fix, then commit fails asking to re-add
   ```

2. **Test Hook Bypass**
   ```powershell
   git commit -m "Emergency fix" --no-verify
   # Expected: Commit succeeds without running hooks
   ```

3. **Test Each Hook Individually**
   ```powershell
   pre-commit run trailing-whitespace --all-files
   pre-commit run end-of-file-fixer --all-files
   pre-commit run isort --all-files
   pre-commit run black --all-files
   pre-commit run ruff --all-files
   ```

### Manual Testing Checklist
- [ ] Pre-commit installs without errors
- [ ] Hooks execute on `git commit`
- [ ] Black formats code automatically
- [ ] isort sorts imports automatically
- [ ] Ruff catches linting issues
- [ ] Failed hooks show clear error messages
- [ ] `--no-verify` bypasses hooks
- [ ] Hook execution completes in < 5 seconds

### Performance Benchmarks
- **Baseline**: Time a commit without hooks
- **Target**: Hooks add < 5 seconds overhead
- **Measurement**: `Measure-Command { git commit -m "test" }`

---

## Acceptance Criteria

- [x] isort added to `requirements-dev.txt`
- [x] `.pre-commit-config.yaml` created with all 5 hooks
- [x] Tool configurations added to `pyproject.toml`
- [x] `setup.bat` updated to install pre-commit
- [x] `setup.sh` updated to install pre-commit
- [x] Pre-commit installed locally
- [x] Hooks execute on test commit
- [x] All hooks pass on sample files
- [x] Hook execution time < 5 seconds
- [x] No changes to existing Python source files

---

## Rollout

### Deployment Steps
1. Add isort to requirements-dev.txt
2. Create .pre-commit-config.yaml
3. Update pyproject.toml with tool configs
4. Update setup.bat and setup.sh
5. Commit configuration files
6. Test installation on clean clone

### Database Migrations
- None required

### Configuration Updates
- Pre-commit configuration in `.pre-commit-config.yaml`
- Tool settings in `pyproject.toml`

---

## Documentation

### Code Comments Needed
- None (configuration files are self-documenting)

### User-facing Docs to Update
- Defer to Sortie 4 (Documentation)

### Architecture Docs to Revise
- Defer to Sortie 4 (Documentation)

---

**Status**: ✅ Ready to Implement  
**Blocked By**: None  
**Blocks**: Sortie 2 (depends on configuration)  
**Estimated Completion**: 2-3 hours  

**Next**: After this sortie, run pre-commit on existing codebase in Sortie 2
