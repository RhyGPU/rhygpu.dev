import base64
import hashlib
import json
import re
import zipfile
from datetime import datetime
from pathlib import Path


ROOT = Path(r"D:\정준화\rhygpu.dev\Mnemosyne Chat Log")
OUT_DIR = ROOT / "00_FINAL_DELIVERABLES"
OUT = OUT_DIR / "Mnemosyne_COMPLETE_CAUSAL_LOG_ANTHOLOGY.txt"
MANIFEST = OUT_DIR / "Mnemosyne_COMPLETE_CAUSAL_LOG_ANTHOLOGY.manifest.json"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_text(path: Path) -> str:
    data = path.read_bytes()
    for enc in ("utf-8-sig", "utf-8", "cp949", "utf-16"):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def section_header(title: str, source: Path | str, note: str, data: bytes | None = None) -> str:
    source_text = str(source)
    size = len(data) if data is not None else "n/a"
    digest = sha256_bytes(data) if data is not None else "n/a"
    return (
        "\n\n"
        + "=" * 96
        + f"\nSECTION: {title}\n"
        + f"SOURCE: {source_text}\n"
        + f"BYTE_LENGTH: {size}\n"
        + f"SHA256: {digest}\n"
        + f"CAUSAL_NOTE: {note}\n"
        + "=" * 96
        + "\n\n"
    )


def binary_section(title: str, source: Path | str, note: str, data: bytes) -> str:
    encoded = base64.b64encode(data).decode("ascii")
    return (
        section_header(title, source, note + " Stored as base64 to preserve non-text bytes.", data)
        + "BEGIN_BASE64\n"
        + encoded
        + "\nEND_BASE64\n"
    )


def text_section(title: str, source: Path | str, note: str, data: bytes, text: str | None = None) -> str:
    if text is None:
        try:
            text = data.decode("utf-8-sig")
        except UnicodeDecodeError:
            text = data.decode("utf-8", errors="replace")
    return (
        section_header(title, source, note, data)
        + "BEGIN_SOURCE_TEXT\n"
        + text
        + "\nEND_SOURCE_TEXT\n"
    )


def natural_part_key(path: Path):
    name = path.name
    match = re.search(r"(?:part_|_)(\d+)\.txt$", name)
    if match:
        return int(match.group(1))
    return name


def zip_inventory(path: Path) -> dict:
    with zipfile.ZipFile(path, "r") as zf:
        return {
            "zip": str(path),
            "entries": [
                {
                    "name": info.filename,
                    "compressed_size": info.compress_size,
                    "file_size": info.file_size,
                    "date_time": info.date_time,
                }
                for info in zf.infolist()
            ],
        }


def is_probably_text(name: str, data: bytes) -> bool:
    lower = name.lower()
    if lower.endswith((".txt", ".md", ".json", ".jsonl", ".log", ".html", ".js", ".css", ".csv", ".tsv", ".xml", ".yaml", ".yml")):
        return True
    if b"\x00" in data[:4096]:
        return False
    sample = data[:4096]
    if not sample:
        return True
    printable = sum(1 for b in sample if b in b"\r\n\t" or 32 <= b <= 126 or b >= 128)
    return printable / len(sample) > 0.92


