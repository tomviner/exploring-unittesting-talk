Copyright https://twitter.com/chrisdcunha

===============================
europython_testing
===============================

From Holger Krekel's pytest tutorial at EuroPython 2014.

NOTES
-----

- means to communicate between colleagues
- cross project works better
- test discovery is name based:
    - file starts with test_*
    - test_ function
    - unittest.TestCase class
- `-x` == fail fast
- assertTrue won't give you details about expression, assert will
- exact string diff location
- `pytest.mark.blabla` for `py.test -m "blabla"`
- `@xfail` if implementation is currently lacking (e.g. refactor)
    - use `@skipif` only for environment skipping
    - can decorate class
    - use xfail as a todo list and provide bug number in reason
- fixtures
    - suggested to not use setup teardown
    - dependency injection - construct your classes by passing in the dependencies
    - `@pytest.fixture`
        - if you skip the fixture, then all the related test are automatically skipped
    - `py.test --fixture test_functionality.py`
    - scope and duration:

```bash
$ py.test tests/test_fixture_cache_scope.py --duration=10
==================================================================== test session starts =====================================================================
platform darwin -- Python 2.7.2 -- py-1.4.22 -- pytest-2.6.0
collected 2 items

tests/test_fixture_cache_scope.py ..

================================================================= slowest 10 test durations ==================================================================
1.00s setup    tests/test_fixture_cache_scope.py::test_func
1.00s setup    tests/test_fixture_cache_scope.py::test_func2
0.00s call     tests/test_fixture_cache_scope.py::test_func
0.00s call     tests/test_fixture_cache_scope.py::test_func2
0.00s teardown tests/test_fixture_cache_scope.py::test_func2
0.00s teardown tests/test_fixture_cache_scope.py::test_func
```

- fixtures + parametrization
    - "request" object (this is the caller)
        - request.addfinalizer()
    - parametrizing fixtures (pass in MySql once, Postgres second)
        - tests are called twice
    - parametrize tests to test with multiple inputs
        - you can use fixtures in fixtures
    - fixtures can be in class
    - automatic finding of fixtures in conftest.py
        - probably best to just import the fixtures you want
    - tmpdir fixture is a commonly used
        - pytest keeps the last four runs
    - `autouse=True` so that all tests in the specified scope will depend on that fixture
    - parser.addption in conftest.py allows you to expose command line options to the fixtures
    - use markers to talk to fixtures from functions or modules

```python
@pytest.fixture
def driver():
    opts = request.get_marker('driver_opts') or 'a'
    return opts

@pytest.mark.driver_opts('b')
def test_different_opts(driver):
    pass
```

- HPK Opinion: Not a good idea to want to support all three libs (unittest, nose, pytest)
    - we can only use the minimal shared feature set
