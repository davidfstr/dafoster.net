---
layout: post
title: "Beautiful Code: SQLite"
tags: [Software]

---

It has been said that you can learn a lot from reading other people's high-quality software. So I gave it a try this weekend by reading the SQLite source.

SQLite is a lightweight embedded database that does not require a standalone server. It is designed to be reliable, highly portable, and require minimal administration.

SQLite has some of the [most rigorous testing methodology] I have seen in an open source project. Thus its true defect count is likely to be extremely low, making it high quality.

Such a high quality product probably contains useful patterns and techniques, some of which I could reuse in my own programs. So I decided to dive into the SQLite source and see what gems I could pull out. Here are my notes:

[most rigorous testing methodology]: https://www.sqlite.org/testing.html

## Architecture & Design

I started by reading the high-level design documentation. SQLite has exceptionally good documentation of this type.

* [Documentation Index] - *Root of all documentation.*

* [Architecture Documentation] - *Excellent overview of the architecture.*

* Query Planner Documentation - *Describes how prepared statements are executed.*
    * [The Virtual Database Engine]
    * [Virtual Machine Opcodes]

### Internal Tools of Note

#### [Fossil]

Distributed version control system used by SQLite. I've never heard of this. Beyond version control also provides bug tracking, a wiki, and a blog.

#### [Lemon]

A custom parser generator used by SQLite. Alternative to the old bison/yacc combination which has some improvements:

* Syntax that is less error-prone.
* Fast. Reentrant. Thread-safe.
* Easier to write parsers that avoid leaking memory upon error conditions.
    * Important since SQLite is serious about handling out of memory conditions.

#### [VFS]

OS abstraction layer. Despite the acronym (Virtual Filesystem), it is more than just filesystem manipulation routines.

[Fossil]: http://www.fossil-scm.org/index.html/doc/trunk/www/index.wiki
[Lemon]: http://www.sqlite.org/src/doc/trunk/doc/lemon.html
[VFS]: http://www.sqlite.org/vfs.html

## Implementation Notes

### table.c (sqlite3_get_table)

* This is the main entry point into the SQLite API.
  It executes a SQL statement and returns the result.

* First impression is that most methods have a lot of malloc-failed handling. And indeed if you read the testing procedures, they involve causing random malloc errors throughout the code, so there has to be handling for such errors.

* Hungarion notation is used as well. Ick. But at least it is consistent.
    * z = string
    * a = array
    * p = object pointer
    * n = int
    * x = function pointer

* `/* Assume 32-bit assignment is atomic */`
    * Interesting that such a property would be *consciously* relied on.

### legacy.c (sqlite3_exec)

* This is the legacy entry point into the SQLite API.
  It still exists and is actually used internally by the currently
  recommended API entry point (`sqlite3_get_table`).

* There are some odd syntactic conventions.
    * Multi-line comments use double-stars to prefix middle lines.
    * No space before closing `{`.
    * Spaces inside outer parentheses for most statements
      (`if`, `while`, `assert`) but not all (`for`).

* It appears that functions that begin with `sqlite3_` are public,
  whereas functions starting with `sqlite3` (no underscore) are private.


### vdbeapi.c (sqlite3_step)

* This function executes one or more instructions from the instruction list
  inside of a prepared SQL statement. The instruction is executed inside
  of the SQLite virtual database engine (VDBE), which is a virtual machine.
    * It has a lot of support code for EXPLAIN and profiling callbacks.
    * The meat of instruction execution is done by `sqlite3VdbeExec`.

* Contains own mutex implementation. (`sqlite3_mutex_enter`)

* Deals with a somewhat crazy circumstance: If the database schema changes
  in the middle of executing a (prepared) SQL statement, the statement is
  reprepared and rerun automatically.

* Generally there is good commenting for weird and backward-compatibility
  behaviors.

* Practically every function can fail. They all return an integer error code.
    * Some functions that operate on an in-out data structure will
      additionally store an error code (and message) in that structure.

### vdbe.c (sqlite3VdbeExec)

* This function executes as many instructions as possible from a prepared
  SQL statement. It contains the monsterous switch statement that 
  enumerates every possible opcode that can be executed.
    * Related reference documentation: [Virtual Machine Opcodes]
    * Related guide documentation: [The Virtual Database Engine]

### Future

* If I were to continue reading into the implementation,
  I think the opcodes that manipulate B-trees would likely be
  the most interesting ones to look at.

## Summary

This is a very high-quality C library.

* Internal commenting is good.
* Consistent syntax is used, despite being a bit odd IMHO.
* The guide-level documentation is wonderful.
* Error handling is air-tight and enforced by crazy amounts of test code. 
* The architecture provides good separation of roles and is easy to understand.
* Once again, the documentation is excellent.

And its design requirements show through in the implementation:

**Reliable**

* There is more than 1000 times as much test code as there is product code.
* 100% branch coverage. That's insanely good.
* Very crazy error classes such as out of memory errors, crashes, integer overflow are all considered and tested for.
    * Malloc checks are prevalent and handled.
    * Transactions, journaling, and related testing deal with crashes.

**Portable**

* The chosen language is C, which is highly portable when written in the appropriate style.
* The so-called VFS layer provides an OS abstraction. Thus porting to an OS mainly just involves writing a new implementation of this abstraction.
* All C files are combined into one giant C file before being sent to the compiler, which provides for better compile-time optimizations for dumber C compilers, which may occur on embedded systems.
* The database format does not depend on endianness or native data type sizes, making it suitable for cross-platform use.
* Very low memory configurations are available, making SQLite suitable for use on embedded devices such as cellphones.
* The code is in the public domain, which removes any licensing barriers.

**Simple**

* SQLite is embedded into the program that uses it, requiring no separate server. And no administration for such a server.
* Minimal schema is imposed by SQLite, distinguishing only between integers, reals, text, and blobs at a low level. And even so, a column's type is advisory only - you can store a value of any type in any column (except an `INTEGER PRIMARY KEY` column).

Of course being simple sacrifices certain other properties such as high concurrency and the ability to perform fine-grained access control (which requires administrability).




[Documentation Index]: http://www.sqlite.org/docs.html
[Architecture Documentation]: http://www.sqlite.org/arch.html
[The Virtual Database Engine]: http://www.sqlite.org/vdbe.html
[Virtual Machine Opcodes]: http://www.sqlite.org/opcode.html