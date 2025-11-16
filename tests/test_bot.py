import asyncio
import json

import pytest

from juiced.lib.bot import Bot
from juiced.lib.error import SocketConfigError, ChannelError, ChannelPermissionError, Kicked
from juiced.lib.user import User


class FakeSocket:
    def __init__(self, emit_return=None, close_raises=False):
        self.emit_return = emit_return
        self.closed = False
        self.close_raises = close_raises

    async def emit(self, *args, **kwargs):
        # simple passthrough return or coroutine
        if callable(self.emit_return):
            return await self.emit_return(*args, **kwargs)
        return self.emit_return

    async def close(self):
        if self.close_raises:
            raise RuntimeError('close failed')
        self.closed = True

    async def recv(self):
        await asyncio.sleep(0)
        return ('noop', {})


def make_bot():
    # create a Bot with simple domain/channel and no DB
    return Bot('example.com', 'chan', user='bot')


def test_on_off_handlers():
    bot = make_bot()
    calls = []

    def h1(e, d):
        calls.append(('h1', e, d))

    async def h2(e, d):
        calls.append(('h2', e, d))

    bot.on('evt', h1, h2)
    assert 'evt' in bot.handlers
    # duplicate add should warn but not duplicate
    bot.on('evt', h1)
    assert bot.handlers['evt'].count(h1) == 1

    bot.off('evt', h1)
    assert h1 not in bot.handlers['evt']


@pytest.mark.asyncio
async def test_trigger_sync_and_async_handlers_stop():
    bot = make_bot()
    seq = []

    def s1(e, d):
        seq.append('s1')

    async def a1(e, d):
        seq.append('a1')

    def stopper(e, d):
        seq.append('stopper')
        return True

    bot.on('test', s1, a1)
    await bot.trigger('test', {'x': 1})
    assert seq == ['s1', 'a1']

    seq.clear()
    bot.on('test', stopper)
    await bot.trigger('test', {})
    # stopper should have stopped further handlers
    assert 'stopper' in seq


@pytest.mark.asyncio
async def test_trigger_kick_raises():
    bot = make_bot()
    with pytest.raises(Kicked):
        await bot.trigger('kick', {'reason': 'nope'})


@pytest.mark.asyncio
async def test_get_socket_config_success_and_failure(monkeypatch):
    bot = make_bot()

    async def fake_get(url):
        # return JSON string with secure server
        return json.dumps({'servers': [{'url': 's1', 'secure': False}, {'url': 's2', 'secure': True}]})

    bot.get = fake_get
    await bot.get_socket_config()
    assert bot.server is not None
    assert 's2' in bot.server

    async def fake_get_bad(url):
        return json.dumps({'servers': []})

    bot.get = fake_get_bad
    with pytest.raises(SocketConfigError):
        await bot.get_socket_config()


@pytest.mark.asyncio
async def test_disconnect_close_behavior():
    bot = make_bot()
    bot.socket = FakeSocket()
    bot.user.rank = 5
    await bot.disconnect()
    assert bot.socket is None
    assert bot.user.rank == -1

    bot.socket = FakeSocket(close_raises=True)
    with pytest.raises(RuntimeError):
        await bot.disconnect()
    # even when close raises, socket is cleared and rank reset
    assert bot.socket is None
    assert bot.user.rank == -1


@pytest.mark.asyncio
async def test_chat_success_and_timeouts():
    bot = make_bot()
    # ensure permission checks pass
    bot.channel.permissions['chat'] = -1
    bot.user.name = 'bot'

    # success
    bot.socket = FakeSocket(emit_return=('chatMsg', {'username': 'bot', 'msg': 'hi'}))
    res = await bot.chat('hi')
    assert res['msg'] == 'hi'

    # timeout (emit returns None)
    bot.socket = FakeSocket(emit_return=None)
    with pytest.raises(ChannelError):
        await bot.chat('hi')


@pytest.mark.asyncio
async def test_kick_permission_and_success():
    bot = make_bot()
    # prepare userlist and users
    target = User('alice', rank=0)
    bot.channel.userlist.add(target)

    # set bot rank low => cannot kick
    bot.user.rank = 0
    bot.channel.permissions['kick'] = -1
    with pytest.raises(ChannelPermissionError):
        await bot.kick('alice')

    # set bot rank higher and socket returns userLeave
    bot.user.rank = 100
    bot.socket = FakeSocket(emit_return=('userLeave', {'name': 'alice'}))
    await bot.kick('alice')


@pytest.mark.asyncio
async def test_login_success_and_needpassword():
    bot = make_bot()

    # helper to produce sequential emit responses
    seq = [('', {}), ('login', {'success': True})]

    async def emit_seq(*args, **kwargs):
        return seq.pop(0)

    async def fake_connect():
        bot.socket = FakeSocket(emit_return=emit_seq)

    bot.connect = fake_connect
    # should not raise
    await bot.login()

    # now simulate needPassword on joinChannel
    seq2 = [('needPassword', {})]

    async def emit_seq2(*args, **kwargs):
        return seq2.pop(0)

    async def fake_connect2():
        bot.socket = FakeSocket(emit_return=emit_seq2)

    bot.connect = fake_connect2
    with pytest.raises(Exception):
        # LoginError expected
        await bot.login()


@pytest.mark.asyncio
async def test_pm_success_and_error():
    bot = make_bot()
    bot.channel.permissions['chat'] = -1
    bot.user.name = 'bot'

    # success
    bot.socket = FakeSocket(emit_return=('pm', {'username': 'bot', 'to': 'alice', 'msg': 'hi'}))
    res = await bot.pm('alice', 'hi')
    assert res['msg'] == 'hi'

    # error
    bot.socket = FakeSocket(emit_return=('errorMsg', {'msg': 'no pm'}))
    with pytest.raises(ChannelError):
        await bot.pm('alice', 'hi')


@pytest.mark.asyncio
async def test_add_media_success_and_queuefail(monkeypatch):
    from juiced.lib.media_link import MediaLink

    bot = make_bot()
    bot.channel.permissions['oplaylistadd'] = -1
    bot.user.name = 'bot'
    link = MediaLink('yt', 'abc')

    # success
    bot.socket = FakeSocket(emit_return=('queue', {'item': {'media': {'type': 'yt', 'id': 'abc'}, 'queueby': 'bot'}}))
    res = await bot.add_media(link)
    assert 'item' in res

    # queueFail
    bot.socket = FakeSocket(emit_return=('queueFail', {'msg': 'bad'}))
    with pytest.raises(ChannelError):
        await bot.add_media(link)


@pytest.mark.asyncio
async def test_pause_leader_and_not_leader():
    bot = make_bot()
    # not leader -> raise
    bot.user = User('bot')
    bot.channel.userlist.leader = None
    with pytest.raises(ChannelPermissionError):
        await bot.pause()

    # set leader and no current media -> no emit and return
    bot.channel.userlist.leader = bot.user
    bot.channel.playlist.current = None
    # socket not required; should not raise
    await bot.pause()
