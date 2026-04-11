"""
基于 org-distill-skill 的中间产物生成最终结论层输出。

输出文件：
1. outputs/analysis_report.md
2. outputs/readable_brief.md
3. outputs/stay_leave_assessment.json
4. outputs/evidence_trace.json

设计原则：
- 优先保守，不把推断写成裁决；
- 优先可回指，让关键结论能回到 evidence / thread / hypothesis；
- 在材料不足时，也要产出“可用但不武断”的最终结果，而不是直接停在中间层。
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BOUNDARY_NOTE = (
    "该结果是基于现有材料形成的保守组织诊断，不构成 HR、法律、绩效、纪律或人格判断依据。"
)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_json(path: Path, default: dict[str, Any] | None = None) -> dict[str, Any]:
    if not path.exists():
        return default or {}
    return json.loads(path.read_text(encoding="utf-8"))


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def top_items(items: list[dict[str, Any]], limit: int = 3, score_key: str = "total_score") -> list[dict[str, Any]]:
    def get_score(item: dict[str, Any]) -> int:
        value = item.get(score_key)
        if isinstance(value, (int, float)):
            return int(value)
        return 0

    return sorted(items, key=get_score, reverse=True)[:limit]


def load_bundle(org_dir: Path) -> dict[str, Any]:
    meta = read_json(org_dir / "meta.json", {})
    normalized = read_json(org_dir / "normalized" / "evidence_units.json", {"count": 0, "items": []})
    thread_map = read_json(org_dir / "derived" / "thread_map.json", {"count": 0, "items": []})
    signal_scores = read_json(org_dir / "derived" / "signal_scores.json", {"count": 0, "items": []})
    relationship_map = read_json(org_dir / "derived" / "relationship_map.json", {"count": 0, "items": []})
    latent_hypotheses = read_json(org_dir / "derived" / "latent_hypotheses.json", {"count": 0, "items": []})

    return {
        "meta": meta,
        "normalized": normalized,
        "thread_map": thread_map,
        "signal_scores": signal_scores,
        "relationship_map": relationship_map,
        "latent_hypotheses": latent_hypotheses,
    }


def infer_user_position(meta: dict[str, Any], bundle: dict[str, Any]) -> tuple[str, str]:
    role = str(meta.get("user_role") or meta.get("user_position") or "").strip()
    hypotheses = bundle["latent_hypotheses"].get("items", [])
    threads = bundle["thread_map"].get("items", [])
    escalated_threads = sum(1 for item in threads if item.get("resolution_state") == "escalated")

    role_text = role.lower()
    if any(keyword in role_text for keyword in ["接口", "协调", "项目", "运营", "pm", "推进"]):
        return "中间缓冲层", "你承担了推进和对齐压力，但不一定握有稳定拍板权。"
    if escalated_threads >= 2:
        return "临时桥接点", "系统缺少稳定接口，所以不少跨角色协作会临时从你这里经过。"
    for hypothesis in hypotheses:
        observation = str(hypothesis.get("observation") or "")
        if "owner" in observation.lower() or "拍板" in observation:
            return "伪 owner", "你看起来像在负责，但关键资源、背景或拍板权未必在你手里。"
    return "信息末梢", "你需要对结果负责，但当前材料显示你未必能稳定拿到完整上下文。"


def evaluate_case(bundle: dict[str, Any]) -> dict[str, Any]:
    meta = bundle["meta"]
    normalized = bundle["normalized"]
    threads = bundle["thread_map"].get("items", [])
    scores = bundle["signal_scores"].get("items", [])
    relations = bundle["relationship_map"].get("items", [])
    hypotheses = bundle["latent_hypotheses"].get("items", [])

    evidence_count = int(normalized.get("count", 0) or 0)
    thread_count = int(bundle["thread_map"].get("count", 0) or 0)
    relation_count = int(bundle["relationship_map"].get("count", 0) or 0)
    escalated_threads = sum(1 for item in threads if item.get("resolution_state") == "escalated")
    missing_context_flags = sum(len(item.get("missing_context", [])) for item in threads)
    insufficient_material = any(item.get("variable") == "insufficient_material" for item in hypotheses)

    top_scores = top_items(scores, limit=3)
    average_score = 0.0
    if scores:
        average_score = sum(int(item.get("total_score", 0) or 0) for item in scores) / len(scores)

    user_position, user_position_note = infer_user_position(meta, bundle)

    signals: list[str] = []
    risks: list[str] = []
    next_actions: list[str] = []

    if insufficient_material or evidence_count < 3:
        recommendation = "observe_and_collect_more"
        recommendation_label = "先观察别上头"
        confidence = "low"
        verdict = "这套材料已经能说明你在承担组织摩擦，但还不足以下终局判断。"
        title = "现在先别急着给这家公司判死刑"
        signals.append("现有材料已经暴露出推进与决策之间存在明显接口摩擦。")
        signals.append("中间产物能形成初步结构假设，但不足以稳定确认深层权责结构。")
        risks.append("材料覆盖面偏窄，容易把局部场景误当成整体组织常态。")
        next_actions.extend([
            "补充更接近拍板、分工、排障和复盘的材料。",
            "优先加入至少一轮完整会议纪要与对应任务分派记录。",
            "继续观察你是否长期承担解释、催办和兜底角色。",
        ])
    elif escalated_threads >= 2 and relation_count == 0 and missing_context_flags >= 3:
        recommendation = "prepare_exit"
        recommendation_label = "建议准备撤退"
        confidence = "medium"
        verdict = "这不像一个权责稳定的协作系统，更像一个靠个人临时补位维持运转的系统。"
        title = "你不是在被培养，你更像在替组织补洞"
        signals.append("多个线程处于升级或悬而未决状态，说明正常协作接口不够稳定。")
        signals.append("关系映射层无法形成稳定责任边，提示谁拍板、谁兜底并不清楚。")
        risks.append("长期承担缓冲与解释成本，却拿不到真实授权。")
        risks.append("上下文持续碎片化，容易导致你对结果负责却无权控制关键变量。")
        next_actions.extend([
            "在继续投入前，先明确一次真实拍板路径和升级路径。",
            "如果后续仍由你承担结果却拿不到更多授权，开始准备退出选项。",
            "保留关键任务拆分、会议纪要和责任转移证据，避免被动背锅。",
        ])
    else:
        recommendation = "stay_and_repair"
        recommendation_label = "可以继续修"
        confidence = "medium"
        verdict = "当前问题更像接口设计差和上下文分布不均，而不是已经完全不可修复。"
        title = "这局不算健康，但还没烂到只能提桶跑路"
        signals.append("现有材料更像在指向接口设计和责任分配问题，而不是单点恶意。")
        signals.append("如果能补齐拍板机制和信息同步路径，系统仍存在修复空间。")
        risks.append("如果结构问题长期不被修复，你会继续承担额外协调成本。")
        next_actions.extend([
            "争取更清晰的拍板点、升级路径和任务 owner 定义。",
            "把关键讨论沉淀成可追踪的书面记录，减少口头漂移。",
            "持续观察下一轮协作中，责任和授权是否开始收敛。",
        ])

    for item in hypotheses[:3]:
        observation = str(item.get("observation") or "").strip()
        if observation:
            signals.append(observation)

    top_score_notes = []
    for item in top_scores:
        subject_id = item.get("subject_id", "unknown")
        total_score = item.get("total_score", 0)
        reasoning = str(item.get("reasoning") or "").strip()
        if reasoning:
            top_score_notes.append(f"{subject_id}（{total_score} 分）：{reasoning}")
        else:
            top_score_notes.append(f"{subject_id}（{total_score} 分）")

    evidence_summary = {
        "evidence_count": evidence_count,
        "thread_count": thread_count,
        "relation_count": relation_count,
        "hypothesis_count": int(bundle["latent_hypotheses"].get("count", 0) or 0),
        "average_signal_score": round(average_score, 2),
        "escalated_threads": escalated_threads,
    }

    return {
        "generated_at": now_iso(),
        "organization_name": meta.get("name") or meta.get("slug") or org_dir_name(meta),
        "organization_slug": meta.get("slug") or org_dir_name(meta),
        "scope": meta.get("scope", "未指定"),
        "core_problem": meta.get("core_problem", "未指定"),
        "stay_leave_question": meta.get("stay_leave_question", "未指定"),
        "user_position": user_position,
        "user_position_note": user_position_note,
        "title": title,
        "verdict": verdict,
        "recommendation": recommendation,
        "recommendation_label": recommendation_label,
        "confidence": confidence,
        "signals": dedupe_preserve_order(signals),
        "risks": dedupe_preserve_order(risks),
        "next_actions": dedupe_preserve_order(next_actions),
        "top_score_notes": top_score_notes,
        "evidence_summary": evidence_summary,
    }


def org_dir_name(meta: dict[str, Any]) -> str:
    return str(meta.get("slug") or meta.get("name") or "organization")


def dedupe_preserve_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    results: list[str] = []
    for item in items:
        text = item.strip()
        if not text or text in seen:
            continue
        seen.add(text)
        results.append(text)
    return results


def make_evidence_trace(bundle: dict[str, Any], assessment: dict[str, Any]) -> dict[str, Any]:
    normalized_items = bundle["normalized"].get("items", [])
    threads = bundle["thread_map"].get("items", [])
    hypotheses = bundle["latent_hypotheses"].get("items", [])

    source_index = {item.get("unit_id"): item for item in normalized_items}
    claims: list[dict[str, Any]] = []

    for idx, signal in enumerate(assessment["signals"][:5], start=1):
        supporting_evidence: list[dict[str, Any]] = []
        for hypothesis in hypotheses:
            refs = hypothesis.get("evidence_refs", [])
            for ref in refs[:3]:
                source = source_index.get(ref, {})
                supporting_evidence.append(
                    {
                        "evidence_ref": ref,
                        "source_path": source.get("source_path", "unknown"),
                        "source_type": source.get("source_type", "unknown"),
                        "excerpt": (source.get("canonical_text") or source.get("raw_text") or "")[:180],
                    }
                )
        if not supporting_evidence:
            for thread in threads[:2]:
                refs = thread.get("evidence_refs", [])
                for ref in refs[:2]:
                    source = source_index.get(ref, {})
                    supporting_evidence.append(
                        {
                            "evidence_ref": ref,
                            "source_path": source.get("source_path", "unknown"),
                            "source_type": source.get("source_type", "unknown"),
                            "excerpt": (source.get("canonical_text") or source.get("raw_text") or thread.get("start_signal") or "")[:180],
                        }
                    )
        claims.append(
            {
                "claim_id": f"claim_{idx:03d}",
                "claim": signal,
                "supporting_evidence": supporting_evidence[:4],
                "boundary_note": BOUNDARY_NOTE,
            }
        )

    return {
        "generated_at": now_iso(),
        "organization_slug": assessment["organization_slug"],
        "claims": claims,
    }


def render_analysis_report(bundle: dict[str, Any], assessment: dict[str, Any], evidence_trace: dict[str, Any]) -> str:
    meta = bundle["meta"]
    summary = assessment["evidence_summary"]
    hypotheses = bundle["latent_hypotheses"].get("items", [])

    hypothesis_lines = "\n".join(
        f"{idx}. **{item.get('variable', 'unknown')}**：{item.get('observation', '未提供观察')}"
        for idx, item in enumerate(hypotheses[:5], start=1)
    ) or "1. 当前尚未形成稳定的高置信结构假设。"

    signal_lines = "\n".join(f"{idx}. {item}" for idx, item in enumerate(assessment["signals"], start=1))
    risk_lines = "\n".join(f"{idx}. {item}" for idx, item in enumerate(assessment["risks"], start=1)) or "1. 当前未识别出需要单列的额外风险。"
    action_lines = "\n".join(f"{idx}. {item}" for idx, item in enumerate(assessment["next_actions"], start=1))
    trace_lines = "\n".join(
        f"- **{claim['claim_id']}**：{claim['claim']}（支撑证据 {len(claim['supporting_evidence'])} 条）"
        for claim in evidence_trace["claims"]
    ) or "- 暂无证据映射。"
    score_lines = "\n".join(f"- {item}" for item in assessment["top_score_notes"]) or "- 当前暂无高置信评分说明。"

    return f"""# {assessment['organization_name']} 组织诊断分析报告

