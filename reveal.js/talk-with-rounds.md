Features of unit-testing
========================
## and how they're covered by our frameworks


## a minimal test: with *class* or *function*?

How should we test this silly example?

    def add(a, b):
        return a + b


### unittest

    def add(a, b):
        return a + b

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

    $ python -m unittest test_unittest_examples.TestAdd
    $ python -m unittest discover -s tests/

### nose

    $ nosetests test_unittest_examples:TestAdd
    $ nosetests test_nose_examples.py

### pytest

    $ py.test test_unittest_examples.py::TestAdd
    $ py.test test_nose_examples.py
    $ py.test test_pytest_examples.py

Note: the new discover command
- it's worth learning the options of whatever tool you use
- notice all 3 frameworks can run `unittest.Testcase`s
    and additionally pytest can run most `nose` tests

---

# testing in 3 steps

- ## arrange
- ## act
- ## assert

---

# arrange
## setting up the environment for a test (and clearing up afterwards)

Note: Code that's necessary but not part of the test
- share common setup code


### unittest

Setup per test:

    class TestMyDataRow(unittest.TestCase):

        def setUp(self):
            self.db_table = make_db_table()

        def tearDown(self):
            self.db_table.drop()

- rerun for every test method
- state is stored on self

Note:
- only get one `setUp` per class. How would we share
 some setup code between classes?


Setup per test class:

    class TestMyDataRow(unittest.TestCase):
        @classmethod
        def setUpClass(cls):
            cls._connection = create_expensive_connection_object()

        @classmethod
        def tearDownClass(cls):
            cls._connection.destroy()

can do per module with `setUpModule` / `tearDownModule`

Note: beware breaking test isolation


recent version of unittest adds:

    class TestMyDataRow(unittest.TestCase):

        def setUp(self):
            self.db_table = make_db_table()
            self.addCleanup(self.db_table.drop)

            # addCleanup with args:
            self.addCleanup(self.db_table.drop, fast=True)

Note: add multiple cleanups as you go
- pass in args to applied to the function
- no tearDown required


nose

    from nose.tools import with_setup

    class TestStuff:

        def setup_func(self):
            self.db_table = make_db_table()

        def teardown_func(self):
            self.db_table.drop()

        @with_setup(self, setup_func, teardown_func)
        def test_table():
            "test ..."
            # um, I don't have access to db_table

Note: it really looks like you could return it and add an arg to the test
- so only use functions for very simple testing. pytest... fully functional test functions


pytest

    @pytest.fixture
    def db_table():
        return make_db_table()

    def test_table(db_table, another_fixture,):
        db_table.do_sql_to_the_things()

Note:
    - no setUp, no self, variables are returned
    - dependancy injection by **function argument**
    - can be a function or method
    - by default still run for every test, but also cachable...
    - more pythonic?


## pytest fixture finalizers

    @pytest.fixture
    def db_table(request):
        db_table = make_db_table()
        request.addfinalizer(db_table.drop) # can't pass args
        return db_table

Note: - like unittests addCleanup
- what about more complicated cleaning up?


## pytest fixture finalizers

    @pytest.fixture
    def db_table(request):
        db_table = make_db_table()
        def clean_db_up():
            db_table.drop(fast=True)
        request.addfinalizer(clean_db_up)
        return db_table

Alternate syntax to use a yield fixture

    @pytest.yield_fixture
    def db_table():
        db_table = make_db_table()
        yield db_table
        db_table.drop(fast=True)

Note: this is like creating a context manager aka an object you use **with**


## more about pytest fixtures

- singular purpose
    - use as many as you need
- cachable
- chainable


### cachable

    @pytest.fixture(scope='session')
    def db_conn():
        return create_db_conn()

- via `scope` argument
- run once per:
    - function (default)
    - cls
    - module
    - session

Note: - this fixture runs once per test session
    - these are like the setUp level with unittest


### chainable

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
    - run only when required
    - `autouse=True` if you really want to always run
    - able to separate setUp tasks into multiple fixtures.
    - with TestCase you must group by common setUp, with pytest you can group by related tests
    - reusable beyond a single class, possibly even share between projects


## An example about testing a spellchecker

---

## happy path: asserting the expected truth
unittest

    self.assertTrue
    self.assertEqual
    self.assertIsNotNone
    self.assertGreaterEqual

    # handy
    self.assertAlmostEqual
    self.assertItemsEqual
    self.assertRegexpMatches(text, regexp)
    self.assertDictContainsSubset(subset, full)

    # per type
    self.assertMultiLineEqual
    self.assertListEqual

    # make more with addTypeEqualityFunc(type, function)


nose

    nose.tools.ok_
    nose.tools.eq_

    nose.tools.assert_greater_equal(result, expected)

Note: Secret: you can use them with other frameworks!


pytest

    def add(a, b):
        return a + b

    assert result == expected
    assert result2 != expected
    a, b = 3, -1
    assert add(a, b) + add(b, b) == expected

Note:
- much simpler, no self.assertX methods to remember
- have to implement things like assertAlmostEqual yourself
    - or use nose.tools.assert_yay_no_camel_case
    - or use a plugin like (pytest-raisesregexp)[https://github.com/Walkman/pytest-raisesregexp]


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

## provoking failure:
### ensuring exceptions raised

Note: often we expect our code to raise exception in certain cases


unittest

    class TestAdd(unittest.TestCase):
        def test_validation(self):
            with self.assertRaises(TypeError) as e:
                add('a', 1)

            self.assertRaisesRegexp(FooBarError, msg_re)

nose

    def test_validation_with():
        with nose.tools.assert_raises(TypeError):
            add('a', 1)

pytest

    def test_validation():
        with pytest.raises(TypeError):
            add('a', 1)

Note: all 3 frameworks provide context managers


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
