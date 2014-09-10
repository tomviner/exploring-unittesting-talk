import unittest


def add(a, b):
    return a + b


class TestAdd(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(1, 1), 2)

    def test_validation(self):
        self.assertRaises(TypeError, add, ('a', 1))

