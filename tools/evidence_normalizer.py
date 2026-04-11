"""
将 organizations/{slug}/evidence 下的材料统一转换为 EvidenceUnit 列表。

当前版本优先做三件事：
1. 把不同目录的材料转成统一结构；
2. 尽可能从文件名与文本头部提取时间、参与者、会话线索；
3. 为后续线程重建、去噪、关系建模保留足够上下文，而不是只截取表面文本。
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from models import EvidenceUnit, MaterialQuality


CATEGORY_TO_SOURCE_TYPE = {
    "docs": "doc",
    "messages": "message",
    "meetings": "meeting",
    "decisions": "decision",
    "snapshots": "snapshot",
}

TEXT_EXTENSIONS = {".md", ".txt", ".log", ".json", ".yaml", ".yml", ".csv"}
HEADER_KEYS = {
    "speaker": ["speaker", "from", "发送人", "发言人"],
    "participants": ["participants", "members", "参与人", "参会人"],
    "timestamp": ["timestamp", "time", "date", "时间", "日期"],
    "topic": ["topic", "subject", "title", "议题", "主题"],
    "conversation": ["conversation", "thread", "channel", "群", "chat"],
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def make_unit_id(source_type: str, relative_path: str) -> str:
    base = f"{source_type}:{relative_path}"
    return re.sub(r"[^a-zA-Z0-9_:\-/]", "_", base)


def safe_read_text(path: Path, max_chars: int = 50000) -> str:
    if path.suffix.lower() not in TEXT_EXTENSIONS:
        return ""
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8", errors="ignore")
    return text[:max_chars]


def normalize_whitespace(text: str) -> str:
    lines = [line.rstrip() for line in text.splitlines()]
    return "\n".join(lines).strip()


def detect_iso_datetime(text: str) -> str | None:
    patterns = [
        r"(20\d{2}-\d{2}-\d{2}[ T]\d{2}:\d{2}(?::\d{2})?)",
        r"(20\d{2}/\d{2}/\d{2}[ T]\d{2}:\d{2}(?::\d{2})?)",
        r"(20\d{2}-\d{2}-\d{2})",
    ]
    for pattern in patterns:
        matched = re.search(pattern, text)
        if matched:
            return matched.group(1)
    return None


def parse_front_matter_candidates(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in text.splitlines()[:20]:
        if ":" not in line and "：" not in line:
            continue
        raw_key, raw_value = re.split(r":|：", line, maxsplit=1)
        key = raw_key.strip().lower()
        value = raw_value.strip()
        for normalized_key, aliases in HEADER_KEYS.items():
            if key in aliases:
                result[normalized_key] = value
                break
    return result


def split_people(value: str) -> list[str]:
    if not value:
        return []
    parts = re.split(r"[,，、/|]", value)
    return [part.strip() for part in parts if part.strip()]


def infer_title(path: Path, text: str, header_map: dict[str, str]) -> str:
    if header_map.get("topic"):
        return header_map["topic"][:120]
    for line in text.splitlines()[:8]:
        stripped = line.strip().lstrip("#").strip()
        if len(stripped) >= 4:
            return stripped[:120]
    return path.stem[:120]


def infer_topic_hint(path: Path, text: str, header_map: dict[str, str]) -> str | None:
    if header_map.get("topic"):
        return header_map["topic"]
    if path.parent.name and path.parent.name not in CATEGORY_TO_SOURCE_TYPE:
        return path.parent.name
    for line in text.splitlines()[:12]:
        stripped = line.strip().lstrip("#").strip()
        if len(stripped) >= 6:
            return stripped[:80]
    return None


def infer_context_hint(category: str, relative_path: str) -> str | None:
    labels = {
        "messages": "聊天材料",
        "meetings": "会议材料",
        "decisions": "决策材料",
        "docs": "文档材料",
        "snapshots": "截图或快照材料",
    }
    label = labels.get(category)
    return f"{label}：{relative_path}" if label else None


def infer_conversation_id(category: str, relative_path: str, header_map: dict[str, str]) -> str | None:
    if header_map.get("conversation"):
        return header_map["conversation"]
    parts = Path(relative_path).parts
    if category == "messages" and len(parts) >= 3:
        return parts[2]
    if len(parts) >= 2:
        return parts[1]
    return None


def infer_material_quality(category: str, text: str, header_map: dict[str, str]) -> MaterialQuality:
    length = len(text.strip())
    has_people = bool(split_people(header_map.get("participants", "")))
    has_time = bool(header_map.get("timestamp") or detect_iso_datetime(text))
    has_topic = bool(header_map.get("topic"))

    if category in {"meetings", "decisions"} and length >= 300:
        return "high_context"
    if length >= 200 and sum([has_people, has_time, has_topic]) >= 2:
        return "high_context"
    if length >= 80:
        return "partial_context"
    if length > 0:
        return "surface_only"
    return "unknown"


def infer_primary_speaker(category: str, header_map: dict[str, str], text: str) -> str | None:
    if header_map.get("speaker"):
        return header_map["speaker"]
    if category != "messages":
        return None
    for line in text.splitlines()[:8]:
        matched = re.match(r"^([\w\u4e00-\u9fff\-·]{2,20})\s*[:：]", line.strip())
        if matched:
            return matched.group(1)
    return None


def infer_participants(category: str, header_map: dict[str, str], text: str, primary_speaker: str | None) -> list[str]:
    participants = split_people(header_map.get("participants", ""))
    if primary_speaker and primary_speaker not in participants:
        participants.append(primary_speaker)

    if category in {"meeting", "meetings"}:
        for line in text.splitlines()[:20]:
            if any(key in line for key in ["参会", "参与人", "attendees", "participants"]):
                _, _, value = line.partition(":")
                extra = split_people(value or line)
                for name in extra:
                    if name not in participants:
                        participants.append(name)
    return participants[:20]


def infer_thread_hint(category: str, path: Path, header_map: dict[str, str]) -> str | None:
    if header_map.get("conversation"):
        return header_map["conversation"]
    if category == "messages":
        parent = path.parent.name
        return parent or None
    return header_map.get("topic")


def build_metadata(path: Path, category: str, header_map: dict[str, str], raw_text: str) -> dict:
    stat = path.stat()
    preview_lines = [line.strip() for line in raw_text.splitlines()[:5] if line.strip()]
    return {
        "file_name": path.name,
        "suffix": path.suffix.lower(),
        "size_bytes": stat.st_size,
        "modified_at": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
        "ingested_at": now_iso(),
        "category": category,
        "header_map": header_map,
        "preview_lines": preview_lines,
    }


def build_evidence_unit(org_dir: Path, category: str, path: Path) -> EvidenceUnit:
    relative_path = str(path.relative_to(org_dir))
    source_type = CATEGORY_TO_SOURCE_TYPE.get(category, "unknown")
    raw_text = safe_read_text(path)
    canonical_text = normalize_whitespace(raw_text)
    header_map = parse_front_matter_candidates(raw_text)
    primary_speaker = infer_primary_speaker(category, header_map, raw_text)
    participants = infer_participants(category, header_map, raw_text, primary_speaker)

    timestamp = header_map.get("timestamp") or detect_iso_datetime(raw_text)
    topic_hint = infer_topic_hint(path, raw_text, header_map)
    metadata = build_metadata(path, category, header_map, raw_text)

    return EvidenceUnit(
        unit_id=make_unit_id(source_type, relative_path),
        source_type=source_type,
        source_path=relative_path,
        title=infer_title(path, raw_text, header_map),
        timestamp_start=timestamp,
        timestamp_end=None,
        participants=participants,
        primary_speaker=primary_speaker,
        conversation_id=infer_conversation_id(category, relative_path, header_map),
        reply_to_unit_id=None,
        topic_hint=topic_hint,
        context_hint=infer_context_hint(category, relative_path),
        thread_hint=infer_thread_hint(category, path, header_map),
        raw_text=raw_text,
        canonical_text=canonical_text,
        position_bias=None,
        material_quality=infer_material_quality(category, raw_text, header_map),
        metadata=metadata,
    )


def iter_supported_files(category_dir: Path) -> Iterable[Path]:
    for path in sorted(category_dir.rglob("*")):
        if path.is_file():
            yield path


def collect_evidence_units(org_dir: Path) -> list[EvidenceUnit]:
    evidence_dir = org_dir / "evidence"
    units: list[EvidenceUnit] = []

    for category in CATEGORY_TO_SOURCE_TYPE:
        category_dir = evidence_dir / category
        if not category_dir.exists():
            continue
        for path in iter_supported_files(category_dir):
            units.append(build_evidence_unit(org_dir, category, path))

    return units


def main() -> None:
    parser = argparse.ArgumentParser(description="组织蒸馏 V2 证据标准化器")
    parser.add_argument("--org-dir", required=True, help="组织目录，例如 ./organizations/acme")
    parser.add_argument(
        "--output",
        default="evidence_units.json",
        help="输出文件名，默认写入组织目录下的 evidence_units.json",
    )
    args = parser.parse_args()

    org_dir = Path(args.org_dir).expanduser().resolve()
    if not org_dir.exists():
        raise SystemExit(f"找不到组织目录：{org_dir}")

    units = collect_evidence_units(org_dir)
    payload = {
        "organization_dir": str(org_dir),
        "generated_at": now_iso(),
        "count": len(units),
        "items": [unit.to_dict() for unit in units],
    }

    output_path = org_dir / args.output
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✅ 已生成标准化证据文件：{output_path}")
    print(json.dumps({"count": len(units)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
