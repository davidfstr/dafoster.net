---
layout: post
title: 'Abandonment vs. Unchecked Exceptions for Error Handling'
tags: [Software]
x_started_on: 2016-05-10

---

Read a very interesting article about [error handling in Midori] recently, and it got me thinking about errors again. I've thought about errors a lot in the past, as you can see in my old [Error Handling] article from 2013.

[error handling in Midori]: http://joeduffyblog.com/2016/02/07/the-error-model/
[Error Handling]: /articles/2013/07/13/error-handling/

Midori mentions a few mechanisms for handling errors:

* **error codes**,
* **unchecked exceptions**, 
* **checked exceptions**, and
* **abandonment**.

Midori has chosen to run with

1. *abandonment* for bugs, and
2. *checked exceptions* for most regular errors,
3. *error codes* for other regular errors.

These seem to be reasonable choices given the special constraints of a language intended for systems, namely:

* **correctness** is more important than convenience,
* **constant-time performance**[^perf1] is important,

However I work mostly in application domains rather than system domains, so I wouldn't make these same choices. In particular *abandonment* really gets under my skin.

### Abandonment

Abandonment in Midori is used for bugs and serious errors where there is no expectation that the error condition can be handled sensibly. Abandonment tears down the entire process.

I have a few problems with this approach:

1. **Abandonment assumes that the *process* is the primary isolation boundary.**

   In a web server, for example, a single *request* being handled would be a more appropriate boundary. It would be better to abort only the current request rather than bring down the entire web server.

2. **Abandonment provides no opportunity for its error condition to be handled in an alternative fashion.**

   For example, code that intentionally allocates large blocks of memory on a regular basis may in fact be prepared to handle out of memory conditions, which would normally trigger abandonment.

   Granted, you can often support this scenario by bifurcating the API, providing one allocate-memory function that returns an explicit error code on failure and a different allocate-memory function that abandons on failure.

But there is one big advantage to using abandonment:

* **Better constant-time performance.**

  Using abandonment in place of unchecked exceptions means that there is no need to pepper functions everywhere with the low-level code needed to propagate unchecked exceptions. Such code globally degrades constant-time performance of all functions in the language.

### Unchecked Exceptions

In most modern programming languages intended for applications (as opposed to systems), *unchecked exceptions* are used for reporting bugs. They have the following advantages:

* **Unchecked exceptions fail fast, terminating the process by default.**

  This is no different than abandonment so far, however...

* **Unchecked exceptions *can* be caught by a higher level error handler**.

  This additional flexibily is useful for web servers, parsers, and other applications that expect to encounter errors but don't want to crash entirely in the presence of errors.


But:

* **Unchecked exceptions degrade constant-time performance.**.

  However this typically doesn't matter in application domains. Only *algorithmic performance* matters.

### Conclusion

I think abandonment is a reasonable approach for systems languages but I still prefer unchecked exceptions myself for application languages. I prefer the additional flexibility you get with unchecked exceptions and don't mind the performance difference.

### *Related Articles*
{% capture content_with_bullets %}

* [Error Handling](/articles/2013/07/13/error-handling/)
    * *Discusses considerations and specific implementation techniques for writing code that is robust in the presence of errors.*

* [Error handling styles in programming](/articles/2014/11/22/error-handling-styles/)
    * *Summarizes the most prominent strategies for handling runtime errors.*

{% endcapture %}
{{ content_with_bullets | fixbullets }}


[^perf1]: As used in this article, **constant-time performance** refers to being sensitive to high constant factors in program time costs. This is in contrast to **algorithmic performance** which cares primarily about avoiding, for example, an O(n^2) algorithm where an O(n) algorithm would suffice.