# Mnemosyne UI Overhaul Causal Path

This folder reorganizes the extracted chat into AI-digestible chronological chunks. Read in numeric order. Each chunk explains the causal role of that section, records the decisions, and includes the raw messages for that time span.

## How To Use

1. Read `00_README.md` first.
2. Read `01_...` through `08_...` in order.
3. Treat `extracted_chats/c63174a8-f6b9-4999-8508-8a699d1dc0ab.chat.md` as the raw source of truth if something seems missing.
4. Before implementing anything, inspect the current repository state and `git diff`; the prior assistant may have left partial edits.

## One-Screen Causal Summary

The user wanted the mock's UX flow applied to the real Mnemosyne app with all existing features preserved. The conversation went wrong because the assistant first over-focused on theme and then built a separate mock-data V2 prototype. The user corrected this repeatedly: the task was a real UI overhaul, not a fake mock app. The locked target became: paper/editorial human UI, terminal Dev UI, persistent nav rail, Home shelves, Play with pipeline status, State Map as a full real data hub, Library/Workshop with original creation/editing features, Settings as a page, Dev reachable clearly, and backend data hidden/revealed by mode rather than deleted.

## Chunk Index

- [01. Mock vs Real App](01_mock_vs_real_app.md) - messages 001-012, 2 user / 10 assistant, ~7,116 chars.
- [02. Theme and Flow Decisions](02_theme_and_flow_decisions.md) - messages 013-030, 6 user / 12 assistant, ~19,770 chars.
- [03. New Plan and Wrong V2 Prototype](03_new_plan_and_wrong_v2_prototype.md) - messages 031-063, 2 user / 31 assistant, ~8,294 chars.
- [04. Real App vs Mock Data Failure](04_real_app_vs_mock_data_failure.md) - messages 064-081, 5 user / 13 assistant, ~6,801 chars.
- [05. Priority Reset and Tab Mapping](05_priority_reset_and_tab_mapping.md) - messages 082-099, 6 user / 12 assistant, ~15,449 chars.
- [06. Partial Home Then Dev Gap](06_partial_home_then_dev_gap.md) - messages 100-118, 4 user / 15 assistant, ~5,961 chars.
- [07. Define All and Final Pass](07_define_all_and_final_pass.md) - messages 119-149, 2 user / 29 assistant, ~10,252 chars.
- [08. Closeout and Pickup Notes](08_closeout_and_pickup_notes.md) - messages 150-151, 1 user / 1 assistant, ~520 chars.

## Locked Requirements

- Use the mock as UX flow inspiration, not as fake product truth.
- Preserve and relocate every OG UI feature; feature parity matters more than new concepts.
- Human-facing UI is book/editorial paper: warm paper, ink, hairline rules, restrained accent.
- Dev UI is terminal/machine-room styled and should be reachable directly.
- State Map is a full page/hub backed by real loaded Soul/session data.
- Mode/Purpose affects visibility only; backend state remains saved.
- Home should include Recent, Recommended/non-played, Best rated, and Waiting/high-positive-affection shelves. Use honest placeholders where backend fields are absent.

## Known Risk From Original Thread

The previous assistant reported uncertainty around build/typecheck due to a Windows/Linux sandbox mirror issue. Do not trust that claim blindly. Run the actual local checks in the current environment and inspect the real current files.
