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


@pytest.mark.asyncio
async def test_bot_db_init_failure(monkeypatch):
    """Test bot handles database initialization failure gracefully."""
    from juiced.lib import bot as bot_module
    
    # Mock BotDatabase to raise exception
    class FailingDB:
        def __init__(self, *args):
            raise ValueError("DB init failed")
    
    original_db = bot_module.BotDatabase
    monkeypatch.setattr(bot_module, "BotDatabase", FailingDB)
    
    bot = bot_module.Bot(
        domain="test.com",
        channel="test",
        user="testuser",
        enable_db=True,
        db_path=":memory:"
    )
    
    # Database should be None after failed init
    assert bot.db is None
    
    monkeypatch.setattr(bot_module, "BotDatabase", original_db)


@pytest.mark.asyncio
async def test_bot_db_module_not_available(monkeypatch):
    """Test bot handles missing database module."""
    from juiced.lib import bot as bot_module
    
    original_db = bot_module.BotDatabase
    monkeypatch.setattr(bot_module, "BotDatabase", None)
    
    bot = bot_module.Bot(
        domain="test.com",
        channel="test",
        user="testuser",
        enable_db=True,
        db_path=":memory:"
    )
    
    # Database should be None when module unavailable
    assert bot.db is None
    
    monkeypatch.setattr(bot_module, "BotDatabase", original_db)


def test_on_rank_updates_user_rank():
    bot = make_bot()
    bot._on_rank(None, 3)
    assert bot.user.rank == 3


def test_on_setMotd_updates_channel_motd():
    bot = make_bot()
    bot._on_setMotd(None, "Welcome to the channel!")
    assert bot.channel.motd == "Welcome to the channel!"


def test_on_channelCSSJS_updates_channel_css_and_js():
    bot = make_bot()
    bot._on_channelCSSJS(None, {"css": "body { color: red; }", "js": "console.log('hi');"})
    assert bot.channel.css == "body { color: red; }"
    assert bot.channel.js == "console.log('hi');"


def test_on_channelCSSJS_handles_missing_keys():
    bot = make_bot()
    bot._on_channelCSSJS(None, {})
    assert bot.channel.css == ""
    assert bot.channel.js == ""


def test_on_channelOpts_updates_channel_options():
    bot = make_bot()
    opts = {"allow_voteskip": True, "allow_dupes": False}
    bot._on_channelOpts(None, opts)
    assert bot.channel.options == opts


def test_on_setPermissions_updates_channel_permissions():
    bot = make_bot()
    perms = {"seeplaylist": True, "playlistadd": False}
    bot._on_setPermissions(None, perms)
    assert bot.channel.permissions == perms


def test_on_emoteList_updates_channel_emotes():
    bot = make_bot()
    emotes = [{"name": "Kappa", "image": "kappa.png"}]
    bot._on_emoteList(None, emotes)
    assert bot.channel.emotes == emotes


def test_on_drinkCount_updates_channel_drink_count():
    bot = make_bot()
    bot._on_drinkCount(None, 42)
    assert bot.channel.drink_count == 42


def test_on_needPassword_raises_on_invalid_password():
    from juiced.lib.error import LoginError

    with pytest.raises(LoginError, match="invalid channel password"):
        Bot._on_needPassword(None, True)


def test_on_needPassword_does_not_raise_when_password_correct():
    # Should not raise when data is False (password accepted)
    Bot._on_needPassword(None, False)


def test_on_noflood_logs_error(caplog):
    bot = make_bot()
    bot._on_noflood(None, {"msg": "Slow down!"})
    assert "noflood" in caplog.text


def test_on_errorMsg_logs_error(caplog):
    bot = make_bot()
    bot._on_errorMsg(None, {"msg": "Something went wrong"})
    assert "error" in caplog.text


def test_on_queueFail_logs_playlist_error(caplog):
    bot = make_bot()
    bot._on_queueFail(None, {"msg": "Failed to add video"})
    assert "playlist error" in caplog.text


def test_on_kick_raises_kicked_exception():
    from juiced.lib.error import Kicked

    with pytest.raises(Kicked):
        Bot._on_kick(None, {"reason": "You were kicked"})


def test_on_userLeave_removes_user_and_tracks_in_db():
    bot = make_bot()

    # Add user first
    bot.channel.userlist.add(User("eve"))

    # Track DB calls
    left_users = []

    class FakeDB:
        def user_left(self, username):
            left_users.append(username)

    bot.db = FakeDB()

    # User leaves
    bot._on_userLeave(None, {"name": "eve"})

    assert "eve" not in bot.channel.userlist
    assert "eve" in left_users


