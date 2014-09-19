# unittest v pytest: FIGHT!

### version one of this talk put 7 people in a coma
### I'm aiming for 5 or less this time

A PyConUK talk by [Tom Viner](http://tomviner.co.uk) /
[@tomviner](http://twitter.com/tomviner)

---

<!-- --- data-background="red" -->

# in the red corner we have: `UNITTEST`

- this heavyweight fighter has been around for over 15 years!
- was welcomed into the family, of the standard library, since Python 2.1
- this is a fighter with heritage
    - unittest's nickname gives it away: PyUnit
    - we're talking xUnit lineage
    - I'm talking jUnit, sUnit aaaaaaallllllll the way back to **Kent Beck**

---

<!-- --- data-background="blue" -->

# in the blue corner we have our challenger: PYTEST

- this new kid on the block is here to make changes
- trainer by Holger Krekel
- `pytest` grew up, and broke away from the original `py` family
    - only the sentimental still call it py **dot** test

---

<!-- --- data-background="black" -->

# THERE HAS BEEN A DISQUALIFICATION!

- Years ago, another fighter was born into this battle
- They call this one **nosetests**, and it came of an early pytest
- The result is that they cover slightly different spaces now...
- and so I have to announce that **nose** has been disqualified from this talk
    - Althought it's sometimes hard to stop these libraries making another appearance

---

# 3 rounds!

- ## arrange
- ## act
- ## assert

- 3 **a**'s
- 3 segments of testing
- seconds out, ding diiiing!

---

# round 1: arrange

- getting things ready to act
- (and clearing the mess up afterward)

- prepare data
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

- standard unittest
- state is stored on self
- rerun for every test method


<!-- --- data-background="#adf" -->

### Arrange using @fixture function

    # Arrange
    @pytest.fixture
    def db_table():
        return make_db_table()

    def test_table(db_table):
        # Act
        success = db_table.ACT()

        # Assert
        assert success

- no setUp, no self, no class
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

- only make the db connection once
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

- chainable
- cachble via `scope` argument
- run once per:
    - function (default)
    - cls
    - module
    - session

---

### what about if we could made a todo list of the clean ups required as we went along?


<!-- --- data-background="#fad" -->

### shed a tearDown

    class TestMyDataRow(unittest.TestCase):

        def setUp(self):
            self.db_table = make_db_table()
            self.addCleanup(self.db_table.drop)

- add multiple cleanups as you go
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

- like unittest's addCleanup
- what about more complicated cleaning up?
- neat alternative - like context manager
    - no tearDown and no addCleanup/addfinalizer

---

# round 1 over!
### how did you score the two fighters on Arrange?

- Advanced py.test Fixtures (Floris Bruynooghe) in CC1.4
---

<!-- --- data-background="css/swiss.png" -->

# round 2: act

- time for a swiss intervention
- as a half swiss, not everything has to be violent you know
- round 2 **act** is neutral to which framework
- so relax
- call your live code
- some code you want to test (we call this the *System Under Test* btw)

---

<!-- --- data-background="css/lion.jpg" -->

# round 3: assert

- out neutral zone now
- straight into round 3!


# round 3: assert

- verify what happened
- was exactly the right data returned?
- did the correct **side-effect** occur?

---

<!-- --- data-background="css/unittest-asserts-tall.png" -->

# unittest loves its assertMethods!


# unittest loves its assertMethods!


nose makes an appearence!
unittest + nose = better together