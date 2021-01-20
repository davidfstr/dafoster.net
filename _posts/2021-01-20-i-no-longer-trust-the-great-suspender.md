---
layout: post
title: I no longer trust The Great Suspender
tags: [Productivity, Software, Offtopic]

---

I know a number of folks use **The Great Suspender** to automatically suspend
inactive browser tabs in Chrome. Apparently recent versions of this extension
have been [taken over by a shady anonymous entity] and is now
[flagged by Microsoft as malware]. Notably the most recent
version of the extension (v7.1.8) has added integrated analytics that can
track all of your browsing activity across all sites. Yikes.

[taken over by a shady anonymous entity]: https://www.reddit.com/r/KyleTaylor/comments/jowlt2/open_source_development_the_great_suspender_saga/
[flagged by Microsoft as malware]: https://www.windowscentral.com/great-suspender-extension-now-flagged-malware-edge-has-built-replacement

**Recommendations for users of The Great Suspender (7.1.8):**

### Temporary easy fix

* Disable analytics tracking by opening the extension options for
  The Great Suspender and checking the box
  "Automatic deactivation of any kind of tracking".
* Pray that the shady developer doesn't issue a malicious update to The Great Suspender later.
  (There's no sensible way to disable updates of an individual extension.)

### Permanent harder fix <small>(👈 **Recommended!**)</small>

* Close as many unneeded tabs as you can.
* Unsuspend all remaining tabs. ⏳
* Uninstall The Great Suspender.
* Download the [latest good version] of The Great Suspender (7.1.6) from GitHub, 
  and move it to some permanent location outside your Downloads folder.
  (It should be commit 9730c09.)
* Load your downloaded copy as [an unpacked extension].
  (This copy will not auto-update to future untrusted versions of the extension.)
* All done! 🎉

**Caveat:** My understanding is that installing an unpacked extension in this way
will cause Chrome to [issue a new kind of security prompt] every time it is
launched, which you'll have to ignore. 😕

[issue a new kind of security prompt]: https://news.ycombinator.com/item?id=25847171

### Other options

Other browser extensions for suspending tabs exist, as mentioned in the
[Hacker New discussion] for this article. However I have not conducted my own
security review on any of those other extensions, so buyer beware.

[latest good version]: https://github.com/greatsuspender/thegreatsuspender/releases/tag/v7.1.6
[an unpacked extension]: https://lifehacker.com/how-you-can-still-download-chrome-extensions-without-us-1826796797
[Hacker New discussion]: https://news.ycombinator.com/item?id=25846504

