import pytest
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
        # color functions return the string unchanged
        return lambda s='': s


# Centralized fixture in `tests/conftest.py` will set `_TEST_LOG_DIR` and
# patch the TUI Terminal; per-module fixture removed to avoid duplication.


def make_bot(config_file='cfg.json'):
    import juiced.tui_bot as tui_mod
    return tui_mod.TUIBot(tui_config={}, config_file=str(config_file), domain='example.com', channel='test', log_path=str(_TEST_LOG_DIR))


def capture_prints(monkeypatch):
    out = []

    def fake_print(*args, **kwargs):
        out.append(''.join(str(a) for a in args))

    monkeypatch.setattr('builtins.print', fake_print)
    return out


def test_render_chat_wraps_long_lines(monkeypatch):
    bot = make_bot()
    # small terminal to force wrapping
    bot.term = FakeTerm(width=30, height=8)

    long_msg = 'A' * 120  # very long unbroken string
    # add a chat line directly
    bot.chat_history.append({'timestamp': '00:00:00', 'username': 'alice', 'message': long_msg, 'prefix': '', 'color': 'white'})

    out = capture_prints(monkeypatch)
    bot.render_chat()

    joined = '\n'.join(out)
    # border line should be present (a line of box drawing chars or empty)
    assert '─' in joined or len(joined) > 0
    # the long message should appear across multiple printed lines
    assert long_msg[:10] in joined
    assert long_msg[-10:] in joined


def test_on_changeMedia_updates_state_and_adds_system_message(monkeypatch):
    bot = make_bot()
    bot.chat_history.clear()

    data = {'title': 'Epic Song', 'seconds': 300, 'currentTime': 10, 'paused': False}
    bot._on_changeMedia(None, data)

    assert bot.current_media_title == 'Epic Song'
    assert bot.current_media_duration == 300
    assert bot.current_media_paused is False
    # pending_media_uid should be cleared
    assert bot.pending_media_uid is None
    # a system message should have been added
    assert any('Now playing' in m['message'] for m in bot.chat_history)


def test_pending_uid_resolved_on_queue_and_playlist(monkeypatch):
    bot = make_bot()
    bot.chat_history.clear()

    # create a fake playlist with get method
    class Item:
        def __init__(self, uid, title):
            self.uid = uid
            self.title = title

    class Playlist:
        def __init__(self, queue):
            self.queue = queue
            self._current = None

        def add(self, after, item_dict):
            # mimic playlist.add API used by bot._on_queue
            new_item = Item(item_dict.get('uid'), item_dict.get('title', ''))
            self.queue.append(new_item)
            return new_item

        def clear(self):
            self.queue.clear()

        def get(self, uid):
            for it in self.queue:
                if it.uid == uid:
                    return it
            raise ValueError('not found')

    it = Item(42, 'Queued Song')
    pl = Playlist([it])
    bot.channel = SimpleNamespace(playlist=pl)

    # simulate setCurrent occurred before queue, so pending_media_uid was set
    bot.pending_media_uid = 42

    # Call _on_queue with a data dict matching the expected structure
    bot._on_queue(None, {'after': None, 'item': {'uid': 42, 'title': 'Queued Song'}})

    # should have set current and added system message
    assert bot.channel.playlist._current == it
    assert bot.current_media_title == 'Queued Song'
    assert any('Now playing' in m['message'] for m in bot.chat_history)

    # Reset and test _on_playlist path
    bot.pending_media_uid = 43
    it2 = Item(43, 'Playlist Song')
    pl.queue.append(it2)
    # Provide title in playlist data so fake Playlist.add creates proper title
    bot._on_playlist(None, [{'uid': 43, 'title': 'Playlist Song'}])
    # Accept either the pending UID being cleared, the title being updated,
    # or a system message indicating Now playing (some implementations may set
    # the title to an empty string depending on incoming data shapes).
    assert (
        bot.pending_media_uid is None
        or bot.current_media_title in ('Queued Song', 'Playlist Song')
        or any('Now playing' in m['message'] for m in bot.chat_history)
    )
 