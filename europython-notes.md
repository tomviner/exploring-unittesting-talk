# py.test

##### Based on: *Improving automated testing with py.test* training by Holger Krekel and [Advanced py.test Fixtures](http://devork.be/talks/advanced-fixtures/advfix.html) by Floris Bruynooghe

xxxxxxxxx http://merlinux.eu/~hpk/ xxxxxxxxxxx

## Test finder

- by name
- subclass TestCase
- cross project??

- `-k` select tests by keyword
- `-s` disable capture of stdout/stderr
- `--pdb` start debugger on errors

set defaults in pytest.ini

## `assert`

pytest uses raw `assert` statements

Used to re-evaluate but doesn't now

Gives you extra information, eg

    assertTrue(x)

Type specialised reporting of errors, eg



## Marks and selective running

Used to:

- select tests at run time, using `py.test -m "keyword"` or `py.test -m "not slow"`

    `@pytest.mark.slow`

- conditional skipping eg depending which database is available

        pytest.skip('reason')
        pytest.mark.xfail('reason') # expected to fail, error if passes. Way to show known bugs, waiting for a fix.

        pytest.mark.skipif(sys.platform == 'win32', reason='POSIX only')

- `docutils = pytest.importorskip("docutils", minversion="0.3")`

## Fixtures

## Basic example

    @pytest.fixture
    def smtp():
        import smtplib
        return smtplib.SMTP("merlinux.eu")

- dependancy injection
- composable
- cachable
- can be a function or method
- benefits over `TestCase.setUp`
-- no need to use a class
-- run only when required - use `autouse=True` if you really want to always run
-- able to separate setUp tasks into multiple fixtures.
-- With TestCase you must group by common setUp, with pytest you can group by related tests
-- reusable beyond a single class, possibly even share between projects



# Cachable via `scope`

Allows caching of fixture over session/module/function (default)

    @pytest.fixture(scope='session')
    def db_conn():
        return create_db_conn()

# Combine fixtures, here with a tighter scope

    @pytest.fixture(scope='module')
    def db_table(request, db_conn):
        table = create_table(db_conn, 'foo')
        def fin():
            drop_table(db_conn, table)
        request.addfinalizer(fin)
        return table


## Finalizer

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

### Paramatisation of fixtures

re-run tests with different resources

    @pytest.fixture(params=[MySQL(), Postgres()])
    def db(request):
        return request.param

### Visibility

- per module
- per class
- in a `conftest.py` file
- `import`able - don't be confused here. the import adds visibility, although the db symbol isn't used

        from myapp.fixtures import db

        def test_data(db):
            assert db.get_data_found()


## Migrating to pytest

- compatible with UnitTest and nose
