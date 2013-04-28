---
layout: project
title: RDiscount
summary: >
    Converts Markdown text to HTML, in Ruby.
    Includes many useful Markdown extensions.
x_started_on: Jan 19, 2013
x_ended_on: Ongoing
x_languages: [Ruby, C, Autoconf]
x_location: Cathode at /Users/davidf/Projects
featured: true

---

RDiscount converts documents in [Markdown] syntax to HTML.

It uses the excellent [Discount] processor by David Loren Parsens
for this purpose, and thereby inherits Discount's numerous useful
extensions to the Markdown language.

[Discount]: http://www.pell.portland.or.us/~orc/Code/discount/
[Markdown]: http://daringfireball.net/projects/markdown/

## Why use Discount? <small>(and RDiscount)</small>

Discount is fast and supports many useful extensions to the original Markdown language:

* [Footnotes] - from *PHP Markdown Extra*
* [Tables] - from *PHP Markdown Extra*
* Multi-level bulleted lists
* Images with sizes
    * `![GitHub Favicon](https://github.com/favicon.ico =16x16)` &rarr; ![GitHub Favicon](https://github.com/favicon.ico =16x16)
* Typographic substitutions with [SmartyPants]
    * Straight quotes (&quot; and &#39;) &rarr; “curly” quotes
* [...and more](http://www.pell.portland.or.us/~orc/Code/discount/#Language.extensions)

Discount 2.1.5 (soon to be supported in RDiscount) also has:

* Fenced code blocks
    * [backtick-delimited] – from *GitHub Flavored Markdown*
    * [tilde-delimited] – from *PHP Markdown Extra*

Some of these extensions are not enabled by default.
See usage instructions below to enable additional extensions.

[SmartyPants]: http://daringfireball.net/projects/smartypants/
[Footnotes]: http://michelf.ca/projects/php-markdown/extra/#footnotes
[Tables]: http://michelf.ca/projects/php-markdown/extra/#table
[backtick-delimited]: https://help.github.com/articles/github-flavored-markdown#fenced-code-blocks
[tilde-delimited]: http://michelf.ca/projects/php-markdown/extra/#fenced-code-blocks

## Installation

<pre>gem install rdiscount</pre>

Ruby 1.9.2 has a known issue with RDiscount. Please use Ruby 1.9.3 or later.

If you are creating a Heroku app that depends on RDiscount, you must specify
a Ruby version in your Gemfile since Heroku currently uses Ruby 1.9.2 by default.

## Usage <small>in Ruby and Jekyll</small>

### In Ruby

RDiscount implements the basic protocol popularized by RedCloth and adopted by BlueCloth:

<pre>
require 'rdiscount'
markdown = RDiscount.new("Hello World!")
puts markdown.to_html
</pre>

Additional extensions can be turned on when creating the RDiscount object:

<pre>
markdown = RDiscount.new("Hello World!", :smart, :filter_html)
</pre>

For a list of all possible extensions, see the instance attributes in the
[RDiscount class documentation].

Inject RDiscount into your BlueCloth-using code by replacing your bluecloth require statements with the following:

<pre>
begin
  require 'rdiscount'
  BlueCloth = RDiscount
rescue LoadError
  require 'bluecloth'
end
</pre>

### In Jekyll

In your site's `_config.yml` file, add the line:

<pre>
markdown: rdiscount
</pre>

To enable extensions, add the following section with the desired list of extensions:

<pre>
rdiscount:
  extensions:
    - autolink      # greedily urlify links
    - footnotes     # footnotes
    - smart         # typographic substitutions with SmartyPants
</pre>

For a list of all possible extensions, see the instance attributes in the
[RDiscount class documentation].

## Contributing

All development is coordinated on the [GitHub project page].

Please report bugs and feature requests on the [issue tracker].

[GitHub project page]: https://github.com/rtomayko/rdiscount
[issue tracker]: https://github.com/rtomayko/rdiscount/issues

[RDiscount class documentation]: http://rdoc.info/github/rtomayko/rdiscount/master/RDiscount