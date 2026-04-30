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

| Category | Patterns |
|----------|-----------------|
| **Organization (file-level)** | local imports, bottom-up function order, unnecessarily public methods, many functions with no grouping section, sections grouped by kind not feature, symmetric operations split across modules, class-specific helpers off the using class, parameters not in visual/logical order |
| **Organization (within-function)** | single concern divided by blank line, multiple concerns without paragraph break, multi-paragraph sections not delimited, long then-block with empty else, guard clause hiding a peer alternative |
| **Good Names** | vague/generic names, names implying wrong type, abbreviations in APIs, failable operations missing `try_` prefix, lifecycle teardown not named `close` |
| **Clarity / Anti-Obscurity** | magic numbers, short CLI flags in subprocess calls, impl details in docstrings, obvious/redundant docstrings, unprefixed comments used as commentary, branch-scoped comments above the conditional, missing clarifying comments, truthy check instead of `is not None` |
| **Correctness / Safety** | silent early return on failure, manual resource cleanup, overscoped `try` block, counter-based wait loops, unmarked rebindings (`# reinterpret`/`# rename`/`# capture`/`# clone`), `let`/`var` instead of `const` (JS/TS) |
| **Formatting & Style** | em/en dashes (signature AI style), British vs. American English, imperative verbs in docstrings |
| **Concision** | duplicate code, unnecessary temporary variables, if/else → conditional expression, dead code, unnecessarily quoted type annotations, hand-rolled caching |
| **Type Design** | data clumps → dataclass, conditionally-meaningful fields, ignored `None` parameters |
| **Type Safety** | non-exhaustive variant dispatch (missing `assert_never`), `type: ignore` / `cast` overuse, untyped parameters, bare `dict` at serialization boundaries, overbroad `except` clauses |

Each pattern has a detailed guide with rationale, "when NOT to apply"
notes, and before/after examples — see the
[patterns/](https://github.com/davidfstr/revise-skill/tree/main/patterns)
directory.

None of the revision types codified in this skill are speculative;
they all [originate from actual revisions I made to real
code](#how-patterns-are-added).


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


## Optional companion: Revise MCP server

The Revise Skill is designed to work alongside the
[Revise MCP server](https://dafoster.net/projects/revise-mcp/),
which exposes refactoring tools (`rename_symbol`, `move_string_in_file`,
`indent_dedent`, `outline_file`) that let an agent edit code more
efficiently than line-based text edits. When the MCP server is
installed, the skill instructs the agent to reach for those tools
where appropriate.

The MCP server is an **optional dependency** — the skill works
without it, falling back to standard text edits.


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


## How patterns are added

Every pattern in this skill traces back to a real revision I made by
hand to AI-drafted code. The workflow:

1. Revise a recent AI-drafted commit by hand and push the revisions
   as a single commit.
2. Invoke the skill on that commit with phrasing like
   *"Learn any new revise patterns from commit `<SHA>`"*.
3. The skill reads the diff (and commit message), interviews me about
   non-obvious choices and any patterns the diff *should* have
   triggered but didn't, then either drafts a new pattern file or
   refines an existing one.

This keeps the catalog grounded in actual friction encountered in
practice rather than speculative best practices. See
[SKILL.md](https://github.com/davidfstr/revise-skill/blob/main/SKILL.md#how-to-learn-new-patterns-from-a-commit)
for the full procedure.


## Learn More

* [Source code on GitHub](https://github.com/davidfstr/revise-skill#readme)
* [Report a bug or request a feature](https://github.com/davidfstr/revise-skill/issues/new)
