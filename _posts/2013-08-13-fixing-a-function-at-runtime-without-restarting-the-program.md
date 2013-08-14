---
layout: post
title: Fixing a function at runtime without restarting the program
tags: [Software]

---

This weekend I spent some time writing programs that scrape the contents of various websites to extract information. One challenge when doing this is that webpages are a mess and the functions I wrote to parse the webpages would frequently crash due to some kind of unexpected input. So I decided I wanted a way to fix these functions at runtime without needing to restart the entire program.

So after hacking around with the Python debugger and employing some magic, I created a new function decorator called `@retriable`. This decorator drops into the debugger if a decorated function raises an exception, allowing you to inspect what caused the crash. Then you could fix the function in the source file and exit the debugger. Afterwards the function would be reloaded and called again with the same input as before, all without interrupting the overall program.

## Demo

Let's illustrate the decorator's use with the following program:

```
# flakey.py

from retriable import retriable

@retriable
def identity(input):
    if input in [5, 7]:
        raise ValueError('Could not understand input: %d' % input)
    return input
```

This contrived function is intended to return its input unmodified, but fails with certain inputs.

The above function will be exercised with the following main program:

```
# main.py

import flakey

for i in xrange(1, 10 + 1):
    print flakey.identity(i)
```

Let's try to run the main program:

```
$ python main.py
1
2
3
4
> /Users/davidf/Projects/scrape-tools/flakey.py(7)identity()
-> raise ValueError('Could not understand input: %d' % input)
(Pdb) 
```

Uh oh. The function crashed. Let's see what the input was:

```
(Pdb) input
5
(Pdb) 
```

Okay. Examining the function in `flakey.py` we see the if-statement that's causing `5` to fail. So we change it to read `if input in [7]:` to fix it and resave the file.

Having made our fix, we tell the debugger to exit, and instruct the next prompt to retry the function.

```
(Pdb) quit
[R]etry after reload, Rais[E], or [Q]uit? [R] r
5
6
> /Users/davidf/Projects/scrape-tools/flakey.py(7)identity()
-> raise ValueError('Could not understand input: %d' % input)
```

Now the function handled `5` but crashed on input `7`. Again we fix the function by removing the condition completely, leaving only: `def identity(input): return input`. Resaving and retrying the function gives:

```
(Pdb) quit
[R]etry after reload, Rais[E], or [Q]uit? [R] r
7
8
9
10
$ 
```

Nice. The program completed without interruption and we were able to fix the `identity` function along the way.

Although this example is contrived you could imagine saving a lot of time if the function to be fixed was moderately expensive and needed to be invoked hundreds of times by the original program instead of just a handful of times. In such cases restarting the entire program is rather expensive.

## The `@retriable` decorator

So, without further ago, here the `@retriable` decorator:

```
# retriable.py

import pdb
import sys

def retriable(func):
    """
    Marks a moderately expensive function that needs to support being
    debugged and fixed at runtime without interrupting the calling program.
    
    A function marked with this decorator that crashes by raising an exception
    will cause the Python debugger to be started at the point where the
    exception was thrown. When the debugger exits, the user will be given the
    option to reload the function and reinvoke it with the original input.
    
    This decorator only works for top-level functions in a module that are
    idempotent, meaning that they return the same result regardless of how many
    times they are invoked with the same input.
    
    Functions marked in this way should only be invoked from external modules
    via its module object. So instead of `from module import retriable_function`
    use `import module` and invoke the function using
    `module.retriable_function(...)`.
    
    NOTE: When a decorated function (and its containing module) is reloaded,
          any callers on the stack that reside within the reloaded module will
          continue to execute the pre-reloaded version of themselves. Therefore
          it is less confusing if functions marked as @retriable are not
          directly or indirectly invoked by methods in the same module.
    
    Author: David Foster (dafoster.net)
    License: MIT
    Tested On: CPython 2.7
    """
    
    if sys._getframe().f_back.f_code.co_name != '<module>':
        raise AssertionError(
            'The @retriable decorator can only be safely applied to ' +
            'top-level functions within a module.')
    
    module = sys.modules[func.__module__]
    func_name = func.__name__
    
    def decorated_func(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except:
                # Start debugger at point where exception was raised
                tb = sys.exc_info()[2]
                pdb.post_mortem(tb)
                
                # Prompt user whether to try again or not
                while True:
                    choice = raw_input(
                        '[R]etry after reload, Rais[E], or [Q]uit? [R] ')
                    if len(choice) == 0 or choice[0].lower() == 'r':
                        # Retry after reload
                        break
                    elif choice[0].lower() == 'e':
                        # Raise
                        raise
                    elif choice[0].lower() == 'q':
                        # Quit
                        sys.exit(1)
                    else:
                        # Not understood... ask again
                        continue
                
                # Retry after reload, recursively
                reload(module)
                return getattr(module, func_name)(*args, **kwargs)
    return decorated_func
```

Some limitations and caveats about this decorator's use are described in its docstring.

Enjoy.