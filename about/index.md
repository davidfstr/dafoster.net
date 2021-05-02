---
layout: home_page
title: About
group: navigation
breadcrumbs: [/]
linkable_headings: true

style: |
  .img-box-right { float: right; margin-left: 1em; }
  
  .img-200 { width: 200px; }
  @media (max-width: 576px) {
    .img-200 { width: 100px; }
  }

---
<h1>{{ page.title }}</h1>

<img class="img-box-right img-200" alt="Picture of David Foster" src="profile.jpg" />

Hi! My name is **David Foster** and my mission is to make the world a better
place, through the tools of creating software and the written word.

I co-founded [TechSmart],
which seeks to bring world-class computer science education to K-12 students.
I specifically engineer the [TechSmart Platform] website.

[TechSmart]: https://www.techsmart.codes
[TechSmart Platform]: /projects/techsmart-platform/

My open source contributions that are probably the most well-known include:

* [TypedDict's initial implementation] and other [typechecking][] [extensions] in Python & [mypy];
* [SSA subtitle support in HandBrake];
* maintaining [RDiscount], Ruby bindings to the Discount Markdown implementation;
* enhancements to [Django].

[RDiscount]: /projects/rdiscount/
[TypedDict's initial implementation]: /projects/typeddict/
[typechecking]: https://www.python.org/dev/peps/pep-0655/
[extensions]: /projects/typeform/
[mypy]: http://mypy-lang.org/index.html
[SSA subtitle support in HandBrake]: /projects/handbrake-subtitle-support/
[Django]: https://www.djangoproject.com/

{% assign hiring = false %}
{% if hiring %}
If you like what you've read on my site and like the idea of bringing
computer science education to the K-12 space, [come work for me]!

[come work for me]: https://techsmart.betterteam.com/
{% endif %}

<h2 id="biography">Biography</h2>

I initially discovered computers when I was 4 and starting programming them at 6.
Since then, programming has been one of my most enduring passions.
Witness my large number of [personal projects](/projects/).

Beyond that I enjoy:

* reading;
* learning about languages (both spoken and programming);
* teaching;
* kayaking, visiting gardens; and
* watching the occasional anime series.

<h2 id="contact">Contact</h2>

Email **david** at this domain (dafoster.net).
