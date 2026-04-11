# V2_IMPLEMENTATION_PLAN

## 一、目标重述

这一轮迭代的目标，不是继续给现有框架补一些描述性 Prompt，而是把项目真正推进到 **Organization Distillation V2**。V2 要解决的是：分析维度过窄、对话关系缺失、闲聊误读严重、以及无法从显性材料中看出隐性组织结构。

因此，实施计划必须围绕“中间分析层”展开，而不是只围绕最终输出文档展开。

## 二、开发优先级

V2 的开发顺序必须遵守“先把输入读对，再谈输出写深”的原则。

| 优先级 | 模块 | 目标 | 不做会怎样 |
|---|---|---|---|
| P0 | `evidence_normalizer.py` | 统一文档、消息、会议、截图的证据结构 | 后续模块输入格式混乱，无法稳定工作 |
| P0 | `thread_reconstructor.py` | 把聊天和会议材料切成议题线程 | 无法识别对话关系，只能按句子乱读 |
| P0 | `noise_filter.py` | 把寒暄、闲聊、执行性口头确认剔出核心诊断 | 会继续把噪音当组织信号 |
| P1 | `relationship_mapper.py` | 识别发起、转译、拍板、协调、背锅等动作关系 | 看不见真正的组织接口 |
| P1 | `signal_scorer.py` | 给证据单元做组织信息密度打分 | 高低价值证据无法区分 |
| P2 | `latent_inference.py` | 从显性现象反推出隐性结构变量 | 输出会继续停留在表面总结 |
| P2 | `perspective_calibrator.py` | 标记当前视角盲区与待补材料 | 容易把切片误当全貌 |
| P3 | `report_assembler.py` | 汇总中间结果并重写最终报告结构 | 结果无法稳定复用 |

## 三、每个模块的最小职责边界

### 1. `evidence_normalizer.py`

它的职责是把所有材料转成统一的 `EvidenceUnit`。这一层不做最终判断，只负责让后续模块拿到稳定输入。

建议最小输出字段如下：

| 字段 | 类型 | 说明 |
|---|---|---|
| `unit_id` | string | 证据单元 ID |
| `source_type` | string | 文档、线程、会议、决策、截图 |
| `source_path` | string | 原文件位置 |
| `timestamp_start` | string/null | 起始时间 |
| `timestamp_end` | string/null | 结束时间 |
| `participants` | list[string] | 参与者或提及角色 |
| `topic_hint` | string/null | 议题线索 |
| `raw_text` | string | 原始文本 |
| `position_bias` | string/null | 视角偏差 |

### 2. `thread_reconstructor.py`

它的职责不是做摘要，而是把消息重建为“事件线程”。

一条线程至少应该包含以下信息：

| 字段 | 说明 |
|---|---|
| `thread_id` | 线程 ID |
| `topic` | 当前议题 |
| `participants` | 主要参与者 |
| `start_signal` | 议题由什么触发 |
| `turns` | 关键轮次 |
| `resolution_state` | 已决、未决、搁置、升级 |
| `org_signal_candidates` | 候选组织信号 |

### 3. `noise_filter.py`

它的职责是给每个证据单元或线程打上信号标签，而不是简单删除内容。因为有些看起来很短的话，本身是关键接口动作。

建议最小标签集合：

| 标签 | 含义 |
|---|---|
| `core_signal` | 直接暴露组织接口、权限、判断或升级链 |
| `supporting_signal` | 只能辅助理解，不可单独下结论 |
| `casual_noise` | 寒暄、玩笑、无组织意义的闲聊 |
| `ambiguous` | 需要二次判断的边界样本 |

### 4. `relationship_mapper.py`

它的职责是把线程中的互动抽象成“组织动作关系”。

建议最小关系集合：`initiates`、`frames`、`translates`、`approves`、`blocks`、`coordinates`、`escalates`、`absorbs_risk`、`complies`。

输出最好兼具两种形式：一是结构化 JSON，二是 Markdown 解释稿，方便后续写报告。

### 5. `signal_scorer.py`

它的职责是给证据分层，不是替代判断。建议最小评分维度包括：上下文丰富度、角色暴露度、决策可见度、流动可见度、冲突诊断价值、噪音占比。

### 6. `latent_inference.py`

