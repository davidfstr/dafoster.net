---
layout: post
title: "Crystal Web Archiver 1.1.0b Released!"
tags: [DigitalPreservation, Other]
x_audience: |
    Anyone who is interested in downloading websites,
    especially folks old enough to have experienced losing a treasured
        website to the sands of time.
    Also digital preservationists in other areas.
x_performance: |
    TODO

style: |
    /* Override blockquote to use same font size as body text */
    blockquote { font-size: 16px !important; }

script: |
    /*public*/ function scrollToSubscribeBlock() {
        var subscribeBlock = document.querySelector('#subscribe-block');
        subscribeBlock.querySelector('.subscribe__prompt').style['backgroundColor'] = '#ffff0070';
        subscribeBlock.scrollIntoView({behavior: 'smooth', block: 'start'});
    }

---

<img class="img-box-right img-200" alt="Logo: Crystal Web Archiver" src="/assets/2021/crystal-web-archiver/logo@2x.png" />

[Crystal] is a **website downloader program** that is intended to save websites for long-term archival, even after the original site has fallen off the internet. Today I'm pleased to announce Crystal's first beta release, bringing support for downloading more complex static sites than ever before, and generally being stable enough for a full public release.

[Crystal]: /projects/crystal-web-archiver/

* [Download Crystal for Windows 7, 8, and 10](https://github.com/davidfstr/Crystal-Web-Archiver/releases/download/v1.2.0b/crystal-win-1.2.0b.exe)
* [Download Crystal for macOS 10.14 and later](https://github.com/davidfstr/Crystal-Web-Archiver/releases/download/v1.2.0b/crystal-mac-1.2.0b.dmg)
    * You will need to [right-click or Control-click on the application 
      and select "Open" to open it for the first time](https://github.com/davidfstr/Crystal-Web-Archiver/issues/20).
* [Quickstart guide](https://github.com/davidfstr/Crystal-Web-Archiver#quickstart-) for downloading your first website

> **Update:** These download links have been updated to point to the 1.2.0b release,
> which has a number of fixes related to first-time-launch issues and improvements for downloading
> large websites (with 10,000+ URLs).

Many new types of sites can be successfully downloaded with this release of Crystal, including DeviantArt portfolio websites at `*.daportfolio.com` (which are scheduled to fall off the internet in about a week after this post), [Otaku World](http://otakuworld.com/), and [16Personalities](https://www.16personalities.com/). <!-- Some others sites of interest like [bongo.cat](https://bongo.cat/) and the [Calm Blog](https://blog.calm.com/) require additional work. -->

### Digital preservation is important

I personally care a lot about **digital preservation**, which makes it possible to access and enjoy digital content even after it was originally released, substantially beyond the usual lifetime of such works. I'm planning to work on a few projects this year to advance the state of the art in preserving both online sites and old Macintosh programs from the 1990's. If this topic is also of interest to you, please consider <a href="javascript:scrollToSubscribeBlock();">following me</a> on Twitter or RSS. I like hearing from people who have similar interests.

### *Related Projects*

* [ClassicBox](/projects/classicbox/) - **(Pre-alpha)** Makes it easy to play old Mac games from the 1990s on modern hardware, similar to the [DOSBox](https://www.dosbox.com/) project.