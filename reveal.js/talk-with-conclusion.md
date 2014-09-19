# review

- arrange, act, assert
- setUp v @fixture
- please try the swiss cheese
- assertThis v assert

- monolithic class
    - with TestCase you must group your tests by common setUp
- with pytest you can group by related tests
    - reusable beyond a single class, possibly even share between projects


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

---

# Thank You

---

I've been [@tomviner](twitter.com/tomviner)*, any
# Questions?

\* link to slides (made with reveal.js btw) has been tweeted

<hr>
<small>
Did I mention we're hiring? See [HogarthWW.com](www.hogarthww.com/jobs/)

we're a big Python shop, who do things like write webapps, have hackdays and host the London dojo
</small>
