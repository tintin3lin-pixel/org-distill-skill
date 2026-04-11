"""
组织蒸馏 V2 去噪与信号评分器。

目标：
1. 区分真正值得分析的组织信号与无关闲聊；
2. 给证据和线程同时打分，形成统一的信号视图；
3. 不把所有聊天都当成“人格材料”，而是优先寻找职责、依赖、拍板、升级和阻塞线索。
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from models import SignalScore


CORE_KEYWORDS = [
    "决定",
    "拍板",
    "批准",
    "升级",
    "阻塞",
    "风险",
    "负责",
    "owner",
    "deadline",
    "评审",
    "对齐",
    "复盘",
    "延期",
    "上线",
    "事故",
]

SUPPORTING_KEYWORDS = [
    "同步",
    "补充",
    "说明",
    "背景",
    "原因",
    "结论",
    "建议",
    "更新",
    "方案",
    "问题",
    "需求",
    "依赖",
]

RELATIONSHIP_KEYWORDS = [
    "你来",
    "我来",
    "谁负责",
    "找",
    "拉",
    "汇报",
    "同步给",
    "抄送",
    "请",
    "麻烦",
    "协调",
    "配合",
]

LATENT_STRUCTURE_KEYWORDS = [
    "没人拍板",
    "等老板",
    "先别发",
    "口头说过",
    "没有结论",
    "再确认一下",
    "谁来定",
    "先推进",
    "暂时无法",
    "只能这样",
]

NOISE_PATTERNS = [
    "收到",
    "好的",
    "ok",
    "哈哈",
    "辛苦",
    "在吗",
    "谢谢",
    "早",
    "晚安",
    "赞",
    "1",
    "111",
    "👌",
    "好的收到",
]



def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()



def normalize_text(text: str) -> str:
    return (text or "").strip().lower()



def count_hits(text: str, keywords: list[str]) -> int:
    lowered = normalize_text(text)
    return sum(keyword.lower() in lowered for keyword in keywords)



def is_short_noise(text: str) -> bool:
    lowered = normalize_text(text)
    if len(lowered) > 30:
        return False
    return count_hits(lowered, NOISE_PATTERNS) > 0



def compute_metrics(text: str, subject_type: str) -> tuple[str, dict[str, int], str, list[str]]:
    lowered = normalize_text(text)
    reasoning_parts: list[str] = []
    recommendations: list[str] = []

    core_hits = count_hits(lowered, CORE_KEYWORDS)
    supporting_hits = count_hits(lowered, SUPPORTING_KEYWORDS)
    relation_hits = count_hits(lowered, RELATIONSHIP_KEYWORDS)
    latent_hits = count_hits(lowered, LATENT_STRUCTURE_KEYWORDS)
    noise_hits = count_hits(lowered, NOISE_PATTERNS)
    length_factor = min(5, max(0, len(lowered) // 120))

    if core_hits >= 1:
        label = "core_signal"
        reasoning_parts.append("命中拍板、升级、阻塞、分工或事故等高价值组织信号")
    elif supporting_hits >= 1 or relation_hits >= 1:
        label = "supporting_signal"
        reasoning_parts.append("包含背景、依赖、请求或关系暴露线索")
    elif is_short_noise(lowered):
        label = "casual_noise"
        reasoning_parts.append("短句且主要为寒暄、确认或礼貌性回应")
        recommendations.append("默认不进入深层组织分析，只保留上下文定位作用")
    else:
        label = "ambiguous"
        reasoning_parts.append("缺少稳定高信号特征，需要与线程上下文联合判断")
        recommendations.append("结合线程重建结果和上下游材料再复核")

    metrics = {
        "context_richness": min(5, 1 + length_factor + supporting_hits),
        "role_exposure": min(5, core_hits + relation_hits),
        "decision_visibility": min(5, core_hits),
        "flow_visibility": min(5, supporting_hits + relation_hits + (1 if subject_type == "thread" else 0)),
        "conflict_diagnostic_value": min(5, core_hits + latent_hits),
        "noise_ratio": min(5, noise_hits + (1 if label == "casual_noise" else 0)),
        "relationship_visibility": min(5, relation_hits + (1 if subject_type == "thread" and supporting_hits > 0 else 0)),
        "structural_hint_strength": min(5, latent_hits + core_hits),
    }

    if label == "core_signal" and metrics["relationship_visibility"] == 0:
        recommendations.append("需要补充参与人和上下游对象，避免只看到事件不看到接口")
    if label in {"supporting_signal", "ambiguous"} and metrics["structural_hint_strength"] > 0:
        recommendations.append("可进入隐性结构推断，但必须附带反证与缺失证据说明")
    if metrics["noise_ratio"] >= 3:
        recommendations.append("噪音占比偏高，优先降权处理")

    return label, metrics, "；".join(reasoning_parts), recommendations



def build_subject_text(item: dict, subject_type: str) -> str:
    if subject_type == "thread":
        turns = item.get("turns", [])
        turn_text = "\n".join(turn.get("content", "") for turn in turns)
        missing = "；".join(item.get("missing_context", []))
        return f"{item.get('topic', '')}\n{turn_text}\n{missing}".strip()
    return item.get("canonical_text") or item.get("raw_text") or ""



def read_payload(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))



def build_scores(items: list[dict], subject_type: str) -> list[SignalScore]:
    scores: list[SignalScore] = []
    id_key = "thread_id" if subject_type == "thread" else "unit_id"

    for item in items:
        label, metrics, reasoning, recommendations = compute_metrics(
            build_subject_text(item, subject_type=subject_type),
            subject_type=subject_type,
        )
        scores.append(
            SignalScore(
                subject_id=item.get(id_key, "unknown"),
                subject_type=subject_type,
                label=label,
                context_richness=metrics["context_richness"],
                role_exposure=metrics["role_exposure"],
                decision_visibility=metrics["decision_visibility"],
                flow_visibility=metrics["flow_visibility"],
                conflict_diagnostic_value=metrics["conflict_diagnostic_value"],
                noise_ratio=metrics["noise_ratio"],
                relationship_visibility=metrics["relationship_visibility"],
                structural_hint_strength=metrics["structural_hint_strength"],
                reasoning=reasoning,
                recommendations=recommendations,
            )
        )
    return scores



def main() -> None:
    parser = argparse.ArgumentParser(description="组织蒸馏 V2 去噪与信号标注器")
    parser.add_argument("--evidence-input", required=True, help="evidence_units.json 路径")
    parser.add_argument("--thread-input", required=True, help="thread_map.json 路径")
    parser.add_argument("--output", required=True, help="signal_scores.json 输出路径")
    args = parser.parse_args()

    evidence_payload = read_payload(Path(args.evidence_input).expanduser().resolve())
    thread_payload = read_payload(Path(args.thread_input).expanduser().resolve())

    evidence_scores = build_scores(evidence_payload.get("items", []), subject_type="evidence")
    thread_scores = build_scores(thread_payload.get("items", []), subject_type="thread")
    all_scores = evidence_scores + thread_scores

    payload = {
        "generated_at": now_iso(),
        "count": len(all_scores),
        "items": [item.to_dict() for item in all_scores],
        "evidence_scores": [item.to_dict() for item in evidence_scores],
        "thread_scores": [item.to_dict() for item in thread_scores],
    }

    output_path = Path(args.output).expanduser().resolve()
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✅ 已生成信号评分卡：{output_path}")
    print(json.dumps({"evidence_scores": len(evidence_scores), "thread_scores": len(thread_scores)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
