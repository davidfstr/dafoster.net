---
layout: page
title: Home
breadcrumbs: []
---
{% include JB/setup %}

<h1>{{ page.title }}</h1>

My name is [David Foster]. On this site you will find [projects] I'm working
on, [articles] I've written, and other useful information.

Much information related to my activities prior to 2010 can also be found on 
my [old site].

{% comment %}[TODO: Create pages for these links.]{% endcomment %}
[David Foster]: /about/
[projects]: /projects/
[articles]: /articles/
[old site]: /prism/

## Recent Articles

{% comment %}[TODO: Only list the most recent 30.]{% endcomment %}
<ul class="posts">
  {% for post in site.posts %}
    <li><span>{{ post.date | date_to_string }}</span> &raquo; <a href="{{ BASE_PATH }}{{ post.url }}">{{ post.title }}</a></li>
  {% endfor %}
</ul>
{% comment %}[TODO: Link to "See all articles..."]{% endcomment %}
