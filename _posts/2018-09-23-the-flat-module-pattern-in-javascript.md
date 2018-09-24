---
layout: post
title: The Flat Module Pattern in JavaScript
tags: [Software]
x_target_audience: [Full-Stack Software Engineers, Frontend Software Engineers]

---

There are several patterns for structuring modules in JavaScript. The most common ones I see talked about is the original [JavaScript Module Pattern], [AMD Modules], [CommonJS Modules], and the emerging [Harmony Modules].

The large JavaScript application that I work on at work - an in-browser IDE - does not presently use any of these well-known patterns but instead uses what I'm going to call the **Flat Module Pattern**.

## The Flat Module Pattern

Here's what the Flat Module Pattern looks like, for an excerpt of a real module called `save.js`:

```
/*public*/ function setupSave() {
    if (isMainOrStandaloneWindow()) {
        setupSaveToken();
    }
}

// -----------------------------------------------------------------------------
// Autosave

var DELAY_AFTER_TYPING_STOPS_TO_AUTOSAVE = 2000;

/*public*/ function autosave(fileInfo) {
    ...
}

// -----------------------------------------------------------------------------
// Save Token

function setupSaveToken() {
    ...
}

/*public*/ function isUnsafeToSave() {
    ...
}

// -----------------------------------------------------------------------------
```

Notice that:

* Only function and constant declarations exist at the top-level. No other executable code may run at the top-level.
* Public functions are marked with the keyword-comment `/*public*/`. A module should not attempt to reference a non-public method in a different module.
* Modules do not import each other or declare cross-module dependencies explicitly.

Consequences of this pattern:

* Modules can be `<script>`-included in any order, since there are no side-effects of including a module.
* All functions are dumped into the global namespace.
    * In practice this is not a problem since well-named application functions have distinct names from other application functions, and libraries don't generally dump functions directly into the global namespace.

All such modules on a particular page are directly included by the HTML page:

{% raw %}

```
{% compress js %}
    <!-- Library -->
    <script src="{% static 'tsk_platform/student_survey.js' %}"></script>
    <script src="{% static 'tsk_platform/util/dialog.js' %}"></script>
    <script src="{% static 'tsk_platform/util/markdown.js' %}"></script>
    <script src="{% static 'tsk_platform/util/slider.js' %}"></script>
    <script src="{% static 'tsk_platform/util/url.js' %}"></script>
    <script src="{% static 'tsk_platform/util/websocket.js' %}"></script>
    <script src="{% static 'tsk_platform/vendor/jquery.min.js' %}"></script>
    <script src="{% static 'tsk_platform/vendor/mdl/material.min.js' %}"></script>

    <!-- Page-Specific -->
    <script src="{% static 'ide/code/__init__.js' %}"></script>
    <script src="{% static 'ide/code/panels/__init__.js' %}"></script>
    <script src="{% static 'ide/code/panels/assignment/__init__.js' %}"></script>
    <script src="{% static 'ide/code/panels/assignment/code_comprehension.js' %}"></script>
    <script src="{% static 'ide/code/panels/assignment/code_writing.js' %}"></script>
    <script src="{% static 'ide/code/panels/code_instructions.js' %}"></script>
    <script src="{% static 'ide/code/panels/project.js' %}"></script>
    <script src="{% static 'ide/code/panels/slides.js' %}"></script>
    <script src="{% static 'ide/code/run/__init__.js' %}"></script>
    <script src="{% static 'ide/code/run/engine/java.js' %}"></script>
    <script src="{% static 'ide/code/run/engine/python.js' %}"></script>
    <script src="{% static 'ide/code/run/run_window.js' %}"></script>
    <script src="{% static 'ide/code/tabs/__init__.js' %}"></script>
    <script src="{% static 'ide/code/tabs/editor/blocks.js' %}"></script>
    <script src="{% static 'ide/code/tabs/editor/font.js' %}"></script>
    <script src="{% static 'ide/code/tabs/editor/image.js' %}"></script>
    <script src="{% static 'ide/code/tabs/editor/scene.js' %}"></script>
    <script src="{% static 'ide/code/tabs/editor/sound.js' %}"></script>
    <script src="{% static 'ide/code/tabs/editor/text.js' %}"></script>
    <script src="{% static 'ide/code/tabs/save.js' %}"></script>
    <script>
        setupCodePage();
    </script>
{% endcompress %}
```

