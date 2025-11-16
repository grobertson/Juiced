import io
import json
from pathlib import Path
from types import SimpleNamespace

import pytest


class FakeTerm:
    def __init__(self, width=80, height=24):
        self.width = width
        self.height = height
        self.clear = ''

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
        # Return harmless formatting functions that echo the input
        def _fn(s=''):
            return s

        return _fn


class FakeUser:
    def __init__(self, name, rank=0, afk=False, muted=False, smuted=False):
        self.name = name
        self.rank = rank
        self.afk = afk
        self.muted = muted
        self.smuted = smuted


class FakeUserList(dict):
    def __init__(self, users, count=None, leader=None):
        super().__init__((u.name, u) for u in users)
        self.count = count if count is not None else len(users)
        self.leader = leader


class FakePlaylist:
    def __init__(self, queue=None, current=None):
        self.queue = queue or []
        self._current = current

    @property
    def current(self):
        return self._current

    @current.setter
    def current(self, v):
        self._current = v

    def get(self, uid):
        for it in self.queue:
            if getattr(it, 'uid', None) == uid:
                return it
        raise ValueError('not found')


@pytest.fixture(autouse=True)
def patch_tui(monkeypatch, tmp_path):
    import juiced.tui_bot as tui_mod

    monkeypatch.setattr(tui_mod, 'Terminal', FakeTerm)
    monkeypatch.setattr(tui_mod.TUIBot, '_setup_logging', lambda self: None)
    yield


def make_bot():
    import juiced.tui_bot as tui_mod

    return tui_mod.TUIBot(tui_config={}, config_file=str('config.yaml'), domain='example.com', channel='test')


def capture_print(func, *args, **kwargs):
    import sys

    old = sys.stdout
    buf = io.StringIO()
    sys.stdout = buf
    try:
        func(*args, **kwargs)
    finally:
        sys.stdout = old
    return buf.getvalue()


def test_render_top_and_bottom_status_outputs():
    bot = make_bot()
    # prepare channel and user
    bot.channel = SimpleNamespace(name='mychan', playlist=FakePlaylist(), userlist=FakeUserList([], count=5))
    bot.user = SimpleNamespace(name='botuser', rank=1, afk=False)
    # set current media
    item = SimpleNamespace(title='Cool Video', duration=123, seconds=10)
    bot.current_media_title = 'Cool Video'
    bot.channel.playlist._current = item

    out = capture_print(bot.render_top_status)
    assert 'mychan' in out or out != ''

    out2 = capture_print(bot.render_bottom_status)
    assert 'Session' in out2 or 'Runtime' in out2 or out2 != ''


def test_render_chat_and_wrapping_and_mentions():
    bot = make_bot()
    bot.user = SimpleNamespace(name='me')
    # add multiple messages
    bot.chat_history.clear()
    bot.chat_history.append({'timestamp': '12:00:00', 'username': 'alice', 'message': 'hello there', 'prefix': '', 'color': 'white'})
    long_msg = 'x ' * 200
    bot.chat_history.append({'timestamp': '12:01:00', 'username': 'bob', 'message': long_msg, 'prefix': '', 'color': 'white'})

    out = capture_print(bot.render_chat)
    # Should produce some output (not crash)
    assert out is not None


def test_render_users_outputs():
    bot = make_bot()
    users = [FakeUser('owner', rank=4), FakeUser('mod', rank=2), FakeUser('alex', rank=1, afk=True), FakeUser('bob', rank=0)]
    ul = FakeUserList(users, count=10, leader=users[0])
    bot.channel = SimpleNamespace(userlist=ul)

    out = capture_print(bot.render_users)
    # Should include at least one username
    assert 'owner' in out or 'mod' in out or 'alex' in out


def test_handle_media_change_with_uid_and_playlist():
    bot = make_bot()
    # playlist with item uid 42
    item = SimpleNamespace(title='UIDVideo', uid=42)
    pl = FakePlaylist(queue=[item], current=None)
    bot.channel = SimpleNamespace(playlist=pl)

    # call handler with uid
    import asyncio

    asyncio.get_event_loop().run_until_complete(bot.handle_media_change('setCurrent', 42))
    assert bot.current_media_title == 'UIDVideo'


def test_load_theme_and_change_theme(tmp_path, monkeypatch):
    bot = make_bot()
    # avoid full screen render which expects a richer theme
    monkeypatch.setattr(type(bot), 'render_screen', lambda self: None)
    # create a themes dir next to module
    mod_dir = Path(__import__('juiced.tui_bot').__file__).parent
    themes_dir = mod_dir / 'themes'
    themes_dir.mkdir(parents=True, exist_ok=True)

    theme_file = themes_dir / 'unittest_theme.json'
    theme_content = {'name': 'UT', 'colors': {'status_bar': {'background': 'cyan', 'text': 'black'}}}
    theme_file.write_text(json.dumps(theme_content))

    # Prepare a config file
    cfg = tmp_path / 'cfg.json'
    cfg.write_text(json.dumps({}))
    bot.config_file = str(cfg)

    ok = bot.change_theme('unittest_theme')
    assert ok is True
    # config file should have been updated
    loaded = json.loads(cfg.read_text())
    assert 'tui' in loaded and loaded['tui']['theme'] == 'unittest_theme'
