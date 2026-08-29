#!/usr/bin/env python3
"""Build a project-separated, deduplicated, chronological devlog source corpus.

The raw archives are deliberately left untouched.  This script creates one
canonical working set for devlog writing, records every duplicate decision,
and merges forked conversations without repeating their common prefix.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import shutil
import sys
import zipfile
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable


ROOT = Path(r"D:\정준화")
EXPORT = ROOT / "AI_SESSION_EXPORTS"
DATED = EXPORT / "2026-08-29"
SOURCE = EXPORT / "SOURCE_LOGS"
SUPPORT_SOURCE = EXPORT / "SUPPORTING_EVIDENCE"
OUT = EXPORT / "DEVLOG_SOURCE"
MN_LOG = ROOT / "rhygpu.dev" / "Mnemosyne Chat Log"
OG = MN_LOG / "01_SOURCE_OG_LOGS" / "OG logs"
DERIVED = MN_LOG / "02_DERIVED_EXTRACTED_CHATS"
RHY_CHAT = ROOT / "rhygpu.dev" / "rhygpu.dev chat log"
DOWNLOADS = Path(r"C:\Users\T-ROBOTICS\Downloads")
CROSS_PROJECT_CLAUDE = Path(
    r"C:\Users\T-ROBOTICS\.claude\projects\C--Users-T-ROBOTICS\085e9948-a3a3-46a3-bd45-f2031fe0ca87.jsonl"
)
SECURITY_LICENSE_SESSION_ID = "019dd69e-ec3b-74a0-b19d-c652aa484d25"
KST = timezone(timedelta(hours=9))


LOCAL_SESSION_OVERRIDES = {
    "019c450e-9c65-7021-8295-45b4ba605016": (
        "개인 플래너 비전 정립과 초기 코드 진단·핵심 버그 수정",
        "옛 `Desktop\\Planner` 작업 경로에서 복구한 OmniPlanner 최초 확인 대화. 저장소 첫 커밋(2/25)보다 15일 앞선다.",
    ),
    "019dfc35-2717-7772-be80-3257d1b68ac2": (
        "Windows 실행·바로가기·시작 지연 문제 정리",
        "옛 Downloads 작업 복사본 경로에서 복구한 OmniPlanner 세션.",
    ),
    "019dfc61-794d-7870-b12f-eb5e1fb924c1": (
        "기능을 유지한 OmniPlanner 중복 코드 정리",
        "옛 Downloads 작업 복사본 경로에서 복구한 OmniPlanner 세션.",
    ),
    "019dd35a-600b-7012-ae76-b4e4052f624a": (
        "Blueprint에서 Tauri MVP·첫 동작 프로토타입까지",
        "옛 `New project 2` 작업 경로에서 복구한 Mnemosyne 최초 구현 세션. 4/28~4/30 초기 커밋 구간을 직접 설명한다.",
    ),
    "019dfbbb-ff7c-7941-bdc3-4de3ee0a957c": (
        "Context Compiler V2·즉시 연속성·Payload Inspector",
        "옛 Downloads 작업 경로에서 복구한 Mnemosyne 세션.",
    ),
    "019e0018-544b-7080-9f60-d1c4a4aaf3a9": (
        "LLM payload 중복 제거와 연속성 파이프라인 안정화",
        "옛 Downloads 작업 경로에서 복구한 Mnemosyne 장기 세션.",
    ),
    "019e39a4-3673-7f23-8e34-b5774effe6a5": (
        "Image Asset Layer와 채팅 이미지 기반 확장",
        "옛 Downloads 작업 경로에서 복구한 Mnemosyne 장기 세션.",
    ),
    "019e4abc-3e86-72c1-b15a-bab261c6d1f0": (
        "Restore Hygiene·Meta No-op·중복 메시지 방지",
        "옛 Downloads 작업 경로에서 복구한 Mnemosyne 세션.",
    ),
    "019e4d07-923d-7581-a954-e6fefbb68fe9": (
        "Rubric 기반 Memory·State Evaluator V1",
        "옛 Downloads 작업 경로에서 복구한 Mnemosyne 세션.",
    ),
    "019e4fa1-a55d-7a12-a1e5-d8c0c7a4fc28": (
        "Evaluator schema 정규화와 anti-replay 안정화",
        "옛 Downloads 작업 경로에서 복구한 Mnemosyne 세션.",
    ),
    "019eb6b6-8893-7f93-a804-1687d8ac3afa": (
        "Schema-enforced evaluator·tool-calling 전환",
        "옛 Downloads 작업 경로에서 복구한 Mnemosyne 세션.",
    ),
    "019ed323-3485-7352-899f-38f3f851dad5": (
        "가짜 benchmark를 Visible AI-vs-AI Chat으로 교체",
        "옛 Downloads 작업 경로에서 복구한 Mnemosyne 세션.",
    ),
}


@dataclass
class Record:
    project: str
    title: str
    provider: str
    start: datetime | None
    end: datetime | None
    text: str
    sources: list[str]
    note: str = ""
    slug: str = "session"
    output_name: str = ""
    sha256: str = ""


@dataclass
class Message:
    role: str
    content: str
    when: datetime | None
    order: int
    sources: set[str] = field(default_factory=set)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def strip_fenced_code(text: str) -> str:
    pattern = re.compile(r"(?ms)^[ \t]*```[^\n]*\n.*?^[ \t]*```[ \t]*\r?\n?")
    previous = None
    while previous != text:
        previous = text
        text = pattern.sub("[코드 블록 생략]\n", text)
    # Some legacy exports contain orphan closing fences or malformed nested
    # fences.  Their boundaries cannot be recovered reliably; remove the
    # residual markers so they cannot create accidental Markdown code blocks.
    text = re.sub(r"(?m)^[ \t]*```[^\n]*$", "[깨진 코드 경계 생략]", text)
    return text.replace("\r\n", "\n").replace("\r", "\n").strip() + "\n"


def safe_slug(text: str) -> str:
    text = re.sub(r"[^0-9A-Za-z가-힣._-]+", "-", text).strip("-._")
    return text[:90] or "session"


def parse_iso(value: str) -> datetime:
    value = value.strip().replace("Z", "+00:00")
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=KST)
    return parsed.astimezone(KST)


def parse_local(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S").replace(tzinfo=KST)


def first_user_preview(text: str) -> str:
    patterns = [
        r"(?ms)^## 0001\. USER[^\n]*\n\s*(.*?)(?=\n---\n|\Z)",
        r"(?ms)^# you asked\s*(.*?)(?=^# chatgpt response|\Z)",
        r"(?ms)^\*\*You:\*\*\s*(.*?)(?=^\* \* \*|^\*\*ChatGPT:\*\*|\Z)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            value = re.sub(r"(?m)^(?:message time:.*|---\s*)$", "", match.group(1))
            value = re.sub(r"\s+", " ", value).strip()
            return value[:120] + ("…" if len(value) > 120 else "")
    return ""


def local_session_record(project: str, path: Path) -> Record:
    text = read_text(path)
    started = re.search(r"(?m)^- Started: `([^`]+)`", text)
    ended = re.search(r"(?m)^- Ended: `([^`]+)`", text)
    if not started or not ended:
        raise ValueError(f"Missing session times: {path}")
    provider = "Claude Code" if "claude_code" in path.parts else "Codex"
    preview = first_user_preview(text)
    title = preview or path.stem
    record = Record(
        project=project,
        title=title,
        provider=provider,
        start=parse_iso(started.group(1)),
        end=parse_iso(ended.group(1)),
        text=text,
        sources=[str(path)],
        slug=f"{provider.lower().replace(' ', '-')}-{path.stem.split('_', 1)[-1][:8]}",
    )
    for session_id, (override_title, override_note) in LOCAL_SESSION_OVERRIDES.items():
        if session_id in path.name:
            record.title = override_title
            record.note = override_note
            record.slug = safe_slug(override_title)
            break
    return record


def chatgpt_record(project: str, path: Path, title: str, note: str = "") -> Record:
    text = read_text(path)
    times = re.findall(r"(?m)^message time:\s*(20\d{2}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", text)
    if not times:
        raise ValueError(f"Missing ChatGPT timestamps: {path}")
    return Record(
        project=project,
        title=title,
        provider="ChatGPT",
        start=parse_local(times[0]),
        end=parse_local(times[-1]),
        text=text,
        sources=[str(path)],
        note=note,
        slug=safe_slug(title),
    )


def legacy_record(
    project: str,
    path: Path,
    title: str,
    provider: str,
    start: datetime | None,
    end: datetime | None,
    note: str,
) -> Record:
    return Record(
        project=project,
        title=title,
        provider=provider,
        start=start,
        end=end,
        text=read_text(path),
        sources=[str(path)],
        note=note,
        slug=safe_slug(title),
    )


def parse_extracted_messages(path: Path) -> list[Message]:
    text = read_text(path)
    pattern = re.compile(
        r"(?ms)^## \d+\. (USER|ASSISTANT) \| ([^\r\n|]+?)(?: \|[^\r\n]*)?\r?\n\r?\n"
        r"(.*?)(?=\r?\n---\r?\n|\Z)"
    )
    messages: list[Message] = []
    occurrence: defaultdict[tuple[str, str], int] = defaultdict(int)
    for order, match in enumerate(pattern.finditer(text)):
        role = match.group(1)
        content = strip_fenced_code(match.group(3)).strip()
        signature = (role, re.sub(r"\s+", " ", content))
        occurrence[signature] += 1
        messages.append(
            Message(
                role=role,
                content=content,
                when=parse_iso(match.group(2).strip()),
                order=order,
                sources={path.stem},
            )
        )
    return messages


def parse_chatgpt_messages(path: Path) -> list[Message]:
    text = read_text(path)
    block = re.compile(
        r"(?ms)^# (you asked|chatgpt response)\s*(.*?)(?=^# (?:you asked|chatgpt response)|\Z)"
    )
    messages: list[Message] = []
    last_user_time: datetime | None = None
    local_order = 0
    for match in block.finditer(text):
        role = "USER" if match.group(1) == "you asked" else "ASSISTANT"
        raw = match.group(2)
        time_match = re.search(
            r"(?m)^message time:\s*(20\d{2}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", raw
        )
        if time_match:
            when = parse_local(time_match.group(1))
            last_user_time = when
            local_order = 0
        else:
            local_order += 1
            when = last_user_time + timedelta(microseconds=local_order) if last_user_time else None
        raw = re.sub(r"(?m)^(?:message time:.*|---\s*)$", "", raw)
        messages.append(
            Message(
                role=role,
                content=strip_fenced_code(raw).strip(),
                when=when,
                order=len(messages),
                sources={path.stem},
            )
        )
    return messages


def merge_message_forks(
    project: str,
    paths: list[Path],
    parser,
    title: str,
    provider: str,
    preferred: Path,
    note: str,
) -> Record:
    merged: dict[tuple[str, str, int], Message] = {}
    occurrence_by_source: dict[str, defaultdict[tuple[str, str], int]] = {}
    for path in paths:
        occurrence: defaultdict[tuple[str, str], int] = defaultdict(int)
        occurrence_by_source[path.stem] = occurrence
        for message in parser(path):
            normalized = re.sub(r"\s+", " ", message.content).strip()
            base = (message.role, normalized)
            occurrence[base] += 1
            key = (message.role, normalized, occurrence[base])
            if key in merged:
                merged[key].sources.update(message.sources)
                if merged[key].when is None and message.when is not None:
                    merged[key].when = message.when
            else:
                merged[key] = message

    preferred_stem = preferred.stem
    ordered = sorted(
        merged.values(),
        key=lambda m: (
            m.when or datetime.max.replace(tzinfo=KST),
            0 if preferred_stem in m.sources else 1,
            m.order,
        ),
    )
    start = min(m.when for m in ordered if m.when is not None)
    end = max(m.when for m in ordered if m.when is not None)
    all_sources = {path.stem for path in paths}
    lines = [
        f"# {title}",
        "",
        f"- Provider: `{provider}`",
        f"- Preferred/latest branch: `{preferred.stem}`",
        f"- Forks merged: {len(paths)}",
        f"- Unique dialogue messages after common-prefix deduplication: {len(ordered)}",
        "- Filtering: user/assistant dialogue only; fenced code blocks omitted.",
        "",
        "---",
        "",
    ]
    for index, message in enumerate(ordered, 1):
        when = message.when.isoformat() if message.when else "time-unknown"
        subset = message.sources != all_sources
        branch = f" | sources: {', '.join(sorted(message.sources))}" if subset else ""
        lines.extend(
            [
                f"## {index:04d}. {message.role} | {when}{branch}",
                "",
                message.content,
                "",
                "---",
                "",
            ]
        )
    return Record(
        project=project,
        title=title,
        provider=provider,
        start=start,
        end=end,
        text="\n".join(lines),
        sources=[str(path) for path in paths],
        note=note,
        slug=safe_slug(title),
    )


def canonical_header(record: Record) -> str:
    start = record.start.isoformat() if record.start else "unknown"
    end = record.end.isoformat() if record.end else "unknown"
    sources = "\n".join(f"  - `{source}`" for source in record.sources)
    note = f"\n- Note: {record.note}" if record.note else ""
    return (
        "<!-- canonical-devlog-source -->\n"
        f"# Canonical source: {record.title}\n\n"
        f"- Project: `{record.project}`\n"
        f"- Provider: `{record.provider}`\n"
        f"- Start (KST): `{start}`\n"
        f"- End (KST): `{end}`{note}\n"
        "- Raw source(s):\n"
        f"{sources}\n\n---\n\n"
    )


def write_record(record: Record, directory: Path, index: int) -> None:
    if record.start:
        stamp = record.start.strftime("%Y-%m-%d_%H%M")
        prefix = f"{index:03d}_{stamp}"
    else:
        prefix = f"{index:03d}_UNDATED"
    filename = f"{prefix}__{safe_slug(record.slug)}.md"
    body = canonical_header(record) + strip_fenced_code(record.text)
    target = directory / "sessions" / filename
    target.write_text(body, encoding="utf-8", newline="\n")
    record.output_name = f"sessions/{filename}"
    record.sha256 = hashlib.sha256(body.encode("utf-8")).hexdigest()


def fmt_time(value: datetime | None) -> str:
    return value.strftime("%Y-%m-%d %H:%M") if value else "정확한 시각 없음"


def relative_record_link(record: Record) -> str:
    prefix = "../" if record.output_name.startswith("shared_sessions/") else ""
    return f"{prefix}{record.output_name}".replace(" ", "%20")


def user_events(record: Record) -> list[tuple[datetime, str]]:
    events: list[tuple[datetime, str]] = []
    extracted = re.compile(
        r"(?ms)^## \d+\. USER \| ([^\r\n|]+?)(?: \|[^\r\n]*)?\r?\n\r?\n"
        r"(.*?)(?=\r?\n---\r?\n|\Z)"
    )
    for match in extracted.finditer(record.text):
        try:
            when = parse_iso(match.group(1).strip())
        except ValueError:
            continue
        preview = re.sub(r"\s+", " ", match.group(2)).strip()
        events.append((when, preview[:180] + ("…" if len(preview) > 180 else "")))
    if events:
        return events

    chatgpt = re.compile(
        r"(?ms)^# you asked\s*\n+message time:\s*"
        r"(20\d{2}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s*\n+"
        r"(.*?)(?=\n---\s*\n+# chatgpt response|\Z)"
    )
    for match in chatgpt.finditer(record.text):
        preview = re.sub(r"\s+", " ", match.group(2)).strip()
        events.append(
            (
                parse_local(match.group(1)),
                preview[:180] + ("…" if len(preview) > 180 else ""),
            )
        )
    return events


def timed_dialogue(record: Record) -> list[Message]:
    extracted = re.compile(
        r"(?ms)^## \d+\. (USER|ASSISTANT) \| ([^\r\n|]+?)(?: \|[^\r\n]*)?\r?\n\r?\n"
        r"(.*?)(?=\r?\n---\r?\n|\Z)"
    )
    messages: list[Message] = []
    for order, match in enumerate(extracted.finditer(record.text)):
        try:
            when = parse_iso(match.group(2).strip())
        except ValueError:
            continue
        messages.append(
            Message(
                role=match.group(1),
                content=strip_fenced_code(match.group(3)).strip(),
                when=when,
                order=order,
                sources={record.output_name},
            )
        )
    if messages:
        return messages

    block = re.compile(
        r"(?ms)^# (you asked|chatgpt response)\s*(.*?)(?=^# (?:you asked|chatgpt response)|\Z)"
    )
    last_user_time: datetime | None = None
    response_order = 0
    for order, match in enumerate(block.finditer(record.text)):
        role = "USER" if match.group(1) == "you asked" else "ASSISTANT"
        raw = match.group(2)
        time_match = re.search(
            r"(?m)^message time:\s*(20\d{2}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", raw
        )
        if time_match:
            when = parse_local(time_match.group(1))
            last_user_time = when
            response_order = 0
        elif last_user_time:
            response_order += 1
            when = last_user_time + timedelta(microseconds=response_order)
        else:
            continue
        raw = re.sub(r"(?m)^(?:message time:.*|---\s*)$", "", raw)
        messages.append(
            Message(
                role=role,
                content=strip_fenced_code(raw).strip(),
                when=when,
                order=order,
                sources={record.output_name},
            )
        )
    return messages


def quote_markdown(text: str) -> str:
    return "\n".join(f"> {line}" if line else ">" for line in text.splitlines())


def write_full_dialogue(
    project: str, records: list[Record], shared_records: Iterable[Record] = ()
) -> dict:
    all_records = [*records, *shared_records]
    timed: list[tuple[datetime, Record, Message]] = []
    session_only: list[Record] = []
    duplicate_messages = 0
    seen: set[tuple[str, str, str]] = set()
    for record in all_records:
        messages = timed_dialogue(record)
        if not messages:
            session_only.append(record)
            continue
        for message in messages:
            normalized = re.sub(r"\s+", " ", message.content).strip()
            key = (message.role, message.when.isoformat(), normalized)
            if key in seen:
                duplicate_messages += 1
                continue
            seen.add(key)
            timed.append((message.when, record, message))
    timed.sort(key=lambda item: (item[0], item[2].order, item[1].title))
    session_only.sort(
        key=lambda record: (
            record.start is not None,
            record.start or datetime.min.replace(tzinfo=KST),
        )
    )

    lines = [
        f"# {project} — full chronological dialogue",
        "",
        "devlog 작성용 단일 읽기 뷰다. 정본은 `sessions/`와 `../shared_sessions/`에 한 번만 있으며, 이 파일은 프로젝트 안의 모든 정본 대화를 메시지 시각순으로 펼친 파생 합본이다.",
        "메시지별 시각이 없는 장기 원본은 맨 앞의 `Session-level sources`에 세션 단위로 보존한다.",
        "",
        f"- Timed dialogue messages: **{len(timed)}**",
        f"- Session-level sources without message timestamps: **{len(session_only)}**",
        f"- Exact duplicate messages removed while combining: **{duplicate_messages}**",
        "- Timezone: **Asia/Seoul (UTC+9)**",
        "- Code policy: fenced code blocks omitted.",
        "",
    ]

    if session_only:
        lines.extend(["## Session-level sources", ""])
        for index, record in enumerate(session_only, 1):
            span = fmt_time(record.start)
            if record.end and record.start and record.end != record.start:
                span += f" → {fmt_time(record.end)}"
            lines.extend(
                [
                    f"### S{index:03d}. [{record.title}]({relative_record_link(record)})",
                    "",
                    f"- Time: {span}",
                    f"- Provider: {record.provider}",
                    f"- Note: {record.note or '메시지별 시각 없음'}",
                    "",
                    quote_markdown(record.text.strip()),
                    "",
                ]
            )

    lines.extend(["## Message-level timeline", ""])
    current_day = None
    for when, record, message in timed:
        day = when.strftime("%Y-%m-%d")
        if day != current_day:
            lines.extend([f"## {day}", ""])
            current_day = day
        lines.extend(
            [
                f"### {when.strftime('%H:%M:%S')} · {message.role} · [{record.title}]({relative_record_link(record)})",
                "",
                quote_markdown(message.content),
                "",
            ]
        )
    target = OUT / project / "FULL_DIALOGUE_CHRONOLOGICAL.md"
    target.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8", newline="\n")
    return {
        "output": str(target),
        "timed_messages": len(timed),
        "session_only_sources": len(session_only),
        "exact_duplicates_removed": duplicate_messages,
    }


def write_message_timeline(
    project: str, records: list[Record], shared_records: Iterable[Record] = ()
) -> None:
    directory = OUT / project
    entries: list[tuple[datetime, Record, str]] = []
    no_message_times: list[Record] = []
    for record in [*records, *shared_records]:
        found = user_events(record)
        if not found:
            no_message_times.append(record)
        for when, preview in found:
            entries.append((when, record, preview))
    entries.sort(key=lambda item: item[0])
    lines = [
        f"# {project} — message-level chronological index",
        "",
        "프로젝트 내부의 시각이 확인되는 **사용자 발화**를 KST 기준으로 교차 정렬했다. 장기 ChatGPT 대화와 동시에 진행된 Codex/Claude 세션도 여기서는 실제 시각대로 섞인다.",
        "본문을 복제하지 않고 해당 canonical 세션으로 링크한다.",
        "",
        f"- Timed user messages: **{len(entries)}**",
        f"- Session-only records without per-message timestamps: **{len(no_message_times)}**",
        "",
        "## Timeline",
        "",
    ]
    current_date = None
    for when, record, preview in entries:
        day = when.strftime("%Y-%m-%d")
        if day != current_date:
            lines.extend([f"### {day}", ""])
            current_date = day
        link = relative_record_link(record)
        lines.append(f"- **{when.strftime('%H:%M:%S')}** — [{preview}]({link})")
    if no_message_times:
        lines.extend(["", "## Session-only / exact message times unavailable", ""])
        for record in no_message_times:
            link = relative_record_link(record)
            lines.append(f"- [{record.title}]({link}) — {record.note or '메시지별 시각 없음'}")
    (directory / "MESSAGE_TIMELINE.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8", newline="\n"
    )


def write_gap_report(project: str) -> None:
    reports = {
        "OmniPlanner": """# OmniPlanner — remaining source/devlog gaps

