"""
组织蒸馏 V2 关系映射器。

输入：thread_map.json 与 signal_scores.json（后者可选）。
输出：relationship_map.json。

核心原则：
1. 关系不是社交关系，而是组织动作关系；
2. 只抽取对组织信息接口有意义的动作，例如请求、汇报、分派、阻塞、升级、拍板；
3. 每条关系都必须附带线程和证据引用，避免空泛的人设式推断。
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from models import RelationEdge


RELATION_MAP = {
    "assignment": "assigns_work_to",
    "status_update": "reports_status_to",
    "clarification": "requests_context_from",
    "blocking_signal": "blocks_or_waits_on",
    "escalation": "escalates_to",
    "decision": "decides_for",
    "issue_raise": "surfaces_issue_to",
}

HIGH_SIGNAL_LABELS = {"core_signal", "supporting_signal"}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_payload(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_score_index(score_path: Path | None) -> dict[str, dict]:
    if score_path is None or not score_path.exists():
        return {}
    payload = load_payload(score_path)
    return {item["subject_id"]: item for item in payload.get("items", [])}


def choose_confidence(turn_type: str, addressed_to: list[str], score_item: dict | None) -> str:
    if turn_type in {"assignment", "decision", "escalation"} and addressed_to:
        return "high"
    if score_item and score_item.get("label") in HIGH_SIGNAL_LABELS:
        return "medium"
    return "needs_validation"


def relation_reasoning(thread: dict, turn: dict, target: str) -> str:
    snippets = [
        f"在线程《{thread.get('topic', 'unknown')}》中",
        f"{turn.get('speaker', 'unknown')} 对 {target} 产生了 {RELATION_MAP.get(turn.get('turn_type', 'unknown'), 'unknown_relation')} 动作。",
    ]
    if turn.get("action_hint"):
        snippets.append(f"动作线索：{turn['action_hint']}。")
    if turn.get("content"):
        snippets.append(f"证据摘要：{turn['content'][:120]}。")
    return "".join(snippets)


def infer_targets(turn: dict, participants: list[str]) -> list[str]:
    targets = [item for item in turn.get("addressed_to", []) if item and item != turn.get("speaker")]
    if targets:
        return targets

    if turn.get("turn_type") in {"status_update", "clarification", "issue_raise"}:
        for participant in participants:
            if participant != turn.get("speaker"):
                return [participant]
    return []


def build_edges(thread_payload: dict, score_index: dict[str, dict]) -> list[RelationEdge]:
    edges: list[RelationEdge] = []
    for thread in thread_payload.get("items", []):
        participants = thread.get("participants", [])
        thread_id = thread.get("thread_id", "")
        thread_score = score_index.get(thread_id)

        for turn in thread.get("turns", []):
            turn_type = turn.get("turn_type", "unknown")
            relation_type = RELATION_MAP.get(turn_type)
            source = turn.get("speaker") or "unknown"
            targets = infer_targets(turn, participants)
            if not relation_type or source == "unknown" or not targets:
                continue

            for target in targets:
                edge = RelationEdge(
                    source=source,
                    target=target,
                    relation_type=relation_type,
                    direction="source_to_target",
                    thread_refs=[thread_id],
                    evidence_refs=turn.get("evidence_refs", []),
                    reasoning=relation_reasoning(thread, turn, target),
                    confidence=choose_confidence(turn_type, targets, thread_score),
                    metadata={
                        "turn_type": turn_type,
                        "thread_topic": thread.get("topic"),
                        "resolution_state": thread.get("resolution_state"),
                    },
                )
                edges.append(edge)
    return edges


def merge_edges(edges: list[RelationEdge]) -> list[RelationEdge]:
    grouped: dict[tuple[str, str, str], list[RelationEdge]] = defaultdict(list)
    for edge in edges:
        grouped[(edge.source, edge.target, edge.relation_type)].append(edge)

    merged: list[RelationEdge] = []
    for (source, target, relation_type), items in grouped.items():
        confidence_rank = {"high": 3, "medium": 2, "needs_validation": 1}
        best_confidence = sorted(items, key=lambda item: -confidence_rank[item.confidence])[0].confidence
        merged.append(
            RelationEdge(
                source=source,
                target=target,
                relation_type=relation_type,
                direction="source_to_target",
                thread_refs=sorted({ref for item in items for ref in item.thread_refs}),
                evidence_refs=sorted({ref for item in items for ref in item.evidence_refs}),
                reasoning="；".join(item.reasoning for item in items[:3]),
                confidence=best_confidence,
                metadata={
                    "occurrence_count": len(items),
                },
            )
        )
    return merged


def main() -> None:
    parser = argparse.ArgumentParser(description="组织蒸馏 V2 关系映射器")
    parser.add_argument("--threads", required=True, help="thread_map.json 输入路径")
    parser.add_argument("--scores", required=False, help="signal_scores.json 输入路径")
    parser.add_argument("--output", required=True, help="relationship_map.json 输出路径")
    args = parser.parse_args()

    thread_path = Path(args.threads).expanduser().resolve()
    if not thread_path.exists():
        raise SystemExit(f"找不到线程文件：{thread_path}")

    score_path = Path(args.scores).expanduser().resolve() if args.scores else None
    thread_payload = load_payload(thread_path)
    score_index = build_score_index(score_path)

    raw_edges = build_edges(thread_payload, score_index)
    merged_edges = merge_edges(raw_edges)

    payload = {
        "generated_at": now_iso(),
        "count": len(merged_edges),
        "items": [edge.to_dict() for edge in merged_edges],
    }

    output_path = Path(args.output).expanduser().resolve()
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✅ 已生成关系地图：{output_path}")
    print(json.dumps({"count": len(merged_edges)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
