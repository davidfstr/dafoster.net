# Website 3.0

This is the personal website of [David Foster].

## Why should I care?

You may be interested in reading the source code if you want an **example of 
how a complex [Jekyll] site is structured**. Notable features include:

* **[breadcrumbs]** on all pages
* **clean URLs** that lack file extensions (or query parameters)
* **advanced Markdown** with footnotes and multi-level bulleted lists
* **deployment automation** to [GitHub Pages] via [git]
* a **[tag index]** for blog posts
    * ...including anchor-based header highlighting

Have specific questions about how these were implemented? [Contact me].

[David Foster]: https://github.com/davidfstr
[Jekyll]: https://github.com/mojombo/jekyll
[breadcrumbs]: http://en.wikipedia.org/wiki/Breadcrumb_(navigation)
[git]: http://git-scm.com
[GitHub Pages]: http://pages.github.com
[tag index]: http://dafoster.net/articles/topics/#Software
[Contact me]: http://dafoster.net/contact/

## Installation

* Install Jekyll.
    * If you already have this installed, you may need to upgrade
      RDiscount to version 2.0.7 or later with `gem update rdiscount`.

```
gem install jekyll
```

* Download the site source:

```
git clone https://github.com/davidfstr/dafoster.net
cd dafoster.net
```


## Usage

##### Run local webserver with the website at: <http://127.0.0.1:4000/>

```
rake
rake prism   # Optional. Run this in a different terminal window.
```

##### Compile to `_site` directory in production mode

```
rake dist
```

##### Deploy to GitHub Pages

```
rake deploy
```

## License

Copyright &copy; 2013 by David Foster. All rights reserved.