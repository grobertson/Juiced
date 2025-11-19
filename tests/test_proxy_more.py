import socket
import types
import pytest


def test_wrap_module_and_set_proxy_monkeypatched(monkeypatch):
    import juiced.lib.proxy as proxy

    # Create a dummy module to be wrapped
    dummy_socket_mod = types.SimpleNamespace()
    # provide a socket submodule object with attributes to be replaced
    dummy_socket_mod.socket = types.SimpleNamespace(
        socket=lambda *a, **k: None, getaddrinfo=lambda *a, **k: None
    )
    dummy_module = types.SimpleNamespace(socket=dummy_socket_mod)

    # Create a fake socks object with required methods/consts
    class FakeSocks:
        SOCKS5 = 123

        def __init__(self):
            self.called = None

        def set_default_proxy(self, proxy_type=None, addr=None, port=None, rdns=None):
            # record call
            self.called = dict(proxy_type=proxy_type, addr=addr, port=port, rdns=rdns)

        def get_default_proxy(self):
            # simulate a proxy configured and rdns True
            return (1, None, None, True, None, None)

    fake_socks = FakeSocks()

    # Enable pysocks path
    monkeypatch.setattr(proxy, "HAS_PYSOCKS", True)
    monkeypatch.setattr(proxy, "socks", fake_socks, raising=False)
    # Make socksocket report a default proxy exists so wrap_module branches
    monkeypatch.setattr(proxy.socksocket, "default_proxy", True, raising=False)

    # Call wrap_module - should set module.socket.socket to proxy.Socket
    proxy.wrap_module(dummy_module)
    assert hasattr(dummy_module.socket, "socket")
    assert dummy_module.socket.socket is proxy.Socket
    assert dummy_module.socket.getaddrinfo is proxy.getaddrinfo

    # Now test set_proxy will call socks.set_default_proxy and wrap modules
    # Reset to a fresh dummy module
    dummy_socket_mod2 = types.SimpleNamespace()
    dummy_socket_mod2.socket = lambda *a, **k: None
    dummy_socket_mod2.getaddrinfo = lambda *a, **k: None
    dummy_module2 = types.SimpleNamespace(socket=dummy_socket_mod2)

    # Call set_proxy with explicit proxy_type equal to fake_socks.SOCKS5 to set rdns True
    proxy.set_proxy(
        "1.2.3.4", 1080, proxy_type=fake_socks.SOCKS5, modules=[dummy_module2]
    )

    # Verify fake_socks recorded the call
    assert fake_socks.called is not None
    assert fake_socks.called["addr"] == "1.2.3.4"
    assert fake_socks.called["port"] == 1080
    assert fake_socks.called["proxy_type"] == fake_socks.SOCKS5
    assert fake_socks.called["rdns"] is True


def test_getaddrinfo_uses_proxy_rdns(monkeypatch):
    import juiced.lib.proxy as proxy

    class FakeSocks2:
        def get_default_proxy(self):
            # proxy_type not None and rdns True
            return (1, None, None, True, None, None)

    fake_socks2 = FakeSocks2()
    monkeypatch.setattr(proxy, "socks", fake_socks2, raising=False)
    # Call getaddrinfo - should return a custom tuple list when rdns True
    result = proxy.getaddrinfo("example.com", 80)
    assert isinstance(result, list)
    assert result[0][0] == socket.AF_INET
    assert result[0][-1] == ("example.com", 80)


def test_socksocket_with_pysocks_available(monkeypatch):
    """Test socksocket instantiation when pysocks is available."""
    import juiced.lib.proxy as proxy

    class FakeRealSocket:
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs

    class FakeSocks:
        socksocket = FakeRealSocket

    monkeypatch.setattr(proxy, "HAS_PYSOCKS", True)
    monkeypatch.setattr(proxy, "socks", FakeSocks())

    sock = proxy.socksocket(socket.AF_INET, socket.SOCK_STREAM)
    assert hasattr(sock, "_real")
    assert isinstance(sock._real, FakeRealSocket)


