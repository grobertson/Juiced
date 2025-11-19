import pytest

from juiced.lib import error as err


def test_exception_hierarchy_and_subclasses():
    # CytubeError is the base for channel-related errors
    assert issubclass(err.ProxyConfigError, err.CytubeError)
    assert issubclass(err.SocketConfigError, err.CytubeError)
    assert issubclass(err.LoginError, err.CytubeError)
    assert issubclass(err.Kicked, err.CytubeError)
    assert issubclass(err.ChannelError, err.CytubeError)
    assert issubclass(err.ChannelPermissionError, err.ChannelError)

    # SocketIOError is a separate base for socket exceptions
    assert issubclass(err.ConnectionFailed, err.SocketIOError)
    assert issubclass(err.ConnectionClosed, err.SocketIOError)
    assert issubclass(err.PingTimeout, err.ConnectionClosed)

    # Cross-family checks
    assert not issubclass(err.SocketIOError, err.CytubeError)


def test_instantiation_and_message_propagation():
    classes = [
        err.CytubeError,
        err.ProxyConfigError,
        err.SocketConfigError,
        err.LoginError,
        err.Kicked,
        err.ChannelError,
        err.ChannelPermissionError,
        err.SocketIOError,
        err.ConnectionFailed,
        err.ConnectionClosed,
        err.PingTimeout,
    ]

    for cls in classes:
        # without message
        ex = cls()
        assert isinstance(ex, Exception)
        assert ex.args == ()

        # with message
        m = f"test-message-for-{cls.__name__}"
        ex2 = cls(m)
        # message should appear in args and str()
        assert ex2.args == (m,)
        assert m in str(ex2)


def test_raise_and_catch_behaviour():
    # Raising a Kicked should be catchable as CytubeError
    with pytest.raises(err.Kicked):
        raise err.Kicked("bye")

    try:
        raise err.Kicked("bye")
    except err.CytubeError as e:
        assert isinstance(e, err.Kicked)
    else:
        pytest.fail("Kicked was not caught as CytubeError")

    # Raising a connection-related error should be catchable as SocketIOError
    with pytest.raises(err.ConnectionClosed):
        raise err.PingTimeout("timeout")

    try:
        raise err.ConnectionFailed("connfail")
    except err.SocketIOError as e:
        assert isinstance(e, err.ConnectionFailed)
    else:
        pytest.fail("ConnectionFailed was not caught as SocketIOError")
