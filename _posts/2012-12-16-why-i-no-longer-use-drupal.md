---
layout: post
title: Why I no longer use Drupal
tags: [Software, Productivity]
date_published: 2012-12-21

---

*<b>TLDR:</b> Drupal is overly complex for a personal blog. It is hard to maintain. Simple static site generators are easier to work with in the long term.*

My portfolio website was written during college using hand-coded HTML and used server-side includes to bring in common navigation.

Then in January 2010 I remade my site in Drupal. It gained lots of fancy features such as first-class support for project categories and project languages. You could subscribe to almost any page as a feed. There were project specific updates that could be commented on. From a feature point of view, it rocked.

But some problems became apparent over time:

* Security updates were frequent and difficult to apply correctly.
* I didn't like writing articles on the site because I couldn't use simple markup formats such as Markdown.
    * Drupal has no good editor plugins for markup languages.
    * And its visual HTML editor generates messy HTML.
* The theme I used for the site was complex and hard to modify.
    * And the CSS often interfered with my article markup, necessitating me to drop into HTML when editing certain articles.
* There was no sane way to test structural changes to the site locally and then automatically deploy them to production.
    * Normally this would be done by keeping the site structure in the filesystem and all user content in a database. This allows the filesystem contents to be easily deployed using `git push`, `rsync`, or similar techniques.
    * Drupal, by contrast, keeps its site structure in both the filesystem *and* in the database, along with user-generated content. Updating only the parts of the database related to site structure is cumbersome and error-prone.
    * Thus, I couldn't really change the site structure after my initial deployment to production.
* Nothing was in revision control, which made me nervous.
* I had to hack the Drupal core to get my contact form to work with my web hosting provider.
* Most of the features of the site weren't being used by readers.

So now I am rewriting my site yet again in straight HTML (via a simple static site generator) and outsourcing all user generated content (like comments) to third party service providers.

Benefits:

* Simple simple simple.
* Automatic security. The web server just serves static files.
* Automatic scalability, for the same reason.
* Simple authoring in Markdown with powerful client-side text editors.
* Instant deployment with `git push`.
* Everything in revision control.
* I can use any web hosting provider. Hell, I can just use [GitHub Pages] for free.
* Ultimate control over the site theme and CSS. I can fix problems myself.

[GitHub Pages]: http://pages.github.com
