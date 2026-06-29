---
title: "OmniPlanner"
slug: "omniplanner"
featured: false
order: 2
subtitle: "Desktop-first planning workspace for goals, weeks, habits, calendar blocks, and AI-assisted organization."
status: "Active App"
summary: "An Electron desktop app for personal planning workflows, built around local data, weekly structure, goals, habits, and optional AI assistance."
repo: "https://github.com/RhyGPU/OmniPlanner"
stack:
  - Electron
  - Vite
  - Desktop app
  - Local data
  - Windows launcher
  - AI assistance
highlights:
  - Weekly planning workspace for goals, tasks, habits, and calendar blocks.
  - Desktop-first flow instead of a tab that competes for attention.
  - Local data model with optional AI assistance layered on top.
  - Windows launcher path for quick entry into the planning surface.
tags:
  - planning
  - productivity
  - local-first
  - desktop
---

## Problem

Planning tools often split real life across separate surfaces: calendar, goals, habits, notes, email, and weekly review. The result is not a plan. It is a pile of sync points.

OmniPlanner is aimed at the place where those pieces meet.

## Solution

The app is built as a desktop-first planning workspace. Weeks, goals, habits, calendar blocks, email-adjacent organization, and optional AI assistance belong in one local workflow instead of a collection of browser tabs.

The point is not to make an AI planner that invents a life for the user. The point is to give structure to the user's own planning loop.

## Technical Shape

OmniPlanner is framed as a local desktop workspace first. The important product choice is ownership of the planning surface: a dedicated app window, local data, and a fast path back into weekly planning instead of another web tab.

The system is organized around practical planning objects: goals, weeks, habits, calendar blocks, and optional AI assistance. AI belongs as an organizing layer, not as the source of truth.

## Current Status

OmniPlanner is a serious secondary project in active development. The honest target is a useful local desktop planner before any broader platform story.

## What This Demonstrates

- Desktop app development with Electron and Vite.
- Local data workflow design.
- Personal productivity systems thinking.
- Practical UX judgment around planning, review, and re-entry.
- AI assistance scoped as support for user-owned organization.
