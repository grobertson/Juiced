import asyncio

import pytest

from juiced.lib.error import Kicked


def test_kicked_is_exception():
    """Ensure the Kicked exception exists and is an Exception subclass."""
    assert issubclass(Kicked, Exception)


def test_kicked_instantiation():
    # Kicked inherits from CytubeError; ensure it can be instantiated
    e = Kicked()
    assert isinstance(e, Kicked)


@pytest.mark.asyncio
async def test_async_noop():
    # Demonstrates async test structure for contributors
    await asyncio.sleep(0)
    assert True
