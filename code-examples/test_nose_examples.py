import nose


def add(a, b):
    return a + b


def test_add():
    nose.tools.assert_equal(add(1, 1), 2)

def test_validation():
    nose.tools.assert_raises(TypeError, add, ('a', 1))
