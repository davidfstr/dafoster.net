---
layout: post
title: "Dependent Types: Impressions of a software practitioner"
tags: [Software]

---

<img class="img-box-right img-200" alt="Book: The Little Typer" src="/assets/2019/the-little-typer.jpg" />

Dependent types are a feature of certain programming language type systems that are unusually powerful, expressive, and precise, compared with other kinds of types. Dependently-typed programming languages such as Coq, Agda, and Idris appear occasionally in academia but not at all in mainstream languages used by software practitioners.

I have been curious about dependent types for some time because of their potential for writing programs that are more correct and have fewer bugs. If you look at my [hierarchy of programming languages](/articles/2014/12/20/languages-by-hardware-distance/) you'll notice dependently typed languages way at the bottom beyond even the "high-typed languages". I even wrote [a provably-correct implementation of insertion sort](https://github.com/davidfstr/idris-insertion-sort) in Idris a few years ago.

Recently my interest in dependent types was rekindled by the release of a new book, [The Little Typer](https://www.amazon.com/Little-Typer-MIT-Press/dp/0262536439/), that aims to be an accessible introduction to dependently typed programming. I just finished reading that book. Below are my impressions of the applicability of dependent types to a software practitioner such as myself.

## What is a dependent type anyway?

A **type** describes the shape of a particular value or the shape of a variable that holds values. Being able to talk about the shape of something in a programming language is useful because most kind of operations always want to be given things of the same shape.

There are **simple types** like `Integer`, `String`, and `List` in all typed languages.

There are **generic types** like `List of Integer` and `Map of String to Integer` that are defined in terms of other *types*. Generic types are extremely useful for describing collection values (i.e. lists, sets, maps, etc), which are pervasive in programming.

Then there are **dependent types** like `List of Integer of length 5` or `IsSorted [1,2,3]` that are defined in terms of *values*.  Since values are more precise things than types, a dependent type (defined with a value as a parameter) is a more precise shape than a simple unparameterized type or a generic type (defined with a type as a parameter).

## What are dependent types useful for?

### More precise types in general

Since dependent types allow defining more precise shapes than other kinds of types, and because type systems can be used by a type checker to verify the consistency of a program, dependent types allow defining functions in a program with more precise input and output restrictions that are automatically checked for correctness by the type checker. Such automatic checking is powerful for providing confidence that the program is correct (i.e. self-consistent).

With dependent types, you can define a known-length collection type such as `List of Integer of length 5`. This is clearly more precise than `List of Integer` or `List`. However I don't think this additional precision is generally *useful*: very few functions in my programs care about how long their lists are at compile type. At most some functions would prefer to disallow empty lists.

With the known-length collection type mentioned above, you can further define a function `first` that takes a *non-empty* list of values (that the type checker can verify as definitely non-empty) and can guarantee that it will return an output value without having any kind of error. In most languages the best you can do is define such a function that takes any list that will fail at runtime if it is given an empty list. With dependent types you can flag such uses at compile time.

### Proofs; Propositions as types

Dependent types allow you to construct [**proof types**](/articles/2015/02/27/proof-terms-in-idris/) such as `(IsPositive 5)` and their associated proof values. The ability to write arbitrary logical statements as types in a dependently typed programming language is sometimes called "propositions as types". This capability is particularly useful for human mathematicians, theorem provers, and academics.

It can be useful to use proof types to write functions that not only compute something useful but also return a proof that they calculated the *correct* value. For example it is possible to write [a sorting function that is proven correct](https://github.com/davidfstr/idris-insertion-sort) in that it returns not only an output sorted list but also a proof that the output list is sorted and also a proof that the output list has the same elements as the input list. That's pretty cool. Unfortunately these proof values can be devilishly difficult to construct and manipulate.

### That's it?

These are all the applications I've been able to discover for dependent types so far. In particular I haven't been able to find any specific "killer application" of dependent types to any common problem that I see as a software practitioner.

## What costs arise from using dependent types?

### Complexity

You must learn, remember, and understand several new kinds of language constructs to manipulate dependent types. In particular in addition to regular function application (λ) you must also learn about how to construct and manipulate dependent pairs using Π and Σ. This creates a **steeper initial learning curve** and **constant mental overhead** while writing dependently-typed programs.

### Verbosity

Dependent types have additional parameters that need to be passed between functions, transformed inside functions, and output by functions. Thus any function manipulating a dependently typed value will require **a lot more code** to manipulate these additional parameters than an equivalent function using simpler-typed values will not.

More code takes longer to write, provides more opportunities for introducing bugs, and is more time-consuming to maintain.

### Lack of encapsulation

Using dependent types frequently seems to involve **pattern matching on the low-level structure of values**. For example it is common for a function manipulating the natural number type (`Nat`) to pattern-match on the specific value constructors of `Nat`, revealing that it is implementated as a `0` base value wrapped inside some number of `add1`s, similar to a linked list.

If you wanted to change the natural number type to instead be implemented using a more-efficient list of bits, you wouldn't be able to do so without breaking every function using the original definition of natural numbers.

### Restrictions on loops and recursion

Several dependently-typed languages I've encountered so far (at least Pie and Agda) disallow function definitions that cannot be proven by the compiler to always terminate, presumably to guard against the type checker going into an infinite loop if presented with a problematic program. In particular this means **no generalized loops** and **no generalized recursion** are allowed. These language constructs are extremely useful and it is frequently a pain to work around their absence.

## Conclusion

There are no killer apps of dependent types that I can identify for software practitioners, and dependent types have significant costs. Thus in general I feel the costs of using dependent types outweigh the benefits for practical software applications outside the domain of theorem-proving.

### *Related Articles*

* [Proof terms in Idris](/articles/2015/02/27/proof-terms-in-idris/)
* [Agda: Second Impressions](/articles/2014/02/17/agda-second-impressions/)
* [Agda: First Impressions](/articles/2014/01/24/agda-notes-and-evaluation/)
* [Unsound type systems are still useful](/articles/2018/04/07/unsound-type-systems-are-still-useful/)
