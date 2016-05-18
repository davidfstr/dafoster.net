---
layout: post
title: How I learn new programming languages
tags: [Personal, Software]

---

I don't learn new programming languages very often. It simply requires an enormous amount of time to properly understand the local philosophy, community, tools, and ecosystem. But every so often I see a glimmer in an unfamilar language that merits me picking it up.

Very recently I decided to learn Clojure to fulfill my future needs for a high-power language[^power]. Before embarking on this journey, I thought it would be valuable to reflect on how I've learned other languages in the past and why I learned them.

{% capture toc_content %}

* [My Journey](#my-journey)
* [Patterns of Learning](#patterns-of-learning)
* [Appendix](#appendix)

{% endcapture %}

<div class="toc">
  {{ toc_content | markdownify }}
</div>

<a id="my-journey"></a>
## My Journey

* **HyperTalk & HyperCard** &ndash; Play
    * This was my first programming language, first used at age 6.
    * The HyperCard environment was sufficiently well designed that I could *play* with existing programs, copy bits and pieces to assemble my own, and eventually build components from scratch. 
    * The physicality of the system, the straightforward syntax, and the composability of program elements enabled this kind of play. I do not know of any programming environments today in which this would be possible.
        - Visual Basic is promising, although I've never used it. It has physicality and native graphics.
        - DarkBASIC is also promising for making 3D games, although I haven't used it for anything serious. It has native 3D graphics.
        - Python has a REPL that you can experiment with and has reasonably straightforward and consistent syntax. However it has no native graphics and no physicality.
        - Processing has a built-in graphics. But it's not designed for composability at all, meaning that you can't mix and match parts from different programs. Its function naming is also haphazard and inconsistent.
    * <p>My game [Dungeons](/prism/projects/dungeons/) was the most advanced program I wrote in HyperCard. Other kids at National Computer Camp would line up at my computer who wanted to play it. I was very proud.</p>
* **BASIC, Pascal** &ndash; Instructional Setting
    * At age 8 I picked these languages up at National Computer Camp because the instructors insisted on learning them before going on to other languages. <!-- With my prior two years of HyperTalk and general programming experience, I blew through these languages very quickly. -->
    * These were my first compiled languages.
    * <p>Neither of these languages were distinctive enough for me to keep using.  
      I did no major projects in these languages.</p>
* **C, C++** &ndash; Brute Force, Instructional Setting
    * I learned these to interface directly with the Mac operating system and to do programs in color, since HyperCard only supported black & white graphics.
    * I also had some instructional assistance at National Computer Camp during the summer.
    * <p>I wish I could remember how I internalized pointers and manual memory management, since these are some of the most confusing bits of these languages for beginners. And most annoying for experts.</p>
* **Java** &ndash; Brute Force
    * I initially learned Java in 2001 when I tried to write RealMediaFixer in C++.[^rmf] When doing this I discovered that CodeWarrior's buffered I/O implementation was busted on Mac OS, behaving in a nondeterministic fashion. So I picked the most similar-looking language to C++ I'd heard of, namely Java, and ported RealMediaFixer to use it instead. It worked on the first try and I didn't look back to C++ for several years. (After all, why would I use a language where *I/O* was broken?)
    * I just wrote tons and tons of programs in Java for the next 8 years or so, through the rest of middle school, high school, and college.[^java-publish]
    * I also had some early instructional assistance at National Computer Camp. I am forever grateful to whatever instructor introduced me to the [Java API documentation](http://docs.oracle.com/javase/6/docs/api/), allowing me to teach myself arbitrary parts of the Java standard library without relying on books or tutorials. Once you can teach yourself, the learning game is really on.
    * <p>My Java decompiler [decomp4](/prism/projects/decomp/) was the most advanced program I wrote in Java.</p>
* **Python** &ndash; Targeted Large Projects
    * While interning at Google in 2008 I noticed that they had three primary languages: Java, C++, and Python. Since Google engineers were the smartest group of developers I'd ever run into, I figured they might be on to something with Python. So I started reading about Python and its capabilities.
    * My first attempt at a real program was the implementing of DiskSurveyorX in late 2008, a disk space visualizer.[^dsx] Unfortunately the best GUI toolkit available in Python, wxPython, I found to be far too clunky to use. So I ended up reverting to implementing in Java using the Swing toolkit.
    * My second and successful attempt to write a substantial Python program was [Crystal Web Archiver](/projects/crystal-web-archiver/) in late 2011, a website downloader and archival system.
        - Again I had to use wxPython. This time though I ended up writing an abstraction layer over the worst parts to remove much of the pain.
    * <p>Python is currently my favorite language for general purpose programming. Particularly for scripting, data analysis, and other kinds of exploratory work.[^other-favs]</p>
* **JavaScript** &ndash; Socialization, Brute Force (via Employment)
    * I've been using JavaScript, HTML, and CSS since mid-2012 to create rich web applications, primarily in the form of Splunk's app development framework. JavaScript was chosen because it is the lingua-franca of web development and because of its enormous leveragable ecosystem of libraries such as JQuery, Backbone, and Bootstrap.
    * Advanced JavaScript is almost impossible to learn on your own because there is no patron company that controls it nor is there a Benevolent Dictator for Life to provide officially blessed documentation or tutorials for how to use the language effectively. And this language has a sufficiently large number of design flaws that you need to learn to use it in a *disciplined* fashion.
    * I wouldn't have been able to get far in JavaScript without help from my coworker Itay who was already proficient. Should you not have access to such a resource probably the next-best thing is to look for non-trivial projects on Github and read them. For example I learned a lot by playing with [BrowserQuest](http://browserquest.mozilla.org/) and reading its [source code](https://github.com/mozilla/BrowserQuest).

<a id="patterns-of-learning"></a>
## Patterns of Learning

The primary patterns observed in my learning journey above include:

* **Play** &ndash; undirected learning, by oneself
    * This only works well with exceptionally well-designed programming environments. Sadly there are very few modern environments that fit the bill.
        - HyperCard is dead. Visual Basic is dying. DarkBASIC is not well known.
        - <p>Processing and Racket work okay but have some issues.</p>
* **Brute Force** &ndash; writing lots and lots of programs
    * This method will certainly give you the most understanding. It also takes the most time.
    * <p>Having access to a mentor to check your work is useful but not required.</p>
* **Targeted Large Projects** &ndash; writing a small number of projects geared toward getting the most experience
    * This is similar to the "brute force" approach but is more [tactical](http://expertenough.com/1423/deliberate-practice). It also requires more mental effort.

These primary patterns are coupled with a few secondary patterns:

* **Instructional Setting** &ndash; taking a class to learn basic and intermediate skills
    * I only found taking classes to be useful when my programming foundations were weak. Such classes provide very little value to me today.
    * <p>Note that taking a class isn't enough by itself. You have to practice on your own outside the class and after the class is finished.</p>
* **Socialization** &ndash; working with other developers to learn intermediate and advanced skills
    * Some things you can only learn efficiently from other developers.
    * Socialization is particularly useful for learning things in a highly fragmented ecosystem (such as JavaScript) or in settings with advanced concepts (such as overall program architecture or the functional programming paradigm).

<a id="appendix"></a>
## Appendix

There are a few languages I learned enough of to decide they weren't worth using in new projects:

* **PHP** &ndash; most widely deployed server-side web language
    * <p>[Just say no.](http://me.veekun.com/blog/2012/04/09/php-a-fractal-of-bad-design/)</p>
* **Ruby** &ndash; used primarily as a server-side web language
    * Insufficiently distinct from Python.
    * Poor backward compatibility guarantees. No release notes.
    * Sloppy design: [Non-formal grammar.](http://madhadron.com/posts/2014-11-10-languages_for_humans_and_subhumans.html) Syntax schizophrenia. Monkeypatching accepted as a valid practice. Mutable strings. <!-- Non-uniform string representation. -->
    * But superior packaging, dependency management, and isolation systems.

### *Related Articles*

* [Unique Features of Various Programming Languages](/articles/2013/01/29/unique-features-of-various-programming-languages/)
    * *Describes unique features of several languages mentioned in this article.*


[^power]: Paul Graham's essays on [Lisp and language power](http://www.paulgraham.com/icad.html) are a thought-provoking read. By my assessment the current most-powerful languages out there are [Haskell](http://www.haskell.org/) and various members of the Lisp family (ex: Scheme, [Racket](http://racket-lang.org/), [Clojure](http://clojure.org/)). I've decided to pass over Haskell for the time being for a number of reasons, particularly because of its high learning curve. I will probably return to it eventually.

[^rmf]: **RealMediaFixer** was a program I wrote that repaired RealMedia (`.rm`) files playable in RealPlayer. Such files downloaded over dialup would often get subtlely corrupted. Since downloading a 30-minute video could easily take a day it was more practical to try repairing the broken file rather than redownloading it.

[^java-publish]: I have a huge trove of Java programs from this time period I'd like to publish some day. A very small subset of these programs are listed on [my old projects page](/prism/projects/).

[^dsx]: **DiskSurveyorX** was a disk space visualizer program that used similar visualizations as the original DiskSurveyor program for classic Mac OS. It however had some nice usability improvements pulled from my learnings from the information visualization class I took at the Technische Universität München. A modern disk space visualizer that uses a similar visualization is [DaisyDisk](http://www.daisydiskapp.com/), which I highly recommend.

[^other-favs]: For desktop GUI development, the Java + Swing combination is still my favorite. Followed closely by the Objective-C + Cocoa + Mac combination. I don't care about GUI programs on Windows or Linux. However now practically all GUI development is going to the web, where solutions based on HTML + CSS + JavaScript reign supreme.