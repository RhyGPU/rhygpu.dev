---
number: "015"
title: "The License Named the Wrong Project"
subtitle: "Publication began with a history scan and ended with a one-minute correction."
slug: "omni-015-the-license-named-the-wrong-project"
project: "OmniPlanner"
date: 2026-04-29
status: "published"
summary: "Before public repository work, OmniPlanner's working tree and reachable history were scanned for common secret patterns, then AGPL-3.0-or-later was added — and a copied Mnemosyne notice was caught immediately after push."
tags:
  - omniplanner
  - open-source
  - agpl
  - security
  - git
  - release
commits:
  - hash: "0434ebd89848305abec43c9badace9b3746e0db3"
    title: "Add AGPL license"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/0434ebd89848305abec43c9badace9b3746e0db3"
  - hash: "2bc3be36adffdc8a490ba96b229fa438832eee61"
    title: "Correct OmniPlanner license notice"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/2bc3be36adffdc8a490ba96b229fa438832eee61"
---

The first request on April 29 was not simply “add a license.”

> Ensure sensitive information is removed, because the entire commit history will become visible. Also add a license for OmniPlanner.

This is the first OmniPlanner entry since February backed again by a surviving direct conversation. The sequence was publication work: inspect before exposing, distinguish secret-shaped code from real credentials, declare the legal terms in every relevant metadata surface, push, and verify what was actually published.

The final verification found that the new license still named Mnemosyne in its example notice.

The correction reached `master` one minute after the first commit.

<div class="section-label">The scan included history, not only the folder</div>

Checking the current files would not satisfy the request.

A removed `.env` file, private key, or hardcoded token can remain recoverable from Git history after it disappears from the working tree. The audit therefore searched the current checkout and reachable history for common credential patterns and committed secret-file names.

The scan found no credential-shaped values or committed environment and private-key files in the inspected history. It did find expected environment-variable names and password fields in application code.

Those are not secrets by themselves.

`GOOGLE_OAUTH_CLIENT_ID`, `API_KEY`, and a TypeScript field called `password` describe configuration and data flow. Treating every occurrence as a leaked credential would make the result noisy enough to hide a real value. The audit narrowed its judgment to values and files that resembled actual secrets.

OmniPlanner's nested README referenced `.env.local`, but that file was not committed and `*.local` was already ignored.

The result was evidence from a pattern-based audit, not a mathematical guarantee that no sensitive information could exist in any encoding or unreachable object. It was the appropriate gate before the requested public push.

<div class="section-label">The repository root had no license</div>

The application lived under `omniplan-ai---executive-life-os`, and the repository's documentation used a nonstandard root filename, `README.mdI`.

Initial content checks for common root files returned nothing because the layout did not match the expected paths. Inspecting the file tree revealed the nested app and confirmed that no root `LICENSE` existed.

The change was kept narrow:

- add the complete AGPL v3 text at repository root;
- declare `AGPL-3.0-or-later` in `package.json`;
- update the lockfile's root package metadata;
- add a short license section to the existing root documentation file;
- correct the package repository URL from `RhyGPU/Planner` to `RhyGPU/OmniPlanner`.

The last correction was adjacent to the license but important for the same reason: package metadata should point recipients to the source repository that carries the corresponding terms.

The `README.mdI` name remained unchanged, so the license note was not guaranteed to render as GitHub's conventional default README. The root `LICENSE` and package field still provided the canonical declaration.

<div class="section-label">`or-later` was an explicit choice</div>

OmniPlanner adopted `AGPL-3.0-or-later`, matching the licensing pattern already used by Mnemosyne.

That is not the same SPDX expression as `AGPL-3.0-only`.

The selected form permits use under GNU AGPL version 3 or a later version published under the license's upgrade terms. The conversation returned to this nuance after the push, and it was confirmed rather than left implied by the package string.

AGPL aligned with the product's open-source and no-server-dependency philosophy while preserving copyleft obligations if modified versions were offered through a network service.

The devlog records the choice and implementation; it does not replace the license text itself.

<div class="section-label">The copied notice survived the first push</div>

The first commit added the correct full AGPL text and correct package identifier.

Near the end of the license file, the recommended program notice still said:

> Mnemosyne — Copyright (C) 2026 Mnemosyne contributors

The license body had been reused from the other repository and its customized appendix had not been replaced.

The problem did not change which standard license text occupied the file. It did make OmniPlanner's own notice name another project.

Post-push verification caught it. The next commit changed the two lines to OmniPlanner and its contributors, then pushed again.

This was the same lesson as a code migration or backup preview: a successful write is not the end of the operation. Read the published result through the path users will receive.

<div class="section-label">Publication became a checked transition</div>

The April 29 sequence was small compared with the product phases before it:

1. identify the exact repository and default branch;
2. scan current files and reachable history for common secret patterns;
3. distinguish configuration references from actual values;
4. add root terms and package metadata;
5. validate the JSON and intended diff;
6. push to `master`;
7. read back the published result;
8. correct the copied project notice;
9. verify the final commit.

No product feature changed. The conditions under which the product could be shared did.

OmniPlanner had called itself free and open in its roadmap and README. On April 29, that statement acquired a root license, a machine-readable package identifier, and a repository URL recipients could follow.

It also acquired a useful footnote: even a standard legal file can carry project-specific residue. The final read mattered because the first push was valid enough to succeed and still wrong enough to fix.
