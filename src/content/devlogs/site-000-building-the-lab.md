---
number: "000"
title: "Building the Lab"
subtitle: "Turning an imported homepage design into the whole site."
slug: "site-000-building-the-lab"
project: "rhygpu.dev"
date: 2026-07-01
status: "published"
summary: "How rhygpu.dev went from a single imported homepage mockup to a full site: one design system, typed content, and a devlog engine that documents itself."
tags:
  - meta
  - astro
  - design-system
  - devlog-engine
commits: []
---

This is the site writing about itself, which is either the most honest thing a portfolio can do or the most self-indulgent. I am going to say honest.

rhygpu.dev started as a single homepage mockup — one imported design file, a nice hero, and nothing behind it. Everything after that was the same problem I keep circling back to in every project: take something that looks finished and give it real structure.

<div class="section-label">The import</div>

The first version was one page. A dark hero, a flagship card, a devlog list — all hardcoded, all pretend. The devlog entries were fake strings in a template. The screenshots were grey placeholder boxes.

It looked done. It was not done.

A homepage that lies about having content is worse than an empty one, because it invites you to click things that go nowhere.

<div class="section-label">One system, not one page</div>

The real work was making the rest of the site match, and doing it once instead of per page.

So the design moved into shared bones: a single set of tokens, one sticky nav, one footer, applied from the layout down. Every page — projects, devlogs, about, resume, contact — now inherits the same look instead of each carrying its own copy that slowly drifts out of sync.

> The homepage stopped being a special case. It became the first page of a system.

<div class="section-label">Content that can't quietly break</div>

Projects and devlogs are not hand-written HTML. They are typed Markdown collections, validated at build time.

That sounds like bureaucracy until the first time a missing field turns into a build error instead of a blank space in production. The structure is the point. A project is data. A devlog is data. The pages are just a view over that data.

<div class="section-label">A devlog engine that documents itself</div>

The part I actually like: every project gets its own devlog homepage, automatically.

A new entry only needs a project name in its frontmatter, and it flows into the right journal. Projects with no entries yet still get a page, with an honest "no devlogs yet" state instead of a dead link. Which is exactly why this entry can exist at all —

> rhygpu.dev is a project. So rhygpu.dev gets a devlog.

The site is built the same way it documents everything else in the lab: in the open, with the machinery visible. This is entry 000. There will be more when there is more worth writing down.