> 범위: 대화·문서가 devlog 서술을 얼마나 뒷받침하는지만 본다. 최신 버전, 제품 완성도, 릴리스 준비도, WIP 여부는 판정하지 않는다.

## 판정

- **최초 대화를 찾음.** 2026-02-10 `Desktop\\Planner` Codex 세션에 “개인 planner + iCalendar + todo + self goals + email”이라는 시작 비전, 기존 코드 진단, 수정 요청, 초기 버그가 있다. Git 첫 커밋(2/25)보다 15일 이르다.
- 4/29 보안·AGPL 공용 세션, 5/6 실행/바로가기/시작 지연 및 중복 정리 세션, 7월 작업 세션과 8/29 교차 감사도 복구됐다.
- **남은 직접 대화 밀도 공백은 2/11~4/28.** 이 기간의 개발 사실은 Git과 기존 `DEVLOG.md`에 상세하지만, 매 커밋 당시 질문·판단 대화가 연속적으로 남아 있지는 않다.
- 기존 `DEVLOG.md`는 “Phase 0–1: 2/25 repository”부터 시작한다. 새 devlog 000은 2/10 원시 대화를 앞에 놓아 제품 발상과 저장소 생성 사이를 연결했다.
- 새 `작업-체크리스트-안내`가 v4.0 실기 검증과 v4.1(custom alarms, missions, Smart Snooze)을 보강했다.
- 7/5 후반 커밋의 직접 대화가 없어도 Git·문서로 복원 가능하다. 이는 WIP/최신성 문제가 아니라 직접 인용 가능한 대화 근거의 차이일 뿐이다.

