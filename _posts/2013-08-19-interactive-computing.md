---
layout: post
title: Interactive Computing
tags: [Software]

---

I spent a considerable amount of time yesterday going through the work of [Bret Victor](http://worrydream.com/), who appears to be on a personal mission to bring interactive computing to mainstream developers. The tools he's prototyping and building are just incredible.

What the heck do I mean by *interactive computing* you ask? This is perhaps best demonstrated by examples from Bret's portfolio:

* [**Inventing on Principle**](http://vimeo.com/36579366) (54 minutes)
    * Shows 5 different demos where Bret has programs or other complex objects where he can tweak the object at runtime and get immediate feedback. This is incredibly empowering.
    * <p>It makes me feel that a lot of the developer tools I've been using are obsolete. Particularly for advanced applications that involve the analysis and exploration of data.</p>
* [**Up and Down the Ladder of Abstraction**](http://worrydream.com/LadderOfAbstraction/) (13 pages)
    * Shows how an algorithm based on tunable parameters can be inspected and modified at runtime with immediate feedback.

By happenstance I've been fighting the problem of lacking immediate feedback recently: I've been writing a number of tools for processing complex semi-structured information where the algorithms needed a lot of tweaking.[^web-scraping] To gain a limited form of live tweaking I wrote a [function decorator](http://dafoster.net/articles/2013/08/13/fixing-a-function-at-runtime-without-restarting-the-program/) that allowed me to modify and reload functions at runtime without interrupting the program. The tools that Bret is prototyping are considerably more advanced than this, allowing changes to individual expressions without even a reload step.

Other small steps in the direction of interactivity in mainstream environments include the display of non-text results in interactive prompts. The [IPython](http://ipython.org/notebook.html) environment, for example, allows image values to be displayed directly in interactive prompts. This is great for statistical visualizations on complex datasets and for image processing functions. The [Racket](http://docs.racket-lang.org/quick/index.html) environment (a Scheme/Lisp dialect) also supports direct display of image values. It would be nice if HTML elements, sound waveforms, and video objects were also directly displayable.

The recent work on the [Light Table](http://www.chris-granger.com/2012/04/12/light-table---a-new-ide-concept/) web IDE is directly inspired by Bret's work, which I didn't realize the first time I heard about it. And now I notice that Light Table has support for Python[^python-in-lt] in addition to the original Clojure and JavaScript/HTML languages. Sweet.

Exciting developments.


[^web-scraping]: In case you're wondering, these tools are designed to scrape various kinds of data from popular websites. I'm experimenting with the idea of making it easy to extract structured information out of semi-structured websites. If it was trivially easy to get data out of websites, what could you do with it? What new mashups and applications would arise that you didn't think of before?

[^python-in-lt]: Sadly it seems that Light Table's current Python support is limited to allowing reevaluation of individual expressions upon request. Its support for Clojure is better, including an "instarepl" which evaluates all expressions as they are typed and displays the results of all intermediate variables and data flows.