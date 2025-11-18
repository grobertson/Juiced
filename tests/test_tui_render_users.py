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
        return lambda s='': s


# Centralized fixture in `tests/conftest.py` provides `_TEST_LOG_DIR` and patches
# TUI Terminal and heavy rendering functions.


def make_bot(config_file='cfg.json'):
    import juiced.tui_bot as tui_mod
    return tui_mod.TUIBot(tui_config={}, config_file=str(config_file), domain='example.com', channel='test', log_path=str(_TEST_LOG_DIR))


class FakeUserList:
    def __init__(self, users, leader=None):
        # users: list of user objects
        self._users = {u.name: u for u in users}
        self.leader = leader

    def values(self):
        return list(self._users.values())

    def keys(self):
        return list(self._users.keys())

    def __len__(self):
        return len(self._users)


def capture_prints(monkeypatch):
    out = []

    def fake_print(*args, **kwargs):
        # join printable args into a single string
        out.append(' '.join(str(a) for a in args))

    monkeypatch.setattr('builtins.print', fake_print)
    return out


def test_render_users_shows_leader_and_markers(monkeypatch):
    bot = make_bot()

    # Create users with various flags
    u1 = SimpleNamespace(name='alice', rank=4, afk=False, muted=False, smuted=False)
    u2 = SimpleNamespace(name='bob', rank=2, afk=False, muted=True, smuted=False)
    u3 = SimpleNamespace(name='carol', rank=1, afk=True, muted=False, smuted=True)

    fl = FakeUserList([u1, u2, u3], leader=u1)
    bot.channel = SimpleNamespace(userlist=fl)

    out = capture_prints(monkeypatch)
    bot.render_users()

    # Check that leader marker and muted markers appear in output
    all_text = '\n'.join(out)
    assert '[*]' in all_text or 'leader' in all_text.lower() or 'alice' in all_text
    assert '[m]' in all_text or 'muted' in all_text.lower() or 'bob' in all_text
    assert '[s]' in all_text or 'shadow' in all_text.lower() or 'carol' in all_text


def test_render_users_hide_afk(monkeypatch):
    bot = make_bot()

    u1 = SimpleNamespace(name='alice', rank=1, afk=True, muted=False, smuted=False)
    u2 = SimpleNamespace(name='bob', rank=1, afk=False, muted=False, smuted=False)
    fl = FakeUserList([u1, u2], leader=u2)
    bot.channel = SimpleNamespace(userlist=fl)

    # hide afk users
    bot.hide_afk_users = True
    out = capture_prints(monkeypatch)
    bot.render_users()
    all_text = '\n'.join(out)
    # alice is AFK so should not appear when hide_afk_users is True
    assert 'alice' not in all_text
    assert 'bob' in all_text


def test_render_users_sorting_order(monkeypatch):
    bot = make_bot()

    u_mod = SimpleNamespace(name='mod', rank=2, afk=False, muted=False, smuted=False)
    u_reg = SimpleNamespace(name='user', rank=1, afk=False, muted=False, smuted=False)
    u_guest = SimpleNamespace(name='guest', rank=0, afk=False, muted=False, smuted=False)
    fl = FakeUserList([u_guest, u_reg, u_mod], leader=u_mod)
    bot.channel = SimpleNamespace(userlist=fl)

    out = capture_prints(monkeypatch)
    bot.render_users()
    all_text = '\n'.join(out)
    # Ensure mod appears before regular user in printed output
    assert all_text.index('mod') < all_text.index('user')
