---
layout: home_page
title: Home
breadcrumbs: []
---
<h1>{{ page.title }}</h1>

My name is [David Foster]. On this site you will find [articles] I've written
and [projects] I've done.

Much information related to my activities prior to 2010 can also be found on 
my [old site].

[David Foster]: /about/
[projects]: /projects/
[articles]: /articles/
[old site]: /prism/

## Featured Articles

<ul class="x-posts">
  {% for post in site.posts %}
    {% if post.featured %}
      <li>
        <span>{{ post.date | date_to_string }}</span> &raquo; <a href="{{ BASE_PATH }}{{ post.url }}">{{ post.title }}</a>
        {% if post.featured %}
          <span title="Featured Article">&#x2606;</span>
        {% endif %}
      </li>
    {% endif %}
  {% endfor %}
</ul>

## Recent Articles

<ul class="x-posts">
  {% for post in site.posts limit:30 %}
    <li>
      <span>{{ post.date | date_to_string }}</span> &raquo; <a href="{{ BASE_PATH }}{{ post.url }}">{{ post.title }}</a>
      {% if post.featured %}
        <span title="Featured Article">&#x2606;</span>
      {% endif %}
    </li>
  {% endfor %}
</ul>
<a href="/articles/">See all articles...</a>