## 一、结论摘要

**总体判断：** {assessment['verdict']}

**行动倾向：** {assessment['recommendation_label']}（`{assessment['recommendation']}`，置信度 `{assessment['confidence']}`）

## 二、样本边界

| 字段 | 内容 |
| --- | --- |
| 组织名称 | {assessment['organization_name']} |
| 范围 | {assessment['scope']} |
| 用户角色 | {meta.get('user_role', '未指定')} |
| 核心问题 | {assessment['core_problem']} |
| 去留问题 | {assessment['stay_leave_question']} |

## 三、材料覆盖概览

| 指标 | 数值 |
| --- | --- |
| 证据单元数 | {summary['evidence_count']} |
| 线程数 | {summary['thread_count']} |
| 关系边数 | {summary['relation_count']} |
| 假设数 | {summary['hypothesis_count']} |
| 升级线程数 | {summary['escalated_threads']} |
| 平均信号分 | {summary['average_signal_score']} |

## 四、关键结构判断

{signal_lines}

## 五、用户所处位置

**位置标签：** {assessment['user_position']}

{assessment['user_position_note']}

## 六、隐性结构假设

{hypothesis_lines}

## 七、高信号材料提示

{score_lines}

## 八、主要风险

{risk_lines}

## 九、建议动作

{action_lines}

