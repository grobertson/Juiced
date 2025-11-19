import asyncio
import json

import pytest
import websockets.exceptions

from juiced.lib.error import ConnectionClosed, PingTimeout, SocketIOError
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
async def test_socketio_response_match_event_non_dict_data():
    """Test match_event raises NotImplementedError for non-dict data when called."""
    matcher = SocketIOResponse.match_event(r"ev", data="string")
    with pytest.raises(NotImplementedError, match="!isinstance"):
        matcher("ev", {})


@pytest.mark.asyncio
async def test_socketio_response_equality():
    """Test SocketIOResponse equality checks."""
    r1 = SocketIOResponse(lambda e, d: True)
    r2 = SocketIOResponse(lambda e, d: True)
    # Should compare by id
    assert r1 == r1
    assert r1 == r1.id
    assert not (r1 == r2)


@pytest.mark.asyncio
async def test_socketio_response_str_repr():
    """Test SocketIOResponse string representation."""
    r = SocketIOResponse(lambda e, d: True)
    assert f"#{ r.id}" in str(r)
    assert f"#{r.id}" in repr(r)


@pytest.mark.asyncio
async def test_socketio_response_cancel_methods():
    """Test SocketIOResponse set and cancel methods."""
    r = SocketIOResponse(lambda e, d: True)
    r.set("result")
    assert r.future.result() == "result"

    r2 = SocketIOResponse(lambda e, d: True)
    r2.cancel()
    assert r2.future.cancelled()

    r3 = SocketIOResponse(lambda e, d: True)
    ex = ValueError("error")
    r3.cancel(ex)
    with pytest.raises(ValueError):
        r3.future.result()


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


@pytest.mark.asyncio
async def test_error_property_setter():
    """Test error property setter behavior."""
    loop = asyncio.get_running_loop()
    ws = FakeWebSocket()
    config = {"pingInterval": 100000, "pingTimeout": 100000}
    sio = SocketIO(ws, config, qsize=0, loop=loop)

    ex = ValueError("test error")
    sio.error = ex
    assert sio.error == ex
    assert sio.close_task is not None

    # Setting error again should be ignored
    sio.error = ValueError("second error")
    assert sio.error == ex  # Still the first error

    await sio.close()


@pytest.mark.asyncio
async def test_close_idempotency():
    """Test that close() is idempotent and handles multiple calls."""
    loop = asyncio.get_running_loop()
    ws = FakeWebSocket()
    config = {"pingInterval": 100000, "pingTimeout": 100000}
    sio = SocketIO(ws, config, qsize=0, loop=loop)

    # First close
    try:
        await sio.close()
    except asyncio.CancelledError:
        pass
    assert sio.closed.is_set()

    # Second close should return immediately
    try:
        await sio.close()
    except asyncio.CancelledError:
        pass
    assert sio.closed.is_set()


@pytest.mark.asyncio
async def test_emit_when_error_set():
    """Test emit raises error when connection has error."""
    loop = asyncio.get_running_loop()
    ws = FakeWebSocket()
    config = {"pingInterval": 100000, "pingTimeout": 100000}
    sio = SocketIO(ws, config, qsize=0, loop=loop)

    sio._error = ConnectionClosed()
    with pytest.raises(ConnectionClosed):
        await sio.emit("test", {})

    try:
        await sio.close()
    except asyncio.CancelledError:
        pass


@pytest.mark.asyncio
async def test_emit_response_timeout():
    """Test emit with response timeout."""
    loop = asyncio.get_running_loop()
    ws = FakeWebSocket()
    config = {"pingInterval": 100000, "pingTimeout": 100000}
    sio = SocketIO(ws, config, qsize=0, loop=loop)

    # Emit with short timeout, no response
    res = await sio.emit(
        "evt", {}, match_response=lambda e, d: True, response_timeout=0.01
    )
    assert res is None  # Timeout should return None

    await sio.close()


@pytest.mark.asyncio
async def test_emit_response_cancelled():
    """Test emit when response future is cancelled."""
    loop = asyncio.get_running_loop()
    ws = FakeWebSocket()
    config = {"pingInterval": 100000, "pingTimeout": 100000}
    sio = SocketIO(ws, config, qsize=0, loop=loop)

    async def canceller():
        while not sio.response:
            await asyncio.sleep(0)
        # Cancel the response future
        sio.response[0].future.cancel()

    task = loop.create_task(canceller())
    with pytest.raises(asyncio.CancelledError):
        await sio.emit("evt", {}, match_response=lambda e, d: True, response_timeout=1)

    task.cancel()
    await sio.close()


@pytest.mark.asyncio
async def test_emit_non_socketio_exception():
    """Test emit wraps non-SocketIOError exceptions."""
    loop = asyncio.get_running_loop()

    class FailingWebSocket(FakeWebSocket):
        async def send(self, data):
            raise ValueError("send failed")

    ws = FailingWebSocket()
    config = {"pingInterval": 100000, "pingTimeout": 100000}
    sio = SocketIO(ws, config, qsize=0, loop=loop)

    with pytest.raises(SocketIOError):
        await sio.emit("evt", {})

    try:
        await sio.close()
    except asyncio.CancelledError:
        pass


