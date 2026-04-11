# pmf-org-distill-skill

**pmf-org-distill-skill** 是一个把 [colleague-skill][1] 从“识人”扩展到“识组织”的工程仓库。你也可以把它理解为一套面向真实职场协作现场的**组织生态位诊断骨架**：它不只是判断某个人像不像某种风格，而是试图从聊天记录、会议纪要、评审意见、任务记录和项目文档中，提炼出组织真实运转时暴露出来的 **信息接口**、**关系链路**、**权限边界** 与 **隐性结构**。

这个项目背后的核心判断是：很多低信息、低质量、令人疲惫的协作输出，并不一定只是某个人能力不足，也可能是**岗位接口只暴露了低信息版本**，或者组织在传递、拍板与执行的过程中持续发生上下文损耗。因此，本仓库的目标不是做抽象管理学评论，而是尽量把“谁真正掌握背景、谁只在传声、谁承担执行却拿不到上下文、谁在反复升级和阻塞”拆成可回溯的分析链。

## 项目当前定位

当前版本不是完整产品，而是一个正在从 MVP 走向 **V2 分析框架** 的工程骨架。与早期只依赖 Prompt 直接读材料并输出结论的方式相比，V2 的重点是在“原材料”和“最终诊断”之间补出一层真正关键的**中间分析层**：先把原始证据标准化，再重建讨论线程，过滤闲聊噪音，抽取组织关系边，最后才做隐性结构推断。

这意味着当前仓库希望稳定回答的，已经不只是“这个人像不像”，而是下面这些更接近组织现实的问题。

| 分析维度 | 要回答的核心问题 |
|---|---|
| 信息接口 | 哪些岗位真正掌握上下文，哪些岗位只暴露接口表层 |
| 关系链路 | 谁向谁请求、汇报、升级、拍板、阻塞，真实协作如何发生 |
| 信息流 | 关键判断从哪里来，经过哪些环节被翻译、压缩、损耗 |
| 权限结构 | 谁能做决定，谁只能解释决定，谁负责执行却拿不到背景 |
| 组织症状 | 低信息输出究竟是个人问题、岗位问题，还是组织结构问题 |
| 隐性结构 | 对话里没有直接说出来的 owner 缺口、决策集中、协同成本和可见性断层在哪里 |

## 参考与结构映射

本项目直接继承了 `titanwings/colleague-skill` 的部分结构设计与写入器思路，但目标层已经发生根本改写。[1]

| colleague-skill | pmf-org-distill-skill | 改写逻辑 |
|---|---|---|
| `work.md` | `role_interfaces.md` | 从“个人如何干活”改成“岗位向外暴露什么接口、掌握哪层信息” |
| `persona.md` | `org_diagnosis.md` | 从“人物风格”改成“组织症状、权限结构、接口问题与风险判断” |
| 合并后的角色 skill | 合并后的组织 skill | 从“调用某个人”改成“解释某个组织切片” |
| `knowledge/` | `evidence/` | 从个人材料归档改成组织证据归档 |
| `colleagues/{slug}` | `organizations/{slug}` | 每个组织切片单独成目录 |

## V2 的关键升级

V1 的主要问题并不在于“分析写得不够多”，而在于直接从表层材料跳到表层判断。V2 引入的关键升级，是在“原材料”和“最终结论”之间补出一条可追溯的分析链。

| V2 模块 | 作用 | 当前状态 |
|---|---|---|
| `tools/models.py` | 定义证据、线程、关系边、信号评分和隐性假设的统一数据结构 | 已实现 |
| `tools/evidence_normalizer.py` | 将多类原材料统一标准化为 `EvidenceUnit` | 已实现基础版 |
| `tools/thread_reconstructor.py` | 将消息类材料按时间、主题和上下文重建为可分析线程 | 已实现基础版 |
| `tools/noise_filter.py` | 为证据和线程打上核心信号、辅助信号、闲聊噪音和歧义标签 | 已实现基础版 |
| `tools/relationship_mapper.py` | 从线程中抽取请求、汇报、升级、拍板、阻塞等组织关系边 | 已实现基础版 |
| `tools/latent_structure_inferer.py` | 基于线程、关系和评分，保守地产出可追溯组织假设 | 已实现基础版 |
| `tools/evidence_indexer.py` | 扫描证据目录并生成索引与来源统计 | 已实现 |
| `tools/org_skill_writer.py` | 创建、更新、列出组织 skill 目录与产物 | 已实现 |

