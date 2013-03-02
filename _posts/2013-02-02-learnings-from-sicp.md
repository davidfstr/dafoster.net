---
layout: post
title: Learnings from SICP (and Lisp)
tags: [Software]

---

<img src="/assets/2013/sicp_cover.jpg"
  alt="Cover of The Structure and Interpretation of Computer Programs"
  style="float: right;"
  width="170" height="246" />

Recently I took the liberty of reading one of the defining books in the domain of computer science: [The Structure and Interpretation of Computer Programs][sicp], often abbreviated as SICP.

SICP is the computer science textbook given to undergraduates at MIT. It serves as an advanced text on software design and as an introductory text for the Lisp programming language.

Here are some interesting things I learned:

<div class="toc">
  <ul>
    <li><a href="#role-of-programming-languages">Role of Programming Languages</a></li>
    <li><a href="#abstract-data-types">Abstract Data Types</a></li>
    <ul>
      <li><a href="#lisp-vs-pascal-design-philosophies">Lisp vs. Pascal Design Philosophies</a></li>
      <li><a href="#polymorphism">Polymorphism</a></li>
      <li><a href="#cross-type-operations">Cross-Type Operations</a></li>
    </ul>
    <li><a href="#assignments-mutable-state-and-side-effects">Assignments, Mutable State, and Side Effects</a></li>
    <ul>
      <li><a href="#lazy-evaluation">Lazy Evaluation</a></li>
    </ul>
    <li><a href="#declarative-languages">Declarative Languages</a></li>
    <li><a href="#conclusion">Conclusion</a></li>
  </ul>
</div>

[sicp]: http://mitpress.mit.edu/sicp/

<a id="role-of-programming-languages"></a>
## Role of Programming Languages

Languages should:

* provide the means for **combining simple ideas to form complex ideas**,
* provide the means for **abstracting units of computation**, and
* serve as a framework within which we **organize our ideas about processes**.

Units of computation can be abstracted in several forms:

* **procedure** - *Assigns names to common patterns, allowing you to work in terms of the named abstractions directly.*
    * AKA function, method
* **abstract data type** - *Allows the choice of representation (i.e. the implementation) to vary separately from the API (i.e. the interface).*[^impl-vs-interface]
    * Built-in language support is often provided in the form of **classes**.
    * See also: LISP constructors
        * AKA **constructor** or **static factory method** in other languages
    * See also: LISP selectors
        * AKA **accessors**, mutators, or **properties** in other languages
* **module**[^mod-asm] - *Groups several procedures and data types into a namespace independent from other modules.*
    * AKA package (Java), namespace (C++), module (Python)
    * Languages that don't have built-in support for this concept typically use prefixes to create de-facto namespaces. (C, Objective-C, PHP < 5.3.0)
* **assembly** - *Groups several modules together in a single versioned [^versioning] package. Assemblies can depend on other assemblies, often from separate vendors.*
    * AKA **shared library** (C, C++), gem (Ruby), egg (Python)

[^impl-vs-interface]: For example, complex numbers can be expressed in rectangular (a + b*i*) or polar form (r*cos(𝜽)). -- Some representations are better than others for different operations. Adding works better in rectangular form. Multiplying works better in polar form.

