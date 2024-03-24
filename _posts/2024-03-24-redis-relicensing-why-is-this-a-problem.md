---
layout: post
title: "Redis relicensing: Why is this a problem?"
tags: [Software]

---

I find the fire & heat around [Redis changing licensing] surprising. Maintaining Redis takes effort which cannot be free in a sustainable fashion.

Consider [this post] which complains Redis isn't "uphold[ing] the ideals of Free and Open Source Software", as if it was created as a vehicle to evangelize the FSF and OSI missions. But it was not, it was created to be *useful*, as a data structure server.

I also disagree with that post's assertion that Redis contributions would have been withheld if it started with a different license. I expect contributions would come from existing users of Redis who wanted new features themselves and were willing to sponsor the related effort, regardless of the license in use.

Certainly if Redis has started under its new license and I was using Redis on Azure - which Microsoft has already bought a commercial license for - then I wouldn't care that Redis was licensed under the SSPL.

Frankly **I think it would be a win for software sustainability if there was a trend of new software projects being offered under source-available licenses** requiring large cloud providers like AWS, Azure, and GCP to give back financially to the core maintainers.

I plan to be announcing a project of my own soon under a source-available license restricting unlicensed commercial use. I've already put several years of effort into this project. No way in hell do I want to ["get Jeff'ed"](https://youtu.be/XZ3w_jec1v8?si=tUHKi3BVzqwTzyIS&t=1695), with someone else selling what I've put so much of my own effort into creating without giving anything back.



[Redis changing licensing]: https://redis.com/blog/redis-adopts-dual-source-available-licensing/
[this post]: https://andrewkelley.me/post/redis-renamed-to-redict.html