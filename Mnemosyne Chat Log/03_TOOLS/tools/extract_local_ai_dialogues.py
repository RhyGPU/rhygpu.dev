import argparse
import hashlib
import json
import ntpath
import os
import re
import subprocess
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


FENCE_START = re.compile(r"^\s*(`{3,}|~{3,})")
HTML_CODE = re.compile(r"<pre\b[^>]*>.*?</pre>", re.IGNORECASE | re.DOTALL)
INJECTED_BLOCK = re.compile(
    r"<(?P<tag>environment_context|recommended_plugins|system-reminder|"
    r"command-message|command-name|command-args|local-command-stdout|"
    r"ide_opened_file|task-notification|permissions instructions|app-context|"
    r"skills_instructions|plugins_instructions|apps_instructions|"
    r"collaboration_mode|multi_agent_mode)\b[^>]*>.*?</(?P=tag)>",
    re.IGNORECASE | re.DOTALL,
)
SPACE_RUN = re.compile(r"[ \t]+\n")
BLANK_RUN = re.compile(r"\n{3,}")
WINDOWS_BAD_FILENAME = re.compile(r"[<>:\"/\\|?*\x00-\x1f]")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Extract user/assistant dialogue from local Claude Code and Codex sessions."
    )
    parser.add_argument("--target", action="append", required=True, help="Project root to match")
    parser.add_argument(
        "--target-alias",
        action="append",
        default=[],
        metavar="CURRENT=LEGACY",
        help=(
            "Map a legacy session cwd to a current --target. Repeatable; "
            "example: D:\\repo=C:\\old\\repo"
        ),
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument(
        "--claude-root",
        type=Path,
        default=Path.home() / ".claude" / "projects",
    )
    parser.add_argument(
        "--codex-root",
        type=Path,
        default=Path.home() / ".codex" / "sessions",
    )
    parser.add_argument("--include-subagents", action="store_true")
    return parser.parse_args()


def windows_norm(value):
    if not value:
        return ""
    normalized = str(value).strip().replace("/", "\\")
    if normalized.startswith("\\\\?\\"):
        normalized = normalized[4:]
    if len(normalized) > 3:
        normalized = normalized.rstrip("\\")
    return ntpath.normcase(ntpath.normpath(normalized))


def is_within(path, root):
    path_norm = windows_norm(path)
    root_norm = windows_norm(root)
    if not path_norm or not root_norm:
        return False
    try:
        return ntpath.commonpath([path_norm, root_norm]) == root_norm
    except ValueError:
        return False


def safe_slug(value):
    value = WINDOWS_BAD_FILENAME.sub("_", str(value)).strip(" ._")
    value = re.sub(r"\s+", "_", value)
    return value or "project"


def normalized_remote(value):
    if not value:
        return ""
    value = str(value).strip().replace("\\", "/")
    match = re.match(r"git@([^:]+):(.+)$", value, re.IGNORECASE)
    if match:
        value = f"https://{match.group(1)}/{match.group(2)}"
    value = re.sub(r"^[a-z]+://", "", value, flags=re.IGNORECASE)
    value = value.rstrip("/")
    if value.lower().endswith(".git"):
        value = value[:-4]
    return value.casefold()


def git_value(cwd, *args):
    if not cwd or not Path(cwd).is_dir():
        return ""
    try:
        completed = subprocess.run(
            ["git", "-C", str(cwd), *args],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    if completed.returncode:
        return ""
    return completed.stdout.strip()


class TargetMatcher:
    def __init__(self, paths, aliases=()):
        self.targets = []
        self.cwd_cache = {}
        used_labels = Counter()
        for raw_path in paths:
            path = str(Path(raw_path))
            base_label = safe_slug(Path(path).name)
            used_labels[base_label] += 1
            label = base_label if used_labels[base_label] == 1 else f"{base_label}_{used_labels[base_label]}"
            common_dir = git_value(path, "rev-parse", "--path-format=absolute", "--git-common-dir")
            remote = git_value(path, "remote", "get-url", "origin")
            self.targets.append(
                {
                    "path": path,
                    "normalized_path": windows_norm(path),
                    "exists": Path(path).exists(),
                    "label": label,
                    "git_common_dir": windows_norm(common_dir),
                    "git_remote": normalized_remote(remote),
                    "aliases": [],
                }
            )
        self.targets.sort(key=lambda item: len(item["normalized_path"]), reverse=True)

        targets_by_path = {target["normalized_path"]: target for target in self.targets}
        for value in aliases:
            if "=" not in value:
                raise ValueError(
                    f"Invalid --target-alias {value!r}; expected CURRENT=LEGACY"
                )
            current, legacy = value.split("=", 1)
            target = targets_by_path.get(windows_norm(current))
            if target is None:
                raise ValueError(
                    f"Alias target {current!r} is not one of the supplied --target paths"
                )
            legacy_norm = windows_norm(legacy)
            if not legacy_norm:
                raise ValueError(f"Alias path is empty in {value!r}")
            target["aliases"].append(legacy_norm)

    def match(self, cwd, repository_url=""):
        cwd_key = windows_norm(cwd)
        remote_key = normalized_remote(repository_url)
        cache_key = (cwd_key, remote_key)
        if cache_key in self.cwd_cache:
            return self.cwd_cache[cache_key]

        match = None
        for target in self.targets:
            if is_within(cwd_key, target["normalized_path"]):
                match = target
                break
            if any(is_within(cwd_key, alias) for alias in target["aliases"]):
                match = target
                break

        if match is None and cwd and Path(cwd).is_dir():
            session_common_dir = windows_norm(
                git_value(cwd, "rev-parse", "--path-format=absolute", "--git-common-dir")
            )
            if session_common_dir:
                for target in self.targets:
                    if target["git_common_dir"] and (
                        session_common_dir == target["git_common_dir"]
                        or is_within(session_common_dir, target["git_common_dir"])
                    ):
                        match = target
                        break

        if match is None and remote_key:
            for target in self.targets:
                if target["git_remote"] and remote_key == target["git_remote"]:
                    match = target
                    break

        self.cwd_cache[cache_key] = match
        return match


def strip_fenced_code(text):
    output = []
    in_fence = False
    fence_char = ""
    placeholder_pending = False
    for line in text.splitlines():
        match = FENCE_START.match(line)
        if not in_fence and match:
            in_fence = True
            fence_char = match.group(1)[0]
            placeholder_pending = True
            continue
        if in_fence:
            if match and match.group(1)[0] == fence_char:
                in_fence = False
                if placeholder_pending:
                    output.append("[코드 블록 생략]")
                    placeholder_pending = False
            continue
        output.append(line)
    if placeholder_pending:
        output.append("[코드 블록 생략]")
    return "\n".join(output)


def strip_indented_code(text):
    lines = text.splitlines()
    output = []
    in_code = False
    previous_blank = True
    placeholder_pending = False
    for line in lines:
        is_indented = bool(re.match(r"^(?: {4}|\t)\S", line))
        if not in_code and previous_blank and is_indented:
            in_code = True
            placeholder_pending = True
            continue
        if in_code:
            if not line.strip() or is_indented:
                continue
            if placeholder_pending:
                output.append("[들여쓰기 코드 블록 생략]")
                placeholder_pending = False
            in_code = False
        output.append(line)
        previous_blank = not line.strip()
    if placeholder_pending:
        output.append("[들여쓰기 코드 블록 생략]")
    return "\n".join(output)


def clean_text(value, role):
    if not isinstance(value, str):
        return ""
    text = value.replace("\r\n", "\n").replace("\r", "\n")
    if role == "user":
        while True:
            cleaned = INJECTED_BLOCK.sub("", text)
            if cleaned == text:
                break
            text = cleaned
    text = HTML_CODE.sub("[HTML 코드 블록 생략]", text)
    text = strip_fenced_code(text)
    text = strip_indented_code(text)
    text = SPACE_RUN.sub("\n", text)
    text = BLANK_RUN.sub("\n\n", text).strip()
    if re.fullmatch(r"(?:\[(?:코드|HTML 코드|들여쓰기 코드) 블록 생략\]\s*)+", text):
        return ""
    return text


def content_text(content, allowed_types, role):
    if isinstance(content, str):
        return clean_text(content, role)
    if not isinstance(content, list):
        return ""
    parts = []
    for item in content:
        if not isinstance(item, dict) or item.get("type") not in allowed_types:
            continue
        value = item.get("text")
        cleaned = clean_text(value, role)
        if cleaned:
            parts.append(cleaned)
    return "\n\n".join(parts)


def iter_jsonl(path, parse_errors):
    try:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            for line_number, line in enumerate(handle, 1):
                line = line.rstrip("\r\n")
                if not line:
                    continue
                try:
                    yield line_number, json.loads(line)
                except json.JSONDecodeError as exc:
                    parse_errors.append(
                        {
                            "source": str(path),
                            "line": line_number,
                            "error": f"{exc.msg} at column {exc.colno}",
                        }
                    )
    except (OSError, UnicodeError) as exc:
        parse_errors.append({"source": str(path), "line": None, "error": str(exc)})


def looks_like_subagent(path, source=None, originator=""):
    path_parts = {part.casefold() for part in path.parts}
    if "subagents" in path_parts or path.name.casefold().startswith("agent-"):
        return True
    if "subagent" in str(originator).casefold():
        return True
    if isinstance(source, str):
        return "subagent" in source.casefold()
    if isinstance(source, dict):
        return any("subagent" in str(key).casefold() and bool(value) for key, value in source.items())
    return False


def deduplicate(messages):
    result = []
    seen = set()
    for message in messages:
        key = (message["role"], message["text"], message.get("phase"))
        if key in seen:
            continue
        seen.add(key)
        result.append(message)
    for index, message in enumerate(result, 1):
        message["sequence"] = index
    return result


def extract_claude(path, matcher, include_subagents, parse_errors):
    if not include_subagents and looks_like_subagent(path):
        return None
    records = []
    session_ids = Counter()
    target = None
    session_cwd = ""
    for line_number, obj in iter_jsonl(path, parse_errors):
        cwd = obj.get("cwd") or session_cwd
        if obj.get("cwd"):
            session_cwd = str(obj["cwd"])
        if target is None and cwd:
            target = matcher.match(cwd)
        session_id = obj.get("sessionId")
        if session_id:
            session_ids[str(session_id)] += 1
        if obj.get("isSidechain") or obj.get("isMeta"):
            continue
        record_type = obj.get("type")
        message = obj.get("message") or {}
        role = message.get("role") or record_type
        if record_type == "user" and role == "user":
            text = content_text(message.get("content"), {"text"}, "user")
        elif record_type == "assistant" and role == "assistant":
            text = content_text(message.get("content"), {"text"}, "assistant")
        else:
            continue
        if not text:
            continue
        records.append(
            {
                "line": line_number,
                "timestamp": obj.get("timestamp"),
                "role": role,
                "phase": None,
                "record_id": obj.get("uuid"),
                "parent_id": obj.get("parentUuid"),
                "text": text,
            }
        )
    if target is None or not records:
        return None
    session_id = session_ids.most_common(1)[0][0] if session_ids else path.stem
    return make_session("claude_code", path, session_id, session_cwd, target, records)


def extract_codex(path, matcher, include_subagents, parse_errors):
    response_records = []
    fallback_records = []
    target = None
    session_id = path.stem
    session_cwd = ""
    session_timestamp = None
    source = None
    originator = ""
    repository_url = ""
    for line_number, obj in iter_jsonl(path, parse_errors):
        record_type = obj.get("type")
        payload = obj.get("payload") or {}
        if record_type == "session_meta":
            session_id = str(payload.get("id") or session_id)
            session_cwd = str(payload.get("cwd") or "")
            session_timestamp = payload.get("timestamp") or obj.get("timestamp")
            source = payload.get("source")
            originator = str(payload.get("originator") or "")
            git_info = payload.get("git") or {}
            if isinstance(git_info, dict):
                repository_url = str(git_info.get("repository_url") or "")
            target = matcher.match(session_cwd, repository_url)
            continue
        if record_type == "response_item" and payload.get("type") == "message":
            role = payload.get("role")
            if role not in {"user", "assistant"}:
                continue
            allowed = {"input_text", "text"} if role == "user" else {"output_text", "text"}
            text = content_text(payload.get("content"), allowed, role)
            if not text:
                continue
            response_records.append(
                {
                    "line": line_number,
                    "timestamp": obj.get("timestamp"),
                    "role": role,
                    "phase": payload.get("phase"),
                    "record_id": payload.get("id"),
                    "parent_id": None,
                    "text": text,
                }
            )
            continue
        if record_type == "event_msg" and payload.get("type") in {"user_message", "agent_message"}:
            role = "user" if payload.get("type") == "user_message" else "assistant"
            raw_text = payload.get("message") or payload.get("text") or ""
            text = clean_text(raw_text, role)
            if text:
                fallback_records.append(
                    {
                        "line": line_number,
                        "timestamp": obj.get("timestamp"),
                        "role": role,
                        "phase": None,
                        "record_id": None,
                        "parent_id": None,
                        "text": text,
                    }
                )
    if not include_subagents and looks_like_subagent(path, source, originator):
        return None
    if target is None:
        target = matcher.match(session_cwd, repository_url)
    records = response_records or fallback_records
    if target is None or not records:
        return None
    return make_session(
        "codex", path, session_id, session_cwd, target, records, session_timestamp
    )


def make_session(product, path, session_id, cwd, target, records, session_timestamp=None):
    messages = deduplicate(records)
    timestamps = [item["timestamp"] for item in messages if item.get("timestamp")]
    started_at = session_timestamp or (timestamps[0] if timestamps else None)
    ended_at = timestamps[-1] if timestamps else started_at
    return {
        "product": product,
        "session_id": session_id,
        "source_path": str(path),
        "cwd": cwd,
        "target": target["path"],
        "target_label": target["label"],
        "started_at": started_at,
        "ended_at": ended_at,
        "messages": messages,
    }


def markdown_for_session(session):
    lines = [
        f"# {session['product']} dialogue — {session['session_id']}",
        "",
        f"- Project: `{session['target']}`",
        f"- Session cwd: `{session['cwd']}`",
        f"- Started: `{session.get('started_at') or 'unknown'}`",
        f"- Ended: `{session.get('ended_at') or 'unknown'}`",
        f"- Messages: {len(session['messages'])}",
        "- Filtering: user/assistant text only; tools, reasoning, system/developer messages, and code blocks omitted.",
        "",
        "---",
        "",
    ]
    for message in session["messages"]:
        role = message["role"].upper()
        stamp = message.get("timestamp") or "no timestamp"
        phase = f" | {message['phase']}" if message.get("phase") else ""
        lines.extend(
            [
                f"## {message['sequence']:04d}. {role} | {stamp}{phase}",
                "",
                message["text"],
                "",
                "---",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def write_outputs(output_dir, matcher, sessions, parse_errors, source_roots):
    output_dir.mkdir(parents=True, exist_ok=False)
    output_files = []
    flattened = []
    include_target_directory = len(matcher.targets) > 1
    sessions.sort(key=lambda item: (item.get("started_at") or "", item["product"], item["session_id"]))
    for session in sessions:
        started = (session.get("started_at") or "unknown")[:10].replace("-", "")
        relative = Path(session["product"]) / f"{started}_{safe_slug(session['session_id'])}.md"
        if include_target_directory:
            relative = Path(session["target_label"]) / relative
        destination = output_dir / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(markdown_for_session(session), encoding="utf-8")
        output_files.append(destination)
        session["output_path"] = str(relative)
        for message in session["messages"]:
            flattened.append(
                {
                    "product": session["product"],
                    "target": session["target"],
                    "session_id": session["session_id"],
                    "source_path": session["source_path"],
                    "cwd": session["cwd"],
                    **message,
                }
            )

    combined_lines = [
        "# Claude Code + Codex project dialogue export",
        "",
        f"- Sessions: {len(sessions)}",
        f"- Messages: {len(flattened)}",
        "- Scope: user/assistant dialogue only; code blocks and non-dialogue records omitted.",
        "",
    ]
    for session in sessions:
        combined_lines.extend(
            [
                "---",
                "",
                markdown_for_session(session),
                "",
            ]
        )
    combined_path = output_dir / "ALL_DIALOGUE.md"
    combined_path.write_text("\n".join(combined_lines).rstrip() + "\n", encoding="utf-8")
    output_files.append(combined_path)

    jsonl_path = output_dir / "dialogue.jsonl"
    with jsonl_path.open("w", encoding="utf-8") as handle:
        for message in flattened:
            handle.write(json.dumps(message, ensure_ascii=False) + "\n")
    output_files.append(jsonl_path)

    session_summary = []
    for session in sessions:
        session_summary.append(
            {
                key: session[key]
                for key in (
                    "product",
                    "session_id",
                    "source_path",
                    "cwd",
                    "target",
                    "target_label",
                    "started_at",
                    "ended_at",
                    "output_path",
                )
            }
            | {
                "message_count": len(session["messages"]),
                "role_counts": dict(Counter(item["role"] for item in session["messages"])),
            }
        )

    manifest = {
        "format_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_roots": source_roots,
        "targets": [
            {
                key: target[key]
                for key in (
                    "path",
                    "exists",
                    "label",
                    "git_common_dir",
                    "git_remote",
                    "aliases",
                )
            }
            for target in matcher.targets
        ],
        "filtering": {
            "included_roles": ["user", "assistant"],
            "excluded": [
                "system/developer messages",
                "reasoning/thinking",
                "tool calls and tool results",
                "terminal output",
                "attachments and images",
                "subagent and sidechain sessions",
                "fenced, HTML, and Markdown-indented code blocks",
                "known injected context blocks",
            ],
            "retained": ["inline identifiers and short inline code spans inside prose"],
        },
        "counts": {
            "sessions": len(sessions),
            "messages": len(flattened),
            "products": dict(Counter(item["product"] for item in sessions)),
            "targets": dict(Counter(item["target_label"] for item in sessions)),
            "roles": dict(Counter(item["role"] for item in flattened)),
            "parse_errors": len(parse_errors),
        },
        "sessions": session_summary,
        "parse_errors": parse_errors,
    }
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    output_files.append(manifest_path)

    fence_lines = 0
    for path in output_files:
        if path.suffix.lower() != ".md":
            continue
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            fence_lines += sum(1 for line in handle if FENCE_START.match(line))
    hashes = {}
    for path in output_files:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        hashes[str(path.relative_to(output_dir))] = digest
    verification_path = output_dir / "verification.txt"
    verification_path.write_text(
        "\n".join(
            [
                "Claude Code + Codex dialogue export verification",
                f"sessions={len(sessions)}",
                f"messages={len(flattened)}",
                f"parse_errors={len(parse_errors)}",
                f"markdown_fence_lines={fence_lines}",
                "sha256:",
                *[f"{digest}  {name}" for name, digest in sorted(hashes.items())],
                "",
            ]
        ),
        encoding="utf-8",
    )
    return manifest, verification_path


def main():
    args = parse_args()
    matcher = TargetMatcher(args.target, args.target_alias)
    parse_errors = []
    sessions = []

    if args.claude_root.is_dir():
        for path in sorted(args.claude_root.rglob("*.jsonl")):
            session = extract_claude(path, matcher, args.include_subagents, parse_errors)
            if session:
                sessions.append(session)
    if args.codex_root.is_dir():
        for path in sorted(args.codex_root.rglob("*.jsonl")):
            session = extract_codex(path, matcher, args.include_subagents, parse_errors)
            if session:
                sessions.append(session)

    manifest, verification_path = write_outputs(
        args.output_dir,
        matcher,
        sessions,
        parse_errors,
        {"claude_code": str(args.claude_root), "codex": str(args.codex_root)},
    )
    print(f"output={args.output_dir}")
    print(f"sessions={manifest['counts']['sessions']}")
    print(f"messages={manifest['counts']['messages']}")
    print(f"products={json.dumps(manifest['counts']['products'], ensure_ascii=False)}")
    print(f"targets={json.dumps(manifest['counts']['targets'], ensure_ascii=False)}")
    print(f"parse_errors={manifest['counts']['parse_errors']}")
    print(f"verification={verification_path}")


if __name__ == "__main__":
    main()
