---
layout: post
title: AI Attribution in Git
tags: [Software]

---

When making a git commit I've been looking for a way to record what AI model or coding agent harness I used to help me write the commit, ideally in a machine-readable way.

For **AI-drafted code that I've reviewed** or **self-drafted code with significant AI revisions**, I add one of the following trailers to my git commit message:

* `Co-authored-by: Claude Opus 4.6 <noreply@anthropic.com>`
* `Co-authored-by: Claude Sonnet 4.6 <noreply@anthropic.com>`
* `Co-authored-by: Claude Haiku 4.5 <noreply@anthropic.com>`
* `Co-authored-by: GPT-5.3-Codex <noreply@openai.com>`
* `Co-authored-by: Google Gemini 3.1 Flash Image (Nano Banana 2)`
    * TODO: Identify an email address to use for Gemini

> Tip: I use [text expansion macros] like `coa → "Co-authored-by: "` and `aco → "Claude Opus 4.6 <noreply@anthropic.com>"` to type those trailers quickly.

[text expansion macros]: https://www.typesnap.app/blog/mac-text-replacement-guide/

For **AI-drafted code that I've NOT reviewed** (rare; mostly for internal or one-off tools):

* Author = one of the emails above, via `git commit --author="AI Model <noreply@example.com>"`.
* Co-authored-by = me:
    * `Co-authored-by: David Foster <david@dafoster.net>`

If I ever want to make such unreviewed or minimally-reviewed AI-drafted code public, I can use `git blame` to easily identify which lines are principally AI-drafted, so that I can go back and review them carefully; I never publish AI-written code that I haven't reviewed myself.

> Tip: I use the [Git Spotlight] tool to quickly see which lines of code are written by AI (`C4` = Claude Opus 4.6) or by me (`DF` = David Foster). See below:

<img alt="Visual 'git blame' view from the Git Spotlight VS Code extension" src="/assets/2026/ai-attribution-in-git/git-blame-view-in-git-spotlight.png" style="max-width: 100%" />

[Git Spotlight]: https://marketplace.visualstudio.com/items?itemName=SyedNisarUlHaq.git-spotlight

## Why the Co-authored-by pattern?

Claude Code introduced the convention of adding a `Co-Authored-By: Claude <noreply@anthropic.com>` trailer to any AI-authored commits by telling the AI to use such trailers [in its system prompt], much to the [annoyance] of some users. GitHub recognizes that Co-Authored-By trailer and displays Claude as a co-author of the related commit.

[in its system prompt]: https://github.com/Piebald-AI/claude-code-system-prompts/blob/5bb71ee182ec4005d8fad0ae18fc70a19da9572b/system-prompts/tool-description-bash-git-commit-and-pr-creation-instructions.md
[annoyance]: https://github.com/anthropics/claude-code/issues/45137#issuecomment-4234095781

I think that kind of attribution is lightweight and makes sense.