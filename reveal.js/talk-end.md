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

    # xxx


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