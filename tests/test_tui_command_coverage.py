import pytest
import asyncio
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


# Centralized test fixture (tests/conftest.py) sets _TEST_LOG_DIR and patches TUI terminal.


def make_bot():
    import juiced.tui_bot as tui_mod
    return tui_mod.TUIBot(tui_config={}, config_file='cfg.json', domain='example.com', channel='test', log_path=str(_TEST_LOG_DIR))


@pytest.mark.asyncio
async def test_current_no_media_and_with_current():
    bot = make_bot()

    # No channel
    bot.channel = None
    await bot.handle_slash_command('/current')
    assert any('No media currently playing' in m['message'] or 'No media' in m['message'] for m in bot.chat_history)

    # With current in playlist
    item = SimpleNamespace(uid=1, title='Song', duration=120, seconds=10, username='dj')
    pl = SimpleNamespace(queue=[item], current=item)
    bot.channel = SimpleNamespace(playlist=pl)
    bot.chat_history.clear()
    await bot.handle_slash_command('/current')
    assert any('Current Media Info' in m['message'] or 'Title:' in m['message'] for m in bot.chat_history)


@pytest.mark.asyncio
async def test_move_to_beginning_not_supported_and_move_usage():
    bot = make_bot()
    i1 = SimpleNamespace(uid=1, title='One', duration=10)
    i2 = SimpleNamespace(uid=2, title='Two', duration=20)
    pl = SimpleNamespace(queue=[i1, i2])
    bot.channel = SimpleNamespace(playlist=pl)

    # move to beginning (to_pos == 1) should be not supported
    await bot.handle_slash_command('/move 1 1')
    assert any('Moving to beginning not yet supported' in m['message'] for m in bot.chat_history)

    # insufficient args
    bot.chat_history.clear()
    await bot.handle_slash_command('/move 1')
    assert any('Usage: /move' in m['message'] for m in bot.chat_history)


@pytest.mark.asyncio
async def test_jump_errors():
    bot = make_bot()
    # no args
    await bot.handle_slash_command('/jump')
    assert any('Usage: /jump' in m['message'] for m in bot.chat_history)

    # invalid int
    bot.chat_history.clear()
    await bot.handle_slash_command('/jump abc')
    assert any('Invalid position number' in m['message'] for m in bot.chat_history)

    # out of range
    i1 = SimpleNamespace(uid=1, title='One', duration=10)
    pl = SimpleNamespace(queue=[i1])
    bot.channel = SimpleNamespace(playlist=pl)
    bot.chat_history.clear()
    await bot.handle_slash_command('/jump 5')
    assert any('Position must be between' in m['message'] for m in bot.chat_history)


@pytest.mark.asyncio
async def test_add_failure_and_remove_usage(monkeypatch):
    bot = make_bot()

    # Make MediaLink.from_url raise
    class ML:
        @staticmethod
        def from_url(url):
            raise ValueError('bad url')

    import juiced.tui_bot as tui_mod
    monkeypatch.setattr(tui_mod, 'MediaLink', ML, raising=False)

    await bot.handle_slash_command('/add http://bad')
    assert any('Failed to add media' in m['message'] for m in bot.chat_history)

    # remove with no args
    bot.chat_history.clear()
    await bot.handle_slash_command('/remove')
    assert any('Usage: /remove' in m['message'] for m in bot.chat_history)
