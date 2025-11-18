import json
from pathlib import Path
from types import SimpleNamespace

import pytest


@pytest.fixture(autouse=True)
def patch_terminal_and_render(monkeypatch):
    # Provide a minimal fake Terminal and disable full render
    class FakeTerm:
        def __init__(self, width=80, height=24):
            self.width = width
            self.height = height
            self.clear = ""

        class _Loc:
            def __init__(self, *a, **k):
                pass

            def __enter__(self):
                return None

            def __exit__(self, exc_type, exc, tb):
                return False

        def location(self, x, y=None):
            return FakeTerm._Loc()

        def __getattr__(self, name):
            return lambda s="": s

    import juiced.tui_bot as tui_mod

    monkeypatch.setattr(tui_mod, "Terminal", FakeTerm)
    monkeypatch.setattr(tui_mod.TUIBot, "render_screen", lambda self: None)
    yield


def make_bot():
    import juiced.tui_bot as tui_mod

    return tui_mod.TUIBot(
        tui_config={}, config_file="config.json", domain="example.com", channel="test"
    )


def test_list_and_load_themes(tmp_path):
    bot = make_bot()
    mod_dir = Path(__import__("juiced.tui_bot").__file__).parent
    themes_dir = mod_dir / "themes"
    themes_dir.mkdir(parents=True, exist_ok=True)

    # Create two themes
    t1 = themes_dir / "blue.json"
    t1.write_text(
        json.dumps(
            {
                "name": "Blue",
                "colors": {"status_bar": {"background": "blue", "text": "white"}},
            }
        )
    )
    t2 = themes_dir / "simple.json"
    t2.write_text(
        json.dumps(
            {
                "name": "Simple",
                "colors": {"status_bar": {"background": "cyan", "text": "black"}},
            }
        )
    )

    themes = bot.list_themes()
    names = [n for n, _ in themes]
    assert "blue" in names and "simple" in names


def test_change_theme_creates_config_when_missing(tmp_path):
    bot = make_bot()
    mod_dir = Path(__import__("juiced.tui_bot").__file__).parent
    themes_dir = mod_dir / "themes"
    themes_dir.mkdir(parents=True, exist_ok=True)

    theme_file = themes_dir / "mytheme.json"
    theme_file.write_text(
        json.dumps(
            {
                "name": "MyTheme",
                "colors": {"status_bar": {"background": "green", "text": "black"}},
            }
        )
    )

    cfg = tmp_path / "cfg.json"
    # ensure config does not exist
    if cfg.exists():
        cfg.unlink()

    bot.config_file = str(cfg)
    ok = bot.change_theme("mytheme")
    assert ok is True
    # config file should now exist and contain tui.theme
    loaded = json.loads(cfg.read_text())
    assert loaded.get("tui", {}).get("theme") == "mytheme"


def test_change_theme_rejects_missing_colors(tmp_path):
    bot = make_bot()
    mod_dir = Path(__import__("juiced.tui_bot").__file__).parent
    themes_dir = mod_dir / "themes"
    themes_dir.mkdir(parents=True, exist_ok=True)

    bad = themes_dir / "bad.json"
    bad.write_text(json.dumps({"name": "BadTheme"}))

    cfg = tmp_path / "cfg2.json"
    cfg.write_text(json.dumps({}))
    bot.config_file = str(cfg)

    ok = bot.change_theme("bad")
    # change_theme should return False because theme lacks 'colors'
    assert ok is False
    loaded = json.loads(cfg.read_text())
    # config should remain unchanged (no tui.theme)
    assert "tui" not in loaded or loaded.get("tui", {}).get("theme") != "bad"


def test_load_theme_with_invalid_json_returns_fallback(tmp_path):
    bot = make_bot()
    # write invalid theme file at absolute path
    mod_dir = Path(__import__("juiced.tui_bot").__file__).parent
    themes_dir = mod_dir / "themes"
    themes_dir.mkdir(parents=True, exist_ok=True)

    badfile = themes_dir / "broken.json"
    badfile.write_text("{ this is not: valid json")

    # load using name
    res = bot._load_theme("broken")
    assert isinstance(res, dict)
    assert "colors" in res
