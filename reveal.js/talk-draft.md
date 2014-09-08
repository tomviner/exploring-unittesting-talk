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

***

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

Features of unit-testing
========================
## and how they're covered by our frameworks

***
## a minimal test: with *class* or *function*?
***
## running your tests from the command line

    py.test


***
## setting up the environment for a test, and clearing up afterwards
***
## happy path: asserting the expected truth
***
## provoking failure: ensuring exceptions raised

---

Advanced techniques
===================
## not available in all 3 frameworks

***

## parameterised test generators
***
## skipping and xfails
***
## next level: marking your params
