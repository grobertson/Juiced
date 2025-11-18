"""
Test template for contributors.

Guidance:
- Name tests `test_*.py` and functions `test_*`.
- Use simple arrange/act/assert sections.
- For async code, use `pytest.mark.asyncio` or `pytest-asyncio` fixtures.
"""


def test_arithmetic_happy_path():
    # Arrange
    a = 2
    b = 3

    # Act
    res = a + b

    # Assert
    assert res == 5
