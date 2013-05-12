---
layout: post
title: Implicit Partial Application (Currying) Considered Harmful
tags: [Software]

---

<div style="padding: .8em 1em .8em; margin-bottom: 1em; border: 1px solid #94da3a;">
    <p style="font-weight: bold; color: #487858;">
        Audience
    </p>
    <p style="margin-bottom: 0em;">
        I assume familiarity with the Haskell programming language or some other language that supports calling a function with less arguments than the function's signature requires. In academic-speak, this is called "partial application of a function".
    </p>
</div>

Consider the following function-call expression in Haskell:

```
(alpha beta gamma)
```

What can be deduced?

* `alpha` is a function (either imported or in a variable).

In most languages (that disallow implicit partial application) you could additionally deduce:

* `alpha` takes exactly 2 arguments
* The expression's return type matches that of `alpha`.

Neither of those two properties are necessarily true in Haskell.

### Case 1: alpha takes exactly 2 arguments

In this case, the expression behaves as you'd expect in any other language. In particular:

* `alpha` takes exactly 2 arguments
* The expression's return type matches that of `alpha`.

### Case 2: alpha takes more than 2 arguments

In this case, the expression is a partial application of `alpha`, and would be perhaps better read as:

`(\ ... -> alpha beta gamma ...)`

Or, in a more C-like notation:

`function (...) { return alpha(beta, gamma, ...); }`

Thus:

* `alpha` takes exactly 2+K arguments, for some unknown K.
* The expression returns a function of K arguments.

### Case 3: alpha takes less than 2 arguments

Let's say `alpha` takes 1 argument. This would be intuitively read as:

`((alpha beta) gamma)`

After this reformulation you need to recursively examine the new expression. 

In this example, we can deduce:

* `(alpha beta)` returns an anonymous function of (at least) 1 argument.
* If this anonymous function takes 1 argument, then it is just called with `gamma`, and the original expression's return type matches the return type of the anonymous function.
* If this anonymous function takes more than one argument (1+K), then it is partially applied to `gamma`, and yet another anonymous function (that takes K parameters) is returned as the result of the original expression.

### Summary

What a mess. If `alpha` does not in fact take two arguments then I have to exert non-trivial effort to derive the type of the expression - or even what the expression semantics are.

## Eliminating the Ambiguity

There are two ways I can see to simplify these weird cases:

### Make partial application *explicit*

Then we would see syntax like:

<pre>
-- alpha takes 2 arguments
-- return type matches that of alpha
(alpha beta gamma)

-- alpha takes 2+K arguments;
-- return type is a partially applied K-argument function
(alpha beta gamma ...)   

-- alpha takes 1 argument and returns a 1-argument function;
-- expression's return type matches that of the 1-argument function
((alpha beta) gamma)

-- alpha takes 1 argument and returns a (1+K)-argument function;
-- expression's return type is a partially applied K-argument function
((alpha beta) gamma ...)
</pre>

Notice that each conceptually different case now has a unique syntactic representation - it's no longer just `(alpha beta gamma)` for all cases.

### Use a grouping operator for function application

For example parentheses could be used instead of a space to signify function calls.

Using a grouping operator syntactically prohibits relying on the left-associativity of space for partial function application, since a grouping operator doesn't have associativity.

If you combined this suggestion with the explicit syntax extension above, you would get syntax like:

<pre>
-- alpha takes 2 arguments
-- return type matches that of alpha
alpha(beta, gamma)

-- alpha takes 2+K arguments;
-- return type is a partially applied K-argument function
alpha(beta, gamma, ...)   

-- alpha takes 1 argument and returns a 1-argument function;
-- expression's return type matches that of the 1-argument function
alpha(beta)(gamma)

-- alpha takes 1 argument and returns a (1+K)-argument function;
-- expression's return type is a partially applied K-argument function
alpha(beta)(gamma, ...)
</pre>

This more C-like (or ALGOL-like) notation is a lot more readable to mainstream programmers than the original Haskell syntax.

### *Related Articles*

* [Unique Features of Various Programming Languages](/articles/2013/01/29/unique-features-of-various-programming-languages/)
    * *Describes several other programming languages and their unique features.*
* [Visual Guide to Programming Language Properties](/articles/2013/02/20/visual-guide-to-programming-language-properties/)
    * *Visualizes how various programming language properties interact.*


## Appendix

I originally got bitten by this syntactic ambiguity when trying to decipher the meaning of:

```
(flip (/) 20)
```

I was not previously familar with `flip` and so I assumed that it took two arguments, a function (namely `(/)`) and a non-function (namely `20`). And that it probably returned a function, since its surrounding context expected a function.

In fact `flip` takes only one argument and thus is more clearly written as:

```
((flip (/)) 20)
```

And inlined further to be the lower-order:

```
(\x -> x / 20)
```

And, if desired, further rewritten to be the more-compact:

```
(/ 20)
```

This last form uses left-currying, which is obvious since `/` is a well-known built-in infix operator that requires an unspecified left argument, which would be filled in by currying.