---
layout: post
title: "Programming for Perfectionists (P4P): A Book Outline"
tags: [Software]
featured: true
x_date_written: 2013-05-05

style: |
  /* Make inline links extra obvious */
  .post a:link { text-decoration: underline; }

---

I've read a lot of programming books. Many focus on teaching a particular language or tool, or are for teaching beginner developers the ropes. Precious few are designed to bring intermediate developers up to an advanced level. It's time to change that.

Here is an outline of a book I would like to write. I will probably try writing some of these sections and chapters as future article posts. When that happens, each section below will be replaced with a link to the associated article.

"Programming for Perfectionists" is the working title for the book and may be revised later.

{% capture toc_content %}

* [Introduction](#introduction)
* [Fundamentals](#fundamentals)
    * [Representations](#representations)
        * [Numbers](#numbers)
        * [Text](#text)
        * [Color](#color)
        * [Pictures](#pictures)
        * [Sound](#sound)
        * [Time](#time)
        * [Video](#video)
    * [Collections](#collections)
    * [Error Handling](#error-handling)
    * [Concurrency](#concurrency)
    * [Memory Management](#memory-management)
* [Languages](#languages)
    * [Comparing Programming Languages](#comparing-programming-languages)
    * [Programming Paradigms](#programming-paradigms)
* [Process](#process)
    * [Collaborative Software Development](#collaborative-software-development)
    * [Code Conventions](#code-conventions)
    * [Communicating Software Designs](#communicating-software-designs)
    * [Detecting Defects Early (Testing)](#detecting-defects-early)
    * [Improving Code Quality (Basic Refactoring)](#improving-code-quality)
    * [Debugging Techniques](#debugging-techniques)
    * [Profiling/Instrumentation](#profiling-instrumentation)
    * [Maintaining Legacy Code Safely (Advanced Refactoring)](#maintaining-legacy-code-safely)
* [Other](#other)
    * [Persistence](#persistence)
* [Comments?](#comments)
* [Progress](#progress)

{% endcapture %}

<div class="toc">
  {{ toc_content | markdownify }}
</div>

<a id="introduction"></a>
## Introduction

The purpose of this book is to provide a *wide and shallow* overview of important concepts in real-world software development. As such the treatment of various topics will not be comprehensive. Entire books have been written on the topic of each chapter, and appropriate references will be provided where appropriate.

This book will not teach specific tools, languages, or programs in depth. It deals in concepts and patterns. However references to specific tools and languages will be provided liberally in concrete examples.

Many concepts presented here are ones that I feel are missing from the traditional "computer science" curriculum, yet which I feel to be vital to understand when working with real-world software.

<a id="fundamentals"></a>
## Fundamentals

<a id="representations"></a>
### Representations

Many developers do not understand the common ways of representing various kinds of real-world data, such as text, integers, color, and time. This leads to errors such as munging of international characters, integer overflow vulnerabilities, ignorance of color correction, and bugs that only trigger at midnight on leap years.

* <a id="numbers"></a>**Numbers**
    * Integers
        * Fixed-precision 2's complement
        * Arbitrary Precision Integers
    * Decimals
        * Floating Point
        * Fixed Point
* <a id="text"></a>[**Text**](/articles/2013/06/01/handling-text-correctly/)
    * Characters and Codepoints
    * Text Encodings
        * "ANSI"
    * Unicode, UTF-8, UCS-2, UTF-16
        * Basic Multilingual Plane, Astral Characters
        * BOM        
    * "Characters" and "Strings" in popular programming languages
    * Line-ending sequences
* <a id="color"></a>**Color**
    * Color Models, "RGB", Colorspaces, CIE, Gamma
* <a id="pictures"></a>**Pictures**
    * Resolution
        * Magic: 72 dpi and 96 dpi
        * Resolution Independence
        * Pixel Doubling
    * Non-Square Pixels (ex: NTSC)
    * Anamorphic Projections
* <a id="sound"></a>**Sound**
* <a id="time"></a>**Time**
* <a id="video"></a>**Video**

<a id="collections"></a>
### Collections

Collections are the backbone for representing compound data in any programming language. Specific implementations are covered in great detail in most any traditional CS textbook. However there are a number of more advanced collections which are useful for tough problems.

* **Basic Collections**
    * Arrays
        * Bit Vectors
    * Lists
        * Array lists
        * Linked lists
        * Linked lists of arbitrary objects
    * Sets
        * Hash set
        * Linked hash set
    * Sorted Sets
        * Red & black trees
        * Heaps
    * Maps
* **Advanced Collections**
    * Bags
        * Counted Bags
        * Partitioning Bags
    * Multimaps
    * Bidi Multimaps
* **Advanced Data Structures**
    * Trees
    * Graphs (including: directed, multi)

<a id="error-handling"></a>
### [Error Handling](/articles/2013/07/13/error-handling/)

There are many more ways for a program to fail than succeed.

* **Signaling (Error Codes vs. Exceptions vs. Sentinels)**
    * Sentinels - null, 0, -1, false
* **Guarantees after failure**
    * In original state (Atomic, Transactional)
    * In different but valid state
    * In different and potentially illegal state
* **Behaviors upon failure**
    * Delegate to caller
    * Handle internally
        * Aside: Minix is the extreme of this approach.
    * Exit program
        * Linux Kernel: panic()
        * Python, PHP: die()
    * Display to user
* **Error Locality & Failing Fast**
    * Assertions
* **Designing Error Messages**
* **Error Seriousness**
    * Expected - `Exception`
    * Unexpected - `RuntimeException`
    * Fatal - `Error` (esp. `OutOfMemoryError`)
        * Aside: Certain programs are actually designed to handle OOM errors (ex: SQLite). Most are not.

Bonus:

* **Checked Exceptions**
* **Exception Wrapping**

<a id="concurrency"></a>
### Concurrency

Early languages like C pretend that threads don't even exist. And even amidst the multi-core systems today, many programmers would like to pretend that concurrent execution doesn't exist. A huge number of concurrency-related bugs are found in production code today.

Many developers are familiar with the "shared memory & locks" model used by most mainstream programming languages for working with concurrency. This model unfortunately makes it very easy to introduce bugs, and these bugs are often difficult to detect since they depend on the precise ordering of randomly-ordered events. Deadlocks and livelocks also lurk to trip the unwary. This and other more-robust models will be presented here.

* **Terminology**
    * Processes, Threads, and Green Threads
    * Concurrency vs. Parallelism
* **Shared Memory & Locks Model**
    * Thread Safe vs. Thread Unsafe vs. Thread Hostile
    * Deadlocks, Livelocks, and Lock Hierarchies
* **Apartment Threading**
    * Thread Affinity
    * Run Loops
* **Actor Model**
* **Immutability**
    * Read-Copy-Update

<a id="memory-management"></a>
### Memory Management

Tradeoffs should be described for each of the following:

* **Manual Memory Management**
    * Ownership - "Own & Borrow" Model
    * Hierarchy, Composites vs. Aggregates
* **Reference Counting**
    * Automatic Reference Counting
* **Garbage Collection**
    * Generational Collectors
    * Mark & Sweep

Bonus:

* **Special-Purpose Memory Allocators** (to reduce calls to system's malloc)
    * Slab Allocaters

<a id="languages"></a>
## Languages

<a id="comparing-programming-languages"></a>
### Comparing Programming Languages <small>(The Right Tool for the Right Job)</small>

A programming language is a tool for getting work done. Some tools are better at certain tasks than others. Thus picking your tool wisely for the task at hand will save you effort down the road.

It should also be noted that a programming language does not stand alone; it comes with an entire ecosystem of tools and people along with it. Such ecosystems often cater to a particular domain and make it easier to work with programs in that domain.[^ruby_ecosystem]

* **Native Development (Desktop, Mobile, and Embedded)**
    * C/C++ - lingua franca; easiest to bind to OS; hand-optimized performance-critical code
    * Java - rich cross-platform development (including GUIs); server programming
    * Python - rich cross-platform CLI scripting; text & data processing
    * C# - rich Windows app programming
    * Objective-C - native OS X development; native iOS development
    * PowerShell - Windows CLI scripting
* **Web Development (Server-Side)**
    * PHP - web application prototyping; most widely deployed server-side scripting language
        * Java & JSP - Java's clone of PHP
        * C# & ASP.NET - Microsoft's clone of PHP
    * Ruby & Ruby on Rails - bleeding-edge full-stack web framework
    * Python & Django - mature full-stack web framework; rapid development; excellent ORM
    * Python & web2py - mature full-stack web framework
        * Anecdotal evidence suggests PHP refugees prefer web2py over Django,
          probably because it uses implicit behavior (i.e. magic) to avoid boilerplate.
          In contrast Django's philosophy is "explicit is better than implicit",
          which is more in line with general Python philosophy.
    * Python & (lots of choices) - lightweight web framework; for maximum control
        * Pyramid
        * Flask
        * web.py
        * CherryPy
* **Web Development (Client-Side)**
    * HTML, CSS, JavaScript - assembly languages
    * Haml, Sass, CoffeeScript - 2nd-order languages
* **Special-Purpose Languages**
    * Fortran - high-performance numerical programming
    * Lua - embedded game programming (ex: game mods, AIs)
    * Lisp (Racket) - academic programming<sup>AcadProg</sup>; dynamic; great for embedded DSLs
    * Haskell - academic programming<sup>AcadProg</sup>; static; better compile-time safety than any mainstream language

<span style="font-variant: small-caps;">AcadProg</span>: This language tends to be used in academia, especially by programming language researchers. Thus it also gets various cutting-edge programming language features before mainstream languages.

[^ruby_ecosystem]: For example, the early appearance of the Ruby on Rails web framework in the Ruby language caused a lot of the Ruby ecosystem to cater to web development needs. Subsequently Ruby gained the "move fast and break things" web mentality, along with the necessary tooling to support that mentality: heavy-duty testing, continuous integration, semantic versioning, package management, etc.

<a id="programming-paradigms"></a>
### Programming Paradigms <small>(Ideas that Change the World)</small>

*The following paradigms are presented in chronological order by their recognition in the wider programming community.*

* **(Ye Olde) Structured Programming (ALGOL)**
    * ban `goto` &ndash; GOTO Considered Harmful
    * single entry, single exit
* **Declarative Programming (Prolog, SQL, and other DSLs)**
    * "Tell me what you want to do and I'll figure out how to actually do it."
* **Object-Oriented Programming (Smalltalk & Java)**
    * Decomposing the behavior of a large system into smart modules that interact with each other through interfaces.
* **Functional Programming (Lisp & Haskell)**
    * Higher-order functions.
    * Building complex data structures out of simple primitive collections (especially lists).
    * Constrained side effects.

<a id="process"></a>
## Process

<a id="collaborative-software-development"></a>
### Collaborative Software Development

* **Open Source**
    * Stand on the shoulders of giants. Learn new techniques.
    * Work on projects you're passionate about.
    * Start your own projects to get free development resources from the community.
* **Version Control Systems**
    * Centralized (CVS, SVN, Perforce)
    * Distributed (Git, Mercurial)
    * Patches - create, view, apply, submit
* **Automated Build Systems**
    * configure, make (C<wbr/>)
    * Ant (Java)
    * Rake (Ruby)
* **Dependency Management**
    * Versioning
        * Semantic Versioning
    * Package Managers, Environment Isolators

<a id="code-conventions"></a>
### Code Conventions

* **Philosophy**
    * Clarity is paramount.
    * Consistency is a close second.
* **Indentation**
    * 2 columns vs. 4 columns
    * Tabs vs. spaces
* **80 column lines** (or max 100)
* **Brace positioning** (when applicable)
* **Whitespace around operators**
* **Method ordering and grouping**
* **Blank lines and paragraphs**

<a id="communicating-software-designs"></a>
### Communicating Software Designs <small>(UML & Other Diagrammatic Notations)</small>

*Most of the following diagram notations assume the use of object-oriented programming. Non-OO languages do not have any standard diagram types, to my knowledge.*

* **(Ye Olde) Flow Chart**
* **Class Diagrams**
* **State Charts**
* **Sequence & Communication Diagrams**
* **Use Cases (Fully Dressed)**
* **CRC Cards** (designing classes with responsibilities in mind)

<a id="detecting-defects-early"></a>
### Detecting Defects Early <small>(Testing)</small>

* **Unit Testing, Code Coverage, Continuous Integration**
* **Static Analysis**
    * Compiler
        * Strong static typing
        * Enabling extra warnings (`-Wall`, `-Weverything`, `-Werror`)
    * Lint
* **Dynamic Analysis**
    * Valgrind
    * Fault Injection
* **Test Matrixes, Environment Isolators, Virtual Machines**
* **"Large Hammers"**
    * Fuzzing
    * Stress Testing
    * Longhaul Testing
    * (many more)

<a id="improving-code-quality"></a>
### Improving Code Quality <small>(Basic Refactoring)</small>

Transforming the structure of existing code to improve it while maintaining its original behavior is a process called refactoring. Regularly applying refactoring to your code will greatly extend its maintainable life.

* **Rename Method or Variable**
* **Extract Method**
* **Introduce Explaining Variable**
* **Replace Magic Number with Symbolic Constant**
* **Replace Nested Conditional with Guard Clauses**

Meta:

* Duplication is the root of all evil.
* Prefer delegation over inheritance.
* Prefer interfaces over abstract classes.

<a id="debugging-techniques"></a>
### Debugging Techniques <small>(When It Breaks)</small>

No program is perfect. Even if one were, requirement changes will break it soon enough.

* **Print Statements, Logging**
* **Debuggers**
    * Breakpoints, Catchpoints
    * Conditional Breakpoints & Watching variables
* **Heap Analyzers**

<a id="profiling-instrumentation"></a>
### Profiling/Instrumentation <small>(Making It Faster)</small>

Meta:

* Premature optimization is frequently a waste of time.
    * Programmer time is more valuable that machine time.
    * Algorithm choice has a larger impact on performance than almost any manual tweaking.

<a id="maintaining-legacy-code-safely"></a>
### Maintaining Legacy Code Safely <small>(Advanced Refactoring)</small>

*Although the concept of refactoring can be applied to any code, not just legacy code, the *deliberate and careful* application of refactoring techniques is mostly restricted to legacy code.*

*This is covered in great detail in the "Refactoring" book by Martin Fowler.*


<a id="other"></a>
## Other

The topics in this section don't fit in any of the other major topics. Should these extra topics not form a cohesive whole, they will not be included in the book.

<a id="persistence"></a>
### Persistence

* Prefer the use of a standard metaformat instead of rolling your own format.  
  You'll save a ton of time.
* **Standard Metaformats**
    * XML
    * JSON
    * YAML
    * Config files
        * UNIX config file
        * Windows INI file
        * Mac Plist file
    * SQLite database
* **Considerations with custom formats**:
    * Text vs. Binary
    * Backward Compatibility, Forward Compatibility, Version Numbers
    * Extensibility
    * In-place Modifications & Appendability
        - For text formats, this means the preservation of comments and whitespace.
    * Partially-loadable
* **Examples of custom formats**:
    * Hotline protocol - highly extensible, featureful, binary protocol
    * Mac resource fork format - partially-loadable appendable binary file format
    * QuickTime video container - highly extensible binary file format
    * Matroska video container - highly extensible binary file format
    * ZIP file format
* **Bundles** - a means for combining multiple subfiles into a single virtual file

<a id="comments"></a>
## Comments?

Does any of this content sound interesting to you? If so, [drop me a line]. I may add/remove content and/or modify the order that I write the chapters based on feedback.

<a id="progress"></a>
## Progress

* **2013-07-13**: Added the [Error Handling](/articles/2013/07/13/error-handling/) chapter.
* **2013-06-01**: Added the [Text](/articles/2013/06/01/handling-text-correctly/) chapter.

[drop me a line]: /contact/