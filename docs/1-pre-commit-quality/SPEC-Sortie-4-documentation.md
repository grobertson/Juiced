# Sortie 4: Documentation and Rollout

**Sprint**: 1 - Pre-commit & Code Quality  
**Sortie**: 4 of 4  
**Estimated Time**: 2 hours  
**Dependencies**: Sorties 1-3 (all previous work)  
**Status**: 📋 Ready to Start (after Sorties 1-3)

---

## Overview

Comprehensive documentation of the pre-commit system for developers and contributors. This ensures everyone understands how to use the tools and what to do when hooks fail.

**What this achieves**: Complete developer onboarding and troubleshooting resources.

**Why it's a logical unit**: Documentation should cover the complete system after all components are implemented.

---

## Scope and Non-Goals

### Included

- ✅ Update README.md with pre-commit section
- ✅ Create/update CONTRIBUTING.md with detailed workflow
- ✅ Add troubleshooting guide
- ✅ Document bypass procedures
- ✅ Update setup scripts documentation
- ✅ Add examples and screenshots (optional)
- ✅ Update CHANGELOG.md

### Explicitly Excluded

- ❌ Modifying code behavior
- ❌ Changing configurations (done in Sortie 1)
- ❌ Architecture documentation (different sprint)

---

## Requirements

### Functional Requirements

1. README.md mentions pre-commit in setup section
2. CONTRIBUTING.md has complete pre-commit guide
3. Troubleshooting section covers common issues
4. Bypass procedure documented
5. Examples show expected behavior
6. CHANGELOG.md updated

### Non-functional Requirements

- **Clarity**: Examples for common scenarios
- **Completeness**: Covers all use cases
- **Accessibility**: Beginner-friendly language
- **Maintainability**: Easy to update as tools change

---

## Design

### Documentation Structure

```
README.md
├── Quick Start (brief mention)
└── Link to CONTRIBUTING.md

CONTRIBUTING.md (create if doesn't exist)
├── Getting Started
│   ├── Installing Pre-commit
│   └── First Commit
├── Pre-commit Hooks
│   ├── What Runs
│   ├── Why We Use Them
│   └── How They Work
├── Working with Pre-commit
│   ├── Normal Workflow
│   ├── When Hooks Fail
│   └── Bypassing Hooks (emergencies)
├── Troubleshooting
│   ├── Hook Execution Fails
│   ├── Formatting Conflicts
│   └── CI vs Local Differences
└── FAQ

CHANGELOG.md
└── Add entry for pre-commit system
```

---

## Implementation Plan

### Step 1: Update README.md

**File**: `README.md`

**Add section** (after Installation):

```markdown
## Development Setup

### Prerequisites
- Python 3.11+
- Git

### Quick Start
```bash
# Clone repository
git clone https://github.com/grobertson/Juiced.git
cd Juiced

# Run setup script (installs dependencies and pre-commit hooks)
# On Windows:
setup.bat

# On Linux/macOS:
./setup.sh
```

The setup script will:
- Install Python dependencies
- Configure pre-commit hooks for code quality
- Set up the development environment

**Note**: Pre-commit hooks will automatically format your code on commit. See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Manual Pre-commit Setup
If you didn't run the setup script:
```bash
pip install -r requirements-dev.txt
pre-commit install
```

Now hooks will run automatically on `git commit`.
```

### Step 2: Create/Update CONTRIBUTING.md

