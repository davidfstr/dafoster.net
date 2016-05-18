---
layout: post
title: Error handling styles in programming
tags: [Software]

---

There are many ways that programs can handle errors at runtime. The excellent book [Exercises in Programming Style] proposes an interesting categorization of common error handling patterns. Fascinatingly, the programming language that you work in often actively encourages one particular error handling pattern over another.

## Reinterpret and Continue <small>(Constructivist)</small>

<img style="float: right;" src="/assets/2014/error-handling-styles/constructivist.jpg" title="Constructivist"/>

In this style, a function that receives a bad input or encounters an error always returns a sensible result to its caller, silently reinterpreting the error to a valid value. Such a function will never crash the program but may produce unexpected results in the presence of bad inputs or errors.

Languages whose standard libraries and syntax regularly reinterpret errors and questionable input make it difficult to write programs that are not in this style.

Environments that encourage this style:

<img style="float: right;" src="/assets/2014/error-handling-styles/php-web.png" title="PHP, HTML, CSS, JavaScript"/>

* **PHP**
    * Very few PHP errors will actually crash the program - instead you get strange results and error text inserted into rendered pages.
    * Errors are printed to a server log file that nobody reads.
* **HTML, CSS**
    * Web browsers reinterpret bad markup as best they can to valid markup. Of course different browsers do this in different ways, so the only way to get a consistent rendering is to use valid markup.
    * Rendering errors are not generally logged anywhere.
* **JavaScript**

Developers that wish to use a more Fail Fast style of error handling (see below) but are forced to write in one of these languages may use special validation and linting tools to look for errors in the program text before they can be reinterpreted.


## Fail Fast <small>(Tantrum, Passive Aggressive)</small>

In this style, a function that receives a bad input or encounters an error refuses to continue, returning an error back to its caller.

<img style="float: right;" src="/assets/2014/error-handling-styles/tantrum.jpg" title="Tantrum"/>

<img style="float: right; clear: both; margin-top: .5em; margin-left: .5em;" src="/assets/2014/error-handling-styles/passive-aggressive.jpg" title="Passive Aggressive"/>

[Exercises in Programming Style] makes the additional distinction that functions in some programs try to handle errors immediately at their point of detection no matter what ("Tantrum"), whereas functions in other programs prefer to bubble up errors to callers until a caller with enough context is reached that decides to actually handle the error ("Passive Aggressive").

Programs in the Tantrum substyle have lots of error handling code scattered throughout the program text, whereas programs in the Passive Aggressive substyle tend to consolidate most error handling code in top-level functions and let lower-level code just bubble up errors.

Languages that have built-in exceptions make it easy to implement programs in the Passive Aggressive substyle.

Environments that encourage this style:

<img style="float: right;" src="/assets/2014/error-handling-styles/java-csharp-python.png" title="Java, C#, Python"/>

* **Java**
* **C#**
* **Python**

### *Related Articles*
{% capture content_with_bullets %}

* [Error Handling](/articles/2013/07/13/error-handling/)
    * *More comprehensively discusses considerations and specific implementation techniques for writing code that is robust in the presence of errors.*

* [Abandonment vs. Unchecked Exceptions for Error Handling](/articles/2016/05/17/abandonment-vs-unchecked-exceptions-for-error-handling/)
    * *Describes abandonment, an uncommon error-handling style.*

{% endcapture %}
{{ content_with_bullets | fixbullets }}

[Exercises in Programming Style]: https://www.amazon.com/Exercises-Programming-Style-Cristina-Videira/dp/1482227371/ref=as_sl_pc_ss_til?tag=dafo07-20&linkCode=w01&linkId=7FSPMMHJB3KVNUKV&creativeASIN=1482227371