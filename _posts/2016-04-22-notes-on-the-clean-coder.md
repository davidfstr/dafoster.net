---
layout: post
title: 'Notes on &ldquo;The Clean Coder&rdquo;'
tags: [Software]
x_started_on: 2016-03-23
style: |
    .notcc-page-location {
        color: lightgray;
        margin-bottom: .7em;
        speak: none;
    }

---

I recently picked up a copy of [The Clean Coder]: An excellent book about the non-technical aspects of being a senior software engineer.

Below are my notes taken while reading the book.

[The Clean Coder]: http://www.amazon.com/Clean-Coder-Conduct-Professional-Programmers/dp/0137081073/ref=as_li_ss_tl?ie=UTF8&keywords=the%20clean%20coder&qid=1461339725&ref_=sr_1_1&sr=8-1&linkCode=ll1&tag=dafo07-20&linkId=11da6a52e5ac10bdef1499cb5b5fab88

## Introduction

<div class="notcc-page-location">xvi.</div>

Management sometimes doesn't view software engineers as professionals in the same way, for example, they treat lawyers as professionals.

In this situation management is likely to babysit the engineers, micromanage them, and be more prone to asking them to sacrifice their personal lives for the current project.

As an engineer this situation is undesirable. This book intends to show you how to present yourself and interact as a *professional*.

<div class="notcc-page-location">xxii.</div>

Specifically:

* What is a software professional?
* How does a professional behave?
* How does a professional deal with conflict, tight schedules, and unreasonable managers?
* When, and how, should a professional say "no"?
* How does a professional deal with pressure?


## Values

### Responsible

<div class="notcc-page-location">10.</div>

"Upon reflection I realized that shipping without testing the routine had been irresponsible. The reason I neglected the test was so I could say I had shipped on time. It was about me saving face. I had not been concerned about the customer, nor about my employer. I had only been concerned about my own reputation."

"I should have taken responsibility early and told Tom that the tests weren't complete and that I was not prepared to ship the software on time. That would have been hard, and Tom would have been upset. But no customers would have lost data, and no service managers would have called."

### Accountable

<div class="notcc-page-location">12.</div>

It is the lot of a professional to be accountable for errors even though errors are virtually certain. Practice apologizing.

Apologies are necessary but insufficient. As you mature, your error rate should rapidly decrease toward the asymptote of zero.

### Bugs that Escape

<div class="notcc-page-location">12.</div>

QA should find nothing.

If a bug reaches QA, figure out why those bugs managed to escape your notice and do something to prevent it from happening again.

Every time QA, or worse a *user*, finds a problem, you should be surprised, chagrined, and determined to prevent it from happening again.

### Strive for Quality

<div class="notcc-page-location">13.</div>

100% line coverage is a minimum bar of quality, in the opinion of Robert C. Martin.

<div class="notcc-page-location">15.</div>

Merciless refactoring: Every time you look at a module you make small, lightweight changes to it to improve its structure.

### Learning & Teaching

<div class="notcc-page-location">16.</div>

Train yourself outside of work. For your career.

* Buy books.
* Goto conferences.
* Spend time each week practicing.
* Know the history of computer science. Many gems are there.

<div class="notcc-page-location">20.</div>

Train your juniors! The best way to learn is to teach.


### Know Your Business Domain

<div class="notcc-page-location">21.</div>

Know your business domain well enough to be able to recognize and challenge specification errors.


## Estimates & Saying No

<div class="notcc-page-location">25.</div>

Stick to your guns RE schedule estimates. Professionals speak truth to power. Professionals have the courage to say no to their managers.

<div class="notcc-page-location">26-28. 30.</div>

Negotiate!

<div class="notcc-page-location">30.</div>

Being a *team player* means player your position as well as you possibly can, and helping out your teammates when they get into a jam.

<div class="notcc-page-location">32-36.</div>

There is no "trying".

If you are not holding back some energy in reserve, if you don't have a new plan, if you aren't going to change your behavior, and if you are reasonably confident in your original estimate, then promising to try is fundamentally dishonest. You are *lying*. And you are probably doing it to save face and to avoid a confrontation.

<div class="notcc-page-location">34.</div>

(Passive aggression is when you let someone else hang themselves through inaction on your part.)


## How and When to Code

<div class="notcc-page-location">58.</div>

Confidence and error-sense is the key to mastery.

<div class="notcc-page-location">59.</div>

Write code to reveal intent.

Worrying? Tired? Don't code!

<div class="notcc-page-location">62-64.</div>

The author avoids the flow zone. I find it useful for routine code, and less useful for novel code.

<div class="notcc-page-location">63.</div>

Music can be a plus or minus when writing code. It only works well for me when I'm writing routine code (and not novel code).

<div class="notcc-page-location">63.</div>

Interruptions happen. Try not to be rude.

Refinding your place after an interruption can be tricky. I personally find having an active card useful, as I can just review the card and the checklist on it that I was working through.


## Automated Tests

### Acceptance Tests

Acceptance tests are a special kind of automated test that specifically test the *stakeholder-desired* behaviors of a feature. Once the acceptance tests pass, the feature is "done" from the perspective of the stakeholders. This is extremely powerful.

