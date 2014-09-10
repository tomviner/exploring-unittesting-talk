import pytest


def add(a, b):
    return a + b


def test_add():
    a = 1
    b = 2
    expected = 7
    assert add(a, b) + add(b, b) == expected


def test_validation():
    with pytest.raises(TypeError):
        add('a', 1)
