---
layout: post
title: "Privacy Sandbox: Google's answer to privacy-conscious advertising"
tags: [Privacy]
x_audience: |
    technologists who care about privacy and use Google products
x_performance: |
    24 hits on day 1 of publish and post to Hacker News as response
        to comment on high-ranking prior article posted by someone else
    TODO hits on week 1 of publish, with daily numbers of:
        24, 3, TODO, TODO, TODO, TODO, TODO

style: |
    /* Override blockquote to use same font size as body text */
    blockquote { font-size: 16px !important; }

---

Google is working on a new technology called [Privacy Sandbox] to replace the
need for advertisers to track individuals with third party cookies. This is
interesting to me for a couple of reasons:

Google is an advertising company, so they definitely want the ability to
continue being able to classify users into cohorts based on their behavior in
order to deliver targeted ads to them.

But they are *also* a browser company (as the makers of Chrome), and there
appears to be enormous public (and increasingly competitive) pressure on
browser vendors to provide stronger privacy protections by default in browsers.
Apple for example has rolled out various<!-- TODO: footnote --> privacy measures in its
very popular mobile browser Safari<!-- TODO: footnote -->. I speculate that Google is
concerned that if they *don't* find a way to better protect user privacy
(while still preserving the ability to provide targeted advertisements)
that an increasingly privacy-conscious public might eventually reach a 
tipping point where folks might start abandoning Chrome en masse for a
competitor browser that is viewed as more privacy-conscious.

So Google has twin incentives: to support tracking users to put them into
cohorts that can be addressed with targeted advertising, and to do this kind
of tracking in a *privacy-conscious* way. Hence I assume these incentives are
how Privacy Sandbox has come to be.

So how does Privacy Sandbox work exactly? Similar to current advertising
practice, there still exists an algorithm which is fed a user's browsing
history and that algorithm is used to put the user into an advertising cohort.
However the interesting change with Privacy Sandbox is that this algorithm
is run *locally* within the user's browser, and never actually needs to 
transmit the user's browsing history over the internet. Instead only a code 
for the identified cohort is transmitted, and a remote ad server can use that 
cohort directly.

On one hand I like that this scheme implies that third party advertisers aren't
constructing a detailed dossier of my browsing history themselves. 

On the other hand I believe the transmitted cohort code could inadvertently
reveal that I'm a member of one or more protected classes, which could cause
online companies I interact with to treat me in ways that I don't like or seek
to predate me. Google has identified this as a risk and seeks to mitigate it
by doing things like recognizing certain [protected classes] and removing
features from any identified cohort that put it to close to a protected class.

> **Update:** Everything discussed about Privacy Sandbox so far is only talking
> about the [FLoC] component of it. But there is also a [TURTLEDOVE] component
> which avoids the problem of transmitting one's cohort code outside the browser
> by running the full ad bidding process on the local device. Neat! (Thanks to
> [jefftk](https://news.ycombinator.com/item?id=26027504) on Hacker News 
> for the clarification.)

[FLoC]: https://github.com/WICG/floc#readme
[TURTLEDOVE]: https://github.com/WICG/turtledove#readme

Now a number of advertising companies who like their tried-and-true methods of
third party tracking are worried about Google closing the door on traditional
third party tracking in favor of Privacy Sandbox and are now 
[pursuing anti-trust actions] against Google regarding impending removal of 
support for third party cookies (which is a core technology for enabling
third party tracking).

I'm personally optimistic about the promise of Privacy Sandbox and removing
the ability of browsers to broadcast my browsing history to third parties.
If it can meet its stated goals, enabling businesses that rely on internet
advertising to stay afloat while making the mechanism of advertising *also* be
privacy-conscious, then I'm all for it.

[Privacy Sandbox]: https://blog.google/products/ads-commerce/2021-01-privacy-sandbox/

[protected classes]: https://support.google.com/adspolicy/answer/143465?hl=en

[pursuing anti-trust actions]: https://digiday.com/media/why-googles-approach-to-replacing-the-cookie-is-drawing-antitrust-scrutiny/

### *Related Media*

* [The Social Dilemma (2020)](https://www.thesocialdilemma.com/) - 
  An excellent docudrama on the kinds of tracking that social networking 
  advertising companies are conducting on their users. Very concerning.

### *Related Articles*

* [Shame on the NSA](/articles/2013/10/21/shame-on-the-nsa/) - Back in 2013 
  I was particularly vexed with the kind of privacy-invasive tracking that 
  Edward Snowden revealed the NSA to be conducting on all US citizens, 
  and almost certainly still is.

* [Exploring Onionland: The Tor .onion Darknet](/articles/2013/04/21/exploring-onionland-the-tor-onion-darknet/) - Tor 
  is a technology that provides strong anonymization when browsing the internet.
  It also gives access to Tor Hidden Services (`.onion` domains) which is like a 
  parallel version of the internet. Here I describe my brief adventures in 
  exploring Tor Hidden Services.
