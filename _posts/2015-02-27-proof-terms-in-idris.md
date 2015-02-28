---
layout: post
title: Proof terms in Idris
tags: [Software]
style: |
    .formula-box pre {
        background-color: #ffffe0; /* light yellow */
        
        background-image: url("/assets/2015/star.png");
        background-position: top right;
        background-repeat: no-repeat;
    }
    
    .terminal-box pre {
        background-color: #333333; /* chalkboard */
        color: white;
        
        background-image: url("/assets/2015/terminal.png");
        background-position: top right;
        background-repeat: no-repeat;
    }

---

Recently I've been experimenting with the language [Idris], one of the rare **dependently-typed** programming languages.[^also-agda] For example you can write a sorting function that is proven correct by the compiler at *compile time*:

```
sort : (inputList:Vect n e) -> 
       (outputList:Vect n e ** (IsSorted outputList) ** 
                               (ElemsAreEq inputList outputList))
```

The preceding is a function that takes an input list (or "vector") of elements and returns a tuple containing:

1. an output list, 
2. a **proof** that the output list is sorted (`IsSorted`), and 
3. a **proof** that the input list and output list have the same elements (`ElemsAreEq`).

Since the type signature is verified at compile time, any function implementing this signature is a provably correct sort function.[^careful-about-proof-terms]

The notion that a proof can be represented explicitly in a program is fascinating and a unique capability of dependently-typed languages.

In this article I will focus specifically on what proof terms are, how to define them, and how to construct them.

I assume that the reader has basic familiarity with Haskell-like syntax.

<!--
To reach the widest audience possible I assume only that the reader has general programming experience, perhaps only in imperative languages with C-derived syntax. Basic familiarity with Haskell-like syntax is useful but not assumed. I will try to explain new syntax when it appears, particularly when it differs from C-style syntax.
-->

[Idris]: http://www.idris-lang.org

