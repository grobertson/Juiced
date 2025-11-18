## Testing guide for contributors

This document describes when, where, and how to contribute tests for Juiced. It is the canonical source for testing requirements and workflows; the `AGENTS.md` contribution policy delegates all testing details here.

When to add tests
------------------
- New code: Any new module, class, or function that implements behaviour must include tests.
- Bug fixes: Add a regression test that reproduces the bug before fixing it, then verify it fails and passes after the fix.
- Refactors: If behaviour changes are possible, add or update tests to cover expected behaviour and edge cases.
- Documentation-only edits do not require tests.

Where tests live
----------------
- All tests live under the `tests/` directory at the repository root.
- File naming: `test_*.py` modules. Test functions and classes should be prefixed with `test_`.
- Tests should avoid long-running network calls or heavy external dependencies. Use mocks or fixtures instead.

Test tooling and dependencies
----------------------------
- Required test runner: `pytest`.
- Async tests: use `pytest-asyncio` (mark async tests with `@pytest.mark.asyncio`).
- Use `pytest-*` plugins as needed (for example `pytest-mock` for fixtures, `pytest-xdist` for parallel runs in CI).
- Recommended dev dependencies (pin in `requirements-dev.txt` or `pyproject.toml`):
  - pytest
  - pytest-asyncio
  - pytest-mock
  - coverage

Writing tests — guidance
-----------------------
- Keep tests small and focused: one behaviour / assertion per test whenever possible.
- Use arrange / act / assert sections and clear, descriptive names.
- Prefer fixtures for setup/teardown to avoid duplication.
- For code interacting with sockets or networks, isolate logic behind interfaces and unit-test small units; use `monkeypatch` or `pytest-mock` to replace network calls.
- For async code, prefer `pytest.mark.asyncio` and avoid custom event loop hacks.
- Use `tmp_path` or `tmp_path_factory` for filesystem tests.
- Avoid global state mutation in tests; reset or use fixtures to isolate tests.
Avoid global state mutation in tests; reset or use fixtures to isolate tests.

### Theme fixtures (UI / TUI tests)

- Theme-related tests should not write files into the packaged `juiced/` directory.
- A reusable fixture `themes_dir` is provided in `tests/conftest.py`. Use it in tests that need to create or read theme JSON files. The fixture:
    - creates a temporary module-like directory under pytest's `tmp_path` (e.g. `<tmp_path>/tui_module/themes`);
    - sets the `JUICED_THEMES_BASE` environment variable so lookups like `Path(__file__).parent / 'themes'` resolve inside the temporary dir;
    - returns a `pathlib.Path` to the temporary `themes` directory so tests can write fixture JSON files there.

Example usage in a test:

```python
def test_example(themes_dir):
        # themes_dir is a pathlib.Path to a tmp 'themes' directory
        (themes_dir / "blue.json").write_text(json.dumps({...}))
        # run code that loads or lists themes; it will read from themes_dir
        ...
```

Notes:
- Production code is unchanged — tests may set the `JUICED_THEMES_BASE` environment variable to point theme lookups at a temporary directory. Tests that don't use the fixture will continue to read from the package `themes/` directory.
- This keeps tests self-contained and prevents tests from modifying or leaving artifacts in the source tree.

Example patterns
----------------
1) Simple unit test

```python
def test_addition():
    # arrange
    a, b = 1, 2
    # act
    res = a + b
    # assert
    assert res == 3
```

2) Async test with `pytest-asyncio`

```python
import pytest

@pytest.mark.asyncio
async def test_async_example():
    await some_async_function()
    assert True
```

3) Testing exceptions and error messages

```python
from juiced.lib.error import Kicked

def test_kicked_message():
    e = Kicked('kicked-by-op')
    assert 'kicked' in str(e).lower()
```

Running tests locally
---------------------
Install dev dependencies and run tests with coverage:

```powershell
python -m pip install -r requirements.txt
python -m pip install pytest pytest-asyncio coverage
coverage run -m pytest
coverage report --fail-under=60
```

CI and required checks
----------------------
- The project CI must run the full test suite and enforce `coverage report --fail-under=60`.
- Tests should run deterministically. If a test is flaky, either fix it or mark it with `@pytest.mark.flaky` and explain the flakiness in the PR.

Contributing tests in a PR
--------------------------
1. Add or update tests under `tests/` covering new behaviour.
2. Ensure tests are fast and do not rely on networked services unless explicitly marked as integration tests.
3. Run the full suite locally and include the results in the PR description if helpful.
4. Update coverage-related expectations in the PR body (if you intentionally reduce or require different coverage for a special case, document and request maintainer approval).

Test review checklist (include in your PR description)
- [ ] New/changed behaviour covered by tests.
- [ ] Tests are deterministic and isolated.
- [ ] Used fixtures/mocks instead of real network calls where possible.
- [ ] Async tests use `pytest-asyncio` and are marked appropriately.

Help and troubleshooting
------------------------
- If tests fail on CI but pass locally, ensure identical Python versions and dependency pins; run tests with `-k` to narrow failing tests and add diagnostic logs.
- For intermittent CI failures, capture full output and open an issue with the failing job link and test name.

Contact
-------
For questions about testing policy or to request an exception (for example, native bindings or infra-only code that cannot be easily unit-tested), open an issue and tag the maintainers.
