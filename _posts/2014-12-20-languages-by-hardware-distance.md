---
layout: post
title: Spectrum of Languages by Hardware&nbsp;Distance
tags: [Software]

include_jquery: true
include_bootstrap_js: true

full_width: true

style: |
    /* Add space between the diagram bottom and the following text */
    #spectrum-diagram { margin-bottom: 1em; }

---
{% capture content_with_bullets %}

Programming languages (and the ecosystems that surround them) are incredibly interesting. They can be sliced in many different ways based on syntactic similarity, type system similarity, suitedness for various problem domains, and many other attributes.

Below I present an spectrum of various languages, arranged by **distance from the underlying hardware**[^hw-dist]:

<ul class="nav nav-tabs">
  <li class="active">
    <a href="#diagram-tldr" class="tab-header" data-toggle="tab">
      TLDR
    </a>
  </li>
  <li class="">
    <a href="#diagram-full" class="tab-header" data-toggle="tab">
      Full
    </a>
  </li>
</ul>
<div class="tab-content" id="spectrum-diagram">
  <img class="tab-pane active" id="diagram-tldr" src="/assets/2014/hardware-distance/tldr-125perc-72dpi.png" />
  <img class="tab-pane"        id="diagram-full" src="/assets/2014/hardware-distance/full-100perc-72dpi.png" />
</div>

A few interesting patterns become evident in this diagram:

* **Expressiveness <span title="is proportional to" style="cursor: help">∝</span> Distance from Hardware**
    * Usually the closer you are to the hardware, the more you have to think like a computer and less like a human, decreasing expressiveness.
    * There are some outlier languages (such as Go, Lua, and Forth) which are more expressive than their distance from the hardware would suggest.

* **Type systems tend to be similar for languages with similar hardware-distance.**
    * Bare Metal languages like machine code and assembly have no type system at all. Every piece of data is just a machine word and no type checking is done at all.
    * Almost Bare Metal languages like C and C++ have a type system that is just strong enough to tell the compiler how to compile operations efficiently, but these type systems are not specifically designed for the elimination of bugs or expressiveness.
    * High Level languages care more about expressiveness, and they tend to divide into two camps: **statically-typed** (Java, C#) and **dynamically-typed** (Python, Ruby, Lisps).
    * Anything that is Intermediate Typed or below has a stronger focus on the type system, usually for preventing bugs or just having very precise types.

* **"PhD required below this line"**
    * I have observed generally two large groups of people that work with programming languages, the **Practitioners** and the **Academics**. Each group uses their own specialized jargon[^jargon] and tends not to talk to each other that much.
    * Languages inside the "PhD required below this line" area are generally used primarily by Academics, and therefore their documentation (often only in the form of research papers) is difficult to read by Practitioners.
    * I currently group myself as a Practitioner who is trying to read Academic.
    * Of course some so-called Academic languages are sometimes used in practice for commercial systems. The Java bytecode verifier, for example, is defined in Prolog.
    * Many languages in or near this region are lumped under the vague term **functional programming**, which roughly translates to a programming style that avoids mutable data structures & side effects by default, or just "a language that feels like Haskell" (the canonical "functional" language).

* **Middle of the spectrum = Sweet spot**
    * There are a quite a lot of languages in the middle layers (High Level and Intermediate Typed). Probably because they intersect most with expressive languages, which are the most fun to program in.
    * Programming near the hardware is unfun and generally unnecessary unless you're writing an OS, an embedded system, a CPU-intensive scientific computation, or a graphics shader.
    * I suspect there aren't as many languages at the bottom in Academic-land because there are fewer Academics than Practitioners, such languages are harder to write (because of more complex type systems), or because I simply am not aware of many such languages as a non-Academic.

* **Declarative Languages that are general-purpose are rare.**
    * Most Declarative Languages are domain-specific. Arguably Prolog is general since it answers arbitrary questions from logic. And arguably SQL is general because most data stores (and every SQL database) is queryable with it.
    * Other examples of declarative languages not listed here are VHDL and Verilog (used for hardware design), and ReceiptTally[^rt] (used for personal finance).

[^hw-dist]: When speaking of "hardware distance", the hardware I am referring to is the common commodity hardware architectures such as x86 and ARM. It should be noted that there are also specialized architectures where Forth, Lisp, and Prolog *are* the assembly language. And some architectures like the Burroughs actually have typed memory and pointers, which eliminates a lot of the dangers of working with untyped assembly.

[^jargon]: Examples of Practitioner-jargon: "inheritance", "generics", "dependency injection", "covariance". Examples of Academic-jargon: "monad", "functor", "reduce", "dependent type", "currying". More examples from this [presentation on functional programming](http://www.slideshare.net/ScottWlaschin/fp-patterns-buildstufflt/10).

[^rt]: ReceiptTally is a custom language of my own designed to describe household receipts. With this description it can be calculated who owes whom money for reimbursement purposes. I haven't bothered to make this project public at this time.


### *Related Articles*

* [Visual Guide to Programming Language Properties](/articles/2013/02/20/visual-guide-to-programming-language-properties/)
    * *Shows programming language features, how they are related, and which features are present in popular languages.*
    * *Visualizes some of the languages discussed in this article.*
* [Unique Features of Various Programming Languages](/articles/2013/01/29/unique-features-of-various-programming-languages/)
    * *Discusses several programming languages and their unique features.*

{% endcapture %}
{{ content_with_bullets | fixbullets }}


 