[^also-agda]: [Agda](http://wiki.portal.chalmers.se/agda/pmwiki.php) is another dependently typed language that I've looked at. However I was [not impressed](/articles/2014/02/17/agda-second-impressions/).

[^careful-about-proof-terms]: <p>Actually to prove the correctness of the `sort` function you need to verify one more thing in addition to the function signature: You must verify that the definitions of the related proof types (in this case `IsSorted` and `ElemsAreEq`) correctly implement what their name implies.</p> <p>Usually the definitions of proof types are fairly compact so inspection isn't much of a burden. By contrast the correct *construction* of proof terms within an algorithm is considerably more complex. Happily the compiler checks your work ruthlessly within the algorithm itself, so you don't have to worry about messing up term construction.</p>

[^first-idris-program]: My first non-trivial program in Idris was a [tic-tac-toe game](https://github.com/davidfstr/tic-tac-idris). It uses almost no Idris-specific features (such as dependent types), but was a useful implementation exercise nevertheless. It would be trivial to translate it to an equivalent Haskell program.

## A simple built-in proof type: `Data.So`

Proof types are tricky to grasp at first. Thus let's start by examining the simplest proof type in the Idris standard library[^standard-library], the `So` type.

[^standard-library]: The Idris community appears to prefer the term "the standard library" to refer specifically to the prelude part of the library code that ships with Idris and "the library" to refer to the non-prelude part. I think this distinction is unimportant and confusing so I will use the term "standard library" to refer to *all* library code that ships with Idris, which is consistent with terminology usage in other languages (Python, Java, C#, Perl, PHP, etc).

Here is the definition of the `Data.So` type:

```
data So : Bool -> Type where 
    Oh : So True
```

<!--
Syntax notes:

* Function-like things are declared with `funcName : argType1 -> argType2 -> returnType`.
    * In this case `So` takes a `Bool` and defines a type.
    * Thus `So` is a parameterized type, not unlike the parameterized types `List` and `IList` in Java and C# respectively, which are parameterized by their element type. So a `List<String>` or `IList<string>` is a list of strings. In Idris the same type would be written as `(List String)` (with a space) and declared as `List : e -> Type`, where `e` represented the element type of the list.
* `So` is defined as a data type parameterized[^actually-indexed] by a boolean expression (of type `Bool`). You can create a type expression like `So (1 < 1)` or `So (1 > 2)`.
* `So` has a single type constructor `Oh` which takes no parameters. It is an atomic thing.
* You can only make an `Oh` when the boolean expression in the resultant `So (...)` type can be proven equal to `True` by the compiler at compile time.

[^actually-indexed]: Type theory buffs will probably correct me by emphasizing that types can be *parameterized* by other types but are *indexed* by values. Again I think this distinction is immaterial to the practitioner and therefore will say that a type can be parameterized by either types or values.

-->

The `So` type represents a proof that a particular boolean test has been performed and that it evaluated to `True`. For example it is possible to construct a proof value (`Oh`) of type `So (1 < 2)` but it is not possible to construct a value of type `So (1 > 2)`.

<!--
`Oh`? `So`? These are rather strange names, no? I personally find this type easier to understand if I think of it as:

```
data IsTrue : Bool -> Type where 
    ProvablyTrue : IsTrue True
```
-->

You can construct a value of `So (1 < 2)` directly on the command-line:

{% capture terminal %}

```
$ idris --nobanner
Idris> :module Data.So
*So> the (So (1 < 2)) Oh
Oh : So True
```

{% endcapture %}
<div class="terminal-box">{{ terminal | markdownify }}</div>

The function `(the FooType fooValue)` tells the compiler that `fooValue` should be of type `FooType`, which is occasionally useful. In this case I am asserting to the compiler that `So (1 < 2)` is so obvious that it should just try to construct the proof value `Oh` immediately.

However you can't make a `So (1 > 2)`:

{% capture terminal %}

```
$ idris --nobanner
Idris> :module Data.So
*So> the (So (1 /= 1)) Oh
(input):1:5:When elaborating argument x to function Prelude.Basics.the:
        Can't unify
                So True
        with
                So (fromInteger 1 > fromInteger 2)
        
        Specifically:
                Can't unify
                        True
                with
                        fromInteger 1 > fromInteger 2
```

{% endcapture %}
<div class="terminal-box">{{ terminal | markdownify }}</div>

Here the error message indicates that the compiler isn't convinced that `True == (1 > 2)`, which is absolutely correct.

In a real program the main way to construct a `So` is to use the `choose` function, whose definition is:

```
choose : (b : Bool) -> Either (So b) (So (not b))
choose True  = Left Oh
choose False = Right Oh
```

You might have to stare at this definition for a while to understand how it works. I know it took me a while to grok it. Let me try to explain:

The `choose` function is performing a pattern match on the `Bool` argument it receives. If it successfully pattern matches on `True`, the compiler itself understands that argument `b` is equivalent to `True`, so it permits the construction of the value `Oh` (of type `So b`) on the right-hand-side of the `choose True` definition. The `choose False` definition works via similar reasoning to construct a value `Oh` of type `So (not b)`, since the compiler can deduce that `not b` is `True` when `b` is `False`.

## A simple derived proof type: `IsLte`

What if we wanted to prove specifically that one element is less than or equal to another? We could write a proof type derived directly from `Data.So`.

{% capture formula %}

```
IsLte : Ord e => (x:e) -> (y:e) -> Type
IsLte x y = So (x <= y)
```

{% endcapture %}
<div class="formula-box">{{ formula | markdownify }}</div>

<!--
Syntax notes:

* `Ord e` is a type constraint on `e` which requires that elements of type `e` implement a comparison function, so that expressions like `x <= y` can work (where `x` and `y` are of type `e`).
    * In Java the equivalent constaint is implemented by the interface `Comparable`, and in C# it is `IComparable`.
-->

Here the `IsLte` type is defined directly in terms of the `So` proof type that was described previously. Note that it is necessary to add the `Ord e` type constraint so that the compiler will allow the use of `<=` to compare `x` and `y` in `(x <= y)`.

Strictly speaking the definition of `IsLte` here doesn't create a new type, but rather a type alias to the underlying `So`. Therefore you must use the `Oh` proof value to actually make an `IsLte`:

{% capture terminal %}

```
$ idris --nobanner IsLte.idr 
*IsLte> the (IsLte 1 2) Oh
Oh : So True
*IsLte> the (IsLte 2 1) Oh
(input):1:5:When elaborating argument x to function Prelude.Basics.the:
        Can't unify
                So True
        with
                IsLte (fromInteger 2) (fromInteger 1)
        
        Specifically:
                Can't unify
                        True
                with
                        fromInteger 2 <= fromInteger 1
```

{% endcapture %}
<div class="terminal-box">{{ terminal | markdownify }}</div>

Now it's fine and all to create a `So` or `IsLte` directly on the command line. But how would you create one in an actual program?

{% capture formula %}

```
mkIsLte : Ord e => (x:e) -> (y:e) -> Maybe (IsLte x y)
mkIsLte x y =
    case (choose (x <= y)) of 
        Left proofXLteY =>
            Just proofXLteY
        Right proofNotXLteY =>
            Nothing
```

{% endcapture %}
<div class="formula-box">{{ formula | markdownify }}</div>

<!--
Syntax notes:

* The `choose` function here is the same one mentioned before that operates on `So` types, which works here because an `IsLte` is actually a `So`.
* The `case...of` statement is like a fancy switch statement: It does pattern matching to determine which branch to take.
* Notice the use of the naming convention `proof...` for proof values. Having longish descriptive names for proof values really helps in more complex code that has a lot of proof values.
-->

This function takes an `x` and a `y` at runtime and constructs a proof value of type `(IsLte x y)` if x <= y. If x is not <= y then it fails by returning a `Nothing`.

On the Idris CLI, let's try to construct a valid proof that `(IsLte 1 2)`:

{% capture terminal %}

```
$ idris --nobanner InsertionSort.idr
*InsertionSort> mkIsLte 1 2
Just Oh : Maybe (So True)
```

{% endcapture %}
<div class="terminal-box">{{ terminal | markdownify }}</div>

Nice. How about a proof that `(IsLte 2 1)`?

{% capture terminal %}

```
$ idris --nobanner InsertionSort.idr
*InsertionSort> mkIsLte 2 1
Nothing : Maybe (So False)
```

{% endcapture %}
<div class="terminal-box">{{ terminal | markdownify }}</div>

Fails as expected.

## A simple standalone proof type: `HeadIs`

Let's implement our own simple proof type. How about a proof that a vector begins with a particular value?

{% capture formula %}

```
data HeadIs : Vect n e -> e -> Type where
    MkHeadIs : HeadIs (x::xs) x
```

{% endcapture %}
<div class="formula-box">{{ formula | markdownify }}</div>

<!--
Syntax notes:

* `Vect n e` represents a list (or "vector") of length `n` containing elements of type `e`.
* Regarding vectors:
    * `Nil` is the empty vector. It can also be written as `[]` in some contexts.
    * The operator `::` in `x::xs` takes an element `x` and prepends it to a vector `xs` returning a new vector `x::xs` with the prepended element.
        * Most functional languages define **prepend** as the more basic operation than **append**, in contrast to most imperative languages.
    * The first element of a vector is called the "head". The remainder is called the "tail".
* Regarding naming conventions:
    * `x`, `y`, and `z` will be used to refer to elements in vectors.
    * `xs`, `ys`, and `zs` will be used to refer to vectors.
    * `n` will be used to refer to the length of a vector.
-->

A value of type `HeadIs xs y` represents a proof that a vector `xs` begins with ("has the head") `y`.

Based on the definition above, the compiler will only permit the construction of the atomic `MkHeadIs` proof value if it can destructure its first vector argument and see that its head matches the second argument.

## A complex proof type: `IsSorted`

How about we try to make a more complex proof type? How about a proof that a list of elements is sorted? Such a proof type would be useful in the `sort` function mentioned at the beginning of this article.

Let's take a first stab at thinking about the initial signature of `IsSorted`. We want to be able to write `IsSorted xs`, so we need `IsSorted` to take a vector `xs` argument and return a type:

```
data IsSorted : (xs:Vect n e) -> Type where
    ...
```

Okay. Now, since proof terms work entirely by pattern matching on the arguments received, let's think about what cases exist for matching on the single `xs` vector argument:

* `Nil` -- Definitely sorted, since it's an empty vector. **(Case 1)**
* `x::xs` -- Not enough information to determine whether sorted. Let's decompose `xs`:
    * `x::Nil` -- Definitely sorted, since it's a vector with only one element. **(Case 2A)**
    * `x::(y::ys)` -- Sorted if: **(Case 2B)**
        * (1) we can prove `(x <= y)` and that
        * (2) `(y::ys)` is sorted.[^ys-sorted-insufficient]

[^ys-sorted-insufficient]: In my initial attempt to define `IsSorted` I incorrectly required only the subproof `IsSorted ys` and not `IsSorted (y::ys)` when proving `IsSorted x::(y::ys)`. But that restriction allows you to construct `IsSorted [9,10,1,2]` which is clearly bogus. Pay attention to how your proof types are defined.

So let's write out the preceding cases in code:

```
data IsSorted : (xs:Vect n e) -> Type where
    IsSortedZero :
        ... ->
        IsSorted Nil
    IsSortedOne  :
        ... ->
        IsSorted (x::Nil)
    IsSortedMany :
        ... ->
        IsSorted (x::(y::ys))
```

Straightforward. Now let's fill in the holes for the parameter types:

```
data IsSorted : (xs:Vect n e) -> Type where
    IsSortedZero :
        IsSorted Nil
    IsSortedOne  :
        (x:e) ->
        IsSorted (x::Nil)
    IsSortedMany :
        (x:e) -> (y:e) -> (ys:Vect n'' e) ->     -- (n'' == (n - 2))
        (IsLte x y) -> IsSorted (y::ys) ->
        IsSorted (x::(y::ys))
```

* The `IsSortedZero` case didn't require any parameters at all. Easy enough.
* The `IsSortedOne` case had only the variable `x` in its return type, so we just need to declare the parameter `(x:e)` so that it knew what `x` to use.
* The `IsSortedMany` case is a lot more interesting:
    * It needs the three `x`, `y`, and `ys` objects that appear in the return type `(x::(y::ys))` to be defined.
    * It needs a proof that `x <= y`. So let's use an `(IsLte x y)`.
    * It needs a proof that `y::ys` is sorted, so let's recursively use the `IsSorted` proof type that we're in the middle of defining!
        * Yay recursively defined types. Just like recursively defined functions. And sometimes just as mind-bending.
        * I believe Idris will only allow recursive definitions of types in this way because the compiler itself can determine that the `IsSorted (y::ys)` proof type is "smaller than" the `IsSorted (x::(y::ys))` proof type whose definition it feeds into.

Let's try to compile this:

{% capture terminal %}

```
$ idris -o Scratch Scratch.idr 
Scratch.idr:17:18:When elaborating type of Main.IsSortedMany:
Can't resolve type class Ord e
```

{% endcapture %}
<div class="terminal-box">{{ terminal | markdownify }}</div>

Whoops. The `IsSortedMany` definition doesn't know what to fill in for the implicit `Ord e` parameter to the `IsLte` type. So let's add that parameter to `IsSortedMany`:

```
data IsSorted : (xs:Vect n e) -> Type where
    IsSortedZero :
        IsSorted Nil
    IsSortedOne  :
        (x:e) ->
        IsSorted (x::Nil)
    IsSortedMany :
        Ord e =>
        (x:e) -> (y:e) -> (ys:Vect n'' e) ->    -- (n'' == (n - 2))
        (IsLte x y) -> IsSorted (y::ys) ->
        IsSorted (x::(y::ys))
```

Now this actually compiles and I could stop here. However I know based on painful experience[^unification-hints] that we will run into type unification errors down the road if we don't additionally put the `Ord e` constraint on the `IsSorted` type itself. So let's just do that:

{% raw %}
[^unification-hints]: If you fail to add the `Ord e` constraint to the other type constructors, you will eventually run into errors like `Can't unify "So (<=) {{constrarg1}} x y" with "So (<=) {{constrarg}} x y"` where the compiler loses type information about the specific `Ord e` instance when trying to pull type information through the `IsSortedZero` or `IsSortedOne` type constructors during type unification. That probably didn't make much sense - especially the part about "type unification" - but you'll probably have to debug a similar issue at some point.
{% endraw %}

{% capture formula %}

```
data IsSorted : Ord e => (xs:Vect n e) -> Type where
    IsSortedZero :
        Ord e =>
        IsSorted Nil
    IsSortedOne  :
        Ord e =>
        (x:e) ->
        IsSorted (x::Nil)
    IsSortedMany :
        Ord e => 
        (x:e) -> (y:e) -> (ys:Vect n'' e) ->    -- (n'' == (n - 2))
        (IsLte x y) -> IsSorted (y::ys) ->
        IsSorted (x::(y::ys))
```

{% endcapture %}
<div class="formula-box">{{ formula | markdownify }}</div>

Boom. Done.

Now, similar to the `mkIsLte` function from before, let's create a `mkIsSorted` function that, given a list, checks whether it is sorted and returns an `IsSorted` sortedness proof if it is.

{% capture formula %}

```
mkIsSorted : Ord e => (xs:Vect n e) -> Maybe (IsSorted xs)
mkIsSorted Nil =
    Just IsSortedZero
mkIsSorted (x::Nil) =
    Just (IsSortedOne x)
mkIsSorted (x::(y::ys)) =
    case (mkIsLte x y) of
        Just proofXLteY =>
            case (mkIsSorted (y::ys)) of
                Just proofYYsIsSorted =>
                    Just (IsSortedMany x y ys proofXLteY proofYYsIsSorted)
                Nothing =>
                    Nothing
        Nothing =>
            Nothing
```

{% endcapture %}
<div class="formula-box">{{ formula | markdownify }}</div>

This implementation is interesting. Note how the proof values `IsSortedZero`, `IsSortedOne`, and `IsSortedMany` are constructed directly.

Also notice in particular that to construct an `IsSortedMany` value that the subproof values `proofXLteY` and `proofYYsIsSorted` needed to be constructed first. And that the latter subproof required a recursive invocation of `mkIsSorted`. Lots of recursion in Idris.

Let's try calling the function with a valid sorted list:

{% capture terminal %}

```
$ idris --nobanner InsertionSort.idr
*InsertionSort> mkIsSorted [1,2,3]
Just (IsSortedMany 1
                   2
                   [3]
                   Oh
                   (IsSortedMany 2
                                 3
                                 []
                                 Oh
                                 (IsSortedOne 3))) : Maybe (IsSorted [1, 2, 3])
```

{% endcapture %}
<div class="terminal-box">{{ terminal | markdownify }}</div>

Nice. See how the proof term embeds the `(IsLte 1 2)` and `(IsLte 2 3)` values (both `Oh`) which represent the comparison checks made to determine whether the list was sorted. In this fashion a proof value effectively embeds an execution trace of the program that generated it. Neato.

We can generalize this observation: The contents of a big proof value is a nested structure of smaller proof values that taken together are used to derive the big proof value. Here, an `IsSorted [1,2,3]` value contains both an `IsLte 1 2` and an `IsLte 2 3` value, which is enough to deduce that `[1,2,3]` is sorted.

Now let's try calling `mkIsSorted` with a non-sorted list:

{% capture terminal %}

```
$ idris --nobanner InsertionSort.idr
*InsertionSort> mkIsSorted [3,2,1]
Nothing : Maybe (IsSorted [3, 2, 1])
```

{% endcapture %}
<div class="terminal-box">{{ terminal | markdownify }}</div>

As expected, we couldn't construct a proof that an unsorted list was actually sorted.

## Conclusion

Hopefully you now have a better grasp of proof types and values, and also have some practice in constructing them.

In an upcoming article I hope to demonstrate how proof types like `IsSorted` and `ElemsAreEq` can be used to create a provably correct implementation of [insertion sort]. Stay tuned.

[insertion sort]: https://en.wikipedia.org/wiki/Insertion_sort
