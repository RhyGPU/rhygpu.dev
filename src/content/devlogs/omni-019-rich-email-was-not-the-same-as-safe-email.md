---
number: "019"
title: "Rich Email Was Not the Same as Safe Email"
subtitle: "MIME parsing restored the message people sent; an empty iframe sandbox contained it without sanitizing it."
slug: "omni-019-rich-email-was-not-the-same-as-safe-email"
project: "OmniPlanner"
date: 2026-07-04
status: "published"
summary: "OmniPlanner's inbox moved from plain IMAP body extraction to mailparser-backed text and HTML parts, then rendered rich messages inside a sandboxed srcDoc iframe with an explicit plaintext fallback — while leaving remote-content and sanitization policy unfinished."
tags:
  - omniplanner
  - email
  - imap
  - mime
  - security
  - electron
commits:
  - hash: "a133c562dafbe6af1ee24cc53e0a030a684061da"
    title: "feat: file-system storage adapter and Electron shell upgrades (v3.0)"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/a133c562dafbe6af1ee24cc53e0a030a684061da"
  - hash: "e96edf8ad2d608d0bd87147abf05e0dc840ab2ae"
    title: "feat: MIME email parsing with sandboxed rich HTML view (v3.0)"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/e96edf8ad2d608d0bd87147abf05e0dc840ab2ae"
---

OmniPlanner's first email integration made messages actionable before it made them readable.

The early inbox could fetch IMAP metadata, retrieve a body, extract a date and time with AI, and convert the result into the same calendar model as an imported ICS event. But email is not normally a single block of plain text. Real messages are MIME trees: alternative text and HTML bodies, encoded content, inline assets, attachments, and provider-specific structure.

On July 4, the inbox began preserving both human-readable forms.

The implementation arrived across two commits only 27 seconds apart. `mailparser` and main-process MIME extraction were included in the broader filesystem-storage commit. The next commit added the renderer type, rich-message UI, and plaintext fallback, then described the whole feature under one email-specific title.

There is no surviving direct conversation for this change. The commit split is part of the evidence.

<div class="section-label">The main process stopped pretending MIME was text</div>

When a user opened a message, Electron already fetched the full source by IMAP UID in the main process. v3 passed that source to `mailparser.simpleParser()`.

The result exposed two separate values:

- `parsed.text` became the normal `body`;
- `parsed.html` became `htmlBody` when the message supplied an HTML part.

That parsing location was appropriate. IMAP credentials and the raw message remained on the Electron side of the preload boundary, while the renderer received only the body representations it needed.

The platform `EmailService` contract then gained optional `htmlBody`. That type correction mattered because the Electron adapter was already forwarding the main-process result. Without the shared field, the UI's use of rich content produced `TS2339` even though the runtime object contained the value.

Selecting a message stored both representations on the existing `Email` record. Opening another message reset the preferred view to HTML, but the UI displayed the toggle only when rich content existed.

Plain messages stayed plain. Multipart messages became switchable.

<div class="section-label">The renderer used containment, not trust</div>

Injecting email markup into the React document would have handed an untrusted message the same DOM as the planner.

Instead, OmniPlanner constructed a small `srcDoc` document inside an iframe. It supplied a neutral font and color baseline, constrained images to the frame width, and set the iframe's `sandbox` attribute to an empty value.

An empty sandbox applies the restrictions without granting exceptions such as `allow-scripts`, `allow-forms`, `allow-popups`, or `allow-same-origin`. That substantially reduces what embedded message markup can do to the application. The iframe also received its own layout boundary and a descriptive title.

The user retained an immediate escape hatch: switch from HTML to Text and read the parser's plain representation instead.

That was a better default than rendering arbitrary markup directly or forcing every message through a degraded text view.

<div class="section-label">“Sandboxed” did not mean “sanitized”</div>

The shared type comment called `htmlBody` “sanitized-for-iframe.” The implementation did not actually sanitize the HTML.

`mailparser` parses MIME structure; it does not turn hostile or privacy-invasive markup into trusted content. The application placed `parsed.html` directly inside the `srcDoc` body.

The empty iframe sandbox blocks major active capabilities, but it is not a content policy by itself. The commit did not visibly:

- remove remote image URLs or tracking pixels;
- strip remote CSS resources;
- rewrite or warn on links;
- sanitize misleading forms and visual phishing content before display;
- provide a “load remote content” consent step;
- record dedicated tests for hostile HTML fixtures.

Whether a particular remote resource can load may also depend on Electron's Content Security Policy and frame behavior. The email feature should not rely on that incidental interaction as its privacy control. A deliberate remote-content policy belongs next to MIME rendering.

The safest description of the July implementation is therefore precise: untrusted rich email was isolated in a restricted iframe, not converted into trusted HTML.

<div class="section-label">Credential honesty improved at the same boundary</div>

The email settings screen also gained a warning when the platform credential service was unavailable:

> Running in Web Sandbox — passwords will be saved in plaintext browser storage. Use the desktop app for secure hardware encryption.

The first half corrected an important UX problem. A web fallback that accepts an IMAP password should not visually resemble the Electron path backed by `safeStorage`.

The phrase “secure hardware encryption” was stronger than the implementation proved. Electron `safeStorage` delegates to the operating system's available cryptographic storage; hardware backing varies by platform and configuration. “OS-protected encryption” would have been the more defensible promise.

The warning still established the right product distinction: the platform can change the security properties of the same-looking settings form.

<div class="section-label">Readable email expanded the stored-data surface</div>

Rich bodies were attached to the same email records that the app persisted. That made subsequent viewing fast, but it also meant local planner storage could now contain substantially larger and more complex message content.

This change arrived beside the new file-backed Electron adapter for a reason. MIME bodies, especially HTML, make the browser-storage ceiling more relevant. Moving Electron state to JSON files gave the inbox more room, although it did not address attachment retention or per-message cache limits.

The commit changed three renderer-facing files — 73 insertions and six deletions — and did not add a test file. The parser dependency and main-process extraction had entered one commit earlier.

Functionally, the result completed an important email loop:

1. fetch the exact message source by UID;
2. parse its MIME alternatives in the trusted main process;
3. return both text and HTML through a typed platform service;
4. isolate HTML from the planner document;
5. let the user choose the plain representation;
6. retain the body for planning and extraction workflows.

OmniPlanner no longer reduced every email to a text approximation. It also did not declare email HTML safe merely because it looked correct.

The next hardening step was clear: preserve the fidelity gained from MIME while explicitly controlling the remote content and deceptive markup fidelity can carry with it.