**File**: `CONTRIBUTING.md` (create if doesn't exist)

**Full content** (see detailed template in implementation section below)

### Step 3: Add Troubleshooting Section

**File**: `CONTRIBUTING.md` (append)

**Content**: Common issues and solutions (see template below)

### Step 4: Update CHANGELOG.md

**File**: `CHANGELOG.md`

**Add under appropriate version**:

```markdown
### Added
- Pre-commit hooks for automated code quality enforcement
  - Black for code formatting (line length 100)
  - isort for import sorting
  - Ruff for linting
  - Trailing whitespace removal
  - End-of-file newline enforcement
- GitHub Actions workflow for CI quality checks
- Comprehensive contribution guidelines in CONTRIBUTING.md

### Changed
- All Python files reformatted with Black
- All imports sorted with isort
- Updated setup scripts to install pre-commit hooks automatically
```

### Step 5: Test Documentation

**Actions**:
1. Fresh clone of repository
2. Follow README.md instructions
3. Verify pre-commit installs correctly
4. Make a test commit with bad formatting
5. Verify hooks catch and fix issues
6. Verify documentation is accurate

---

## CONTRIBUTING.md Template

```markdown
# Contributing to Juiced

Thank you for your interest in contributing to Juiced! This guide will help you get started.

## Table of Contents
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Pre-commit Hooks](#pre-commit-hooks)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)

## Getting Started

### Prerequisites
- Python 3.11 or higher
- Git
- Familiarity with async Python (for core development)

### Setup
```bash
# Clone the repository
git clone https://github.com/grobertson/Juiced.git
cd Juiced

# Run setup script
# Windows:
setup.bat

# Linux/macOS:
./setup.sh
```

The setup script installs:
- Python dependencies (pytest, black, ruff, etc.)
- Pre-commit hooks
- Development tools

## Development Workflow

### Making Changes

1. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write code
   - Add tests (coverage target: 60%+)
   - Update documentation

3. **Commit your changes**
   ```bash
   git add .
   git commit -m "Description of changes"
   ```
   
   Pre-commit hooks will automatically:
   - Format code with Black
   - Sort imports with isort
   - Check for linting issues with Ruff
   - Remove trailing whitespace
   - Ensure files end with newlines

4. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

## Pre-commit Hooks

### What Runs on Commit

1. **Black** - Code formatter (line length: 100)
2. **isort** - Import sorter (Black-compatible)
3. **Ruff** - Fast Python linter
4. **trailing-whitespace** - Removes trailing spaces
5. **end-of-file-fixer** - Ensures newline at EOF

### Why We Use Them

- **Consistency**: All code follows same style
- **Efficiency**: Catches issues before CI
- **Focus**: Code reviews focus on logic, not style
- **Quality**: Enforces best practices automatically

### When Hooks Fail

If pre-commit fails:

1. **Auto-fixes applied** (Black, isort)
   ```bash
   # Hooks modified files, stage them and re-commit
   git add .
   git commit -m "Your message"
   ```

2. **Manual fixes needed** (Ruff warnings)
   ```bash
   # Read error messages
   # Fix issues in code
   # Stage and commit again
   git add .
   git commit -m "Your message"
   ```

### Bypassing Hooks (Emergencies Only)

```bash
# Skip hooks (use responsibly!)
git commit --no-verify -m "Emergency fix"
```

**Note**: CI will still enforce quality checks. Use `--no-verify` only for:
- Emergency hotfixes
- Work-in-progress commits
- Debugging hook issues

## Testing

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov --cov-report=term-missing

# Run specific test file
python -m pytest tests/test_bot.py -v
```

### Writing Tests

- Place tests in `tests/` directory
- Name test files `test_*.py`
- Use pytest fixtures from `conftest.py`
- Aim for 60%+ coverage on new code
- Test both success and error cases

See [TESTS.md](TESTS.md) for detailed testing guidelines.

## Troubleshooting

### Hook Installation Failed

**Problem**: `pre-commit install` fails

**Solution**:
```bash
# Ensure pre-commit is installed
pip install pre-commit

# Try installing hooks again
pre-commit install
```

### Hook Execution is Slow

**Problem**: Pre-commit takes > 5 seconds

**Solution**:
```bash
# Update hooks to latest versions
pre-commit autoupdate

# Clear hook cache
pre-commit clean
pre-commit install --install-hooks
```

### Black and My IDE Conflict

**Problem**: IDE formatter and Black disagree

**Solution**:
1. Configure IDE to use Black:
   - VS Code: Install "Black Formatter" extension
   - PyCharm: Settings → Tools → Black
2. Set line length to 100 in both IDE and Black

### CI Passes Locally but Fails on GitHub

**Problem**: Pre-commit passes locally, CI fails

**Solution**:
```bash
# Run exactly what CI runs
pre-commit run --all-files

# If issues found, fix and commit
git add .
git commit -m "Fix quality issues"
```

### Ruff Complains About Code That Works

**Problem**: Ruff flags working code

**Solution**:
1. Review warning - it may catch real issues
2. If false positive, add inline ignore:
   ```python
   # ruff: noqa: E501
   very_long_line_that_needs_to_be_long()
   ```
3. Or add to pyproject.toml:
   ```toml
   [tool.ruff.lint.per-file-ignores]
   "path/to/file.py" = ["E501"]
   ```

## FAQ

### Do I need to run pre-commit manually?

No. After `pre-commit install`, hooks run automatically on `git commit`.

### Can I format code without committing?

Yes:
```bash
# Format specific file
black juiced/bot.py

# Format all Python files
black .

# Sort imports
isort .
```

### What if I disagree with Black's formatting?

Black is intentionally opinionated to eliminate style debates. If you have concerns, open an issue to discuss.

### How do I update pre-commit hooks?

```bash
pre-commit autoupdate
```

This updates to the latest stable versions of all hooks.

### Can I use different tools locally?

Yes, but CI enforces Black/isort/Ruff. To avoid surprises, use the same tools locally.

## Code Style

- **Line Length**: 100 characters (Black/Ruff enforced)
- **Imports**: Sorted by isort (stdlib, third-party, local)
- **Quotes**: Double quotes preferred (Black enforced)
- **Docstrings**: Required for public APIs
- **Type Hints**: Encouraged (future: required)

## Commit Messages

Follow standard format:
```
Brief title (50 chars or less)

Detailed description of what changed and why.
Include context for reviewers.

- Bullet points for specific changes
- Reference issues if applicable
```

For sprint work, use sortie format (see AGENTS.md).

## Questions?

- Open an issue for bugs or feature requests
- Check existing issues before creating new ones
- Be respectful and constructive

Thank you for contributing! 🎉
```

---

## Testing Strategy

### Manual Testing

**Test 1: New Developer Setup**
1. Clone repo fresh
2. Follow README instructions
3. Verify pre-commit installs
4. Make commit with bad formatting
5. Verify hooks catch issues

**Test 2: Documentation Accuracy**
1. Follow each troubleshooting step
2. Verify solutions work
3. Check all links resolve
4. Verify code examples are correct

**Test 3: Contribution Workflow**
1. Create feature branch
2. Make changes
3. Commit (hooks should run)
4. Push to GitHub
5. Verify CI runs and passes

---

## Acceptance Criteria

- [x] README.md updated with pre-commit section
- [x] CONTRIBUTING.md created with comprehensive guide
- [x] Pre-commit hooks explained (what, why, how)
- [x] Workflow documented (normal and failure cases)
- [x] Bypass procedure documented
- [x] Troubleshooting section with 5+ common issues
- [x] FAQ with 5+ questions
- [x] CHANGELOG.md updated
- [x] Documentation tested with fresh clone
- [x] All links work
- [x] Code examples are accurate

---

## Rollout

### Deployment Steps

1. Create/update CONTRIBUTING.md
2. Update README.md
3. Update CHANGELOG.md
4. Test with fresh clone
5. Commit all documentation
6. Announce in PR

### Communication

**PR Description** should highlight:
- Pre-commit hooks now enforced
- Link to CONTRIBUTING.md for setup
- Encourage all contributors to read guide
- Offer help with setup issues

---

## Documentation

### Files Updated

- `README.md` - Quick start section
- `CONTRIBUTING.md` - Comprehensive guide (created)
- `CHANGELOG.md` - Release notes
- `docs/1-pre-commit-quality/` - Sprint documentation

---

**Status**: ✅ Ready to Implement (after Sorties 1-3)  
**Blocked By**: Sorties 1-3 (must complete system first)  
**Blocks**: None (final sortie)  
**Estimated Completion**: 2 hours  

**Sprint Complete**: After this sortie, Sprint 1 is 100% done! 🎉
