---
layout: post
title: "Database clamps: Deterministic performance tests for database-dependent code"
tags: [Django, Software]
x_audience: |
    Django users who write automated tests;
    secondarily, users of other backend web frameworks 
        (like Rails) who write automated tests
x_performance: |
    18 pageviews on day 1 of publish and post to r/django
    53 pageviews on week 1 of publish, with daily numbers of:
        18, 3, 0, 0, 22, 6, 4; 4, 1, 5
         ↑ r/django
                      ↑ referred from home page of DaFoster on a Sat

---

If you've got a moderate-sized [Django] web application then you're probably already writing automated tests to make sure none of its pages break unexpectedly when you're making changes to them. That is, you're testing page *functionality*.

However another way that pages can break is that they take too long to display, or otherwise don't have enough *performance*. The very first Django application I deployed to customers got crushed with only *12* concurrent users! How embarassing! 🤭 I hadn't even bothered to do basic performance testing before that initial deployment because I didn't think it was *possible* for such a small number of expected users to bring down my site. I now know better and require that any new web page have **automated performance tests** before being deployed to customers.

There are many kinds of performance tests, but right now I'd like to focus on automated *database* performance tests, or what I like to call **database clamps**: 

[Django]: https://www.djangoproject.com/

### What are they?

A database clamp measures the number of database queries issued when a web page is being rendered server-side. For example:

```
from django.test import TestCase

class TodoListPageTests(TestCase):
    ...
    
    def test_todo_list_mdp(self):  # mdp = maintains database performance
        self.client.login(username='user', password='password')
        with self.assertNumQueries(3):  # <-- DATABASE CLAMP
            response = self.client.get(reverse('todo:list'))
            self.assertEqual(200, response.status_code)
```

Here, [assertNumQueries] is used to clamp the number of database queries issued when the `todo:list` page is rendered server-side. If any changes are made to the the page that increases (or otherwise changes) the number of database queries issued, then the test will detect the change and fail.

[assertNumQueries]: https://docs.djangoproject.com/en/3.1/topics/testing/tools/#django.test.TransactionTestCase.assertNumQueries

### Why are they useful?

Database clamps are particularly useful for web applications because **server-side rendering time is typically dominated by database query time**. If you get your database access patterns under control then it's likely the remaining server-side rendering time will be negligible.

Also, unlike most [other kinds of performance tests], database clamps are fully *deterministic* and always give consistent results no matter how fast the machine the test is being run on. Very useful!

[other kinds of performance tests]: /articles/2018/06/02/performance-testing/

### Conclusion

Avoid the embarassment of your site falling over when only a handful of customers try to use it. Use database clamps!

### Appendix: Better database clamps

A database clamp which uses Django's [assertNumQueries] function will fail not just when the number of database queries *increases* (which is usually a problem) but will also fail when the number of queries *decreases* (which is usually okay, and even desirable).

In my own Django web application I use a custom version of `assertNumQueries` that still fails if the number of queries *increases* but only issues a warning (via `warnings.warn(...)`) if the number of queries *decreases*:

```
$ python3 manage.py test gradebook
System check identified no issues (0 silenced).
.
----------------------------------------------------------------------
Ran 1 test in 0.758s

OK

Warnings:
gradebook/tests/test_gradebook.py:425: UserWarning: 14 database queries executed, no more than 15 expected. Consider reducing the expected query count to match.
```

In addition, my version of `assertNumQueries` expects to be called from an automated test method whose name contains the word `mdp` ("maintains database performance") and warns if it is being called from a test lacking that acronym. This restriction allows my engineering team to easily search for and run exactly those tests which use database clamps when making large scale changes that may break many database clamps at once:

```
$ python3 manage.py test $(python3 manage.py list_tests mdp -s)
System check identified no issues (0 silenced).
..............s..s..................................................
----------------------------------------------------------------------
Ran X tests in Ys

OK (skipped=Z)
```

### *Related Articles*

* [Performance Testing](/articles/2018/06/02/performance-testing/) - Details a few of the big guns of performance testing.
* [Tests as Policy Automation](/articles/2021/02/02/tests-as-policy-automation/) - Has more ideas for creatively using automated tests to enforce additional (non-functional) properties in your backend web application.
