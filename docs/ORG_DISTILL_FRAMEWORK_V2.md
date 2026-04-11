# 组织蒸馏框架 V2

## 一、重构目标

V2 的目标不是把现有三份输出文档继续写得更长，而是把当前项目从一个“组织主题摘要器”重构成一个真正的**组织信息接口分析器**。

这一版必须解决四类核心问题：第一，分析维度不够全面；第二，群聊与会议中的关系结构没有被真正理解；第三，系统会把大量无关闲聊误当成组织信号；第四，系统只能总结显性内容，无法从显性材料反推出隐性组织结构。

因此，V2 的核心变化不是增加更多形容词，而是补齐一个完整的中间分析层。

## 二、V2 的总流程

V2 需要把当前的轻流程：

```text
材料归档 -> 角色接口分析 / 信息流分析 / 组织诊断
```

改造成下面这条强流程：

```text
材料导入
-> 证据标准化
-> 线程切分与去噪
-> 关系建模
-> 组织信号评分
-> 隐性结构推断
-> 多视角校准
-> 结果汇总与诊断输出
```

这八步里，真正决定质量的，是中间五层。

## 三、V2 的六层分析框架

### 1. Evidence Normalization Layer

第一层不是分析，而是把不同来源的材料统一成同一种可处理结构。因为文档、会议纪要、长消息线程、群聊截图，原始格式差异太大，如果不先标准化，后面几层很难稳定工作。

建议所有证据先转成统一记录结构：

| 字段 | 说明 |
|---|---|
| `source_id` | 证据唯一 ID |
| `source_type` | `doc` / `message_thread` / `meeting_note` / `decision` / `snapshot` |
| `time_range` | 这段材料覆盖的时间范围 |
| `participants` | 涉及到的人或角色 |
| `raw_text` | 原始文本 |
| `context_hint` | 议题、项目、群组、会议背景 |
| `position_bias` | 该材料天然带有的视角偏差 |

这一层的目标，是让系统后续分析的对象不再是“散乱文件”，而是“结构化证据单元”。

### 2. Threading & Noise Filtering Layer

这是 V2 最关键的一层之一。它负责回答两个问题：

第一，这些消息到底属于哪一个议题线程；第二，哪些内容值得分析，哪些只是噪音。

这一层要做的不是简单删闲聊，而是把材料分成至少四类：

| 类别 | 含义 | 处理方式 |
|---|---|---|
| Strong Org Signal | 明确暴露权限、接口、判断或升级链 | 高权重进入后续分析 |
| Supporting Signal | 能补充语气、关系、节奏，但不能单独下结论 | 低于主证据权重使用 |
| Noise / Casual Chat | 寒暄、插科打诨、无上下文闲聊 | 默认不进入核心诊断 |
| Ambiguous Signal | 表面普通，但可能暗含权力关系或信息断层 | 标记后进入人工/模型二次判定 |

这一层不应该只靠关键词过滤，而要结合线程位置、前后文和角色动作来判断。比如一句“收到”，单看没意义；但如果只对某个人的“收到”会触发任务收口，它就是组织信号。

### 3. Relationship Modeling Layer

这一层解决“当前系统读句子、不读关系”的问题。这里不是做社交网络图那么简单，而是要识别**组织中的动作关系**。

建议把群聊、会议和文档互动统一抽成以下关系类型：

| 关系类型 | 含义 |
|---|---|
| `initiates` | 发起议题、抛出问题、要求动作 |
| `frames` | 定义问题边界、给出口径、限定讨论方式 |
| `translates` | 把上层判断翻译成任务或结论 |
| `approves` | 拍板、确认、决定是否继续 |
| `blocks` | 延缓、阻断、要求补材料 |
| `absorbs_risk` | 替别人承接风险或背锅 |
| `escalates` | 把问题上提或升级 |
| `coordinates` | 横向协调资源与节奏 |
| `complies` | 接任务、确认执行 |
| `silence_pressure` | 虽未发言但其在场会影响他人表达 |

这一层输出的不只是“谁跟谁说话”，而是“谁对谁施加了什么组织动作”。只有这样，系统才可能看见真正的信息接口。

### 4. Signal Scoring Layer

当前项目虽然有证据权重文档，但没有真正的动态评分。V2 需要把“组织信息密度”显式化。

建议每个证据单元都得到一组维度分数：

| 评分维度 | 问题 |
|---|---|
| Context Richness | 是否包含前因后果与边界条件 |
| Role Exposure | 是否暴露了角色分工与接口责任 |
| Decision Visibility | 是否能看见判断过程或拍板机制 |
| Flow Visibility | 是否暴露信息如何被翻译、压缩或损耗 |
| Conflict Diagnostic Value | 是否能看见冲突、扯皮、背锅或升级 |
| Noise Ratio | 无关内容占比多高 |

最终不是机械求和，而是形成“高价值组织信号优先阅读”的顺序。

### 5. Latent Structure Inference Layer

这是 V2 的灵魂层。它负责把显性现象转成隐性结构假设。

这一层要回答的，不是“材料里写了什么”，而是：

> 这些显性材料共同指向了一个怎样的组织结构？

建议至少推断以下结构变量：

