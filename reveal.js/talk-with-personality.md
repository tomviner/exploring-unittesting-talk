# unittest v pytest: FIGHT!

### version one of this talk put 7 people in a coma
### I'm aiming for 5 or less this time

A PyConUK talk by [Tom Viner](http://tomviner.co.uk) /
[@tomviner](http://twitter.com/tomviner)

---

# in the red corner we have: `UNITTEST`

- this heavyweight fighter has been around for over 15 years!
- was welcomed into the family, of the standard library, since Python 2.1
- this is a fighter with heritage
    - unittest's nickname gives it away: PyUnit
    - we're talking xUnit lineage
    - I'm talking jUnit, sUnit aaaaaaallllllll the way back to **Kent Beck**

---

# in the blue corner we have our challenger: PYTEST

- this new kid on the block is here to make changes
- `pytest` grew up, and broke away from the original `py` family
    - only the sentiental

---

# THERE HAS BEEN A DISQUALIFICATION!

- Years ago, another fighter was born into this battle
- They call it nose, and he came of an early pytest
- Not many people know that, but today they cover slightly different spaces
- And so I have to announce that nose has been disqualified from this talk
    - Althought it's sometimes hard to stop these libraries making another appearance

---

# 3 rounds

- ## arrange
- ## act
- ## assert

- they are the 3 activities of unittesting
- seconds out, ding diiiing!

---

# round 1: arrange

- setting up the environment
- clearing up afterward

Note: Code that's necessary but not part of the test
- share common setup code

