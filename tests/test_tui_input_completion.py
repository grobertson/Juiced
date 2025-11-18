import asyncio
from collections import deque
from types import SimpleNamespace

import pytest


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
        return lambda s="": s


# Centralized fixture handles Terminal and _TEST_LOG_DIR


def make_bot():
    import juiced.tui_bot as tui_mod

    return tui_mod.TUIBot(
        tui_config={},
        config_file="cfg.json",
        domain="example.com",
        channel="test",
        log_path=str(_TEST_LOG_DIR),
    )


def test_tab_completion_emote_cycle():
    bot = make_bot()
    bot.emotes = ["#smile", "#sad", "#smiley"]

    bot.input_buffer = "#s"
    bot.handle_tab_completion()
    first = bot.input_buffer
    assert first in bot.emotes

    bot.handle_tab_completion()  # cycle
    second = bot.input_buffer
    assert second in bot.emotes
    assert second != first


def test_tab_completion_username_cycle():
    bot = make_bot()
    # userlist must be dict-like with keys()
    users = {
        "alice": SimpleNamespace(name="alice"),
        "alex": SimpleNamespace(name="alex"),
        "bob": SimpleNamespace(name="bob"),
    }
    bot.channel = SimpleNamespace(userlist=users)

    bot.input_buffer = "al"
    bot.handle_tab_completion()
    first = bot.input_buffer
    assert first.lower().startswith("al")

    bot.handle_tab_completion()
    second = bot.input_buffer
    assert second.lower().startswith("al")
    assert second != first


def test_navigate_history_up_down_restores_temp():
    bot = make_bot()
    bot.input_history = deque(["first", "second"])
    bot.input_buffer = "typing"

    bot.navigate_history_up()
    assert bot.input_buffer == "second"
    bot.navigate_history_up()
    assert bot.input_buffer == "first"

    bot.navigate_history_down()
    assert bot.input_buffer == "second"
    bot.navigate_history_down()
    assert bot.input_buffer == "typing"


@pytest.mark.asyncio
async def test_process_command_sends_chat_and_handles_slash(monkeypatch):
    bot = make_bot()

    called = {}

    async def fake_chat(msg):
        called["chat"] = msg

    async def fake_handle_slash(text):
        called["slash"] = text

    monkeypatch.setattr(
        type(bot), "chat", lambda self, msg: asyncio.ensure_future(fake_chat(msg))
    )
    monkeypatch.setattr(
        type(bot),
        "handle_slash_command",
        lambda self, text: asyncio.ensure_future(fake_handle_slash(text)),
    )

    # Non-command
    bot.input_buffer = "hello world"
    await bot.process_command()
    # chat should be scheduled; wait a short moment
    await asyncio.sleep(0.01)
    assert called.get("chat") == "hello world"

    # Slash command
    called.clear()
    bot.input_buffer = "/help"
    await bot.process_command()
    await asyncio.sleep(0.01)
    assert called.get("slash") == "/help"
