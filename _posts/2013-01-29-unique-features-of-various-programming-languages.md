---
layout: post
title: Unique Features of Various Programming Languages
tags: [Software]

---

<blockquote>
  A language that doesn't affect the way you think about programming, is not worth knowing.<br/>
  <br/>
  &ndash; <a href="http://www-pu.informatik.uni-tuebingen.de/users/klaeren/epigrams.html">Alan Perlis</a>
</blockquote>

I like learning new languages to get myself to think about problems in different ways.

Here's a list of a few well-known languages I've worked with and some of the more interesting features I've encountered:

### C

* **Undefined behavior**
    * The idea that a language specification would explicitly specify certain constructs as having undefined behavior is interesting. Most specifications leave things undefined by omission, not commission.
    * Although this allows various compiler optimizations, many developers rely on their particular compiler's implementation of undefined behavior without even realizing it.[^overflow]

[^overflow]: For example it is undefined what happens when you add to an integer variable and the variable overflows. In most compilers adding 1 to the largest integer wraps around to result in the smallest integer, and thus a number of programs depend on this behavior.

### Java

* **Objects are the primary unit of composition**
    * There are no standalone functions.
    * Design Patterns can be used to describe high level object coordination patterns.
    * However sometimes the community's focus on objects can be a bit extreme[^java-rant].
* **Checked exceptions**
    * Great when used *sparingly*, as it forces the caller to handle expected error conditions.    
        * I do think that it was a usability error to make `Exception` checked and `RuntimeException` unchecked. Rather it should be `Exception` that is *unchecked* and a new `CheckedException` should be the base for all checked exceptions. This makes it clear that *unchecked* exceptions should be the default.
    * Managing checked exceptions *correctly* is quite difficult. <!-- TODO: ARTICLE-IDEA -->
* **Unicode strings**
    * Tons of other languages use "bytestrings" as the main string type which causes all kinds of problems when working with international characters. <!-- TODO: ARTICLE-IDEA -->
* **Documentation focus**
    * Every library is expected to have JavaDoc documentation, which is generated from documentation comments in the source
    * This is really powerful, since it makes it easy for developers to write documentation, and to do so at the same time the implementation is coded, when the desired behavior is most fresh in the mind.