这意味着当前仓库已经具备一个更合理的分析顺序：**先整理证据，再理解关系，最后才做组织判断**。

## 当前目录结构

当前仓库围绕 `prompts/`、`tools/`、`organizations/` 与 `docs/` 四个核心目录展开。

```text
pmf-org-distill-skill/
├── SKILL.md
├── README.md
├── ARCHITECTURE.md
├── TODO.md
├── ENGINEERING_GUIDELINES.md
├── prompts/
│   ├── intake.md
│   ├── role_interface_analyzer.md
│   ├── info_flow_analyzer.md
│   ├── org_diagnosis_analyzer.md
│   ├── thread_reconstruction_analyzer.md
│   ├── latent_structure_inferer.md
│   ├── interface_builder.md
│   ├── flow_builder.md
│   ├── diagnosis_builder.md
│   ├── merger.md
│   └── correction_handler.md
├── tools/
│   ├── models.py
│   ├── evidence_indexer.py
│   ├── evidence_normalizer.py
│   ├── thread_reconstructor.py
│   ├── noise_filter.py
│   ├── relationship_mapper.py
│   ├── latent_structure_inferer.py
│   ├── org_skill_writer.py
│   └── version_manager.py
├── organizations/
│   └── .gitkeep
├── references/
├── docs/
└── scripts/
```

其中，`tools/` 是当前最核心的工程目录，因为 V2 的主要价值就在于把“分析过程”从口头原则落成可接力的中间产物。

## 组织目录约定

每个组织切片都应落在 `organizations/{slug}/` 下。按照我们当前的协作分工，**我负责代码、接口、Prompt 和文档，你负责把真实材料放到正确位置**。只要目录结构稳定，后续流程就能持续复用。

```text
organizations/{slug}/
├── meta.json
├── evidence/
│   ├── docs/
│   ├── messages/
│   ├── meetings/
│   ├── decisions/
│   └── snapshots/
├── normalized/
│   └── evidence_units.json
├── derived/
│   ├── thread_map.json
│   ├── signal_scores.json
│   ├── relationship_map.json
│   └── latent_hypotheses.json
├── outputs/
│   ├── role_interfaces.md
│   ├── info_flows.md
│   ├── org_diagnosis.md
│   └── SKILL.md
└── versions/
```

上面这套结构的意义不只是“放整齐”，而是把每一层产物都显式分开：原材料、标准化结果、中间分析产物、最终输出，彼此不要混写。这样后面无论人工检查、模型回溯还是别的开发者接手，都知道每一层究竟在干什么。

## 你需要如何放置文件

按照当前分工，你只需要负责把材料放进约定目录，不需要再处理代码实现细节。为了让现有脚本后续能稳定工作，建议你按下表整理。

| 材料类型 | 建议放置目录 | 说明 |
|---|---|---|
| 项目文档、评审文档、排障记录 | `evidence/docs/` | 优先高信息材料，文件名尽量语义化 |
| 群聊导出、IM 文本记录 | `evidence/messages/` | 保留时间、说话人和会话信息 |
| 会议纪要、录音转写 | `evidence/meetings/` | 尽量保留主持人、参与者和议题 |
| 明确的决策记录、任务分派、周报 | `evidence/decisions/` | 这是高价值材料，优先补齐 |
| 截图、白板、流程图等快照 | `evidence/snapshots/` | 如果后续要做 OCR/多模态，可在这里扩展 |

如果你只能先提供一部分样本，建议优先补三类：**决策记录、排障/评审文档、连续群聊片段**。因为这三类最容易暴露真实接口、owner 分布和上下文损耗点。

## 当前核心脚本与典型产物

为了避免后续接力开发时不知道每个脚本应该吐出什么，当前仓库默认采用下面这条产物链。

