---
layout: project
title: TypedDict
subtitle: Structured Dicts for Python
summary: >
    Python typechecker support for recognizing structured dictionaries with specific
    named keys mapped to specific value types. Ubiquitous in JSON.
logo_filename: logo.svg
started_on: 2016-09-24
ended_on: 2017-01-22
featured: true
x_started_on_source: https://github.com/python/mypy/issues/985#issuecomment-249400784
x_ended_on_source: commit b3f571ab3af12d034d2143e4d8d00febc12f2784 in local git repo
x_languages: [Python]
x_lines_of_code: TBD
x_location: Cathode at /Users/davidf/Projects/0-META/ARCHIVE/2016+/2016/mypy

---
A TypedDict is a new kind of type recognized by Python typecheckers such as [mypy].
It describes a structured dictionary/map with an expected set of 
named string keys mapped to values of particular expected types.

Such structures are ubiquitous when exchanging JSON data,
which is common for Python web applications to do.

[mypy]: http://mypy-lang.org/

For example, a web API for fetching TV show ratings may return a JSON response that looks like:

```python
{
    "title": "Queen's Gambit",
    "stars": 5
}
```

That API probably always returns responses in a particular generic shape:

```
{
    "title": <some str>,
    "stars": <some int>
}
```

and that shape can be described by a `TypedDict` definition:

```python
from typing import TypedDict

class MediaRating(TypedDict):
    title: str
    stars: int
```

With that TypedDict definition in place, you can take any JSON value received from
that API and use it directly in Python, without any additional conversions
or additional parsing[^parsing]:

[^parsing]: If you want to be *sure* that a JSON-like value is actually in the format you're expecting you might consider using [`trycast(...)`](/projects/trycast/) to actually check the value's shape at runtime rather than trusting a regular `cast(...)`.

```python
import requests
from typing import cast

response_json = requests.get(
    'https://media-api.example.com/rating',
    data=dict(search="Queen's Gambit")
).json
media_rating = cast(MediaRating, response_json)  # free; always succeeds; trusts endpoint

print(f'Title: {media_rating['title']}')
print(f'Stars: {media_rating['stars']}')
```

And if you try to access a part of the API response that isn't defined in the
TypedDict definition, your typechecker will helpfully tell you that you made
a mistake:

```python
print(f'Stars: {media_rating['sars']}')  # error: TypedDict "MediaRating" has no key 'sars'
```

Having your program automatically checked for inconsistencies like this by
typecheckers is especially helpful to quickly detect the introduction of bugs
in large Python projects maintained by multiple people over a long period of time.


## Installation

TypedDict is included in the Python standard library as of Python 3.8, so all
you need to do is import it from the `typing` module:

```python
from typing import TypedDict
```

If you are using an earlier version of Python, install the `typing_extensions`
module using pip (via: `pip install typing_extensions`), and then you can
import it from there:

```python
from typing_extensions import TypedDict
```


## Usage

See the [mypy documentation for TypedDict], or the [PEP for TypedDict].

[mypy documentation for TypedDict]: https://mypy.readthedocs.io/en/stable/more_types.html#typeddict
[PEP for TypedDict]: https://www.python.org/dev/peps/pep-0589/


## History

[I] was initially motivated to create TypedDict because I wanted better 
typechecking support for describing and manipulating some very large structured 
dictionaries in the code managing the [TechSmart Platform]'s curriculum import 
process<!-- ...specifically calendar_file.py -->.

[I]: /about/
[TechSmart Platform]: /projects/techsmart-platform/

In Sep 2016 I started designing (and [naming]) what would become TypedDict on the
[typing issue tracker] and implementing on the [mypy issue tracker].
Big kudos especially to [Guido van Rossom](https://github.com/gvanrossum), 
[Jukka Lehtosalo](https://github.com/JukkaL), and
[Ivan Levkivskyi](https://github.com/ilevkivskyi) for providing design
and implementation feedback.

[typing issue tracker]: https://github.com/python/typing/issues/28
[mypy issue tracker]: https://github.com/python/mypy/issues/985
[naming]: https://github.com/python/typing/issues/28#issuecomment-249992739

Later, others in the mypy community continued to extend TypedDict, notably
adding [class-based syntax] and [total=False] support.

[class-based syntax]: https://github.com/python/typing/issues/28#issuecomment-254243330
[total=False]: https://github.com/python/mypy/issues/2632

Finally in Mar 2019 Jukka wrote up TypedDict as an official [PEP] for it to be 
standardized and added to the standard `typing` module in Python 3.8.

[PEP]: https://www.python.org/dev/peps/pep-0589/


## Learnings

This project is the first where I had detailed collaboration with others in
*design* while working in open source.