| 隐性结构变量 | 解释 |
|---|---|
| Decision Concentration | 决策权是集中还是分散 |
| Explanation Coverage | 判断过程是否被稳定下传 |
| Translation Burden | 中层是否承担过重的翻译负担 |
| Interface Clarity | 岗位之间的接口是否清晰 |
| Escalation Cost | 问题上提是否昂贵、迟缓或政治化 |
| Local Autonomy | 一线是否具备局部判断权 |
| Visibility Asymmetry | 不同层级之间的信息可见性差距 |
| Ritualization Level | 是否用流程和口号代替真实认知对齐 |

这一层的输出必须分成三档：高置信结构判断、中置信结构推断、待验证结构假设。

### 6. Perspective Calibration Layer

任何组织蒸馏都不可能天然全知，因此 V2 必须把“你是从哪个位置看见这个组织的”写进系统里，而不是只在文末轻描淡写提一句。

这一层要显式生成三类信息：

| 校准项 | 说明 |
|---|---|
| Visible From Current Position | 从当前材料位置能稳定看见什么 |
| Blind Spots | 当前材料天然看不见什么 |
| Missing Evidence Needed | 还需要补哪些材料才能验证关键判断 |

这样输出才不会继续伪装成“全貌”。

## 四、V2 的输出结构要怎么改

V2 不应该废掉当前三份核心输出，但需要在其上游加入新的中间产物，并重写每份文件的结构。

### 1. 新增中间产物

建议新增以下中间文件：

| 文件 | 作用 |
|---|---|
| `thread_map.md` | 把材料切成议题线程，并标注主要参与者与时间顺序 |
| `relationship_map.md` | 输出角色之间的动作关系与发言权结构 |
| `signal_scorecard.md` | 给每类证据做组织信号分级 |
| `latent_structure.md` | 汇总隐性结构变量及其证据支持情况 |
| `perspective_limits.md` | 显式记录当前分析视角与盲区 |

### 2. 保留但升级三份核心输出

| 原输出 | V2 变化 |
|---|---|
| `role_interfaces.md` | 不再只总结接口，而要基于关系建模解释接口是如何形成的 |
| `info_flows.md` | 不再只画路径，而要指出哪些路径来自真实线程，哪些只是弱推断 |
| `org_diagnosis.md` | 不再只列症状，而要明确哪些症状来自隐性结构判断 |

## 五、V2 的模块设计

在代码层，建议新增或改造以下模块。

| 模块 | 职责 | 形式 |
|---|---|---|
| `tools/evidence_normalizer.py` | 将不同材料转成统一证据单元 | Python |
| `tools/thread_reconstructor.py` | 将聊天和会议材料重建为议题线程 | Python |
| `tools/noise_filter.py` | 给证据做去噪与闲聊过滤 | Python |
| `tools/relationship_mapper.py` | 抽取动作关系网络 | Python |
| `tools/signal_scorer.py` | 对证据做组织信息密度评分 | Python |
| `tools/latent_inference.py` | 根据显性现象推断隐性组织结构 | Python |
| `tools/perspective_calibrator.py` | 输出视角偏差与盲区 | Python |
| `tools/report_assembler.py` | 汇总中间文件并生成最终报告 | Python |

## 六、Prompt 层要怎么改

Prompt 也要从“提问式分析”改成“阶段式执行”。建议对应新增或重写：

| Prompt | 作用 |
|---|---|
| `prompts/thread_segmentation.md` | 先切线程，再决定哪些内容是同一议题 |
| `prompts/noise_filtering.md` | 明确区分寒暄、执行确认、冲突信号、权限信号 |
| `prompts/relationship_mapping.md` | 把对话转成动作关系，而非内容摘要 |
| `prompts/signal_scoring.md` | 对证据做组织信息密度打分 |
| `prompts/latent_structure_inference.md` | 从显性现象反推隐性结构 |
| `prompts/perspective_calibration.md` | 输出视角盲区和待补材料 |

## 七、最小实现顺序

V2 不需要一次性把所有东西都写满，但实现顺序必须正确。

第一步，先补 `thread_reconstructor.py` 和 `noise_filter.py`，因为如果线程和噪音都没处理，后面所有判断都会漂。

第二步，补 `relationship_mapper.py` 和 `signal_scorer.py`，让系统先具备“关系感”和“信号强弱感”。

第三步，再做 `latent_inference.py` 和 `perspective_calibrator.py`，把结果从摘要推向组织诊断。

第四步，最后再改 `report_assembler.py` 和最终三份输出文档结构。

## 八、V2 的判断标准

V2 是否真的有效，不看它写得是不是更长，而看它能不能做到下面四件事：

| 判断标准 | 合格表现 |
|---|---|
| 闲聊不过度解读 | 寒暄与低信号内容不会被当成核心结论来源 |
| 理解对话关系 | 能识别谁在发起、转译、拍板、背锅、协调 |
| 能做深层推断 | 能从显性材料中提出有依据的隐性结构判断 |
| 显式说明盲区 | 不把单一视角伪装成组织全貌 |

## 九、结论

V2 的本质，不是“把组织分析写得更像咨询报告”，而是把这个 Skill 真正从“识人”升级为“识组织”，再进一步升级为“识别一个组织的**信息接口系统**”。

只有当系统能稳定地区分噪音与信号、句子与关系、现象与结构、视角与全貌，它才真正具备了这个项目最想要的能力：**不是总结谁说了什么，而是看出这个组织为什么会这样说、只能这样说、以及有哪些信息根本没有机会被说出来。**