## 十、证据回指说明

{trace_lines}

## 十一、边界说明

> {BOUNDARY_NOTE}

> 本报告优先依据 `normalized/` 与 `derived/` 中间产物生成，最终自然语言结论属于解释层，不应脱离结构化产物单独使用。
"""


def render_readable_brief(bundle: dict[str, Any], assessment: dict[str, Any]) -> str:
    evidence_summary = assessment["evidence_summary"]
    why_part_1 = assessment["signals"][0] if assessment["signals"] else "当前材料只足够支持保守判断。"
    why_part_2 = assessment["signals"][1] if len(assessment["signals"]) > 1 else "要想下更稳的判断，还需要更多接近拍板和分工的材料。"
    risk_text = assessment["risks"][0] if assessment["risks"] else "你可能正在承担额外的组织摩擦成本。"
    action_items = [item.rstrip("。；; ") for item in assessment["next_actions"][:2] if item.strip()]
    action_text = "；".join(action_items)

    return f"""# {assessment['title']}

**一句话判词：** {assessment['verdict']}

## 你的位置

你现在更像一个“{assessment['user_position']}”。{assessment['user_position_note']}

## 为什么会这样

{why_part_1}

{why_part_2}

更直接一点说，你的问题未必是能力不够，更可能是你正在替一套还没把接口讲明白的系统承担摩擦。{risk_text}

