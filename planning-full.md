## Random talk ideas

A tour of the features of pytest
Compare to unittest (and nose)
Gotchas (fixture args, )
de facto standard unit testing framework

- Introduction to pytest
- What's the point of pytest
- A deep dive into pytest
- PyUnit / nose / pytest: a comparison
- A history of unittesting in Python
- A survey of the unittesting landscape in Python
- Why you should switch from unittest to pytest
- Advancements in unit-testing in Python
- Techniques in unit-testing and how to use them in PyUnit, nose & pytest

- Exploring unit-testing with PyUnit (aka unittest), nose and pytest


Cover:


We'll start off by looking at what a unit-test framework does. We'll cover the basics, and find out what makes test code different to normal code.



We'll start by introducing our three test frameworks:
- unittest (sometimes called PYUnit) and it's xUnit origins
- nose: extends unittest to make testing easier
- pytest: more pythonic tests?

We'll look at several features of unit-testing and how they're covered by our three test frameworks. Covering:
- preparing the environment for a test
- happy path: asserting the expected truth
- provoking failure: ensuring exceptions raised

In the remaining time we'll move on to some more advanced techniques:
- paramatised test generators
- marking tests
- skipping and xfails
- next level: marking your params

---

Unit testing in Python has traditionally been based on the unittest module (formerly called PYUnit), we'll trace it's origins back to Kent Beck's JUnit and Smalltalk testing framework.

-- collect your tests
-- run your tests and collect the results
-- display failures etc
--- colour
--- pacman hack day project

---


This talk will look at number of different unit-testing techniques, explain why you might use them, and show you how they work in the top three Python unit-testing frameworks: the builtin unittest module, nose and pytest.

Some techniques we'll look at:
- the fixture process
- assertions
- test generators / paramatisation
- marking
-- marking of params
- skips
-- xfail


Unit testing in Python has traditionally been based on the unittest module (formerly called PYUnit), we'll trace it's origins back to Kent Beck's JUnit and Smalltalk testing framework.

We'll then look at nose and py.test.

---


This talk argues that pytest enables a more Pythonic style of testing. For example whereas Javans have no choice but to write classes as the smallest unit of code, Pythonistas have the ability to use functions. We cover pytest's fixture function system, and the ability to write tests themselves as functions.

Having left all the self.assertX methods behind, we see how pytest works, and infact does better, with plain assert statements.


Features:

- fixtures
-- basic example
-- builtin fixtures
-- scope
-- compare to setUp
-- finalisers (add, yield_fixture)
- paramatisation
- marking
-- marking of params
- skips
-- xfail
-- skiponfail etc
- compatible with UnitTest and nose
