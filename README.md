# Website 3.0

This is the personal website of [davidfstr](https://github.com/davidfstr).

## Installation

* Install custom RDiscount with footnotes support.

```
cd /tmp
git clone https://github.com/davidfstr/rdiscount
cd rdiscount
gem build rdiscount.gemspec
gem install rdiscount-1.6.8.gem 
```

* Install Jekyll.

```
gem install jekyll
```

## Usage

* Run local webserver with the website: <http://127.0.0.1:4000/>

```
jekyll --server
```