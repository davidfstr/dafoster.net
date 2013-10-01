---
layout: post
title: Strange Loop 2013 Highlights
tags: [Software]

---

This year I attended [Strange Loop](https://thestrangeloop.com/), a conference on emerging tools, languages, and trends in software. I found the following sessions to be most interesting.

Session videos are available for attendees now, and for the general public closer to March 2014.

## Emerging Languages Camp

* [**Noether: Symmetry in Programming Language Design**](http://www.infoq.com/presentations/noether) - Daira Hopwood - 45 min
    * A language system, composed of several different language levels, each level breaking successively more symmetries to gain expressive power at the expense of static reasoning about the program's behavior. Very flexible.
    * This is the only language presented during the Emerging Languages Camp that had a strong theoretical foundation.
    * <p>I will definitely be looking into this language family when it has been implemented.</p>
* [**Nimrod: A new approach to meta programming**](http://www.infoq.com/presentations/nimrod) - Andreas Rumpf - 25 min
    * A new statically-typed systems language. Full-featured.
    * Already has non-trivial tooling, such as an IDE.
    * Has a realtime garbage collector, macros, whole program dead code elimination, and generics.
    * Can automatically promote sideeffect-free functions to *compile*-time execution.
    * <p>Compile-time optimizations on the AST can be coded directly in Nimrod. This is similar to macros but acts like a global peephole optimization. Very powerful.</p>
* [**The J Programming Language**](http://www.infoq.com/presentations/j-language) -  Tracy Harms - 27 min
    * An array-based data language.
    * Successor to the famous [APL language], which allows very succinct representations of numeric computations. Although extremely hard to read for those unfamiliar with the syntax:
        * Find all prime numbers: `(~R∊R∘.×R)/R←1↓ιR`
        * Conway's Game of Life: `life←{↑1 ⍵∨.∧3 4=+/,¯1 0 1∘.⊖¯1 0 1∘.⌽⊂⍵}`
    * <p>If you've never used an array-based numerical language before, this is a great beginner's introduction.</p>
* [**BODOL, or How To Accidentally Build Your Own Language**](http://www.infoq.com/presentations/bodol) - Bodil Stokke - 42 min
    * A guide to implementing your own language on top of Clojure.
    * A very entertaining presentation.

[APL language]: https://en.wikipedia.org/wiki/APL_(programming_language)

**Honorable Mention:**

* [**Qbrt Bytecode: Interface Between Code and Execution**](http://www.infoq.com/presentations/qbrt-bytecode) - Matthew Graham - 26 min
    * A bytecode assembly language with builtin primitives for concurrency and inline asynchronous I/O.
    * I liked the presentation itself although I'm not sure I'd want to use Qbert for any of my own projects.

## Unsessions

* **QuickCheck** - no video available
    * QuickCheck is a testing tool that automatically generates test cases for a program given a description of its inputs, outputs, and expected semantics. Quite powerful.
    * When a failing test case is found, QuickCheck is able to automatically reduce the test case to the *minimal* reproducing test case. Extremely useful.
    * Although QuickCheck was originally written for Haskell, there are now ports to several other languages.
    * There a commercial versions of QuickCheck that are superior to the open-source versions in a few ways.

## Sessions & Themes

### Async <small>(Reducing callback hell)</small>

If you only watch one of these presentations, pick the Clojure one.

* **Async in C# and F#**
    * Although not presented at Strange Loop, the implementation of the `async` and `await` keywords in C# and F# seems to have greatly inspired similar mechanisms in other languages.
    * <p>`async`/`await` avoids the callback hell problem often seen in JavaScript, where a series of nested callbacks just keeps increasing the indentation level of the code. And callbacks in the midst of complex control flow like loops are even more problematic.</p>
* [**Async in Scala**](http://www.infoq.com/presentations/scala-async) - Philipp Haller - 44 min
    * Similar to async/await in C# and F#.
    * <p>Implemented in Scala as a macro, using the experimental support for Scala macros.</p>
* [**Async in Clojure: Channels & Queues**](http://www.infoq.com/presentations/clojure-core-async) - Rich Hickey - 44 min
    * Appears to be different in spirit to the async-implementation in other languages: Seems to be intended for implementing *channels* (from the Go language), rather than attempting to target the callback hell problem.
    * <p>The presentation itself has some interesting general thoughts on concurrency in software.</p>
* **Async in Python**
    * Again, not presented at Strange Loop, but it appears that the `yield from` expression in Python 3 can be used to implement C#/F#-style async/await. I need to look into this.

### Creativity and Artificial Intelligence

* [**Creative Machines**](http://www.infoq.com/presentations/ai-machine-creativity) - Joseph Wilk - 41 min
    * Interesting philosohpical discussion on how computers can create creative things.
    * Teaching computers to play music.
    * <p>Joseph's program for creating music compositions makes, in his opinion, better music than he could compose himself. This brings up the interesting observation that a student, in this case a computer, can surpass the teacher. This is not unheard of when both teacher and student are human, but it's a bit uncomfortable to conventional thinking when the student is a "soulless" or "non-understanding" computer and the teacher is a "sentient" human.</p>
* [**Learnfun and Playfun: A Nintendo automation system**](http://www.infoq.com/presentations/nintendo-automation) - Tom Murphy VII - 28 min
    * Teaching computers to play video games.
    * I found it particularly amusing that the computer learned to manipulate the random number generator (by pausing the game for calculated periods) to create its own luck. In pinball games this allowed the computer to play perfectly.

### Theory Meets Practice

* [**The Trouble With Types**](http://www.infoq.com/presentations/data-types-issues) - Martin Odersky - 49 min
    * A balanced description of static vs. dynamic types, a classic debate in computing.
    * <p>Martin himself, being the creator of Scala, is firmly in the static typing camp but still provides a good overview of when dynamic typing is useful as well.</p>
* [**Add ALL the things: abstract algebra meets analytics**](http://www.infoq.com/presentations/abstract-algebra-analytics) - Avi Bryant - 37 min
    * A good introduction to parts of category theory, using analytics systems for concrete examples throughout the talk.
    * <p>There was another presentation on category theory at Strange Loop but I found this talk far easier to follow.</p>
* [**Finding a way out**](http://www.infoq.com/presentations/reimagining-software) - Chris Granger - 33 min
    * Thoughts on the future of programming and how it can be made better.
    * The second half of the presentation walks through a demo of Aurora, a new alpha-stage tool that Chris is working on, incorporating some of Chris's new thoughts on the programming process.
    * Chris Granger is the creator of Light Table, a visual programming environment that attempts to bring improved interactivity and feedback to the development process. Light Table is inspired by Bret Victor's excellent talk [Inventing on Principle](http://vimeo.com/36579366).

### Tools

* [**Native Speed on the Web: JavaScript and asm.js**](http://www.infoq.com/presentations/javascript-asmjs) - Alon Zakai - 30 min
    * Useful overview of asm.js, which can compile C/C++ to fast JavaScript.
    * <p>This capability is very exciting since it can connect programs written for the traditional desktop environment to the web deployment platform. For example my efforts at making old Mac software easy to emulate on modern hardware, which currently requires installation on a desktop computer, could be altered to be widely deployable to the web.</p>
* [**The Birth & Death of JavaScript**](http://www.infoq.com/presentations/birth-death-javascript) - Gary Bernhardt - 20 min (without comments) or 40 min (with)
    * A very creative presentation on how asm.js could be used to make major changes to computing, bringing all traditional desktop applications to the browser.
    * Uses the narrative style of presenting as if from a different time period, also used to great effect in Bret Victor's talk on [The Future of Programming](http://vimeo.com/71278954).

### Minorities in Computing

#### Women

It's been known for some time that women are strongly underrepresented in computing. I know they're falling out of the training pipeline early as I receive almost no women applicants to the Splunk Seattle office.

So far the primary discouraging factors I've been able to identify include a lack of female role models in software and a hostile learning environment created by guys when girls try to enter the field.

* [**Making Software Development Make Sense to Everyone**](http://www.infoq.com/presentations/software-development-everyone) - Jen Myers - 58 min
    * <p>Very informative. Full of data and ideas.</p>
* **Rails Girls: Empowering women through code** - Adriana Palacio, Laura Garcia - 13 min
    * <p>Key takeaway is that there are a lack of female role models in computing.</p>
* [**The History of Women in Technology**](http://www.infoq.com/presentations/history-women-technology) - Sarah Dutkiewicz - 40 min
    * Reviews a number of important women in computing. Unfortunately very few from the modern era.

#### Kids

It is also difficult to get kids into computing. No longer are computers widely shipped with BASIC interpreters, HyperCard, or other well-designed introductory programming environments that kids can just jump into. Additionally the bar for what is considered an acceptable game or program has risen considerably, making it harder to get excited about simple programs.

* [**How to teach your kid to code with Hopscotch**](http://www.infoq.com/presentations/hopscotch)
    * Hopscotch is a visual programming language for the iPad designed to help kids get started with programming.
    * Another system for introducing kids to programming is [Scratch](http://scratch.mit.edu/).
    * Notes:
        * Finding good *ideas* for programs is tricky. For kids, ideas have to be applicable to their cultural context. Drawing things is more interesting than scraping Twitter.
        * Making all available tools and commands *visible* is important for a system designed for learning.
        * The game of "program your parent" is amusing.
        * Traditional editors, code, and IDEs actually look rather intimidating to new users. It's like a non-aviation operator being confronted with the full control panel of an airplane cockpit.
        * Poor typing skills is a non-trivial barrier for young kids.

### Other

* [**Exercises in Style**](http://www.infoq.com/presentations/style-methodology) - Crista Lopes - 39 min
    * A fascinating experient where the same program is written in several different styles.
    * This experiment makes it obvious that not only are there lots of ways of writing the same program, but also that different languages encourage different styles.
    * <p>The material in this presentation will eventually be incorporated into a book [Exercises in Programming Style](http://www.amazon.com/gp/product/1482227371/ref=as_li_ss_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=1482227371&linkCode=as2&tag=dafo07-20) that will be released in Spring of 2014. I'm definitely getting a copy.</p>
* [**Taking PHP Seriously**](http://www.infoq.com/presentations/php-history) - Keith Adams - 40 min
    * Reviews the *good* parts of PHP.
    * Introduces Hack, a gradually-typed version of PHP that in production use at Facebook.
    * <p>The HipHop project also includes a lot of useful tools such as a debugger, profiler, and IDE integration.</p>
<!--
* [**Programming a 144-computer chip to minimize power**](http://www.infoq.com/presentations/power-144-chip) - Chuck Moore - 40 min
    * A custom hardware programming environment for programming very low power applications.
    * Easily the lowest-level talk at the conference. Basically involves using a custom assembly language. Includes tips and tricks to optimize the assembly for the hardware and power.
    * Skip this presentation if low-level programming and bit twiddling isn't your thing.
-->