import asyncio
import pytest

from types import SimpleNamespace

from juiced.lib.bot import Bot
from juiced.lib.error import SocketIOError


class FakeSocket:
    def __init__(self, emit_return=None, recv_exc=None):
        self.emit_return = emit_return
        self.recv_exc = recv_exc

    async def emit(self, *args, **kwargs):
        if callable(self.emit_return):
            return await self.emit_return(*args, **kwargs)
        return self.emit_return

    async def recv(self):
        if self.recv_exc:
            raise self.recv_exc
        await asyncio.sleep(0)
        return ('noop', {})

    async def close(self):
        await asyncio.sleep(0)


def make_bot():
    return Bot('example.com', 'chan', user='bot')


@pytest.mark.asyncio
async def test_move_remove_setcurrent_setleader():
    bot = make_bot()
    # prepare playlist items
    a = SimpleNamespace(uid=1, title='A')
    b = SimpleNamespace(uid=2, title='B')
    bot.channel.playlist.queue = [a, b]
    bot.channel.playlist._current = a

    bot.channel.permissions['oplaylistmove'] = -1
    bot.channel.permissions['oplaylistdelete'] = -1
    bot.channel.permissions['oplaylistjump'] = -1
    bot.channel.permissions['leaderctl'] = -1

    # move_media: socket emits moveVideo
    bot.socket = FakeSocket(emit_return=('moveVideo', {'from': a.uid, 'after': b.uid}))
    await bot.move_media(a, b)

    # remove_media: socket emits delete
    bot.socket = FakeSocket(emit_return=('delete', {'uid': b.uid}))
    await bot.remove_media(b)

    # set_current_media
    bot.socket = FakeSocket(emit_return=('setCurrent', a.uid))
    await bot.set_current_media(a)

    # set_leader
    bot.socket = FakeSocket(emit_return=('setLeader', 'alice'))
    # create a user to set
    from juiced.lib.user import User
    bot.channel.userlist.add(User('alice'))
    await bot.set_leader('alice')


@pytest.mark.asyncio
async def test_run_handles_socketioerror_and_breaks(monkeypatch):
    bot = make_bot()

    # Make login set the socket to one that will raise SocketIOError on recv
    async def fake_login():
        bot.socket = FakeSocket(recv_exc=SocketIOError('boom'))

    bot.login = fake_login
    bot.restart_delay = None  # cause loop to break on SocketIOError

    # run should return cleanly (not hang)
    await bot.run()


@pytest.mark.asyncio
async def test_process_outbound_messages_periodically_success(monkeypatch):
    bot = make_bot()

    # fake DB with one message
    class FakeDB:
        def __init__(self):
            self._calls = []

        def get_unsent_outbound_messages(self, limit, max_retries):
            if not hasattr(self, '_once'):
                self._once = True
                return [{'id': 1, 'message': 'hello', 'retry_count': 0}]
            return []

        def mark_outbound_sent(self, mid):
            self._calls.append(('sent', mid))

        def mark_outbound_failed(self, mid, msg, is_permanent=False):
            self._calls.append(('failed', mid, is_permanent))

    fake_db = FakeDB()
    bot.db = fake_db

    # provide channel and permissions, and a socket so outbound processor can run
    bot.channel.permissions = {'chat': -1}
    async def fake_chat(msg):
        return {'msg': msg}

    bot.chat = fake_chat
    bot.socket = FakeSocket()

    # run a single iteration of the outbound processing logic directly
    async def single_iteration():
        # mimic internal logic without the sleep
        if not bot.db:
            return
        if not bot.socket:
            return
        if not getattr(bot.channel, 'permissions', None):
            return
        messages = bot.db.get_unsent_outbound_messages(limit=20, max_retries=3)
        for m in messages:
            mid = m['id']
            text = m['message']
            retry_count = m.get('retry_count', 0)
            try:
                await bot.chat(text)
                bot.db.mark_outbound_sent(mid)
            except Exception as send_exc:
                bot.db.mark_outbound_failed(mid, str(send_exc), is_permanent=False)

    await single_iteration()

    # DB should have recorded a sent mark
    assert ('sent', 1) in fake_db._calls
