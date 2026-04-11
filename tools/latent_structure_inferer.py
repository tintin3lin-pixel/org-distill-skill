"""
组织蒸馏 V2 隐性结构推断器。

本模块输出的不是定论，而是“带证据、带反证、带待补材料”的组织假设。
设计目标是从显性互动中保守反推出：
1. 拍板权集中在哪里；
2. owner 机制是否清晰；
3. 升级链路是否替代了常规协作；
4. 组织是否存在高协同成本或信息断层。
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from models import LatentHypothesis



def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()



def read_payload(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))



def relation_counter(relation_payload: dict) -> Counter:
    return Counter(item.get("relation_type", "unknown") for item in relation_payload.get("items", []))



def score_index(score_payload: dict) -> dict[str, dict]:
    return {item.get("subject_id", ""): item for item in score_payload.get("items", [])}



def collect_thread_ids_by_label(score_payload: dict, label: str) -> list[str]:
    result = []
    for item in score_payload.get("thread_scores", []):
        if item.get("label") == label:
            result.append(item.get("subject_id", ""))
    return result



def build_participant_load(relation_payload: dict) -> dict[str, Counter]:
    load: dict[str, Counter] = defaultdict(Counter)
    for item in relation_payload.get("items", []):
        relation_type = item.get("relation_type", "unknown")
        source = item.get("source", "unknown")
        target = item.get("target", "unknown")
        load[source][f"out:{relation_type}"] += 1
        load[target][f"in:{relation_type}"] += 1
    return load



def first_refs_from_threads(thread_ids: list[str], thread_payload: dict, limit: int = 5) -> list[str]:
    refs: list[str] = []
    thread_map = {item.get("thread_id", ""): item for item in thread_payload.get("items", [])}
    for thread_id in thread_ids[:limit]:
        refs.extend(thread_map.get(thread_id, {}).get("evidence_refs", [])[:2])
    return list(dict.fromkeys(refs))[:limit]



def infer_decision_concentration(thread_payload: dict, relation_payload: dict) -> LatentHypothesis | None:
    load = build_participant_load(relation_payload)
    decision_receivers = Counter()
    for item in relation_payload.get("items", []):
        if item.get("relation_type") in {"decides_for", "escalates_to"}:
            decision_receivers[item.get("target", "unknown")] += 1

    if not decision_receivers:
        return None

    top_actor, top_count = decision_receivers.most_common(1)[0]
    total = sum(decision_receivers.values())
    if total < 2 or top_count / total < 0.5:
        return None

    evidence_refs: list[str] = []
    for item in relation_payload.get("items", []):
        if item.get("target") == top_actor and item.get("relation_type") in {"decides_for", "escalates_to"}:
            evidence_refs.extend(item.get("evidence_refs", [])[:1])

    return LatentHypothesis(
        hypothesis_id="hyp_decision_concentration",
        variable="decision_concentration",
        observation=f"拍板或升级动作明显集中流向 {top_actor}，其可能承担非正式或正式的关键决策接口。",
        confidence="medium" if top_count < 4 else "high",
        evidence_refs=list(dict.fromkeys(evidence_refs))[:6],
        reasoning=f"关系图中共有 {total} 条拍板/升级相关边，其中 {top_count} 条指向 {top_actor}，说明关键收口点较集中。",
        counter_evidence=["若这些线程都处于特殊项目节点，集中现象可能是阶段性的。"],
        missing_evidence_needed=["更长时间窗口的决策记录", "正式组织架构或审批链"],
        validation_questions=[f"{top_actor} 是否在组织里实际承担跨团队拍板职责？"],
    )



def infer_owner_gap(thread_payload: dict, relation_payload: dict, score_payload: dict) -> LatentHypothesis | None:
    relations = relation_counter(relation_payload)
    unresolved_threads = [
        item for item in thread_payload.get("items", [])
        if item.get("resolution_state") in {"stalled", "unresolved"}
    ]
    if relations.get("assigns_work_to", 0) >= max(2, relations.get("escalates_to", 0)):
        return None
    if not unresolved_threads:
        return None

    refs = []
    for item in unresolved_threads[:4]:
        refs.extend(item.get("evidence_refs", [])[:2])

    return LatentHypothesis(
        hypothesis_id="hyp_owner_gap",
        variable="owner_clarity_gap",
        observation="组织里可能存在问题会被持续提出和升级，但 owner 落点不稳定的情况。",
        confidence="medium",
        evidence_refs=list(dict.fromkeys(refs))[:6],
        reasoning=(
            f"当前关系中升级边 {relations.get('escalates_to', 0)} 条，"
            f"明确分派边 {relations.get('assigns_work_to', 0)} 条；"
            f"同时存在 {len(unresolved_threads)} 个 stalled/unresolved 线程。"
        ),
        counter_evidence=["如果材料主要来自问题暴露阶段，而不包含后续执行阶段，也会低估 owner 分派。"],
        missing_evidence_needed=["任务分配记录", "项目 owner 清单", "周报或工单状态流转"],
        validation_questions=["问题在提出后，是否有明确 owner 被持续追踪到关闭？"],
    )



def infer_coordination_cost(relation_payload: dict, score_payload: dict) -> LatentHypothesis | None:
    relations = relation_counter(relation_payload)
    supporting_threads = collect_thread_ids_by_label(score_payload, "supporting_signal")
    sync_like = relations.get("requests_context_from", 0) + relations.get("reports_status_to", 0)
    if sync_like < 4 or len(supporting_threads) < 2:
        return None

    return LatentHypothesis(
        hypothesis_id="hyp_coordination_cost",
        variable="coordination_cost",
        observation="组织可能存在较高的横向对齐或上下文搬运成本。",
        confidence="needs_validation",
        evidence_refs=supporting_threads[:5],
        reasoning=(
            f"关系图中请求上下文/状态汇报类动作共 {sync_like} 条，"
            f"且 supporting_signal 线程较多，说明大量材料在传递背景、同步状态，而不是直接推进决策。"
        ),
        counter_evidence=["项目处于需求澄清或交接期时，同步动作本来就会显著增多。"],
        missing_evidence_needed=["跨团队依赖清单", "项目阶段信息", "会议纪要中的决策闭环记录"],
        validation_questions=["团队是否经常需要重复解释背景，才能推动事情继续？"],
    )



def infer_visibility_gap(thread_payload: dict, score_payload: dict) -> LatentHypothesis | None:
    core_threads = collect_thread_ids_by_label(score_payload, "core_signal")
    ambiguous_threads = collect_thread_ids_by_label(score_payload, "ambiguous")
    if len(core_threads) >= 2 or not ambiguous_threads:
        return None

    refs = first_refs_from_threads(ambiguous_threads, thread_payload)
    return LatentHypothesis(
        hypothesis_id="hyp_visibility_gap",
        variable="visibility_gap",
        observation="当前样本更像组织表层互动窗口，而不是决策与职责接口的全貌。",
        confidence="medium",
        evidence_refs=refs,
        reasoning=(
            f"核心高信号线程仅 {len(core_threads)} 个，而 ambiguous 线程有 {len(ambiguous_threads)} 个，"
            "说明当前材料更容易看到零散互动，难以直接看到关键接口。"
        ),
        counter_evidence=["如果样本本身就是日常工作流而非管理层材料，也会天然降低高信号密度。"],
        missing_evidence_needed=["评审意见", "排障记录", "带 owner 的项目推进材料", "决策纪要"],
        validation_questions=["现在拿到的材料，是否主要来自群聊表层而非关键工作文档？"],
    )



def infer_hypotheses(thread_payload: dict, relation_payload: dict, score_payload: dict) -> list[LatentHypothesis]:
    hypotheses: list[LatentHypothesis] = []

    for candidate in [
        infer_decision_concentration(thread_payload, relation_payload),
        infer_owner_gap(thread_payload, relation_payload, score_payload),
        infer_coordination_cost(relation_payload, score_payload),
        infer_visibility_gap(thread_payload, score_payload),
    ]:
        if candidate is not None:
            hypotheses.append(candidate)

    if not hypotheses:
        hypotheses.append(
            LatentHypothesis(
                hypothesis_id="hyp_insufficient_material",
                variable="insufficient_material",
                observation="当前材料尚不足以稳定推断隐性组织结构。",
                confidence="needs_validation",
                evidence_refs=[],
                reasoning="现有线程、关系和信号评分可以支撑基础梳理，但仍不足以稳定反推出组织深层接口。",
                counter_evidence=[],
                missing_evidence_needed=["更多决策记录", "更完整线程上下文", "会议纪要", "任务分派与复盘材料"],
                validation_questions=["是否有更接近拍板、分工、排障和复盘的材料可补充？"],
            )
        )

    return hypotheses



def main() -> None:
    parser = argparse.ArgumentParser(description="组织蒸馏 V2 隐性组织结构推断器")
    parser.add_argument("--thread-input", required=True, help="thread_map.json 路径")
    parser.add_argument("--relation-input", required=True, help="relationship_map.json 路径")
    parser.add_argument("--score-input", required=True, help="signal_scores.json 路径")
    parser.add_argument("--output", required=True, help="latent_hypotheses.json 输出路径")
    args = parser.parse_args()

    thread_payload = read_payload(Path(args.thread_input).expanduser().resolve())
    relation_payload = read_payload(Path(args.relation_input).expanduser().resolve())
    score_payload = read_payload(Path(args.score_input).expanduser().resolve())

    hypotheses = infer_hypotheses(thread_payload, relation_payload, score_payload)
    payload = {
        "generated_at": now_iso(),
        "count": len(hypotheses),
        "items": [item.to_dict() for item in hypotheses],
    }

    output_path = Path(args.output).expanduser().resolve()
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✅ 已生成隐性结构假设：{output_path}")
    print(json.dumps({"count": len(hypotheses)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