它的职责是根据多条显性证据，输出组织层面的结构变量判断。这里最重要的，不是敢不敢推断，而是**必须把推断依据显式写出来**。

建议统一输出格式：

| 字段 | 说明 |
|---|---|
| `variable` | 结构变量名称 |
| `confidence` | 高 / 中 / 待验证 |
| `evidence_refs` | 支撑证据 ID 列表 |
| `reasoning` | 推断逻辑 |
| `counter_evidence` | 反例或未解释现象 |

### 7. `perspective_calibrator.py`

它的职责是告诉系统：现在看到的是哪一层的组织切片，以及还看不到什么。

这个模块尤其重要，因为它决定输出是否诚实。

### 8. `report_assembler.py`

最后一层才负责汇总。它不应该重新发明判断，而应该忠实汇总前面几层已经形成的结构性结论。

## 四、Prompt 改造顺序

代码和 Prompt 要并行，但 Prompt 的顺序必须服务于代码模块。

| 顺序 | Prompt | 目的 |
|---|---|---|
| 1 | `thread_segmentation.md` | 先切线程，避免混读 |
| 2 | `noise_filtering.md` | 先去噪，避免闲聊污染 |
| 3 | `relationship_mapping.md` | 再识别动作关系 |
| 4 | `signal_scoring.md` | 再做信号分层 |
| 5 | `latent_structure_inference.md` | 最后做结构推断 |
| 6 | `perspective_calibration.md` | 显式写盲区与待补材料 |

## 五、建议的数据模型

建议在 `tools/models.py` 中统一定义数据结构，避免后续不同模块各写一套字段。

核心数据类至少包括：

| 数据类 | 用途 |
|---|---|
| `EvidenceUnit` | 标准化证据单元 |
| `ThreadUnit` | 重建后的议题线程 |
| `RelationEdge` | 组织动作关系边 |
| `SignalScore` | 证据评分对象 |
| `LatentHypothesis` | 隐性结构推断对象 |
| `PerspectiveLimit` | 当前分析盲区与待补材料 |

## 六、验收标准

V2 的验收不能再看“文档写得是不是更像样”，而要看下面这些能力是否真正出现。

| 能力 | 验收问题 | 合格标准 |
|---|---|---|
| 去噪能力 | 是否还会把大段闲聊当核心分析材料 | 明显减少，并能解释为何过滤 |
| 线程能力 | 是否能看懂同一议题的来龙去脉 | 能输出稳定线程地图 |
| 关系能力 | 是否能识别谁发起、谁拍板、谁转译、谁背锅 | 能输出关系边与解释 |
| 深层推断能力 | 是否能提出隐性结构判断 | 能给出有证据支撑的结构变量 |
| 诚实性 | 是否会把切片误装成全貌 | 会明确写出视角盲区 |

## 七、开发时的工程约束

V2 代码开发时，必须遵守以下约束：

| 约束 | 说明 |
|---|---|
| 单模块单职责 | 不把清洗、推断、汇总混在一个脚本里 |
| 结构化输出优先 | 中间结果尽量先落 JSON，再生成 Markdown |
| 证据引用强制化 | 任何结构判断都必须能追溯到证据 ID |
| 弱推断显式标注 | 推断不是问题，偷换成事实才是问题 |
| 保持可替换性 | Prompt 与 Python 逻辑要能独立替换和升级 |

## 八、推荐的第一批具体任务

如果现在就交给另一个代码助手继续开发，我建议它先做下面四件事，而不是一上来就重写全仓库。

| 任务编号 | 任务 | 目标产物 |
|---|---|---|
| T1 | 补 `tools/models.py` | 统一数据结构 |
| T2 | 实现 `evidence_normalizer.py` | 生成标准化证据单元 JSON |
| T3 | 实现 `thread_reconstructor.py` | 生成线程地图 JSON / Markdown |
| T4 | 实现 `noise_filter.py` | 给线程与证据加信号标签 |

这四步完成后，再进入关系映射和隐性结构推断，整个项目会稳很多。

## 九、结论

这份实施计划的核心思想很简单：**先让系统读懂组织，再让系统评论组织。**

如果中间层仍然缺失，哪怕最终报告再像样，也只是一个“会写组织分析腔调”的工具；只有把线程、关系、信号和隐性结构真正建出来，这个项目才会回到你最初要的方向上。
