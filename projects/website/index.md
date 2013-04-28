---
layout: project
title: Website
summary: >
    This website.
x_languages: [Web]
x_location: Online at /

linkable_headings: true

---
This website has gone through a number of rewrites over the years.

<div class="toc">
  <ul>
    <li><a href="#version-1-0">Version 1.0</a></li>
    <li><a href="#version-2-0">Version 2.0</a></li>
    <li><a href="#version-3-0">Version 3.0</a></li>
  </ul>
</div>
<br clear="all" />

<h2 id="version-1-0">
Version 1.0 <small>HTML with SSI (Aug 25, 2007 - Nov 12, 2007)</small>
</h2>

I originally wanted to create a portfolio website to advertise my skills
and help me get internships during college. Given my tenure at Google and
Microsoft, I'd say I succeeded. :-)

This [original website] was maintained until around 2011 and is still
referenced by parts of this site.

### Technologies

* HTML, CSS
* Server Side Includes (SSI)

### Special Features

* Compatible with Internet Explorer 6[^ie6]
* Accessible design for screenreaders


<h2 id="version-2-0" style="margin-top: .7em;">
Version 2.0 <small>Drupal, PHP (Jun 14, 2010 - Sep 27, 2010)</small>
</h2>

Version 1.0 had a great fine-tuned layout but was difficult to modify,
given the limited power of server side includes - the only dynamic rendering
facility available.

This version was intended to make it easy to add new projects, and to provide
blogging capabilities.

### Technologies

* Drupal, PHP
* limited HTML & CSS customizations

### Special Features

* Editable in the browser from any computer
* Graphic design (professional)
* First-class Projects, Project Languages, Project Categories, and Project Updates
* Blog.
* RSS feeds everywhere.


<h2 id="version-3-0" style="margin-top: .7em;">
Version 3.0 <small>Jekyll, Markdown, Liquid (Dec 17, 2012 - Ongoing)</small>
</h2>

Editing site content and structure in Drupal for version 2.0 was sufficiently
annoying that I ended up doing less updates to the site than I wanted.

In particular articles weren't getting written because the Markdown syntax in
Drupal was getting munged by input filters and the CSS from the site theme.
Since there were a lot of layers to Drupal's processing, this was complicated
to debug and fix.

So I decided to [stop using Drupal] and go with a simpler system: render all
pages to static HTML which can then be deployed to any web host, including
free ones. All dynamic behavior is farmed out to JavaScript and third party
services (ex: Disqus).

### Technologies

* Jekyll[^jb], Liquid - generate pages
* Markdown - author content
* Bootstrap - base CSS
* Discus - comments
* Google Analytics - basic analytics
* HTML5 Shim - make IE play nice with HTML5
* JQuery - trivial DOM manipulation in JavaScript
* Git - version control, deployment

### Special Features

* Markdown for authoring everything.
    * Can author with great local tools like [Mou] or any good text editor[^txt].
* Easy deployment with git.
* Deployable anywhere (since it's just static HTML).
    * In particular, deployable to free services like [GitHub Pages].
    * When deployed to free services, gains additional resilience against
      my death.[^preservation]
* Version control. For content *and* site structure.


[original website]: /prism/
[^ie6]: IE6 is surprisingly difficult to support. It doesn't understand PNGs, has a different layout model than other browsers, and has lots of other quirks.
[stop using Drupal]: /articles/2012/12/16/why-i-no-longer-use-drupal/
[^jb]: It's hard to learn Jekyll from its documentation, which is fairly poor (as of early 2013). Instead I learned Jekyll by forking the code for [Jekyll-Bootstrap](http://jekyllbootstrap.com) and modifying the code (significantly) to get today's structure. If I were to do this site over again, I'd probably start with [Octopress](http://octopress.org) instead of Jekyll-Bootstrap.
[Mou]: http://mouapp.com
[^txt]: [BBEdit](http://www.barebones.com/products/bbedit/) and its free cousin [TextWrangler](http://www.barebones.com/products/textwrangler/) are my favorite text editors. [Sublime Text](http://www.sublimetext.com) is also good if you need cross-platform support. Many new Mac users like TextMate, but it is less powerful than BBEdit.
[GitHub Pages]: http://pages.github.com
[^preservation]: Given my hobbies of archival and digital preservation, I definitely think about how artifacts I create (such as this website) will operate after I am no longer alive to actively maintain them.
