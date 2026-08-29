---
number: "018"
title: "The Local Model Was Not Part of the Repository"
subtitle: "v3 moved planner data to files, taught Electron to run llamafile, and drew a hard line around multi-gigabyte binaries."
slug: "omni-018-the-local-model-was-not-part-of-the-repository"
project: "OmniPlanner"
date: 2026-07-04
status: "published"
summary: "OmniPlanner v3 replaced Electron's localStorage backend with per-key files, added lifecycle control for local llamafile servers, and exposed provider usage metrics — after an aborted model add left 5.8 GB of unreachable Git objects."
tags:
  - omniplanner
  - local-ai
  - electron
  - storage
  - llamafile
  - git
commits:
  - hash: "8e54c79c272ac92eb2fee7533b781d1d9ffd36bc"
    title: "chore: gitignore local LLM binaries, design assets, and archives"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/8e54c79c272ac92eb2fee7533b781d1d9ffd36bc"
  - hash: "a133c562dafbe6af1ee24cc53e0a030a684061da"
    title: "feat: file-system storage adapter and Electron shell upgrades (v3.0)"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/a133c562dafbe6af1ee24cc53e0a030a684061da"
  - hash: "a68997e526ad5cb17ca8218e0ab4df6a86c969f4"
    title: "feat: local AI presets, llamafile panel, and token usage tracking (v3.1)"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/a68997e526ad5cb17ca8218e0ab4df6a86c969f4"
---

OmniPlanner's local-first claim became literal on July 4.

Until v3, the Electron build still used Chromium localStorage for most planner state. Local AI meant entering an endpoint for software such as Ollama or LM Studio. The app did not own the lifecycle of a model server, and its storage abstraction still inherited the browser backend's practical size ceiling.

Three adjacent commits changed that boundary.

The first did not add a feature. It prevented local model files from becoming repository history.

The commit records that an aborted `git add` had already hashed 5.8 GB of model binaries into unreachable objects. The files were never committed, but Git's object database had still absorbed the cost until those orphaned objects were pruned.

There is no surviving direct development conversation for this sequence. The reconstruction comes from the commits, their messages, and the resulting implementation.

<div class="section-label">Local capability required repository hygiene first</div>

A self-contained llamafile can be convenient precisely because it packages model weights and a server executable together. It is also far too large to treat like ordinary source code.

The root `.gitignore` began excluding local design sources, archives, and Claude workspace state. The nested app ignore file added `models/` and archive patterns.

That separation defined the product distribution model:

- source code can describe and control a local model server;
- exported application icons can remain versioned;
- model executables and weights stay on the user's machine;
- the repository does not promise or distribute a particular model.

The distinction matters for size, licensing, security review, and updates. A user placing a binary under `models/` is adding a local runtime dependency, not modifying the source history.

The application therefore gained local-model support without becoming a model repository.

<div class="section-label">Planner state moved beyond the browser quota</div>

v3 introduced `ElectronFileStorageAdapter` behind the existing synchronous `StorageAdapter` interface.

At startup, the renderer requests all stored values through IPC. The adapter loads them into an in-memory map, so the rest of the React application can continue using synchronous `get`, `set`, `remove`, and `keys` calls. Each `omni_*` value is persisted as a separate JSON file under Electron's user-data directory with owner-only file permissions where supported.

This was a pragmatic compatibility design. Changing the entire application to await asynchronous disk reads would have touched every domain path. Hydrating once and then using a write-through cache preserved the existing interface while escaping localStorage's roughly five-megabyte class of limitation.

On an empty file store, the adapter attempted a one-time migration:

1. enumerate legacy localStorage keys beginning with `omni_`;
2. parse each value;
3. send it to the main process for file persistence;
4. copy it into the memory cache;
5. remove the legacy localStorage entry.

The architecture was stronger than the failure contract.

The main-process write handler returned `false` on a disk error instead of rejecting. The migration awaited that result but did not inspect it, then removed the localStorage source anyway. A failed write could therefore be treated as success and delete the only legacy copy.

