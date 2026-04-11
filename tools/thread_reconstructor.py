"""
组织蒸馏 V2 线程重建器。

目标不是简单按文件夹聚类，而是尽量恢复：
1. 一个议题是如何被提出的；
2. 谁在补充、推进、阻塞、升级；
3. 当前材料是否足以把它视为一条真正的组织线程。
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from models import ThreadTurn, ThreadUnit


THREAD_SOURCE_TYPES = {"message", "meeting", "decision"}
ACTION_PATTERNS = {
    "escalation": ["升级", "上升", "老板", "负责人", "拉齐", "协调"],
    "decision": ["决定", "拍板", "结论", "定了", "批准"],
    "assignment": ["负责", "owner", "跟进", "你来", "安排"],
    "blocking_signal": ["阻塞", "卡住", "风险", "延迟", "来不及"],
    "clarification": ["为什么", "背景", "解释", "说明", "补充"],
    "status_update": ["进展", "更新", "同步", "done", "完成"],
    "issue_raise": ["问题", "异常", "bug", "故障", "需求"],
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_topic(raw: str) -> str:
    text = (raw or "untitled-thread").strip().lower()
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"[^a-z0-9\-\u4e00-\u9fff]", "", text)
    return text or "untitled-thread"


def build_thread_id(topic: str, index: int) -> str:
    return f"thread-{index:03d}-{normalize_topic(topic)}"


def load_items(input_path: Path) -> list[dict]:
    payload = json.loads(input_path.read_text(encoding="utf-8"))
    return payload.get("items", [])


def choose_topic(item: dict) -> str:
    if item.get("thread_hint"):
        return item["thread_hint"]
    if item.get("topic_hint"):
        return item["topic_hint"]
    path = Path(item.get("source_path", "unknown"))
    if path.parent.name and path.parent.name not in {"messages", "meetings", "decisions"}:
        return path.parent.name
    return item.get("title") or "untitled-thread"


def choose_group_key(item: dict) -> tuple[str, str]:
    conversation = item.get("conversation_id") or "unknown-conversation"
    topic = choose_topic(item)
    return conversation, topic


def infer_turn_type(text: str) -> str:
    lowered = (text or "").lower()
    for turn_type, patterns in ACTION_PATTERNS.items():
        if any(pattern.lower() in lowered for pattern in patterns):
            return turn_type
    return "unknown"


def infer_action_hint(turn_type: str) -> str:
    mapping = {
        "escalation": "出现升级或跨层协调动作",
        "decision": "出现拍板或结论表达",
        "assignment": "出现责任分配或 owner 指派",
        "blocking_signal": "出现阻塞、风险或延期信号",
        "clarification": "出现背景补充或解释动作",
        "status_update": "出现状态同步或进展更新",
        "issue_raise": "出现问题提出或异常暴露",
        "unknown": "需要进一步推断具体动作",
    }
    return mapping[turn_type]


def infer_addressed_to(text: str, participants: list[str], speaker: str | None) -> list[str]:
    addressed: list[str] = []
    for participant in participants:
        if participant and participant != speaker and participant in text and participant not in addressed:
            addressed.append(participant)
    return addressed[:5]


def make_turn(item: dict, participants: list[str]) -> ThreadTurn:
    content = (item.get("canonical_text") or item.get("raw_text") or "").strip()
    preview_lines = [line.strip() for line in content.splitlines() if line.strip()]
    preview = "\n".join(preview_lines[:3])[:500]
    speaker = item.get("primary_speaker") or "unknown"
    turn_type = infer_turn_type(preview)
    return ThreadTurn(
        speaker=speaker,
        addressed_to=infer_addressed_to(preview, participants, speaker),
        reply_to_speaker=None,
        action_hint=infer_action_hint(turn_type),
        turn_type=turn_type,
        content=preview,
        timestamp=item.get("timestamp_start") or item.get("metadata", {}).get("modified_at"),
        evidence_refs=[item.get("unit_id", "")],
        metadata={
            "source_type": item.get("source_type"),
            "conversation_id": item.get("conversation_id"),
        },
    )


def sort_items(items: list[dict]) -> list[dict]:
    return sorted(items, key=lambda item: item.get("timestamp_start") or item.get("metadata", {}).get("modified_at") or "")


def infer_candidates(grouped_items: list[dict]) -> list[str]:
    candidates: list[str] = []
    for item in grouped_items:
        source_type = item.get("source_type")
        if source_type == "decision":
            candidates.append("contains_decision_record")
        elif source_type == "meeting":
            candidates.append("contains_meeting_alignment")
        elif source_type == "message":
            candidates.append("contains_chat_thread")
        quality = item.get("material_quality")
        if quality == "high_context":
            candidates.append("high_context_material")
    return sorted(set(candidates))


def infer_owner(turns: list[ThreadTurn]) -> str | None:
    candidate_counter: dict[str, int] = {}
    for turn in turns:
        if turn.turn_type in {"assignment", "status_update", "decision"} and turn.speaker != "unknown":
            candidate_counter[turn.speaker] = candidate_counter.get(turn.speaker, 0) + 1
    if not candidate_counter:
        return None
    return sorted(candidate_counter.items(), key=lambda item: (-item[1], item[0]))[0][0]


def infer_resolution_state(turns: list[ThreadTurn]) -> str:
    types = [turn.turn_type for turn in turns]
    if "decision" in types:
        return "resolved"
    if "escalation" in types:
        return "escalated"
    if "blocking_signal" in types:
        return "stalled"
    return "unknown"


def infer_missing_context(grouped_items: list[dict], participants: list[str]) -> list[str]:
    gaps: list[str] = []
    if len(participants) <= 1:
        gaps.append("参与角色暴露不足，无法稳定恢复互动关系")
    if not any(item.get("timestamp_start") for item in grouped_items):
        gaps.append("缺少明确时间戳，线程顺序只能依赖文件修改时间")
    if not any(item.get("source_type") == "decision" for item in grouped_items):
        gaps.append("缺少决策类材料，无法确认线程是否被真正拍板")
    return gaps


def build_threads(items: list[dict]) -> list[ThreadUnit]:
    grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for item in items:
        if item.get("source_type") not in THREAD_SOURCE_TYPES:
            continue
        grouped[choose_group_key(item)].append(item)

    threads: list[ThreadUnit] = []
    for index, ((conversation_id, topic), grouped_items) in enumerate(sorted(grouped.items()), start=1):
        ordered_items = sort_items(grouped_items)
        participants = sorted(
            {
                participant
                for item in ordered_items
                for participant in item.get("participants", [])
                if participant
            }
        )
        turns = [make_turn(item, participants) for item in ordered_items]
        evidence_refs = [item.get("unit_id", "") for item in ordered_items]

        thread = ThreadUnit(
            thread_id=build_thread_id(topic, index),
            topic=topic,
            participants=participants,
            probable_owner=infer_owner(turns),
            start_signal=ordered_items[0].get("context_hint") or "unknown",
            resolution_state=infer_resolution_state(turns),
            org_signal_candidates=infer_candidates(ordered_items),
            evidence_refs=evidence_refs,
            turns=turns,
            missing_context=infer_missing_context(ordered_items, participants),
            metadata={
                "generated_at": now_iso(),
                "heuristic": "conversation_topic_time_grouping",
                "item_count": len(ordered_items),
                "conversation_id": conversation_id,
            },
        )
        threads.append(thread)

    return threads


def main() -> None:
    parser = argparse.ArgumentParser(description="组织蒸馏 V2 线程重建器")
    parser.add_argument("--input", required=True, help="evidence_units.json 路径")
    parser.add_argument("--output", required=True, help="thread_map.json 输出路径")
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    if not input_path.exists():
        raise SystemExit(f"找不到输入文件：{input_path}")

    items = load_items(input_path)
    threads = build_threads(items)
    payload = {
        "generated_at": now_iso(),
        "count": len(threads),
        "items": [thread.to_dict() for thread in threads],
    }

    output_path = Path(args.output).expanduser().resolve()
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✅ 已生成线程地图：{output_path}")
    print(json.dumps({"count": len(threads)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
