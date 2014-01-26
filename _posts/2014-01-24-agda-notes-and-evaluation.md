---
layout: post
title: "Agda: First Impressions"
tags: [Software]

---
{% capture content_with_bullets %}

These are my first impressions of the Agda programming language after researching it in some depth but before writing any actual Agda programs.

If you only want the highlights, just read the [Executive Summary](#executive-summary). If you also want to see supporting material and notes, continue reading further.

{% capture toc_content %}

* [Executive Summary](#executive-summary)
* [Getting Started](#getting-started)
* [Environment](#environment)
* [Libraries](#libraries)
* [Papers](#papers)
* [Books](#books)
* [Other Resources](#other-resources)

{% endcapture %}

<div class="toc">
  {{ toc_content | markdownify }}
</div>

<a id="executive-summary"></a>
## Executive Summary

Agda, by virtue of it possessing a *dependent type system*, makes it a very powerful programming language. Agda is distinguished from its cousins like Coq in that it makes more of an effort at being a *programming language* as opposed to being merely a proof assistant. Certainly worthy of study for the purpose of learning what a truly powerful type system is capable of expressing.

However Agda I judge to not presently be worthy as a full production-quality programming language, suitable for long term development. My reasons:

* Agda lacks a package manager
    - Acts as a barrier for the creation of 3rd party libraries.
      A language cannot be used effectively without 3rd party libraries.
    - Library discoverability is also impaired.

* The standard library has a version number less than 1.0, namely 0.7.
    - A lack of a forward-compatibility promise from the standard library
      is not acceptable for long term development.

* I can find no books about Agda development, let alone *real-world*
  Agda development.

Other tripping points:

* Agda does not have a (traditional-style) documentation generator tool,
  which discourages somewhat the creation of API documentation and
  especially the creation of guide-level documentation.
    - Agda API documentation is instead issued via hyperlinked versions
      of Agda source code, which appear to emulate the Agda Emacs mode
      that Agda is traditionally developed with.
    - Such API documentation *can* be used effectively but it is not the
      format that the larger programming community expects (i.e. styled
      HTML) and is lacking in aesthetic appeal.

* Agda only appears to have integration with the Emacs code editor.
  In particular there is no obvious integration with any GUI code editors,
  like Sublime Text. And such editor integration is *necessary* at minimum
  for the Unicode-style input that Agda requires.

* Agda's main website and "marketing" has very little polish.
    - It's a shame that this matters, but it makes Agda appear unfinished
      and not ready for prime time. In practice this will scare away users.
    - The main website, for example, is just a stock wiki.
    - Agda has no logo.

I expect that many of these shortcomings will be addressed over time.

In the meantime, as I mentioned before, I think Agda is still worthy of investigation for expanding one's knowledge of what is possible in a powerful type system. In fact, any language where you can do something like write a sorting function that both works and proves itself to be a correct implementation in the same stroke deserves a closer look.[^sort]

[^sort]: <p>I forget the specific tutorial where I first recognized that you could write this kind of provably correct sorting function. You end up having a sorting function with a signature like `sort : (inList : List a) -> (outList : List a, IsSorted outList, EqElements inList outList)`.</p> <p>The `IsSorted outList` type represents proofs that `outList` is sorted. Thus the existence of a member of the `IsSorted outList` type proves that `outList` is sorted. Similarly the `EqElements inList outList` is a proof type where `inList` and `outList` are proven to have equal elements.</p>


<a id="getting-started"></a>
## Getting Started

Official website of Agda is <http://wiki.portal.chalmers.se/agda/pmwiki.php>:

- Yes, it's a wiki. Automatically lowers the quality. :-(
- (1) "Agda is a dependently typed functional programming language."
- (2) "Agda is a proof assistant."

Uses Unicode operators all over the place. Nice to read. Tricky to type. Even library developers use them.


<a id="environment"></a>
## Environment

Has 3 backends: Haskell, JavaScript, and Epic

* Only the Haskell one should be taken seriously, since the
  latest version of the standard library (0.7) only supports
  the Haskell backend.

Agda should not be used on Windows. None of the core release maintainers run Windows.[^no-windows]

Strongly expects that you use Emacs, as Agda provides its own interactive Emacs mode.

[^no-windows]: None of the people who currently release Agda are running Windows according to the latest [Agda Implementors' Meeting](http://wiki.portal.chalmers.se/agda/pmwiki.php?n=Main.AIMXVIII).


<a id="libraries"></a>
## Libraries

Apparently the Agda community is sufficiently small that all libraries (of significance?) can be listed comfortably on the main Agda website at <http://wiki.portal.chalmers.se/agda/pmwiki.php?n=Main.Libraries>.

* Informal sampling shows several libraries to be outdated,
  not updated within the last 2 years.
* Therefore the number of actual *usable* up-to-date libraries
  is expected to be quite small, in the 4-7 range. Not promising.

Only two libraries under the <https://github.com/agda> umbrella have been updated within the last year. One of them is the Agda standard library. Not a good sign of activity.

Libraries do not carry external documentation. Instead all documentation is within the source code itself. The expectation is that you will use the Agda emacs mode to jump around between modules and explore to find what you want. Not ideal but serviceable.

* There seems to be some tool used to compile HTML that acts like the
  Agda Emacs mode. In particular hyperlinking between modules is
  supported.

Readers of the documentation are assumed to have high mathematical training. I see terms like "communative semiring", "coinductive", "lemma", and "decidable".

### [agda-frp-js](https://github.com/agda/agda-frp-js) <small>(last activity 2 years ago)</small>

This is an FRP implementation in Agda. I'll look at it because I've been working in FRP systems recently (i.e. Elm). And because I'd like to see how well libraries are packaged by the Agda community.

"Beh" is short for "behavior" and is equivalent to an Elm Signal.

I note that there is no API documentation whatsoever for the module. You have to browse through the examples in the source tree manually. This suggests that either Agda has no doc generator tool (likely!) or this library author simply didn't bother to generate docs for the public to read.

Virtually no comments.

Has own definition of Bool (booleans), RSet (function types), Int (integer types), and possibly other super primitive notions. This appears to be related to the use of the JavaScript backend, as most of these primitives have native JS code defined for many of these definitions.

### [agda-frp-ltl](https://github.com/agda/agda-frp-ltl) <small>(last activity 2 years ago)</small>

Not going to look at this closely due to the lack of activity.


<a id="papers"></a>
## Papers

Agda is used in quite a number of academic papers. Certainly more papers than actual libraries, so far as I can tell. There's a whole [list of papers that use Agda](http://wiki.portal.chalmers.se/agda/pmwiki.php?n=Main.PapersUsingAgda).

### [Safe Functional Reactive Programming through Dependent Types (2009)](http://ivanych.net/doc/SafeFunctionalProgrammingDependentTypes.pdf)

Describes an FRP system that is slightly more powerful than that of Yampa. It defines a type system around FRP that guarantees that FRP programs written within the type system will necessarily continue to make progress (i.e. not deadlock). (It is possible for an FRP system to deadlock if its signal graph get reconfigured into certain kinds of loops.) It also eliminates the distinction between continuous and discrete signals, reducing one class of errors. Furthermore it allows programs to include feedback loops and uninitialised signals in an FRP program, whilst guaranteeing evaluation progress at the type level.


<a id="books"></a>
## Books

Hard to find books on Agda. I get nothing.

However I do see some [books on Coq](http://stackoverflow.com/questions/13796557/books-about-coq), which Agda is inspired by. Let's not get distracted by those at the moment.


<a id="other-resources"></a>
## Other Resources

* [Dependently Typed Programming in Agda (2008)](http://www.cse.chalmers.se/~ulfn/papers/afp08/tutorial.pdf)
    - Appears to be the original paper that introduced the Agda
      programming language. Or at the very least a fairly complete
      description of the language along with tutorial-style content.

* [The Power of Pi (2008)](http://www.staff.science.uu.nl/~swier004/Publications/ThePowerOfPi.pdf)
    - Despite the indescriptive name, promises to show a number of design
      patterns and techniques that apply to dependently types languages,
      particularly Agda.
    - "Dependent types matter. And not just for program verification
       and proof assistants: dependent types matter to programmers."
    - "This paper demonstrates how to program with dependent types.
       In particular, we present three case studies.
       Each case study describes a domain-specific language that is
       difficult to embed in conventional functional languages such
       as Haskell."
    - "design patterns of dependently-typed programming"
    - "domain-specific embedded type systems"

* [Brutal (Meta)Introduction to Dependent Types in Agda](http://oxij.org/note/BrutalDepTypes/)
    - Aims to describe at a high-level how dependently typed languages
      work at the level of theory, without going into too many
      details. Uses Agda as a concrete language to work with.

* [Learn You an Agda](https://github.com/liamoc/learn-you-an-agda/blob/master/pages/introduction.md)
    - Already read this. Good high level introduction to the *promise*
      (or taste) of what's possible in dependently typed languages.
    - Difficult to browse, since the rendered HTML of these markdown
      pages fell off the internet a while ago.

{% endcapture %}
{{ content_with_bullets | fixbullets }}