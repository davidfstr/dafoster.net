---
layout: post
title: Visual Guide to Programming Language Properties
tags: Software
featured: true

include_jquery: true
include_accordian: true

style: |
    .property { background-color: #ceecff; }
    .benefit { background-color: #b7ef86; }
    .detriment { background-color: #eec3cc; }
    
    .tab-content { overflow: auto; }
    .tab-content img { max-width: none; }

script: |
    // When a tab header is clicked automatically click all
    // other tab headers with the same language
    $('.tab-header').click(function() {
        if (!window.ignoreTabHeaderClicks) {
            var classNameForTabsWithSameLang = this.className.split(' ')[1];
            
            window.ignoreTabHeaderClicks = true;
            $('.' + classNameForTabsWithSameLang).click();
            window.ignoreTabHeaderClicks = false;
        }
    });

# The interactive graphs do not render well in Atom/RSS feeds.
# Therefore just direct the reader to the full article on the site.
feed_content: |
    Here's an interactive chart showing high-level properties of various programming languages.  
    You can filter the chart to only show the properties that your favorite language supports.
    
    [Read more...](/articles/2013/02/20/visual-guide-to-programming-language-properties/)

metadata_extra: |
    <a href="http://m.csdn.net/article/2013-06-28/2816045-Visual-Guide-to-Programming-Language-Properties">
        <img src="/assets/2013/china_flag.gif" style="margin-right: .3em;"/>
        Chinese translation
    </a>

---

Here's an interactive chart showing high-level properties of various programming languages.  
You can filter the chart to only show the properties that your favorite language supports.

Interesting observations:

* Some <span class="property">properties</span> enable (but do not always imply) other <span class="property">properties</span>, as shown by arrows.
* <span class="property">Properties</span> result in both <span class="benefit">benefits</span> and <span class="detriment">detriments</span> to a language, as shown by arrows.
* Sometimes it is necessary for *multiple* <span class="property">properties</span> to be present for a particular <span class="benefit">benefit</span> to
  manifest, as shown by arrows interrupted by a vertical bar.

## Type System

{% include 2013/2013-02-20-visual-guide-to-programming-language-properties/type_system.html.inc %}

<br/>
† "Programming with collections" is discussed in [Lisp vs. Pascal Design Philosophies].

[Lisp vs. Pascal Design Philosophies]: /articles/2013/02/01/learnings-from-sicp/#lisp-vs-pascal-design-philosophies

## Resource Management

{% include 2013/2013-02-20-visual-guide-to-programming-language-properties/resource_management.html.inc %}

<br/>
§ See also the idea of **monadic regions** for block-scoped resource management.

¶ Objective-C is the only known language that supports automatic reference counting.

## Domain Specific Language Support

{% include 2013/2013-02-20-visual-guide-to-programming-language-properties/dsl_support.html.inc %}

<br/>
‡ Beyond the Lisp family, Prolog is the only other language I know of that is homoiconic.  
&nbsp;&nbsp;&nbsp;Its syntax is reasonably easy to read, unlike Lisp.

## Tools

{% include 2013/2013-02-20-visual-guide-to-programming-language-properties/tools.html.inc %}

{% capture details_table %}
&nbsp;               | C++ | ObjC        | Java  | Haskell          | Python      | Ruby       | Lisp
---------------------|-----|-------------|-------|------------------|-------------|------------|---------------
Code coverage        | -   | -           | EMMA  | hpc              | coverage.py | SimpleCov  | *varies* <!-- ex: code-coverage -->
Unit test automation | -   | -           | JUnit | HUnit            | unittest    | *many*     | *varies* <!-- ex: RackUnit -->
Package manager      | -   | -           | -     | Cabal            | pip         | gem        | *varies* <!-- ex: PLaneT -->
Environment isolater | -   | -           | -     | cabal-dev, hsenv | virtualenv  | rvm        | *varies* <!-- no known example -->
{% endcapture %}

{% include accordian/begin %}
    Tool Details
{% include accordian/middle %}
    {{ details_table | markdownify }}
{% include accordian/end %}


### *Related Articles*

* [Spectrum of Languages by Hardware Distance](/articles/2014/12/20/languages-by-hardware-distance/)
    * *Visualizes programming languages by their distance from the hardware.*
* [Unique Features of Various Programming Languages](/articles/2013/01/29/unique-features-of-various-programming-languages/)
    * *Discusses several programming languages and their unique features.*
    * *Describes some <span class="property">properties</span> mentioned in this article in more detail.*

<div style="padding: .8em 1em .8em; margin-bottom: 1em; border: 1px solid #94da3a;">
    <p style="font-weight: bold; color: #487858;">
        Series
    </p>
    <p style="margin-bottom: 0em;">
        This article is part of the <a href="/articles/2013/05/11/book-outline/">Programming for Perfectionists</a> series.
    </p>
</div>

<hr/>

Please send comments and corrections to [David Foster](/contact/).