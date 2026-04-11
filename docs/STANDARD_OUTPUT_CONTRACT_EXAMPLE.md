# 标准输出契约示例

本文档的目标，不是替代分析本身，而是让外部 Agent、工作流节点和后续产品层都能明确知道：`pmf-org-distill-skill` 这一轮运行之后，**最值得消费的是什么，哪些字段应该被优先依赖，哪些自然语言结论只能当作解释层而不是底层协议**。[1] [2]

## 一、为什么优先消费中间产物

当前版本最成熟的是**中间分析骨架**，而不是一套对所有场景都稳定的终稿表达模板。因此，上层系统最推荐的做法不是直接解析自然语言，而是优先消费这五类结构化文件。[1]

| 文件 | 核心用途 | 是否建议作为协议层 |
| --- | --- | --- |
| `normalized/evidence_units.json` | 确认原始材料是否被正确吸收 | 是 |
| `derived/thread_map.json` | 查看讨论上下文如何被串起 | 是 |
| `derived/signal_scores.json` | 识别高信号与低信号内容 | 是 |
| `derived/relationship_map.json` | 识别请求、汇报、升级、阻塞等关系 | 是 |
| `derived/latent_hypotheses.json` | 形成保守组织结构假设 | 是 |
| `outputs/*.md` | 面向人阅读的解释层结论 | 否，建议视作表现层 |

## 二、推荐的最小输出目录

```text
{org_dir}/
├── normalized/
│   └── evidence_units.json
├── derived/
│   ├── thread_map.json
│   ├── signal_scores.json
│   ├── relationship_map.json
│   └── latent_hypotheses.json
└── outputs/
    ├── analysis_report.md
    ├── readable_brief.md
    └── stay_leave_assessment.json
```

## 三、结构化文件的最小字段关注点

### 1. `normalized/evidence_units.json`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `count` | number | 证据单元总数 |
| `items[].unit_id` | string | 单元唯一标识 |
| `items[].source_type` | string | 来源类型，例如 `messages`、`meetings` |
| `items[].primary_speaker` | string | 主要说话人或责任主体 |
| `items[].content` | string | 标准化后的文本内容 |

### 2. `derived/thread_map.json`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `threads[].thread_id` | string | 线程唯一标识 |
| `threads[].participants` | array | 线程参与人 |
| `threads[].summary` | string | 线程摘要 |
| `threads[].evidence_ids` | array | 对应证据单元 |

### 3. `derived/signal_scores.json`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `scores[].unit_id` | string | 对应证据单元 |
| `scores[].score` | number | 综合信号分值 |
| `scores[].factors` | array | 评分解释因子 |

### 4. `derived/relationship_map.json`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `edges[].source` | string | 发起方 |
| `edges[].target` | string | 目标方 |
| `edges[].relation_type` | string | 例如请求、汇报、升级、阻塞 |
| `edges[].evidence_ids` | array | 支撑该关系的证据单元 |

### 5. `derived/latent_hypotheses.json`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `hypotheses[].type` | string | 假设类型 |
| `hypotheses[].description` | string | 假设内容 |
| `hypotheses[].supporting_evidence` | array | 支撑证据 |
| `hypotheses[].confidence_note` | string | 保守性说明 |

## 四、解释层输出建议

解释层不是协议层，但为了方便人工阅读与前端展示，建议至少补两类 Markdown 和一类 JSON。它们更像**消费层接口**，而不是底层事实源。[2] [3]

| 文件 | 作用 | 备注 |
| --- | --- | --- |
| `outputs/analysis_report.md` | 严谨版分析输出 | 强调证据回指与结构判断 |
| `outputs/readable_brief.md` | 可直接阅读的轻量版摘要 | 强调可读性，但不得背离分析层 |
| `outputs/stay_leave_assessment.json` | 去留判断结构化结果 | 适合上层产品直接消费 |

推荐的 `stay_leave_assessment.json` 示例：

```json
{
  "recommendation": "stay_and_observe",
  "reasoning": [
    "当前问题主要集中在拍板与协调职责分离",
    "用户承担了显著的上下文整合成本",
    "证据显示系统存在 owner 缺口，但尚不足以断言完全无解"
  ],
  "next_actions": [
    "补充更多决策记录",
    "观察下一轮是否仍由用户承担会后补位",
    "明确一次正式拍板路径"
  ],
  "boundary_note": "该结论为保守组织假设，不构成 HR、法律或纪律处理依据"
}
```

## 五、对上层产品最重要的提醒

如果你在做可视化前端、工作流节点或其他 Agent 集成，最重要的一条不是“把报告写得多像人”，而是**始终保留从结论回到中间产物的路径**。一旦只有漂亮话术，没有证据映射，这个项目就会从组织诊断骨架退化为低可信的情绪输出。[1] [3]

## References

[1]: ../README.md "pmf-org-distill-skill README"
[2]: ../SKILL.md "pmf-org-distill-skill SKILL"
[3]: ./DIAGNOSIS_OUTPUT_CONTRACT.md "Diagnosis Output Contract"
