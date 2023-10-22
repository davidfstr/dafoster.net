---
layout: post
title: "Agda: Second Impressions"
tags: [Software]
x_date_started: 2014-02-09

include_accordian: true

style: |
    /* Remove borders and other styling from accordions with source files */
    .accordion code { border: 0; }
    .accordion-body pre { border: 0; margin: 0; padding: 0; background-color: inherit; }

---
{% capture content_with_bullets %}

These are my second impressions of the Agda programming language after writing (or trying to write) a few simple Agda programs.

If you only want the highlights, just read the [Executive Summary](#executive-summary). If you also want to see supporting material and notes, continue reading further.

{% capture toc_content %}

* [Executive Summary](#executive-summary)
* [Programs](#programs)
    * [Peano](#peano)
    * [HelloNumber](#hellonumber)
    * [HelloWorld](#helloworld)
    * [PrintTwoThings](#printtwothings)
    * [EchoInput](#echoinput)
    * [PromptForName](#promptforname)
    * [EchoInputReverse](#echoinputreverse)
    * [ParseInt](#parseint)

{% endcapture %}

<div class="toc">
  {{ toc_content | markdownify }}
</div>

<a id="executive-summary"></a>
## Executive Summary

Agda is simultaneously touted as (1) a dependently-typed *programming language* and (2) a proof assistant. I find that Agda is a considerably better proof assistant than it is a programming language at this time.

A few issues I found when trying to use Agda as a programming language to get real work done:

* I/O is painful:
    * The Agda standard library lacks any functions for reading from standard input. Clearly the ability to write basic command-line programs is not a priority for the Agda library implementors.
        * You must implement such functions yourself as native functions that call into Haskell.
    * The I/O that does exist is based on Haskell's I/O monad, which by itself is difficult enough to learn.
    * It appears that one has to learn what [coinduction] is in order to use Agda's native `IO` module. Yet another abstract academic construct.
        * I can work around this by restricting myself to the `IO.Primitive` module. This module directly mirrors Haskell's IO system and thus only requires knowledge of monads.

* Some basic numerical operations are very inefficient.
    * The `div` and `mod` operators for the default implementation of natural numbers (`Data.Nat`) run in *linear* time relative to the magnitude of the divisor.[^data-bin]
        * Consequently it takes about **16 seconds** to print the number 4000 because of division inefficiency when formatting the number for display.
    * At least `≤?`, `≟`, `+`, and `*` appear to be logarithmic- or constant-time.

* The "Hello World" program compiles to a 14 MB binary. Unacceptably large.

* The "Hello World" program takes 3 seconds to compile. Unacceptably slow.

* It takes quite a lot of effort to get a basic environment running. You have to:
    * Install Agda.
    * Install the Agda standard library separately.
    * Compile the Agda IO.FFI module manually.
    * Install and learn Emacs.
    * Configure Emacs to work with Agda.[^debug-emacs]

### *Related Articles*

* [Agda: First Impressions](/articles/2014/01/24/agda-notes-and-evaluation/)
    * *Previous article in this series.*

[^data-bin]: There is another module called `Data.Bin` which provides a representation of natural numbers which uses an efficient binary representation. But most of the standard library does not use it.

[coinduction]: http://adam.chlipala.net/cpdt/html/Coinductive.html

[^debug-emacs]: I found configuring Emacs for Agda to be nontrivial. I had to learn enough Emacs Lisp to debug my `.emacs` configuration file.

<a id="programs"></a>
## Programs

The following are all the simple programs I've written with Agda so far.

<a id="peano"></a>
### Peano

A manual reimplementation of natural numbers (i.e. non-negative integers) just so that I can get my Agda environment up and running.[^peano-credits]

{% capture code_peano %}

```
module Peano where

data ℕ : Set where
  zero : ℕ
  suc : ℕ → ℕ

_+_ : ℕ → ℕ → ℕ
zero + zero  = zero
zero + n     = n
(suc n) + n' = suc (n + n')
```

{% endcapture %}

{% include accordian/begin %}
    <code>Peano.agda</code>
{% include accordian/middle %}
    {{ code_peano | markdownify }}
{% include accordian/end %}

* I resent being forced to use Emacs as opposed to my favorite text editor.
    - Particularly since the installation instructions are not bulletproof.

[^peano-credits]: Kudos to [Learn You an Agda > Hello, Peano](https://github.com/liamoc/learn-you-an-agda/blob/master/pages/peano.md) for helping me implement this first Agda program.

<a id="hellonumber"></a>
### HelloNumber

A program that prints the number 5.

No more reimplementing silly stuff like numbers. Let's use the standard library.

{% capture code_hello_number %}

```
module HelloNumber where

-- Agda standard library 0.7
open import Data.Nat
open import Data.Nat.Show using (show)
open import Data.Unit using (⊤)
open import IO
import IO.Primitive as Prim

five : ℕ
five = 5

main' : IO ⊤
main' = putStrLn (show five)

main : Prim.IO ⊤
main = run main'
```

{% endcapture %}

{% include accordian/begin %}
    <code>HelloNumber.agda</code>
{% include accordian/middle %}
    {{ code_hello_number | markdownify }}
{% include accordian/end %}

* The [Agda standard library](https://github.com/agda/agda-stdlib/) is not installed with Agda by default. WTF?
    - It also has not yet reached v1.0.
* Standard library IO appears to be defined equivalently to Haskell's IO monad.
* I am amused that compiling the IO module also implies compiling the entirety of Algebra.
* I'm sad that declaration order in Agda matters. In particular items must be declared before they can be used.
    - This forces me to write programs in the annoying bottom-to-top order, requiring lots of extra up-down eye scanning for large programs.
* Surprise! The main function doesn't have type `IO ⊤` (which would be equivalent to the Haskell `IO ()`). Instead it has type `Prim.IO ⊤` which can be obtained by passing an `IO ⊤` through the `IO.run` function.
* Even after installing the standard library, I have to manually compile the IO.FFI library to perform basic IO. \*grumble\*
* My test program that just prints the number 5 takes up 14 MB. What a waste of space...
    - I assume those 14 MB are primarily the bulk added by the standard library.

<a id="helloworld"></a>
### HelloWorld

Now let's try printing strings, which should allow writing the standard "Hello world" program.

{% capture code_hello_world %}

```
module HelloWorld where

-- Agda standard library 0.7
open import Data.String
open import Data.Unit using (⊤)
open import IO
import IO.Primitive as Prim

greeting : String
greeting = "Hello World"

main' : IO ⊤
main' = putStrLn greeting

main : Prim.IO ⊤
main = run main'
```

{% endcapture %}

{% include accordian/begin %}
    <code>HelloWorld.agda</code>
{% include accordian/middle %}
    {{ code_hello_world | markdownify }}
{% include accordian/end %}

* It takes 3 seconds to type-check my Hello World program when compiling to an executable. That's really slow.
    - I hope those 3 seconds are just fixed overhead and not proportional to the size of the program.

<a id="printtwothings"></a>
### PrintTwoThings

Now let's try stringing multiple IO actions together.

{% capture code_print_two_things %}

```
module PrintTwoThings where

-- Agda standard library 0.7
open import Coinduction using (♯_)
open import Data.String
open import Data.Unit using (⊤)
open import IO
import IO.Primitive as Prim

doThis : IO ⊤
doThis = putStr "Everybody say coinductive deep embedding! "

thenThat : IO ⊤
thenThat = putStrLn "Coinductive deep embedding!"

main' : IO ⊤
main' = (♯ doThis) >> (♯ thenThat)

main : Prim.IO ⊤
main = run main'
```

{% endcapture %}

{% include accordian/begin %}
    <code>PrintTwoThings.agda</code>
{% include accordian/middle %}
    {{ code_print_two_things | markdownify }}
{% include accordian/end %}

* Surprise! The `>>` operator used to join two IO actions isn't `IO A -> IO B -> IO B`. Rather it is `∞ (IO A) -> ∞ (IO B) -> IO B`.
    * This means I need to wrap IO actions inside the `∞` type before I can chain them together.
    * What is the `∞` type? No idea. It has something to do with "coinduction", which Wikipedia failed to explain to me coherently.
        - Information [here](http://people.inf.elte.hu/divip/AgdaTutorial/Revise.Coinduction.html) suggests that a `∞ A` represents a lazy unevaluated computation of type `A` that might not terminate when it is actually evaluated.
        - Representing the possibility of nontermination explicitly is probably required since Agda normally requires all of its function definitions to provably terminate.
    * According to the `Coinduction` library, I can make a `∞` using the `♯` operator which takes a value of any type `A` and makes a `∞ A` out of it.
    * Therefore instead of `action1 >> action2` I need `♯ action1 >> ♯ action2`

<!--
#### Interlude: Agda evaluates strictly?

It appears that Agda performs strict evaluation by default. Thus the introducion of the "coinductive" type `∞` to represent potentially infinite computations.

However if this is the case then calling out to Haskell functions through the foreign function interface could get weird since Haskell *is* a lazily evaluation language.
-->

<a id="echoinput"></a>
### EchoInput

Read a line from standard input. Write it back to the screen.

{% capture code_echo_input %}

```
module EchoInput where

-- Agda standard library 0.7
open import Data.String
open import Foreign.Haskell using (Unit)
open import IO.Primitive

postulate
  getLine : IO Costring

{-# COMPILED getLine getLine #-}

doThis : IO Costring
doThis = getLine

thenThat : Costring → IO Unit
thenThat = λ s → putStrLn s

main : IO Unit
main = doThis >>= thenThat
```

{% endcapture %}

{% include accordian/begin %}
    <code>EchoInput.agda</code>
{% include accordian/middle %}
    {{ code_echo_input | markdownify }}
{% include accordian/end %}

* There is no function in the standard library to read from standard input. Nor is there a reference to `stdin` itself. Unbelievable.
    - I can [define getLine manually](http://people.inf.elte.hu/divip/AgdaTutorial/Revise.IO.html) using the foreign function interface. But I really shouldn't have to define such a simple function. This should be in the standard library...
* When writing native IO functions it's a lot easier to directly use Agda's `Primitive.IO` module instead of the regular `IO` module. I no longer need to use `∞` or `♯` either, which is nice.

<a id="promptforname"></a>
### PromptForName

{% capture code_prompt_for_name %}

```
module PromptForName where

-- Agda standard library 0.7
open import Data.String
open import Foreign.Haskell using (Unit)
open import IO.Primitive

postulate
  getLine : IO Costring

{-# COMPILED getLine getLine #-}

main : IO Unit
main = 
  putStrLn (toCostring "What's your name?") >>= (λ _ → 
  getLine >>= (λ s → 
  putStr (toCostring "Hello ") >>= (λ _ → 
  putStrLn s)))
```

{% endcapture %}

{% include accordian/begin %}
    <code>PromptForName.agda</code>
{% include accordian/middle %}
    {{ code_prompt_for_name | markdownify }}
{% include accordian/end %}

* Surprise! `Primitive.IO` defines the `>>=` operator but not `>>`. Asymmetric with the regular `IO` module.
* Native IO functions require `Costring` objects. So a string literal has to be passed to `toCostring` to be used.

<a id="echoinputreverse"></a>
### EchoInputReverse

Read a line from standard input. Reverse it in Agda. Write the reversed line back to the screen.

{% capture code_echo_input_reverse %}

```
module EchoInputReverse where

-- Agda standard library 0.7
open import Data.List using (reverse)
open import Data.String
open import Foreign.Haskell using (Unit)
open import IO.Primitive

postulate
  getLine : IO String

{-# COMPILED getLine getLine #-}

main : IO Unit
main = 
  getLine >>= (λ s → 
  return (toCostring (fromList (reverse (toList s)))) >>= (λ s' → 
  putStrLn s'))
```

{% endcapture %}

{% include accordian/begin %}
    <code>EchoInputReverse.agda</code>
{% include accordian/middle %}
    {{ code_echo_input_reverse | markdownify }}
{% include accordian/end %}

* Problem: The line from standard input is a `Costring`. I can't reverse it or do anything useful with it without first converting it to a `String`. But there is no function in the standard library to do this conversion, even as a runtime cast.
* Surprise workaround: Even though the Haskell type `String` maps to the Agda type `Costring` in the general case, it is still possible to postulate that it maps directly to the Agda type `String` for certain functions where you can assert that the string won't be infinite.
    * So the Agda FFI must be capable of performing implicit coercion between the native `Costring` and `String` datatypes. This is [not documented](http://wiki.portal.chalmers.se/agda/agda.php?n=Docs.FFI).
    * This approach has the disadvantage that it marks the result of `getLine` as being a *finite* string when it may not in fact be. See discussion at [StackOverflow](http://stackoverflow.com/questions/21808186/reading-a-line-of-standard-input-as-a-string-instead-of-a-costring/).

<a id="parseint"></a>
### ParseInt

Prompt the user for a number, parse it, and output it. If an invalid number was input, output zero.

{% capture code_parse_int %}

```
module ParseInt where

-- Agda standard library 0.7
open import Data.Char
open import Data.List
open import Data.Maybe
open import Data.Nat
open import Data.Nat.Show
open import Data.String
open import Foreign.Haskell using (Unit)
open import IO.Primitive

postulate
  getLine : IO String

{-# COMPILED getLine getLine #-}

parseInt : String → Maybe ℕ
parseInt s = 
  then? (unwrap (parseDigits s)) (λ s' → 
  just (digitsToℕ s'))
  where
    parseDigits : String → List (Maybe ℕ)
    parseDigits s = map toDigit (toList s) where
      toDigit : Char → Maybe ℕ
      toDigit '0' = just 0
      toDigit '1' = just 1
      toDigit '2' = just 2
      toDigit '3' = just 3
      toDigit '4' = just 4
      toDigit '5' = just 5
      toDigit '6' = just 6
      toDigit '7' = just 7
      toDigit '8' = just 8
      toDigit '9' = just 9
      toDigit _   = nothing

    -- TODO: There's probably a standard-library function that does this
    --       but I can't find it.
    unwrap : List (Maybe ℕ) → Maybe (List ℕ)
    unwrap xs = unwrap' (just []) xs where
      unwrap' : Maybe (List ℕ) → List (Maybe ℕ) → Maybe (List ℕ)
      unwrap' (just xs) (just y ∷ ys) = unwrap' (just (Data.List._++_ xs [ y ])) ys  -- makes unwrap O(N^2)!
      unwrap' (just xs) (nothing ∷ _) = nothing
      unwrap' (just xs) []            = just xs
      unwrap' nothing   _             = nothing
    
    -- TODO: Look for a monadic _>>=_ that does the same thing
    then? : {A : Set} → {B : Set} → Maybe A → (A → Maybe B) → Maybe B
    then? nothing _ = nothing
    then? (just r1) op2 = op2 r1
    
    digitsToℕ : List ℕ → ℕ
    digitsToℕ xs = digitsToℕ' (reverse xs) where
      digitsToℕ' : List ℕ → ℕ
      digitsToℕ' []       = 0
      digitsToℕ' (x ∷ xs) = x + (10 * (digitsToℕ' xs))

ℕ? : Maybe ℕ -> ℕ
ℕ? (just x) = x
ℕ? nothing  = 0

main : IO Unit
main = 
  getLine >>= (λ s → 
  return (show (ℕ? (parseInt s))) >>= (λ s' → 
  putStrLn (toCostring s')))
```

{% endcapture %}

{% include accordian/begin %}
    <code>ParseInt.agda</code>
{% include accordian/middle %}
    {{ code_parse_int | markdownify }}
{% include accordian/end %}

* Agda type checking errors are really hard to read:
    * Actual:
      
      ```
      List Char !=< _A_10 s → _B_11 s of type Set
      when checking that the expression toList s has type
      _A_10 s → _B_11 s
      ```
    * Better:
      
      ```
      Expected type (A → B) but found type (List Char).
      ```
* Agda's `show` function that converts a natural number to a string has quadratic performance!
    * It takes 0.3s to print 1000, 2.2s to print 2000, 6.9s to print 3000, and 15.9s to print 4000.
    * This is crazy! It probably means that at least one of {`+`, `*`, `mod`} is not constant time. Not cool.
        * Indeed the `_divMod_` operator runs in *linear* time with respect to the magnitude of the dividend. Madness.

* Surprise! Equality comparison between two numbers is not `=` or `==` but rather `≟`.
    * It doesn't return a `Bool` either. Instead it returns a fancy boolean called a `Decidable` with an embedded equality proof.
    * A `Decidable` can be converted to a regular boolean with the `⌊_⌋` operator. Weird.
* I suspect that (arbitrary precision) natural numbers from `Data.Nat` take *linear* memory to represent rather than *logarithmic*.
    * There is `Data.Bin` which represents natural numbers using binary, but most of the standard library doesn't use it.

{% endcapture %}
{{ content_with_bullets | fixbullets }}