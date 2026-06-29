---
title: "Mnemosyne"
slug: "mnemosyne"
featured: true
order: 1
subtitle: "Local-first memory architecture for persistent AI characters."
status: "active alpha"
summary: "A desktop AI narrative engine that separates character memory, world state, prompt context, and debugging traces so LLM-driven characters can change without losing continuity."
repo: "https://github.com/RhyGPU/mnemosyne"
devlog: "/devlog/"
stack:
  - React
  - Tauri
  - Rust
  - SQLite
  - LLM orchestration
highlights:
  - Soul memory separated from world continuity.
  - Context Compiler for clean recent chat plus structured state.
  - Hidden state and patch protocol for traceable story changes.
  - Payload inspector, regenerate/fix flows, and fresh scenario reset.
  - State Map roadmap for player, reader, GM, and dev visibility.
tags:
  - local-first
  - AI roleplay
  - memory systems
  - state engine
---

## Problem

AI roleplay breaks when the model has to remember everything as prose. Raw chat gets bloated, summaries flatten the scene, and hidden continuity can leak into narration or disappear between turns.

Mnemosyne treats the problem as architecture, not prompt decoration.

## Solution

The core rule is simple:

> The narrator writes. The state map remembers.

The app separates character memory, world state, recent chat, prompt context, and debugging traces. The model gets the parts it needs to write the next scene, while the engine keeps track of what changed, why it changed, and whether the change can be regenerated, corrected, restored, or branched.

## Current Status

Mnemosyne is an active alpha. The focus is still on correctness before polish: Soul memory, World Log behavior, context compilation, patch protocol reliability, inspector tooling, reset boundaries, and the State Map visibility model.
