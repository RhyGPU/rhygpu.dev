---
number: "011"
title: "The Planner Outgrew Electron"
subtitle: "A platform boundary made web and mobile possible without moving the domain."
slug: "omni-011-the-planner-outgrew-electron"
project: "OmniPlanner"
date: 2026-03-20
status: "published"
summary: "OmniPlanner moved Electron calls behind platform services, then reused the core in an IndexedDB PWA and Capacitor shell with native credentials, local reminders, storage health, and honest mobile UX."
tags:
  - omniplanner
  - architecture
  - pwa
  - capacitor
  - offline-first
  - mobile
commits:
  - hash: "c73801b009cb5b36505bce1e69ca6355855782dd"
    title: "Create the cross-device platform service boundary"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/c73801b009cb5b36505bce1e69ca6355855782dd"
  - hash: "1fa788543490007fcead49f3e25c252fa8d0d9ae"
    title: "Add the local-first PWA shell"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/1fa788543490007fcead49f3e25c252fa8d0d9ae"
  - hash: "20c5d2c1bc1f8ca70fb807123bb34c4a4bb8cca0"
    title: "Add the Capacitor mobile shell and notification service"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/20c5d2c1bc1f8ca70fb807123bb34c4a4bb8cca0"
  - hash: "890faaea5ab9cd260338052dff584d45986c161c"
    title: "Add native secure storage and wire reminders"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/890faaea5ab9cd260338052dff584d45986c161c"
  - hash: "301a9d476c393c38691ff5440dcaf02580191d82"
    title: "Add storage health and conflict-free restore"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/301a9d476c393c38691ff5440dcaf02580191d82"
  - hash: "96ceb4d41788c0157aa7809a44ab41d4b37da495"
    title: "Polish mobile interaction and local-first copy"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/96ceb4d41788c0157aa7809a44ab41d4b37da495"
---

OmniPlanner's domain was portable before its code was.

Goals, weeks, habits, planning selectors, backups, and calendar parsing did not fundamentally require Electron. The UI still called `window.electronAPI` directly for credentials, email, networking, links, and quitting. A browser or mobile shell could reuse the files only by imitating an undeclared desktop object.

On March 20, the project introduced an explicit platform boundary. Within the next four hours, the same core ran behind an IndexedDB PWA and a Capacitor mobile adapter, gained local reminders and native credential storage, reported storage degradation, validated restores before writing, and repaired its smallest mobile controls.

The speed came from the order. Web and mobile did not begin with separate copies of the planner. They began by removing the desktop shell from the planner's vocabulary.

This article reconstructs Phases 8–13 from six commits. It describes a foundation, not proof that every generated native project or offline edge had already been tested on every device.

<div class="section-label">Components stopped asking for Electron</div>

The platform layer defined four initial services:

- credentials;
- email;
- network;
- shell operations.

Electron adapters wrapped the existing preload bridge. Web adapters used browser fetch and window opening where possible, and returned unavailable or safe no-op results for desktop-only credentials, IMAP, and quit behavior.

A factory selected one `PlatformServices` object at runtime. Components called that object instead of checking for `window.electronAPI` themselves.

The distinction was more than naming. An email settings component could now ask whether email was available and display a truthful message. It no longer needed to know that Electron implemented the answer with IPC and `imapflow`.

A `core/index.ts` barrel documented the portable surface: types, goal and week managers, planning intelligence, milestones, ICS parsing, storage, and backup logic. Platform shells received an explicit import boundary instead of an informal promise that some files probably worked elsewhere.

<div class="section-label">The web shell changed the storage backend</div>

Electron kept the synchronous local-storage adapter. The web shell initialized IndexedDB.

The IndexedDB adapter loaded durable values into an in-memory map, then satisfied the existing synchronous storage interface from that cache. Writes updated the cache immediately and opened write-through IndexedDB transactions in the background.

That preserved the application's synchronous domain code while gaining a larger browser persistence backend.

On a first web run, existing `omni_*` local-storage keys moved into IndexedDB. The delegate behind the storage proxy changed only after asynchronous initialization, so the rest of the application continued using the same `storage.get` and `storage.set` calls.

Startup became a guarded sequence:

1. initialize the platform storage;
2. run schema migrations;
3. register the service worker on web;
4. render even if an earlier step failed.

The white-screen lesson from goal migration had become startup policy.

<div class="section-label">The first PWA was a minimum offline shell</div>

The web build gained a manifest, install metadata, placeholder icons, and a service worker.

The worker used network-first requests with cache fallback for same-origin GETs. It pre-cached the HTML shell, manifest, and favicon. Cross-origin AI requests were not intercepted.