## Devlog 작성 우선순위

1. **000–025 작성 완료:** 2/10 원시 대화부터 7/5 v4.2 Pulse clock/focus suite까지 시간순으로 서술. 001–014·017 전반부·018–022·024–025는 Git·문서 복원, 000·015·016·017 후반부·023은 직접 대화 근거를 본문에서 구분했다.
2. v4.1–v4.2 직접 실기 gate는 최종 통과 기록이 없으므로 이후 증거에서 재확인.
3. 이후 남은 July implementation/history를 커밋과 대화 기준으로 계속 복원.
""",
        "between_dawns": """# between_dawns — remaining source/devlog gaps

> 범위: 대화·문서가 devlog 서술을 얼마나 뒷받침하는지만 본다. 최신 버전, 제품 완성도, 릴리스 준비도, WIP 여부는 판정하지 않는다.

## 판정

- **아이디어 생성 공백은 해결됨.** `컨트롤러-협동게임-추천`에 8/23 16시경 Dead Town 후속작 발상, 18:26 v0.1 문서 생성, 18:52 v0.2 갱신, 18:57 `BETWEEN DAWNS` 명명이 모두 있다.
- 이후 Codex 구현 2세션, Claude 네 분기의 공통-prefix 제거 통합본, 저장소 생성, 8/29 교차 검증·커밋 세션까지 이어진다.
- Git 3커밋(8/26 initial, 8/29 district, 8/29 M1)은 위 기록으로 모두 설명 가능하다. 현재 확인된 중대한 원시 대화 공백은 없다.
- **000–003 작성 완료.** 발상부터 Godot 전환, v0.3 감사, 절차적 district·M1 출발선·8/29 검증 커밋까지 현재 확보된 전체 개발 시간선을 공개 devlog로 옮겼다.

