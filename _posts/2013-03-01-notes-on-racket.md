---
layout: post
title: Notes on Racket (PLT-Scheme)
tags: [Software]

---

Generally [Racket] appears to be a very usable dialect of Lisp/Scheme.

Racket is particularly well suited for those who want to develop their own programming language (including those not based on S-expressions), given that the creators of Racket are programming language researchers. For example, a number of Racket subsets have been created to assist students who are learning Racket/Scheme via the [How to Design Programs] book.[^Racket-subsets] The Arc language by Paul Graham is also implemented in the Racket environment.

Racket's developers wanted to make sure it was a *practical* language. To that end, there is a bundled IDE (DrRacket) with syntax highlighting, parentheses matching, and integrated debugging. There is also a package management system (PLaneT).[^import-planet] And built-in libraries for working with several real-world systems, such as GUIs, networking, databases, JSON/XML, etc. A cross-platform executable can easily be built. And everything is well documented.

Graphics and GUI programs are supported better than the average language. For example pictures are rendered natively in the Racket REPL, including their use within expressions. And the built-in Racket GUI library is fairly decent.

The combination of a decent built-in GUI library along with the ability to compile cross-platform executables makes Racket useful for writing cross-platform GUI applications.

## Racket's GUI library (RacketGUI)

The original version of Racket's GUI library was implemented on top of wxWidgets.[^gui-rewrite] Thus some of wxWidget's poor design decisions leak through:

* A visual component is called a "window", not a control.
* Visual components must be associated with their parent container at creation time.

However, some fixes were made too:

* There is no notion of a wxWidgets "sizer" as distinct from a "container window".
    * This simplifies the mental model considerably, since it is no longer necessary to keep track of both a "window" hierarchy and a sizer hierarchy.
    * Instead, a wxWidgets "sizer" is represented as a lightweight RacketGUI "pane", which can be nested naturally inside containers along with other components.
* The event handling loop is managed in the background automatically.

Sadly, RacketGUI lacks some advanced controls I often want:

* trees
* tables containing controls in cells
    * However the `list-box%` control supports cells that only contain text.
* tree-tables

This is not surprising since these controls are hard to implement and are not well-supported by the original underlying wxWidgets library:

* The wxWidgets tree interface (wxTreeCtrl) is annoying for dynamically generated trees.
* Tables (wxListCtrl) only support text and image cells, not controls as cells.

### *Related Articles*

* [Unique Features of Various Programming Languages](/articles/2013/01/29/unique-features-of-various-programming-languages/)
    * *Describes several other programming languages and their unique features.*
* [Notes on Prolog](/articles/2013/02/25/notes-on-prolog/)
    * *Describes Prolog, a highly declarative language. Useful for verification of proofs.*


[Racket]: http://racket-lang.org
[^import-planet]: It is possible to import modules directly from the PLaneT repository, which will automatically download and install the module if it isn't already present. Neat!
[How to Design Programs]: http://htdp.org
[^Racket-subsets]: The [HtDP](http://htdp.org) book uses the dialects "Beginning Student", "Intermediate Student", and "Advanced Student". These sublanguages restrict the use of certain language features (such as using functions as objects) and can provide better error messages (which avoid mentioning advanced features not supported by the sublanguage).
[^gui-rewrite]: Racket's GUI layer has apparently been redone a couple of times. Originally it was based on wxWidgets. Later it was rewritten to about 200,000 lines of C++ glue to Xt, Win32, and Carbon. Then in Racket 5.1 it was replaced with about 80,000 lines of Racket glue to Gtk, Win32, Cocoa, Cairo, and Pango. That's a 60% reduction in code! More details on the [Racket blog](http://blog.racket-lang.org/2010/12/racket-version-5.html).