{% endraw %}

In considering how modules may reference members of each other:

* Page-specific modules may freely reference members from each other and from library modules.
* Most library modules are self-contained and do not reference members from anybody, although some library modules may reference members from other library modules.

The Flat Module Pattern is incredibly simple to follow, with almost no boilerplate. It is also easy to concatenate and minify.

My team has been using this pattern successfully over the last 4 years or so with a codebase that is now approximately 55,000 lines of JavaScript. I'm pretty happy with it.

## The Encapsulated Flat Module Pattern

The one major drawback of the above Flat Module Pattern is that public functions are advisory-only since they are just marked with `/*public*/` comments. It is still possible (and easy) to accidentally improperly reference a non-public function from outside the module it is declared in.

So here's an enhanced variation I call the **Encapsulated Flat Module Pattern** that doesn't have that problem:

```
(function() {
    function public(func) { window[func.name] = func; }

    public(function setupSave() {
        if (isMainOrStandaloneWindow()) {
            setupSaveToken();
        }
    });

    // -----------------------------------------------------------------------------
    // Autosave

    var DELAY_AFTER_TYPING_STOPS_TO_AUTOSAVE = 2000;

    public(function autosave(fileInfo) {
        ...
    });

    // -----------------------------------------------------------------------------
    // Save Token

    function setupSaveToken() {
        ...
    }

    public(function isUnsafeToSave() {
        ...
    });

    // -----------------------------------------------------------------------------
})();
```

Notice that each `/*public*/` advisory comment has been replaced with a call to a special `public(...)` function that actually exports the provided function. Any function that is not marked as public is truly private and not available for reference by other modules.

Benefits of this pattern:

* Public functions are easy to distinguish from private functions at their definition site.
* Public functions and private functions can be freely interleaved. In particular there is no need to group public functions in the module together.
* Public and private functions in the same module can call each other naturally and with the same syntax. In particular public functions do not have a special calling convention.
* No function names are duplicated by the boilerplate. In particular there's no need to repeat function names in a public exports list, as is common with other JavaScript module patterns.
* It is easy to convert a function from private to public or visa-versa. In particular no references need to be updated since public and private functions are referenced the same way.

## Conclusions

I've found these JavaScript module patterns to be very useful in structuring JavaScript application code I've written over the last few years.

I think these patterns would work well in any large JavaScript application that avoids class inheritance[^inheritance] and has reasonable non-colliding public function names.

I do *not* think these patterns would be a good idea for JavaScript *libraries* that need to avoid polluting the global namespace. For such libraries, falling back on the [Universal Module Definition] pattern seems more prudent. 


[JavaScript Module Pattern]: http://www.adequatelygood.com/JavaScript-Module-Pattern-In-Depth.html

[AMD Modules]: https://addyosmani.com/resources/essentialjsdesignpatterns/book/#detailamd

[CommonJS Modules]: https://addyosmani.com/resources/essentialjsdesignpatterns/book/#detailcommonjs

[Harmony Modules]: https://addyosmani.com/resources/essentialjsdesignpatterns/book/#detailharmony

[Universal Module Definition]: https://github.com/umdjs/umd

[^inheritance]: Supporting class inheritance requires serializing the order of top-level definitions since the definition of a subclass depends of the definition of its superclass, and therefore subclasses must be declared *after* its related superclass. The module patterns in this article do not serialize top-level definition order and therefore cannot reliably support subclasses being declared in a different module than its superclass.