---
layout: post
title: Debugging a deadlock in Python
tags: [Software]

include_mermaid: true
include_accordian: true

style: |
    .accordion-inner > pre:last-child {
        margin-bottom: 0;
    }
    .accordion:has(.accordion-inner > pre:last-child) {
        margin-bottom: 15px;
    }

---

I recently encountered a deadlock while running the automated tests of my [website downloader, Crystal]. The process for investigating and fixing this deadlock was interesting, so I thought I'd share it:

## What does a deadlock look like?

One day after making some changes to my program, when I ran the program's automated tests the program just completely froze, becoming unresponsive to all input and not providing any further output:

```
$ crystal --test
...
======================================================================
RUNNING: test_some_tasks_may_complete_immediately (crystal.tests.test_tasks)
----------------------------------------------------------------------
    "GET /_/https/example.com/ HTTP/1.1" 404 -
    *** Requested resource not in archive: https://example.com/
    "GET /_/https/xkcd.com/1/ HTTP/1.1" 200 -
⚠️ No further output printed. No further input accepted. Program is stuck.
```

To investigate why the program was frozen I wanted to **see exactly which lines of code the program was stuck on**. Python has a useful [faulthandler] module in the standard library that, among other things, can start listening for various Unix signals and print out a traceback showing the line of code being executed on all threads.

To enable the faulthandler when running a program you can use the `PYTHONFAULTHANDLER` environment variable:

```
$ PYTHONFAULTHANDLER=1 crystal --test
```

Then after the program becomes stuck, you can open a new terminal window and send a SIGABRT signal to the stuck program to trigger the faulthandler:

```
$ kill -SIGABRT 7984  # 7984 = PID of the python process
```

When triggered on the Crystal program, the faulthandler printed tracebacks like:

{% capture traceback %}
```
======================================================================
RUNNING: test_some_tasks_may_complete_immediately (crystal.tests.test_tasks)
----------------------------------------------------------------------
    "GET /_/https/example.com/ HTTP/1.1" 404 -
    *** Requested resource not in archive: https://example.com/
    "GET /_/https/xkcd.com/1/ HTTP/1.1" 200 -
Fatal Python error: Aborted

Thread 0x0000700058d9b000 (most recent call first):
  File "/Users/me/Crystal/venv3.9/lib/python3.9/site-packages/tqdm/std.py", line 111 in acquire
  File "/Users/me/Crystal/venv3.9/lib/python3.9/site-packages/tqdm/std.py", line 134 in __enter__
  File "/Users/me/Crystal/venv3.9/lib/python3.9/site-packages/tqdm/std.py", line 577 in __new__
  File "/Users/me/Crystal/src/crystal/util/progress.py", line 143 in __init__
  ...

Thread 0x0000700057d98000 (most recent call first):
  File "/Users/me/Crystal/venv3.9/lib/python3.9/site-packages/tqdm/std.py", line 111 in acquire
  File "/Users/me/Crystal/venv3.9/lib/python3.9/site-packages/tqdm/std.py", line 134 in __enter__
  File "/Users/me/Crystal/venv3.9/lib/python3.9/site-packages/tqdm/_monitor.py", line 66 in run
  File "/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/threading.py", line 973 in _bootstrap_inner
  File "/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/threading.py", line 930 in _bootstrap

(... 🤔 62 copies of the above paragraph ...)

Thread 0x0000700017c55000 (most recent call first):
  File "/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/selectors.py", line 416 in select
  File "/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/socketserver.py", line 232 in serve_forever
  File "/Users/me/Crystal/src/crystal/tests/test_download_body.py", line 129 in do_serve_forever
  File "/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/threading.py", line 910 in run
  File "/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/threading.py", line 973 in _bootstrap_inner
  File "/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/threading.py", line 930 in _bootstrap

Thread 0x000070000ab28000 (most recent call first):
  File "/Users/me/Crystal/src/crystal/tests/util/runner.py", line 130 in run
  File "/Users/me/Crystal/src/crystal/util/xthreading.py", line 101 in wrapper
  File "/Users/me/Crystal/src/crystal/tests/util/runner.py", line 49 in run_test
  File "/Users/me/Crystal/src/crystal/util/xthreading.py", line 101 in wrapper
  File "/Users/me/Crystal/src/crystal/tests/index.py", line 107 in _run_tests
  File "/Users/me/Crystal/src/crystal/tests/index.py", line 80 in run_tests
  File "/Users/me/Crystal/src/crystal/util/xthreading.py", line 101 in wrapper
  File "/Users/me/Crystal/src/crystal/__main__.py", line 314 in bg_task
  File "/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/threading.py", line 910 in run
  File "/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/threading.py", line 973 in _bootstrap_inner
  File "/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/threading.py", line 930 in _bootstrap

Current thread 0x000000011b0405c0 (most recent call first):
  File "/Users/me/Crystal/venv3.9/lib/python3.9/site-packages/wx/core.py", line 2262 in MainLoop
  File "/Users/me/Crystal/src/crystal/__main__.py", line 323 in _main
  File "/Users/me/Crystal/src/crystal/__main__.py", line 45 in main
  File "/Users/me/Crystal/venv3.9/bin/crystal", line 6 in <module>
```
{% endcapture %}

