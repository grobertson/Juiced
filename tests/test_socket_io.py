import asyncio
import json

import pytest

from juiced.lib.error import ConnectionClosed, ConnectionFailed, PingTimeout
from juiced.lib.socket_io import SocketIO, SocketIOResponse


class FakeWebSocket:
    def __init__(self, recv_messages=None):
        self.sent = []
        self._recv_q = asyncio.Queue()
        self.closed = False
        if recv_messages:
            for m in recv_messages:
                self._recv_q.put_nowait(m)

    async def send(self, data):
        self.sent.append(data)

    async def recv(self):
        return await self._recv_q.get()

    async def close(self):
        self.closed = True


@pytest.mark.asyncio
async def test_socketio_response_match_event():
    m = SocketIOResponse.match_event(r"^ev$", {"k": 1})
    assert m("ev", {"k": 1})
    assert not m("no", {"k": 1})


@pytest.mark.asyncio
async def test_get_config_success_and_invalid():
    async def fake_get(url):
        return ")]}\n" + json.dumps(
            {"sid": "S", "pingInterval": 1000, "pingTimeout": 1000}
        )

    cfg = await SocketIO._get_config("http://x", fake_get)
    assert cfg["sid"] == "S"

    async def fake_get_bad(url):
        return "nojson"

    with pytest.raises(Exception):
        await SocketIO._get_config("http://x", fake_get_bad)


@pytest.mark.asyncio
async def test_connect_probe_mismatch_and_success(monkeypatch):
    async def fake_get(url):
        return json.dumps({"sid": "SID", "pingInterval": 1000, "pingTimeout": 1000})

    # probe mismatch -> websocket closed and exception
    class BadWS(FakeWebSocket):
        def __init__(self):
            super().__init__(recv_messages=["bad"])

    async def bad_connect(url):
        return BadWS()

    loop = asyncio.get_running_loop()
    with pytest.raises(Exception):
        await SocketIO._connect("http://x", 0, loop, fake_get, bad_connect)

    # successful connect: websocket returns '3probe'
    class GoodWS(FakeWebSocket):
        def __init__(self):
            super().__init__(recv_messages=["3probe"])

    async def good_connect(url):
        return GoodWS()

    sio = await SocketIO._connect("http://x", 0, loop, fake_get, good_connect)
    assert isinstance(sio, SocketIO)
    # cleanup - close may cancel background tasks; ignore CancelledError here
    try:
        await sio.close()
    except asyncio.CancelledError:
        pass


@pytest.mark.asyncio
async def test_emit_with_response_and_recv_event():
    loop = asyncio.get_running_loop()
    # make websocket that doesn't produce pings
    ws = FakeWebSocket()
    config = {"pingInterval": 100000, "pingTimeout": 100000}
    sio = SocketIO(ws, config, qsize=0, loop=loop)

    async def responder():
        # wait until response object is appended
        while not sio.response:
            await asyncio.sleep(0)
        # set response result
        sio.response[0].set(("myevt", {"ok": True}))

    task = loop.create_task(responder())
    res = await sio.emit(
        "evt", {"a": 1}, match_response=lambda e, d: True, response_timeout=1.0
    )
    assert res == ("myevt", {"ok": True})
    task.cancel()
    await sio.close()


@pytest.mark.asyncio
async def test_close_and_recv_behavior():
    loop = asyncio.get_running_loop()
    ws = FakeWebSocket(recv_messages=['42["ev",{"x":1}]'])
    config = {"pingInterval": 100000, "pingTimeout": 100000}
    sio = SocketIO(ws, config, qsize=1, loop=loop)

    # let recv process one message
    await asyncio.sleep(0.05)
    ev = await sio.recv()
    assert ev[0] == "ev"

    # set error and ensure recv raises
    sio.error = ConnectionClosed()
    with pytest.raises(ConnectionClosed):
        await sio.recv()

    # closing should complete and set websocket.closed
    await sio.close()
    assert ws.closed is True
