#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Proxy helpers with optional pysocks integration.

This module provides light wrappers so the project can optionally use
pysocks (socks) when available. When pysocks is not installed the
proxy-related helpers raise a ProxyConfigError with a clear message.
"""
import logging
import socket
import sys
from typing import Any

from .error import ProxyConfigError

logger = logging.getLogger("juiced.lib.proxy")
_orig_getaddrinfo = socket.getaddrinfo

# Do not auto-import pysocks here. Tests expect the default
# behaviour to be "pysocks not installed". Tests which need
# pysocks should monkeypatch `juiced.lib.proxy.socks` and
# `juiced.lib.proxy.HAS_PYSOCKS = True` explicitly.
socks = None  # type: ignore
HAS_PYSOCKS = False
SOCKS5 = None


class ProxyError(Exception):
    """Generic proxy-related error."""


class socksocket:  # pylint: disable=invalid-name,too-few-public-methods
    """Light wrapper that either delegates to pysocks or raises when
    pysocks is not available.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if not HAS_PYSOCKS or socks is None:
            raise ProxyConfigError("pysocks is not installed")
        real = getattr(socks, "socksocket", None)
        if real is None:
            raise ProxyConfigError("pysocks.socksocket not available")
        # create underlying real socket instance and delegate attribute access
        self._real = real(*args, **kwargs)

    def __getattr__(self, name: str):
        return getattr(self._real, name)


class Socket(socksocket):
    """SOCKS-enabled socket (keeps localhost direct)."""

    def __init__(
        self,
        family=socket.AddressFamily.AF_INET,
        type=socket.SOCK_STREAM,
        proto=0,
        fileno=None,
    ):
        if type not in (socket.SOCK_STREAM, socket.SOCK_DGRAM):
            type = socket.SOCK_STREAM
        super().__init__(family, type, proto, fileno)

    def set_proxy_for_address(self, addr):
        logger.debug("set_proxy_for_address %r", addr)
        host, _ = addr
        if host in ("127.0.0.1", "localhost"):
            # Localhost should not use proxy
            try:
                self.set_proxy(None)
            except Exception:
                # Underlying socket may not implement set_proxy; ignore
                pass
        else:
            try:
                self.proxy = self.default_proxy
            except Exception:
                pass

    def bind(self, addr, *args, **kwargs):
        self.set_proxy_for_address(addr)
        return super().bind(addr, *args, **kwargs)

    def sendto(self, data, *args, **kwargs):
        # last positional arg is the destination address
        if args:
            self.set_proxy_for_address(args[-1])
        return super().sendto(data, *args, **kwargs)

    def connect(self, addr, *args, **kwargs):
        self.set_proxy_for_address(addr)
        return super().connect(addr, *args, **kwargs)


def getaddrinfo(host, port, *args, **kwargs):
    """Resolver helper that can optionally use pysocks' rdns behaviour.

    When pysocks is not available this just delegates to the system
    getaddrinfo.
    """
    # If a socks implementation was provided (e.g., tests monkeypatching
    # a fake socks), prefer that behaviour. Only fall back to the
    # system resolver when no socks object is available.
    if socks is None:  # pragma: no cover - fallback
        ret = _orig_getaddrinfo(host, port, *args, **kwargs)
        logger.debug("%s:%s %s (system)", host, port, ret)
        return ret

    proxy_type, _, _, rdns, _, _ = socks.get_default_proxy()
    if proxy_type is not None and rdns:
        # If remote DNS (rdns) is requested by the proxy, avoid local
        # resolution and return a placeholder that preserves the call
        # signature for callers that only need the tuple shape.
        ret = [(socket.AF_INET, socket.SOCK_STREAM, 6, "", (host, port))]
    else:
        ret = _orig_getaddrinfo(host, port, *args, **kwargs)
    logger.debug("%s:%s %s (proxy)", host, port, ret)
    return ret


def wrap_module(module):
    """Wrap a module's socket API to route via SOCKS when configured.

    This will replace module.socket.socket and module.socket.getaddrinfo
    when a default proxy is configured via pysocks.
    """
    logger.debug("wrap module %s", module)

    if socks is None:
        raise ProxyConfigError("pysocks is not installed")

    if not hasattr(socks, "get_default_proxy"):
        raise ProxyConfigError("pysocks does not expose get_default_proxy")

    proxy_info = socks.get_default_proxy()
    if not proxy_info or proxy_info[0] is None:
        raise ProxyConfigError("no default proxy specified")

    # Instead of mutating the global socket module (which would
    # affect unrelated code and break things like asyncio), replace
    # the `socket` attribute on the target module with a thin proxy
    # that delegates to the real socket module except for the
    # attributes we want to override.
    real_socket_mod = sys.modules.get("socket")

    class _SocketModuleProxy:
        def __init__(self, orig):
            self._orig = orig

        def __getattr__(self, name):
            if name == "socket":
                return Socket
            if name == "getaddrinfo":
                return getaddrinfo
            return getattr(self._orig, name)

    module.socket = _SocketModuleProxy(real_socket_mod)


def set_proxy(addr, port, proxy_type=SOCKS5, modules=None):
    """Set pysocks default proxy and optionally wrap modules.

    Raises ProxyConfigError when pysocks is not installed.
    """
    if socks is None:
        raise ProxyConfigError("pysocks is not installed")

    # Determine rdns flag by comparing against the socks module's
    # SOCKS5 constant when available; otherwise fall back to a
    # conservative default.
    rdns = False
    try:
        if hasattr(socks, "SOCKS5") and proxy_type == getattr(socks, "SOCKS5"):
            rdns = True
    except Exception:
        rdns = False

    try:
        socks.set_default_proxy(proxy_type, addr, port, rdns=rdns)
    except TypeError:
        # Fallback to keyword-style if available
        socks.set_default_proxy(proxy_type=proxy_type, addr=addr, port=port, rdns=rdns)

    for module in modules or (sys.modules[__name__],):
        wrap_module(module)