{% include accordian/begin %}
    faulthandler traceback
{% include accordian/middle %}
    {{ traceback | markdownify }}
{% include accordian/end %}

Notice in the traceback above that several of the stuck threads are at `tqdm/std.py", line 111 in acquire`, which is trying to acquire a low-level [threading.RLock].

**When there is at least one thread trying to acquire a lock and not making any progress, there's probably a deadlock.** So the program definitely seems to be deadlocked.

## Isolating and fixing a deadlock

To debug further, it would be **useful for the program to detect when it cannot acquire the lock it wants and then immediately print out:**

1. **the traceback which is trying to acquire the lock** and 
2. **the traceback which is currently holding the lock**. 

So I made some modifications around the code that acquires/releases the lock to log that information:

{% capture lock_logging_code %}
```python
✚ import threading
✚ import traceback

class TqdmDefaultWriteLock(object):
    th_lock = TRLock()
✚   th_lock_holders = []  # type: List[Tuple[threading.Thread, traceback.StackSummary]]

    def acquire(self, *a, **k):
✚       if 'timeout' not in k:
✚           k['timeout'] = 5.0  # seconds

        for lock in self.locks:
            ok = lock.acquire(*a, **k)
✚           if not ok:
✚               print(
✚                   f'*** TqdmDefaultWriteLock: Failed to acquire lock in '
✚                   f'{k["timeout"]} seconds. '
✚                   f'Lock holder is {TqdmDefaultWriteLock.th_lock_holders[-1][0]} at:\n'
✚                   f'{"".join(TqdmDefaultWriteLock.th_lock_holders[-1][1])}')
✚               print(f'*** New acquirer is:\n{"".join(traceback.format_stack())}')
✚               raise AssertionError('Failed to acquire TqdmDefaultWriteLock')

✚       TqdmDefaultWriteLock.th_lock_holders.append((
✚           threading.current_thread(),
✚           traceback.format_stack()
✚       ))

    def release(self):
✚       TqdmDefaultWriteLock.th_lock_holders.pop()

        for lock in self.locks[::-1]:  # Release in inverse order of acquisition
            lock.release()
```
{% endcapture %}

{% include accordian/begin %}
    Code to add deadlock detection and logging to lock acquire & release
{% include accordian/middle %}
    {{ lock_logging_code | markdownify }}
{% include accordian/end %}

With those modifications in place, I can pinpoint the smoking gun:

```
======================================================================
RUNNING: test_project_opens_as_readonly_when_project_is_on_readonly_filesystem (crystal.tests.test_readonly_mode)
----------------------------------------------------------------------
*** TqdmDefaultWriteLock: Failed to acquire lock in 5.0 seconds. Lock holder is <_MainThread(MainThread, started 4446586304)> at:
  ...
  File "/Users/me/Crystal/src/crystal/model.py", line 679, in _apply_migrations
    self._process_table_rows(
  File "/Users/me/Crystal/src/crystal/model.py", line 785, in _process_table_rows
    progress_bar.update()
  File "/Users/me/Crystal/venv3.9/lib/python3.9/site-packages/tqdm/std.py", line 1263, in update
    self.refresh(lock_args=self.lock_args)
  File "/Users/me/Crystal/venv3.9/lib/python3.9/site-packages/tqdm/std.py", line 1367, in refresh
    self._lock.acquire()

*** New acquirer is:
  File "/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/threading.py", line 930, in _bootstrap
    self._bootstrap_inner()
  File "/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/threading.py", line 973, in _bootstrap_inner
    self.run()
  File "/Users/me/Crystal/venv3.9/lib/python3.9/site-packages/tqdm/_monitor.py", line 66, in run
    with self.tqdm_cls.get_lock():
  File "/Users/me/Crystal/venv3.9/lib/python3.9/site-packages/tqdm/std.py", line 134, in __enter__
    self.acquire()
```

