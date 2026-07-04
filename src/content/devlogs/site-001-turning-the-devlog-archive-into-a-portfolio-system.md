---
number: "site-001"
title: "Turning the Devlog Archive into a Portfolio System"
subtitle: "From one project journal to a layered portfolio for projects, proof, and build history."
slug: "site-001-turning-the-devlog-archive-into-a-portfolio-system"
project: "rhygpu.dev"
date: 2026-07-04
status: "published"
summary: "How rhygpu.dev moved from a Mnemosyne-heavy devlog archive into a portfolio system with project pages, proof media, profile pages, and cleaner reader paths."
tags:
  - rhygpu.dev
  - portfolio
  - devlog
  - astro
  - information-architecture
commits: []
---

rhygpu.dev started with a gravitational problem.

The site had depth, but almost all of that depth pointed toward Mnemosyne. That made sense at the time. Mnemosyne had the most written history, the clearest technical struggle, and the most interesting failures to document. It was the project that taught the site what a devlog could be.

But depth is not the same thing as a front door.

A reader landing on the site should not have to reconstruct the value of the work from raw logs, old build notes, and a chain of journal entries. That is asking them to become an archaeologist before they even know what they are looking at.

<div class="section-label">The starting point</div>

The first real version of rhygpu.dev read mostly like a Mnemosyne archive.

That was useful. It preserved a trail of decisions: why memory split into subjective and objective layers, why payload inspection mattered, why bad generations needed repair paths instead of hand-waving. It gave the work a spine.

It was also too narrow.

There were other projects with different kinds of proof. OmniPlanner had desktop UI surfaces. Pythagorean Harmony had a gameplay-system idea that needed honest prototype framing. The site itself had become a build artifact with its own architecture. None of that fit cleanly inside a Mnemosyne-heavy journal.

The archive had become real enough that it needed a better shape around it.

<div class="section-label">The problem</div>

GitHub repos alone do not explain intent.

They can prove that code exists, but they do not explain why a system was shaped a certain way, what tradeoffs were made, or what part of the project is actually worth inspecting first.

Devlogs have the opposite problem. They preserve time. They show the work in sequence. That is valuable, but it is dense. A devlog is a trail, not a map.

Raw chat logs are even deeper source material. They are useful for provenance, reconstruction, and future writing, but they are not the first reader path. They contain too much context and not enough direction.

The site needed layers:

- A homepage for orientation.
- Project pages for case studies.
- A devlog archive for build history.
- About, Resume, and Contact pages for the human/profile layer.
- Raw archive material for source context.

Not one pile. A path.

<div class="section-label">What changed</div>

The homepage became a portfolio hub instead of a single-project wrapper.

The `/projects/` route became the public project index: Mnemosyne first as the flagship, OmniPlanner as a desktop planning app with real UI proof, Pythagorean Harmony as a playable prototype, and rhygpu.dev as a meta-project instead of an accidental container.

Each project page now has a case-study shape: summary, status, stack, architecture notes, media, proof notes, and links. The point is not to make every project look equally finished. The point is to make each one legible at its actual maturity.

Mnemosyne and OmniPlanner use real screenshots because those screenshots exist.

Pythagorean Harmony does not pretend. It uses the combat-loop system diagram and a private-source note instead of fake gameplay screenshots or a public repo link that does not exist.

rhygpu.dev uses real site screenshots for the homepage and devlog archive, with planned slots left visible where the remaining captures still need to be made.

The CTAs also stopped being hardcoded. Repository links appear only when `repo` exists. Devlog links appear only when `devlog` exists. `devlogLabel` controls the text, which lets rhygpu.dev say "Site journal" without making every project use the same label.

That is a small implementation detail with a large honesty payoff. The page no longer implies links that are not real.

<div class="section-label">The rule</div>

> A portfolio is not a dump. It is a guided path through proof.

That became the organizing principle.

Project pages are the front door. They tell the reader what the thing is, why it exists, what is real, what is planned, and where the evidence lives.

Devlogs are build history. They preserve the sequence: mistakes, decisions, reversals, fixes, and the slow shape of a system becoming clearer.

Raw logs are archive/source material. They are allowed to be messy because they are not pretending to be the polished public surface.

GitHub repos are implementation proof. They matter most when the source is public and ready to inspect.

Screenshots and diagrams are evidence, not decoration. They should prove something: a working surface, a current UI, a system shape, or a deliberate absence.

<div class="section-label">What this unlocked</div>

Mnemosyne now reads like the flagship instead of just the project with the most words around it.

OmniPlanner can stand on its own because the page shows actual app surfaces: dashboard, reminders, inbox, calendar, deep planning, vision, and settings/data.

Pythagorean Harmony gets to be honest. It is a prototype with a specific combat-loop experiment, not a fake finished RPG.

rhygpu.dev is now part of the portfolio instead of only the container holding the portfolio. That matters because the site has its own architecture: content collections, route generation, media/proof modeling, metadata-driven CTAs, and an archive layer.

The meta-project became visible.

<div class="section-label">Still unfinished</div>

This is baseline polish, not the final form.

The site needs more site-specific devlogs as the portfolio system changes. Future project work should get project-specific devlogs instead of everything flowing through Mnemosyne by default. Screenshots should be added when the underlying projects mature enough to capture honestly.

There is also room for branding polish: social preview images, favicon/app icons, and a cleaner shared-card story for links. That polish matters, but only after the proof model is real.

The important part is that the reader path exists now.

The archive is still there. The logs still matter. But the first question is no longer "can you reconstruct what happened?"

The first question is simpler:

What is this project, what proof exists, and where should I go next?
