---
layout: project
title: Revise Skill
summary: >
    An Agent Skill that performs common code quality revisions on
    AI-drafted code, optimizing it for human readers.
logo_filename: logo-big.svg
logo_png_filename: logo-big.png
started_on: 2026-04-06
ended_on: ongoing
x_started_on_source: first commit in git repo
x_ended_on_source: TBD
x_languages: [Markdown]
x_location: Cathode at /Users/davidf/.claude/skills/revise
featured: true

---
The **Revise Skill** is an [Agent Skill] that performs common code quality
revisions on AI-drafted code, optimizing it for human readers.

[Agent Skill]: https://agentskills.io/


## Why?

Reviewing/revising AI generated code is now the bottleneck for me when
using AI agent harnesses like Claude Code and VS Code Copilot Agent to
write software. **This skill teaches an agent to revise its own code,
in the same way that I would do so personally**, so that I can automate
away commonplace revisions in advance of human review.

AI-written code is usually drafted in a way that is easy for an AI to
*write* but not necessarily easy to *read* later. For example, AIs
frequently use local imports in Python (contrary to convention) and tend
to write low-level functions before high-level ones (harder to skim).
The revise skill catches these patterns and fixes them.


## What it reviews

The skill checks for **code smells** organized into categories:

| Category | Example patterns |
|----------|-----------------|
| **Organization** | Local imports, bottom-up function order, parameter order mismatches, missing section headings |
| **Good Names** | Vague/generic names, names implying wrong type, abbreviations in APIs |
| **Clarity** | Magic numbers, short CLI flags in subprocess calls |
| **Formatting & Style** | Em/en dashes (signature AI style), British vs. American English |
| **Concision** | Unnecessary temporary variables, if/else → conditional expression |
| **Type Design** | Data clumps → dataclass, conditionally-meaningful fields |
| **Type Safety** | Missing `assert_never`, untyped parameters, `type: ignore` / `cast` overuse |

Each pattern has a detailed guide with rationale, "when NOT to apply"
notes, and before/after examples — see the
[patterns/](https://github.com/davidfstr/revise-skill/tree/main/patterns)
directory.

None of the revision types codified in this skill are speculative;
they all originate from actual revisions I made to real code.


## Installation

Clone the [revise-skill repository] into one of the skill directories
recognized by your AI coding tool.

[revise-skill repository]: https://github.com/davidfstr/revise-skill

### VS Code Copilot Agent — personal (all workspaces)

Any of these paths work:

```bash
git clone https://github.com/davidfstr/revise-skill.git ~/.claude/skills/revise
git clone https://github.com/davidfstr/revise-skill.git ~/.copilot/skills/revise
git clone https://github.com/davidfstr/revise-skill.git ~/.agents/skills/revise
```

### VS Code Copilot Agent — per-project

Clone into the project's `.github/skills/`, `.agents/skills/`, or
`.claude/skills/` directory:

```bash
git clone https://github.com/davidfstr/revise-skill.git .github/skills/revise
```

Or add as a git submodule to version-control the dependency:

```bash
git submodule add https://github.com/davidfstr/revise-skill.git .github/skills/revise
```

### Claude Code

```bash
git clone https://github.com/davidfstr/revise-skill.git ~/.claude/skills/revise
```

> **Note:** `~/.claude/skills/revise` is the one path that works for
> both VS Code Copilot and Claude Code.


## Usage

Invoke the skill and optionally specify what to review:

| Argument | What it reviews |
|----------|-----------------|
| `uncommitted` (default) | Uncommitted changes (`git diff` + `git diff --staged`) |
| `last-commit` | The most recent commit (`git diff HEAD~1`) |
| A list of files | The specified files in their entirety |
| A list of functions/classes | The specified symbols in context |

### VS Code Copilot

Type `/revise` in Copilot Chat, optionally followed by an argument:

```
/revise
/revise last-commit
/revise src/mymodule.py
```

### Claude Code

```
/revise
/revise uncommitted
```


## Learn More

* [Source code on GitHub](https://github.com/davidfstr/revise-skill#readme)
* [Report a bug or request a feature](https://github.com/davidfstr/revise-skill/issues/new)
