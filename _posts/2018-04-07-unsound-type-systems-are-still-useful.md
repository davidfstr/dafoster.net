---
layout: post
title: Unsound type systems are still useful
tags: [Software]
x_target_audience: [Type System Academics, Software Engineers]

---

The conventional wisdom in the academic community [appears to be] that a type system is not useful if it cannot be proven to be *sound*[^sound].

[appears to be]: https://frenchy64.github.io/2018/04/07/unsoundness-in-untyped-types.html

[^sound]: Soundness means that a type system never misjudges the runtime type of a value. In practice this means that (1) the type system defines a static type for *all* variables and expressions and (2) type casts that override the type system are *not* permitted.

However as a software practitioner I definitely find unsound type systems to still be quite useful. The principal benefits that I get out of a type system include:

* **Identification of many common types of errors**, in particular:

    - misspelled names of functions and variables,
    - missing import statements,
    - null-pointer dereference errors,
    - type mismatch errors, and
    - <p>inexhaustive case handling of type codes and algebraic data types.<p>

* **API documentation that is machine-checked** for consistency and correctness that cannot silently get outdated.

Common unsound type systems such as [mypy] and [TypeScript] typically provide all of these benefits.

A *sound* type system can additionally provide a few additional benefits that I don't miss much in practice:

* **<i>All</i> runtime types will be consistent with the static types assigned by the type system.**

  This property permits the **elimination of most or all runtime type checks**, which can improve the constant-factor performance of programs by a factor of 100 - 1,000x. I don't miss this type of performance reduction because the programs I write - typically web applications - are usually I/O-bound rather than CPU-bound. Therefore I care far more about the *algorithmic* performance of programs I write rather than the *constant-factor* performance.[^algor-vs-constant-perf]

* **It is safe to fully "lean on the type system"** to locate and fix consistency errors when performing common refactorings such as renames, moves, and function signature changes.

  In absence of a sound type system it becomes necessary to lean on *tests* instead of the type system to locate and fix consistency errors.

In short, I get a lot of mileage out of unsound type systems, so I would encourage those who research and implement type systems to still consider type systems that are unsound as worthy of study, such as the Gradual Typing family of type systems.

[^algor-vs-constant-perf]: <p>I use the term <b>algorithmic performance</b> to refer to the Big-Oh average case and worst case CPU performance of a particular program. I use the term <b>constant-factor performance</b> to refer to differences in program CPU performance due to differences in constant factors only.</p><p>For example in comparing an implementation of merge sort on integers written in a statically-typed language such as C to an implementation written in a dynamically-typed language such as Python, they will be equivalently fast in terms of Big-Oh notation (so they have the same algorithmic performance) but the C version will be faster in terms of constant-factor performance due to having no runtime type checks.</p>

[mypy]: https://www.infoworld.com/article/3066749/application-development/mypy-improves-static-type-checking-for-big-python-apps.html

[TypeScript]: http://www.typescriptlang.org/