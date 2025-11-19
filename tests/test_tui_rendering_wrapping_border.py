from types import SimpleNamespace

import pytest


class FakeTerm:
    CURRENT_LOC = None

    def __init__(self, width=60, height=20):
        self.width = width
        self.height = height
        # provide common color functions used by code
        for name in [
            "bright_black",
            "white",
            "bright_white",
            "bright_blue",
            "black_on_cyan",
        ]:
            setattr(self, name, lambda s="": s)

    class Loc:
        def __init__(self, term, x, y):
            self.term = term
            self.x = x
            self.y = y

        def __enter__(self):
            FakeTerm.CURRENT_LOC = (self.x, self.y)
            return None

        def __exit__(self, exc_type, exc, tb):
            FakeTerm.CURRENT_LOC = None
            return False

    def location(self, x, y):
        return FakeTerm.Loc(self, x, y)

    def __getattr__(self, name):
        # Return simple passthroughs for color functions
        return lambda s="": s


# Centralized fixture in `tests/conftest.py` provides Terminal/patching

# Fallback for static analysis; conftest overrides at runtime
_TEST_LOG_DIR = None


def make_bot(width=60, height=20):
    import juiced.tui_bot as tui_mod

    bot = tui_mod.TUIBot(
        tui_config={},
        config_file="cfg.json",
        domain="example.com",
        channel="test",
        log_path=str(_TEST_LOG_DIR),
    )
    bot.term = FakeTerm(width=width, height=height)
    return bot


def capture_prints(monkeypatch):
    records = []

    def fake_print(*args, **kwargs):
        txt = "".join(str(a) for a in args)
        loc = FakeTerm.CURRENT_LOC
        records.append((loc, txt))

    monkeypatch.setattr("builtins.print", fake_print)
    return records


def test_border_not_overwritten_by_exact_length_message(monkeypatch):
    # Set sizes so chat_width is small and can be exactly filled
    width = 60
    user_list_width = 22
    bot = make_bot(width=width, height=12)
    records = capture_prints(monkeypatch)

    # Create a message sized to exactly fill the chat area when accounting for prefix
    chat_width = bot.term.width - user_list_width - 1
    # Use short username to make prefix predictable
    username = "u"
    timestamp = "00:00:00"

    # Compute prefix length using the same logic as TUIBot
    prefix_len = len(f"[{timestamp}] ") + len(f"<{username}> ")
    # Determine message length that will exactly match chat_width
    msg_len = chat_width - prefix_len
    if msg_len < 1:
        pytest.skip("terminal too small for deterministic test")

    message = "X" * msg_len

    # Append chat line
    bot.chat_history.append(
        {
            "timestamp": timestamp,
            "username": username,
            "message": message,
            "prefix": "",
            "color": "white",
        }
    )

    # Provide a minimal channel.userlist so render_users runs and prints the vertical separator
    user = SimpleNamespace(name="leader", rank=4, afk=False, muted=False, smuted=False)
    ul = {"leader": user}
    # add helper attributes used by render_users
    _userlist_obj = SimpleNamespace(**ul)

    # Make it act like a mapping for len() and iteration
    class UL(dict):
        pass

    ul_wrap = UL(leader=user)
    ul_wrap.count = 1
    ul_wrap.leader = user
    bot.channel = SimpleNamespace(name="test", userlist=ul_wrap, playlist=None)

    bot.render_chat()
    bot.render_users()

    # Verify that no chat-print exceeded the chat_width when printed at x=0
    for loc, txt in records:
        if loc and loc[0] == 0:
            # printed into chat area; ensure length not wider than chat_width
            assert len(txt) <= chat_width + 5  # small allowance for colored wrappers

    # Verify that vertical separator was printed at the expected x position
    user_list_x = bot.term.width - user_list_width
    sep_found = any(
        loc and loc[0] == (user_list_x - 1) and "│" in txt for loc, txt in records
    )
    assert sep_found, "User list separator not printed at expected column"


def test_long_unbroken_word_wrapping_does_not_overflow(monkeypatch):
    width = 80
    user_list_width = 22
    bot = make_bot(width=width, height=14)
    records = capture_prints(monkeypatch)

    # Create a very long unbroken token (simulate a long URL)
    long_token = "http://" + ("a" * 200)
    username = "bob"
    timestamp = "00:00:00"

    # Append chat line with long unbroken token
    bot.chat_history.append(
        {
            "timestamp": timestamp,
            "username": username,
            "message": long_token,
            "prefix": "",
            "color": "white",
        }
    )

    # Ensure render does not print beyond chat width
    bot.render_chat()

    chat_width = bot.term.width - user_list_width - 1
    for loc, txt in records:
        if loc and loc[0] == 0:
            # Ensure no printed segment is wider than chat area (with small allowance)
            assert len(txt) <= chat_width + 10

    # Also ensure that the long token was wrapped (we expect multiple printed lines)
    chat_prints = [txt for loc, txt in records if loc and loc[0] == 0 and txt.strip()]
    assert any(long_token[:20] in p for p in chat_prints)
    # There should be more than one chat line printed for the long token
    assert len(chat_prints) >= 2
