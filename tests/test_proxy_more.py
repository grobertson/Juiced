import socket
import types


def test_wrap_module_and_set_proxy_monkeypatched(monkeypatch):
    import juiced.lib.proxy as proxy

    # Create a dummy module to be wrapped
    dummy_socket_mod = types.SimpleNamespace()
    # provide a socket submodule object with attributes to be replaced
    dummy_socket_mod.socket = types.SimpleNamespace(socket=lambda *a, **k: None, getaddrinfo=lambda *a, **k: None)
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
    monkeypatch.setattr(proxy, 'HAS_PYSOCKS', True)
    monkeypatch.setattr(proxy, 'socks', fake_socks, raising=False)
    # Make socksocket report a default proxy exists so wrap_module branches
    monkeypatch.setattr(proxy.socksocket, 'default_proxy', True, raising=False)

    # Call wrap_module - should set module.socket.socket to proxy.Socket
    proxy.wrap_module(dummy_module)
    assert hasattr(dummy_module.socket, 'socket')
    assert dummy_module.socket.socket is proxy.Socket
    assert dummy_module.socket.getaddrinfo is proxy.getaddrinfo

    # Now test set_proxy will call socks.set_default_proxy and wrap modules
    # Reset to a fresh dummy module
    dummy_socket_mod2 = types.SimpleNamespace()
    dummy_socket_mod2.socket = lambda *a, **k: None
    dummy_socket_mod2.getaddrinfo = lambda *a, **k: None
    dummy_module2 = types.SimpleNamespace(socket=dummy_socket_mod2)

    # Call set_proxy with explicit proxy_type equal to fake_socks.SOCKS5 to set rdns True
    proxy.set_proxy('1.2.3.4', 1080, proxy_type=fake_socks.SOCKS5, modules=[dummy_module2])

    # Verify fake_socks recorded the call
    assert fake_socks.called is not None
    assert fake_socks.called['addr'] == '1.2.3.4'
    assert fake_socks.called['port'] == 1080
    assert fake_socks.called['proxy_type'] == fake_socks.SOCKS5
    assert fake_socks.called['rdns'] is True


def test_getaddrinfo_uses_proxy_rdns(monkeypatch):
    import juiced.lib.proxy as proxy

    class FakeSocks2:
        def get_default_proxy(self):
            # proxy_type not None and rdns True
            return (1, None, None, True, None, None)

    fake_socks2 = FakeSocks2()
    monkeypatch.setattr(proxy, 'socks', fake_socks2, raising=False)
    # Call getaddrinfo - should return a custom tuple list when rdns True
    result = proxy.getaddrinfo('example.com', 80)
    assert isinstance(result, list)
    assert result[0][0] == socket.AF_INET
    assert result[0][-1] == ('example.com', 80)
