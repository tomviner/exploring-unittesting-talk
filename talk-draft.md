    ## Exploring unit-testing
## with unittest, nose and pytest

A PyConUK talk by [Tom Viner](http://tomviner.co.uk) /
[@tomviner](http://twitter.com/tomviner)

---

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

# unittest <!-- .element: class="unittest" -->

- sometimes called PyUnit
- `xUnit` origins

***

# nose <!-- .element: class="nose" -->

- nose: "extends unittest to make testing easier"

***

# pytest <!-- .element: class="pytest" -->

- pytest: more pythonic tests?

---

We'll look at several features of unit-testing and how they're covered by our frameworks

***
## running your tests from the command line

    py.test


***
## a minimal test: with class or function?
***
## setting up the environment for a test, and clearing up afterwards
***
## happy path: asserting the expected truth
***
## provoking failure: ensuring exceptions raised

---

In the remaining time we'll move on to some more advanced techniques:
***
## parameterised test generators
***
## skipping and xfails
***
## next level: marking your params