* **Compatibility focus**
    * I have never seen a community so focused on maintaining backward compatibility. I can't think of a single deprecated method in the Java library that was actually deleted.
    * Even the Java Language Specification has an entire chapter devoted to [binary compatibility](http://docs.oracle.com/javase/specs/jls/se5.0/html/binaryComp.html).
    * This focus may be partially attributable to the early mantra of [Write once, run anywhere][wora].
* **Garbage Collection**
    * Being freed from the confines of manual memory management makes it a ton easier to focus on more important things.

[^java-rant]: Steve Yegge has a great rant on the over-focus on objects in the Java community: [Execution in the Kingdom of Nouns](http://steve-yegge.blogspot.com/2006/03/execution-in-kingdom-of-nouns.html)

[wora]: http://en.wikipedia.org/wiki/Write_once,_run_anywhere

### C&#35;[^java-copycat]

* **Assemblies**
    * This is a level of encapsulation above the typical namespaces or modules in most languages. Assemblies are similar to the idea of static/dynamic libraries in C or JAR files in Java.
    * Notably, you can mark members as `internal`, which makes them public within the same assembly, but private to everybody outside the assembly. This is quite useful.

[^java-copycat]: C# is by design almost a direct copy of Java. It amazes me that Microsoft (C#'s sponsor) would spend so much effort making a copy of an existing language.

### Python

* **Indentation is significant**
    * Everyone notices this pretty fast.
    * Overall I think requiring correct indentation is a Good Thing™, as it contributes directly to *readable* code.
    * However this makes lambda expressions much less powerful than in other languages, since you can't easily nest statements inside a lambda expression without explicit braces (or similar delimiters).
    * Another side effect of having significant indentation is that the choice of tabs vs. spaces really matters. If you mix them, your program probably won't run.
* **Interactive interpreter (REPL)**
    * Amazingly useful for prototyping quickly, running experiments, and learning the language.
* **Collections are first class**
    * You can type `[1,2,3]` to get a list, `{'key': 'value'}` to get a dictionary, and `{1,2,3}` to get a set. So much faster than `new ArrayList<Integer>(...)`, `new HashMap<Integer>(...)`, or `new HashSet<Integer>(...)`.
* **Functions are first class**
    * You can declare them as literals, pass them around, and create higher-order functions that take functions as parameters.
    * Functions can also live on their own without an enclosing class, in contrast to Java. This is often the simplest approach for a given implementation.
* **"Magic" marked explicitly**
    * Anything "magic" that the language treats specially has names surrounded by double underscores.
    * For example:
        * An object's constructor is called `__init__`.
        * The method implementing an operator overload for plus is called `__add__`.
        * A class's metaclass is held by the `__metaclass__` field.
* **Metaclasses**
    * Deep magic. I will say no more.

### JavaScript

* **No blocking I/O**
    * All I/O is non-blocking and asynchronous. This results in heavy use of [continuation passing style].
* **Successful despite huge flaws**
    * Ease of deployment and ubiquity (i.e. business considerations) trump ease of use. (PHP also wins for the same reason.)
    * A few flaws:
        * Everything is in the one global namespace.
        * No user-defined namespaces, modules, or importing of other files.[^js-no-namespaces]
        * No built-in facility for classes.[^js-no-classes]
        * Bizarre loose semantics for `==`.[^js-equality]
        * Multiple illegal value sentinels: `null` and `undefined`.[^js-truthy]
* **JSON (JavaScript Object Notation)**
    * A fantastically compact, readable, and portable notation for representing all kinds of data structures. Great for data interchange.

[continuation passing style]: http://en.wikipedia.org/wiki/Continuation-passing_style

[^js-no-namespaces]: Hence workarounds like [RequireJS](http://requirejs.org) to get includes and modules.

[^js-no-classes]: Hence reimplementions of class semantics in libraries like MooTools, Prototype, and [random blog posts](http://ejohn.org/blog/simple-javascript-inheritance/). (That blog post has the best implementation, IMHO.)

[^js-equality]: Hence recommendations to always use `===` instead of `==`.

[^js-truthy]: Hence recommendations to only depend on the "truthy" and "falsy" values of expressions instead of direct comparisons with `null` or `undefined`.

### Haskell

* **Lazy evaluation**
    * Expressions are only evaluated when some primitive operation (like `print` or `add`) requires the value of the expression.
    * Allows you to define your own control flow operators.[^control-flow]
    * Allows you to extract complex expressions without fear of introducing a performance hit (since the expression will only actually be evaluated if it is needed).
* **Pure &ndash; Side effects are disallowed by default**
    * Mutation of data structures and I/O, both of which have order-sensitive side effects, are not allowed except within the confines of **monad**.
    * A **monad** is a construct that explicitly controls evaluation order, in contrast to the usual unpredictable lazy evaluation behavior.
* **`null` banned by default.**
    * Unlike many languages, there is no special `null` value in Haskell that can be substituted anywhere.
    * Instead if a function wants to return a value of type `T` or null, you would declare the function as returning type `Option<T>`, which could either have the value `Some(tValue)` or `None`. When declared in this way, callers are *required* to handle both possibilies.
* **Type inference (+ static typing)**
    * The benefits of static typing without the need to specify the types for everything?  
      Count me in!

[^control-flow]: Want to implement Ruby's `until` loop or `unless` conditional? No problem.

### Lisp <small>(Common Lisp, Scheme, Clojure)[^lisp-dialects]</small>

* **Homeoiconic // Grammar and Abstract Syntax Tree (AST) equivalent**
    * When you write a Lisp program, the notation you use (the *grammar*) is equivalent to what a compiler would see (an *AST*).
    * Furthermore this Lisp code is represented as a nested structure of lists, symbols, and literals, all of which can be directly generated and manipulated in Lisp itself!
    * This allows Lisp code at runtime to generate list structures which can then be run as Lisp code directly.
    * And at *compile* time, Lisp **macros** can do the same thing, generating arbitrary new statements and control structures. This is extremely powerful.
        * Domain specific languages, in particular, are very easy to implement in Lisp thanks to macros.
    * However the highly uniform structure of Lisp code, devoid of operator and syntactic diversity, makes for lousy typography and thus low readability.
* **Lisp Conditions and Restarts**
    * Allows bidirectional communication between different parts of the call stack. More powerful than exceptions, since conditions can not only unwind the stack but also wind it back again via a restart.
* **Call-with-current-continuation**
    * Allows you to save the current execution state of the program in a variable and jump back to it later. Multiple times, even. It's like a friggin' time machine. You can implement fairly complex control flow operators with this function.

<!-- TODO: Add Prolog -->

[^lisp-dialects]: There are more dialects of Lisp than any other language I can think of. These 3 (Common Lisp, Scheme, and Clojure) are just the most popular dialects. I've directly used [Racket](http://racket-lang.org) in the past, which is itself a dialect of Scheme.