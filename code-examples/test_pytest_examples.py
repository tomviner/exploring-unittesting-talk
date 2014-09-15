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

import tempfile

@pytest.yield_fixture
def open_file():
    with tempfile.TemporaryFile(mode='w') as f:
        yield f
    assert f.closed

def test_file(open_file):
    open_file.write('test')
    assert not open_file.closed
