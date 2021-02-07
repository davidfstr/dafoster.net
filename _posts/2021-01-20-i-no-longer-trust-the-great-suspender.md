---
layout: post
title: I no longer trust The Great Suspender
tags: [Productivity, Software, Offtopic]
x_audience: |
    all users of The Great Suspender browser extension,
    which is a subset of all Chrome and Edge users
    (but not Firefox or Safari users)
x_performance: |
    32,350 hits on day 1 of publish and post to Hacker News.
        Was in the top 2 items on Hacker News from
        6:02 AM to at least 1:28 PM (7.5 hours)
        on the day of its posting.
    38,628 hits on week 1 of publish, with daily numbers of:
        32350, 2651, 1954, 628, 447, 344, 254
    
    878 hit spike on 2021-02-04 from Google organic traffic,
        up from 39 on the previous day (2,151% increase),
        probably because of news that Google has blocked
        The Great Suspender in the Chrome Web Store:
        https://www.zdnet.com/article/google-kills-the-great-suspender-heres-what-you-should-do-next/
        
        Wow. There's a fairly good chance that this article
        was a major contributor to TGS getting pulled,
        considering how much attention it got.

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
    * ⚠️ Any tabs that you forget to unsuspend will be lost
      when uninstalling The Great Suspender in the next step.
* Uninstall The Great Suspender.
* Download the [latest good version] of The Great Suspender (7.1.6) from GitHub, 
  and move it to some permanent location outside your Downloads folder.
  (It should be commit 9730c09.)
* Load your downloaded copy as [an unpacked extension].
  (This copy will not auto-update to future untrusted versions of the extension.)
* All done! 🎉

<s>**Caveat:** My understanding is that installing an unpacked extension in this way
will cause Chrome to [issue a new kind of security prompt] every time it is
launched, which you'll have to ignore. 😕</s>
I see no security prompt for using an unpacked extension at least on
macOS 10.14 Mojave with Chrome 88 and Developer Mode left on.

[issue a new kind of security prompt]: https://news.ycombinator.com/item?id=25847171

### Other options

Other browser extensions for suspending tabs exist, as mentioned in the
[Hacker News discussion] for this article. However I have not conducted my own
security review on any of those other extensions, so buyer beware.

**2021-02-06 Update:** Wow. [Google has pulled The Great Suspender] from its web store.
It is still possible to install the latest clean version of The Great Suspender
using the "Permanent harder fix" instructions above. Or you might consider one
of the [alternatives suggested by Lifehacker].

[latest good version]: https://github.com/greatsuspender/thegreatsuspender/releases/tag/v7.1.6
[an unpacked extension]: https://lifehacker.com/how-you-can-still-download-chrome-extensions-without-us-1826796797
[Hacker News discussion]: https://news.ycombinator.com/item?id=25846504
[Google has pulled The Great Suspender]: https://www.zdnet.com/article/google-kills-the-great-suspender-heres-what-you-should-do-next/
[alternatives suggested by Lifehacker]: https://lifehacker.com/ditch-the-great-suspender-before-it-becomes-a-security-1845989664

### *Related Articles*

In {% assign tag = 'Software' %}{% include blocks/tag_single %}:

* [How to Design Large Programs with Abstraction and Encapsulation](/articles/2017/03/25/how-to-design-large-programs-with-abstraction-and-encapsulation/)

In {% assign tag = 'Productivity' %}{% include blocks/tag_single %}:

* [Block Distracting Websites](/articles/2015/03/23/block-distracting-websites/)
* [Sending email from command line scripts](/articles/2013/07/27/sending-email-from-command-line-scripts/)
* [Scrivener: An IDE for thinkers, creators, and writers](/articles/2013/10/27/scrivener-an-ide-for-thinkers-creators-and-writers/)