## Devlog 작성 우선순위

- 현재 확보된 직접 대화·Git 범위의 Between Dawns devlog 000–003은 작성 완료.
- 다음 글은 M1 잔여 7건(물리 소음·전투 피드백 등)의 실제 구현 대화나 커밋이 추가될 때 이어간다.
""",
        "mnemosyne": """# mnemosyne — remaining source/devlog gaps

> 범위: 대화·문서가 devlog 서술을 얼마나 뒷받침하는지만 본다. 최신 버전, 제품 완성도, 릴리스 준비도, WIP 여부는 판정하지 않는다.

## 판정

- 발상 원본, 릴리스 전략, Soul, memory/search, slash routing, evaluator/benchmark, UI overhaul, local LLM, Memory Compiler V2, 8/29 교차 감사까지 가장 풍부하다.
- 동일 ChatGPT URL의 구버전 `.txt`는 더 긴 `.md`로 교체했고, Slash 분기는 공통 52메시지를 제거하면서 고유 4메시지를 보존했다.
- **초기 구현 대화가 이미 있었고 재추출됐다.** 4/28~4/30 Codex 세션 1개(260개 user/assistant 발화)가 Blueprint 전달, Tauri scaffold, mock provider, delete controls, narrator 정렬, native build, diagnostics까지 초기 커밋 흐름을 직접 설명한다.
- 기존 `mnemosyne start of a history.txt`도 단순 pre-repo 발상만이 아니라 이름·제품 구조·MVP 계획과 초기 구현 점검까지 이어진다. 단, 이 ChatGPT 파일은 메시지별 시각이 없어 4/28 Codex 세션보다 앞선 설계 원본으로만 배치하고 정확한 날짜는 만들지 않는다.
- Git에도 5/1~5/5 커밋이 없고 5/4 recovery 세션이 다음 흐름을 잇는다. 따라서 종전에 적은 “4/28~5/3 초기 구현 공백”은 철회한다.
- 5/6~6/19의 누락됐던 Context Compiler, continuity, image layer, restore hygiene, evaluator, tool-calling, visible benchmark Codex 세션도 복구됐다. devlog를 쓸 원자료 밀도는 충분하다.
- 공개 devlog 000–010 이후 시점의 글이 아직 적다는 것은 **작성 범위 표시**일 뿐, 프로젝트나 로그가 미완성이라는 판정이 아니다.

## Devlog 작성 우선순위

1. 초기편: undated ChatGPT 설계 원본 → 4/28~4/30 실제 Codex 구현 → 5/4 recovery를 연결.
2. Context Priority Stack·Payload Inspector·evaluator 전환을 5/6 이후 시간순으로 작성.
3. visible AI benchmark의 blocking→실제 채팅 파이프라인 전환과 실패 복구.
4. UI 전면 재설계의 성공·실패 양쪽 기록.
5. DB/SQL+semantic retrieval 선행 결정에서 Memory Compiler V2까지 연결.
""",
        "rhygpu.dev": """# rhygpu.dev — remaining source/devlog gaps

> 범위: 대화·문서가 devlog 서술을 얼마나 뒷받침하는지만 본다. 최신 버전, 제품 완성도, 릴리스 준비도, WIP 여부는 판정하지 않는다.

## 판정

- 사이트 탄생(도메인·Cloudflare·첫 구조), devlog 작성, GitHub 로그 비교, Astro 포트폴리오 엔진, 프로젝트 증거·이미지·분석까지 원시 대화가 이어져 **핵심 source gap은 작다.**
- 8/29 교차 프로젝트 Claude 세션이 mobile tap 이후 미커밋 변경 검증과 최신 에셋 커밋까지 보강한다.
- 현재 site journal은 `site-000`(7/1), `site-001`(7/4) 두 편뿐이다. 7/4 PWA/SEO, 8/26 mobile tap targets, 8/29 icon source assets, GitHub/Cloudflare 분석은 후속 journal이 없다.
- 프로젝트 목록에는 Mnemosyne·OmniPlanner·Pythagorean Harmony·rhygpu.dev만 있고 **Between Dawns 페이지가 아직 없다.**
- OmniPlanner 페이지도 현대 프로젝트별 devlog 링크가 없어, 기존 `devlog-omni.html` 회고가 새 journal 구조와 분리돼 있다.

## Devlog 작성 우선순위

