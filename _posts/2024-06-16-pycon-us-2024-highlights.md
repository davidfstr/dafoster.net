---
layout: post
title: PyCon US 2024 Highlights
tags: [Software]

---

I was happy to be able to attend [PyCon US 2024] this past year, a prominent conference for the Python programming language. I got to meet in person a number of folks I've interacted with online, from the Python Typing community and elsewhere.

[PyCon US 2024]: https://us.pycon.org/2024/

## Favorite Talks

I particularly liked the following talks, which I've organized by topic. 

Most video links below are to the Hublio platform, which only conference attendees can access. Unfortunately the talk recordings have not yet been shared more widely on YouTube.

### Performance

* **Unlocking the Parallel Universe: Subinterpreters and Free-Threading in Python 3.13** - Anthony Shaw
    * Shows many ways to run Python programs in parallel: in different processes, different interpreters, and different threads. There are tradeoffs with each strategy.
    * Insight: "Subinterpreters will be a better solution than Multiprocessing for long-running workers."
    * Insight: Free threading is a good solution for workers that need the fastest data exchange between workers. But free threading is difficult to program correctly, without race conditions.
    * [📽 Video (Hublio)](https://events.hubilo.com/pycon-us-2024/session/234270)
* **Overcoming GIL with subinterpreters and immutability** - Yury Selivanov
    * Introduces [memhive], a new library for safely sharing state across multiple Python interpreters in the same process, by providing an immutable/persistent map structure (HAMT) that can be efficiently updated and shared between interpreters
    * Insight: Subinterpreters are a better solution than Multiprocessing for workers that need to share state - such as a cache - between workers, because subinterpreter workers share memory. Subinterpreters are easier to program than free threading.
    * [📽 Video (Hublio)](https://events.hubilo.com/pycon-us-2024/session/234227)

[memhive]: https://github.com/edgedb/memhive

### Debugging

* **Profiling at the speed of light** - Pablo Galindo Salgado
    * Showed how to use the [perf] tool on a Python 3.12 and 3.13 process to look at low-level performance metrics like CPU-level and instruction-level counters.
    * Showed how to make flame graphs to see where a mixed Python+C program is spending its time visually.
    * [📽 Video (Hublio)](https://events.hubilo.com/pycon-us-2024/session/234204)
* **Rewind: Python Time-Travel Debugger** - Toby Ho
    * Showed [pyrewind], a time-travel reverse-debugger for Python. Looks like a promising tool for pure Python code.
    * It's unclear whether the tool supports [debugging in the presence of C extensions], which may have side effects that the debugger does not track.
    * [📽 Video (Hublio)](https://events.hubilo.com/pycon-us-2024/session/234187)

[perf]: https://perf.wiki.kernel.org/index.php/Main_Page
[pyrewind]: https://github.com/airportyh/time-traveling-debugger
[debugging in the presence of C extensions]: https://github.com/airportyh/time-traveling-debugger/issues/47

### AI

* **Keynote** - Simon Willison
    * Great talk about AI and Machine Learning. Many interesting quotes from this presentation.
    * "You shouldn't need a CS degree to automate stuff with a computer"
    * [📽 Video (Hublio)](https://events.hubilo.com/pycon-us-2024/session/234277)
* **Lies, damned lies and large language models** - Jodie Burchell
    * Describes different types of hallucinations that Large Language Models (LLMs) can experience.
    * Shows how to measure how much a particular model hallucinates.
    * [📽 Video (Hublio)](https://events.hubilo.com/pycon-us-2024/session/234236)

### Typing System

* **Theory of Type Hints, Revisited** - Carl Meyer
    * Covers in-progress efforts to increase the formality of the underlying theory behind Python's type system, especially with respect to what the `Any` type means. These efforts have been partially motivated by ongoing work (for over a year) to attempt to introduce an `Intersection` type into Python's typing system.
    * [📽 Video pending](https://discuss.python.org/t/typing-summit-at-pycon-us-2024-17-may-2024/44421)
* **TypeForm: Type Hint for Type Expressions** - David Foster
    * Covers `TypeForm`, an in-progress Python type system feature for spelling a "type expression object" at runtime. This was my own talk. More details in PEP 747.
    * [📽 Video (YouTube)](https://www.youtube.com/watch?v=GOSG2qXMdcM)

### Fun

* **Build in-browser 3D experiences with WebGL and PyScript** - Łukasz Langa
    * Showed how to use Python to draw 3D graphics in the browser with WebGL.
    * Showed how to take data from a data processing library in Python and directly visualize it by talking to JavaScript visualization libraries.
    * [📽 Video (Hublio)](https://events.hubilo.com/pycon-us-2024/session/234214)
* **Connecting Old to New with CircuitPython: Retrocomputer input devices on modern PCs** - Jeff Epler
    * Shows how to use Python to build connectors to old keyboards, mice, and other hardware devices.
    * [📽 Video (Hublio)](https://events.hubilo.com/pycon-us-2024/session/234265)

