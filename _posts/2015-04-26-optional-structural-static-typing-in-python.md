---
layout: post
title: Optional Structural Static Typing in Python
tags: [Software]

---

I'm working on a new project to build a typechecking linter for Python, in the same vein as [mypy]. The big difference between mypy and what I'm hoping to build is that my type system will be a *structural* type system rather than a *nominal* type system.

[mypy]: http://www.mypy-lang.org

## Structural vs. Nominal Type Systems

Let's consider the following program:

```
interface Foo { public int length(); }
interface Bar { public int length(); }

Foo foo = ...
Bar bar = foo;   // Will this work?
```

In a structural type system (ex: Go, OCaml) the assignment would be allowed because both interfaces have exactly the same set of methods.[^subset] If it looks like a duck then it *is* a duck.

In a nominal type system (ex: Java, C#) the assignment would be rejected because there is no declared subtype relationship between the names `Foo` and `Bar`. The actual *structure* of the interfaces is completely ignored.

[^subset]: To be more precise, the assignment would be allowed because `Foo` structure contains everything that `Bar` requires: the methods on `Bar` are a subset of the methods on `Foo`.

## Why not Nominal Typing?

It generally requires explicit type annotations for all function parameters, and sometimes function return types too. I don't want to write *any* type annotations for the majority of programs that I write, and certainly not annotations for every single function.

There is a serious risk that Python code written with a nominal type system in mind will start introducing large numbers of new abstract base classes for the *sole* purpose of making the typechecker happy. This is exactly the kind of pollution that I'm trying to escape from when working in dynamic languages such as Python.

## Why Structural Typing?

The philosophy behind structural typing meshes a lot better with the "duck typing" that you see in classic Python with no type annotations. If you try to invoke a method on an object and the object has a method with a matching name, the program will work. This is exactly the properly that a structural type system checks.

* Loosely defined protocols such as "file-like objects" continue to work.

* More complex protocols such as "file-like objects that support fileno()" (as needed by the `subprocess` module) also work without needing to introduce further abstract base classes.

* Lightweight JSON-based objects continue to work and benefit from type checking.

More importantly, structural type systems are much more amenable to global type inference, which can be used to eliminate the need for explicit type annotations. This would allow Python programs to still be type-checked without the need to specify type annotations in the usual case. Imagine if your programs *today*, without any type annotations, could suddenly become type checked with no additional effort from you, the programmer.

## Challenges with Structural Typing

Of course structural typing isn't all good. It has one major sticking point: Structural type systems tend to generate huge verbose error messages that aren’t particularly actionable.

This happens because the type checker only knows that two (complex) inferred types are incompatible. It doesn't know which of the two types is correct. And the error messages containing the derivation of the inferred types typically involves lots of locations in the code unrelated to where the actual error lies. Imagine the same level of verbosity as C++ template errors.

## Mission: Difficult

So in summary the goal is to make a type checking linter for Python with a structural type system and global type inference which nevertheless presents comprehensible and actionable error messages in a majority of error scenarios.

I see some original research in my near future.

## References

* [Uncovering the Unknown: Principles of Type Inference](https://www.youtube.com/watch?v=fDTt_uo0F-g) (1h3m)
    * Excellent presentation outlining the difference between nominal vs. structural subtyping, typing inference, and some pros/cons between both kinds of type systems.
* [Types and Programming Languages](http://www.amazon.com/Types-Programming-Languages-Benjamin-Pierce/dp/0262162091/ref=sr_1_1?ie=UTF8&qid=1430091478&sr=8-1&keywords=types+and+programming+languages) (645 pages)
    * Excellent broad overview of type systems and type theory. Leans toward covering type systems similar to those used in mainstream programming languages. Has only limited information about type reconstruction and type inference.