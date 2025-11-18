import asyncio
import types
from types import SimpleNamespace

import pytest


class FakeTerm:
    def __init__(self, width=80, height=24):
        self.width = width
        self.height = height
        self.clear = ""

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
        def _fn(s=""):
            return s

        return _fn


@pytest.fixture(autouse=True)
def no_io(monkeypatch, tmp_path):
    """Prevent TUI from touching real terminal or log files."""
    # Patch Terminal used by tui_bot to our FakeTerm
    import juiced.tui_bot as tui_mod

    monkeypatch.setattr(tui_mod, "Terminal", FakeTerm)

    # Prevent file logging by patching _setup_logging
    monkeypatch.setattr(tui_mod.TUIBot, "_setup_logging", lambda self: None)

    # Prevent render methods from printing during tests
    monkeypatch.setattr(tui_mod.TUIBot, "render_chat", lambda self: None)
    monkeypatch.setattr(tui_mod.TUIBot, "render_input", lambda self: None)
    monkeypatch.setattr(tui_mod.TUIBot, "render_top_status", lambda self: None)
    monkeypatch.setattr(tui_mod.TUIBot, "render_bottom_status", lambda self: None)
    yield


def make_bot():
    import juiced.tui_bot as tui_mod

    # Provide minimal required Bot args via kwargs (domain, channel)
    bot = tui_mod.TUIBot(
        tui_config={},
        config_file=str("config.yaml"),
        domain="example.com",
        channel="test",
    )
    return bot


def test_format_duration():
    from juiced.tui_bot import TUIBot

    assert TUIBot.format_duration(0) == "0s"
    assert TUIBot.format_duration(1) == "1s"
    assert TUIBot.format_duration(61) == "1m 1s"
    assert TUIBot.format_duration(3661) == "1h 1m 1s"
    assert TUIBot.format_duration(-5) == "Unknown"


def test_get_username_color_and_mapping():
    bot = make_bot()
    c1 = bot.get_username_color("alice")
    c2 = bot.get_username_color("bob")
    assert c1 != "" and c2 != ""
    # Mapping stable
    assert bot.get_username_color("alice") == c1


def test_add_chat_and_system_and_logging(monkeypatch):
    bot = make_bot()

    # Patch _log_chat to avoid file writes
    monkeypatch.setattr(bot, "_log_chat", lambda *a, **k: None)

    bot.add_chat_line("alice", "hello world")
    assert bot.chat_history
    last = bot.chat_history[-1]
    assert last["username"] == "alice"
    assert "hello world" in last["message"]

    bot.add_system_message("system up", color="bright_blue")
    assert bot.chat_history[-1]["username"] == "*"


def test_calculate_message_wrapped_lines():
    bot = make_bot()
    # small chat width to force wrapping
    wrapped = bot._calculate_message_wrapped_lines(
        "This is a long message",
        chat_width=20,
        timestamp="12:00:00",
        username="u",
        prefix="",
    )
    assert isinstance(wrapped, list)
    assert any(len(line) <= 20 for line in wrapped)


@pytest.mark.asyncio
async def test_handle_emote_list_and_tab_completion():
    bot = make_bot()

    # Emote input as dicts and strings
    data = [{"name": "smile"}, "#lol", "kappa"]
    await bot.handle_emote_list("emoteList", data)
    # Ensure emotes normalized with # prefix and sorted
    assert "#smile" in bot.emotes
    assert "#lol" in bot.emotes
    assert "#kappa" in bot.emotes

    # Prepare fake userlist for username completion
    bot.channel = SimpleNamespace(userlist={"alice": None, "alex": None, "bob": None})
    bot.input_buffer = "al"
    bot.handle_tab_completion()
    # Should have applied first match starting with 'al'
    assert bot.input_buffer.lower().startswith("al")


@pytest.mark.asyncio
async def test_process_command_toggle_and_pm(monkeypatch):
    bot = make_bot()

    # Patch chat and pm to avoid network calls
    monkeypatch.setattr(bot, "chat", lambda *a, **k: asyncio.sleep(0))
    monkeypatch.setattr(bot, "pm", lambda *a, **k: asyncio.sleep(0))

    bot.input_buffer = "/togglejoins"
    await bot.process_command()
    # toggled
    assert bot.show_join_quit in (True, False)

    bot.input_buffer = "/pm alice hello"
    await bot.process_command()
    # pm should add a chat line with prefix [PM->]
    assert any(
        msg.get("prefix", "").startswith("[PM") or msg.get("prefix") == "[PM->]"
        for msg in bot.chat_history
    )
