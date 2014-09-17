import pytest


def add(a, b):
    return a + b


def test_add():
    1/0
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


@pytest.mark.parametrize("n", range(0, 5))
def test_evens(n):
    nn = n * 3
    assert n % 2 == 0 or nn % 2 == 0
