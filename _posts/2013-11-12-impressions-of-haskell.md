---
layout: post
title: Impressions of Haskell
tags: [Software]

include_jquery: true
include_bootstrap_js: true

---

I finally found an online tutorial for Haskell that involves writing a *non-trivial* program:

* [Write Yourself a Scheme in 48 Hours]

It's an excellent tutorial and has given me a good impression of Haskell for building a medium-sized non-trivial program: a LISP interpreter.

This impression, however, has been more negative than positive. I would consider Haskell for use for doing programs that do heavy computation with pure functions alone.[^pure] However if there's any significant amount of I/O, error handling, or state, using Haskell is just bloody painful.

### Monads are painful

* I/O must be done inside an I/O *monad*.[^monad]

* Error handling must be done inside an error monad.[^errors]

* Passing around shared state must be done inside a state monad.[^state]

The preceding by itself would not be such a problem except that, in addition:

* Code that is pure uses a different syntax than code that is in a monad.

* Code that needs to be in multiple monads at the same time is a royal pain to write. It requires the use of *monad transformers* and explicit converting (or "lifting") between individual monads and combined monads.

Having monadic code be in a different syntax than pure code requires the programmer to learn and use two different syntaxes. And these syntaxes aren't even similar: they read in different directions. Mixing code that is both pure and monadic becomes confusing. Upgrading pure code to be monadic, which is not uncommon during development and maintenance, requires a lot of non-trivial syntactic transformations.

* **Pure code** - Reads inside-out, generally bottom-to-top and right-to-left.
* **Monadic code** - Reads top-to-bottom (with do-notation) and left-to-right (with bind operations).
* **Pure + monadic code** - Reads in multiple directions.

<!--
<ul class="nav nav-tabs">
  <li class="active"><a href="#pure" data-toggle="tab">Pure Code</a></li>
  <li><a href="#monadic" data-toggle="tab">Monadic Code</a></li>
  <li><a href="#mixed" data-toggle="tab">Pure + Monadic Code</a></li>
</ul>
<div class="tab-content">
  <div class="tab-pane fade in active" id="pure">
    <p><i>Reads inside-out, generally bottom-to-top and right-to-left.</i></p>
    <p>[TODO: code sample]</p>
  </div>
  <div class="tab-pane fade" id="monadic">
    <p><i>Reads top-to-bottom (with do-notation) and left-to-right (with bind operations).</i></p>
    <p>[TODO: code sample]</p>
  </div>
  <div class="tab-pane fade" id="mixed">
    <p><i>Reads in multiple directions.</i></p>
    <p>[TODO: code sample]</p>
  </div>
</div>
-->

Using a pure value within monadic code requires you to "lift" the pure value into a monad value with an explicit conversion. Similarly using a monadic value in multi-monadic code (created by a monad transformer) requires you to lift the monadic value into a multi-monad value first. These explicit conversions pepper and obscure the main program logic. One has to do an annoying amount of gymnastics to make the type system happy.

### Code golf erodes readability

Another factor complicating the readability of code is the Haskell community's propensity for *code golf*: the tendancy to write code that is especially terse to the point of making it difficult to understand. There are many language and library features in Haskell that enable this:

* Overuse of operator overloading and custom operators:
    * The ability to mix custom infix and prefix operators in the same expression. Confusing.
    * The ability to treat an infix operator as prefix or visa-versa, when using certain syntax. Inconsistent.
    * The usage of custom operators in ambiguous fashion requiring knowledge of either the operator associativity or precedence to disambiguate. Requires non-local knowledge to parse expressions.
        * <p>For example the `$` operator appears to be a precedence hack to avoid the need to parenthesize an expression properly. I don't think it worth introducing tricky syntax to avoid typing a single close paren.</p>
* Implicit partial application of functions. Infix operator sections.
    * <p>You must know the arity of a function to determine what an expression containing that function means.[^arity] Requires non-local knowledge to parse expressions.</p>
* Point-free style.
    * Discourages the use of explaining variables.

Terseness at the expense of readability was a hallmark of Perl. I don't find it any more attractive in Haskell.

Here's a short example containing monadic code, point-free style, and an operator section.

```
-- Parses the expression in the first argument to the program, evaluates it, and prints the result.
main :: IO ()
main = getArgs >>= putStrLn . show . eval . readExpr . (!! 0)
```

I argue that the preceding code is manifestly confusing for any newcomer to Haskell, yet this type of code I see frequently in Haskell written by others.

It is possible to rewrite the code to be more explicit:

```
main = do args <- getArgs
          putStrLn (show (eval (readExpr (args !! 0))))
```

Although I think the preceding would not be considered idiomatic Haskell.

### The end?

Haskell's strong type system and heavy restrictions on mutable state provide good assurance that the programs you write are correct, assuming you manage to write the program in the first place.

However I find Haskell difficult to write (due to monads and the type system) and difficult to read (due to code golf). I also do not require such a high assurance of correctness in the domains I work in. I typically find that a disciplined minimization of mutable state in other languages is sufficent to provide the necessary level of correctness I require, and with more flexibility during maintenance.


[Write Yourself a Scheme in 48 Hours]: http://jonathan.tang.name/files/scheme_in_48/tutorial/functions.html

[^pure]: Types of programs I might consider doing in Haskell include, for example, maze generators, Sudoku solvers (non-visual), parsers, and compilers. Games involving lots of state such as platformers, adventure games, or anything with multiple screens would be a pain. GUIs and other interactive programs based on events would be a pain.

[^monad]: A *monad* is a particular pattern of sequencing computation involving the type system. The use of monads is unique to Haskell so far as I am aware.

[^errors]: Granted it is possible to handle errors using [`throw`](http://hackage.haskell.org/package/base-4.6.0.1/docs/Control-Exception.html#v%3athrow) but this is discouraged because it yields non-deterministic ordering with respect to I/O operations. It is also possible to use [`throwIO`](http://hackage.haskell.org/package/base-4.6.0.1/docs/Control-Exception.html#v%3athrowIO) but only if the function is already in the IO monad. Should the function be otherwise pure, you'd be forced to "infect" it with the IO monad in order to use `throwIO`.

[^state]: Of course you could just incorporate the shared state into the parameters and return type of all functions, but this gets annoying fast. Granted it is possible to use [`IORef`s](http://www.haskell.org/ghc/docs/latest/html/libraries/base/Data-IORef.html) if the function using state is already in the IO monad. Should the function be otherwise pure, you'd be forced to "infect" it with the IO monad in order to use `IORef`s.

[^arity]: <p>I wrote an [entire article](/articles/2013/05/12/implicit-partial-application-and-currying-considered-harmful/) on just this point of implicit partial application being confusing. Unfortunately I think r/haskell was confused by my argument.</p> <p>Consider the expression `f 3` by itself, possibly part of a larger expression like `f 3 $ g`. In a typical language I consider functions to be entities that take some fixed number of arguments and then produce a single result. This means that if I encounter a well-named function `f` that I haven't seen before, I can usually guess from its name what it does and what its return type is. I can also assume that an expression like `f 3` will evaluate to this assumed return type.</p> <p>In Haskell I cannot make that assumption: Support for implicit partial function application might mean that an expression `f 3` might not evaluate to the return type of `f`. I have to ask myself "Does it look like this function needs more arguments here to perform the action that its name suggests?". If the answer is yes then I assume that the expression evaluates to a new function with some unknown number of arguments with the return type I expect. That's very confusing. I object to the possibility that two function applications that begin with `f 3 ...` could return different types of values.</p>