<div class="notcc-page-location">100.</div>

Acceptance tests should be written as a collaboration of the stakeholders and the programmers.

<div class="notcc-page-location">109.</div>

Unit tests and acceptance tests (which are not the same thing) are documents first and tests second. Their primary purpose is to formally document the design, structure, and behavior of the system. The fact that they automatically verify the design, structure, and behavior that they specify is wildly useful, but the specification is the true purpose.

<div class="notcc-page-location">110.</div>

Make sure that all your unit tests and acceptance tests are run several times per day in a *continuous integration* system.

It is very important to keep the CI tests running at all times. A broken build in the CI system should be viewed as an emergency, a "stop the presses" event.

### Other kinds of automated tests

<div class="notcc-page-location">114.</div>

Automated tests can act to:

1. *Specify* the desired behavior or properties of a component.
2. *Characterize* the current behavior of a component. Useful to detect unexpected changes. Unlike a specifying test, a characterizing test does not worry as much whether the behavior being tested is actually the intended behavior.

<div class="notcc-page-location">116-117.</div>

Automated tests can be classified based on the size of the things they put under test:

* Unit tests - Test individual functions or classes.
* Component tests - Test individual components or features.
* Integration tests - Test how multiple components or features interact.
* System tests - Test the entire system. Throughput and performance tests are commonly of this variety.


## Time Management

### Meetings

There are two truths about meetings:

1. Meetings are necessary.
2. Meetings are huge time wasters.

Be very careful about which meetings you attend and which you politely refuse.

One of the most important duties of your manager is to keep you out of meetings.

Have an agenda and a goal: If you are asked to go to a meeting, make sure you know what discussions are on the table, how much time is allotted for them, and what goal is to be achieved. If you can't get a clear answer on these things, then politely decline to attend.

### Focus: A scarce resource

<div class="notcc-page-location">127-128.</div>

Focus is a scarce resource, rather like manna.

It is wise to manage one's time to take advantage of when focus-manna is available. Focus-manna is a decaying resource so it often needs to be used when it is available.

Sleep is paramount to recharge focus.

Power naps also work well for me personally.

### Blind alleys

<div class="notcc-page-location">131.</div>

The Rule of Holes: When you are in one, stop digging.

### Messes

<div class="notcc-page-location">132.</div>

Messes slow you down but don't stop you. Messes are worse than blind alleys because you can always see the way forward, and it always looks shorter than the way back (but it isn't).


## Estimates

<div class="notcc-page-location">138.</div>

Businesses like to view estimates as commitments. Developers like to view estimates as guesses.

* A commitment is something you must achieve.
* An estimate is a guess. No commitment is implied.

Commitment is about certainty. Other people are going to make plans based on your commitments.

An estimate is not number, despite it often being presented as such. Rather, it is a *distribution*.

<div class="notcc-page-location">141.</div>

There is a system of estimation called "PERT" or "trivariate analysis". You give an estimate as a combination of {Optimistic Estimate, Nominal Estimate, Pessimistic Estimate}, which creates a beta distribution. These distributions can be added together to determine the combined time distribution for performing a *series* of tasks.

<div class="notcc-page-location">141.</div>

Estimating tasks with a group of team-members is more accurate than estimating by oneself. There are many techniques for this. Probably the most famous is "planning poker". There is also "affinity estimation" and "flying fingers".


## Pressure

<div class="notcc-page-location">153.</div>

You know what you believe by observing yourself in a crisis.

If in a crisis you follow your disciplines, then you truly believe in those disciplines. On the other hand, if you change your behavior in a crisis, then you don't truly believe in your normal behavior.

Choose disciplines that you feel comfortable following in a crisis. Then follow them all the time.

<div class="notcc-page-location">154.</div>

Avoid creating surprises. Nothing makes people more angry and less rational than surprises.


## Teams

<div class="notcc-page-location">168.</div>

When assigning work to folks, there's no such thing as half a person. You cannot sensibly tell a programmer to devote half their time to project A and half their time to project B.

<div class="notcc-page-location">169.</div>

For a 12-person team, here's a suggested team composition:

* 7 devs
* 2 testers -- Who write acceptance tests, focusing on correctness, failure, boundary cases.
* 2 analysts -- Who write acceptance tests, focusing on business value and the happy path.
* 1 project manager

<div class="notcc-page-location">171.</div>

It's reasonable to assign multiple projects to a single team. Particularly if the team has gelled.

On the other hand assigning multiple projects to a single person is not a great idea.


## Mentoring, Apprenticeship, and Craftsmanship

<div class="notcc-page-location">182.</div>

Software apprenticeship: A very interesting idea. Consider the following levels of proficiency:

* Master
* Journeymen
* Apprentice / Intern

(See the descriptions in the book.)

<div class="notcc-page-location">184.</div>

A *craftsman* is someone who works quickly, but without rushing, who provides reasonable estimates and meets commitments. A craftsman knows when to say no, but tries hard to say yes. A craftsman is a professional.

School can teach the theory of computer programming. But school does not, and cannot teach the discipline, practice, and skill of being a craftsman.