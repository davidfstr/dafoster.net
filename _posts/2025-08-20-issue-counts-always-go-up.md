---
layout: post
title: Issue counts always go up
tags: [Software]

wide_image_filepath: /assets/2025/issue-counts-always-go-up/issue-asteroids.jpg

style: |
    #issue-asteroids {
        max-width: 350px;
        max-height: 400px;
        float: right;
        margin-left: 5px;
    }
    @media (max-width: 690px) {
        #issue-asteroids {
            max-width: 300px;
        }
    }
    @media (max-width: 560px) {
        #issue-asteroids {
            max-width: 250px;
        }
    }
    @media (max-width: 500px) {
        #issue-asteroids {
            max-width: 100%;
            float: none;
            display: block;
            margin: 0 auto;
        }
    }

---

<a href="/assets/2025/issue-counts-always-go-up/issue-asteroids.jpg"><img id="issue-asteroids" src="/assets/2025/issue-counts-always-go-up/issue-asteroids.jpg" alt="A spaceship labelled 'Me' firing shots at a big asteroid, labelled '-1 Issue'. The big asteroid is exploding into 3 smaller asteroids, each labelled '+1 Issue'." data-credits="Gemini 2.0 Flash Preview Image Generation, prompted and manually edited in Acorn by David Foster" /></a>

I've noticed that the GitHub issue count on my software project Crystal always seems to go up, even though I'm the only one who ever files issues (for now) and even though I'm actually completing issues occasionally.

I think I've figured out why: Often when I complete an issue, I only complete the first 80% of the issue which is most valuable to me and file smaller issues for the remaining 20% that is left. So I end up with 1 big issue completed and 2+ smaller issues created. Net effect is that **more issues are opened than closed even though the missing functionality goes down**.

It's like a game of asteroids, where blowing up the big asteroid just creates a bunch of smaller asteroids.

So I can't easily see progress by watching the *issue count* go down. Instead I need to think of a way to measure the amount of *missing functionality* so that I can see that go down instead and feel good about completing issues. 🙂

<img src="/assets/2025/issue-counts-always-go-up/measuring-bugs.jpg" style="max-width: 100%; max-height: 300px; display: block; margin: 0 auto;" alt="Professor holding a measuring tool over a set of small bugs arranged on a table." data-credits="Gemini 2.0 Flash Preview Image Generation, prompted by David Foster" />
