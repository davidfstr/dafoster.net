---
layout: post
title: Interview with David Foster
tags: [Personal]

x_original_url: https://softdroid.net/interviews/david-foster

metadata_extra: |
    <a href="https://softdroid.net/interviews/david-foster-ru">
        🇷🇺
        Russian translation
    </a>

---

<span style="color: gray;">*In March 2021 I was interviewed by Vladislav from softdroid.net. Since it gives a bit of my personal background, it may be of interest to others:*</span>

<span style="font-size: 1.5em; font-weight: 500;">I'm David Foster, software engineer, writer, and educator. I'm the CTO of TechSmart, where we seek to bring world-class computer science education to the next generation of K-12 students & teachers.</span>

### What is your programming background?

I've been programming since I was 6 years old, which means I've been at it for more than 25 years. I started with HyperCard (similar to Visual Basic or a 2D version of Unity) on a Mac SE making my own board games, music players, painting programs, and other toys for myself. Later I picked up Pascal, C/C++, and Java at National Computer Camps. And I continued learning on my own, picking up C#, Python, and JavaScript among other less-well-known languages.

### What languages / frameworks do you use mainly for coding?

These days I spend most of my time in web development, using Python/Django on the backend, JavaScript/Vue on the frontend, and Amazon Web Services for datacenter operations. Python is probably my favorite all-around language, with Java coming in second.

### How does your typical working day look like? How COVID-19 changed your working routine?

I wake around 6 AM, get myself ready to go, maybe work on a short personal item, and then start work at 8:30 AM. For the next 30 minutes I plan and write down what I'd like to do during the work day and process email. At 9 AM I have a daily standup meeting with the rest of the engineering team. Often immediately afterwards one or more folks will want to trade code reviews with me, or have a quick design discussion. For the rest of the morning until lunch I process various administrative items, reading email, updating our board of cards that track workitems, and have short meetings with other teammembers as needed. I take an hour lunch from 11:30 - 12:30, where the last half of that time I'll read up on the latest technical news, often from Hacker News and some other sources. Directly after lunch there may be someone else who wants to trade code reviews. Then I'll go heads-down coding for the rest of the day, working on my own items that require deep focus, up until the end of the work day at 5 PM sharp.

I'm rather structured with my time and am very careful to keep work within working hours. Otherwise - since I actually rather *enjoy* my work - I might just keep going and not get anything done with my personal time! It's important to avoid burning out even with a fun job.

COVID-19 has eliminated my commute entirely (saving about 30 minutes each way), and has encouraged me to increase my lunch break from 30 minutes to a full hour, so that I could take more time to make my own lunch and do some house chores at the same time. Not much else has changed at work.

### What is your current project you work on?

I just finished releasing [Crystal Web Archiver], a website downloader that is designed to archive and preserve websites for the long-term. I was dismayed to hear that DeviantArt's old portfolio websites were falling off the internet March 31st, so I wanted to get my downloader working again (so that I could save a few sites) before that happened.

I'm currently working on extending Python's optional static typechecking with [a new feature for TypedDict], that will make it easy to mark optional vs. required keys in a dictionary type, hopefully in time to make it into Python 3.10.

Later this year I hope to finish work on another optional static typechecking feature called [TypeForm], that will make it easy for me to implement [trycast], a library for validating the shape of JSON blobs (among other things) at runtime, which makes it easier to write secure web applications (among other uses). Hopefully this will be done before the Typing Summit at this year's PyCon conference.

In the background I'm striving to post a useful article on [my blog] each week, at least for the first quarter or two of 2021, with the goal of letting a wider variety of folks know about some of the interesting things I'm up to.

I'm not usually working on quite this many projects at the same time, but I seem to have gained a lot of new energy at the start of this year after the low of 2020 so I'm rolling with it for now. :)

[Crystal Web Archiver]: /articles/2021/03/23/crystal-web-archiver-beta-released/?utm_source=news&utm_medium=vlad&utm_campaign=crystal-2021

[a new feature for TypedDict]: https://www.python.org/dev/peps/pep-0655/?utm_source=news&utm_medium=vlad&utm_campaign=required

[TypeForm]: /projects/typeform/?utm_source=news&utm_medium=vlad&utm_campaign=typeform

[trycast]: /projects/trycast/?utm_source=news&utm_medium=vlad&utm_campaign=trycast

[my blog]: /articles/?utm_source=news&utm_medium=vlad&utm_campaign=articles

### Who would you recommend to look at TechSmart?

Right now TechSmart is focused on bringing computer science education to grades 3 through 12 in the United States. Any parent who is interested in their children learning to code that is in Washington, California, Texas, or Utah in particular may already be in a school district that we're serving.

Over the next few years I'd like to expand TechSmart to the majority of schools in the United States, and perhaps even go international to other countries, once we have enough staff to provide a quality experience to such a large number of locations. With patience and diligence I expect to realize this dream over time.