This made revisited assets available offline after they had been cached. It was not yet a complete precache manifest for every hashed application asset, nor did it make external AI or email work without a network. “Offline-first” applied to the core planner and locally persisted data, not to every integration.

That boundary was consistent with the product thesis: the planner had to work without a server; optional services could degrade.

<div class="section-label">Capacitor became the third adapter</div>

The next phase added Capacitor as a thin native shell around the same built web assets.

Platform selection became Electron, Capacitor, or web. Capacitor supplied credentials, local notifications, and browser-style shell behavior. Email remained unavailable and network behavior delegated to the web adapter.

The first credential implementation used Capacitor Preferences and documented that it was app-sandboxed storage, not hardware-backed secret storage.

One hour later, that transitional path was replaced by a secure-storage plugin using the iOS Keychain or Android Keystore where supported. An idempotent migration moved API and email credential keys out of Preferences and removed the old entries.

The quick replacement is important. Cross-platform abstraction can make an insecure implementation look interchangeable with a secure one because both satisfy `CredentialService`. The interface guarantees shape, not security strength. The platform adapter and UI still have to communicate the actual capability.

<div class="section-label">Notifications existed differently on every platform</div>

The platform aggregate gained a notification service.

Capacitor used native local notifications. Web used the Notifications API plus in-page timers and therefore worked only while the browser context remained alive. Electron initially used a null adapter — the desktop app did not yet implement desktop notifications despite being the oldest shell.

Settings kept the master switch off by default and required permission. Three reminder tracks were derived from current planner data:

- a daily planner reminder;
- a habit reminder only when active habits existed;
- a reminder before the nearest upcoming focus block today.

Stable notification IDs made rescheduling idempotent. Changes to settings, today's focus events, or active habits triggered a targeted synchronization.

The UI described platform limitations instead of presenting every toggle as equally capable. This prevented an interface-level repeat of the old “Real-Time Sync” label: a visible control was not allowed to imply a service the current shell did not provide.

<div class="section-label">Write-through needed a failure signal</div>

The IndexedDB cache made synchronous reads convenient. Its background writes introduced a new failure mode: the session could appear updated while durable storage rejected the transaction.

Phase 12 added storage health state. IndexedDB quota errors and initialization failures marked the backend degraded. The application displayed an amber banner with an immediate backup export action.

This did not make a failed write durable. It made the failure visible while the in-memory state was still available to save.

That is a crucial local-first property. If the browser cannot persist, the app must not continue displaying a calm success state until the tab closes and the data vanishes.

<div class="section-label">Restore became one validated transition</div>

Backup restore had accumulated normalization and UI state updates over earlier versions.

The new validator inspected the backup before any write. Fatal structural errors rejected it. Advisory issues — such as suspicious but recoverable content — returned warnings.

On success, import wrote the normalized data once. The UI showed restore status, waited briefly, and reloaded the application so every state atom came from the same freshly imported storage.

The previous path could write in more than one place and leave React holding a mixture of old and restored objects. Reloading was less elegant than a transactional in-memory replacement and more reliable than pretending every component could be synchronized manually.

The flow became:

> validate → write once → report warnings → restart from the new truth

<div class="section-label">Mobile exposed hover assumptions</div>

The final commit in the sequence did not add another platform service. It audited the existing UI with fingers instead of a mouse.

Habit buttons grew from 20 to 36 pixels on mobile. Goal-link controls stopped depending on hover opacity. Tab controls reached a 48-pixel height. Event start and duration fields stacked vertically inside the narrow modal. Reminder settings reduced wasted padding and stopped overflowing.

The sidebar copy changed from **Real-time Sync Active** with a pulsing dot to **Local — no server sync**.

That line summarized the architectural work better than a platform badge could. IndexedDB, Electron storage, and mobile secure storage did not create a shared cloud account. They created local persistence behind three shells.

Calling that real-time sync would have converted internal state propagation into a false external promise.

<div class="section-label">One planner, unequal capabilities</div>

By the end of Phase 13, OmniPlanner could express the same core on desktop, web, and mobile without claiming that the shells were identical.

Electron had IMAP and encrypted desktop credentials but no notification implementation. Capacitor had native local notifications and secure mobile credentials but no direct email service. Web had installability, IndexedDB, and best-effort notifications but no secure browser credential store.

The platform layer did not erase those differences. It made them explicit and let the UI degrade around them.

That is the durable result of March 20. The planner did not become cross-platform because a build command produced three targets. It became cross-platform when the domain stopped depending on the target, persistence could swap behind one interface, and unsupported capabilities had honest answers.
