---
title: "rhygpu.dev"
slug: "rhygpu-dev"
featured: false
order: 99
subtitle: "The site you're reading — a systems lab, built in the open."
status: "Live"
summary: "The Astro portfolio and devlog engine behind rhygpu.dev: a personal systems lab that documents its own construction alongside the work it hosts."
repo: "https://github.com/RhyGPU/rhygpu.dev"
stack:
  - Astro
  - TypeScript
  - CSS
  - Markdown content
  - Cloudflare Pages
highlights:
  - Modeled projects and devlogs as typed content collections instead of hardcoded pages.
  - Built a per-project devlog engine where every project gets its own journal automatically.
  - Unified the whole site on one design system with shared nav, footer, and tokens.
  - Ships as a static build — no server, fast to load, cheap to host.
proofNotes:
  - The site is open source; the repo is linked in the footer as "Site Source".
  - Every project and devlog page is generated from Markdown, not hand-authored HTML.
  - This project has its own devlog, documenting how the site itself was built.
showHighlightsPanel: true
tags:
  - meta
  - astro
  - web
  - local-first
---

## Why the site is a project

A portfolio should demonstrate how someone builds, not just claim it.

So rhygpu.dev is not a static brochure bolted on top of the real work. It is a small system in its own right, with the same values as everything else in the lab: typed structure, inspectable content, and a build you can read end to end. The site documents its own construction the same way it documents Mnemosyne — in the open, in a devlog.

## Core Systems

<div class="case-grid">
  <article>
    <h3>Content Collections</h3>
    <p>Projects and devlogs are typed Markdown collections validated at build time, so a missing field is a build error, not a broken page in production.</p>
  </article>
  <article>
    <h3>Per-Project Devlog Engine</h3>
    <p>Every project automatically gets its own devlog homepage. A new entry only needs a project name in its frontmatter to flow into the right journal.</p>
  </article>
  <article>
    <h3>Shared Design System</h3>
    <p>One set of tokens, one sticky nav, one footer, applied across every page — so the whole site stays coherent instead of drifting page by page.</p>
  </article>
  <article>
    <h3>Static Build</h3>
    <p>The entire site is prerendered to static files. No server, fast loads, and a deploy that is cheap and hard to break.</p>
  </article>
</div>

## Current Status

rhygpu.dev is live and actively evolving.

It started as an imported homepage design and grew into the full lab: project pages, per-project devlogs, a shared design system, and this meta thread. The active work is the same as any project — filling in real screenshots, writing more devlogs, and tightening the parts that still read as placeholder.

## What This Demonstrates

<div class="proof-list">
  <span>Astro / static sites</span>
  <span>TypeScript</span>
  <span>Content modeling</span>
  <span>Design systems</span>
  <span>Documentation habits</span>
  <span>Shipping in the open</span>
</div>
