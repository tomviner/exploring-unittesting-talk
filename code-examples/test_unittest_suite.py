import unittest

def add(a, b):
    return a + b


class TestKnownGood(unittest.TestCase):
    def __init__(self, input, output):
        super(TestKnownGood, self).__init__()
        self.input = input
        self.output = output

    def runTest(self):
        self.assertEqual(add(*self.input), self.output)

def suite():
    suite = unittest.TestSuite()
    known_values = [
        ((1, 2), (3)),
        ((2, 3), (5)),
    ]
    suite.addTests(TestKnownGood(input, output)
        for input, output in known_values)
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())