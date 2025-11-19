import pytest

from juiced.lib.bot import Bot
from juiced.lib.error import SocketIOError
from juiced.lib.user import User


def make_bot():
    return Bot("example.com", "chan", user="bot")


def test_on_userlist_and_add_user_and_usercount_updates_db():
    bot = make_bot()

    # fake DB to observe calls
    calls = {}

    class FakeDB:
        def user_joined(self, username):
            calls.setdefault("joined", []).append(username)

        def update_high_water_mark(self, chat_users, connected_count):
            calls["hwm"] = (chat_users, connected_count)

        def user_left(self, username):
            calls.setdefault("left", []).append(username)

    bot.db = FakeDB()

    # initial userlist
    bot._on_userlist(None, [{"name": "alice", "rank": 1}, {"name": "bob", "rank": 2}])
    assert "alice" in bot.channel.userlist
    assert "bob" in bot.channel.userlist

    # add user
    bot._on_addUser(None, {"name": "carol"})
    assert "carol" in bot.channel.userlist
    assert "carol" in calls.get("joined", [])

    # usercount event should update db high water mark
    bot._on_usercount(None, 42)
    assert calls.get("hwm") is not None


def test_set_user_meta_and_rank_and_afk_and_leader():
    bot = make_bot()
    # add user
    bot.channel.userlist.add(User("dave"))

    # set user meta for existing user - set known meta keys
    bot._on_setUserMeta(None, {"name": "dave", "meta": {"afk": True, "aliases": ["x"]}})
    m = bot.channel.userlist["dave"].meta
    assert m["afk"] is True
    assert "x" in m["aliases"]

    # set rank
    bot._on_setUserRank(None, {"name": "dave", "rank": 3})
    assert bot.channel.userlist["dave"].rank == 3

    # set afk
    bot._on_setAFK(None, {"name": "dave", "afk": True})
    assert bot.channel.userlist["dave"].afk is True

    # set leader
    bot._on_setLeader(None, bot.channel.userlist["dave"])
    assert bot.channel.userlist.leader == bot.channel.userlist["dave"]


@pytest.mark.asyncio
async def test_run_creates_and_cancels_background_tasks_on_socketioerror():
    bot = make_bot()

    # make DB truthy so tasks are created
    bot.db = object()

    # fake login that sets a socket whose recv raises SocketIOError
    async def fake_login():
        class S:
            async def recv(self):
                raise SocketIOError("boom")

            async def close(self):
                return None

        bot.socket = S()

    bot.login = fake_login
    bot.restart_delay = None

    await bot.run()

    # background tasks should have been created and canceled
    assert bot._history_task is not None
    assert bot._status_task is not None
    assert bot._outbound_task is not None
    assert bot._maintenance_task is not None

    # Tasks should be done (cancelled or finished)
    assert bot._history_task.done()
    assert bot._status_task.done()
    assert bot._outbound_task.done()
    assert bot._maintenance_task.done()
