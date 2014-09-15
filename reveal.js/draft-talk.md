## Exploring unit-testing
## with unittest, nose and pytest

A PyConUK talk by [Tom Viner](http://tomviner.co.uk) /
[@tomviner](http://twitter.com/tomviner)

---

## Coming up:

- Our three test frameworks
- Some features of unit-testing
- Advanced techniques
- Conclusions

---

Our three test frameworks
=========================


# unittest

- sometimes called PyUnit
    - standard library since Python 2.1 (2001)
- `xUnit` / Kent Beck *(creator of XP, one of the fathers of Test-Driven-Design) origins:*

    *"Kent wants people to control their own environment, so he liked to have each team build the framework themselves (it only took a couple of hours), that way they would feel happy to change it to suit their particular circumstances"
    http://www.martinfowler.com/bliki/Xunit.html*
- updated (codename *unittest2*) in python 2.7/3.2 with extra features


# py.test

- Originally the unittesting part of Holger Krekel's `py` development support library
- pytest: more pythonic tests?


# nose

- *extends `unittest` to make testing easier*
- about the name:
    - **Nose Obviates Suite Employment**
- there is a `nose2` but I'm not covering it here
    -- get's 90x fewer downloads
- nose was originally created as a clone of pytest

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

### nose

    from nose.tools import eq_

    def test_add():
        eq_(add(1, 1), 2)

### pytest

    # no need to: import pytest

    def test_add():
        assert add(1, 1) == 2

---

## running your tests from the command line

### unittest
Note the new discover command

    $ python -m unittest test_unittest_examples.TestAdd
    $ python -m unittest discover -s tests/

### nose

    $ nosetests test_unittest_examples:TestAdd
    $ nosetests test_nose_examples.py

### pytest

    $ py.test test_unittest_examples.py::TestAdd
    $ py.test test_nose_examples.py
    $ py.test test_pytest_examples.py

- Note it's worth learning the options of whatever tool you use
- Note notice all 3 frameworks can run `unittest.Testcase`s
    and additionally pytest can run most `nose` tests

---

# testing in 3 steps

- ## arrange
- ## act
- ## assert


# arrange
## setting up the environment for a test, and clearing up afterwards


### unittest

Setup per test:

    class TestSequenceFunctions(unittest.TestCase):

        def setUp(self):
            self.db_table = make_db_table()

        def tearDown(self):
            self.db_table.drop()

Setup per test class:

    class Test(unittest.TestCase):
        @classmethod
        def setUpClass(cls):
            cls._connection = createExpensiveConnectionObject()

        @classmethod
        def tearDownClass(cls):
            cls._connection.destroy()

Setup per module:

    # unittesting
    def setUpModule():
        createConnection()

    def tearDownModule():
        closeConnection()


Unittest2 (i.e. unittest in Python>=2.7) adds:

    class TestSequenceFunctions(unittest.TestCase):

        def setUp(self):
            self.db_table = make_db_table()
            self.addCleanup(self.db_table.drop)


nose

    from nose.tools import with_setup

    def setup_func():
        "set up test fixtures"

    def teardown_func():
        "tear down test fixtures"

    @with_setup(setup_func, teardown_func)
    def test():
        "test ..."


pytest

    @pytest.fixture
    def smtp():
        import smtplib
        return smtplib.SMTP("merlinux.eu")

    def my_test(smtp):
        assert smtp.connected

- dependancy injection
- can be a function or method
- chainable
- cachable


## pytest fixtures

- cachable via `scope` over session/module/function (default)
- chainable

Fixture runs once per test run:

    @pytest.fixture(scope='session')
    def db_conn():
        return create_db_conn()

Combine fixtures, here with a tighter scope

    @pytest.fixture(scope='function')
    def db_table(db_conn):
        return create_table(db_conn, 'foo')

Then just name the 2nd fixture as a *funcarg*:

    def test_table(db_table):
        assert db_table.num_rows >= 10


## pytest fixtures

- benefits over `unittest.TestCase.setUp`
    - no need to use a class
    - run only when required - use `autouse=True` if you really want to always run
    - able to separate setUp tasks into multiple fixtures.
    - with TestCase you must group by common setUp, with pytest you can group by related tests
    - reusable beyond a single class, possibly even share between projects


## pytest fixture finalizers

    @pytest.fixture(scope="module")
    def smtp(request):
        smtp = smtplib.SMTP("merlinux.eu")
        def fin():
            print ("teardown smtp")
            smtp.close()
        request.addfinalizer(fin)
        return smtp  # provide the fixture value

Alternate syntax to use a yield fixture

    @pytest.yield_fixture(scope="module")
    def smtp(): # no request required
        smtp = smtplib.SMTP("merlinux.eu")

        # provide the fixture value
        yield smtp
        # now test is run

        # after the yield, is the finalizer code
        print ("teardown smtp")
        smtp.close()

---

## happy path: asserting the expected truth
unittest

    # unittest
    self.assertTrue
    self.assertEqual
    self.assertIsNotNone
    self.assertGreaterEqual

    self.assertAlmostEqual
    self.assertItemsEqual
    # self.assertRegexpMatches(text, regexp)
    # self.assertDictContainsSubset(subset, full)

    # make more with addTypeEqualityFunc(type, function)

nose

Note secret: you can use them with other frameworks!

    nose.tools.assert_greater_equal(result, expected)

    nose.tools.ok_
    nose.tools.eq_


pytest

    def add(a, b):
        return a + b

    assert result == expected
    assert result2 != expected
    a, b = 3, -1
    assert add(a, b) + add(b, b) == expected

- much simpler, no self.assertX methods to remember
- have to implement things like assertAlmostEqual yourself
    -- or use a plugin like (pytest-raisesregexp)[https://github.com/Walkman/pytest-raisesregexp]


### pytest naked assert

    def test_add():
        a = 1
        b = 2
        expected = 4
        assert add(a, b) + add(b, b) == expected

Test result

        def test_add():
            a = 1
            b = 2
            expected = 4
    >       assert add(a, b) + add(b, b) == expected
    E       assert (3 + 4) == 4
    E        +  where 3 = add(1, 2)
    E        +  and   4 = add(2, 2)

    test_pytest_examples.py:12: AssertionError

---

## provoking failure: ensuring exceptions raised

all 3 frameworks provide context managers

unittest

    class TestAdd(unittest.TestCase):
        def test_validation(self):
            with self.assertRaises(TypeError) as e:
                add('a', 1)

    # self.assertRaisesRegexp(FooBarError, msg_re)

nose

    def test_validation_with():
        with nose.tools.assert_raises(TypeError):
            add('a', 1)

pytest

    def test_validation():
        with pytest.raises(TypeError):
            add('a', 1)


No need to use the other versions:

unittest

    class TestAdd(unittest.TestCase):
        def test_validation(self):
            self.assertRaises(TypeError, add, ('a', 1))

nose

    @nose.tools.raises(TypeError)
    def test_validation_decorator():
        add('a', 1)

    def test_validation():
        nose.tools.assert_raises(TypeError, add, ('a', 1))

<!--
test message with a regex

    msg_re = "^You shouldn't Foo a Bar$"
    with self.assertRaisesRegexp(FooBarError, msg_re) as e:
        foo_the_bar()
 -->
---

Advanced techniques
===================


## parameterised test generators


### unittest

    # insert ammusing example of people trying this with unittest


### nose

    def test_evens():
        for i in range(0, 5):
            yield check_even, i, i*3

    def check_even(n, nn):
        assert n % 2 == 0 or nn % 2 == 0


### pytest

    @pytest.mark.parametrize("n", range(0, 5))
    def test_evens():
        nn = n * 3
        assert n % 2 == 0 or nn % 2 == 0

---

### Paramatisation of fixtures

re-run tests with different resources

    from databases import MySQL, Postgres
    @pytest.fixture(params=[MySQL(), Postgres()])
    def db(request):
        return request.param


## skipping tests

### Why we might want to skip certain tests?


unittest

    class MyTestCase(unittest.TestCase):

        @unittest.skip("demonstrating skipping")
        def test_nothing(self):
            self.fail("shouldn't happen")

nose

    from nose.tools import nottest

    @nottest
    def test_my_sample_test():
        pass

pytests

    import sys
    @pytest.mark.skipif(sys.version_info < (3,3),
                        reason="requires python3.3")
    def test_function():
        pass


## expected failures

### Why we might want to xfail certain tests?


unittest

    class MyTestCase(unittest.TestCase):

        @unittest.skip("demonstrating skipping")
        def test_nothing(self):
            self.fail("shouldn't happen")

nose

    from nose.tools import nottest

    @nottest
    def test_my_sample_test():
        pass

pytest

    xxx


## using skips and xfail on paramaters

pytest only

    from databases import MySQL, Postgres
    db_params = (
        MySQL(),
        pytest.mark.xfail(Postgres(), reason="psql not supported yet")
    )
    @pytest.fixture(params=db_params)
    def db(request):
        return request.param

---

# Conclusions

---

I've been [@tomviner](twitter.com/tomviner)*, any:
# Questions?

\* link to slides has been tweeted