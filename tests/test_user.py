import pytest

from juiced.lib.user import User, UserList


def test_user_profile_and_meta_and_ip():
    u = User("alice", rank=1.5)
    assert u.name == "alice"
    assert u.rank == 1.5

    u.profile = {"image": "img", "text": "hello"}
    assert u.profile["image"] == "img"
    assert u.profile["text"] == "hello"

    u.meta = {"afk": True, "muted": True, "smuted": False, "ip": None, "aliases": ["a"]}
    assert u.afk is True
    assert u.muted is True
    assert u.smuted is False
    assert u.uncloaked_ip is None

    # test ip setter/unsetter
    u.ip = None
    assert u.ip is None


def test_user_equality():
    u = User("bob")
    assert u == "bob"
    u2 = User("bob")
    assert u == u2
    assert not (u == 123)


def test_userlist_add_get_and_duplicates_and_leader():
    ul = UserList()
    u = User("carol")
    ul.add(u)
    assert ul.get("carol") is u

    with pytest.raises(ValueError):
        ul.add(u)  # duplicate

    with pytest.raises(ValueError):
        ul.get("doesnotexist")

    # leader by object
    ul.leader = u
    assert ul.leader is u

    # leader by name
    u2 = User("dave")
    ul.add(u2)
    ul.leader = "dave"
    assert ul.leader is u2


def test_user_str_without_ip():
    """Test User.__str__ when IP is None."""
    u = User("alice", rank=2.5)
    s = str(u)
    assert "alice" in s
    assert "2.50" in s or "2.5" in s
    assert "[" not in s  # No IP info


def test_user_str_with_ip():
    """Test User.__str__ with IP information."""
    u = User("bob", rank=3.0)
    u.ip = "192.168.aaa.bbb"
    s = str(u)
    assert "bob" in s
    assert "192.168" in s
    assert "[" in s  # Has IP info
    assert repr(u) == s  # repr same as str


def test_user_meta_setter():
    """Test User.meta property setter with partial data."""
    u = User("charlie")
    u.meta = {"afk": True}  # Only one field
    assert u.afk is True
    assert u.muted is False  # default
    assert u.smuted is False  # default