Normal writes had a related split-brain risk. `set()` updated the memory cache immediately and launched the IPC write without waiting. A disk failure produced a warning, but the current session still read the new in-memory value. The UI could look saved until restart revealed that persistence had failed.

The file adapter was an important capacity upgrade, but it still needed acknowledged writes, atomic replacement, and migration verification before deletion to become a durable storage boundary.

<div class="section-label">Electron became a local-model supervisor</div>

The main process gained four IPC operations for local models: list, start, stop, and status.

Model discovery scanned the app's untracked `models/` directory for `.exe` and `.llamafile` files. Starting a selection spawned it as a server bound to `127.0.0.1`, defaulting to port 8080. Starting another model stopped the previous child, and app shutdown attempted to terminate the active process.

The AI settings screen exposed that lifecycle. Selecting the custom OpenAI-compatible provider revealed:

- presets for Ollama on port 11434;
- a preset for LM Studio on port 1234;
- discovered llamafile binaries;
- Start and Stop controls;
- automatic endpoint configuration to `http://localhost:8080/v1`.

This turned “local AI” from a text field into an operable desktop workflow. The user could place a runtime beside the app, start it from Settings, and route OmniPlanner's existing OpenAI-compatible provider to it.

The app did not download models, verify their origin, select a compatible prompt format, or guarantee acceleration. The UI note claimed the server would offload computation to the system GPU automatically, but the spawn command only requested server mode, host, and port. Actual GPU use depended on the llamafile build, hardware, and runtime detection.

There was also an IPC hardening gap. The main process joined renderer-provided model names and storage keys directly into filesystem paths. The normal UI supplied names obtained from the controlled directory listing and known `omni_*` keys, but the handlers themselves did not reject separators, parent traversal, or unexpected prefixes. A compromised renderer had more filesystem influence than the intended interface suggested.

Local execution reduced dependency on a remote provider. It did not remove the need to validate the local boundary.

<div class="section-label">“Optional AI” gained an operating cost panel</div>

v3.1 added a small `tokenLogger` service and capture hooks to Gemini, OpenAI, Anthropic, and OpenAI-compatible providers.

The settings screen could now show total calls, prompt tokens, output tokens, and estimated US-dollar cost. The counters were local and resettable. Custom and OpenRouter calls were assigned zero cost; the other providers used one fixed prompt and completion price per provider.

That made AI use visible without turning telemetry into a server feature. It also kept the wording honest: cost was estimated.

The prices were provider-wide constants rather than model- and date-specific tariffs. They could not represent cached tokens, tiered pricing, batch discounts, or a custom endpoint's electricity cost. The board was an orientation tool, not billing reconciliation.

The usage key also began as a raw string inside `tokenLogger` rather than part of the central storage-key registry. The following v4 work corrected that ownership.

<div class="section-label">v3 widened the local-first boundary and its blast radius</div>

Across the three commits, OmniPlanner gained a stronger local architecture:

- large planner state could live as files instead of browser storage;
- existing `omni_*` data had a migration path;
- local model runtimes stayed outside Git;
- Electron could supervise one local inference server;
- standard local servers had one-click endpoint presets;
- provider use became inspectable without remote telemetry;
- production Content Security Policy was tightened while development retained the exceptions it needed.

No dedicated test files changed with these storage and local-model commits. The most important risks were not pure calculation errors anyway. They were transition failures: disk writes that returned false, legacy values removed too early, child processes that might not terminate, unvalidated IPC path segments, and a UI promise about GPU behavior the launcher did not enforce.

The local-first direction was real. So was the new responsibility.

OmniPlanner was no longer merely storing browser-sized JSON and calling APIs. It was writing durable files, executing user-supplied binaries, owning a localhost process, and presenting estimates about external and local computation. v3 made the desktop shell more capable — and made its operating-system boundary part of the product.
