
    a

# we

    import unittestz

    class TestAdd(unittest.TestCase):
        def test_add(self):
            self.assertEqual(add(1, 1), 2)

# unittest

- sometimes called PyUnit
    - standard library since Python 2.1
- `xUnit`/Kent Beck (creator of XP, one of the fathers of Test-Driven-Design) origins:

    "Kent wants people to control their own environment, so he liked to have each team build the framework themselves (it only took a couple of hours), that way they would feel happy to change it to suit their particular circumstances"
    http://www.martinfowler.com/bliki/Xunit.html


# py.test

- Originally the unittesting part of Holger Krekel's `py` development support library
- pytest: more pythonic tests?


# nose

- *extends `unittest` to make testing easier*
- About the name:
    - nose is the least silly short synonym for discover in the dictionary.com thesaurus that does not contain the word ‘spy.’
    - Pythons have noses
    - The nose knows where to find your tests
    - **Nose Obviates Suite Employment**
---

Features of unit-testing
========================
## and how they're covered by our frameworks


## a minimal test: with *class* or *function*?

How should we test this silly example?

    def add(a, b):
        return a + b


### unittest

    import unittest

    class TestAdd(unittest.TestCase):
        def test_add(self):
            self.assertEqual(add(1, 1), 2)

### more