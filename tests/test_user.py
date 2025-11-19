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