@pytest.mark.asyncio
async def test_recv_task_various_message_types():
    """Test _recv task handles various socket.io message types."""
    loop = asyncio.get_running_loop()
    messages = [
        "2",  # Ping (should send pong)
        "3extra",  # Pong (should set ping_response)
        "40",  # Event with no name or data
        "41disconnect",  # Event with name only, no data
        '42["ev1"]',  # Event with name only (array length 1)
        '42["ev2",{"k":"v"}]',  # Event with name and data
        '42["ev3",1,2,3]',  # Event with name and multiple data items
        "invalid",  # Unknown message type
    ]
    ws = FakeWebSocket(recv_messages=messages)
    config = {"pingInterval": 100000, "pingTimeout": 100000}
    sio = SocketIO(ws, config, qsize=10, loop=loop)

    # Wait for messages to be processed
    await asyncio.sleep(0.1)

    # Check pong was sent for ping
    assert "3" in ws.sent

    # Check events were queued
    ev1 = await sio.recv()
    assert ev1[0] == ""  # Empty event from "40"

    ev2 = await sio.recv()
    assert ev2[0] == "disconnect"  # From "41disconnect"

    ev3 = await sio.recv()
    assert ev3[0] == "ev1"

    ev4 = await sio.recv()
    assert ev4 == ("ev2", {"k": "v"})

    ev5 = await sio.recv()
    assert ev5 == ("ev3", [1, 2, 3])

    await sio.close()


@pytest.mark.asyncio
async def test_recv_task_invalid_json():
    """Test _recv task handles invalid JSON in events."""
    loop = asyncio.get_running_loop()
    messages = ['42notjson']
    ws = FakeWebSocket(recv_messages=messages)
    config = {"pingInterval": 100000, "pingTimeout": 100000}
    sio = SocketIO(ws, config, qsize=10, loop=loop)

    await asyncio.sleep(0.05)
    # Should log error but not crash
    await sio.close()


@pytest.mark.asyncio
async def test_recv_task_connection_errors():
    """Test _recv task handles various connection errors."""
    loop = asyncio.get_running_loop()

    class ErrorWebSocket(FakeWebSocket):
        def __init__(self):
            super().__init__()
            self.recv_count = 0

        async def recv(self):
            self.recv_count += 1
            if self.recv_count == 1:
                raise websockets.exceptions.ConnectionClosed(None, None)
            await asyncio.sleep(10)  # Never return

    ws = ErrorWebSocket()
    config = {"pingInterval": 100000, "pingTimeout": 100000}
    sio = SocketIO(ws, config, qsize=0, loop=loop)

    await asyncio.sleep(0.05)
    assert isinstance(sio.error, ConnectionClosed)

    await sio.close()


@pytest.mark.asyncio
async def test_recv_task_response_matching():
    """Test _recv task matches responses correctly."""
    loop = asyncio.get_running_loop()
    messages = ['42["event",{"id":1}]']
    ws = FakeWebSocket(recv_messages=messages)
    config = {"pingInterval": 100000, "pingTimeout": 100000}
    sio = SocketIO(ws, config, qsize=10, loop=loop)

    # Add a response matcher
    response = SocketIOResponse(lambda e, d: e == "event" and d.get("id") == 1)
    sio.response.append(response)

    # Wait for message processing
    await asyncio.sleep(0.05)

    # Response should be set
    result = await response.future
    assert result == ("event", {"id": 1})

    await sio.close()


@pytest.mark.asyncio
async def test_connect_with_retry():
    """Test connect with retry logic."""

    async def fake_get(url):
        return json.dumps({"sid": "S", "pingInterval": 1000, "pingTimeout": 1000})

    attempt = {"count": 0}

    async def failing_connect(url):
        attempt["count"] += 1
        if attempt["count"] < 2:
            raise ConnectionError("fail")
        ws = FakeWebSocket(recv_messages=["3probe"])
        return ws

    loop = asyncio.get_running_loop()
    sio = await SocketIO.connect(
        "http://test", retry=2, retry_delay=0.01, loop=loop, get=fake_get, connect=failing_connect
    )
    assert attempt["count"] == 2
    try:
        await sio.close()
    except asyncio.CancelledError:
        pass


@pytest.mark.asyncio
async def test_connect_cancelled():
    """Test connect handles cancellation."""

    async def fake_get(url):
        raise asyncio.CancelledError()

    with pytest.raises(asyncio.CancelledError):
        await SocketIO.connect("http://test", get=fake_get)


@pytest.mark.asyncio
async def test_close_with_close_task_is_current():
    """Test close when close_task is the current task."""
    loop = asyncio.get_running_loop()
    ws = FakeWebSocket()
    config = {"pingInterval": 100000, "pingTimeout": 100000}
    sio = SocketIO(ws, config, qsize=0, loop=loop)

    # Manually trigger close which sets close_task
    try:
        await sio.close()
    except asyncio.CancelledError:
        pass
    assert sio.closed.is_set()
