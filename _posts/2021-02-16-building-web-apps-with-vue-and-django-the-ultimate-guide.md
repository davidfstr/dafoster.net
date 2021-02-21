---
layout: post
title: Building web apps with Vue and Django - The Ultimate Guide
tags: [Django, Software]
featured: true
x_audience: |
    novice web devs who want to build their first web app;
    experienced web devs coming from Django or Rails who 
        want to build their next web app in Django, 
        and are thinking about using Vue too;
    Django web dev with existing Django site who wants to 
        integrate Vue, perhaps migrating away from JQuery 
        or another frontend rendering technology;
    Vue web dev with existing Vue site on standalone server, 
        who wants to use Django as either an API server, 
        or *maybe* to potentially replace the Vue server 
        entirely (but it seems unlikely if a lot of effort 
        has already been put into a standalone Vue server)
x_performance: |
    595 pageviews on day 1 of publish (2021-02-18) and post to r/django
    TODO pageviews on week 1 of publish, with daily numbers of:
        595, 233, 115, TODO, TODO, TODO, TODO
         ↑ r/django (lots of traction)
               ↑ HN (almost no traction)

style: |
    /* Override blockquote to use same font size as body text */
    blockquote { font-size: 16px !important; }
    
    .toc-floating {
        float: right;
        margin-left: 1em;
    }
    @media (max-width: 650px) {
        .toc-floating {
            display: none;
        }
    }
    
    .bundling-diagram {
        max-width: 100%;
        float: right;
        margin-left: 5px;
    }
    @media (max-width: 440px) {
        .bundling-diagram:not(.bundling-diagram-wide) {
            max-width: 200px;
        }
    }
    @media (max-width: 380px) {
        .bundling-diagram:not(.bundling-diagram-wide) {
            max-width: 150px;
        }
    }
    @media (max-width: 850px) {
        .bundling-diagram-wide {
            float: none;
        }
    }

---

{% capture toc_content %}