def test_socksocket_missing_socksocket_attr(monkeypatch):
    """Test socksocket when pysocks exists but lacks socksocket attr."""
    import juiced.lib.proxy as proxy
    from juiced.lib.error import ProxyConfigError

    class FakeSocksNoAttr:
        pass

    monkeypatch.setattr(proxy, "HAS_PYSOCKS", True)
    monkeypatch.setattr(proxy, "socks", FakeSocksNoAttr())

    with pytest.raises(ProxyConfigError, match="socksocket not available"):
        proxy.socksocket()


def test_socket_dgram_fallback(monkeypatch):
    """Test Socket with DGRAM socket type fallback."""
    import juiced.lib.proxy as proxy

    class FakeRealSocket:
        def __init__(self, family, type, proto, fileno):
            self.type = type

    class FakeSocks:
        socksocket = FakeRealSocket

    monkeypatch.setattr(proxy, "HAS_PYSOCKS", True)
    monkeypatch.setattr(proxy, "socks", FakeSocks())

    # Invalid type should fallback to SOCK_STREAM
    sock = proxy.Socket(type=999)
    assert sock._real.type == socket.SOCK_STREAM

    # Valid DGRAM should be preserved
    sock2 = proxy.Socket(type=socket.SOCK_DGRAM)
    assert sock2._real.type == socket.SOCK_DGRAM


def test_wrap_module_missing_get_default_proxy(monkeypatch):
    """Test wrap_module when socks lacks get_default_proxy."""
    import juiced.lib.proxy as proxy
    from juiced.lib.error import ProxyConfigError

    class FakeSocksNoMethod:
        pass

    monkeypatch.setattr(proxy, "socks", FakeSocksNoMethod())

    dummy_module = types.SimpleNamespace(socket=None)
    with pytest.raises(ProxyConfigError, match="get_default_proxy"):
        proxy.wrap_module(dummy_module)


def test_wrap_module_no_proxy_configured(monkeypatch):
    """Test wrap_module when no default proxy is set."""
    import juiced.lib.proxy as proxy
    from juiced.lib.error import ProxyConfigError

    class FakeSocksNoProxy:
        def get_default_proxy(self):
            return (None, None, None, None, None, None)

    monkeypatch.setattr(proxy, "socks", FakeSocksNoProxy())

    dummy_module = types.SimpleNamespace(socket=None)
    with pytest.raises(ProxyConfigError, match="no default proxy"):
        proxy.wrap_module(dummy_module)


def test_set_proxy_typeerror_fallback(monkeypatch):
    """Test set_proxy with TypeError fallback for keyword-style call."""
    import juiced.lib.proxy as proxy

    class FakeSocksTypeError:
        def __init__(self):
            self.call_count = 0
            self.kwargs_call = None

        def set_default_proxy(self, *args, **kwargs):
            self.call_count += 1
            if self.call_count == 1:
                raise TypeError("positional not supported")
            # Second call should be keyword-style
            self.kwargs_call = kwargs

        def get_default_proxy(self):
            return (1, None, None, False, None, None)

    fake_socks = FakeSocksTypeError()
    monkeypatch.setattr(proxy, "socks", fake_socks)
    monkeypatch.setattr(proxy, "HAS_PYSOCKS", True)

    # Should try positional, catch TypeError, then retry with keywords
    proxy.set_proxy("1.1.1.1", 9999, modules=[])
    assert fake_socks.call_count == 2
    assert fake_socks.kwargs_call["addr"] == "1.1.1.1"


def test_set_proxy_rdns_edge_cases(monkeypatch):
    """Test set_proxy rdns flag determination edge cases."""
    import juiced.lib.proxy as proxy

    class FakeSocksNoSOCKS5:
        def __init__(self):
            self.rdns_value = None

        def set_default_proxy(self, proxy_type, addr, port, rdns):
            self.rdns_value = rdns

        def get_default_proxy(self):
            return (1, None, None, False, None, None)

    fake_socks = FakeSocksNoSOCKS5()
    monkeypatch.setattr(proxy, "socks", fake_socks)
    monkeypatch.setattr(proxy, "HAS_PYSOCKS", True)

    # Without SOCKS5 attribute, rdns should be False
    proxy.set_proxy("2.2.2.2", 1234, proxy_type=999, modules=[])
    assert fake_socks.rdns_value is False
