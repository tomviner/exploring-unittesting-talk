Advanced techniques
===================


## parameterised test generators


### unittest

    # Adapted from http://stackoverflow.com/a/3772008/15890
    class TestKnownGood(unittest.TestCase):
        def __init__(self, input, output):
            super(TestKnownGood, self).__init__()
            self.input = input
            self.output = output

        def runTest(self):
            self.assertEqual(add(*self.input), self.output)

Then

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


### nose

    def test_evens():
        for i in range(0, 5):
            yield check_even, i, i*3

    def check_even(n, nn):
        assert n % 2 == 0 or nn % 2 == 0


### pytest

    @pytest.mark.parametrize("n", range(0, 5))
    def test_evens(n):
        nn = n * 3
        assert n % 2 == 0 or nn % 2 == 0


### Paramatisation of fixtures

re-run tests with different resources

    from databases import MySQL, Postgres
    @pytest.fixture(params=[MySQL(), Postgres()])
    def db(request):
        return request.param

---

## skipping tests

### Why we might want to skip certain tests?

Note: - TDD and our test too far ahead
- Or certain lib versions we don't support:


unittest

    class MyTestCase(unittest.TestCase):

        @unittest.skip("demonstrating skipping")
        @unittest.skipIf(mylib.__version__ < (1, 3),
                             "not supported in this library version")
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

Note: -mark known issues


unittest

    class MyTestCase(unittest.TestCase):

        @unittest.expectedFailure
        def test_nothing(self):
            # bug test

pytest

    @pytest.mark.xfail(reason="Issue #123")
    def test_function():
        # bug test


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

### unittest

- current *standard* - consistent testing style
- really handy special assert methods
    - assertAlmostEqual
    - assertDictContainsSubset

Note: -


### nose

- if you're happy writing test classes, great test runner
- some cool tools built in, like @timed decorator
- liberates unittest's assert methods, for everyone to use
- rich ecosystem of plugins


### pytest

- group methods purely by the feature they test
- modular fixture system
- more pythonic?
- rich ecosystem of plugins
    - xdist - parallelise your test runs
    - pytest-django - run Django DB tests without Django's `TestCase`

---

I've been [@tomviner](twitter.com/tomviner), any
# Questions?

\* link to slides (made with reveal.js btw) has been tweeted
