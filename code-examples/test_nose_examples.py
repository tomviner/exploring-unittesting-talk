import nose


def add(a, b):
    return a + b


def test_add():
    nose.tools.assert_equal(add(1, 1), 2)

def test_validation():
    nose.tools.assert_raises(TypeError, add, ('a', 1))

def test_validation_with():
    with nose.tools.assert_raises(TypeError) as e:
        add('a', 1)

@nose.tools.raises(TypeError)
def test_validation_decorator():
    add('a', 1)
