import pytest


class FakeTerm:
    def __init__(self, width=80, height=24):
        self.width = width
        self.height = height

    class _Loc:
        def __enter__(self):
            return None

        def __exit__(self, exc_type, exc, tb):
            return False

    def location(self, *a, **k):
        return FakeTerm._Loc()

    def __getattr__(self, name):
        return lambda s="": s


@pytest.fixture(autouse=True)
def test_environment(monkeypatch, tmp_path, request):
    """Centralized autouse fixture for TUI tests.

    - Sets a module-level `_TEST_LOG_DIR` to pytest's `tmp_path` so tests that
      reference that variable don't need their own autouse fixture.
    - Monkeypatches the TUI Terminal and disables full-screen rendering to
      avoid side-effects during tests.
    """
    # If the test module defines or expects `_TEST_LOG_DIR`, set it here.
    mod = getattr(request, "module", None)
    if mod is not None:
        try:
            setattr(mod, "_TEST_LOG_DIR", tmp_path)
        except Exception:
            # best-effort; continue if we can't set it
            pass

    # Try to patch juiced.tui_bot if it's importable in the test environment.
    try:
        import juiced.tui_bot as tui_mod

        monkeypatch.setattr(tui_mod, "Terminal", FakeTerm)
        # disable heavy rendering helpers that operate on the terminal
        if hasattr(tui_mod, "TUIBot"):
            monkeypatch.setattr(tui_mod.TUIBot, "render_screen", lambda self: None)
            monkeypatch.setattr(tui_mod.TUIBot, "render_input", lambda self: None)
        # Redirect module __file__ to a temporary location under tmp_path so
        # tests that compute Path(__file__).parent / "themes" will operate
        # in a test-local directory instead of writing into the installed
        # package directory.
        try:
            module_dir = tmp_path / "tui_module"
            module_dir.mkdir(parents=True, exist_ok=True)
            # Provide a module-level THEMES_BASE that points to the temporary
            # module_dir so theme lookups use tmp_path during tests.
            monkeypatch.setattr(tui_mod, "__file__", str(module_dir / "tui_bot.py"))
            try:
                monkeypatch.setattr(tui_mod, "THEMES_BASE", module_dir)
            except Exception:
                # best-effort; continue if we can't set it
                pass
        except Exception:
            # best-effort; if this fails, tests may still patch manually
            pass
    except Exception:
        # If the package isn't importable yet, tests will import it later and
        # may patch as needed; don't fail the fixture.
        pass

    yield