def add_zip_contents(parts: list[str], manifest: list[dict], zip_path: Path, title: str, note: str):
    zip_data = zip_path.read_bytes()
    parts.append(binary_section(f"{title} - RAW ZIP BYTES", zip_path, note + " Raw zip bytes included for strict no-omission preservation.", zip_data))
    manifest.append({"kind": "zip_raw_binary_base64", "path": str(zip_path), "sha256": sha256_bytes(zip_data), "bytes": len(zip_data)})

    inv = zip_inventory(zip_path)
    inv_bytes = json.dumps(inv, ensure_ascii=False, indent=2).encode("utf-8")
    inventory_source = f"{zip_path}::INVENTORY"
    parts.append(text_section(f"{title} - ZIP INVENTORY", inventory_source, note, inv_bytes, inv_bytes.decode("utf-8")))
    manifest.append({"kind": "zip_inventory", "path": inventory_source, "sha256": sha256_bytes(inv_bytes), "bytes": len(inv_bytes), "entries": inv["entries"]})

    with zipfile.ZipFile(zip_path, "r") as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            data = zf.read(info.filename)
            virtual = f"{zip_path}::{info.filename}"
            entry_note = f"Extracted from zip in archive order. Parent zip SHA256={sha256_bytes(zip_data)}."
            if is_probably_text(info.filename, data):
                try:
                    text = data.decode("utf-8-sig")
                except UnicodeDecodeError:
                    text = data.decode("utf-8", errors="replace")
                parts.append(text_section(f"{title} - ZIP ENTRY - {info.filename}", virtual, entry_note, data, text))
                kind = "zip_text_entry"
            else:
                parts.append(binary_section(f"{title} - ZIP ENTRY - {info.filename}", virtual, entry_note, data))
                kind = "zip_binary_entry_base64"
            manifest.append({"kind": kind, "path": virtual, "sha256": sha256_bytes(data), "bytes": len(data)})


def add_file(parts: list[str], manifest: list[dict], path: Path, title: str, note: str, force_binary: bool = False):
    data = path.read_bytes()
    if force_binary or not is_probably_text(path.name, data):
        parts.append(binary_section(title, path, note, data))
        kind = "binary_base64"
    else:
        parts.append(text_section(title, path, note, data, read_text(path)))
        kind = "text"
    manifest.append({"kind": kind, "path": str(path), "sha256": sha256_bytes(data), "bytes": len(data)})


