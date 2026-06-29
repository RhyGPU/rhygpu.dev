import argparse
import json
import re
from pathlib import Path


INVALID_ESCAPE = re.compile(r'\\(?!["\\/bfnrtu])')


def load_jsonl_line(line: str):
    try:
        return json.loads(line)
    except json.JSONDecodeError:
        repaired = INVALID_ESCAPE.sub(r"\\\\", line)
        return json.loads(repaired)


def content_to_text(content):
    if isinstance(content, str):
        return content.strip()
    if not isinstance(content, list):
        return ""

    parts = []
    for item in content:
        if not isinstance(item, dict):
            continue
        if item.get("type") == "text":
            parts.append(str(item.get("text", "")))
    return "\n\n".join(part.strip() for part in parts if part and part.strip())


def is_human_message(obj):
    if obj.get("type") != "user":
        return False
    msg = obj.get("message") or {}
    content = msg.get("content")
    if isinstance(content, str):
        return True
    if isinstance(content, list):
        return any(isinstance(x, dict) and x.get("type") == "text" for x in content)
    return False


def is_assistant_text_message(obj):
    if obj.get("type") != "assistant":
        return False
    msg = obj.get("message") or {}
    return msg.get("role") == "assistant" and bool(content_to_text(msg.get("content")))


def extract(input_path: Path):
    records = []
    parse_errors = []
    seen = set()

    with input_path.open("r", encoding="utf-8", errors="replace") as fh:
        for line_no, line in enumerate(fh, 1):
            line = line.rstrip("\n")
            if not line:
                continue
            try:
                obj = load_jsonl_line(line)
            except Exception as exc:
                parse_errors.append({"line": line_no, "error": str(exc), "preview": line[:240]})
                continue

            role = None
            text = ""
            if is_human_message(obj):
                role = "user"
                text = content_to_text((obj.get("message") or {}).get("content"))
            elif is_assistant_text_message(obj):
                role = "assistant"
                text = content_to_text((obj.get("message") or {}).get("content"))

            if not role or not text:
                continue

            key = (obj.get("uuid"), role, text)
            if key in seen:
                continue
            seen.add(key)
            records.append(
                {
                    "line": line_no,
                    "timestamp": obj.get("timestamp"),
                    "role": role,
                    "uuid": obj.get("uuid"),
                    "parentUuid": obj.get("parentUuid"),
                    "sessionId": obj.get("sessionId"),
                    "text": text,
                }
            )

    return records, parse_errors


def write_markdown(records, parse_errors, input_path: Path, output_path: Path, missing_uuid: str):
    lines = [
        f"# Extracted chat: {input_path.stem}",
        "",
        f"- Source: `{input_path}`",
        f"- Messages extracted: {len(records)}",
        f"- Parse errors skipped: {len(parse_errors)}",
        f"- Requested UUID search: `{missing_uuid}` was not found in the provided zip files or workspace search.",
        "",
        "---",
        "",
    ]
    for i, rec in enumerate(records, 1):
        stamp = rec.get("timestamp") or "no timestamp"
        role = "USER" if rec["role"] == "user" else "ASSISTANT"
        lines.extend(
            [
                f"## {i}. {role} | {stamp}",
                "",
                f"`uuid: {rec.get('uuid')}`",
                "",
                rec["text"].strip(),
                "",
                "---",
                "",
            ]
        )

    if parse_errors:
        lines.extend(["# Skipped malformed JSONL lines", ""])
        for err in parse_errors[:50]:
            lines.append(f"- line {err['line']}: {err['error']} | `{err['preview']}`")
        if len(parse_errors) > 50:
            lines.append(f"- ... {len(parse_errors) - 50} more")
        lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--missing-uuid", default="019eff9c-e677-7f31-b539-48924bf74cb5")
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    records, parse_errors = extract(args.input)

    stem = args.input.stem
    md_path = args.output_dir / f"{stem}.chat.md"
    jsonl_path = args.output_dir / f"{stem}.chat.cleaned.jsonl"
    errors_path = args.output_dir / f"{stem}.parse-errors.json"

    write_markdown(records, parse_errors, args.input, md_path, args.missing_uuid)
    with jsonl_path.open("w", encoding="utf-8") as fh:
        for rec in records:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    errors_path.write_text(json.dumps(parse_errors, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"messages={len(records)}")
    print(f"errors={len(parse_errors)}")
    print(md_path)
    print(jsonl_path)
    print(errors_path)


if __name__ == "__main__":
    main()
