---
layout: post
title: Visual Guide to Programming Language Properties
tags: Software

include_jquery: true
include_bootstrap_js: true

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

## Resource Management

{% include 2013/2013-02-20-visual-guide-to-programming-language-properties/resource_management.html.inc %}

## Domain Specific Language Support

{% include 2013/2013-02-20-visual-guide-to-programming-language-properties/dsl_support.html.inc %}

## Tools

{% include 2013/2013-02-20-visual-guide-to-programming-language-properties/tools.html.inc %}

{% capture details_table %}
&nbsp;               | C++ | ObjC        | Java  | Haskell | Python      | Ruby       | Lisp
---------------------|-----|-------------|-------|---------|-------------|------------|---------------
Code coverage        | -   | -           | EMMA  | hpc     | coverage.py | SimpleCov  | code-coverage
Unit test automation | -   | -           | JUnit | HUnit   | unittest    | *many*     | RackUnit
Package manager      | -   | -           | -     | Cabal   | pip         | gem        | PLaneT
Environment isolater | -   | -           | -     | -       | virtualenv  | rvm        | -
{% endcapture %}

<div class="accordion" id="accordion2">
  <div class="accordion-group">
    <div class="accordion-heading">
      <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseOne">
        Tool Details
      </a>
    </div>
    <div id="collapseOne" class="accordion-body collapse">
      <div class="accordion-inner">
        {{ details_table | markdownify }}
      </div>
    </div>
  </div>
</div>

### *Related Articles*

* [Unique Features of Various Programming Languages](/articles/2013/01/29/unique-features-of-various-programming-languages/)
    * *Discusses several programming languages and their unique features.*
    * *Describes some <span class="property">properties</span> mentioned in this article in more detail.*