def main():
    parts: list[str] = []
    manifest: list[dict] = []

    now = datetime.now().isoformat(timespec="seconds")
    intro = f"""MNEMOSYNE COMPLETE CAUSAL LOG ANTHOLOGY
Generated: {now}
Workspace: {ROOT}

Priority policy used:
1. No omission / no removal / no lossy summarization.
2. Causal and chronological ordering.
3. AI readability and manageable sectioning.
4. Human readability.

Important preservation rule:
Every source section below includes the full source payload between BEGIN_SOURCE_TEXT/END_SOURCE_TEXT, or base64 for binary payloads. Causal notes and episode titles are additive metadata only; they do not replace source content.

High-level causal order:
EP00: Manifest and source map.
EP01: Initial identity / memory-engine framing.
EP02: RP history and Soul/state seed material.
EP03: Main June 8 build log.
EP04: Slash command routing / command-channel correction.
EP05: Benchmark, evaluator, repair, and local-model hardening.
EP06: Manual/local LLM install and post-benchmark continuation.
EP07: UI handoff bundle and June 26-27 session export.
EP08: Extracted cleaned chat and causal chunks created by Codex.
EP99: Legacy user-made episode splits preserved as appendix.
"""
    parts.append(section_header("EP00 - ANTHOLOGY INTRO AND ORDER", OUT, "Generated metadata; not an original log.", intro.encode("utf-8")) + intro)

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    og = ROOT / "01_SOURCE_OG_LOGS" / "OG logs"
    add_file(parts, manifest, og / "AI-Memory-Engine-Design.txt", "EP01 - AI Memory Engine / Identity Framing", "Explicit message times begin 2026-05-28. This frames the project as local-first AI memory/state infrastructure.")
    add_file(parts, manifest, og / "mnemosyne start of a history.txt", "EP02 - Start Of History / RP Seed And Soul-State Material", "No explicit export timestamp in file, but filename and contents identify this as the narrative/state seed material that precedes or grounds the engineering work.")
    add_file(parts, manifest, og / "AI coding RP Narraitor web project complete log. do not read YOU DO NOT HAVE INFINTE TOEKNS - Mnemosyne AI Roleplay Engine_2026-06-08_09-44.txt", "EP03 - Main Build Log - Mnemosyne AI Roleplay Engine 2026-06-08 09:44", "Primary long coding/build transcript. Placed after project framing and seed state.")
    add_file(parts, manifest, og / "Slash-Command-Routing.txt", "EP04 - Slash Command Routing / Command Channel Correction", "Explicit message time begins 2026-06-08 10:56:49. Follows the main June 8 build log and focuses command routing/persona/state-channel corrections.")
    add_file(parts, manifest, og / "GPT chat session mk2.txt", "EP05A - GPT Catch-Up / Evaluator Architecture Status", "Catch-up log based on repository/chat history; placed before/alongside the Claude benchmark grind because it orients the state of evaluator/product hardening.")
    add_file(parts, manifest, og / "chatlog cluade that follows mk2.txt", "EP05B - Claude Benchmark / Evaluator / Repair Grind", "Claude follow-up log fixing AI-to-AI benchmark, evaluator reliability, repair, and local-model path.")
    add_file(parts, manifest, og / "Manual-LLM-Installation.txt", "EP06 - Manual LLM Installation / Local Repair Continuation", "Explicit message times span 2026-06-19 through 2026-06-23. Continues after benchmark/evaluator work toward local model repair runtime.")

    add_zip_contents(parts, manifest, og / "Mnemosyne_ AI roleplay state engine-handoff.zip", "EP07A - UI DESIGN HANDOFF ZIP", "Claude Design handoff bundle uploaded for the June 26 UI comparison thread.")
    add_zip_contents(parts, manifest, og / "session-export-1782538316039.zip", "EP07B - SESSION EXPORT ZIP", "Claude/Cowork session export for the June 26-27 UI overhaul failure thread. Full JSONL and app logs preserved.")

    extracted = ROOT / "02_DERIVED_EXTRACTED_CHATS" / "extracted_chats"
    add_file(parts, manifest, extracted / "handoff-bundle-notes.md", "EP08A - Codex Extracted Handoff Notes", "Codex-created note explaining the handoff bundle content.")
    add_file(parts, manifest, extracted / "c63174a8-f6b9-4999-8508-8a699d1dc0ab.chat.cleaned.jsonl", "EP08B - Cleaned Session Chat JSONL", "Codex-extracted human/assistant messages from session export. Preserved after raw zip contents as derived but useful reordered chat.")
    add_file(parts, manifest, extracted / "c63174a8-f6b9-4999-8508-8a699d1dc0ab.chat.md", "EP08C - Cleaned Session Chat Markdown", "Markdown rendering of the same extracted chat. Included because user requested extracted/reordered logs too; duplicate by design.")
    add_file(parts, manifest, extracted / "c63174a8-f6b9-4999-8508-8a699d1dc0ab.parse-errors.json", "EP08D - Parse Errors Record", "Parse-error record for the extraction.")

    causal = extracted / "causal_path"
    for path in sorted(causal.glob("*.md")):
        title = "EP08E - Codex Causal Chunk - " + path.name
        add_file(parts, manifest, path, title, "Codex-created causal reorder chunk. Included after raw/cleaned session to preserve the derived reading order.")

    legacy_dirs = [
        ROOT / "90_LEGACY_USER_EPISODE_SPLITS" / "Episode 1 Start of a hitory",
        ROOT / "90_LEGACY_USER_EPISODE_SPLITS" / "Episode 2 Bulding the base",
        ROOT / "90_LEGACY_USER_EPISODE_SPLITS" / "Episode 3 The grind that never ends",
    ]
    for legacy_dir in legacy_dirs:
        files = sorted(legacy_dir.glob("*.txt"), key=natural_part_key)
        for idx, path in enumerate(files, 1):
            add_file(
                parts,
                manifest,
                path,
                f"EP99 - LEGACY USER SPLIT APPENDIX - {legacy_dir.name} - {idx:03d} - {path.name}",
                "Legacy pre-existing episode split preserved verbatim. This may overlap with OG originals; kept for no-omission priority.",
            )

    manifest_bytes = json.dumps(manifest, ensure_ascii=False, indent=2).encode("utf-8")
    manifest_section = text_section("EP00B - COMPLETE SOURCE MANIFEST", MANIFEST, "Generated manifest of every included payload.", manifest_bytes, manifest_bytes.decode("utf-8"))
    parts.insert(1, manifest_section)

    OUT.write_text("".join(parts), encoding="utf-8", newline="\n")
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(OUT)
    print(MANIFEST)
    print(f"sections={len(manifest)}")
    print(f"bytes={OUT.stat().st_size}")


if __name__ == "__main__":
    main()
