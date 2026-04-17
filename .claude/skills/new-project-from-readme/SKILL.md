---
name: new-project-from-readme
description: Scaffold a new project page under the dafoster.net site's projects/<slug>/ directory from an existing project's README.md. Creates index.md with the site's project frontmatter and copies over logo files.
disable-model-invocation: true
argument-hint: <project-slug> <absolute-path-to-README.md>
---

# new-project-from-readme

Scaffold a new project page on [dafoster.net] at `projects/<slug>/index.md`
from an existing project's `README.md`.

[dafoster.net]: https://dafoster.net/projects/

This skill is local to the dafoster.net site repo. Run it from the site
repo's root directory (the one containing `projects/`, `_config.yml`,
etc.) — paths referenced below are relative to that root.

## Why this skill exists

The GitHub-hosted README.md of an open-source project is SEO-disadvantaged
compared with a dedicated project page at `https://dafoster.net/projects/<slug>/`.
So whenever David creates a substantive open-source project, he adds a
project page to `dafoster.net` that mirrors much of the README's content,
adapted for a public portfolio context.

The site's Jekyll build renders these pages from `index.md` using the
`project` layout, which expects a specific set of frontmatter fields.
This skill handles that scaffolding.

## Input

`$ARGUMENTS` is `<project-slug> <absolute-path-to-README.md>`.

- **`<project-slug>`** — The directory name under `projects/` (e.g.
  `revise-mcp`, `burn-planner`). Conventionally matches the project's
  GitHub repository name.
- **`<absolute-path-to-README.md>`** — Absolute path to the source
  project's `README.md`. The project's root directory is the parent of
  this file; the git repo is assumed to live there.

If either argument is missing, stop and ask the user.

## Procedure

### 1. Examine the source project

- Read `README.md` at the given path.
- List the contents of the project's root directory and its `README/`
  subdirectory (if present) to locate logo files. Common names:
  `logo-big.svg`, `logo-big.png`, `logo.svg`, `logo.png`.
- Run `git log --reverse --format="%ai %s" | head -3` in the project root
  to find the first commit date (for `started_on`).
- Check for language cues in the project root (e.g. `pyproject.toml` →
  Python, `package.json` → JavaScript/TypeScript, `Cargo.toml` → Rust,
  `Gemfile` → Ruby).

### 2. Create the target directory

Target: `projects/<slug>/` (relative to the site repo root).

If it already exists and is non-empty, stop and ask the user whether to
overwrite before proceeding.

### 3. Copy logo files

Copy the project's logo files into the target directory. Prefer both an
SVG and PNG if both exist (`logo_filename` in frontmatter points at the
SVG, `logo_png_filename` at the PNG fallback). If only one format
exists, use that.

### 4. Draft `index.md`

Write `index.md` with the frontmatter below, followed by Markdown body
content adapted from the README.

#### Frontmatter

Always include these fields:

```yaml
---
layout: project
title: <human-readable project name from README's top-level heading>
summary: >
    <1–3 sentence description, typically adapted from the README's
    intro paragraph. Keep it tight — this shows up in listings.>
logo_filename: <e.g. logo-big.svg, or logo.png if no SVG>
logo_png_filename: <e.g. logo-big.png — omit if logo_filename is already a PNG>
started_on: <YYYY-MM-DD of first commit in the project's git repo>
ended_on: ongoing
x_started_on_source: first commit in git repo
x_ended_on_source: TBD
x_languages: [<primary language, e.g. Python>]
x_location: Cathode at <absolute path to the project root>
featured: true

---
```

Notes on specific fields:

- `title` — Usually matches the README's `# <Title>` heading. For
  projects with a disambiguating subtitle (e.g. "gvc (Git Visual
  Compare)"), preserve that.
- `summary` — Use YAML's folded-block (`>`) form indented 4 spaces.
  Aim for one to three sentences.
- `logo_filename` / `logo_png_filename` — See reference pages for
  patterns. If no logo is available, omit both fields.
- `x_languages` — A list; use `[Python]`, `[JavaScript, TypeScript]`,
  etc. If uncertain, make a best guess from project files.
- `x_location` — The absolute path to the project's root directory on
  David's machine (Cathode), prefixed with `Cathode at `.
- `featured: true` — Default to `true` unless the user indicates
  otherwise.

#### Body

Do NOT paste the README verbatim. Adapt it for a standalone portfolio
page that a stranger might land on via search. Suggested structure,
loosely modeled on `projects/revise-skill/index.md` and
`projects/revise-mcp/index.md`:

1. **Lead paragraph** — One sentence: bold the project name, say what
   it is, link to the upstream concept if applicable (e.g. "an [MCP]
   server", "an [Agent Skill]").
2. **`## Why?`** — Motivation. Often the README has a "Why This Exists"
   or intro section that can be adapted here. This is the most
   important section for a portfolio reader.
3. **One or two feature-overview sections** — E.g. "What it reviews",
   "Tools", "How it works". Favour a summary table over exhaustive
   reference material.
4. **`## Installation`** — Copy the install steps from the README.
5. **`## Usage`** — Short usage examples. Not exhaustive.
6. **`## Learn More`** — Bulleted pointers:
   - Source code on GitHub (link to the repo's README)
   - Design doc / further reading (if the project has one)
   - Report a bug / request a feature (link to GitHub issues)

Skip README sections that are contributor-facing (local dev setup,
release process, internal conventions) — those belong on GitHub, not
the portfolio page.

### 5. Report to the user

Summarise what was created:
- Target path
- Frontmatter fields filled in (especially `started_on`,
  `x_languages`, `logo_filename`)
- Logo files copied
- Any fields left as `TBD` or assumptions made that the user should
  sanity-check

## Reference pages

Look at these existing pages in the site repo for style and structure
cues before drafting:

- `projects/revise-skill/index.md`
- `projects/revise-mcp/index.md`

Both are good templates for a tool/library-style project. For
GUI/app-style projects, see `projects/gvc/index.md`.
