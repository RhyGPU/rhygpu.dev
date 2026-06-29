import base64
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path


ROOT = Path(r"D:\정준화\rhygpu.dev\Mnemosyne Chat Log")
OUT_DIR = ROOT / "00_FINAL_DELIVERABLES"
ANTHOLOGY = OUT_DIR / "Mnemosyne_COMPLETE_CAUSAL_LOG_ANTHOLOGY.txt"
MANIFEST = OUT_DIR / "Mnemosyne_COMPLETE_CAUSAL_LOG_ANTHOLOGY.manifest.json"
REPORT = OUT_DIR / "Mnemosyne_COMPLETE_CAUSAL_LOG_ANTHOLOGY.verification.txt"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def anthology_payloads(text: str):
    pattern = re.compile(
        r"SECTION: (?P<section>.*?)\n"
        r"SOURCE: (?P<source>.*?)\n"
        r"BYTE_LENGTH: (?P<byte_length>.*?)\n"
        r"SHA256: (?P<sha256>[0-9a-fA-F]{64}|n/a)\n"
        r"CAUSAL_NOTE: (?P<note>.*?)\n"
        r"={96}\n\n"
        r"(?P<body>.*?)(?=\n\n={96}\nSECTION: |\Z)",
        re.S,
    )
    return [m.groupdict() for m in pattern.finditer(text)]


def extract_payload_bytes(payload: dict):
    body = payload["body"]
    if "BEGIN_SOURCE_TEXT\n" in body and "\nEND_SOURCE_TEXT" in body:
        inner = body.split("BEGIN_SOURCE_TEXT\n", 1)[1].rsplit("\nEND_SOURCE_TEXT", 1)[0]
        return inner.encode("utf-8")
    if "BEGIN_BASE64\n" in body and "\nEND_BASE64" in body:
        inner = body.split("BEGIN_BASE64\n", 1)[1].rsplit("\nEND_BASE64", 1)[0].strip()
        return base64.b64decode(inner)
    return None


def expected_root_payloads():
    expected = []
    og = ROOT / "01_SOURCE_OG_LOGS" / "OG logs"
    for path in [
        og / "AI-Memory-Engine-Design.txt",
        og / "mnemosyne start of a history.txt",
        og / "AI coding RP Narraitor web project complete log. do not read YOU DO NOT HAVE INFINTE TOEKNS - Mnemosyne AI Roleplay Engine_2026-06-08_09-44.txt",
        og / "Slash-Command-Routing.txt",
        og / "GPT chat session mk2.txt",
        og / "chatlog cluade that follows mk2.txt",
        og / "Manual-LLM-Installation.txt",
    ]:
        expected.append(str(path))

    extracted = ROOT / "02_DERIVED_EXTRACTED_CHATS" / "extracted_chats"
    for path in [
        extracted / "handoff-bundle-notes.md",
        extracted / "c63174a8-f6b9-4999-8508-8a699d1dc0ab.chat.cleaned.jsonl",
        extracted / "c63174a8-f6b9-4999-8508-8a699d1dc0ab.chat.md",
        extracted / "c63174a8-f6b9-4999-8508-8a699d1dc0ab.parse-errors.json",
    ]:
        expected.append(str(path))

    for path in sorted((extracted / "causal_path").glob("*.md")):
        expected.append(str(path))

    for legacy_dir in [
        ROOT / "90_LEGACY_USER_EPISODE_SPLITS" / "Episode 1 Start of a hitory",
        ROOT / "90_LEGACY_USER_EPISODE_SPLITS" / "Episode 2 Bulding the base",
        ROOT / "90_LEGACY_USER_EPISODE_SPLITS" / "Episode 3 The grind that never ends",
    ]:
        files = sorted(legacy_dir.glob("*.txt"), key=lambda p: natural_part_key(p.name))
        expected.extend(str(p) for p in files)

    return expected


def natural_part_key(name: str):
    match = re.search(r"(?:part_|_)(\d+)\.txt$", name)
    if match:
        return int(match.group(1))
    return name


def expected_zip_payloads():
    expected = []
    for zip_path in [
        ROOT / "01_SOURCE_OG_LOGS" / "OG logs" / "Mnemosyne_ AI roleplay state engine-handoff.zip",
        ROOT / "01_SOURCE_OG_LOGS" / "OG logs" / "session-export-1782538316039.zip",
    ]:
        expected.append(str(zip_path))
        expected.append(f"{zip_path}::INVENTORY")
        with zipfile.ZipFile(zip_path, "r") as zf:
            for info in zf.infolist():
                if not info.is_dir():
                    expected.append(f"{zip_path}::{info.filename}")
    return expected


