## Exploring unit-testing
## with unittest, nose and pytest

A PyConUK talk by [Tom Viner](http://tomviner.co.uk) /
[@tomviner](http://twitter.com/tomviner)

---

## Coming up:

- Our three test frameworks
- Some features of unit-testing
    - running your tests
    - a minimal test
    - setting up the environment for a test
    - happy path
    - provoking failure
- Advanced techniques
    - parameterised test generators
    - skipping and xfails
    - next level: marking your params

---

Our three test frameworks
=========================


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

### nose

    import nose

    def test_add():
        nose.tools.assert_equal(add(1, 1), 2)

### pytest

    def test_add():
        assert add(1, 1) == 2



## running your tests from the command line

### unittest

    $ python -m unittest test_unittest_examples.TestAdd

### nose

    $ nosetests test_unittest_examples:TestAdd
    $ nosetests test_nose_examples.py

### pytest

    $ py.test test_unittest_examples.py::TestAdd
    $ py.test test_nose_examples.py
    $ py.test test_pytest_examples.py

Note the default is to find `by/file/path` not `dotted.module.path`, so your shell tab complete works


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


## happy path: asserting the expected truth
unittest

    self.assertThisThatEtc(result, expect)

nose

    nose.tools.assert_this_that_etc(result, expect)

pytest

    assert result == expect
    assert result != expect


### pytest naked assert

    def test_add():
        a = 1
        b = 2
        expected = 4
        assert add(a, b) + add(b, b) == expected

Test resultw

        def test_add():
            a = 1
            b = 2
            expected = 4
    >       assert add(a, b) + add(b, b) == expected
    E       assert (3 + 4) == 4
    E        +  where 3 = add(1, 2)
    E        +  and   4 = add(2, 2)

    test_pytest_examples.py:12: AssertionError



## provoking failure: ensuring exceptions raised

unittest

    class TestAdd(unittest.TestCase):
        def test_validation(self):
            self.assertRaises(TypeError, add, ('a', 1))

nose

    def test_validation():
        nose.tools.assert_raises(TypeError, add, ('a', 1))

    @nose.tools.raises(TypeError)
    def test_validation():
        pass

pytest

    def test_validation():
        with pytest.raises(TypeError):
            add('a', 1)

---

Advanced techniques
===================
## not available in all 3 frameworks


## parameterised test generators


### unittest

    [insert ammusing example of people trying this with unittest]


### nose

    import purl
    from nose.tools import eq_

    level1_vars = {
        'var': 'value',
        'hello': 'Hello World!',
    }

    # Tuples of (template, bindings, expected URI)
    test_data = [
        ('{var}', level1_vars, 'value'),
        ('{hello}', level1_vars, 'Hello%20World%21'),
    ]

    def assert_expansion(template, fields, expected):
        eq_(purl.expand(template, fields), expected)

    def test_expansion():
        for template, fields, expected in test_data:
            yield assert_expansion, template, fields, expected

example from http://codeinthehole.com/writing/purl-uri-templates-and-generated-tests/


### pytest

    import pytest

    @pytest.mark.parametrize(("template", "fields", "expected"), data)
    def test_expand(template, fields, expected):
        assert expand(template, fields) ==  expected


### Paramatisation of fixtures

re-run tests with different resources

    @pytest.fixture(params=[MySQL(), Postgres()])
    def db(request):
        return request.param


## skipping and xfails
unittest

    class MyTestCase(unittest.TestCase):

        @unittest.skip("demonstrating skipping")
        def test_nothing(self):
            self.fail("shouldn't happen")

nose

    from nose.tools import nottest

    @nottest
    def test_my_sample_test()
        #code here ...

pytest

    db_params = (
        MySQL(),
        pytest.mark.xfail(Postgres(), reason="psql not supported yet")
    )
    @pytest.fixture(params=db_parms)
    def db(request):
        return request.param


## testing the code in this talk

- live demo!


More for another talk
=====================
- Marking your params
- Django Integration
- Integration with `python setup.py test`