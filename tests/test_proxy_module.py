import pytest


def test_socksocket_instantiation_raises():
    import juiced.lib.proxy as proxy
    from juiced.lib.error import ProxyConfigError

    with pytest.raises(ProxyConfigError):
        proxy.socksocket()


def test_set_proxy_raises_when_missing_pysocks():
    import juiced.lib.proxy as proxy
    from juiced.lib.error import ProxyConfigError

    with pytest.raises(ProxyConfigError):
        proxy.set_proxy('127.0.0.1', 1080)


def test_wrap_module_raises_when_missing_pysocks():
    import juiced.lib.proxy as proxy
    from juiced.lib.error import ProxyConfigError

    class DummyModule:
        pass

    with pytest.raises(ProxyConfigError):
        proxy.wrap_module(DummyModule)
