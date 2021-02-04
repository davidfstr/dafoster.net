---
layout: post
title: "Exploring Onionland: The Tor .onion Darknet"
tags: [Privacy, Offtopic]

---

Today I decided to explore the realm of Tor Hidden Services, which can be identified via URLs that appear to be on an `.onion` top-level domain.

The first hurdle is getting to your first site, since all domains have gibberish-looking names:[^no_verify_by_name]

* **Core.onion** ([eqt5g4fuenphqinx.onion](http://eqt5g4fuenphqinx.onion/))
    * The original starting point for many users since 2007.
    * I began my exploration here.

## Finding Things

The first thing you realize is that there are *no search engines*.[^search_engines] Instead you have to resort to the primitive method of recursively following links from previous sites you found. Bookmarks are essential. It's like 1995 all over again.[^corpnet]

Directory service sites exist with the sole purpose of listing links to other sites:[^directory_site]

* **TorDir** ([dppmfxaacucguzpc.onion](http://dppmfxaacucguzpc.onion/))
    * The original directory site (to my knowledge) since 2007.
* **The Hidden Wiki** ([kpvz7ki2v5agwt35.onion](http://kpvz7ki2v5agwt35.onion/wiki/index.php/Main_Page))
    * The original popular wiki, running the same Mediawiki software as Wikipedia.
    * The main purpose seems to be acting as a directory, although there are a few other interesting articles as well. <!-- http://kpvz7ki2v5agwt35.onion/wiki/index.php/The_Matrix -->
    * Sadly the moderators seem to be losing against spammers, who repeated change links on the home page to redirect through a certain `coinurl.com` site. Thus it is necessary to go through [older revisions of the main page](http://kpvz7ki2v5agwt35.onion/wiki/index.php?title=Main_Page&oldid=52408) to get anything useful.

And also:

* **TorList** ([torlinkbgs6aabns.onion](http://torlinkbgs6aabns.onion/))
    * A newer, more limited, and less organized directory. Moderated.
    * Useful because all its links fit on a single page, so it is a decent starting point.
    * **Edit:** *Link updated. Was previously pointing to a non-authoritative clone. Possibly a spammer. In case you'd like to compare, here is the <a href="http://torlinksysgthcbz.onion/" rel="nofollow">old link</a>.*

## Parallel Worlds

For most popular websites on the public internet, there is a clone in Onionland.

* Twitter -> **TorStatusNet** ([lotjbov3gzzf23hc.onion](http://lotjbov3gzzf23hc.onion/))
    * Microblogging.
* Gmail / Hotmail -> **Tor Mail** ([jhiwjjlqpyawmpjx.onion](http://jhiwjjlqpyawmpjx.onion/))
    * Free email service.
    * Can communicate with regular email addresses too.
    * Although rumored to be unreliable. <!-- http://utup22qsb6ebeejs.onion/?p=149 -->
* 4chan -> **TorChan** ([zw3crggtadila2sg.onion](http://zw3crggtadila2sg.onion/imageboard/))
    * Imageboard. NSFW.

I can only assume human wants must be fairly consistent.

## Commerce

The universal currency for making transactions is [BitCoin](http://bitcoin.org/en/), probably because it is far less traceable than standard currency.

It's really surprising and a bit disturbing what can be purchased: drugs, weapons, assassinations&nbsp;(!!!), among other things. <!-- (No links for you!) -->

## Final Thoughts

It feels really weird being in a part of the internet that is completely unreachable from Google (or any normal search engine). Much like visiting another country the laws, norms, and aesthetics are different.[^another_country] It is an interesting place to visit, but perhaps not the most desirable place to live.

### Related Links

* [/r/onions](http://www.reddit.com/r/onions)
    * *Reddit's collection of onion links.*


[^no_verify_by_name]: Since domain names basically consist of gibberish, it is not practical to verify whether you are at the authentic URL for a domain, since it is hard to remember and recognize the domain name. Thus it relatively easy to get redirected to a spoofed version of a website and not be aware of it. Certain sites like **Black Market**, which I can only assume have been spoofed a lot in the past, take special measures such as putting the (gibberish) domain name in the site logo and instructing visitors on the main home page to check the domain name explicitly. Hardly a reliable solution.

[^search_engines]: Okay, there are are few search engines such as **DeepSearch** ([hpuuigeld2cz2fd3.onion](http://hpuuigeld2cz2fd3.onion/)) and **The Abyss** ([nstmo7lvh4l32epo.onion](http://nstmo7lvh4l32epo.onion/)), but they're about as effective as WebCrawler was back in the day.

[^corpnet]: If your corporate intranet or wiki has no decent search facility (likely), it's the same feeling of not being able to find anything. The only company I've worked for that had *good* internal search was Google (circa 2008). Microsoft sure didn't (circa 2011), although they were using some third-party engine internally, not Bing.

[^directory_site]: The only directory services site on the public web I still know of is the [Open Directory Project](http://www.dmoz.org). It's been a long time since I've used them.

[^another_country]: Instead of travelling to another country physically, you can try browsing the internet in a different language, which is similarly partitioned from the English internet. For example Germany's Facebook is [studiVZ](http://www.studivz.net/). China's Google is [Baidu](http://www.baidu.com). Naturally you need to be able to read the language in question to try this exercise seriously.
