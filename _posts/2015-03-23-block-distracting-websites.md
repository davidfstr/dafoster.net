---
layout: post
title: Block Distracting Websites
tags: [Productivity]

---

<div class="img-box-right">
    <img class="img-225" alt="Comic: Person on left: 'I just watched you open Google News and then close it without reading it <em>five times in a row</em>.' Person on right: 'The fact that I spend most of my time so stupidly only makes it <em>more</em> important not to waste any here.'" src="/assets/2015/distracting-websites.png" />
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

