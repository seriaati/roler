# Plan: Migrate README to mkdocs-material Documentation

## Goal

Move the dense syntax reference and usage guides from [`README.md`](README.md) into a dedicated **mkdocs-material** documentation site under `/docs`, then slim the README down to a concise project overview that links to the full docs.

---

## Documentation Structure

```
docs/
├── index.md                     # Landing page - hero banner, tagline, feature bullets, invite link
├── getting-started.md           # Permissions, invite, first-panel walkthrough (steps 1-5 from README)
├── guide/
│   ├── creating-panels.md       # Writing templates, create/update/delete workflow, row rules
│   └── reusable-templates.md    # [template id=...] system: define, reference, auto-update, end-to-end example
├── reference/
│   ├── button.md                # Full [button] tag reference (role, template, url, color, mode, emoji, disabled, rows)
│   ├── separator.md             # [separator] tag + --- alias
│   ├── image.md                 # [image] tag
│   ├── gallery.md               # [gallery]...[/gallery] + [item] tags
│   ├── webhook.md               # [webhook] tag
│   └── template-tag.md          # [template id=...] tag (definition side)
├── validation.md                # Complete list of validation rules
└── self-hosting.md              # Requirements, env vars, local run, Docker
```

---

## File-by-file Breakdown

### 1. `mkdocs.yml` (project root)

- **Theme**: `material` with custom palette (dark/light toggle)
- **Nav**: mirrors the tree above
- **Plugins**: `search`
- **Markdown extensions**: `admonitions`, `attr_list`, `md_in_html`, `pymdownx.highlight`, `pymdownx.superfences`, `pymdownx.tabbed`, `pymdownx.details`, `tables`, `toc` (with permalink)
- **Extra**: repository link to GitHub, footer with copyright
- **docs_dir**: `docs`

### 2. `docs/index.md`

- Embed banner image from `images/BannerWithLogo.png` (reference via relative path `../images/`)
- One-paragraph description
- Feature bullet list (Components v2, Customizability, Easy edits, etc.)
- Invite button link
- Showcase image
- Quick links to Getting Started + Reference sections

### 3. `docs/getting-started.md`

- Bot invite link
- Required permissions table (from README "Bot permissions" section)
- Role hierarchy note
- Quick walkthrough: write template → right-click → Create Role Panel → select channel
- Link forward to the guide pages for deeper detail

### 4. `docs/guide/creating-panels.md`

Content from README sections "Usage" steps 1–5:

- Writing a template (code blocks, plain text)
- Node types overview (text, buttons, separators, images, galleries, webhook)
- Full example template (the `# Welcome to role picker` example)
- Creating a panel (right-click flow)
- Updating a panel (edit detection, error DM behavior)
- Deleting a panel (right-click flow)
- Link to Reference section for per-tag details

### 5. `docs/guide/reusable-templates.md`

Content from README "Reusable Templates" section:

- What templates are + why
- The `[template id=...]` tag
- Defining a template (context menu)
- Referencing via `template=` on a button
- Auto-update on edit (re-parse, error handling, tag removal = delete)
- End-to-end example (steps 1–5 from README)

### 6. `docs/reference/button.md`

- Syntax: `[button attrs]Label[/button]`
- Full attribute table (role, template, url, color, mode, emoji, disabled) - sourced from README
- Modes explanation (toggle/add/remove)
- Custom Discord emojis section (including animated)
- URL buttons section (always grey, mutually exclusive with role/template)
- Disabled buttons section
- Row rules (same line = one row, blank line = new row, max 5 buttons/row, max 5 rows)
- Examples

### 7. `docs/reference/separator.md`

- Syntax: `[separator]` + `---` alias
- Attribute table (size, visible)
- Examples

### 8. `docs/reference/image.md`

- Syntax: `[image url=... spoiler=...]`
- Attribute table (url, spoiler)
- Examples

### 9. `docs/reference/gallery.md`

- Syntax: `[gallery]...[/gallery]` with `[item]` children
- Attribute table for `[item]` (url, spoiler)
- Item count limit (1–10)
- Examples

### 10. `docs/reference/webhook.md`

- Syntax: `[webhook name=... avatar=...]`
- Attribute table (name, avatar)
- Behavior: not rendered as panel content, bot re-sends on identity change
- Examples

### 11. `docs/reference/template-tag.md`

- Syntax: `[template id=...]`
- ID constraints (alphanumeric, hyphens, underscores, 1–64 chars)
- Scoping (per-guild)
- Placement (top of message)
- Link to guide page for full workflow

### 12. `docs/validation.md`

Full list of validation rules from README "Template validation rules" section, organized into categories:

- Button rules
- Row rules
- Webhook rules
- Template button rules
- URL button rules
- Image rules
- Gallery rules

### 13. `docs/self-hosting.md`

- Requirements (Python 3.14+, PostgreSQL)
- Environment variables table
- Running locally (`uv sync && uv run main.py`)
- Running with Docker

### 14. Slim down `README.md`

New README keeps:

- Banner + Showcase images
- Project name + one-line description
- Invite link
- "Why is this better?" feature bullets
- "📖 Read the full documentation →" link to the docs
- Brief self-hosting pointer (with link to docs/self-hosting.md)
- Acknowledgements

Removes all syntax definitions, validation rules, and step-by-step usage (now in docs).

### 15. `pyproject.toml` changes

Add to `[dependency-groups]` dev:

```toml
docs = ["mkdocs>=1.6", "mkdocs-material>=9.6"]
```

---

## Key Design Decisions

1. **Reference pages per tag** - Each markup tag gets its own page so users can bookmark and link to specific syntax. The attribute tables and examples are self-contained.

2. **Guide vs Reference split** - Guides walk through workflows (create, edit, delete, templates). Reference pages are pure syntax documentation. This avoids the "wall of tables" problem in the current README.

3. **Admonitions for tips/warnings** - Replace the current `> blockquote` notes with Material admonitions (`!!! tip`, `!!! warning`, `!!! note`) for better visual distinction.

4. **Images stay in `/images`** - No need to move them; `mkdocs.yml` can reference them or we copy them to `docs/assets/` during build. Simplest approach: symlink or copy `images/` into `docs/assets/images/`.

5. **Dark/light toggle** - Material theme supports this out of the box; configure in `mkdocs.yml` palette.

---

## Out of Scope

- Deploying the docs site (GitHub Pages, Netlify, etc.) - can be added later
- Auto-generating reference from source code (the markup DSL is too custom for autodoc)
- Changelog / versioned docs