* [1 server or 2 servers?](#1-server-or-2-servers)
* [1-server approach](#1-server-approach)
    * [Bundling strategies](#bundling-strategy)
        * [Concatenated Bundling](#concatenated-bundling)
        * [Import-Traced Bundling](#import-traced-bundling)
        * [Transpiled Bundling](#transpiled-bundling)
    * [Render baseline HTML with Django](#render-baseline-html-with-django)
    * [Enhance baseline HTML with Vue](#enhance-baseline-html-with-vue)
* [2-server approach](#2-server-approach)
* [Conclusion](#conclusion)

{% endcapture %}

<div class="toc toc-floating">
  {{ toc_content | markdownify }}
</div>

[Vue] and [Django] are both fantastic for building modern web apps - bringing declarative functional reactive programming to the frontend, and an integrated web app platform, ecosystem, and battle-hardened ORM to the backend. However they can be somewhat tricky to use *together*. 

Here I'd like to show some approaches for setting Vue and Django up in combination for both new web apps and existing Django-based web apps. I've been building web apps with Django for ~6 years and with Vue for ~3 years, and in particular I've extensively tested the [1&#8209;server]&nbsp;[concatenated bundling] approach described below in production.<br clear="both" />

[Vue]: https://vuejs.org/v2/guide/
[Django]: https://www.djangoproject.com/
[1&#8209;server]: #1-server-approach
[concatenated bundling]: #concatenated-bundling

<a name="1-server-or-2-servers"></a>
# 1 server or 2 servers?

The first question to consider when planning to use Django and Vue together is whether to use a single server that serves both backend endpoints and frontend assets, or to use two different servers, one to host the frontend and a separate "API server" to host the backend.

<a href="/assets/2021/vue-and-django/1-server-vs-2-server.svg">
    <img alt="Diagram: 1-server vs 2-server setup" src="/assets/2021/vue-and-django/1-server-vs-2-server.svg" style="max-width: 100%;" />
</a>

Factors in favor of a 1-server setup:

* **Operational maintenance costs** are significantly simplified with only a single server to deploy, monitor, and manage.
* Relegating Django's role to only that of an API server - in the 2-server setup - will complicate or even prevent you from using any **Django features or third-party apps that rely on server-side rendering by Django**, such as its famous built-in administration interface. Instead you'll be doing most of your server-side rendering with some JavaScript framework that is Node-compatible. And Node-based server-side rendering is generally rather complex to setup.

Factors in favor of a 2-server setup:

* If you want to use the latest and greatest version of JavaScript, with transpilation and module bundling, the 2-server setup has **great community documentation for setting up a frontend server and build pipeline that supports all of these new JavaScript features**.
    * However most of those features can *still* be obtained in a single-server setup with some effort, as described later in this article.
* If your organization already has **separate frontend and backend teams**, it may be easier to have 2 servers - one managed by the frontend team, and one managed by the backend team - to allow each team to focus on each server separately (and satisfy Conway's Law [^conways-law] 🙂).
* If your organization already has a **separate operations team** that has the capacity to manage the additional server implied by a 2-server setup, then the additional operational overhead may be acceptable.

[^conways-law]: [Conway's Law](https://en.wikipedia.org/wiki/Conway%27s_law): The technical architecture of a system tends to mirror the organizational and communication structure of the people that build it. So if you have 2 teams building a compiler, they're likely to build a 2-pass compiler. Similarly if you have a frontend and a backend team, they're likely to build separate frontend and backend servers if left to themselves.

At my company we went with the single server option because our engineering team is small (< 5 engineers) - so we care a lot about minimizing operational overhead - and is composed of full-stack generalists who are familar with both backend and frontend technologies - so we have engineers that can work anywhere in the stack but aggressively prefer *simple* architechures that don't require extreme specialization in multiple domains.

In the next section I'll drill down into the 1-server approach, but you can also skip to the [2-server approach] if that's what you're leaning toward.

[2-server approach]: #2-server-approach

<a name="1-server-approach"></a>
# 1-server approach

When using a single server, you'll need to:

* pick an asset [bundling strategy], 
* [render SEO-friendly HTML server-side] with critical navigation and content available immediately on page load, and 
* [enhance that HTML client-side with Vue after page load] with additional dynamic content.

[bundling strategy]: #bundling-strategy
[render SEO-friendly HTML server-side]: #render-baseline-html-with-django
[enhance that HTML client-side with Vue after page load]: #enhance-baseline-html-with-vue

<a name="bundling-strategy"></a>
## Bundling strategies

When using a single integrated Django server to not only host your backend but also serve your frontend, you'll need to decide how you want to bundle your JavaScript assets on the frontend together. **Bundling of some kind is necessary for a production deployment** that is fast enough to be mobile-friendly and usable by distant international customers who may not have fast network connectivity to your server.

There are multiple bundling techniques that can be used with Django, with various pros and cons:

* [Concatenated Bundling],
* [Import-Traced Bundling], and
* [Transpiled Bundling].

[Concatenated Bundling]: #concatenated-bundling
[Import-Traced Bundling]: #import-traced-bundling
[Transpiled Bundling]: #transpiled-bundling


<a name="concatenated-bundling"></a>
### Concatenated Bundling

<a href="/assets/2021/vue-and-django/bundling-strategies/concatenated.svg">
    <img alt="Diagram: Concatenated Bundling Strategy" src="/assets/2021/vue-and-django/bundling-strategies/concatenated.svg" class="bundling-diagram" />
</a>

This is by far the easiest bundling technique to use with Django and is a good technique to start with.

With concatenated bundling, you write JavaScript files that consist entirely of top-level function definitions and other non-executable code. Your HTML template served by Django contains `<script>`-includes of every JavaScript file that the current page requires, directly or transitively. And after all JavaScript files are included the HTML page uses an inline `<script>` to call the root JavaScript function which sets up the rest of the page:<br clear="both" />

{% capture code %}{% raw %}<!-- todo/templates/todo/todo.html -->
<!DOCTYPE html>
<html>
<head>...</head>
<body>...</body>
{% compress js %}
    <script src="{% static 'todo/todo.js' %}"></script>
    <script src="{% static 'todo/todo/list.js' %}"></script>
    <script src="{% static 'todo/todo/item.js' %}"></script>
    <script>
        setupTodoPage();
    </script>
{% endcompress %}
</html>
{% endraw %}{% endcapture %}
<pre><code>{{ code | replace: "<", "&lt;" | replace: ">", "&gt;" }}</code></pre>

> Note: The {% raw %}`{% compress js %}`{% endraw %} tag above assumes that you are using the excellent [Django Compressor] library which integrates well with Django as your concatenating bundler.

[Django Compressor]: https://django-compressor.readthedocs.io/en/stable/

Pros of concatenated bundling:

* **Very easy to setup.** Leverages excellent documentation from the Django Compressor library.
* **Zero bundle build times during development.**
* Fastest bundle build times during deployment, compared with other approaches.[^fastest-build-times]

[^fastest-build-times]: At the time of writing it takes 2.1 seconds for me to bundle 100,650 lines (5,304 KiB) of JS and 17,617 lines (699 KiB) of CSS using Django Compressor's default settings which uses [rJSMin](http://opensource.perlig.de/rjsmin/) to minify JS (via [regex](https://stackoverflow.com/a/1732454/604063) no less!).

Cons of concatenated bundling:

* You must manage your JS dependencies in HTML manually:
    * Whenever adding a new JS module you must remember to add it to the HTML for the appropriate page(s).
    * If you alter an existing JS module to depend on a new JS module, you must find all page HTMLs that include the first module and update them to include the second module if needed.
    * If you want to avoid managing JS dependencies manually, consider [import-traced bundling] instead.
* JavaScript files are not transformed or transpiled in any way, so if you want to use newer JavaScript features that aren't supported by your customers' browsers then you're out of luck. If you need transpilation consider the [transpiled] or the [2-server] approaches instead.
* It is awkward to define a class in a JavaScript module that inherits from a base class in a different module, because that *requires* `<script>`-including the base class's module first, breaking the usual rule that "the order that JS files are imported should not matter". (However if you just limit inheritance to be within a single module or avoid it entirely, then this restriction doesn't matter in practice.)

Note that choosing concatenated bundling does *not* prevent you from using TypeScript-based type checking in your JS files, which I *do* recommend for long-lived projects. In short, you can put a special `// @ts-check` comment at the top of a JS file to [enable type-checking of JS with the TypeScript compiler] (`tsc`). <!-- Using TypeScript to type-check JS files doesn't seem like a very-well known technique, so I plan to write a future article about it. -->

[transpiled]: #transpiled-bundling
[2-server]: #2-server-approach
[import-traced bundling]: #import-traced-bundling
[enable type-checking of JS with the TypeScript compiler]: https://www.typescriptlang.org/docs/handbook/intro-to-js-ts.html


<a name="import-traced-bundling"></a>
### Import-Traced Bundling

<a href="/assets/2021/vue-and-django/bundling-strategies/import-traced.svg">
    <img alt="Diagram: Import-Traced Bundling Strategy" src="/assets/2021/vue-and-django/bundling-strategies/import-traced.svg" class="bundling-diagram" /> 
</a>

With the advent of the [Snowpack] bundler we can get all the benefits of the [concatenated bundling] approach while eliminating the need to manage JS dependencies manually, at the cost of a slightly-more-complex deployment process.

[Snowpack]: https://www.snowpack.dev/
[concatenated bundling]: #concatenated-bundling

With import-traced bundling, you write a root JavaScript file for each page that uses regular [JavaScript import statements] to bring in related modules. Your HTML template then only needs to include the root JavaScript file:<br clear="both" />

[JavaScript import statements]: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/import

{% capture code %}{% raw %}<!-- todo/templates/todo/todo.html -->
<!DOCTYPE html>
<html>
<head>...</head>
<body>...</body>
<!-- js -->
    <script type="module">
        import { setupTodoPage } from "{% static 'todo/todo.js' %}";
        setupTodoPage();
    </script>
<!-- endjs -->
</html>
{% endraw %}{% endcapture %}
<pre><code>{{ code | replace: "<", "&lt;" | replace: ">", "&gt;" }}</code></pre>

The root JavaScript file might look like:

{% capture code %}{% raw %}// static/todo/todo.js
import { defineTodoList } from "./todo/list.js";

export function setupTodoPage() {
    defineTodoList();
    ...
}
{% endraw %}{% endcapture %}
<pre><code>{{ code | replace: "<", "&lt;" | replace: ">", "&gt;" }}</code></pre>

And that root JS file can include other modules like:

{% capture code %}{% raw %}// static/todo/list.js
import { defineTodoItem } from "./item.js";

export function defineTodoList() {
    defineTodoItem();
    
    Vue.component('todo-list', {
        props: {
            ...
        },
        template: `
            ...
        `,
        methods: {
            ...
        }
    });
}
{% endraw %}{% endcapture %}
<pre><code>{{ code | replace: "<", "&lt;" | replace: ">", "&gt;" }}</code></pre>

Some key differences between import-traced bundling and concatenated bundling:

* The HTML page only needs to include the root JS file for the page and not any of its indirect JS dependencies.
* JS modules must use `import` to declare other JS modules that they depend on, and `export` any functions that they want to be importable by other modules.
* JS files for *all* Django apps in the Django project should be put in a common `static` directory rather than using per-app `static` directories. Having a common directory for all JS files will make it easier to configure Snowpack to build combined JS bundles for production deployments.
* There is no longer a need to use Django Compressor.

For a production deployment, you'll need to alter your deployment script to run Snowpack on the root `static` directory for the Django project, enumerating the set of root JS files, and generating same-named files for deployment to your static asset server.

Pros of import-traced bundling:

* **Easy to setup for development.** (Trickier to setup for deployment.)
* **Zero bundle build times during development.**
* Fast bundle build times during deployment.
* **JS dependencies are automatically managed** through regular `import` statements in JS.

Cons of import-traced bundling:

* JavaScript files are not transpiled at *development time* (although they *are* at deployment time), so if you want to use the most bleeding-edge JavaScript features that aren't even supported by your development browser then you're out of luck. If you need transpilation during development consider the [transpiled] or the [2-server] approaches instead.
* Requires that your development browsers [support JavaScript import] and JS modules in general.

[support JavaScript import]: https://caniuse.com/mdn-javascript_statements_import


<a name="transpiled-bundling"></a>
### Transpiled Bundling

<a href="/assets/2021/vue-and-django/bundling-strategies/transpiled.svg">
    <img alt="Diagram: Transpiled Bundling Strategy" src="/assets/2021/vue-and-django/bundling-strategies/transpiled.svg" class="bundling-diagram bundling-diagram-wide" />
</a>

If you want the latest and greatest JavaScript features that haven't made it even to your latest *development* browser (ex: the latest Chrome or Firefox) then you'll need to pay the cost of needing to transpile during development time:

The transpiled bundling approach generally uses the same kind of HTML, JS, and filesystem structure as the [import-traced bundling] approach but you have additional flexibility depending on the particular set of bundler and transpiler tools you select.

[import-traced bundling]: #import-traced-bundling

Common choices for transpiler tools as of early 2021 are [Webpack], [Babel], and [TypeScript].

[Webpack]: https://webpack.js.org/
[Babel]: https://babeljs.io/
[TypeScript]: https://www.typescriptlang.org/

For a sketch of how you might wire these tools together, take a look at Jacob Kaplan-Moss's [thoughts on the transpiled bundling approach at PyCon 2019].

[thoughts on the transpiled bundling approach at PyCon 2019]: https://youtu.be/E613X3RBegI?t=1203

Pros of transpiled bundling:

* **Latest bleeding-edge JavaScript features are available.**
* **JS dependencies are automatically managed.**
    * You can also manage dependencies automatically with the simpler [import-traced bundling] approach.

Cons of transpiled bundling:

* **Moderate-to-slow bundle build times during development.**
    * You can eliminate build times during development entirely using either the [import-traced bundling] or [concatenated bundling] approaches.
* Slow bundle build times during deployment, assuming you enable aggressive optimizations.


<a name="render-baseline-html-with-django"></a>
## Render baseline HTML with Django

Now that you've picked a [bundling approach], we can move on to rendering our first page with Django and Vue.

[bundling approach]: #bundling-strategy

When a browser (or search engine crawler) first requests a page from your site, it will only be able to immediately render the initial HTML served by Django. In particular, browsers will take some time to start running any JavaScript on your HTML page, so it's important that the initial HTML served by Django contains your most important page content.

For example if we were building the product page of an online store, we'd want to ensure the initial HTML rendered by Django immediately contained things like:

* the site logo and top navigation links,
* the product image,
* the product description,
* placeholders for other less-important panels that are okay to load later in JavaScript, with appropriate animated spinner icons or other loading indicators.

<!-- (TODO: Diagram: Example product page after initial page load) -->

So the HTML rendered by Django might look something like:

{% capture code %}{% raw %}<!-- store/templates/store/product.html -->
<!DOCTYPE html>
<html>
<head>...</head>
<body>
    <!-- Top navigation -->
    <nav class="navbar navbar-inverse">
        <div class="container-fluid">
            <div class="navbar-header">
                <!-- Site logo -->
                <a class="navbar-brand" href="/">Acme Store</a>
            </div>
            <div class="navbar-collapse collapse">
                <!-- Top navigation links -->
                <ul class="nav navbar-nav">
                    <li><a href="/computer-systems/">Computer Systems</a></li>
                    <li><a href="/components/">Components</a></li>
                    <li><a href="/electronics/">Electronics</a></li>
                    ...
                </ul>
            </div>
        </div>
    </nav>
    
    <!-- Main content -->
    <div class="container">
        <div class="content-container">
            <!-- Primary panel -->
            <img alt="Product image" href="{{ product.image_url }}" style="float: left;" />
            <h1>{{ product.title }}</h1>
            <div>
                {{ product.description }}
            </div>
            
            <!-- Secondary panel; a placeholder filled out by JS later -->
            <div id="recommendations-panel">
                <h2>Recommended for You</h2>
                <img
                    v-if="loading" 
                    alt="Loading spinner"
                    src="{% static 'store/loading-spinner.gif' %}" />
                <template
                    v-else
                    v-cloak>
                    ...
                </template>
            </div>
        </div>
    </div>
</body>

{{ recommendations_panel_data|json_script:"recommendations-panel-data" }}

{% compress js %}
    <script src="{% static 'store/product.js' %}"></script>
    <script src="{% static 'store/product/recommendations.js' %}"></script>
    <script>
        setupProductPage();
    </script>
{% endcompress %}
</html>
{% endraw %}{% endcapture %}
<pre><code>{{ code | replace: "<", "&lt;" | replace: ">", "&gt;" }}</code></pre>

Notice that most of the page is initially rendered server-side with Django's built-in templating system and *not* with Vue. This server-side rendered content loads fast and can be appropriately indexed by search engines for better SEO.

However certain less-important panels like the Recommendations panel don't need to be loaded immediately and will be given life by Vue later after the page's JavaScript starts running. Let's consider how that works:

<a name="enhance-baseline-html-with-vue"></a>
## Enhance baseline HTML with Vue

When the browser (or search engine) first loads the Recommendations panel it will initially see just a loading spinner:

{% capture code %}{% raw %}<div id="recommendations-panel">
    <h2>Recommended for You</h2>
    <img
        v-if="loading" 
        alt="Loading spinner"
        src="{% static 'store/loading-spinner.gif' %}" />
    <template
        v-else
        v-cloak>
        ...
    </template>
</div>
{% endraw %}{% endcapture %}
<pre><code>{{ code | replace: "<", "&lt;" | replace: ">", "&gt;" }}</code></pre>

> Note: The `v-cloak` directive is associated with the CSS rule `[v-cloak] { display: none; }` so nothing marked by that directive will be displayed initially.

Later when the page's JavaScript starts running, it will call `setupProductPage()`:

```
// store/product.js
/*public*/ function setupProductPage() {
    setupRecommendationsPanel();
}
```

which will call `setupRecommendationsPanel()`:

```
// store/product/recommendations.js
/*public*/ function setupRecommendationsPanel() {
    new Vue({
        el: '#recommendations-panel',
        data: function() {
            return document.querySelector('#recommendations-panel-data').innerText;
        },
        computed: {
            loading: function() {
                ...
            },
            ...
        },
        methods: {
            ...
        }
    });
}
```

which will use Vue to render the interior of the panel, perhaps after performing an Ajax request back to a Django endpoint to fetch more data.

> Notice that some data for the panel can be prepopulated in HTML via the `{% raw %}{{ ...|json_script:"..." }}{% endraw %}` template tag by Django and then fetched later via `document.querySelector(...).innerText` in JavaScript.

Done! Skip to the [conclusion].

[conclusion]: #conclusion


<a name="2-server-approach"></a>
# 2-server approach

When using a separate frontend server for Vue and a separate backend server for Django, you'll need to:

* setup [a standalone Vue server] and [a standalone Django server] using official documentation from each project,
* alter the frontend Vue server to [support server-side rendering or prerendering] using official documentation,
* create some pages in Vue, some endpoints in Django (perhaps using the [Django REST Framework]), and have those pages access those routes using plain old [window.fetch()]&nbsp;(or something shinier like [Axios]).

[a standalone Vue server]: https://v3.vuejs.org/guide/installation.html#installation
[a standalone Django server]: https://www.djangoproject.com/start/
[support server-side rendering or prerendering]: https://ssr.vuejs.org/#why-ssr
[Django REST Framework]: https://www.django-rest-framework.org/
[window.fetch()]: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
[Axios]: https://github.com/axios/axios#readme


<a name="conclusion"></a>
# Conclusion

Hopefully this guide has been useful in helping you setup Vue inside your new or existing Django web app. Happy coding!


## *Related Articles*

* [Database clamps](/articles/2021/02/09/database-clamps-deterministic-performance-tests-for-database-dependent-code/) - Writing deterministic performance tests for database-dependent code in Django
* [Tests as Policy Automation](/articles/2021/02/02/tests-as-policy-automation/) - Has ideas for creatively using automated tests to enforce various (non-functional) properties in your Django web app.
* Other {% assign tag = 'Django' %}{% include blocks/tag_single %} articles


## *Related Projects*

* [TechSmart Platform](/projects/techsmart-platform) - Large web app that I work on that uses Django and Vue. (Sorry it’s closed-source!)
