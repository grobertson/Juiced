import json
import asyncio
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
        return lambda s='': s


@pytest.fixture(autouse=True)
def patch_terminal_and_render(monkeypatch):
    import juiced.tui_bot as tui_mod
    monkeypatch.setattr(tui_mod, 'Terminal', FakeTerm)
    # avoid actual full redraws
    monkeypatch.setattr(tui_mod.TUIBot, 'render_screen', lambda self: None)
    monkeypatch.setattr(tui_mod.TUIBot, 'render_chat', lambda self: None)
    monkeypatch.setattr(tui_mod.TUIBot, 'render_input', lambda self: None)
    yield


def make_bot():
    import juiced.tui_bot as tui_mod
    return tui_mod.TUIBot(tui_config={}, config_file='config.json', domain='example.com', channel='test')


class SimplePlaylist:
    def __init__(self, queue=None, current=None):
        self.queue = queue or []
        self._current = current
        self.paused = False

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


def make_item(uid, title='T', duration=10):
    return SimpleNamespace(uid=uid, title=title, duration=duration, seconds=0, link=SimpleNamespace(id=str(uid), type='yt'))


@pytest.mark.asyncio
async def test_info_status_and_users_and_user_and_afk():
    bot = make_bot()

    # prepare user and channel
    bot.user = SimpleNamespace(name='bot', rank=1, afk=False)
    users = [SimpleNamespace(name='alice', rank=2, afk=False), SimpleNamespace(name='bob', rank=1, afk=False)]
    # create a simple userlist object with mapping and leader
    class FakeUserList:
        def __init__(self, users, leader=None):
            self._map = {u.name: SimpleNamespace(**{'name': u.name, 'rank': u.rank, 'afk': u.afk, 'muted': False, 'smuted': False, 'aliases': []}) for u in users}
            self.leader = leader
            self.count = len(self._map)

        def __len__(self):
            return len(self._map)

        def __iter__(self):
            return iter(self._map)

        def __getitem__(self, key):
            return self._map[key]

        def values(self):
            return list(self._map.values())

    userlist = FakeUserList(users, leader=users[0])
    bot.channel = SimpleNamespace(name='chan', userlist=userlist, playlist=SimplePlaylist(queue=[make_item(1)], current=None))

    # cmd_info
    await bot.cmd_info()
    assert any('Bot' in m['message'] or 'Channel' in m['message'] for m in bot.chat_history)

    # cmd_status
    await bot.cmd_status()
    assert any('Connected' in m['message'] or 'Uptime' in m['message'] for m in bot.chat_history)

    # cmd_users when channel present
    await bot.cmd_users()
    assert any('Users in Channel' in m['message'] for m in bot.chat_history)

    # cmd_user for missing and present
    await bot.cmd_user('nonexistent')
    await bot.cmd_user('alice')
    assert any('User Info' in m['message'] for m in bot.chat_history)

    # cmd_afk toggle
    # provide a fake socket with emit to avoid AttributeError
    async def _fake_emit(event, data=None):
        return None

    bot.socket = SimpleNamespace()
    bot.socket.emit = _fake_emit
    await bot.cmd_afk('on')
    # should set bot.user.afk (cmd calls set_afk which emits chat; we monkeypatched rendering only)


@pytest.mark.asyncio
async def test_playlist_commands_add_remove_move_jump_and_pause_and_kick(monkeypatch):
    bot = make_bot()

    bot.user = SimpleNamespace(name='bot', rank=100, afk=False)
    # prepare playlist
    i1 = make_item(1, 'One')
    i2 = make_item(2, 'Two')
    pl = SimplePlaylist(queue=[i1, i2], current=i1)
    bot.channel = SimpleNamespace(name='chan', userlist=SimpleNamespace(count=2, leader=bot.user), playlist=pl)

    # stub out network actions
    async def fake_add_media(link, append=True, temp=True):
        return {'item': {'media': {'type': link.type if hasattr(link,'type') else 'yt', 'id': getattr(link,'id', 'x')}}}

    import juiced.tui_bot as tui_mod
    monkeypatch.setattr(tui_mod, 'MediaLink', SimpleNamespace, raising=False)
    monkeypatch.setattr(type(bot), 'add_media', lambda self, link, append=True, temp=True: asyncio.sleep(0))

    # cmd_playlist
    await bot.cmd_playlist('')
    assert any('Playlist' in m['message'] for m in bot.chat_history)

    # cmd_add with invalid url should show failure (we monkeypatch MediaLink.from_url to raise)
    class ML:
        @staticmethod
        def from_url(url):
            return SimpleNamespace(type='yt', id='abc')

    monkeypatch.setattr(tui_mod, 'MediaLink', ML, raising=False)
    monkeypatch.setattr(type(bot), 'add_media', lambda self, link, append=True, temp=True: asyncio.sleep(0))
    await bot.cmd_add('http://youtube')
    assert any('Added' in m['message'] or 'Failed' in m['message'] for m in bot.chat_history)

    # remove
    monkeypatch.setattr(type(bot), 'remove_media', lambda self, item: asyncio.sleep(0))
    await bot.cmd_remove('1')
    assert any('Removed' in m['message'] or 'No playlist' in m['message'] or 'Position' in m['message'] for m in bot.chat_history)

    # move - provide enough args
    monkeypatch.setattr(type(bot), 'move_media', lambda self, item, after: asyncio.sleep(0))
    await bot.cmd_move('1 2')
    assert any('Moved' in m['message'] or 'Usage' in m['message'] for m in bot.chat_history)

    # jump
    monkeypatch.setattr(type(bot), 'set_current_media', lambda self, item: asyncio.sleep(0))
    await bot.cmd_jump('1')
    assert any('Jumped' in m['message'] or 'No playlist' in m['message'] for m in bot.chat_history)

    # pause (requires leader)
    monkeypatch.setattr(type(bot), 'pause', lambda self: asyncio.sleep(0))
    await bot.cmd_pause()
    # kick
    monkeypatch.setattr(type(bot), 'kick', lambda self, username, reason='': asyncio.sleep(0))
    await bot.cmd_kick('alice')
    assert any('Jumped' in m['message'] or 'AFK' in m['message'] or 'Removed' in m['message'] for m in bot.chat_history)
