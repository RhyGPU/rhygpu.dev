---
number: "014"
title: "OAuth Worked on a Branch"
subtitle: "Password login stayed; PKCE and token refresh joined it without reaching master."
slug: "omni-014-oauth-worked-on-a-branch"
project: "OmniPlanner"
date: 2026-04-06
status: "published"
summary: "A feature branch hardened IMAP timeouts, added Gmail and Outlook OAuth with PKCE, and implemented one-refresh/one-retry token recovery while preserving app-password accounts. It remained unmerged."
tags:
  - omniplanner
  - email
  - oauth
  - pkce
  - electron
  - wip
commits:
  - hash: "49c79ed34d1dede9340e98f2e43cd65997c9cfd2"
    title: "Harden email timeouts and main-process crash handling"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/49c79ed34d1dede9340e98f2e43cd65997c9cfd2"
  - hash: "3bec6fcfc9ea61a08369ebe8a4a478032c033aa2"
    title: "Add OAuth login while preserving IMAP passwords"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/3bec6fcfc9ea61a08369ebe8a4a478032c033aa2"
  - hash: "e0867c2f3a0a7aa70ab0b804ebd4cf6737cfdb9f"
    title: "Add OAuth token refresh and re-authentication"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/e0867c2f3a0a7aa70ab0b804ebd4cf6737cfdb9f"
---

OAuth existed in OmniPlanner and did not exist on `master`.

Three commits on `origin/claude/email-timeout-crash-hardening-9KMOl` implemented the full path: bounded IMAP operations, Gmail and Outlook browser sign-in, safe token storage, XOAUTH2 authentication, access-token refresh, a single retry, and a visible reconnect action.

The branch passed the existing 138 tests and TypeScript check. It was never merged into the main branch visible in the repository history.

That status matters. The old devlog grouped OAuth into the March Phase 20–22 summary as if it were part of the same landed productization series. The actual commits are dated April 6 and April 8 and remain on a remote feature branch.

This entry records the implementation as real branch work, not as a released capability.

<div class="section-label">First, make failure finish</div>

The OAuth branch began by hardening password-based IMAP.

Unresponsive servers could leave a connection pending indefinitely. Socket errors could fire outside the awaited call chain and become uncaught main-process exceptions. Cleanup could throw while handling the original failure and replace the useful error with a logout error.

Phase 21-A added three bounds to every IMAP path:

- 15 seconds for connection;
- 10 seconds for the server greeting;
- 30 seconds for socket activity.

Each client received an error listener. Handlers tracked phases from credentials through connect, mailbox open, fetch or parse, and logout. Failure responses included that phase beside the existing code and operation ID.

Logout became best-effort. Error paths used a safe close helper so cleanup could not mask the primary failure.

This work was a prerequisite for OAuth because adding a second authentication method would multiply ambiguity if the underlying connection could still hang or crash without a phase.

<div class="section-label">A provider registry replaced one generic form</div>

The next commit made email-provider capability explicit.

Gmail and Outlook supported OAuth and IMAP via XOAUTH2. Yahoo, Naver, Daum, and custom servers remained app-password or password IMAP. Each provider carried setup guidance instead of sharing one generic credential form.

`EmailAccount` gained an optional `authMethod`: `imap_password` or `oauth`. Keeping it optional allowed existing accounts to behave as password accounts without a migration.

The settings screen offered **Sign in with Google** or Microsoft on desktop and retained **Use app password instead**. Password-only providers showed their manual setup. Account rows displayed which method they used.

OAuth did not replace the working IMAP pipeline. It changed the credentials supplied to it.

The main process selected either `{ user, pass }` from the password credential key or `{ user, accessToken }` from the OAuth credential key. Mailbox fetch and body loading remained the same operations afterward.

<div class="section-label">Desktop OAuth used a public-client flow</div>

Google and Microsoft client IDs came from build-time environment variables. No client secret was embedded.

That is appropriate for a desktop public client: an installed executable cannot keep a distributed client secret confidential.

The implementation generated a random PKCE verifier, derived an S256 challenge, opened the system browser, and waited up to five minutes for `omniplanner://oauth/callback`.

On macOS and Linux, the application listened for `open-url`. On Windows, a second instance received the custom protocol URL; a single-instance lock forwarded it to the running process. The token exchange used the verifier, then fetched the user's address and encrypted access and refresh tokens through the existing safeStorage store.

Tokens never returned to the renderer. The renderer received account identity and outcome.

The implementation supported one pending OAuth flow at a time. Starting another canceled the first rather than leaving two unresolved browser callbacks.

<div class="section-label">PKCE was present; state was not</div>

The branch implemented PKCE correctly as a code-verifier binding. It did not add an OAuth `state` parameter to the authorization URL or validate one in the callback.

PKCE prevents an intercepted authorization code from being redeemed without the verifier. `state` protects a different edge: associating the callback with the browser authorization request and reducing login CSRF or callback confusion.

The single pending-flow object and custom protocol routing provided application context, but they were not a cryptographic state check returned by the provider.

For a branch implementation, this was a concrete hardening item before merge. Custom URI schemes also require care because protocol ownership can be contested by another local application; PKCE limits the value of an intercepted code but does not make callback routing irrelevant.

The absence of a client secret was correct. The absence of `state` was unfinished.

<div class="section-label">Refresh was allowed exactly once</div>

An OAuth login that works only until the first access token expires is not a usable email account.

Phase 21-C extracted the fetch and body operations so handlers could run them normally, then repeat them once without duplicating IMAP logic.

The retry policy was narrow:

1. attempt the requested IMAP operation;
2. only for an OAuth account and an `EMAIL_AUTH_FAILED` result, load the refresh token;
3. request a new access token;
4. store it through safeStorage;
5. retry the original operation once;
6. never enter another refresh loop.

Network, TLS, mailbox, and parsing failures did not trigger token refresh.

Refresh failure received specific codes: token expired, refresh unavailable, refresh failed, invalid response, or reauthentication required. `invalid_grant` and revoked or expired refresh credentials moved the UI to a visible **Reconnect** action instead of repeatedly testing an account that could not recover itself.

That policy separated transient access-token expiry from a broken account grant and from unrelated network failure.

<div class="section-label">Password and OAuth cleanup coexisted</div>

Removing an account deleted the password credential and both OAuth token credentials. Missing keys were harmless, so one cleanup path worked for either authentication method.

The coexistence was pragmatic. OAuth client IDs might not be configured in every build. Some providers did not support the implemented flow. Existing users already had app passwords.

When OAuth configuration was absent, the settings UI could direct Gmail or Outlook users back to the password path rather than making email entirely unavailable.

This also meant the security story was mixed. OAuth avoided storing a long-lived mailbox password and allowed revocable scoped authorization, but the requested scopes were broad enough to support IMAP access. The password path remained for compatibility. Both still depended on the earlier safeStorage and main-process design.

<div class="section-label">Implemented is not integrated</div>

The branch contained a coherent vertical slice:

- provider capability metadata;
- desktop browser authorization;
- PKCE exchange;
- encrypted token storage;
- XOAUTH2 IMAP reuse;
- bounded failures and diagnostic phases;
- single refresh and retry;
- reauthentication UI.

It also retained known work: OAuth state validation, platform verification of custom-protocol callbacks, packaging with real provider client IDs, and merge review against the main branch.

Because the commits remained only on the remote feature branch, none of this should be described as a capability of the mainline April build.

The accurate devlog statement is narrower: OAuth reached an implemented and typechecked branch, preserved IMAP password accounts, and solved token lifecycle far enough to expose the remaining security and integration decisions. It did not reach `master`.