1. site-002: PWA/SEO·프로젝트 아이콘·증거 이미지.
2. site-003: 모바일 tap target과 실기 QA.
3. site-004: 아이콘 원본/에셋 보존과 포트폴리오 proof 정책.
4. Between Dawns 프로젝트 페이지 및 devlog route 추가.
5. OmniPlanner 기존 회고를 현재 프로젝트별 journal 구조에 연결.
""",
    }
    (OUT / project / "GAPS.md").write_text(
        reports[project].strip() + "\n", encoding="utf-8", newline="\n"
    )


def build_records() -> tuple[dict[str, list[Record]], dict[str, list[str]]]:
    records: dict[str, list[Record]] = defaultdict(list)
    duplicates: dict[str, list[str]] = defaultdict(list)

    # Local Codex/Claude sessions.  The four Between Dawns Claude forks are
    # merged below; the administrative extraction session is audit-only.
    for project in ("OmniPlanner", "between_dawns", "mnemosyne", "rhygpu.dev"):
        root = DATED / project
        for path in root.glob("*/*.md"):
            if project == "between_dawns" and path.parent.name == "claude_code":
                continue
            if SECURITY_LICENSE_SESSION_ID in path.name:
                duplicates[project].append(
                    f"공용 이동: `{path}` — OmniPlanner와 Mnemosyne에 걸친 보안 점검·AGPL 정리 세션이라 `shared_sessions/`에 한 번만 보존."
                )
                continue
            if path.name.startswith("20260828_01a04940"):
                duplicates[project].append(
                    f"제외(관리 작업): `{path}` — 프로젝트 개발이 아니라 세션 추출·정리 대화."
                )
                continue
            records[project].append(local_session_record(project, path))

    claude_paths = sorted((DATED / "between_dawns" / "claude_code").glob("*.md"))
    preferred = next(path for path in claude_paths if "7f828e43" in path.name)
    records["between_dawns"].append(
        merge_message_forks(
            "between_dawns",
            claude_paths,
            parse_extracted_messages,
            "v0.3 평가에서 v0.4·월드 구조까지 이어진 Claude 분기 통합",
            "Claude Code",
            preferred,
            "동일한 146개 메시지까지 공유한 네 분기를 한 번만 수록하고, 각 분기의 고유 발화는 실제 시각순으로 보존.",
        )
    )
    duplicates["between_dawns"].append(
        "통합: Claude Code 11b24157 / 2396ef50 / 7f828e43 / 9d56f9f6 — 공통 prefix는 1회만, 7f828e43을 최신 주분기로 삼고 나머지 고유 메시지는 병합."
    )

    # Downloaded ChatGPT conversations.
    records["OmniPlanner"].append(
        chatgpt_record(
            "OmniPlanner",
            SOURCE / "OmniPlanner" / "작업-체크리스트-안내.md",
            "v4.0·v4.1 작업 체크리스트와 실기 검증",
        )
    )
    records["between_dawns"].append(
        chatgpt_record(
            "between_dawns",
            SOURCE / "between_dawns" / "컨트롤러-협동게임-추천.md",
            "컨트롤러 게임 탐색에서 Between Dawns 발상·명명·시스템 설계까지",
            "Between Dawns의 직접적인 아이디어 생성 기록. 18:26 v0.1 문서 생성, 18:52 v0.2 갱신, 18:57 BETWEEN DAWNS 명명까지 모두 포함.",
        )
    )
    for filename, title in (
        ("Test-Release-Strategy.md", "알파 테스트·릴리스 전략과 오류 복구"),
        ("Soul-Configuration-Update.md", "F.R.E.Y.A Soul 설정 갱신"),
        ("AI-Memory-Engine-Design.md", "AI 기억 엔진 설계와 사용자 철학 정리"),
        ("Manual-LLM-Installation.md", "수동 LLM 설치와 로컬 모델 운용"),
    ):
        records["mnemosyne"].append(
            chatgpt_record("mnemosyne", SOURCE / "mnemosyne" / filename, title)
        )

    slash_paths = [
        SOURCE / "mnemosyne" / "Slash-Command-Routing.md",
        SOURCE / "mnemosyne" / "브랜치-·-Slash-Command-Routing.md",
    ]
    records["mnemosyne"].append(
        merge_message_forks(
            "mnemosyne",
            slash_paths,
            parse_chatgpt_messages,
            "Slash Command Routing 본선과 분기 통합",
            "ChatGPT",
            slash_paths[0],
            "52개 공통 메시지는 한 번만 수록하고, 비용·dual-pass 논의로 갈라진 분기의 4개 고유 메시지를 보존.",
        )
    )
    duplicates["mnemosyne"].append(
        "통합: `Slash-Command-Routing.md` + `브랜치-·-Slash-Command-Routing.md` — 52개 공통 메시지 제거, 두 분기의 고유 대화 유지."
    )

    db_path = SOURCE / "mnemosyne" / "DB-y-SQL.md"
    if db_path.exists():
        records["mnemosyne"].append(
            chatgpt_record(
                "mnemosyne",
                db_path,
                "SQL·구조 검색·벡터 검색을 결합한 응답 전 컨텍스트 조회",
                "일반 SQL 질문이 아니라 Mnemosyne의 branch-safe retrieval/RAG 선행 설계.",
            )
        )

    # Mnemosyne's unique legacy/raw source conversations.
    records["mnemosyne"].append(
        legacy_record(
            "mnemosyne",
            OG / "mnemosyne start of a history.txt",
            "Himari RP 문제에서 Mnemosyne 설계·초기 구현 핸드오프까지",
            "ChatGPT",
            None,
            None,
            "메시지 시각은 없지만 저장소 전 발상에서 이름·제품 구조·MVP 설계와 초기 구현 점검까지 이어진다. 4/28 Codex 구현 세션에 전달된 설계의 선행 원본이라 맨 앞에 두되, 전체가 pre-repo라고 간주하지 않는다.",
        )
    )
    big_name = (
        "AI coding RP Narraitor web project complete log. do not read YOU DO NOT HAVE "
        "INFINTE TOEKNS - Mnemosyne AI Roleplay Engine_2026-06-08_09-44.txt"
    )
    records["mnemosyne"].append(
        legacy_record(
            "mnemosyne",
            OG / big_name,
            "Mnemosyne 제품·아키텍처·구현 장기 대화",
            "ChatGPT",
            parse_local("2026-06-08 09:44:00"),
            parse_local("2026-06-22 09:34:36"),
            "시작은 파일명, 종료 상한은 원본 보존 시각 기준. 본문에 메시지별 시각이 없어 세션 단위 정렬만 가능.",
        )
    )
    records["mnemosyne"].append(
        legacy_record(
            "mnemosyne",
            OG / "GPT chat session mk2.txt",
            "GitHub 로그에서 재개한 Mk2 진단·evaluator hardening",
            "ChatGPT",
            parse_local("2026-06-08 11:05:18"),
            parse_local("2026-06-19 10:47:36"),
            "본문의 Unix 타임스탬프 최소·최대값을 KST로 변환해 범위를 산정.",
        )
    )
    records["mnemosyne"].append(
        legacy_record(
            "mnemosyne",
            OG / "chatlog cluade that follows mk2.txt",
            "Visible AI benchmark를 실제 채팅 파이프라인으로 고친 Claude 세션",
            "Claude Code",
            parse_local("2026-06-17 16:17:52"),
            parse_local("2026-06-17 18:16:52"),
            "본문의 benchmark export Unix 타임스탬프를 KST로 변환.",
        )
    )
    extracted_ui = (
        DERIVED
        / "extracted_chats"
        / "c63174a8-f6b9-4999-8508-8a699d1dc0ab.chat.md"
    )
    records["mnemosyne"].append(
        legacy_record(
            "mnemosyne",
            extracted_ui,
            "Claude UI 비교·전면 재설계 세션",
            "Claude Cowork",
            parse_iso("2026-06-26T14:44:04.740Z"),
            parse_iso("2026-06-27T05:31:42.690Z"),
            "session-export ZIP의 151개 user/assistant 메시지를 파싱 오류 0건으로 추출한 대표본.",
        )
    )

    # rhygpu.dev main sources.
    records["rhygpu.dev"].append(
        chatgpt_record(
            "rhygpu.dev",
            SOURCE / "rhygpu.dev" / "Devlog-creation-from-roadmaps.md",
            "로드맵에서 devlog를 만들고 rhygpu.dev를 시작한 장기 대화",
        )
    )
    github_zip = SOURCE / "rhygpu.dev" / "GitHub-Log-Comparison.zip"
    with zipfile.ZipFile(github_zip) as archive:
        github_text = archive.read("GitHub-Log-Comparison.md").decode("utf-8-sig", errors="replace")
    times = re.findall(
        r"(?m)^message time:\s*(20\d{2}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", github_text
    )
    records["rhygpu.dev"].append(
        Record(
            project="rhygpu.dev",
            title="GitHub 로그 비교에서 포트폴리오 구조·증거·분석까지",
            provider="ChatGPT",
            start=parse_local(times[0]),
            end=parse_local(times[-1]),
            text=github_text,
            sources=[f"{github_zip}!/GitHub-Log-Comparison.md"],
            note="ZIP의 이미지 3개는 supporting_evidence로 별도 추출; 대화 대표본은 ZIP 내부의 더 긴 Markdown.",
            slug="GitHub-Log-Comparison",
        )
    )
    records["rhygpu.dev"].append(
        legacy_record(
            "rhygpu.dev",
            RHY_CHAT / "rhygpu.dev build session_2026-07-01.txt",
            "Astro 포트폴리오·프로젝트별 devlog 엔진 구축 세션",
            "Claude Code",
            parse_local("2026-07-01 00:00:00"),
            parse_local("2026-07-01 23:59:59"),
            "원문은 날짜만 제공하므로 해당 날짜 내부 순서는 파일의 발화 순서를 유지.",
        )
    )

    # Same-conversation newer/full exports supersede the old text versions.
    duplicate_pairs = {
        "mnemosyne": [
            (OG / "AI-Memory-Engine-Design.txt", SOURCE / "mnemosyne" / "AI-Memory-Engine-Design.md"),
            (OG / "Manual-LLM-Installation.txt", SOURCE / "mnemosyne" / "Manual-LLM-Installation.md"),
            (OG / "Slash-Command-Routing.txt", SOURCE / "mnemosyne" / "Slash-Command-Routing.md"),
        ],
        "rhygpu.dev": [
            (RHY_CHAT / "Devlog-creation-from-roadmaps.txt", SOURCE / "rhygpu.dev" / "Devlog-creation-from-roadmaps.md"),
            (RHY_CHAT / "GitHub-Log-Comparison.txt", Path(f"{github_zip}!/GitHub-Log-Comparison.md")),
        ],
    }
    for project, pairs in duplicate_pairs.items():
        for old, new in pairs:
            duplicates[project].append(
                f"대표본 교체: `{old}` → `{new}` — 같은 ChatGPT conversation URL/시작시각이며 새 Markdown가 더 길고 후속 대화·서식을 더 보존."
            )

    # Generated/derived sets are not independent source conversations.
    for project in records:
        duplicates[project].append(
            "대표 후보에서 제외: `ALL_DIALOGUE.md`, `dialogue.jsonl`, `90_LEGACY_USER_EPISODE_SPLITS`, `80_WORKING_EXTRACTS` — 원본 대화에서 생성된 합본·분할·작업 파일."
        )
    duplicates["mnemosyne"].extend(
        [
            "대표 후보에서 제외: `Mnemosyne_ AI roleplay state engine-handoff.zip` — README·HTML·JS 디자인 번들이며 대화 없음.",
            "대표본 교체: `session-export-1782538316039.zip`의 원시 로그 → `c63174a8-...chat.md` — 151개 대화, parse error 0인 추출본.",
        ]
    )
    return records, duplicates


def write_supporting() -> list[dict[str, str]]:
    support_dir = OUT / "between_dawns" / "supporting_evidence"
    support_dir.mkdir(parents=True, exist_ok=True)
    items: list[dict[str, str]] = []
    mappings = [
        (
            SUPPORT_SOURCE / "between_dawns" / "ComfyUI-6800-XT-모델.md",
            "2026-06-28_to_2026-07-17__ComfyUI-AMD-visual-pipeline.md",
            "간접 연관: Between Dawns 이전의 game-dev PC·다크 판타지·콘티/캐릭터/배경 제작 파이프라인 연구. 본문에 Between Dawns 명칭은 없어 메인 원인 시간선에서는 제외.",
        ),
        (
            SUPPORT_SOURCE / "between_dawns" / "8월 연장근무.md",
            "2026-08__session-audit-evidence.md",
            "감사 근거: `D------between-dawns` 171건(8/24 15:39~8/28 10:08)을 개인 프로젝트로 분리했다는 증거. 개발 대화가 아니므로 메인 시간선에서는 제외.",
        ),
    ]
    for source, filename, reason in mappings:
        if not source.exists():
            continue
        text = strip_fenced_code(read_text(source))
        target = support_dir / filename
        target.write_text(
            "<!-- supporting-evidence -->\n"
            f"# {source.stem}\n\n- Raw source: `{source}`\n- Classification: {reason}\n\n---\n\n"
            + text,
            encoding="utf-8",
            newline="\n",
        )
        items.append({"source": str(source), "output": str(target), "reason": reason})

    github_zip = SOURCE / "rhygpu.dev" / "GitHub-Log-Comparison.zip"
    image_dir = OUT / "rhygpu.dev" / "supporting_evidence" / "GitHub-Log-Comparison-images"
    image_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(github_zip) as archive:
        for name in sorted(n for n in archive.namelist() if n.lower().endswith((".jpg", ".png", ".webp"))):
            target = image_dir / Path(name).name
            target.write_bytes(archive.read(name))
            items.append(
                {
                    "source": f"{github_zip}!/{name}",
                    "output": str(target),
                    "reason": "GitHub-Log-Comparison 대화에 첨부된 시각 증거.",
                }
            )
    return items


def write_existing_devlogs() -> dict[str, list[dict]]:
    site_devlogs = ROOT / "rhygpu.dev" / "src" / "content" / "devlogs"
    selected = {
        "OmniPlanner": [ROOT / "OmniPlanner" / "DEVLOG.md"]
        + sorted(site_devlogs.glob("omni-*.md")),
        "between_dawns": sorted(site_devlogs.glob("between-*.md")),
        "mnemosyne": sorted(
            path
            for path in site_devlogs.glob("*.md")
            if re.match(r"^\d{3}-", path.name)
        ),
        "rhygpu.dev": sorted(site_devlogs.glob("site-*.md")),
    }
    excluded = {
        "OmniPlanner": [
            f"`{ROOT / 'OmniPlanner' / 'devlog' / 'index.html'}` — DEVLOG.md의 렌더링/배포본이라 작업 정본에서 제외.",
            f"`{ROOT / 'rhygpu.dev' / 'devlog-omni.html'}` — 이전 HTML 게시본; 편집 가능한 최신 DEVLOG.md를 정본으로 선택.",
        ],
        "between_dawns": ["현대 content collection의 `between-*` Markdown만 정본으로 선택."],
        "mnemosyne": [
            f"`{ROOT / 'mnemosyne' / 'devlog-000.html'}` — 000의 이전 HTML 사본.",
            f"`{ROOT / 'rhygpu.dev' / 'devlog-000.html'}` ~ `devlog-006.html` — 현대 Markdown 000~006의 이전 HTML 게시본.",
        ],
        "rhygpu.dev": ["현대 content collection의 `site-*` Markdown만 정본으로 선택."],
    }
    result: dict[str, list[dict]] = {}
    for project, sources in selected.items():
        directory = OUT / project / "existing_devlogs"
        directory.mkdir(parents=True, exist_ok=True)
        items: list[dict] = []
        hashes: set[str] = set()
        for source in sources:
            source_digest = hashlib.sha256(source.read_bytes()).hexdigest()
            if source_digest in hashes:
                continue
            hashes.add(source_digest)
            target = directory / source.name
            raw = read_text(source)
            cleaned = strip_fenced_code(raw)
            target.write_text(cleaned, encoding="utf-8", newline="\n")
            items.append(
                {
                    "source": str(source),
                    "output": str(target),
                    "source_sha256": source_digest,
                    "sha256": hashlib.sha256(cleaned.encode("utf-8")).hexdigest(),
                    "code_blocks_omitted": raw != cleaned,
                }
            )
        lines = [
            f"# {project} — existing devlog canon",
            "",
            "이미 작성된 devlog 가운데 편집 가능한 정본만 이 폴더에 모았다. HTML 렌더링본과 이전 사본은 중복 판정만 기록하고 복사하지 않았으며, 코드 블록은 대화 corpus 정책에 맞춰 생략했다.",
            "",
            f"- Selected files: **{len(items)}**",
            "",
            "## Selected",
            "",
        ]
        if items:
            for item in items:
                name = Path(item["output"]).name
                lines.append(f"- [{name}]({name.replace(' ', '%20')}) — `{item['source']}`")
        else:
            lines.append("- 없음")
        lines.extend(["", "## Duplicate/version decisions", ""])
        lines.extend(f"- {decision}" for decision in excluded[project])
        (directory / "INDEX.md").write_text(
            "\n".join(lines).rstrip() + "\n", encoding="utf-8", newline="\n"
        )
        result[project] = items
    return result


def write_source_map(
    records: dict[str, list[Record]],
    shared_sessions: list[tuple[Record, list[str]]],
) -> None:
    lines = [
        "# Canonical source map",
        "",
        "정리 후 devlog 작성에는 이 `DEVLOG_SOURCE` 트리만 사용하면 된다. 아래 원본은 출처 검증용이며 앱 소유 세션과 보존 아카이브를 이동하거나 복제하지 않았다.",
        "",
    ]
    for project in ("OmniPlanner", "between_dawns", "mnemosyne", "rhygpu.dev"):
        lines.extend([f"## {project}", ""])
        seen: set[str] = set()
        for record in records[project]:
            for source in record.sources:
                if source in seen:
                    continue
                seen.add(source)
                lines.append(f"- `{source}`")
        lines.append("")
    lines.extend(["## Shared sessions", ""])
    for record, projects in shared_sessions:
        lines.append(f"- {record.title} ({', '.join(projects)})")
        lines.extend(f"  - `{source}`" for source in record.sources)
    (OUT / "SOURCE_MAP.md").write_text(
        "\n".join(lines).rstrip() + "\n", encoding="utf-8", newline="\n"
    )


def write_master_index(
    records: dict[str, list[Record]],
    shared_sessions: list[tuple[Record, list[str]]],
    full_dialogue: dict[str, dict],
    existing_devlogs: dict[str, list[dict]],
) -> None:
    lines = [
        "# Devlog source master index",
        "",
        "이 파일이 전체 작업 진입점이다. 프로젝트별 `FULL_DIALOGUE_CHRONOLOGICAL.md`에서 전체 대화를 시간순으로 읽고, `existing_devlogs/`에서 이미 쓴 글을 대조하면 된다.",
        "",
        "| Project | Project canon | Shared refs | Timed messages | Existing devlogs | Working files |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for project in ("OmniPlanner", "between_dawns", "mnemosyne", "rhygpu.dev"):
        shared_count = sum(1 for _, projects in shared_sessions if project in projects)
        stats = full_dialogue[project]
        lines.append(
            f"| {project} | {len(records[project])} | {shared_count} | "
            f"{stats['timed_messages']} | {len(existing_devlogs[project])} | "
            f"[full log]({project}/FULL_DIALOGUE_CHRONOLOGICAL.md) · "
            f"[timeline]({project}/TIMELINE.md) · "
            f"[written]({project}/existing_devlogs/INDEX.md) · "
            f"[gaps]({project}/GAPS.md) |"
        )
    lines.extend(
        [
            "",
            "## Layout",
            "",
            "- `PROJECT/FULL_DIALOGUE_CHRONOLOGICAL.md`: 프로젝트 전체 대화 단일 시간순 읽기본.",
            "- `PROJECT/sessions/`: 중복 제거된 개별 정본.",
            "- `PROJECT/existing_devlogs/`: 이미 작성된 devlog 정본만 모은 폴더.",
            "- `shared_sessions/`: 여러 프로젝트를 다룬 원본을 한 번만 저장.",
            "- `SOURCE_MAP.md`: 원시 Claude/Codex/ChatGPT 파일 출처.",
            "",
        ]
    )
    (OUT / "MASTER_INDEX.md").write_text(
        "\n".join(lines), encoding="utf-8", newline="\n"
    )


def build_cross_project_record() -> Record:
    extractor_path = MN_LOG / "03_TOOLS" / "tools" / "extract_local_ai_dialogues.py"
    spec = importlib.util.spec_from_file_location("local_dialogue_extractor", extractor_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load extractor: {extractor_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    parse_errors: list[dict] = []
    matcher = module.TargetMatcher([r"C:\Users\T-ROBOTICS"])
    session = module.extract_claude(CROSS_PROJECT_CLAUDE, matcher, False, parse_errors)
    if session is None or parse_errors:
        raise RuntimeError(f"Cross-project Claude extraction failed: {parse_errors}")
    return Record(
        project="OmniPlanner + between_dawns + mnemosyne + rhygpu.dev",
        title="네 프로젝트 미커밋 변경 검증·수정·커밋·푸시",
        provider="Claude Code",
        start=parse_iso(session["started_at"]),
        end=parse_iso(session["ended_at"]),
        text=module.markdown_for_session(session),
        sources=[str(CROSS_PROJECT_CLAUDE)],
        note="CWD가 사용자 홈이라 프로젝트 경로 기반 1차 추출에서 누락됐던 교차 프로젝트 유지보수 세션.",
        slug="four-project-git-audit-fix-and-push",
    )


def build_security_license_record() -> Record:
    paths = list((DATED / "mnemosyne" / "codex").glob(f"*{SECURITY_LICENSE_SESSION_ID}*.md"))
    if len(paths) != 1:
        raise RuntimeError(
            f"Expected one security/license session for {SECURITY_LICENSE_SESSION_ID}, found {paths}"
        )
    record = local_session_record("OmniPlanner + mnemosyne", paths[0])
    record.title = "공개 전 저장소 보안 점검과 AGPL 라이선스 정리"
    record.note = (
        "옛 Mnemosyne 작업 경로에서 시작했지만 모든 당시 저장소를 검사하고 "
        "OmniPlanner 라이선스도 수정한 공용 세션. 본문은 한 번만 저장하고 두 프로젝트에서 참조."
    )
    record.slug = "repo-security-and-agpl-license-audit"
    return record


def write_shared_record(record: Record) -> None:
    directory = OUT / "shared_sessions"
    directory.mkdir(parents=True, exist_ok=True)
    stamp = record.start.strftime("%Y-%m-%d_%H%M") if record.start else "UNDATED"
    filename = f"{stamp}__{record.slug}.md"
    body = canonical_header(record) + strip_fenced_code(record.text)
    target = directory / filename
    target.write_text(body, encoding="utf-8", newline="\n")
    record.output_name = f"shared_sessions/{filename}"
    record.sha256 = hashlib.sha256(body.encode("utf-8")).hexdigest()


def write_project(
    project: str,
    records: list[Record],
    decisions: list[str],
    shared_records: Iterable[Record] = (),
) -> None:
    directory = OUT / project
    (directory / "sessions").mkdir(parents=True, exist_ok=True)
    records.sort(key=lambda r: (r.start is not None, r.start or datetime.min.replace(tzinfo=KST)))
    for index, record in enumerate(records, 1):
        write_record(record, directory, index)

    hashes: defaultdict[str, list[Record]] = defaultdict(list)
    for record in records:
        hashes[record.sha256].append(record)
    collisions = {key: values for key, values in hashes.items() if len(values) > 1}
    if collisions:
        raise RuntimeError(f"Canonical duplicate remained in {project}: {collisions}")

    shared_records = list(shared_records)
    ordered_records = sorted(
        [*records, *shared_records],
        key=lambda r: (r.start is not None, r.start or datetime.min.replace(tzinfo=KST)),
    )
    timeline = [
        f"# {project} — devlog source timeline",
        "",
        "이 폴더는 다른 프로젝트와 섞지 않고, 이 프로젝트 내부 기록만 시작 시각(KST) 기준으로 정렬했다.",
        "동일 대화의 구버전·공통 prefix·파생 합본은 제외했으며 판정 근거는 `DUPLICATE_DECISIONS.md`에 있다.",
        "",
        f"- Canonical project sessions: **{len(records)}**",
        f"- Shared sessions referenced without copying: **{len(shared_records)}**",
        "- Ordering timezone: **Asia/Seoul (UTC+9)**",
        "- Code policy: fenced code blocks omitted; user/assistant prose retained.",
        "",
        "## Ordered sources",
        "",
    ]
    shared_ids = {id(record) for record in shared_records}
    for index, record in enumerate(ordered_records, 1):
        span = fmt_time(record.start)
        if record.end and record.start and record.end != record.start:
            span += f" → {fmt_time(record.end)}"
        timeline.extend(
            [
                f"### {index:03d}. [{record.title}]({relative_record_link(record)})",
                "",
                f"- Time: {span} KST" if record.start else f"- Time: {span}",
                f"- Provider: {record.provider}",
                "- Storage: 공용 원본 링크(본문 중복 없음)."
                if id(record) in shared_ids
                else "- Storage: 이 프로젝트 canonical 본문.",
                f"- Note: {record.note}" if record.note else "- Note: 독립 원본 대화",
                "",
            ]
        )
    (directory / "TIMELINE.md").write_text("\n".join(timeline), encoding="utf-8", newline="\n")

    duplicate_text = [
        f"# {project} — duplicate and version decisions",
        "",
        "원시 자료는 증거 보존을 위해 삭제하지 않았다. 아래 항목은 canonical devlog 작업 세트에서만 제거·통합됐다.",
        "",
    ]
    duplicate_text.extend(f"- {decision}" for decision in decisions)
    (directory / "DUPLICATE_DECISIONS.md").write_text(
        "\n".join(duplicate_text) + "\n", encoding="utf-8", newline="\n"
    )


def main() -> None:
    rebuild = "--rebuild" in sys.argv[1:]
    if OUT.exists() and any(OUT.iterdir()):
        marker = OUT / "README.md"
        safe_target = OUT.resolve() == (EXPORT / "DEVLOG_SOURCE").resolve()
        generated = marker.exists() and marker.read_text(encoding="utf-8").startswith(
            "# Project-separated canonical devlog sources"
        )
        if not rebuild or not safe_target or not generated:
            raise SystemExit(f"Refusing to overwrite existing non-empty canonical corpus: {OUT}")
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True, exist_ok=True)
    records, decisions = build_records()
    shared_sessions = [
        (build_security_license_record(), ["OmniPlanner", "mnemosyne"]),
        (
            build_cross_project_record(),
            ["OmniPlanner", "between_dawns", "mnemosyne", "rhygpu.dev"],
        ),
    ]
    shared_sessions.sort(
        key=lambda item: (
            item[0].start is not None,
            item[0].start or datetime.min.replace(tzinfo=KST),
        )
    )
    for record, _ in shared_sessions:
        write_shared_record(record)
    full_dialogue: dict[str, dict] = {}
    for project in ("OmniPlanner", "between_dawns", "mnemosyne", "rhygpu.dev"):
        references = [record for record, projects in shared_sessions if project in projects]
        write_project(project, records[project], decisions[project], references)
        write_message_timeline(project, records[project], references)
        full_dialogue[project] = write_full_dialogue(
            project, records[project], references
        )
        write_gap_report(project)
    existing_devlogs = write_existing_devlogs()
    write_source_map(records, shared_sessions)
    write_master_index(records, shared_sessions, full_dialogue, existing_devlogs)
    support = write_supporting()

    manifest = {
        "created_at": datetime.now(KST).isoformat(),
        "timezone": "Asia/Seoul",
        "policy": {
            "project_separation": True,
            "ordering": "within each project by canonical session start time",
            "raw_archives_modified": False,
            "fenced_code_blocks_omitted": True,
            "fork_policy": "common prefix once; unique branch messages retained",
        },
        "projects": {
            project: [
                {
                    "order": index,
                    "title": record.title,
                    "provider": record.provider,
                    "start_kst": record.start.isoformat() if record.start else None,
                    "end_kst": record.end.isoformat() if record.end else None,
                    "output": str(OUT / project / record.output_name),
                    "sha256": record.sha256,
                    "sources": record.sources,
                    "note": record.note,
                }
                for index, record in enumerate(records[project], 1)
            ]
            for project in records
        },
        "full_dialogue_views": full_dialogue,
        "existing_devlogs": existing_devlogs,
        "shared_sessions": [
            {
                "title": record.title,
                "provider": record.provider,
                "start_kst": record.start.isoformat() if record.start else None,
                "end_kst": record.end.isoformat() if record.end else None,
                "output": str(OUT / record.output_name),
                "sha256": record.sha256,
                "sources": record.sources,
                "referenced_by": projects,
                "note": record.note,
            }
            for record, projects in shared_sessions
        ],
        "supporting_evidence": support,
        "missing_files": [
            str(path)
            for path in (
                DOWNLOADS / "ubuntu-22.04.5-desktop-amd64.iso",
                DOWNLOADS / "SHA256SUMS-ubuntu2204",
            )
            if not path.exists()
        ],
    }
    (OUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    readme = """# Project-separated canonical devlog sources