def main():
    anthology_text = ANTHOLOGY.read_text(encoding="utf-8")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    payloads = anthology_payloads(anthology_text)

    lines = []
    errors = []
    warnings = []

    lines.append("MNEMOSYNE COMPLETE ANTHOLOGY VERIFICATION")
    lines.append(f"anthology: {ANTHOLOGY}")
    lines.append(f"manifest: {MANIFEST}")
    lines.append("")

    manifest_by_path = {m["path"]: m for m in manifest}
    source_payloads = [p for p in payloads if p["sha256"] != "n/a" and p["source"] in manifest_by_path]
    generated_payloads = [p for p in payloads if p["sha256"] != "n/a" and p["source"] not in manifest_by_path]
    lines.append(f"sections_in_txt_total: {len(payloads)}")
    lines.append(f"source_payload_sections_in_txt: {len(source_payloads)}")
    lines.append(f"generated_metadata_sections_in_txt: {len(generated_payloads)}")
    lines.append(f"manifest_entries: {len(manifest)}")

    if len(source_payloads) != len(manifest):
        errors.append(f"Manifest/source section count mismatch: txt={len(source_payloads)} manifest={len(manifest)}")

    payload_by_source = {p["source"]: p for p in source_payloads}

    expected = expected_root_payloads() + expected_zip_payloads()
    lines.append(f"expected_payloads: {len(expected)}")
    missing_expected = [p for p in expected if p not in manifest_by_path]
    if missing_expected:
        errors.append("Expected payloads missing from manifest:")
        errors.extend(f"  MISSING {p}" for p in missing_expected)

    missing_from_txt = [m["path"] for m in manifest if m["path"] not in payload_by_source]
    if missing_from_txt:
        errors.append("Manifest entries missing from anthology TXT sections:")
        errors.extend(f"  MISSING_IN_TXT {p}" for p in missing_from_txt)

    extra_manifest = [m["path"] for m in manifest if m["path"] not in expected]
    if extra_manifest:
        warnings.append("Manifest has extra generated/intentional entries beyond expected list:")
        warnings.extend(f"  EXTRA {p}" for p in extra_manifest)

    bad_header_hash = []
    bad_header_size = []
    bad_actual_hash = []
    bad_actual_size = []

    for m in manifest:
        p = payload_by_source.get(m["path"])
        if not p:
            continue
        if p["sha256"].lower() != m["sha256"].lower():
            bad_header_hash.append((m["path"], p["sha256"], m["sha256"]))
        if str(m["bytes"]) != str(p["byte_length"]):
            bad_header_size.append((m["path"], p["byte_length"], m["bytes"]))

        extracted = extract_payload_bytes(p)
        if extracted is None:
            # Intro is not in manifest. Every manifest source should have one of these markers.
            bad_actual_hash.append((m["path"], "NO_PAYLOAD_MARKERS", m["sha256"]))
            continue
        actual_size = len(extracted)
        actual_hash = sha256_bytes(extracted)

        # Text sections are re-encoded as UTF-8 after decode, so compare exact bytes only
        # for base64 binary payloads. For text payloads, header hash verifies original bytes.
        if "BEGIN_BASE64" in p["body"]:
            if actual_hash.lower() != m["sha256"].lower():
                bad_actual_hash.append((m["path"], actual_hash, m["sha256"]))
            if actual_size != m["bytes"]:
                bad_actual_size.append((m["path"], actual_size, m["bytes"]))

    if bad_header_hash:
        errors.append("Header hash mismatches against manifest:")
        errors.extend(f"  {p}: txt={a} manifest={b}" for p, a, b in bad_header_hash)
    if bad_header_size:
        errors.append("Header size mismatches against manifest:")
        errors.extend(f"  {p}: txt={a} manifest={b}" for p, a, b in bad_header_size)
    if bad_actual_hash:
        errors.append("Base64 payload hash/marker mismatches:")
        errors.extend(f"  {p}: actual={a} manifest={b}" for p, a, b in bad_actual_hash)
    if bad_actual_size:
        errors.append("Base64 payload size mismatches:")
        errors.extend(f"  {p}: actual={a} manifest={b}" for p, a, b in bad_actual_size)

    zip_checks = []
    for zip_path in [
        ROOT / "01_SOURCE_OG_LOGS" / "OG logs" / "Mnemosyne_ AI roleplay state engine-handoff.zip",
        ROOT / "01_SOURCE_OG_LOGS" / "OG logs" / "session-export-1782538316039.zip",
    ]:
        with zipfile.ZipFile(zip_path, "r") as zf:
            entries = [info for info in zf.infolist() if not info.is_dir()]
            included = [f"{zip_path}::{info.filename}" in manifest_by_path for info in entries]
            zip_checks.append((str(zip_path), len(entries), sum(included)))
            if not all(included):
                errors.append(f"Zip entry missing for {zip_path}")
                for info, ok in zip(entries, included):
                    if not ok:
                        errors.append(f"  MISSING_ZIP_ENTRY {info.filename}")

    lines.append("")
    lines.append("ZIP ENTRY CHECKS")
    for z, total, included in zip_checks:
        lines.append(f"{z}: entries={total}, included={included}")

    lines.append("")
    lines.append("KIND COUNTS")
    counts = {}
    for m in manifest:
        counts[m["kind"]] = counts.get(m["kind"], 0) + 1
    for kind, count in sorted(counts.items()):
        lines.append(f"{kind}: {count}")

    lines.append("")
    if warnings:
        lines.append("WARNINGS")
        lines.extend(warnings)
        lines.append("")

    if errors:
        lines.append("RESULT: FAIL")
        lines.extend(errors)
    else:
        lines.append("RESULT: PASS")
        lines.append("No expected source payloads are missing from the manifest or anthology TXT.")
        lines.append("All manifest hashes/sizes match anthology section headers.")
        lines.append("All zip entries are represented.")
        lines.append("Base64 binary payloads decode to the manifest hash and byte length.")

    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(REPORT)
    print(lines[-5:] if len(lines) > 5 else lines)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
