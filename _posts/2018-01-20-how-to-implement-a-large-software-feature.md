---
layout: post
title: How to implement a large software feature
tags: [Software]

style: |
    /* Override blockquote to use same font size as body text */
    blockquote { font-size: 16px !important; }

---

I just started implementing my first big new software feature since the start of the New Year. I thought I'd outline my process since I don't think I've written it down before.

Let's begin: A feature request comes in. In my case:

> **Dynamic Calendar for Teachers:** Extend our existing Plan page, which shows a calendar of daily activities, such that classroom teachers (our customers) can move activities around on the calendar without engaging our support team over live chat.

I'm working in a large existing codebase and this feature needs to be integrated with existing code. This is a common situation.

### 1. Review the current behavior

We already have a **Dynamic Calendar for Staff** feature implemented that our support staff can use to rearrange calendars. It just hasn't been released directly to teachers because there a few rough edges that need to be polished off first.

Therefore this new feature is primarily a UI change, publicizing existing functionality, along with some backend adjustments to the functionality to make it bulletproof.

I annotate a screenshot of the current Dynamic Calendar dropdown that staff can use to manipulate days on the calendar:

<a href="/assets/2018/how-to-implement-a-large-software-feature/before.png">
    <img alt="High-fidelity UX mockup: Weekly calendar with open dropdown menu, that is divided into 3 sections." src="/assets/2018/how-to-implement-a-large-software-feature/before.png" style="max-width: 100%;" />
</a>

### 2. Design the new behavior. Write out the delta between the old and new behaviors.

I mock up proposed new UI. In this case I just use a text file:

```
--------------------
Add empty day / Add teaching day...
Remove empty day
-------------------- ▲ teacher sees
Go to admin page ❏
Add empty day (without relayout)
Remove empty day (without relayout)
Relayout
-------------------- ▲ staff sees
```

In other cases I actually create a visual mockup using a diagram on paper or a graphics program.

I also write up a summary of behavioral changes:

```
* Remove teacher actions (because deprecated):
    - Set as non-teaching day
* Add teacher actions:
    - Add teaching day...
        - Needs to prompt for start/end times.
            > Suggest specific options based on existing schedule.
            > Allow full customization as well.
* Publicize and change actions:
    - Add empty day
        - May now perform a relayout. Is slow. Can fail.
        - Adds day at the current day rather than after it.
    - Remove empty day
        - May now perform a relayout. Is slow. Can fail.
        - Continues to require day to be empty of skipped objects too.
          Teacher can now see skipped objects and move them elsewhere
          before removing an otherwise empty day.
* Remove staff actions (because deprecated):
    - Domino step
    - Domino cascade
* Add staff actions:
    - Add empty day (without relayout)
    - Remove empty day (without relayout)
    - Relayout
```

These behavior changes also imply the addition of some new popups, which I also mock up in another text file.

With the new behavior now clearly written out, it's time to review it with a member of the User Experience team. They approve the proposed design with some changes.

I also review the new behavior with the member of the Engineering team most familar with the affected subsystems. In this example that person is myself, so there is no further action.

### 3. Write out engineering tasks that perform the deltas

For this example, here’s a simplified version of the tasks I write out:

```
[ ] Rip out all DC actions that involve a domino or other magic. #EasyWin
[ ] Merge "can manage" and "can admin" permissions to just "can admin".
=== Familiar with DC logic. Prior system complexity minimized. [1]
[ ] Add "Relayout" action that redirects to the existing "Recreate class calendar suffix" page
[ ] Retitle:
    - Add empty day -> Add empty day (without relayout)
    - Remove empty day -> Remove empty day (without relayout)
[ ] Alter "Add empty day" to add *at* the specified day rather than *after*
=== Staff-facing actions are ready for release [1]
[ ] Add "newdc" feature flag
[ ] Implement new DCD action: Add empty day, behind "newdc" flag
    - ... (details elided)
[ ] Implement new DCD action: Remove empty day, behind "newdc" flag
    - ... (details elided)
=== Teacher-facing actions are ready for release. [3]
[ ] Announce the DC feature to teachers
    - ... (details elided)
[ ] Remove "newdc" feature flag
=== Released. [1]
```

I may review the engineering tasks with another member of the Engineering team if I uncover any additional details that merit review. In this example I do not.

I update the estimated time for the feature on the Project Management calendar. If the new time estimate has significantly increased then I contact Project Management to see whether any external deadlines are impacted and to negotiate if they are.

### 4. Perform the engineering tasks

This is the easy part: Develop, test, code review, merge, repeat.
