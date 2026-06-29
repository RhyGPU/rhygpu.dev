import json
from pathlib import Path


SOURCE = Path("extracted_chats/c63174a8-f6b9-4999-8508-8a699d1dc0ab.chat.cleaned.jsonl")
OUT_DIR = Path("extracted_chats/causal_path")


PHASES = [
    {
        "file": "01_mock_vs_real_app.md",
        "title": "01. Mock vs Real App",
        "start": 1,
        "end": 12,
        "purpose": "The user asks to compare the current Mnemosyne UI with the uploaded design handoff. The first causal fork is that the mock has a strong flow, but it was made without knowing the real app.",
        "decisions": [
            "Current app is functional but reads like a dense settings/control panel.",
            "Mock is not a reliable implementation spec by itself; it is a vision of UX flow and atmosphere.",
            "Real app concepts are Souls, Settings/Worlds, Sessions, Editor/Workshop, Chat, Settings drawer, and richer backend state.",
        ],
        "bridge": "This leads to the user clarifying that the skin itself is not the goal. The desired thing is the mock's easier, more intuitive UX flow, adapted to the actual app.",
    },
    {
        "file": "02_theme_and_flow_decisions.md",
        "title": "02. Theme and Flow Decisions",
        "start": 13,
        "end": 30,
        "purpose": "The user separates visual skin from UX flow, supplies visual references, and locks the aesthetic and high-level navigation direction.",
        "decisions": [
            "Do not copy the dark mock skin. Use a book/editorial paper direction: Kindle/reMarkable calm plus editorial hierarchy.",
            "Dev mode should keep a terminal/machine-room feel.",
            "State Map visibility should be mode-driven: realistic shows minimal info, reader shows more, god/GM shows all.",
            "Backend should retain the full state; UI mode only controls what is revealed.",
            "Adopt the mock's meaningful left nav rail and make State Map a real page, not a drawer or hidden detail.",
        ],
        "bridge": "After these decisions, the user asks for a new UX plan starting from the purpose of sessions, not from the old plan or the mock alone.",
    },
    {
        "file": "03_new_plan_and_wrong_v2_prototype.md",
        "title": "03. New Plan and Wrong V2 Prototype",
        "start": 31,
        "end": 63,
        "purpose": "The assistant creates a new UX plan, but then implements the wrong artifact: a separate V2 prototype with mock data instead of overhauling the real app.",
        "decisions": [
            "Purpose is composable toggles, not a single fixed mode.",
            "Purpose can change mid-campaign; visibility recomputes while backend data remains saved.",
            "God mode maps to GM for now.",
            "Theme is locked: book/editorial for human UI, terminal for dev UI.",
            "The assistant builds `docs/UX-plan-v2.md` and then creates a `?v2` prototype, which becomes a mistake because it lacks real feature parity.",
        ],
        "bridge": "The user rejects the prototype approach and tells the assistant to apply the overhaul to local real files, because git can protect against bad changes.",
    },
    {
        "file": "04_real_app_vs_mock_data_failure.md",
        "title": "04. Real App vs Mock Data Failure",
        "start": 64,
        "end": 81,
        "purpose": "The user calls out the core failure: the assistant replaced the working app with a half-functional mock. The assistant admits this and starts touching the real app, but only fixes theme first.",
        "decisions": [
            "The default app must be the real app, not `?v2` mock data.",
            "The correct job is: mock UX flow, all original UI features moved into it, everything functional.",
            "Paper theme should be near-monochrome warm paper and ink, not reddish or green/teal.",
            "The assistant applies a real stylesheet color pass, but still has not done the UX flow first.",
        ],
        "bridge": "The next day, the user re-centers the work: UX flow was the priority all along, not a color pass.",
    },
    {
        "file": "05_priority_reset_and_tab_mapping.md",
        "title": "05. Priority Reset and Tab Mapping",
        "start": 82,
        "end": 99,
        "purpose": "The user forces the assistant to restate the real target: this is a UI overhaul of the existing app using the mock's flow, not a mock app creation.",
        "decisions": [
            "Feature parity is the priority: every existing OG UI feature must be relocated into the new flow.",
            "Mock tabs are mapped into app vocabulary: Campaigns becomes Home, Play stays Play, State Map becomes the full info hub, Characters/Library/Workshop map to existing creation/editing surfaces, Settings becomes a page.",
            "Home must have four shelves: Recent, Recommended/non-played, Best rated, Waiting/high-positive-affection characters.",
            "State Map must be a whole view with all session state visible on one page, including state, memories, relationships, and related info.",
            "Backend gaps are discovered: ratings and per-soul aggregate affection are not directly available, so some shelves need placeholders unless backend fields are added.",
        ],
        "bridge": "The assistant starts building Home with real data plus placeholders, but the user pushes back against stopping after partial completion.",
    },
    {
        "file": "06_partial_home_then_dev_gap.md",
        "title": "06. Partial Home Then Dev Gap",
        "start": 100,
        "end": 118,
        "purpose": "The assistant builds Home and claims progress, then tries to finish the five-tab rail. The user points out that Dev mode was still missed.",
        "decisions": [
            "Recent shelf uses real conversations and resumes through the existing `handleSelectConversation` path.",
            "Recommended shelf uses souls with no conversation.",
            "Best rated and Waiting are explicit placeholders because the backend does not expose the needed fields yet.",
            "The rail becomes Home, Play, State Map, Library, Settings.",
            "Dev is not a normal paper tab; it should be a distinct terminal-styled entry pinned near the bottom of the rail and enter the in-session dev terminal.",
        ],
        "bridge": "The user then demands a definition of ALL, because the assistant keeps declaring partial wins while missing adjacent agreed requirements.",
    },
    {
        "file": "07_define_all_and_final_pass.md",
        "title": "07. Define All and Final Pass",
        "start": 119,
        "end": 149,
        "purpose": "The assistant defines ALL as the mock flow plus every OG feature, functional, paper/terminal themed, and attempts a final broad pass.",
        "decisions": [
            "ALL means no partial tab-by-tab victory: rail, Home, Play, State Map, Library/Workshop, Settings, Dev, paper theme, terminal dev, and OG feature parity.",
            "State Map should render the real loaded Soul: memories, relationships, world, plots, psyche, objects, timeline, and schema/memory data.",
            "Play should keep the rail, remove redundant Library button, and include a real pipeline progress bar from `latestPipelineTrace.stages`.",
            "Home should lead with a Continue hero like the mock, then shelves.",
            "Settings should become a real page rather than only the chat drawer.",
            "The assistant reports a compile/typecheck uncertainty caused by a possibly torn sandbox mirror, while saying authoritative file reads looked balanced.",
        ],
        "bridge": "The final state is unresolved from the user's perspective: work was attempted, but trust is gone and the user exits.",
    },
    {
        "file": "08_closeout_and_pickup_notes.md",
        "title": "08. Closeout and Pickup Notes",
        "start": 150,
        "end": 151,
        "purpose": "The conversation ends with the user abandoning the thread and the assistant acknowledging the failure mode.",
        "decisions": [
            "The main failure was not grasping ALL and priorities up front.",
            "The assistant says changes exist across `App.tsx`, `uiTypes.ts`, and `styles.css` and can be inspected with git.",
            "The next AI should not restart from the mock alone; it must read the causal path and verify the actual current files.",
        ],
        "bridge": "A successor should begin by checking git diff, build/typecheck output, and whether the real app currently reflects the agreed flow.",
    },
]