| 阶段 | 输入 | 脚本 | 输出 |
|---|---|---|---|
| 证据标准化 | `organizations/{slug}/evidence/` | `tools/evidence_normalizer.py` | `normalized/evidence_units.json` |
| 线程重建 | `normalized/evidence_units.json` | `tools/thread_reconstructor.py` | `derived/thread_map.json` |
| 去噪与评分 | `thread_map.json` / `evidence_units.json` | `tools/noise_filter.py` | `derived/signal_scores.json` |
| 关系映射 | `thread_map.json` / `signal_scores.json` | `tools/relationship_mapper.py` | `derived/relationship_map.json` |
| 隐性结构推断 | `thread_map.json` / `relationship_map.json` / `signal_scores.json` | `tools/latent_structure_inferer.py` | `derived/latent_hypotheses.json` |
| 结果写入 | 上述中间产物 + 分析文本 | `tools/org_skill_writer.py` | `outputs/*.md` 与组织 skill |

这条链条的重点是：**任何最终判断都应该能回溯到中间产物和原始证据**。如果不能回溯，就说明分析仍然过于玄学。

## 当前输出结构

最终的组织分析结果应主要落在 `outputs/` 中，并至少包括以下文件。

| 文件 | 作用 |
|---|---|
| `role_interfaces.md` | 解释哪些角色掌握什么层级的信息，以及他们向上、向下、向平级输出什么 |
| `info_flows.md` | 解释信息如何流动、在哪些接口被压缩、误传、损耗或重新翻译 |
| `org_diagnosis.md` | 解释组织症状、权限边界、决策集中度、owner 缺口与高协同成本 |
| `SKILL.md` | 汇总后的组织分析 skill |

其中，V2 特别强调一点：`org_diagnosis.md` 不能只是“看起来像管理有问题”的抒情总结，而必须尽可能引用线程、关系边和假设清单来支撑。

## 推荐开发顺序

既然当前分工已经明确，后续最合理的推进方式不是让你来补代码，而是由我继续把实现和文档收口，你只负责维护材料输入的稳定性。建议顺序如下。

| 顺序 | 任务 | 负责人 |
|---|---|---|
| 1 | 继续加固 V2 中间层脚本、字段和接口契约 | 我 |
| 2 | 补齐提示词协议，让模型分析与中间产物格式对齐 | 我 |
| 3 | 更新 README、ARCHITECTURE、实施计划和工程规范 | 我 |
| 4 | 按目录约定放入真实样本包 | 你 |
| 5 | 基于真实样本跑第一轮闭环并修正字段与规则 | 我主导，你配合提供材料 |
| 6 | 再决定是否接入自动采集器和更复杂的报告生成 | 共同决策 |

## 开发与协作原则

这个项目如果想真正可用，最怕的不是“代码写得慢”，而是边写边改口径，最后目录、字段、文档和 Prompt 各说各话。因此，当前默认遵守以下原则。

| 原则 | 含义 |
|---|---|
| 先证据、后判断 | 不允许跳过证据分层直接下组织结论 |
| 先线程、后诊断 | 不理解对话关系，就不要急着解释组织结构 |
| 先去噪、后放大 | 闲聊、寒暄、低信号互动不得直接放大为组织症状 |
| 先保守推断、后升级置信度 | 隐性结构只能做假设，不能伪装成已证实事实 |
| 一层一输出 | 原材料、标准化产物、中间分析产物和最终报告必须分层存放 |
| 文档跟着代码走 | 字段、目录和命令一旦改动，README 与架构文档必须同步更新 |

## 下一步最需要什么

当前最关键的，不是再写更多“组织洞察”，而是尽快拿一份真实样本把中间层跑通。只有真实样本能暴露哪些字段不够、哪些规则太粗、哪些 Prompt 仍然把闲聊误判为信号。

因此，如果你要继续配合我推进，最有价值的动作不是解释更多抽象想法，而是按照目录规范放入一批**连续、可追溯、能看出角色关系的真实材料**。我会继续把代码、接口和文档补齐到可以稳定接力的状态。

## References

[1]: https://github.com/titanwings/colleague-skill "titanwings/colleague-skill"
