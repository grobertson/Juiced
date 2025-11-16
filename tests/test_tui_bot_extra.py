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
        # Return simple lambdas for color/formatting functions
        return lambda s='': s


@pytest.fixture(autouse=True)
def patch_terminal(monkeypatch):
    import juiced.tui_bot as tui_mod
    monkeypatch.setattr(tui_mod, 'Terminal', FakeTerm)
    # Avoid heavy screen renders
    monkeypatch.setattr(tui_mod.TUIBot, 'render_screen', lambda self: None)
    monkeypatch.setattr(tui_mod.TUIBot, 'render_chat', lambda self: None)
    monkeypatch.setattr(tui_mod.TUIBot, 'render_input', lambda self: None)
    yield


def make_bot():
    import juiced.tui_bot as tui_mod
    return tui_mod.TUIBot(tui_config={}, config_file='config.json', domain='example.com', channel='test', log_path='logs_test')


def test_format_duration():
    from juiced.tui_bot import TUIBot

    assert TUIBot.format_duration(0) == '0s'
    assert TUIBot.format_duration(59) == '59s'
    # 60 seconds formats to '1m' (seconds omitted when zero)
    assert TUIBot.format_duration(60) == '1m'
    assert TUIBot.format_duration(3600 + 65) == '1h 1m 5s'
    assert TUIBot.format_duration(-1) == 'Unknown'


def test_calculate_wrapped_lines():
    bot = make_bot()
    # small chat width to force wrapping
    message = 'This is a long message that should be wrapped across multiple lines.'
    lines = bot._calculate_message_wrapped_lines(message, chat_width=20, timestamp='12:00:00', username='alice', prefix='')
    assert isinstance(lines, list)
    assert len(lines) >= 2


def test_handle_emote_list_parsing():
    bot = make_bot()
    data = [{'name': 'smile'}, '#lol', 'kappa']
    # call handler synchronously
    asyncio.get_event_loop().run_until_complete(bot.handle_emote_list(None, data))
    # All emotes should start with '#'
    assert all(e.startswith('#') for e in bot.emotes)
    # Should include normalized names and be sorted
    assert '#kappa' in bot.emotes
    assert '#lol' in bot.emotes
    assert '#smile' in bot.emotes


def test_get_completion_matches_emotes_and_usernames():
    bot = make_bot()
    # emotes
    bot.emotes = ['#smile', '#sad', '#kappa']
    em_matches = bot._get_completion_matches('#s', is_emote=True)
    assert '#sad' in em_matches and '#smile' in em_matches

    # usernames
    # create a simple userlist mapping
    usermap = {
        'Alice': SimpleNamespace(name='Alice', rank=1),
        'bob': SimpleNamespace(name='bob', rank=0),
        'charlie': SimpleNamespace(name='charlie', rank=2)
    }
    bot.channel = SimpleNamespace(userlist=usermap)
    uname_matches = bot._get_completion_matches('a', is_emote=False)
    # _get_completion_matches does not enforce minimum partial length; it should
    # return matches that start with the partial (case-insensitive)
    assert 'Alice' in uname_matches
    uname_matches2 = bot._get_completion_matches('al', is_emote=False)
    assert 'Alice' in uname_matches2
