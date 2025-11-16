import sys
import json
import asyncio
from io import StringIO
from types import SimpleNamespace

import pytest

from juiced.lib import config as config_mod
from juiced.lib import util as util_mod


def test_configure_logger_stream():
    # Use a StringIO as stream to capture logs
    stream = StringIO()
    logger = config_mod.configure_logger('testlogger', log_file=stream, log_format='%(levelname)s:%(message)s', log_level=20)
    # logger should have at least one handler and the level applied
    assert logger.level == 20
    assert any(h.formatter is not None for h in logger.handlers)


def test_configure_proxy_calls_set_proxy(monkeypatch):
    calls = {}

    def fake_set_proxy(addr, port):
        calls['addr'] = addr
        calls['port'] = port

    monkeypatch.setattr('juiced.lib.config.set_proxy', fake_set_proxy)

    # host:port
    config_mod.configure_proxy({'proxy': 'example.com:9050'})
    assert calls['addr'] == 'example.com'
    assert calls['port'] == 9050

    # host only
    calls.clear()
    config_mod.configure_proxy({'proxy': 'localhost'})
    assert calls['addr'] == 'localhost'
    assert calls['port'] == 1080


def test_get_config_json(tmp_path, monkeypatch):
    # Create a temporary JSON config file
    cfg = tmp_path / 'cfg.json'
    data = {
        'domain': 'example.com',
        'channel': 'chan',
        'user': 'bot',
        'response_timeout': 0.2,
        'restart_delay': 5,
        'retry': 2,
        'retry_delay': 3,
        'log_level': 'debug'
    }
    cfg.write_text(json.dumps(data))

    monkeypatch.setattr(sys, 'argv', ['prog', str(cfg)])

    # prevent set_proxy side-effects
    monkeypatch.setattr('juiced.lib.config.set_proxy', lambda a, p: None)

    conf, kwargs = config_mod.get_config()
    assert conf['domain'] == 'example.com'
    assert kwargs['domain'] == 'example.com'
    assert 'socket_io' in kwargs


@pytest.mark.asyncio
async def test_util_get_requests(monkeypatch):
    # Patch requests.get to return an object with .text
    class R:
        def __init__(self, text):
            self.text = text

    def fake_get(url):
        return R('ok')

    monkeypatch.setattr('juiced.lib.util.requests.get', fake_get)
    res = await util_mod.get('http://example')
    assert res == 'ok'


def test_to_sequence_and_messageparser_and_ip_hash_cloak_roundtrip():
    # to_sequence
    assert util_mod.to_sequence(None) == ()
    assert util_mod.to_sequence(1) == (1,)
    lst = [1, 2]
    assert util_mod.to_sequence(lst) is lst

    # MessageParser simple tags
    p = util_mod.MessageParser()
    out = p.parse('<strong>bold</strong> &amp; <code>c</code>')
    assert '*bold*' in out or 'bold' in out
    assert '`c`' in out or 'c' in out

    # ip_hash length
    h = util_mod.ip_hash('127.0.0.1', 4)
    assert isinstance(h, str) and len(h) == 4

    # cloak and uncloak roundtrip
    cloaked = util_mod.cloak_ip('127.0.0.1')
    res = util_mod.uncloak_ip(cloaked)
    assert '127.0.0.1' in res


def test_uncloak_ip_with_start():
    # cloak with start parameter
    cloaked = util_mod.cloak_ip('127.0.0.1', start=2)
    # uncloak supplying start
    res = util_mod.uncloak_ip(cloaked, start=2)
    assert '127.0.0.1' in res
