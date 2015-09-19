---
layout: post
title: "State of the Union in Programming Languages (2015)"
tags: [Software]

style: |
    /* Table layout */
    .post table {
        width: 100%;
        table-layout: fixed;
        overflow: hidden;
    }
    .post table tr th:first-child,
    .post table tr td:first-child {
        width: 25%;
    }
    .post table tr th,
    .post table tr td {
        width: 15%;
    }
    
    /* Table borders */
    .post table tr th:first-child {
        border: none;
    }
    .post table tr th,
    .post table tr td {
        border: 1px solid lightgray;
    }

---

Some programming languages are better at some tasks than others. Below I have presented my own assessment of how various languages stack up against each other for the following common classes of tasks:

* **Programmer-bound**: Degree of expressive power. Magnitude of what you can implement with a small development staff. Affected by design simplicity, platform stability, and library availability.
* **I/O-bound**: Suitedness for programs that spend most of their time performing I/O.
* **CPU-bound**: Suitedness for programs that spend most of their time calculating.

Additionally, some programming languages are on the rise or on the decline, for a wide variety of reasons. So I have also provided an assessment of:

* **Platform longevity**: Degree to which the language is likely to attract and retain people and resources.

The rating scale is:

* **Excellent** (+2)
* **Good** (+1)
* **Okay** (0)
* **Poor** (-1)
* **Fail** (-2)

### Application Domain / General Purpose

| &nbsp;                 | Python        | Java          | C#            | C             | C++           |
|------------------------|---------------|---------------|---------------|---------------|---------------|
| **Programmer-bound**   | Excellent     | Okay          | Okay[^2.1]    | Poor          | Okay[^2]      |
| **I/O-bound**          | Good          | Good          | Good          | Good          | Good          |
| **CPU-bound**          | Poor          | Good          | Good          | Excellent     | Excellent     |
| **Platform longevity** | Good          | Okay[^0]      | Excellent     | Excellent[^1] | Good          |

[^0]: Normally Good, but Oracle is a poor steward for the language.
[^1]: Cemented as the just-above-assembly language of all CPUs.
[^2]: Normally Poor, based on the language design, but has a good standard library and massive corporate support for tooling.
[^2.1]: Normally Good, but still leans verbose, similar to Java.

### Web Domain

| &nbsp;                 | JavaScript[^J]| PHP[^3]       | NodeJS        | Ruby          | Go            |
|------------------------|---------------|---------------|---------------|---------------|---------------|
| **Programmer-bound**   | Okay[^6]      | Okay[^9]      | Poor          | Good[^11]     | Okay          |
| **I/O-bound**          | ?             | ?             | Excellent     | Good          | Excellent     |
| **CPU-bound**          | Good[^7]      | ?             | Good[^4]      | Poor          | Excellent     |
| **Platform longevity** | Excellent[^8] | Good[^10]     | Good[^5]      | Good[^12]     | Okay          |

[^J]: Specifically JavaScript used on the frontend in a web browser.
[^3]: Is actually a Web Framework masquerading as a Programming Language.
[^4]: Normally Poor, but has highly performant VMs due to massive corporate support.
[^5]: Drafts off of JavaScript's popularity.
[^6]: Normally Poor, but has a huge number of external libraries and massive corporate support for tooling around inefficiencies in the language.
[^7]: Normally Poor, but has highly performant VMs due to massive corporate support.
[^8]: Cemented as the assembly language of the web browser.
[^9]: Normally Poor, but has easiest deployment model of any web framework.
[^10]: Normally Okay, but being propped up by cheap web hosting providers and an army of amateurs.
[^11]: Normally Excellent, due to massive community support, but degraded by platform instability and lack of language specification, which retards tooling development.
[^12]: Normally Okay, but being propped up by startups.

### Other Domains

| &nbsp;                 | Objective-C   | Haskell       | Perl          | Fortran       | Lua           |
|------------------------|---------------|---------------|---------------|---------------|---------------|
| **Domain**             | OS X, iOS     | Academia      | SysAdmin      | Computation   | Game Mods     |
| **Programmer-bound**   | Good[^14]     | Okay[^15]     | Good[^18]     | ?             | Good          |
| **I/O-bound**          | Good          | Poor[^16]     | Good?         | ?             | Good          |
| **CPU-bound**          | Excellent     | Good          | Poor?         | Excellent     | Good          |
| **Platform longevity** | Good          | Good[^17]     | Poor[^19]     | Good          | Okay          |

[^14]: Normally Okay, but has a top-class standard library.
[^15]: Normally Good, but degraded by impenetrable documentation and pervasive speculative generality.
[^16]: Normally Good, but degraded by making I/O difficult to perform.
[^17]: Normally Okay, but is being propped up by academia.
[^18]: Normally Excellent, but degraded by excessive redundant syntax.
[^19]: Normally Fail, but lives on as a preinstalled scripting language for Linux.

### Other Worthy-of-Consideration Languages

* Swift
* Clojure - a Lisp dialect
* OCaml
* Standard ML
* Ada
* Rust
* Idris
* Forth
