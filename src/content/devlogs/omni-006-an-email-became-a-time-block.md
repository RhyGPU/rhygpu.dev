---
number: "006"
title: "An Email Became a Time Block"
subtitle: "The inbox and imported calendars entered the same week store."
slug: "omni-006-an-email-became-a-time-block"
project: "OmniPlanner"
date: 2026-03-12
status: "published"
summary: "Real IMAP retrieval replaced the placeholder inbox, AI could turn a message into a calendar event, and an ICS importer merged external calendars into OmniPlanner's week-isolated model."
tags:
  - omniplanner
  - email
  - imap
  - icalendar
  - electron
  - integration
commits:
  - hash: "d22cc7ef1a207e7b9613dcca5ffb12ef999ddcca"
    title: "Add email retrieval and AI-powered calendar extraction"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/d22cc7ef1a207e7b9613dcca5ffb12ef999ddcca"
  - hash: "b80080f6128a00c8cf6b2f4e17e5d6e27ba6e462"
    title: "Fix IMAP connection and implement ICS calendar import"
    repo: "OmniPlanner"
    url: "https://github.com/RhyGPU/OmniPlanner/commit/b80080f6128a00c8cf6b2f4e17e5d6e27ba6e462"
---

OmniPlanner's first inbox contained a welcome message from OmniPlan itself.

It proved the interface could list, open, mark, archive, and delete an `Email` object. It did not prove the app could receive email.

On March 12, the inbox crossed that boundary. The Electron main process connected to real IMAP servers, the renderer loaded message bodies on demand, and an AI action could extract a dated event from a message and insert it into the planner.

The next day, the connection failed because Electron's embedded Node runtime was older than a transitive logging dependency expected. Fixing that runtime mismatch arrived in the same commit as the first working iCalendar importer.

This is a repository reconstruction rather than a transcript-backed entry. The two commits show both the intended integration and its first compatibility failure. They also show where the implementation was still deliberately thin.

<div class="section-label">The inbox moved into the main process</div>

IMAP could not be treated like another browser fetch.

It needed raw network access, credentials, mailbox locks, and a long-lived protocol client. That work belonged behind Electron's process boundary rather than inside the React renderer.

The main process gained handlers for fetching message envelopes and loading one message body. The preload bridge exposed those operations to the UI without turning Node integration back on.

For Gmail, Outlook, Yahoo, and Naver, OmniPlanner supplied known IMAP hosts on secure port 993. A custom provider accepted its own host and port. The account screen let the user name an account, enter an address and app password, test the connection, and remove the configuration.

Fetching mail opened the inbox, took a mailbox lock, and read up to the most recent 50 envelopes. The list stored sender, subject, timestamp, read state, UID, and account identity. Bodies were deferred until a message was opened.

That separation made the first retrieval cheaper and preserved enough provenance to return to the correct account for the body.

At this point, account passwords were stored with the rest of the settings in `localStorage`. That was a functional prototype, not an acceptable final credential boundary. Electron `safeStorage` and a unified secure-settings service came later. The early implementation proved the workflow before it proved the security model.

<div class="section-label">The first connection failed below the feature</div>

`imapflow` depended on `pino`, and the installed logging stack expected `diagnostics_channel.tracingChannel`, an API introduced after the Node version embedded in the Electron release used by OmniPlanner.

The application code could be correct and still fail before the IMAP client did useful work.

The next commit added a compatibility implementation in the main process. When `tracingChannel` did not exist, it assembled the expected start, end, async, and error channels from the older `diagnostics_channel` primitives.

This was not an email-protocol fix. It was a runtime-contract fix between Electron, Node, and a transitive dependency.

The distinction matters in desktop JavaScript. Updating an npm package does not update the Node runtime inside Electron. A package can install successfully, type-check, and then call a platform API the packaged application does not provide.

The polyfill was scoped to the missing API and installed before `imapflow` was required. If the diagnostics module itself was unavailable, the email path still failed through its normal error result rather than taking down the entire app.

<div class="section-label">Mail became a planner input</div>

Retrieval alone would have made OmniPlanner an inbox client. The product goal was to connect incoming obligations to planning.

When a loaded message had a body, the inbox displayed **Add to Calendar**. The AI provider layer received the text and attempted to return a title, date, start hour, and duration. The renderer converted that result into a `CalendarEvent` and passed it to the application shell.

From there, the operation used the same route as manual calendar editing:

- find or create the week containing the extracted date;
- find the corresponding daily plan;
- append the event to that day's events;
- save the updated week through `allWeeks`.

The inbox did not maintain its own appointment list. It produced an input for the calendar domain.

The action also remained explicitly fallible. No configured AI, an extraction failure, or a message without a recognizable event produced feedback instead of inventing a date silently.

The parsing and review experience was still minimal. The first version added the returned event after a confirmation alert rather than presenting an editable preview. Later work would make email-to-calendar a more deliberate two-step workflow.

<div class="section-label">The disabled iCalendar card became a file input</div>

The Data tab already showed an **Integrate iCal (.ics)** card.

It was disabled and labeled “coming soon.” On March 13, the placeholder became a file picker.

The parser unfolded RFC 5545 continuation lines, walked `VEVENT` blocks, and extracted `SUMMARY`, `DESCRIPTION`, `DTSTART`, and `DTEND`. It accepted compact date-time values and all-day dates. Same-day start and end values produced a duration; an absent end defaulted to one hour.

Every parsed event received a date and the planner's `CalendarEvent` shape. The application grouped those events into the correct week and day, appending them to the same daily event arrays used by manual edits and email extraction. The import card reported how many events were added or whether parsing returned nothing.

The old placeholder had promised that Google Calendar, Outlook, and Apple Calendar exports would “merge into your weekly timeline.” This commit made that specific path real.

<div class="section-label">The first parser was intentionally incomplete</div>

Supporting an `.ics` extension is not the same as implementing all of iCalendar.

The first parser ignored recurrence rules, exceptions, alarms, locations, organizer metadata, and most parameter semantics. It extracted a value after `TZID` but did not apply the named timezone. A trailing `Z` was accepted without converting UTC to local time. All-day events became 9:00 AM blocks. Multi-day events became a one-hour block on their starting date.

Import also appended events without a stable external UID or deduplication rule. Importing the same file twice could create the same appointments twice.

The email body reader was similarly narrow. It searched the raw message source for a plain-text MIME section with a regular expression. Multipart encodings, HTML-only mail, quoted-printable content, and complex charsets could escape it.

These limitations are important because the UI now crossed real external-data boundaries. The commit established a working vertical slice, not a standards-complete calendar or mail engine.

Later phases added MIME parsing, sandboxed rich HTML, error taxonomy, OAuth lifecycle, preview-based flows, and stronger credentials. The value of the first slice was that those future improvements now had an end-to-end route to strengthen.

<div class="section-label">Three ways into one week</div>

By the end of March 13, a calendar event could enter OmniPlanner in three ways:

- the user could create it in the monthly or weekly planner;
- AI could extract it from a fetched email;
- an external calendar could supply it in an ICS file.

All three ended in the same week-isolated data model.

That convergence was more important than the number of integrations. If each source had created its own event store, the monthly calendar, weekly grid, backup system, and future analytics would all need to reconcile competing truths.

Instead, email and iCalendar became ingestion paths. The planner remained the owner of planned time.

The original product sentence had placed personal planning, iCalendar, todos, goals, and email beside one another. A month after that sentence, two of those boundaries finally touched: an incoming message could become time, and an external calendar could become a week.
