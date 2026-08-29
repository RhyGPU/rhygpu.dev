---
number: "009"
title: "The Password Left localStorage"
subtitle: "Most of it did — and the fallback showed why migration is harder than encryption."
slug: "omni-009-the-password-left-localstorage"
project: "OmniPlanner"
date: 2026-03-19
status: "published"
summary: "Electron safeStorage moved API keys and IMAP passwords out of planner data, but the first migration could discard credentials when encryption was unavailable. Security improved while its failure paths became visible."
tags:
  - omniplanner
  - security
  - credentials
  - electron
  - migrations
  - goals
commits:
  - hash: "b2c81e1ee4226d884456af3e21bb9ca1d6517a23"
    title: "Harden credentials and link daily execution to goals"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/b2c81e1ee4226d884456af3e21bb9ca1d6517a23"
---

OmniPlanner's local-first promise had a contradiction.

The app kept planning data on the user's device, but it also kept AI API keys and IMAP passwords as readable JSON in `localStorage`. Anyone with access to the Electron profile could inspect the same secrets the settings screen hid behind password dots.

The March 18 security model named that as unacceptable. On March 19, Electron `safeStorage` became the new credential boundary.

The change separated account metadata from passwords, encrypted secrets into a file under Electron's user-data directory, migrated existing plaintext on startup, and excluded credentials from backup and restore.

It was a substantial improvement. It also contained two fallback mistakes capable of removing a credential instead of preserving it when encryption was unavailable.

This entry is based on the commit and its exact control flow, not only its phase summary. Security work needs that level of reading because comments describe intent; failure branches describe what the application will actually do.

<div class="section-label">Settings and secrets became different data</div>

An AI configuration contains both ordinary preferences and a credential.

The selected provider, custom endpoint, and model name can remain in planner settings. The API key should not.

`secureSettings.ts` split those shapes. Non-sensitive AI settings continued through the storage adapter. The key moved to a credential named `omni_api_key` in the main-process store.

Email accounts underwent the same separation. Provider, address, host, port, display name, and enabled state remained in the account list. Password became optional in the TypeScript type and moved to a key derived from the account ID.

Backups did not include the encrypted file. Restoring planner data therefore required credentials to be entered again.

That was intentional. A portable backup containing everything needed to decrypt external accounts would recreate the original problem in another format.

<div class="section-label">The encrypted file was not the key</div>

Electron's main process imported `safeStorage` and wrote a JSON object to `credentials.enc.json` in the application data directory.

Each value was encrypted by the operating-system-backed service and encoded as base64 for persistence. The file was created with owner-only read and write mode where the platform honored it.

The JSON file itself was not the protection. Its values remained useful only to a process able to decrypt them through the current user's operating-system context.

The implementation checked `safeStorage.isEncryptionAvailable()` before encryption or decryption. Settings displayed a warning when a new save could not use the keychain.

For email retrieval, the separation was meaningful at runtime too. After an account was saved, the renderer sent account metadata and ID to `email:fetch`. The main process looked up the password itself. The password no longer crossed IPC on every mailbox request.

A pre-save connection test still accepted credentials inline once, because the account had no stored ID yet. That path tested without persisting.

<div class="section-label">The AI key still returned to the renderer</div>

AI providers were still implemented in renderer-side TypeScript.

To keep their synchronous settings API unchanged, startup called `credentialGet('omni_api_key')` and placed the decrypted value in an in-memory renderer cache. Provider calls then read that cache.

The key had left persistent browser storage, but it still entered renderer memory and crossed IPC once per startup.

The preload bridge also exposed generic `credentialGet`, `credentialSet`, and `credentialDelete` methods taking an arbitrary key string. The declared use was migration and AI initialization, but the capability was not limited to the AI key. Renderer code knowing an email credential's key could request it too.

This was safer at rest and still broader at runtime than a least-privilege design. A narrower bridge would expose domain operations — save AI key, test account, fetch mail — without giving renderer code a generic credential reader.

The previous administrator and generic network-proxy architecture also remained in place. `safeStorage` solved plaintext persistence; it did not by itself unwind the privileged process boundary from March 16.

<div class="section-label">Migration ran before the cache warmed</div>

On startup, the app attempted two idempotent operations:

1. move any legacy plaintext credentials into `safeStorage`;
2. load the AI key into the renderer cache.

For an existing safeStorage value, migration preserved the stored value rather than overwriting it with a stale local copy. Email passwords were keyed per account. After migration, password fields were removed from the account array.

That was the correct desired sequence: write encrypted, verify availability, then erase plaintext.

The implementation skipped the verification step.

For a legacy AI key, it called `credentialSet` and then stripped the key from local storage regardless of whether the call returned `true`. For an email password, it did the same: attempt the encrypted write, then delete the plaintext field and save the sanitized account list.

On a system where `safeStorage` was unavailable, the migration could therefore turn an insecure but working credential into no credential at all.

Idempotence protected against repeated overwrites. It did not protect against a failed first write followed by successful deletion of the source.

The safe migration rule should have been stricter:

> Never destroy the old representation until the new representation has been written and read back successfully.

<div class="section-label">The fallback contradicted its sanitizer</div>

The new-account flow tried to provide a fallback.

If `credentialSet` returned false, it attached the password to the account object and warned that the value would be stored in plain local storage. That was an explicit degradation rather than silent failure.

Immediately afterward, `saveEmailAccounts` removed every `password` field before writing the array.

The fallback object and the sanitizer canceled each other. The UI could warn that a plain password was saved while the persistence helper had discarded it.

This is a useful example of why credential handling should not be distributed across component state and generic serializers. Each function followed a plausible local rule:

- the save action wanted a working fallback;
- the account serializer wanted to guarantee no password reached local storage.

Together they produced neither property.

A better product choice would be to refuse persistent account creation when secure storage is unavailable, or to make an explicitly temporary session credential. Claiming a plaintext fallback while globally sanitizing plaintext was not a stable contract.

<div class="section-label">Daily work joined goal progress</div>

The same phase extended the goal model from weekly commitments to daily tasks.

The link picker extracted in the previous phase was reused beside each day's todo list. A daily task could point to the same `GoalItem.id` as a weekly business or personal commitment.

Goal progress then combined two derived scans:

- weekly linked todos from `week.goals.business` and `week.goals.personal`;
- daily linked todos from every `dailyPlans[date].todos` collection.

The summary retained weekly and daily counts separately and exposed a combined total. Completing every linked item still did not automatically complete the long-range goal.

This added the final operational step to the goal chain:

> life goal → weekly commitment → daily action

The relationship remained stored once, on each todo's `parentGoalId`. No reverse arrays needed synchronization.

<div class="section-label">A real improvement with unfinished edges</div>

Phase 4 materially changed OmniPlanner's security posture:

- routine planner backups stopped carrying account secrets;
- email passwords stayed in the main process after initial save;
- AI and email metadata separated from their credentials;
- existing users had an automatic migration path;
- settings could report that OS encryption was unavailable;
- the preload API received a TypeScript contract.

It did not complete the boundary:

- the AI key still crossed into renderer memory;
- generic credential methods remained exposed;
- the administrator/network architecture remained;
- failed encryption during legacy migration could erase the only copy;
- the new-account plaintext fallback was sanitized before persistence.

Recording those edges does not erase the improvement. It identifies the work the improvement made newly possible to see.

Before this commit, secrets and settings were the same object. After it, the application had a place where a credential was supposed to live, a migration path toward that place, and concrete failure cases to harden.

The password left `localStorage`. The next security work would need to make sure it always arrived somewhere safer before the old copy disappeared.
