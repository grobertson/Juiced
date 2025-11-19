## Agents / Contribution Policy

### Purpose

This document sets a baseline for code contributions (agents) to Juiced. It focuses on tests, quality gates, versioning, and error-message standards so maintainers and contributors have clear, enforceable expectations.

### Scope

- Applies to any new code, refactor, or behavioural change (including new modules, CLI changes, and automation).
- Small documentation-only edits are exempt from adding tests, but large doc-driven behaviour changes must include tests.

## Core requirements (must be satisfied for PRs)

### Testing

See `TESTS.md` for the canonical testing requirements and contributor guidance (pytest, async testing, test locations, templates, and examples).

### Coverage

- Project-wide coverage must be >= 60%.
- PRs touching code must include tests that bring the changed code coverage to an acceptable level; CI will enforce `coverage report --fail-under=60`.

### Clear, meaningful errors

- All exceptions must have explanatory messages and use domain-specific exception classes where appropriate (see `juiced/lib/error.py`).
- Avoid bare `except:`; catch explicit exception types and re-raise with contextual information when surfacing errors across boundaries.

### Modern coding practices

- Use type hints on public functions and methods. Prefer gradual typing; keep annotations readable.
- Formatting and linting: adopt Black/ruff/isort (or equivalent). Add `pre-commit` hooks to enforce locally.
- Favor small, single-responsibility functions and avoid large monolithic functions unless justified and documented.

### Semantic Versioning

- Follow semver for releases (MAJOR.MINOR.PATCH). Bump `setup.py`/release metadata and tag releases (e.g., `v1.2.3`).
- Feature work targets `main` or feature branches; releases are cut from `main` and tagged.

### PR checklist (required)

- [ ] Testing: follow `TESTS.md` for contributor guidance; add/modify tests as required by the change.
- [ ] Coverage check: `coverage run -m pytest && coverage report --fail-under=60` passes locally.
- [ ] Meaningful exception messages and documented error classes.
- [ ] Type hints added for public surfaces and documented where unclear.
- [ ] CI passes (unit tests + coverage + linting).

### Recommended local commands (PowerShell)

Run tests and coverage locally before pushing:
```powershell
python -m pip install -r requirements.txt
python -m pip install pytest coverage
coverage run -m pytest
coverage report --fail-under=60
```

### Pre-commit (recommended)

We recommend using `pre-commit` to enforce formatting and linting hooks locally before pushing. Example PowerShell commands to install and run hooks locally:

```powershell
python -m pip install --user pre-commit
python -m pre_commit install
# Run all hooks once across the repository
python -m pre_commit run --all-files
```

Suggested minimal `.pre-commit-config.yaml` (examples of commonly used hooks):

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: stable
    hooks:
      - id: black

  - repo: https://github.com/PyCQA/isort
    rev: stable
    hooks:
      - id: isort

  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: stable
    hooks:
      - id: ruff

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.0.1
    hooks:
      - id: end-of-file-fixer
      - id: trailing-whitespace
```

Add this file to the repository and run `pre-commit install` to enable the hooks locally. We also recommend running `pre-commit run --all-files` in CI as an early check step.

### Suggested CI enforcement (GitHub Actions snippet)

Use a workflow that runs pytest and enforces coverage. Minimal example (put in `.github/workflows/ci.yml`):

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.11
      - name: Install
        run: python -m pip install -r requirements.txt
      - name: Run tests with coverage
        run: |
          python -m pip install pytest coverage
          coverage run -m pytest
          coverage report --fail-under=60
```

- Automate tagging and changelog generation where possible; CI should block release if tests/coverage fail.

### Notes for maintainers

- If a proposed change cannot reasonably meet the 90% coverage requirement (e.g., infra-only or native bindings), document the trade-off in the PR and seek explicit maintainer approval.
- Consider adding `pre-commit` and a GitHub Action to run `pre-commit` on every PR to keep the repository consistent.
