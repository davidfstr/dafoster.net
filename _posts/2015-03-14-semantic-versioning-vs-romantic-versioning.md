---
layout: post
title: "Semantic Versioning vs. Romantic Versioning"
tags: [Software]

---

In recent years the larger software development community has started to pay more attention to version numbers.

## Semantic Versioning

The Node community in particular has introduced specific guidelines for what it means when you increment various parts of a version number. Generally:

* A version number is a 3-part value **X.Y.Z** where **X, Y**, and **Z** are the **major**, **minor**, and **patch** components respectively.
* When making a new release that contains **bug fixes only**, you may increment the patch component.
    * `X.Y.Z -> X.Y.(Z+1)`
* When making a new release that contains **new features** (and possibly some bug fixes) but not breaking changes, you may increment the minor component (and reset the patch component to zero).
    * `X.Y.Z -> X.(Y+1).0`
* When making a new release that contains **breaking changes** (and possibly some new features or bug fixes), you may increment the major component (and reset both the minor and patch components to zero).
    * `X.Y.Z -> (X+1).0.0`

This scheme for version numbering, called **[semantic versioning]** (or SemVer), is easy for automatic dependency management systems to understand, making it highly useful for communities that encourage liberal use of third-party libraries.

[semantic versioning]: http://semver.org

### When to use Semantic Versioning

Use of semantic versioning is highly recommended for projects that are intended to be depended on and automatically upgraded, such as:

* **libraries** (ex: jQuery, Underscore, requests, libxml2).

Semantic versioning is also useful for slower-moving projects that may require some manual upgrade steps, such as:

* **frameworks** (ex: Django, Ruby on Rails, Spring);
* **language platforms** (Java, C#, Python, Ruby);
* **runtime platforms** (ex: JVM, CLR, CPython, MRI); and
* **OS platforms** (ex: OS X, Windows, Debian).

Using semantic versioning makes it easy for high-level projects to regularly upgrade their lower-level dependencies, either automatically or manually.

## Romantic Versioning

By contrast, I use the term **romantic versioning**[^sentimental-versioning] to refer to all other version numbering schemes that adhere to the following fuzzy guidelines:

* A version number is a multi-part value such as **X**, **X.Y**, or **X.Y.Z**; with numeric components.
* A *conceptually* major change bumps the first component of the value.
* A *conceptually* minor change or bug fix bumps a later component of the value.

Romantic versioning is meant primarily for *humans* to understand, at the possible expense of easy understanding by a computer. This makes it suitable for marketing purposes (since marketing is directed at humans) but often not suitable for automated dependency management (which is performed by a computer).

[^sentimental-versioning]: I have seen other people use different terms to refer to **romantic versioning**. For example Dominic Tarr calls such versioning schemes ["sentimental versioning"](http://sentimentalversioning.org). However he mainly mocks such schemes, highlighting the negative aspects of romantic versioning as perceived by a developer without considering the positive aspects for marketing to consumers.

### When to use Romantic Versioning

As mentioned before, romantic versioning is mainly suitable for projects that are actively marketed and updated over time but not depended on by other projects, such as:

* **applications** (Microsoft Word, Firefox, Spotify, Evernote).

Some projects are not updated over time (such as many console games) and so have no version number at all.

## Hybrid Romantic & Semantic Versioning

There are many projects that maintain two different version numbers simultaneously: a romantic version for marketing purposes and a semantic version for developer purposes. For example:

* Java
    * Currently at "product version" `8.40` ("Java SE 8u40"), which is the romantic version; and "developer version" `1.8.40`, which is the semantic version.
* Windows
    * At marketing version `7` ("Windows 7"), which is the romantic version; and at internal version `6.1`, which is the best approximation of its semantic version.

There are also some libraries that advertise a romantic version as if it were a semantic version which causes [lots of problems] when automated dependency management systems try to consume the library.

[lots of problems]: https://github.com/jashkenas/underscore/issues/1805

## Final Observations

* Projects typically[^unversioned-esoteric] have a **romantic version**, a **semantic version**, or both.
* Applications tend to have a **romantic version** only, since they are marketed to consumers rather than developers.
* Libraries tend to have a **semantic version** only, since they are used only by automated tooling and developers.
* Other types of projects like frameworks and platforms have more variation, often providing both a romantic and semantic version since they are often both marketed to consumers and used by developers.

---

Enjoy this article? Follow my [Twitter account](https://twitter.com/davidfstr) for notifications of new articles. 😃

### *Related Articles*

* [Unique Features of Various Programming Languages](/articles/2013/01/29/unique-features-of-various-programming-languages/)
    * *Describes programming languages and their unique features.*
* [Visual Guide to Programming Language Properties](/articles/2013/02/20/visual-guide-to-programming-language-properties/)
    * *Visualizes how various programming language properties interact.*


[^unversioned-esoteric]: Projects that receive no updates are **unversioned**, with no version number, such as many console games. And a small number of projects use an **esoteric versioning** scheme, with version numbers that are hard to interpret by either human or computer. For example successive version numbers of [TeX](https://en.wikipedia.org/wiki/TeX) are closer and closer approximations of π.
