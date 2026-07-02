---
title: "rhygpu.dev"
slug: "rhygpu-dev"
featured: false
order: 4
subtitle: "Portfolio system and development archive for RhyGPU projects."
status: "Active Site"
summary: "The Astro portfolio, devlog hub, and meta-build archive for RhyGPU projects: a public layer that turns raw project history into readable case studies."
repo: "https://github.com/RhyGPU/rhygpu.dev"
devlog: "/projects/rhygpu-dev/devlog/"
devlogLabel: "Site journal"
stack:
  - Astro
  - TypeScript
  - Markdown content collections
  - Static site generation
  - Static deploy
  - CSS
highlights:
  - Modeled projects and devlogs as content collections instead of hardcoded one-off pages.
  - Built a portfolio path from summary cards to case studies, devlogs, proof media, and archive material.
  - Added project media/proof sections so screenshots and system diagrams can support claims without fake polish.
  - Preserved raw build and chat history as source material while keeping the public reader path curated.
  - Hardened the repo by removing generated/vendor artifacts from version control.
architecture:
  - Markdown content
  - Astro content collections
  - Project/devlog route generation
  - Shared layouts/components
  - Static build
  - Public portfolio
media:
  - title: Homepage portfolio hub
    type: screenshot
    src: /projects/rhygpu-dev/homepage-portfolio-hub.png
    alt: rhygpu.dev homepage showing the portfolio hero, featured projects, latest devlogs, and shared navigation.
    caption: Portfolio landing page organizing projects, devlogs, and profile navigation into one reader path.
    status: available
  - title: Projects index
    type: placeholder
    caption: Planned screenshot slot for the project collection view showing flagship, secondary app, prototype, and meta-site structure.
    status: planned
  - title: Mnemosyne case study
    type: placeholder
    caption: Planned screenshot slot for the flagship case-study page combining architecture, proof media, devlog links, and roadmap.
    status: planned
  - title: Devlog archive
    type: screenshot
    src: /projects/rhygpu-dev/devlog-archive.png
    alt: rhygpu.dev devlog archive showing project filters and chronological development journal entries.
    caption: Development journal archive for project history and technical decision records.
    status: available
  - title: rhygpu.dev project page
    type: placeholder
    caption: Planned screenshot slot for the meta-project page documenting the portfolio system itself as a build artifact.
    status: planned
proofNotes:
  - Mnemosyne, OmniPlanner, and Pythagorean Harmony are represented as project pages.
  - Mnemosyne devlogs 000-010 exist in the shared development journal.
  - Real screenshots are used where available, including Mnemosyne and OmniPlanner.
  - Raw chat and build logs are retained as archive/source material, not treated as the primary reader path.
showHighlightsPanel: false
tags:
  - meta
  - portfolio
  - astro
  - devlog
  - archive
---

## Problem

A GitHub repo alone does not explain project intent.

Source code can show what exists, but it rarely explains why the project exists, what changed over time, which tradeoffs mattered, or what is still unfinished. Raw chat logs and dense devlogs have the opposite problem: they preserve too much texture for a first impression.

A useful portfolio needs layered access. Someone should be able to scan a project summary, open a case study, inspect real proof media, follow the devlog if they want the history, and only then reach for raw/archive material when provenance matters.

That is the job of `rhygpu.dev`: make the path from messy build history to public project narrative readable without sanding off the engineering reality.

## Solution

`rhygpu.dev` organizes RhyGPU work into a public system:

- A portfolio homepage for the current project set.
- Project pages for technical case studies.
- A shared devlog archive for project history.
- Proof/media sections for screenshots, diagrams, and honest planned slots.
- About, Resume, and Contact pages for the human/profile layer.
- Tracked build/archive logs where they are useful as source material.

The site-building notes and project devlogs live in the shared development journal. Raw chat/build logs are archive material, not the main route a reader is expected to take.

## Core Systems

<div class="case-grid">
  <article>
    <h3>Project Collection</h3>
    <p>Projects are modeled as Markdown content entries with status, stack, proof notes, media, architecture, and long-form body content.</p>
  </article>
  <article>
    <h3>Devlog Collection</h3>
    <p>Development entries are structured content, so the archive, project links, metadata, and individual pages stay generated from one source.</p>
  </article>
  <article>
    <h3>Case-Study Pages</h3>
    <p>Each project gets a reusable page shell for problem, solution, systems, proof, current status, and skills demonstrated.</p>
  </article>
  <article>
    <h3>Proof / Media Layer</h3>
    <p>Project pages can show real screenshots, diagrams, demo links, and planned slots without pretending unfinished assets already exist.</p>
  </article>
  <article>
    <h3>Metadata / SEO Layer</h3>
    <p>Shared layout metadata handles titles, descriptions, canonical URLs, Open Graph, and Twitter summary tags.</p>
  </article>
  <article>
    <h3>Build / Archive Logs</h3>
    <p>Raw site-building material can be retained as archive/source evidence while the public surface stays curated and readable.</p>
  </article>
  <article>
    <h3>Static Generation</h3>
    <p>The site builds into static pages, keeping hosting simple and making route generation easy to validate before deploy.</p>
  </article>
</div>

## Architecture / System Shape

The site is intentionally small and inspectable:

Markdown content becomes typed Astro collections, collections generate project and devlog routes, shared components provide the frame, and the static build becomes the public portfolio.

## Current Status

`rhygpu.dev` is an active portfolio site.

The homepage, project index, individual project pages, devlog archive, About, Resume, and Contact pages exist. Mnemosyne, OmniPlanner, and Pythagorean Harmony now have distinct public surfaces, and this page makes the site itself visible as the fourth meta-project.

The meta-build archive exists, but it should remain behind the scenes unless a future page intentionally explains it. The next cleanup pass should focus on site-specific devlogs, stronger live deployment QA, and replacing planned site screenshots with real captures once the layout stabilizes.

## What This Demonstrates

<div class="proof-list">
  <span>Portfolio information architecture</span>
  <span>Astro / static site development</span>
  <span>Content modeling</span>
  <span>Technical writing</span>
  <span>Project framing</span>
  <span>Source-to-public narrative transformation</span>
  <span>Build / repo hygiene</span>
</div>
