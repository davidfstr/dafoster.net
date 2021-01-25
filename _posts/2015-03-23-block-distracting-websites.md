---
layout: post
title: Block Distracting Websites
tags: [Productivity]
date_updated: 2021-01-25

---

<div class="img-box-right">
    <a href="/assets/2015/distracting-websites.png">
        <img class="img-225" alt="Comic: Person on left: 'I just watched you open Google News and then close it without reading it <em>five times in a row</em>.' Person on right: 'The fact that I spend most of my time so stupidly only makes it <em>more</em> important not to waste any here.'" src="/assets/2015/distracting-websites.png" />
    </a>
    <div><i>Courtesy of <a href="http://xkcd.com/1502/">xkcd</a></i></div>
</div>

If you spend a lot of time on the computer like I do, there's a good chance that there are some websites that you spend too much time on. Recently I've taken measures to outright block various distracting websites on my home computer.

On OS X and Linux you can block websites by adding entries like the following to the `/etc/hosts` file. (On Windows, the hosts file lives at `C:\Windows\system32\Drivers\etc`.)

```
# Block distracting websites
127.0.0.1 news.ycombinator.com
127.0.0.1 arstechnica.com
127.0.0.1 slashdot.org
#127.0.0.1 facebook.com
#127.0.0.1 www.facebook.com
#127.0.0.1 reddit.com
#127.0.0.1 www.reddit.com
```

On OS X, you would also need to running the following terminal command to refresh the hosts file:

```
dscacheutil -flushcache
```

After doing both of these, attempting to visit one of the websites listed in `/etc/hosts` will display an error page.

Of course if you need to temporarily visit one of the blocked sites you can just go back to the hosts file and add a `#` before the corresponding entry.

## 2021 Update

I still use the above `/etcs/hosts` technique (from 2013) to block 
distracting websites on my Mac laptop.

On the iPhone I use the built-in **[Screen Time]** feature to block myself from
distracting websites:

* Open the Settings app and navigate to [Screen Time > Content & Privacy 
  Restrictions > Content Restrictions > Web Content].
* Alter the restriction type from the default "Unrestricted Access" to
  "Limit Adult Websites".
* Then scroll down to the "Never Allow" section and add any distracting websites
  you'd like to block by default. For example I have `news.ycombinator.com`
  there. 🙂
* Then whenever you want to actually access a distracting website intentionally
  (as opposed to when you reflexively auto-type such a website), you can just
  temporarily go back to [Settings > Screen Time > Content & Privacy 
  Restrictions] and just flip the "Content & Privacy Restrictions" switch
  off temporarily.

On macOS 10.15 Catalina and later there is a similar built-in "Screen Time"
feature that appears to be usable in the same way as the "Screen Time" feature
on iPhone. However since I've elected to limit my Macs to upgrade to a max of
macOS 10.14, I still preferentially use the older `/etc/hosts` trick described
earlier in this article.

[Screen Time]: https://support.apple.com/en-us/HT208982
