---
layout: home_page
title: Home
breadcrumbs: []

style: |
  .img-box-right { float: right; margin-left: 1em; }
  
  .img-100 { width: 100px; }
  @media (min-width: 768px) {
    .img-100 { width: 125px; }
  }

---
<img class="img-box-right img-100" alt="Picture of David Foster" src="/about/profile.jpg" style="margin-top: 1em;" />

<h1>DaFoster</h1>

My name is [David Foster]. Check out the cool [software I've written]!

My [articles] may also be of interest:

[David Foster]: /about/
[software I've written]: /projects/
[articles]: /articles/

## Featured Articles {% include featured_article_star %}

<ul class="x-posts">
  {% for post in site.posts %}
    {% if post.featured %}
      <li>
        <span>{{ post.date | usa_date_to_string }}</span> &raquo; <a href="{{ BASE_PATH }}{{ post.url }}">{{ post.title }}</a>
        {% if post.date_updated %}
          <span title="Updated {{ post.date_updated | usa_date_to_string }}" style="cursor: help;">✚</span>
        {% endif %}
      </li>
    {% endif %}
  {% endfor %}
</ul>

## Recent Articles

<ul class="x-posts">
  {% for post in site.posts limit:10 %}
    <li>
      <span>{{ post.date | usa_date_to_string }}</span> &raquo; <a href="{{ BASE_PATH }}{{ post.url }}">{{ post.title }}</a>
      {% if post.date_updated %}
        <span title="Updated {{ post.date_updated | usa_date_to_string }}" style="cursor: help;">✚</span>
      {% endif %}
      {% if post.featured %}
        {% include featured_article_star %}
      {% endif %}
    </li>
  {% endfor %}
</ul>
<a href="/articles/">See all articles...</a>

## Featured Projects {% include featured_project_star %}

<div class="x-projects" style="margin-bottom: 1.25em; margin-top: -.7em;">
  {% for cur_page in site.pages %}
    {% if cur_page.layout == "project" and cur_page.featured %}
      {% assign project_title = cur_page.title %}
      {% assign project_url = cur_page.url | replace: '/index.html', '/' %}
      {% assign project_summary = cur_page.summary %}
      {% assign project_is_redirect = cur_page.redirect_to_url %}
      
      <div class="project">
        <a href="{{ project_url }}"><img src="{{ project_url }}{% if cur_page.logo_filename %}{{ cur_page.logo_filename }}{% else %}logo-128.png{% endif %}" alt="Logo for {{ project_title }}" /></a>
        <div>
          <h2><a href="{{ project_url }}"{% if project_is_redirect %} class="external"{% endif %}>{{ project_title }}</a>
          </h2>
          <p>
            {{ project_summary }}
          </p>
        </div>
      </div>
    {% endif %}
  {% endfor %}
</div>

## Miscellaneous

Much information related to my activities prior to 2010 can also be found on 
my [old site].

[old site]: /prism/