def test_on_userLeave_handles_nonexistent_user(caplog):
    bot = make_bot()
    bot._on_userLeave(None, {"name": "ghost"})
    assert "not found" in caplog.text


def test_on_setUserMeta_ignores_blank_username():
    bot = make_bot()
    # Should not raise, just return early
    bot._on_setUserMeta(None, {"name": "", "meta": {"afk": True}})


def test_on_setUserMeta_logs_warning_for_unknown_user(caplog):
    bot = make_bot()
    bot._on_setUserMeta(None, {"name": "unknown", "meta": {"afk": True}})
    assert "not in userlist yet" in caplog.text


def test_on_setUserRank_ignores_blank_username():
    bot = make_bot()
    # Should not raise, just return early
    bot._on_setUserRank(None, {"name": "", "rank": 3})


def test_on_setUserRank_logs_warning_for_unknown_user(caplog):
    bot = make_bot()
    bot._on_setUserRank(None, {"name": "unknown", "rank": 3})
    assert "not in userlist yet" in caplog.text


def test_on_setAFK_ignores_blank_username():
    bot = make_bot()
    # Should not raise, just return early
    bot._on_setAFK(None, {"name": "", "afk": True})


def test_on_setAFK_logs_warning_for_unknown_user(caplog):
    bot = make_bot()
    bot._on_setAFK(None, {"name": "unknown", "afk": True})
    assert "not in userlist yet" in caplog.text


def test_on_setPlaylistMeta_updates_playlist_time():
    bot = make_bot()
    bot._on_setPlaylistMeta(None, {"rawTime": 12345})
    assert bot.channel.playlist.time == 12345


def test_on_setPlaylistMeta_handles_missing_rawTime():
    bot = make_bot()
    bot._on_setPlaylistMeta(None, {})
    assert bot.channel.playlist.time == 0


def test_on_mediaUpdate_updates_playlist_state():
    bot = make_bot()
    bot._on_mediaUpdate(None, {"paused": False, "currentTime": 42.5})
    assert bot.channel.playlist.paused is False
    assert bot.channel.playlist.current_time == 42.5


def test_on_mediaUpdate_handles_missing_fields():
    bot = make_bot()
    bot._on_mediaUpdate(None, {})
    assert bot.channel.playlist.paused is True
    assert bot.channel.playlist.current_time == 0


def test_on_voteskip_updates_voteskip_counts():
    bot = make_bot()
    bot._on_voteskip(None, {"count": 3, "need": 5})
    assert bot.channel.voteskip_count == 3
    assert bot.channel.voteskip_need == 5


def test_on_voteskip_handles_missing_fields():
    bot = make_bot()
    bot._on_voteskip(None, {})
    assert bot.channel.voteskip_count == 0
    assert bot.channel.voteskip_need == 0


def test_on_setCurrent_updates_current_media():
    bot = make_bot()
    # Add a proper playlist item first
    item = {
        "uid": 1,
        "temp": False,
        "queueby": "testuser",
        "media": {"type": "yt", "id": "abc123", "title": "Test Video", "seconds": 120},
    }
    bot.channel.playlist.add(None, item)
    # Now set it as current - _on_setCurrent receives the uid as data
    bot._on_setCurrent(None, 1)
    assert bot.channel.playlist.current.uid == 1


def test_on_queue_adds_item_to_playlist():
    bot = make_bot()
    item = {
        "uid": 1,
        "temp": False,
        "queueby": "testuser",
        "media": {"type": "yt", "id": "xyz", "title": "New Video", "seconds": 180},
    }
    bot._on_queue(None, {"after": None, "item": item})
    assert len(bot.channel.playlist.queue) == 1
    assert bot.channel.playlist.queue[0].uid == 1


def test_on_delete_removes_item_from_playlist():
    bot = make_bot()
    # Add item with proper structure
    item = {
        "uid": 1,
        "temp": False,
        "queueby": "testuser",
        "media": {"type": "yt", "id": "abc", "title": "Video", "seconds": 60},
    }
    bot.channel.playlist.add(None, item)
    # Delete it
    bot._on_delete(None, {"uid": 1})
    assert len(bot.channel.playlist.queue) == 0
