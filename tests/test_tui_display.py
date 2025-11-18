
from juiced.tui_bot import TUIBot


class FakeUser:
    def __init__(self, name, rank=0):
        self.name = name
        self.rank = rank


def test_get_display_username_mod_and_regular(tmp_path, monkeypatch):
    # Create a TUIBot with minimal required args
    bot = TUIBot(
        tui_config={},
        domain="example.com",
        channel="test",
        user=None,
        config_file=str(tmp_path / "config.yaml"),
    )

    # Replace channel.userlist with a simple dict mapping username -> FakeUser
    bot.channel.userlist = {}
    bot.channel.userlist["alice"] = FakeUser("alice", rank=1)  # registered
    bot.channel.userlist["modjoe"] = FakeUser("modjoe", rank=2)  # moderator

    # Regular user should be unchanged
    assert bot.get_display_username("alice") == "alice"

    # Moderator should have leading @ in display only
    assert bot.get_display_username("modjoe") == "@modjoe"

    # Unknown user (not in userlist) should return raw username
    assert bot.get_display_username("nobody") == "nobody"
