# 快速开始

`pmf-org-distill-skill` 当前最值得公开展示的，不是“一键看透组织”的幻觉，而是一条**从粗糙材料到保守结构假设**的最小可运行链路。这个文档的目标，就是让第一次接触项目的人在 **5 分钟内看懂目录协议，在 10 分钟内完成第一次试跑**。[1] [2]

## 一、先确认你要跑的是什么

这个仓库不是个人人格分析器，也不是 HR 判案工具。它更像一个**组织反向蒸馏工作台**：你把群聊、会议纪要、任务分派、用户自述等工作痕迹放进来，它帮助你把这些材料转成可复查的中间产物，再在此基础上形成**保守的组织诊断假设**。[1] [3]

| 你将得到的东西 | 当前是否成熟 | 说明 |
| --- | --- | --- |
| 原始材料吸收 | 是 | 可以把多类粗糙材料统一纳入同一目录协议 |
| 中间产物生成 | 是 | 可以形成 `evidence_units`、线程、信号、关系和结构假设 |
| 最终结论层输出 | 是 | 可以继续生成 `analysis_report.md`、`readable_brief.md`、`stay_leave_assessment.json` 与 `evidence_trace.json` |
| 一键终局真相 | 否 | 当前版本给的是保守结论，不是绝对裁决 |

## 二、最快的试跑方式

最省心的方式，是直接参考仓库里的脱敏样例目录：`samples/anonymized-minimal/`。这份样例不是来自真实组织，也不对应任何真实个人，而是专门为了公开演示而整理的**合成脱敏输入**。[2]

如果你希望先自己手动搭一套目录，也可以直接照着下面这个结构创建。

```text
samples/anonymized-minimal/
├── meta.json
├── evidence/
│   ├── docs/
│   ├── messages/
│   ├── meetings/
│   ├── decisions/
│   └── snapshots/
├── normalized/
├── derived/
└── outputs/
```

## 三、准备最小输入

### 1. 写一个最小 `meta.json`

下面这份示例已经放在样例目录中。它不是“产品配置文件”，而是一次组织诊断任务的**问题边界说明**。

```json
{
  "name": "Anonymized Demo Org",
  "slug": "anonymized-minimal",
  "scope": "一个跨职能项目小组",
  "user_role": "项目推进接口 / 运营协调",
  "core_problem": "任务不断推进，但没有稳定拍板点，责任反复漂移",
  "stay_leave_question": "这是不是一个还能修的系统",
  "suspected_pattern": "信息碎片化、多人协调、单点 owner 缺失",
  "interaction_targets": ["项目负责人A", "产品接口B", "研发负责人C"],
  "available_sources": ["群聊节选", "会议纪要", "任务分派记录", "用户自述"]
}
```

### 2. 把材料原样放进 `evidence/`

当前版本的设计原则是：**尽量接住现实世界里本来就不整齐的工作痕迹**，而不是要求使用者先做复杂预处理。[1]

| 你手头有什么 | 放到哪里 | 公开样例里的对应文件 |
| --- | --- | --- |
| 用户自述 | `evidence/docs/` | `evidence/docs/user_statement.md` |
| 群聊记录或 CSV 导出 | `evidence/messages/` | `evidence/messages/group_chat_excerpt.csv` |
| 会议纪要 | `evidence/meetings/` | `evidence/meetings/weekly_sync.md` |
| 任务分派记录 | `evidence/decisions/` | `evidence/decisions/task_split.md` |
| 截图或流程图 | `evidence/snapshots/` | 当前样例未附，保留目录占位 |

## 四、运行最小分析链路

在仓库根目录执行以下命令。当前最小链路已经不只停在中间产物，而是会在第七步继续生成最终结论层输出。下面的命令与实际文件名和命令行参数保持一致。[4]

```bash
python3 tools/evidence_indexer.py \
  --org-dir samples/anonymized-minimal

python3 tools/evidence_normalizer.py \
  --org-dir samples/anonymized-minimal \
  --output normalized/evidence_units.json

python3 tools/thread_reconstructor.py \
  --input samples/anonymized-minimal/normalized/evidence_units.json \
  --output samples/anonymized-minimal/derived/thread_map.json

python3 tools/noise_filter.py \
  --evidence-input samples/anonymized-minimal/normalized/evidence_units.json \
  --thread-input samples/anonymized-minimal/derived/thread_map.json \
  --output samples/anonymized-minimal/derived/signal_scores.json

python3 tools/relationship_mapper.py \
  --threads samples/anonymized-minimal/derived/thread_map.json \
  --scores samples/anonymized-minimal/derived/signal_scores.json \
  --output samples/anonymized-minimal/derived/relationship_map.json

python3 tools/latent_structure_inferer.py \
  --thread-input samples/anonymized-minimal/derived/thread_map.json \
  --relation-input samples/anonymized-minimal/derived/relationship_map.json \
  --score-input samples/anonymized-minimal/derived/signal_scores.json \
  --output samples/anonymized-minimal/derived/latent_hypotheses.json

python3 tools/final_report_generator.py \
  --org-dir samples/anonymized-minimal
```

