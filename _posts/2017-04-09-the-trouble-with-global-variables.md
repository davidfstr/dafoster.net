---
layout: post
title: The Trouble with Global Variables
tags: [Software]

---

You've probably heard that global variables are bad. Today I want to explain *why* they are problematic, with examples, and give some design alternatives where you might be tempted to use a global variable.

## What is a global?

A global is a variable from the environment that a function can directly read or write without going through a function parameter.

For example, here is a `warn` function that adds a warning message to a global warnings list.

```
warnings = []

def warn(message):
    warnings.append(message)
```

## When is it tempting to use a global?

Globals are tempting to use when there are a large number of related functions that need to read or write a common piece of information.

For example consider a parser that has a root `parse_calendar_file` function that calls a tree of subordinate functions to parse data from a YAML document into domain objects. Any of these subordinate functions may emit warnings.

![](/assets/2017/the-trouble-with-global-variables/parse_calendar_file.png)

## Why are globals problematic?

Globals create hidden dependencies that are difficult to discover and easy to propagate.

### Globals are hidden 

> Globals act as a kind of *hidden* parameter or return value of any function that uses them, which callers may be unaware of. Such global-dependent functions are fragile and easy to misuse.

A function that reads a global expects it to be in a particular state before the function is called. If it is not in the correct state, the function will misbehave. And yet you don't see the global mentioned in the function's parameter list.
  
A function that writes a global relies on the global to return information to the caller or an ancestor of the caller. And yet you don't see the global mentioned in the function's return value.
  
In fact to see whether a function depends on a global you *must* crack it open and examine its implementation. This breaks encapsulation, requiring you to inspect the function's private implementation and not just its public interface to discern how to use it properly. Thus functions that manipulate globals are easy to misuse.

### Globals are viral

> Globals silently infect both direct *and* indirect callers such that they have a dependency on the global, which new callers may be unaware of. Globals create spooky action at a distance.

In the parsing example above consider what would happen if you were to invoke a subordinate parsing function like `parse_bell_schedule` directly, without going through the root function that initializes the `warnings` global. Since the call tree of the subordinate function eventually reaches `warn`, which expects `warnings` to be initialized, calling the subordinate function directly will crash!
  
![](/assets/2017/the-trouble-with-global-variables/write_crashes.png)
  
It is not possible to read only the implementation of the subordinate function `parse_bell_schedule` to discern that it depends on the `warnings` global: you have to read the implementation of *every* function that it calls, directly or indirectly, to see whether it uses the global! This is a massive encapsulation violation of the entire call tree that leads to the global! Every function in the call tree becomes easy to misuse.

### Globals are thread-hostile

> Functions that depend on mutable globals directly or indirectly cannot be used safely in a multi-threaded program. Attempting to do so will create race conditions, garbage output, and crashes.

Consider what would happen if you had two threads that independently and simultaneously called the root function `parse_calendar_file`.
  
Say thread A gets halfway through parsing when B just starts parsing. Thread B will clobber thread A's version of the `warnings` global when it starts parsing. As thread A and B continue parsing, warnings from *both* threads will be mixed together into a nonsensical mishmash. After the first-finishing thread  destroys the global, the other thread may crash when it tries to doubly destroy the global. Either way both threads will either return bogus warnings or crash outright.

To make multi-threaded usage of `warnings` safe, it is necessary for there to be a separate version of `warnings` owned by each call tree or thread. Globals by definition are global in scope and are not themselves divisible into separate versions per call tree or thread.[^thread-local]

[^thread-local]: You can get around the natural thread-hostility of a global variable by wrapping its value in a **thread local**. A thread local is a little-known special kind of Cell object that stores an independent value depending on which thread it is accessed from. In Python see `threading.local`. In Java see `java.lang.ThreadLocal`.

## What can I use instead of a global?

Considering that the big issue with globals is that they are *invisible* and, well, *globally* scoped, let's consider alternatives that are actually *visible* and *more-tightly* scoped.


### Explicit Parameters

One way to eliminate a global variable is to just pass its value around as an explicit parameter.[^return-values]

This approach provides no encapsulation around the shared variable and doesn't allow you to easily add additional shared variables to the same function group. This approach is thus suited to when you explicitly don't want encapsulation, don't anticipate adding new shared variables, and don't want to change the variable itself, such as when you're passing a Whole Object around.

For our parsing example, we'll create a `warnings` parameter on all parsing functions:

![](/assets/2017/the-trouble-with-global-variables/explicit_parameters.png)

Our parsing example really wants some encapsulation around the shared `warnings` variable and is likely to want more shared variables later (like `errors`) so the explicit parameter approach is not appropriate here.

[^return-values]: If you need to *modify* the base of a shared variable when it is being passed around as an explicit parameter then you must *also* pass back the altered variable through the return value. However this gets unwieldly very fast. In such cases you probably want to either wrap the shared variable in a Cell so that you don't have to modify the variable itself or use a Context Object. If you truly must use explicit parameters and return values, such as in a functional language that disallows direct mutation of values, consider using the Monad pattern to reduce syntactic overhead.


### Context Objects

A Context Object bundles together a bunch of variables that are shared among a set of related functions as fields. The related functions then take the Context Object as an explicit parameter.

For our parsing example, we'll create a `WarningsContext` class which is then passed around among all parsing functions:
  
![](/assets/2017/the-trouble-with-global-variables/context_object.png)

It now becomes explicit as to which functions depend on the ability to issue warnings, at the cost of adding noise to the function signatures.

In our parsing example if a new caller was introduced that wanted to call the subordinate `parse_bell_schedule` function directly it would now be obvious that the caller would need to create and initialize a `WarningsContext` object first and pass it to the subordinate function. No more crashes. Nice.
  
Also notice that `WarningsContext` is sufficiently encapsulated to be usable by not just the calendar file parser code but also *reusable* by other code that wishes to generate warnings. Cool.

If there is a desire to add another variable that the parsing functions all depend on (like `errors`), it is easy to add it to the `WarningsContext` class which is already being passed around everywhere, and then rename the class to something more specific like `CalendarParsingContext`. However if you are using a very specific context name you probably want a Method Object instead...


### Method Objects

A Method Object is like a Context Object but is even more cohesive: it bundles together not only the shared variables but the functions themselves into a single class. This new class is instantiated internally by the root function and lives only for the duration of the original function call.[^method-object-name]

For our parsing example we'll create a `CalendarFileParser` class:

![](/assets/2017/the-trouble-with-global-variables/method_object.png)

A Method Object is especially useful when there are *many* variables that are used by the same set of cohesive functions and these variables are tightly bound to the functions themselves.

If we wanted to add an `errors` variable to the parsing functions here in addition to `warnings`, we'd just declare it as another field on `CalendarFileParser`. Easy.

[^method-object-name]: A Method Object gets its name from the fact that it exposes only a single public method and all of the other private methods and fields exist to serve that method.

## Ende

Hopefully this discussion has been useful in explaining why global variables are to be avoided and what design techniques can be used instead.

I anticipate the next few articles will continue on the theme of considerations and techniques when designing *large* software systems. Stay tuned.