Here, I notice that the traceback [`_apply_migrations()` → `_process_table_rows()` → `update()`] is holding the global `tqdm._lock`, which is strange because **there shouldn't be a reason for this code to hold a lock at all**.

### Culprit: Inappropriate locking

Originally I thought `update()` just called `display()` directly:

<div class="mermaid">
sequenceDiagram
    participant Project
    participant ProgressBar as ProgressBar<br/>(extends tqdm)
    participant lock as tqdm._lock<br/>«global»
    participant ProgressListener

    Project->>+Project: _process_table_rows
        loop each table row
            Project->>+ProgressBar: update
                ProgressBar->>+ProgressBar: display [about once per second]
                ProgressBar->>ProgressListener: update_gui_progress_bar_func
                deactivate ProgressBar
            deactivate ProgressBar
        end
    deactivate Project
</div>

But actually `update()` calls a `refresh()` method first, and *that* call to `refresh()` grabs the global `tqdm._lock`!

<div class="mermaid">
sequenceDiagram
    participant Project
    participant ProgressBar as ProgressBar<br/>(extends tqdm)
    box rgb(191, 223, 255)
        participant lock as tqdm._lock<br/>«global»
    end
    participant ProgressListener

    Project->>+Project: _process_table_rows
        loop each table row
            Project->>+ProgressBar: update
                rect rgb(191, 223, 255)
                    note over ProgressBar,ProgressListener: ⚠️ Intermediate refresh() method acquires tqdm._lock!
                    ProgressBar->>+ProgressBar: refresh [about once per second]
                        ProgressBar->>lock: acquire
                        rect white
                            ProgressBar->>+ProgressBar: display
                            ProgressBar->>ProgressListener: update_gui_progress_bar_func
                            deactivate ProgressBar
                        end
                        ProgressBar->>lock: release
                    deactivate ProgressBar
                end
            deactivate ProgressBar
        end
    deactivate Project
</div>

It makes sense for the `update()` method on a normal `tqdm` instance to use a lock because it prints its progress bar to a shared terminal, possibly at the same time that other instances are also trying to print to the same terminal. However the custom `ProgressBar` subclass of `tqdm` which is used here is displaying a *graphical* progress bar in an unshared dialog and so it does not need to do additional locking.

So we need to avoid the locking done by `refresh()`. 

When looking at the code for that method, I notice that it's possible to pass a `nolock=True` argument to disable its locking behavior:

```python
class tqdm(...):
    def refresh(self, nolock=False, lock_args=None):
        if not nolock:
            self._lock.acquire(...)
        self.display()
        if not nolock:
            self._lock.release()
        return True
```

So it should be possible to override `refresh()` to *always* assume `nolock=True`:

```
class ProgressBar(tqdm):
✚   @overrides
✚   def refresh(self, nolock=False, lock_args=None) -> bool:
✚       # Never grab the global tqdm._lock,
✚       # because we're NOT printing a CLI progress bar to a shared terminal
✚       return super().refresh(nolock=True, lock_args=lock_args)

    # Override tqdm's normal behavior of printing a CLI progress bar
    # to instead update a GUI progress bar
    @overrides
    def display(self, *args, **kwargs) -> None:
        update_gui_progress_bar_func(self.n, self.miniters)
```

Lo and behold, the deadlocking behavior is no longer observed! 🎉

### Common culprit: Acquiring multiple locks in an inconsistent order

Although not a problem in the above example, another common cause of deadlocks happens when a section of code acquires multiple locks at the same time but a different section of code tries to acquire the same locks in a different order.

**A common fix for deadlock related to acquiring locks in an inconsistent order is to give each lock a unique ID upon construction. Whenever a section of code wants to acquire multiple locks at a time, it must acquire each individual lock in increasing order of ID.**

### Fin

So, that was my recent adventure in tracking down and fixing a deadlock in Python. Perhaps some of the techniques mentioned above will be helpful for you in debugging your own programs. Happy coding!


[website downloader, Crystal]: /projects/crystal-web-archiver/
[faulthandler]: https://docs.python.org/3/library/faulthandler.html
[threading.RLock]: https://docs.python.org/3/library/threading.html#threading.RLock