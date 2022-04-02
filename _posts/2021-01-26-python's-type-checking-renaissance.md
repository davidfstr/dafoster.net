---
layout: post
title: "Python's type checking renaissance"
tags: [Software]
x_audience: |
    all Python developers, including hobbyists, academics, and practitioners
x_performance: |
    4,143 hits on day 1 of publish and post to Hacker News
    6,473 hits on week 1 of publish, with daily numbers of:
        4143, 1500, 453, 144, 69, 80, 84
                                  ↑ interesting to see increase here
                                        21 from Hacker News
                                         1 from Twitter
                                         * from elsewhere
date_updated: 2022-03-29

include_jquery: true

script: |
    // Rotate triangle symbol when accordian toggled
    $('.accordion-toggle .expand-symbol').text('▸ ');
    $('.accordion-toggle').click(function() {
        var accordianBodySelector = $(this).attr('href');
        var isCollapsed = $(accordianBodySelector).attr('class').indexOf("in") !== -1;
        
        if (isCollapsed) {
            $('.expand-symbol', this).text('▸ ');
        } else {
            $('.expand-symbol', this).text('▾ ');
        }
    });

---

You may have heard that TypeScript has been taking the web development space by storm in the [last](https://2018.stateofjs.com/javascript-flavors/typescript/) [few](https://2019.stateofjs.com/javascript-flavors/typescript/) [years](https://2020.stateofjs.com/en-US/technologies/javascript-flavors/), bringing to it static types. I believe the same thing is starting to happen in the world of Python, where type checkers like [mypy],  [Pyre], and [Pyright] are increasingly used, at least where Python is used by companies to write large systems.

[mypy]: http://mypy-lang.org/
[Pyre]: https://pyre-check.org/
[Pyright]: https://github.com/Microsoft/pyright

For the last several releases of Python, there have been an increasing number of type checking features added to each release by various PEPs:

{% capture python_releases %}

* Python 3.5 <small>(Released Sep 2015)</small>
    * [Type Hints (PEP 484)](https://www.python.org/dev/peps/pep-0484/) - The original introduction of type checking type annotations into the Python language.
* Python 3.6 <small>(Released Dec 2016)</small>
    * [Syntax for variable annotations (PEP 526)](https://www.python.org/dev/peps/pep-0526/)
* Python 3.7 <small>(Released Jun 2018)</small>
    * [Deferred Evaluation of Annotations with Strings (PEP 563)](https://www.python.org/dev/peps/pep-0563/#non-typing-usage-of-annotations) - Most type checking annotations no longer need to be in runtime context.
    * New kinds of types:
        * [TypedDict is available in mypy_extensions](/projects/typeddict/) - Typed dictionaries have specific named keys mapped to specific value types. Such dictionaries are ubiquitous in JSON.
        * [Data Classes (PEP 557)](https://www.python.org/dev/peps/pep-0557/#rationale) - Data classes are analogous to typed dictionaries.
* Python 3.8 <small>(Released Oct 2019)</small>
    * New kinds of types:
        * [TypedDict is standardized (PEP 589)](https://www.python.org/dev/peps/pep-0589/)
        * [Literal types are standardized (PEP 586)](https://www.python.org/dev/peps/pep-0586/)
* Python 3.9 <small>(Released Oct 2020)</small>
    * Fewer imports from the `typing` module are needed:
        * [Type Hinting Generics In Standard Collections (PEP 585)](https://www.python.org/dev/peps/pep-0585/) - Can use `list[T]`, `dict[K, V]`, etc in place of `List[T]` and `Dict[K, V]`. 
* Python 3.10 <small>(Released Oct 2021)</small>
    * New kinds of types:
        * [Parameter Specification Variables: `ParamSpec` (PEP 612)](https://www.python.org/dev/peps/pep-0612/)
        * [User-Defined Type Guards: `TypeGuard` (PEP 647)](https://www.python.org/dev/peps/pep-0647/)
    * New syntax useful for types:
        * [Explicit Type Aliases (PEP 613)](https://www.python.org/dev/peps/pep-0613)
        * <strike>[Support for indexing with keyword arguments (PEP 637)](https://www.python.org/dev/peps/pep-0637/)</strike> (Rejected 😞)
    * Fewer imports from the `typing` module are needed:
        * [Union types are shortened to `X | Y` (PEP 604)](https://www.python.org/dev/peps/pep-0604/)
            * Optional types shortened to `X | None`
        * <strike>[Optional types shortened to `X?` (PEP 645)](https://www.python.org/dev/peps/pep-0645/)</strike> ([Withdrawn 👌](https://mail.python.org/archives/list/typing-sig@python.org/message/YVEIYEK3H6KPZVYR5NBTXSVJ77WHBXHY/))
* Python 3.11 <small>(Scheduled for Oct 2022)</small>
    * New kinds of types:
        * [Arbitrary Literal String Type (PEP 675)](https://peps.python.org/pep-0675/)
        * [`Self` Type (PEP 673)](https://peps.python.org/pep-0673/)
        * [Variadic Generics with `TypeVarTuple` (PEP 646)](https://peps.python.org/pep-0646/)
    * New syntax useful for types:
        * <strike>[Callable Type Syntax (PEP 677)](https://peps.python.org/pep-0677/)</strike> (Rejected 😞)
    * Extensions to existing typing features:
        * [Required[] and NotRequired[] items for TypedDict (PEP 655)](https://peps.python.org/pep-0655/)
        * (?) [Data Class Transforms (PEP 681)](https://peps.python.org/pep-0681/)
* Python 3.12 <small>(Forecasted for Oct 2023)</small>
    * New kinds of types:
        * (??) [Type Hint for Runtime Type Annotation Objects: `TypeForm`](https://dafoster.net/projects/typeform/) (planned)
    * New syntax useful for types:
        * (??) [Deferred Evaluation Of Annotations Using Descriptors (PEP 649)](https://peps.python.org/pep-0649/) - Most type checking annotations no longer need to be in runtime context.

{% endcapture %}

<div class="accordion" id="python-releases" style="margin-bottom: 1em;">
  <div class="accordion-group">
    <div class="accordion-heading">
      <a class="accordion-toggle" data-toggle="collapse" data-parent="#python-releases" href="#collapseOne">
        <span class="expand-symbol"></span><strong>Python releases, and related type checking features</strong>
      </a>
    </div>
    <div id="collapseOne" class="accordion-body collapse">
      <div class="accordion-inner">
        {{ python_releases | markdownify }}
      </div>
    </div>
  </div>
</div>

The traffic on [typing-sig], the mailing list where most major new typing features are proposed and designed, has also been seeing increasing traffic year over year.[^typing-sig-traffic]

[typing-sig]: https://mail.python.org/archives/list/typing-sig@python.org/

[^typing-sig-traffic]: Increasing traffic on [typing-sig](https://mail.python.org/archives/list/typing-sig@python.org/) is reflected in an increasing number of discussions year-over-year. In 2019 there were 63 discussions. In 2020 there were 113 discussions (79% increase). And 2021 is just beginning.

I personally have found type checking to be very useful when working on large Python applications[^large-web-apps]. It helps me find numerous small errors that are introduced during regular development<!-- such as import errors-->. Sure, most of these errors would be caught by the automated tests that I write for each new feature anyway<!-- TODO: footnote+link to TDD or similar practice? -->, but the type checker can find a whole bunch of errors all at once without even running the program, which decreases cycle times when adding new features:

[^large-web-apps]: I personally use type checking in [a large Django web application](/projects/techsmart-platform/) that I work on.

Without type checking I tend to:

* Write a bunch of new code.
* **Repeat 4-6 times, in rapid succession:**
    * Run program to manually test.
    * Find basic error (like a missing import).
    * Fix basic error.
* Debug/fix deeper errors in the new code.
 
But *with* type checking I can:

* Write a bunch of new code.
* **Run the type checker. Get a report of 4-6 basic errors. Fix basic errors immediately.**
* Debug/fix deeper errors in the new code.

I appreciate this increased productivity that type checking gives me when working on large programs. And I hope that more Python users try type checking for themselves, especially as Python gains an increasing number of related features in recent releases. It's an exciting time to be a Python developer!

### *Related Articles*

* [Unsound type systems are still useful](/articles/2018/04/07/unsound-type-systems-are-still-useful/)
* [Dependent Types: Impressions of a software practitioner](/articles/2019/01/06/dependent-types-impressions-of-a-software-practitioner/)

### *Related Projects*

* [TypedDict](/projects/typeddict/) - Python typechecker support for recognizing structured dictionaries with specific named keys mapped to specific value types.
* [trycast](/projects/trycast/) — Parses JSON-like values whose shape is defined by typed dictionaries (TypedDicts) and other standard Python type hints.

### *Related Discussion*

* [Hacker News](https://news.ycombinator.com/item?id=25916628)

### *Update History*

* 2022-03-29:
    * Update final PEPs for Python 3.10, which has now been released.
    * Update in-progress PEPs for Python 3.11, which is now in development.
    * Update speculative PEPs for Python 3.12, which is in the future.
