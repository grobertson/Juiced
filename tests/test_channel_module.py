import pytest

from juiced.lib.channel import Channel
from juiced.lib.user import User
from juiced.lib.error import ChannelPermissionError


def test_channel_str_and_permissions():
    ch = Channel('mychan')
    assert 'mychan' in str(ch)

    u = User('alice', rank=1)
    ch.permissions['act'] = 2.0
    with pytest.raises(ChannelPermissionError):
        ch.check_permission('act', u)

    # unknown action
    with pytest.raises(ValueError):
        ch.check_permission('noaction', u)

    # has_permission returns bool
    ch.permissions['act2'] = 0.0
    assert ch.has_permission('act2', u) is True
