# RhyGPU Astro Migration Roadmap

## Goal

Turn `rhygpu.dev` from a hand-edited HTML archive into a Git-based static publishing system.

The long-term target is simple:

- write devlogs as Markdown
- keep one shared layout
- generate homepage, archive, previous/next links, related posts, tags, SEO, and RSS automatically
- stop manually editing every article page and `index.html`

The existing static HTML site must remain live until the Astro build is ready and Cloudflare Pages settings are intentionally changed.

---

## Current problem

The current site works, but every new post requires manual work:

- create a new `devlog-00X.html`
- copy layout structure
- apply `style.css` manually
- update homepage manually
- write previous/next links manually
- keep commit lists consistent manually

This is manageable at 7 posts. It will not scale to 30+ posts.

---

## Target architecture

```txt
rhygpu.dev/
  public/
    images/

  src/
    content/
      devlogs/
        000-before-the-repository.md
        001-soul-update-packet.md
        ...
      projects/
        mnemosyne.md
        omniplanner.md

    components/
      Header.astro
      Footer.astro
      PostCard.astro
      PostNav.astro
      RelatedPosts.astro
      CommitList.astro
      TagList.astro

    layouts/
      BaseLayout.astro
      BlogPostLayout.astro
      ProjectLayout.astro

    pages/
      index.astro
      devlog/
        index.astro
        [slug].astro
      projects/
        [slug].astro
      tags/
        [tag].astro
      rss.xml.ts
      sitemap.xml.ts

    styles/
      global.css

  package.json
  astro.config.mjs
```

---

## Content model

Each devlog becomes Markdown with frontmatter:

```yaml
---
number: "006"
title: "Opening the Black Box"
subtitle: "LLM Payload Inspector, Latest Exchange, and the tail excerpt bug."
slug: "006-opening-the-black-box"
project: "mnemosyne"
date: 2026-05-29
status: "published"
summary: "The moment I stopped guessing and started inspecting the exact payload sent to the model."
tags:
  - mnemosyne
  - context
  - payload
  - debugging
  - continuity
commits:
  - hash: "7985475"
    title: "Clean up LLM payload context and latest exchange"
    repo: "RhyGPU/mnemosyne"
    url: "https://github.com/RhyGPU/mnemosyne/commit/7985475596fcbcb1f7f2e22dbb7e809539745113"
---

Article body here.
```

---

## Phase 1, Scaffold without breaking live site

Status: in progress.

Add Astro project files beside the current HTML site:

- `package.json`
- `astro.config.mjs`
- `tsconfig.json`
- `src/content/config.ts`
- base layout
- blog layout
- initial components
- archive routes
- global CSS

Do not delete existing HTML yet.
Do not change Cloudflare build settings yet.

The existing static site remains the production source until the Markdown conversion is complete.

---

## Phase 2, Convert current devlogs to Markdown

Convert:

- `devlog-000.html`
- `devlog-001.html`
- `devlog-002.html`
- `devlog-003.html`
- `devlog-004.html`
- `devlog-005.html`
- `devlog-006.html`

into:

- `src/content/devlogs/000-before-the-repository.md`
- `src/content/devlogs/001-turning-the-code-block-into-a-soul-update.md`
- `src/content/devlogs/002-splitting-memory-in-two.md`
- `src/content/devlogs/003-hiding-the-machine.md`
- `src/content/devlogs/004-feeding-the-model-a-session-packet.md`
- `src/content/devlogs/005-keeping-the-scene-from-replaying.md`
- `src/content/devlogs/006-opening-the-black-box.md`

Keep HTML versions until Astro output matches the current live site.

---

## Phase 3, Auto navigation

Implement automatic:

- homepage latest posts
- `/devlog/` archive
- individual `/devlog/[slug]` pages
- previous/next links by series order
- related posts by project and tags
- commit list rendering from frontmatter

No more manual homepage edits for every post.

---

## Phase 4, Project and tag pages

Add:

- `/projects/mnemosyne/`
- `/projects/omniplanner/`
- `/tags/[tag]/`

Each project page should show:

- project summary
- status
- repo links
- devlog timeline
- related technical notes

---

## Phase 5, SEO and feed

Add:

- metadata per page
- Open Graph tags
- RSS feed
- sitemap
- canonical URLs

This makes `rhygpu.dev` behave like a real technical archive, not a folder of pages.

---

## Phase 6, Cloudflare cutover

Only after the Astro build reproduces the current site:

Cloudflare Pages settings:

```txt
Framework preset: Astro
Build command: npm run build
Build output directory: dist
```

After cutover:

- keep legacy HTML temporarily for redirects or fallback
- verify `rhygpu.dev`
- verify all old devlog links
- verify mobile layout
- verify SEO metadata

---

## Rule

Do not overbuild before the content migration works.

The first win is this:

```txt
New devlog = one Markdown file.
Homepage, previous/next, related posts, and commit list update automatically.
```
