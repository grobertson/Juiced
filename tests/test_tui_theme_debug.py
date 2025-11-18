import pytest
import asyncio
import json
from types import SimpleNamespace


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
        return lambda s='': s


# Use centralized `tests/conftest.py::test_environment` which sets
# `_TEST_LOG_DIR` and patches the TUI Terminal and rendering helpers.


def make_bot(config_file='config.json'):
    import juiced.tui_bot as tui_mod
    return tui_mod.TUIBot(tui_config={}, config_file=str(config_file), domain='example.com', channel='test', log_path=str(_TEST_LOG_DIR))


def test_theme_list_and_change_success(tmp_path):
    bot = make_bot(config_file=tmp_path / 'cfg.json')

    # list themes - should return available themes (repo includes themes/)
    themes = bot.list_themes()
    assert isinstance(themes, list)
    # pick default if present
    names = [t[0] for t in themes]
    if 'default' in names:
        ok = bot.change_theme('default')
        assert ok is True
        # config file should have been created and contain tui.theme
        cfg = json.loads((tmp_path / 'cfg.json').read_text())
        assert cfg.get('tui', {}).get('theme') == 'default'


def test_theme_change_fails_on_bad_theme(monkeypatch, tmp_path):
    # Force _load_theme to return an invalid dict (missing 'colors')
    bot = make_bot(config_file=tmp_path / 'cfg2.json')
    monkeypatch.setattr(type(bot), '_load_theme', lambda self, name: {'name': 'bad'})
    ok = bot.change_theme('bad')
    assert ok is False


@pytest.mark.asyncio
async def test_debug_command_no_playlist_and_with_playlist():
    bot = make_bot()

    # No playlist
    bot.channel = None
    await bot.handle_slash_command('/debug')
    assert any('No playlist available' in m['message'] for m in bot.chat_history)

    # With playlist
    class Item:
        def __init__(self, uid, title):
            self.uid = uid
            self.title = title

    item1 = Item(1, 'First')
    item2 = Item(2, 'Second')

    class Playlist:
        def __init__(self, queue):
            self.queue = queue
            self._current = None

        def get(self, uid):
            for it in self.queue:
                if it.uid == uid:
                    return it
            raise ValueError('not found')

        @property
        def current(self):
            return self._current

    bot.channel = SimpleNamespace(playlist=Playlist([item1, item2]))
    bot.pending_media_uid = 2
    await bot.handle_slash_command('/debug')
    # Should show queue length and mention pending UID
    assert any('Queue length' in m['message'] or 'Pending UID' in m['message'] or 'Found pending UID' in m['message'] for m in bot.chat_history)
