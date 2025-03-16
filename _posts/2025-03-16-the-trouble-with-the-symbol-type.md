---
layout: post
title: The trouble with the Symbol type
tags: [Software]

---

There are a few languages that offer **a symbol type**, notably JavaScript, Ruby, Lisp, and Erlang. A symbol is similar to a string but guarantees that only one copy of the symbol exists with the same value. In JavaScript you can create a symbol with the code:

```javascript
Symbol.for('hello')
// Symbol(hello)
```

**Symbols can be compared with each other for equality very quickly** because only the object references need to be compared; the values do not need to be compared. This high speed of comparison is the main advantage that symbols offer over strings.

However:

* Every symbol that is created must be added to a global registry of all symbols to ensure that it is unique. Since all symbols live in this global registry and there is no way to remove a symbol from the registry, **a symbol may never be garbage collected**.
* Because symbols live forever, **it is unwise to create a symbol from an arbitrary (unknown) string**, because doing so repeatedly will fill up memory with immortal symbol objects.
* Similarly it is **unwise to deserialize a symbol** from (untrusted) input because - again - doing so repeatedly will fill up memory with immortal symbol objects.

To avoid the above problems **I generally prefer using strings instead of symbols**. Strings can be freely serialized/deserialized safely and they can be garbage collected. Although strings cannot be compared with each other as fast as symbols can, they still compare very fast, especially for short strings.

## Related: Interned Strings

Some languages don't have a symbol type but do have **a string type that can be "interned"**, notably Java and Python. When a string is interned it is added to the global registry of all interned strings (if it wasn't there already) and the copy from the registry is returned.

Java's interned strings are immortal and are never garbage collected.

Python's interned strings are NOT immortal and will be garbage collected if no references to an interned string exist outside of the global registry.
