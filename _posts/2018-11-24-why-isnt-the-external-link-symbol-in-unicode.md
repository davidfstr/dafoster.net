---
layout: post
title: "Why isn't the external link symbol in Unicode?"
tags: [Software]
x_audience: |
    folks who use Unicode characters in computerized writing
x_performance: |
    I seem to get about 30 hits per week as of 2021-02-06,
        mostly from this Quora article:
        https://www.quora.com/Is-the-symbol-for-external-link-available-in-Unicode-If-so-how-do-I-get-in-on-my-Mac

---

I have frequently wanted to use the external link symbol ( ![external link](/assets/2018/external_link.png) ) in text that I'm writing, without having to resort to including an image. Normally the solution there would be to find the graphical symbol in Unicode and figure out how to type it.

Apparently at least one [proposal] for the external link symbol was submitted to the Unicode Consortium as far back as August 2006. It was reviewed at a meeting on November 2006 and it was decided to post a [public review].

Later in April 2012 someone noticed that the public review had never been posted because the symbols subcomittee (which was tasked with posting the review) had been folded into the Unicode Technical Committee group and that task had gotten [lost in the shuffle].

Then in June 2012 that proposal was finally [rejected] on the following basis:

> **2012-2, EXTERNAL LINK SIGN, 2012-June-06**
> 
> Proposals to encode a character for the "external link sign", which is often seen as a graphic element indicating a link to a document located external to the website where the page using the external link sign resides. (See L2/06-268, L2/12-143, L2/12-169.)
> 
> **Disposition**: The UTC rejected the proposals to add "external link sign", most recently in L2/12-169. It is unclear that the entity in question is actually an element of plain text, given the inevitable connection to its function in linking to other documents, and thus its coexistence with markup for links. Furthermore, the existing widespread practice of representing this sign on web pages using images (often specified via CSS styles) would be unlikely to benefit from attempting to encode a character for this image. (This notice of non-approval should not be construed as precluding alternate proposals which might propose encoding a simple shape-based symbol or symbols similar in appearance to the images used for external link signs, should an appropriate plain-text argument for the need to encode such a simple graphic symbol be forthcoming.) References to UTC Minutes: [131-C26], May 10, 2012.

I find this rejection disappointing.

Its main rationale appears to be that the external link icon is not an element of plain text. I would agree that is the case. However I would like to point out that emoji and other similar useful symbols are not plain text either yet they have been accepted and continue to be accepted.

I wonder if the external link symbol would be accepted as an emoji? I don't have enough energy right now to pursue that myself.

<!-- Also of interest: The rationale for rejecting the external link symbol discouraged another person from even submitting the feed symbol for consideration: https://jameshfisher.com/2017/09/29/unicode-is-only-for-plaintext.html -->

**2021 Update:** These days I use the ⎋ symbol to approximate the external link
symbol in my own informal writing. I've also used 🔗 in the past.

[proposal]: https://www.unicode.org/L2/L2006/06268-ext-link.pdf
[public review]: https://www.unicode.org/L2/L2006/06324.htm#109-C26
[lost in the shuffle]: https://www.unicode.org/L2/L2012/12143-ext-link.html
[rejected]: https://www.unicode.org/alloc/nonapprovals.html