## 留还是走

当前更接近“{assessment['recommendation_label']}”。{action_text if action_text else '建议先继续补材料，再决定是否升级判断。'}。

## 证据提醒

这份判断主要基于 {evidence_summary['evidence_count']} 条证据单元、{evidence_summary['thread_count']} 个线程、{evidence_summary['relation_count']} 条关系边和 {evidence_summary['hypothesis_count']} 条结构假设。{BOUNDARY_NOTE}
"""


def write_outputs(org_dir: Path, bundle: dict[str, Any]) -> dict[str, Path]:
    outputs_dir = org_dir / "outputs"
    ensure_dir(outputs_dir)

    assessment = evaluate_case(bundle)
    evidence_trace = make_evidence_trace(bundle, assessment)
    analysis_report = render_analysis_report(bundle, assessment, evidence_trace)
    readable_brief = render_readable_brief(bundle, assessment)

    stay_leave_assessment = {
        "generated_at": assessment["generated_at"],
        "organization_slug": assessment["organization_slug"],
        "organization_name": assessment["organization_name"],
        "recommendation": assessment["recommendation"],
        "recommendation_label": assessment["recommendation_label"],
        "confidence": assessment["confidence"],
        "title": assessment["title"],
        "verdict": assessment["verdict"],
        "user_position": assessment["user_position"],
        "user_position_note": assessment["user_position_note"],
        "reasoning": assessment["signals"],
        "key_risks": assessment["risks"],
        "next_actions": assessment["next_actions"],
        "sufficient_for_final_verdict": assessment["recommendation"] != "observe_and_collect_more",
        "boundary_note": BOUNDARY_NOTE,
        "evidence_summary": assessment["evidence_summary"],
    }

    analysis_report_path = outputs_dir / "analysis_report.md"
    readable_brief_path = outputs_dir / "readable_brief.md"
    assessment_path = outputs_dir / "stay_leave_assessment.json"
    evidence_trace_path = outputs_dir / "evidence_trace.json"

    analysis_report_path.write_text(analysis_report.rstrip() + "\n", encoding="utf-8")
    readable_brief_path.write_text(readable_brief.rstrip() + "\n", encoding="utf-8")
    assessment_path.write_text(json.dumps(stay_leave_assessment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    evidence_trace_path.write_text(json.dumps(evidence_trace, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    return {
        "analysis_report": analysis_report_path,
        "readable_brief": readable_brief_path,
        "stay_leave_assessment": assessment_path,
        "evidence_trace": evidence_trace_path,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="根据中间产物生成最终组织诊断结论层输出")
    parser.add_argument("--org-dir", required=True, help="组织样本目录，例如 samples/anonymized-minimal")
    args = parser.parse_args()

    org_dir = Path(args.org_dir).expanduser().resolve()
    if not org_dir.exists():
        raise FileNotFoundError(f"找不到组织目录：{org_dir}")

    bundle = load_bundle(org_dir)
    outputs = write_outputs(org_dir, bundle)

    print("✅ 最终结论层已生成：")
    for key, path in outputs.items():
        print(f"- {key}: {path}")


if __name__ == "__main__":
    main()
