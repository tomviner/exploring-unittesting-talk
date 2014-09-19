Impl of nose test/setup function, using unit test?

Slide note server

Clear message of talk
Setup v fixture

assertThis v assert

Why: skip, xfail

django plugin?

unittest + nose = a great combination


### unittest

- current *standard* - consistent testing style
- really handy special assert methods
    - assertAlmostEqual
    - assertDictContainsSubset
- no magic going on

Note: -


### nose

- liberates unittest's assert methods, for everyone to use


### pytest

- modular fixture system
    - group tests purely by the feature they test
- can run unittests
- more pythonic? you decide
