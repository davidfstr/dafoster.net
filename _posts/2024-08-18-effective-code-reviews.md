---
layout: post
title: Effective Code Reviews
tags: [Software]

---

Software engineering research has identified[^making-software] some techniques and rules of thumb for making code reviews more effective at identifying defects:

1. Limit code reviews to **1 hour or less**.
    * After 60-90 minutes into a code review the ability to find further defects drops off dramatically due to focus fatigue.
    * If a code review in progress is dragging on past 1 hour, consider taking a break and continuing the remainder later in a "part 2".
2. Limit code reviews to **400 lines of code or less**.
    * Code reviews performed faster than 400-500 lines of code per hour show a dramatic drop in density of detected defects.
    * Combining that result with the earlier result that reviews lasting longer than 1 hour are problematic, we can conclude that no more than 400 lines of code should be reviewed in the same session.
3. **Identify the most complex/risky/controversial changes to review first** when there is the least focus fatigue.[^risky-changes-first]
4. **Link to related "context" (i.e. files, documentation, classes, etc)** alongside the immediate changes of a code review, for a 15-30% increase in defect detection.
5. **Self-review changes before posting them for external review**, because 50% of defects can be found in a self-review at half the time cost of an external review.
6. An individual code review should be either asynchronous or synchronous but not both.
    * For a code review posted asynchronously, there is little gain in following up with an additional full synchronous review: Only an additional 4% of defects are likely to be found.

[^making-software]: All results in this article originate from the "Modern Code Review" chapter of ["Making Software: What Really Works, and Why We Believe It"](https://www.amazon.com/Making-Software-Really-Works-Believe/dp/0596808321) by Jason Cohen, unless otherwise specified.

[^risky-changes-first]: This result comes from another source which I have since forgotten.