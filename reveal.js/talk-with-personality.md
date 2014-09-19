## Exploring unit-testing
## with unittest, nose and pytest

A PyConUK talk by [Tom Viner](http://tomviner.co.uk) /
[@tomviner](http://twitter.com/tomviner)

---

# unittest v pytest: FIGHT!

A PyConUK talk by [Tom Viner](http://tomviner.co.uk) /
[@tomviner](http://twitter.com/tomviner)

---

<!-- --- data-background="red" -->

# in the red corner we have: `UNITTEST`

Note: - this heavyweight fighter has been around for over 15 years!
- was welcomed into the family, of the standard library, since Python 2.1
- this is a fighter with heritage
    - unittest's nickname gives it away: PyUnit
    - we're talking xUnit lineage
    - I'm talking jUnit, sUnit aaaaaaallllllll the way back to **Kent Beck**

---

<!-- --- data-background="blue" -->

# in the blue corner we have our challenger: PYTEST

Note: - this new kid on the block is here to make changes
- trainer by Holger Krekel
- `pytest` grew up, and broke away from the original `py` family
    - only the sentimental still call it py **dot** test

---

<!-- --- data-background="black" -->

# THERE HAS BEEN A DISQUALIFICATION!

Note: - Years ago, another fighter was born into this battle
- They call this one **nosetests**, and it came of an early pytest
- The result is that they cover slightly different spaces now...
- and so I have to announce that **nose** has been disqualified from this talk
    - Althought it's sometimes hard to stop these libraries making another appearance

---

# 3 rounds!

- ## arrange
- ## act
- ## assert

Note: - 3 **a**'s
- 3 segments of testing
- seconds out, ding diiiing!

---

# round 1: arrange

- getting things ready to act
- (and clearing the mess up afterward)

Note: - prepare data
- initalise objects
- gentle mocking

---

<!-- --- data-background="#fad" -->

### per test Arrange using setUp method

    class TestMyDataTable(unittest.TestCase):

        # Arrange
        def setUp(self):
            self.db_table = make_db_table()

        def test_table(self):
            # Act
            success = self.db_table.ACT()

            # Assert
            self.assertTrue(success)

        # I always end up doing your tidying up! >:-/
        def tearDown(self):
            self.db_table.drop()

Note: - standard unittest
- state is stored on self
- rerun for every test method


<!-- --- data-background="#adf" -->

### Arrange using @fixture functions

    # Arrange
    @pytest.fixture
    def db_table():
        return make_db_table()

    def test_table(db_table):
        # Act
        success = db_table.ACT()

        # Assert
        assert success

Note: - no setUp, no self, no class
- (Django: no fixture file!)
- variables are returned
- test **function argument** connects
    - dependancy injection

---

<!-- --- data-background="#fad" -->

### per *class* Arrange using setUpClass

    class TestMyDataTable(unittest.TestCase):
        @classmethod
        def setUpClass(cls):
            cls.conn = get_db_connection()

        def setUp(self):
            self.db_table = self.conn.make_db_table()

        def test_one(self):
            ...

        def tearDown(self):
            self.db_table.drop()

        @classmethod
        def tearDownClass(cls):
            cls.conn.disconnect()

So how would this run, with 3 test methods?
<!-- -- class="fragment" -->

    setUpClass
        setUp
            test_one
        tearDown
        setUp
            test_two
        tearDown
        setUp
            test_three
        tearDown
    tearDownClass
<!-- -- class="fragment" -->

Note: - only make the db connection once
- keep test isolation


<!-- --- data-background="#adf" -->

### cache @fixture functions using scope

(ignoring clean up)

    @pytest.fixture(scope='session')
    def db_conn():
        return create_db_conn()

    @pytest.fixture
    def db_table(db_conn):
        return db_conn.make_db_table()

    def test_one(db_table):
        ...

Note: - chainable
- cachble via `scope` argument
- run once per:
    - function (default)
    - cls
    - module
    - session

---

### what about making a todo list of clean ups as we went along?


<!-- --- data-background="#fad" -->

### don't shed a tearDown

    class TestMyDataRow(unittest.TestCase):

        def setUp(self):
            self.db_table = make_db_table()
            self.addCleanup(self.db_table.drop)

Note: - add multiple cleanups as you go
    - great for modular cleanup
- no tearDown required


<!-- --- data-background="#adf" -->

## pytest fixture finalizers

    @pytest.fixture
    def db_table(request):
        db_table = make_db_table()
        request.addfinalizer(db_table.drop) # can't pass args
        return db_table

neat alternative: the yield_fixture
<!-- -- class="fragment" data-fragment-index="2" -->

    @pytest.yield_fixture
    def db_table():
        db_table = make_db_table()
        yield db_table
        # do finalising here:
        db_table.drop(fast=True)
<!-- -- class="fragment" data-fragment-index="2" -->

Note: - like unittest's addCleanup
- what about more complicated cleaning up?
- neat alternative - like context manager
    - no tearDown and no addCleanup/addfinalizer


### fixture have loads more features:
### Paramatisation of fixtures

re-run tests with different resources

    from databases import MySQL, Postgres
    @pytest.fixture(params=[MySQL(), Postgres()])
    def db(request):
        return request.param

---

# round 1 over!
### how did you score the two fighters on Arrange?

- unittest: setUp
- pytest: fixtures
-- Advanced py.test Fixtures (Floris Bruynooghe) in CC1.4

---

<!-- --- data-background="css/swiss.png" -->

# round 2: act

Note: - time for a swiss intervention
- as a half swiss, not everything has to be about battling, violence you know
- round 2 **act** is neutral to which framework
- so relax
- call your live code,
- some code you want to test (we call this the *System Under Test* btw)
- that's all I can say about **act**

---

<!-- --- data-background="css/lion.jpg" -->

# round 3: assert

- out neutral zone now
- straight into round 3!


# round 3: assert

Note: - verify what happened
- was exactly the right data returned?
- did the correct **side-effect** occur?

---

# assert: part i
## happy path: asserting the expected truth


# unittest assertMethods

### unittest.assertIreallyLoveMyAssertMethods!


<!-- --- data-background="css/unittest-asserts-tall.png" -->


<!-- --- data-background="#fad" -->

core of basic asserts

    self.assertTrue(x)
    self.assertEqual(x, y)
    self.assertIsNotNone(result)
    self.assertGreaterEqual(four, five)

per type - no need to remember <!-- -- class="fragment" data-fragment-index="2" -->

    self.assertMultiLineEqual(s1, s2)
    self.assertListEqual(l1, l2)
    ...

    # make more with addTypeEqualityFunc(type, function

<!-- -- class="fragment" data-fragment-index="2" -->

handy <!-- -- class="fragment" data-fragment-index="3" -->

    self.assertAlmostEqual(a, b)
    self.assertRegexpMatches(text, regexp)
    self.assertDictContainsSubset(subset, full)

<!-- -- class="fragment" data-fragment-index="3" -->


<!-- --- data-background="#adf" -->

## pytest naked assert

    assert result == expected
    assert result2 != expected
    assert x is not None
    assert y >= z
    assert dict1 == dict2

Note:
- much simpler, no self.assertX methods to remember
- have to implement things like assertAlmostEqual yourself
    - or use a plugin like (pytest-raisesregexp)[https://github.com/Walkman/pytest-raisesregexp]


## nose makes an entry

    nose.tools.assert_yay_no_camel_case
    nose.tools.assert_almost_equal(x, y)

Note: - pulled out of unittest
- better together


<!-- --- data-background="#adf" -->

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

# assert: part ii
## provoking failure:
### ensuring exceptions raised

Note: often we expect our code to raise exception in certain cases


unittest

    class TestAdd(unittest.TestCase):
        def test_validation(self):
            with self.assertRaises(TypeError) as e:
                add('a', 1)

            self.assertRaisesRegexp(FooBarError, msg_re)

pytest

    def test_validation():
        with pytest.raises(TypeError):
            add('a', 1)
