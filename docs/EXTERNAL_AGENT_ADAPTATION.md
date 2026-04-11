# External Agent Adaptation

本文档回答一个很现实的问题：**别的 Agent 能不能直接用 `pmf-org-distill-skill`？** 答案是能，但前提不是“模型足够聪明”，而是运行环境至少具备几项基础能力。[1] [2]

## 一、最适合接入的 Agent 类型

当前版本最适合的，不是只能纯对话的轻代理，而是能够管理目录、读写 JSON、执行命令，并在中间产物之上继续生成解释层文本的通用 Agent。[1]

| Agent 类型 | 适配程度 | 说明 |
| --- | --- | --- |
| 具备文件系统与命令执行能力的通用 Agent | 高 | 可以直接复用当前工程链路 |
| 工作流式 Agent 平台 | 中 | 需要把每个脚本封装成节点或工具 |
| 只能纯对话的聊天 Agent | 低 | 更适合复用方法论，而不是直接复用工程实现 |
| 想做 SaaS 前台的应用层 Agent | 中 | 建议把中间产物层作为后端能力独立封装 |

## 二、外部 Agent 至少要满足什么条件

| 必要条件 | 为什么需要 |
| --- | --- |
| 能读取 `SKILL.md` 或等价调用说明 | 否则无法稳定理解触发条件与输入契约 |
| 能组织目录与文件 | 当前输入和中间产物都依赖目录协议 |
| 能执行命令行脚本 | 最小分析链路通过脚本串联 |
| 能读写 JSON 和 Markdown | intake、产物消费、报告生成都依赖此能力 |
| 能在分析后继续做语言收束 | 当前仓库最成熟的是骨架，不是一键终稿 |

## 三、建议的接入方式

最稳妥的方式，不是把本项目当成“一个神秘黑盒 prompt”，而是把它当成**分层能力**接入。[2] [3]

| 层级 | 建议如何接入 |
| --- | --- |
| Intake 层 | 让上层 Agent 先生成标准 intake JSON |
| Analysis 层 | 调用当前脚本链路生成五类中间产物 |
| Report 层 | 由上层 Agent 基于中间产物写成报告或建议 |
| Product 层 | 如果需要界面，再另外做可视化封装 |

## 四、最小接入协议

任何外部 Agent 在正式调用前，建议先收束到下面这份最小 intake JSON，再进入脚本链路。[1]

```json
{
  "name": "...",
  "scope": "...",
  "user_role": "...",
  "core_problem": "...",
  "stay_leave_question": "...",
  "suspected_pattern": "...",
  "interaction_targets": ["...", "..."],
  "available_sources": ["...", "..."]
}
```

然后再按 Quickstart 中的顺序生成：

1. `normalized/evidence_units.json`
2. `derived/thread_map.json`
3. `derived/signal_scores.json`
4. `derived/relationship_map.json`
5. `derived/latent_hypotheses.json`

## 五、不要把什么能力假设为“项目已经替你做好了”

当前版本很容易被误解成“给几段聊天，仓库就会自动给出完整、漂亮、可执行的最终组织报告”。这并不是当前代码最成熟的部分。[2] [4]

| 不应预设已经完整具备的能力 | 当前真实状态 |
| --- | --- |
| 一键生成最终高质量报告 | 需要上层 Agent 或人工继续收束 |
| 面向所有平台的零改造兼容 | 目前主要适配具备脚本执行能力的环境 |
| 法律、HR、纪律结论 | 不提供，也不应该提供 |
| 在极少上下文下稳定给出重结论 | 不建议，也不可靠 |

## 六、推荐给外部 Agent 的默认话术

如果你要在别的 Agent 里调用这个项目，建议始终带上下面这层解释：

> 这是一个组织诊断骨架，而不是最终裁决器。它最擅长把群聊、会议、任务记录、自述等材料转成结构化中间产物，并据此形成保守的组织假设。最终解释层仍建议结合更多上下文与人工判断完成。

## References

[1]: ../SKILL.md "pmf-org-distill-skill SKILL"
[2]: ../README.md "pmf-org-distill-skill README"
[3]: ../QUICKSTART.md "Quickstart"
[4]: ./KNOWN_LIMITS_AND_MISREADINGS.md "Known Limits and Misreadings"