## 五、第一次跑完后，应该检查什么

最小链路跑通后，不要急着下判断。先确认输入有没有被正确吸收，再看结构假设是否站得住。[2] [3]

| 文件 | 你最先该看什么 | 正常意味着什么 |
| --- | --- | --- |
| `normalized/evidence_units.json` | `count` 与 `items[]` | 原始材料已被拆成证据单元 |
| `derived/thread_map.json` | 线程摘要与参与人 | 对话上下文已被基本串起 |
| `derived/signal_scores.json` | 高分单元与解释因子 | 噪音与高价值片段有区分 |
| `derived/relationship_map.json` | 请求、汇报、升级、阻塞边 | 协作结构开始变得可观察 |
| `derived/latent_hypotheses.json` | 假设文本与支撑证据 | 已形成第一版保守组织判断 |
| `outputs/readable_brief.md` | 一句话判词、位置判断、留走倾向 | 已得到面向普通用户的最终摘要 |
| `outputs/stay_leave_assessment.json` | recommendation、confidence、next_actions | 已得到可供外部系统消费的结构化结论 |

## 六、如果你想继续写成报告或 Skill

当前公开版本已经补上了一个**保守的最终结论层**。也就是说，外部用户或其他 Agent 不必只停在五类 JSON 中间产物上；在跑完主链路后，可以直接读取 `outputs/` 目录中的四个最终输出文件，用于阅读、展示、自动化分支或继续写成组织画像。[1] [3]

| 输出文件 | 用途 | 更适合谁读 |
| --- | --- | --- |
| `outputs/analysis_report.md` | 严谨版分析报告 | 研究者、开发者、复核者 |
| `outputs/readable_brief.md` | 易读版摘要 | 普通用户、前端界面 |
| `outputs/stay_leave_assessment.json` | 结构化去留判断 | 工作流、Agent、程序化消费方 |
| `outputs/evidence_trace.json` | 结论到证据的映射 | 审查、质检、解释性展示 |

如果你已经有稳定的解释层文稿，也可以继续调用：

```bash
python3 tools/org_skill_writer.py \
  --action create \
  --slug anonymized-minimal \
  --name "Anonymized Demo Org" \
  --meta samples/anonymized-minimal/meta.json \
  --reality path/to/my_structural_reality.md \
  --energy path/to/my_energy_drain.md \
  --decision path/to/stay_or_leave_decision.md \
  --base-dir ./organizations
```

如果你要在自己的私有目录上完整跑一遍，把上面的 `samples/anonymized-minimal` 换成 `organizations/your-org` 即可，最终也会在 `organizations/your-org/outputs/` 下生成同名文件。

## 七、最常见的三种误用

第一次接触这个项目时，最容易出现的不是命令报错，而是预期错位。下面这三类误用，建议直接避开。[3] [5]

| 误用方式 | 为什么不对 | 更合理的做法 |
| --- | --- | --- |
| 只给几句情绪吐槽就想出结论 | 材料不足，无法形成局部工作场景 | 至少补一段关键对话或一份任务分派记录 |
| 把输出当事实裁决 | 当前输出是保守组织诊断，不是最终真相 | 把它用于复盘、研究、协作讨论 |
| 只读最终摘要，不看结构证据 | 会失去可解释性，也不利于继续补料 | 至少交叉检查 `latent_hypotheses.json` 与 `evidence_trace.json` |

## 八、接下来该读什么

如果你准备把这个项目接入到自己的 Agent 或工作流里，建议继续阅读下面几份文档。

| 文档 | 作用 |
| --- | --- |
| `README.md` | 了解项目定位、发布边界与整体结构 |
| `SKILL.md` | 了解触发条件、输入约定与调用时机 |
| `docs/EXTERNAL_AGENT_ADAPTATION.md` | 查看其他 Agent 如何接入 |
| `docs/STANDARD_OUTPUT_CONTRACT_EXAMPLE.md` | 查看标准输出契约样例 |
| `docs/KNOWN_LIMITS_AND_MISREADINGS.md` | 了解已知局限与高频误判类型 |

## References

[1]: ./README.md "pmf-org-distill-skill README"
[2]: ./samples/README.md "Anonymized Sample Guide"
[3]: ./docs/KNOWN_LIMITS_AND_MISREADINGS.md "已知局限与常见误读"
[4]: ./docs/CHAT_CSV_COMPATIBILITY_VALIDATION.md "Chat CSV 兼容性验证说明"
[5]: ./docs/EXTERNAL_AGENT_ADAPTATION.md "外部 Agent 适配说明"