def load_rows():
    rows = []
    with SOURCE.open("r", encoding="utf-8") as fh:
        for idx, line in enumerate(fh, 1):
            row = json.loads(line)
            row["seq"] = idx
            rows.append(row)
    return rows


def message_block(row):
    role = row["role"].upper()
    timestamp = row["timestamp"] or "no timestamp"
    uuid = row["uuid"] or "no uuid"
    text = row["text"].strip()
    return f"### {row['seq']:03d}. {role} | {timestamp}\n\n`uuid: {uuid}`\n\n{text}\n"


def write_phase(rows, phase):
    selected = [r for r in rows if phase["start"] <= r["seq"] <= phase["end"]]
    path = OUT_DIR / phase["file"]
    lines = [
        f"# {phase['title']}",
        "",
        f"Source messages: `{phase['start']:03d}` to `{phase['end']:03d}`",
        f"Time span: `{selected[0]['timestamp']}` to `{selected[-1]['timestamp']}`",
        "",
        "## Why This Chunk Exists",
        "",
        phase["purpose"],
        "",
        "## Decisions / Causal Facts",
        "",
    ]
    lines.extend(f"- {item}" for item in phase["decisions"])
    lines.extend(
        [
            "",
            "## Bridge To Next Chunk",
            "",
            phase["bridge"],
            "",
            "## Raw Messages In This Segment",
            "",
        ]
    )
    for row in selected:
        lines.append(message_block(row))
        lines.append("---")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    return path, selected


