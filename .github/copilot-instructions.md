# Project Guidelines

## Overview

Personal website of David Foster — a Jekyll 3.9.1 static site deployed to GitHub Pages. See [README.md](../README.md) for installation and Docker setup.

## Build and Test

All commands run inside the Docker container (`docker exec -it dafoster.net bash --login`):

- `rake preview` — Local dev server at http://localhost:4000/ (auto-rebuilds on changes)
- `rake go` — Same as preview, but opens browser automatically
- `rake prism` — Build the `/prism/` legacy subsite separately
- `rake dist` — Full production build (validates dates, builds Jekyll + prism)
- `rake deploy` — Deploy to GitHub Pages via git

## Architecture

```
_posts/           Blog posts (YYYY-MM-DD-slug.md)
_posts_support/   Post-specific assets (images, code samples)
_posts_unpublished/ Draft posts
_layouts/         Page templates (default → post, page, project, home_page)
_includes/        Reusable partials (blocks/, JB/)
_plugins/         Custom Ruby/Python plugins
projects/         Project showcase pages (each has index.md)
prism/            Legacy web app built via prism.py plugin (SSI-based)
_production/      Git-managed deployment output
```

- **Markdown engine**: RDiscount (supports footnotes, multi-level bulleted lists)
- **CSS framework**: Bootstrap 3
- **Permalinks**: `/articles/:categories/:year/:month/:day/:title/` (clean, no extensions)

## Conventions

### Blog Posts

Frontmatter format:
```yaml
layout: post
title: Post Title Here
tags: [Software]
```

Optional fields: `date_updated`, `title_long`, `description`, `metadata_extra`

- Post dates **must be unique** across all posts (enforced by `checkdates.py` for Atom feed stability)
- File naming: `YYYY-MM-DD-slug.md` in `_posts/`
- Post-specific assets go in `assets/YYYY/slug/`
- If assets require generation scripts or a complex build process, those scripts/sources go in `_posts_support/YYYY-MM-DD-slug/` (with `src/`, `inputs/`, `outputs/` subdirs as needed)

### Project Pages

Frontmatter format:
```yaml
layout: project
title: Project Name
summary: >
    Description of the project.
logo_filename: logo.svg
started_on: YYYY-MM-DD
ended_on: ongoing
x_languages: [Python]
featured: true
```

### Content Authoring

- Use RDiscount markdown features (footnotes, smart quotes via SmartyPants)
- Code blocks: `{% highlight ruby %}...{% endhighlight %}`
- The `fixbullets.rb` plugin handles multi-level list spacing — don't manually add `<p>` tags in lists
- Use `{% long_url %}...{% endlong_url %}` for breaking long URLs

### Plugins

- `customfilters.rb` — Liquid filters (date formatting, sorting, tag helpers)
- `checkdates.py` — Validates unique post dates (runs during `rake dist`)
- `prism.py` — Builds `/prism/` subsite from `.shtml` files
- `fixbullets.rb` — Fixes bulleted list rendering
- `debug.rb` — Development-only `{{ site | debug }}` filter

## Environment

- Ruby 2.6 via RVM, Python 2.7, inside Docker (Ubuntu 14.04)
- Jekyll pinned to 3.9.1 (Jekyll 4.x dropped RDiscount support)
- Bundler 1.17.3
- Development config override: `_config-develop.yml` sets `develop: true`
