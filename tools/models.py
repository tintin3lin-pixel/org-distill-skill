"""
组织蒸馏 V2 的统一数据模型。

设计目标：
1. 让标准化、线程重建、去噪、关系建模、隐性结构推断共享稳定接口；
2. 让每一个判断都能回溯到具体证据与具体轮次；
3. 把“谁在说话、在什么上下文里说、这句话在组织里起什么作用”显式建模；
4. 为后续 LLM 分析与规则分析共用同一套 JSON 结构。
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal


SourceType = Literal["doc", "message", "meeting", "decision", "snapshot", "unknown"]
SignalLabel = Literal["core_signal", "supporting_signal", "casual_noise", "ambiguous"]
ResolutionState = Literal["resolved", "unresolved", "stalled", "escalated", "unknown"]
ConfidenceLevel = Literal["high", "medium", "needs_validation"]
MaterialQuality = Literal["high_context", "partial_context", "surface_only", "unknown"]
TurnType = Literal[
    "issue_raise",
    "assignment",
    "status_update",
    "clarification",
    "decision",
    "escalation",
    "blocking_signal",
    "social_noise",
    "unknown",
]


@dataclass(slots=True)
class EvidenceUnit:
    """标准化后的最小证据单元。"""

    unit_id: str
    source_type: SourceType
    source_path: str
    title: str = ""
    timestamp_start: str | None = None
    timestamp_end: str | None = None
    participants: list[str] = field(default_factory=list)
    primary_speaker: str | None = None
    conversation_id: str | None = None
    reply_to_unit_id: str | None = None
    topic_hint: str | None = None
    context_hint: str | None = None
    thread_hint: str | None = None
    raw_text: str = ""
    canonical_text: str = ""
    position_bias: str | None = None
    material_quality: MaterialQuality = "unknown"
    metadata: dict[str, Any] = field(default_factory=dict)

    def effective_text(self) -> str:
        return self.canonical_text or self.raw_text

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["effective_text"] = self.effective_text()
        return data


@dataclass(slots=True)
class ThreadTurn:
    """线程中的一个关键轮次。"""

    speaker: str
    addressed_to: list[str] = field(default_factory=list)
    reply_to_speaker: str | None = None
    action_hint: str = "needs_inference"
    turn_type: TurnType = "unknown"
    content: str = ""
    timestamp: str | None = None
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ThreadUnit:
    """重建后的议题线程。"""

    thread_id: str
    topic: str
    participants: list[str] = field(default_factory=list)
    probable_owner: str | None = None
    start_signal: str = ""
    resolution_state: ResolutionState = "unknown"
    org_signal_candidates: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    turns: list[ThreadTurn] = field(default_factory=list)
    missing_context: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["turns"] = [turn.to_dict() for turn in self.turns]
        return data


@dataclass(slots=True)
class RelationEdge:
    """组织动作关系边。"""

    source: str
    target: str
    relation_type: str
    direction: Literal["source_to_target", "bidirectional", "unknown"] = "source_to_target"
    thread_refs: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    reasoning: str = ""
    confidence: ConfidenceLevel = "needs_validation"
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class SignalScore:
    """证据或线程的组织信号评分。"""

    subject_id: str
    subject_type: Literal["evidence", "thread"]
    label: SignalLabel
    context_richness: int = 0
    role_exposure: int = 0
    decision_visibility: int = 0
    flow_visibility: int = 0
    conflict_diagnostic_value: int = 0
    noise_ratio: int = 0
    relationship_visibility: int = 0
    structural_hint_strength: int = 0
    reasoning: str = ""
    recommendations: list[str] = field(default_factory=list)

    def total_score(self) -> int:
        positive = (
            self.context_richness
            + self.role_exposure
            + self.decision_visibility
            + self.flow_visibility
            + self.conflict_diagnostic_value
            + self.relationship_visibility
            + self.structural_hint_strength
        )
        return positive - self.noise_ratio

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["total_score"] = self.total_score()
        return data


@dataclass(slots=True)
class LatentHypothesis:
    """隐性组织结构推断。"""

    hypothesis_id: str
    variable: str
    observation: str
    confidence: ConfidenceLevel
    evidence_refs: list[str] = field(default_factory=list)
    reasoning: str = ""
    counter_evidence: list[str] = field(default_factory=list)
    missing_evidence_needed: list[str] = field(default_factory=list)
    validation_questions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class PerspectiveLimit:
    """当前分析视角的可见范围与盲区。"""

    visible_from_current_position: list[str] = field(default_factory=list)
    blind_spots: list[str] = field(default_factory=list)
    missing_evidence_needed: list[str] = field(default_factory=list)
    contamination_risks: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class AnalysisBundle:
    """供报告层消费的聚合结果。"""

    organization_slug: str = ""
    evidence_units: list[EvidenceUnit] = field(default_factory=list)
    threads: list[ThreadUnit] = field(default_factory=list)
    relations: list[RelationEdge] = field(default_factory=list)
    scores: list[SignalScore] = field(default_factory=list)
    hypotheses: list[LatentHypothesis] = field(default_factory=list)
    perspective_limit: PerspectiveLimit | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "organization_slug": self.organization_slug,
            "evidence_units": [item.to_dict() for item in self.evidence_units],
            "threads": [item.to_dict() for item in self.threads],
            "relations": [item.to_dict() for item in self.relations],
            "scores": [item.to_dict() for item in self.scores],
            "hypotheses": [item.to_dict() for item in self.hypotheses],
            "perspective_limit": self.perspective_limit.to_dict() if self.perspective_limit else None,
            "metadata": self.metadata,
        }