def write_readme(rows, phase_outputs):
    path = OUT_DIR / "00_README.md"
    lines = [
        "# Mnemosyne UI Overhaul Causal Path",
        "",
        "This folder reorganizes the extracted chat into AI-digestible chronological chunks. Read in numeric order. Each chunk explains the causal role of that section, records the decisions, and includes the raw messages for that time span.",
        "",
        "## How To Use",
        "",
        "1. Read `00_README.md` first.",
        "2. Read `01_...` through `08_...` in order.",
        "3. Treat `extracted_chats/c63174a8-f6b9-4999-8508-8a699d1dc0ab.chat.md` as the raw source of truth if something seems missing.",
        "4. Before implementing anything, inspect the current repository state and `git diff`; the prior assistant may have left partial edits.",
        "",
        "## One-Screen Causal Summary",
        "",
        "The user wanted the mock's UX flow applied to the real Mnemosyne app with all existing features preserved. The conversation went wrong because the assistant first over-focused on theme and then built a separate mock-data V2 prototype. The user corrected this repeatedly: the task was a real UI overhaul, not a fake mock app. The locked target became: paper/editorial human UI, terminal Dev UI, persistent nav rail, Home shelves, Play with pipeline status, State Map as a full real data hub, Library/Workshop with original creation/editing features, Settings as a page, Dev reachable clearly, and backend data hidden/revealed by mode rather than deleted.",
        "",
        "## Chunk Index",
        "",
    ]
    for phase, chunk_path, selected in phase_outputs:
        user_count = sum(1 for r in selected if r["role"] == "user")
        assistant_count = sum(1 for r in selected if r["role"] == "assistant")
        char_count = sum(len(r["text"]) for r in selected)
        lines.append(
            f"- [{phase['title']}]({chunk_path.name}) - messages {phase['start']:03d}-{phase['end']:03d}, "
            f"{user_count} user / {assistant_count} assistant, ~{char_count:,} chars."
        )
    lines.extend(
        [
            "",
            "## Locked Requirements",
            "",
            "- Use the mock as UX flow inspiration, not as fake product truth.",
            "- Preserve and relocate every OG UI feature; feature parity matters more than new concepts.",
            "- Human-facing UI is book/editorial paper: warm paper, ink, hairline rules, restrained accent.",
            "- Dev UI is terminal/machine-room styled and should be reachable directly.",
            "- State Map is a full page/hub backed by real loaded Soul/session data.",
            "- Mode/Purpose affects visibility only; backend state remains saved.",
            "- Home should include Recent, Recommended/non-played, Best rated, and Waiting/high-positive-affection shelves. Use honest placeholders where backend fields are absent.",
            "",
            "## Known Risk From Original Thread",
            "",
            "The previous assistant reported uncertainty around build/typecheck due to a Windows/Linux sandbox mirror issue. Do not trust that claim blindly. Run the actual local checks in the current environment and inspect the real current files.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def write_combined(readme_path, phase_paths):
    combined = OUT_DIR / "combined_causal_path.md"
    parts = []
    for path in [readme_path, *phase_paths]:
        parts.append(path.read_text(encoding="utf-8"))
        parts.append("\n\n")
    combined.write_text("\n".join(parts), encoding="utf-8")
    return combined


def main():
    rows = load_rows()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    phase_outputs = []
    phase_paths = []
    for phase in PHASES:
        path, selected = write_phase(rows, phase)
        phase_outputs.append((phase, path, selected))
        phase_paths.append(path)
    readme = write_readme(rows, phase_outputs)
    combined = write_combined(readme, phase_paths)
    print(readme)
    for path in phase_paths:
        print(path)
    print(combined)


if __name__ == "__main__":
    main()
