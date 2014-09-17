## Exploring unit-testing
## with unittest, nose and pytest

A PyConUK talk by [Tom Viner](http://tomviner.co.uk) /
[@tomviner](http://twitter.com/tomviner)

---

## Coming up:

- Our three test frameworks
- Some features of unit-testing
- Advanced techniques
- Conclusions
- Questions

---

Our three test frameworks
=========================


# unittest

- sometimes called PyUnit
    - standard library since Python 2.1 (2001)
- updated (codename *unittest2*) in python 2.7/3.2 with extra features
- `xUnit` / Kent Beck *(creator of XP, one of the fathers of Test-Driven-Design) origins:*

Note: "Kent wants people to control their own environment, so he liked to have each team build the framework themselves (it only took a couple of hours), that way they would feel happy to change it to suit their particular circumstances"
    http://www.martinfowler.com/bliki/Xunit.html


# py.test

- Originally the unittesting part of Holger Krekel's `py` development support library
- pytest: more pythonic tests?


# nose

- *extends `unittest` to make testing easier*
- about the name:
    - **Nose Obviates Suite Employment**
- there is a `nose2` but I'm not covering it here
    - (it's much less widely used)
- nose was originally created as a clone of pytest 0.8
