---
layout: post
title: Skills I Learned at Microsoft
tags: [Personal]
x_date_written: 2012-11-03

---

## Social

* How to manage managers.
    - Detailed time tracking.
        - I've done this internally at every job I've had,
          but only at Microsoft did I need to report on it externally.
    - Managing expectations.
    - The no-surprises principle.
        - <p>Bad news is okay (socially) if it is known in advance.</p>
* How an [A-grade SDET] (technical tester) thinks.
    - <p>Techniques for making designs mure testable,
      especially in the presence of multi-threading.</p>
* <p>How an [A-grade PM] (Program Manager) can manage politics for you.</p>
* <p>How to work around certain mediocre coworkers. (This is not common.)</p>
* Don't use made up words until you've looked them up first.
    - Counterintuitive. However your "made up word" may actually
      exist and it may not be a pleasant word.

[A-grade SDET]: http://www.linkedin.com/in/rforsbach
[A-grade PM]: http://www.linkedin.com/pub/candace-jackson/40/267/354


## Productivity

* <p>How to aggressively filter my email inbox.</p>
* <p>The zero-inbox style of email management.</p>
* Macro programming on Windows via AutoHotkey.
    - [Keyboard Maestro] on the Mac is more capable and more polished,
      but AutoHotkey was the best thing I found for Windows.

[Keyboard Maestro]: http://www.keyboardmaestro.com/

## Technical

* Microsoft-specific tooling:
    - Visual Studio
    - TAEF (for testing)
    - Octopus (for deployment of MSIs)
    - <p>WiX (for development of MSIs)</p>
* Formalized code review via CodeFlow.
    - <p>(Also did this at Google with Mondrian.)</p>
* Heap profiling to track down memory leaks.
    - <p>Failing to unregister listeners can cause memory leaks,
      particularly if an object registers a listener
      on another longer-lived (or immortal) object.</p>
* How to write *detailed* technical specifications.
    - However the utility of such highly detailed specifications is limited.
