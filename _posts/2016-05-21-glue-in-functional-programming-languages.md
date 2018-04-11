---
layout: post
title: Glue in Functional Programming Languages
tags: [Software]

---

[Why Functional Programming Matters] is a famous paper on the merits of functional programming&nbsp;(FP). It argues that FP has two big special tools for *glueing* programs together:

1. **Higher-order functions can be easily composed** with other functions to create powerful composite functions.

2. **Lazy evaluation** allows efficient processing of streams and large data structures.

[Why Functional Programming Matters]: http://www.cse.chalmers.se/~rjmh/Papers/whyfp.html

### Higher-Order Functions, meet List Comprehensions

I would like to note that Python — a modern imperative language that also supports functional and object-oriented paradigms — has not only higher order functions but something even better: **list&nbsp;comprehensions**.

List comprehensions allow very succinct composition of user functions with the most important higher-order functions: `map`, and `filter`.

Compare the following paired examples, showing a list comprehension first, followed by a composition of `map` and `filter`:

* `[n * 2 for n in nums]`  
  `nums.map(lambda n: n * 2)`

* `[n for n in nums if n % 2 == 0]`  
  `nums.filter(lambda n: n % 2 == 0)`

* `[item.name for item in items if item is not None]`  
  `items.filter(lambda item: item is not None).map(lambda item: item.name)`

I would argue that in all of these cases the list comprehension is both (1) easier to understand and (2)&nbsp;more succinct.

### Lazy Evaluation, meet Generators and Coroutines

Lazy evaluation can certainly be very expressive for processing large data structures, compared with greedy evaluation. However I would like to note the following:

* Lazy evaluation **significantly complicates using a traditional step-by-step debugger tool to step through a program**:[^haskell-debugger] the current instruction pointer constantly warps up and down the call stack, which can be very confusing.

* Lazy evaluation **interacts poorly with error handling, I/O, and other side effects**.[^haskell-effects]
  
  This limits lazy evaluation's advantages in processing large data structures to only those structures which are *in-memory* or *procedurally generated* rather than the (IMHO more-common) structures that reside *on disk* or must be fetched *over the network* - which must be read with I/O and may be malformed, thus requiring error handling.

* Pervasive use of lazy evaluation introduces unnecessary context switching overhead that **degrades the constant-factor performance of algorithms** for which greedy evaluation would be acceptable. This makes pervasive lazy evaluation unsuitable for certain domains, such as systems domains.

Instead of *pervasive* lazy evaluation, I find it sufficient to have lazy evaluation *on demand* in the form of Python's **generators**, **generator comprehensions**, and **coroutines** when needed.

[^haskell-debugger]: Presumably this is why Haskell does not ship with a traditional debugger. (Or at least I am not able to locate documentation for one.)

[^haskell-effects]: Presumably this is one reason why Haskell does not allow unconstrained side effects, although there are many other reasons for having such constraints.