이 디렉터리는 devlog 작성용 단일 작업 세트다. 먼저 `MASTER_INDEX.md`를 연다. 네 프로젝트는 서로 섞지 않았고, 각 프로젝트의 `FULL_DIALOGUE_CHRONOLOGICAL.md`에 전체 대화를 시간순으로 모았다.

- `OmniPlanner/`
- `between_dawns/`
- `mnemosyne/`
- `rhygpu.dev/`

원시 로그는 삭제하거나 덮어쓰지 않았다. 동일 ChatGPT conversation의 구버전, Claude/ChatGPT 분기의 공통 prefix, 생성된 합본·분할본은 canonical 세트에서 제거했다. 고유한 분기 발화는 버리지 않고 병합했다.

옛 작업 폴더에서 발견된 세션은 현재 프로젝트 경로의 alias로 재연결했다. 여러 프로젝트를 다룬 대화는 `shared_sessions/`에 한 번만 저장하고 각 프로젝트 시간선에서 원래 시각에 링크한다.

이미 작성된 devlog는 각 프로젝트의 `existing_devlogs/`에 편집 가능한 정본만 모았다. 이전 HTML 렌더링본은 중복 판정에만 남기고 복사하지 않았다.

`between_dawns/supporting_evidence/`는 직접 개발 대화가 아닌 간접 제작환경·세션 감사 근거다. 메인 시간선과 분리되어 있다.
"""
    (OUT / "README.md").write_text(readme, encoding="utf-8", newline="\n")
    print(json.dumps({project: len(items) for project, items in records.items()}, ensure_ascii=False))
    print(f"OUTPUT={OUT}")


if __name__ == "__main__":
    main()