[^versioning]: Versioning assemblies effectively is a challenging topic onto itself. If done without care you get so-called "dependency hell". Just getting a consistent version numbering scheme can be tricky. One popular versioning scheme is codified as [Semantic Versioning](http://semver.org).

[^mod-asm]: SICP does not mention the notion of a *module* or an *assembly*, however these are common higher-level units for abstracting computation in languages other than Lisp.

<a id="abstract-data-types"></a>
## Abstract Data Types

<a id="lisp-vs-pascal-design-philosophies"></a>
### Lisp vs. Pascal Design Philosophies

*For you youngin's that have never used Pascal, just replace "Pascal" with "Java" in this section and you should get the right idea.*

Two design philosophies:

* **Lisp-school**: Create abstract data types by combining a *small* set of general-purpose data types (particularly collections). These complex structures can then be manipulated using operations on these general-purpose types.

    * *"Lisp is for building organisms -­ imposing, breathtaking, dynamic structures built by squads fitting fluctuating myriads of simpler organisms into place."*
    
    * *"Lisp programs inflate libraries with functions whose utility transcends the application that produced them."*


* **Pascal-school**: Create *many* special-purpose data types (i.e. classes) and specialized operations to manipulate them.

    * *"Pascal is for building pyramids -­ imposing, breathtaking, static structures built by armies pushing heavy blocks into place."*
    
    * *"In Pascal the plethora of declarable data structures induces a specialization within functions that inhibits and penalizes casual cooperation."*

Roughly speaking, I think of the Lisp philosophy as **programming with collections** and the Pascal philosophy as **programming with classes**.[^nonviable]

#### Usage

The Pascal philosophy has won out in most statically typed languages such as C++ and Java, and in languages with poor (or nonexistent) built-in collections.

The Lisp philosophy is more common in dynamically typed languages that lack built-in support for classes, such as Lisp itself and JavaScript.

A hybrid approach (using both philosophies) is seen in languages that are dynamically typed, have built-in collections, and have built-in classes, such as Python and Ruby.

[^nonviable]: In my opinion, a language that supports neither first-class collections nor first-class classes is non-viable for large scale general purpose software development. C, Assembly, and Fortran fall into this category.

<a id="polymorphism"></a>
### Polymorphism

Polymorphism is where multiple abstract data types implement a common *interface*, which is typically defined as a series of methods that can be called on all implementing types.

This allows client code, when given an object known only to implement a particular interface, to invoke interface methods on the object and end up calling the correct implementation of that method depending on the runtime type of the object.

#### Implementation Strategies

Polymorphism can be implemented in several different ways:

* **Switch on Typecode**
    * Easiest to implement. Hardest to maintain.
    * Treated as an anti-pattern in many OO languages.
* **Virtual Lookup Tables**
    * AKA "data-directed programming" (in SICP) or v-tables (C++)
    * Default implementation strategy for most OO languages.
* **Message Passing**
    * Most flexible.

Many languages provide a *default implementation strategy* as a language construct. For example C++ and Java use virtual lookup tables. Smalltalk and Objective-C use message passing. C doesn't give you anything for free, so you have to roll your own polymorphism.

#### Tradeoffs

These implementation strategies for polymorphism have some tradeoffs, which are worth knowing:

* Virtual lookup tables are restricted in that *the total set of operations on the abstract data type must be known in advance*.
* Message passing, on the other hand, can be made more flexible: 
    * Implementing data types may choose to support more operations than the standard set on the interface.[^vfs]
    * Heck, individual *instances* can choose to support more operations than the standard set.
        * In such cases, you would want to interrogate (i.e. reflect on) an individual instance to determine what operations (i.e. messages) it understands/supports.

[^vfs]: For example, the Linux virtual filesystem, which is implemented in message-passing style, has a common set of operations that all filesystems are expected to support (ex: `unlink`). However individual filesystems may support additional operations: For example the HFS+ filesystem on Mac OS X additionally supports a `delete` operation, which has slightly different semantics than the standard `unlink` operation.

<a id="cross-type-operations"></a>
### Cross-Type Operations

Introducing **cross-type operations**, such as `add(Integer, Complex)`, is a very tricky design issue.

Having explicit functions that operate on all combinations of types is possible but highly verbose. With **n** types and **m** operations, you need <strong>n*m</strong> functions to implement all combinations. Impractical.

Another strategy is to use *coercion* to convert a value from one type to another. So instead of defining `add(Integer, Complex)`, just define `convertToComplex(Integer) : Complex`, and use the existing `add(Complex, Complex)`. To convert between all types requires at least **n** but no more than **n<sup>2</sup>** conversion functions.

Many programming languages have built-in facilities to automatically coerce types. For some languages (like JavaScript or PHP) these coersion rules are quite complex (and error-prone). Other languages (like ML) ban implicit coercion entirely.

* Java only has coercion for built-in types.
* C++ lets the datatype designer choose (via `implicit` or explicit one-argument constructors).
* Scala relies on implicit coercion a lot to enable foreign methods to be introduced on types.

One wrinkle is that these conversion functions might introduce a loss in precision. For example not every integer can be represented as double of exactly the same value.

<a id="assignments-mutable-state-and-side-effects"></a>
## Assignments, Mutable State, and Side Effects

Introducing assignment creates lots of complications. In particular *referential transparency* is lost. Optimizations related to reordering and coalescing expressions need to be a lot more careful. Static reasoning of various kinds is impaired.

To reduce bugs it is best to minimize the use of mutation by using immutable objects whenever possible.[^large-structs]

Haskell takes a very aggressive stance against assignments, mutable state, and other side effects: they are banned by default. However Haskell does allow side effects within the context of a **monad**. This is a special construct unique to Haskell (so far as I know).

[^large-structs]: A common case where eliminating mutation may *not* be practical is when defining and working with large data structures that need many small updates made to them over time. If such a structure were made immutable, there would be a large performance penalty for recopying the entire structure whenever a small change needed to be made.

<a id="lazy-evaluation"></a>
### Lazy Evaluation

Normally expressions are evaluated immediately, in the order that they occur in code. **Lazy evaluation** changes this behavior such that expressions are only evaluated when some primitive operation (like print or add) requires the value of the expression. Until then the unevaluated expression is passed around (as a "thunk").

Lazy evaluation enables that creation of **lazy data structures**, which is a useful performance optimization in some contexts.

Unrestricted mutation and lazy evaluation do not mix well in programming languages. Since unrestricted mutation is very common in mainstream programming languages, it is quite rare to be in an environment that supports lazy evaluation. Haskell is one of the few.

<a id="declarative-languages"></a>
## Declarative Languages

Logic programming languages are at the far declarative end of the
imperative-declarative spectrum. They can be used to deduce answers
from a set of initial set of declarative statements.

[Prolog] is the best-known example of a logic programming language.

Query systems for databases are a type of logic programming language.

A "query" (i.e. an expression in the language) is transformed into a
"query plan" (i.e. a specific set of steps to follow) by a query planner. The implemented of these planners is quite complex.

[Prolog]: /articles/2013/02/25/notes-on-prolog/

<a id="conclusion"></a>
## Conclusion

So those are a few interesting things I learned from reading SICP. Taking notes while reading made it a lot easier for me to remember the content. You might try it when reading a technical book with a lot of new concepts.

### *Related Articles*

* [Notes on Racket](/articles/2013/03/01/notes-on-racket/)
    * *Describes Racket, a dialect of Lisp with batteries included.*  
      *Useful for implementing other languages and creating cross-platform GUI programs.*
* [Unique Features of Various Programming Languages](/articles/2013/01/29/unique-features-of-various-programming-languages/)
    * *Discusses several programming languages and their unique features.*
* [Notes on Prolog](/articles/2013/02/25/notes-on-prolog/)
    * *Describes the Prolog language in more detail.*