# pmf-org-distill-skill

**pmf-org-distill-skill** 不是又一个“同事分析器”或“老板吐槽器”。它更像一套面向真实工作痕迹的**组织反向蒸馏 Skill**：从群聊、会议纪要、任务分派、用户自述、零散文档里，反推一个组织究竟如何传递信息、如何形成决策、谁在掌握上下文、谁在承担缓冲，以及你自己到底处在这个系统的什么位置。[1]

这也是它和市面上大量“个人版同事 Skill”“老板画像 Skill”最不一样的地方。别人是在给一个人贴标签，我们是在试着把一群人背后的**协作结构**翻出来。别人回答的是“这个人是不是难搞”，我们更关心的是：**为什么这个组织总在这个接口上失真，为什么某些人永远在补位，为什么有的人看起来有权，实际只是传话筒。**

| 维度 | 常见个人版 Skill | pmf-org-distill-skill |
| --- | --- | --- |
| 分析对象 | 某个同事、某个老板 | 一个组织、一个团队、一个项目协作链 |
| 输入材料 | 主观描述为主 | 群聊、会议、决策记录、文档、自述等混合证据 |
| 输出目标 | 性格判断、相处建议 | 组织结构、信息接口、权力路径、角色位置、留熬逃建议 |
| 结论方式 | 倾向直觉归因 | 尽量回到证据与结构解释 |
| 适用场景 | 情绪疏导、关系判断 | 组织诊断、协作问题排查、职场策略判断 |

## 一、这个项目现在到底能不能用

可以用，但更准确的说法是：**它已经是一个可运行、可验证、可复用的 Skill 原型**，而不是完全产品化的一键式 SaaS。当前仓库已经具备从原始证据到中间结构产物的最小闭环，能稳定吸收多类材料，并在真实群聊样本上完成标准化、线程重建、信号评分、关系映射和隐性结构推断。[2][3]

如果你问“这个东西能不能真拿来分析一个团队”，答案是**能**。如果你问“它是不是已经到了任何人零配置、零判断、双击就出结论的程度”，答案是**还没有**。当前版本最适合的定位，是面向研究者、内容创作者、组织观察者、以及具备执行命令能力的 Agent 开发者的 **v0.x 开源 Skill**。

| 能力层 | 当前状态 | 说明 |
| --- | --- | --- |
| 原始材料吸收 | 可用 | 已支持 docs / messages / meetings / decisions / snapshots，多类粗糙输入可并存 |
| 群聊 CSV 兼容 | 可用 | 已补齐聊天类 CSV 的标准化吸收逻辑，可进入官方链路 |
| 中间分析链路 | 可用 | 可产出 `evidence_units`、`thread_map`、`signal_scores`、`relationship_map`、`latent_hypotheses` |
| 最终解释层 | 可用但仍偏原型 | 适合在中间产物基础上生成分析报告，但报告模板和口径还可继续收束 |
| 跨 Agent 复用 | 有条件可用 | 适合能读 `SKILL.md`、执行命令、管理目录与 JSON 的 Agent |
| 普通用户一键使用 | 暂未完成 | 仍需要 README、样例、说明文档和最小操作能力支撑 |

## 二、它适合谁，不适合谁

这个仓库适合两类人。第一类，是想把“职场直觉”变成“组织证据”的人：你不满足于只说公司乱、老板烂、同事难搞，而是想弄清楚这个局为什么会这样。第二类，是想把这种能力封装成可复用流程的 Agent 开发者：你希望 Agent 能基于真实材料，做一轮结构化而不是情绪化的组织诊断。

它**不适合**被当成最终裁决器。它不能替你做 HR 调查，不能替你下法律判断，也不能在证据极少时假装看透一切。当前版本更像一套“组织侦察骨架”：它负责把隐约感觉拆成证据、关系和假设，而不是制造一种夸张的全知视角。[1][4]

## 三、为什么值得发布

如果今天开源世界里到处都是“个人版同事 Skill”“老板 Skill”“办公室人格分析器”，那我们更想补的是另一个空白：**有没有一种 Skill，不是把所有问题都归到个体人格，而是去反向蒸馏一个组织系统。**

换句话说，我们想开源的不是一句“你的老板控制欲很强”，而是一条更有用的问题链：

> 这个组织的真实决策权分布在哪里？信息在哪一层被折损？谁在承担上下文翻译成本？谁看似在负责，实际没有拍板权？你以为自己在解决执行问题，还是其实在承受结构问题？

这就是这个项目的发布意义。它不是帮人发泄，而是帮人把发泄变成分析；不是替人贴标签，而是把组织运转这件事，尽量还原成一个可以讨论、可以复盘、也可以被其他 Agent 复用的 Skill。

## 四、仓库里现在有什么

当前公开版本的核心由两层组成。第一层是**分析链路**，用于把原始材料转成结构化中间产物。第二层是**Skill 表达层**，用于把分析结果写回成可供 Agent 调用的组织诊断文件。[1][2]

| 目录 / 文件 | 作用 |
| --- | --- |
| `tools/evidence_indexer.py` | 建立证据索引并更新 `meta.json` 统计 |
| `tools/evidence_normalizer.py` | 将原始材料标准化为统一证据单元 |
| `tools/thread_reconstructor.py` | 将证据单元重建为线程上下文 |
| `tools/noise_filter.py` | 对证据和线程进行信号评分 |
| `tools/relationship_mapper.py` | 抽取请求、汇报、协调、阻塞等关系边 |
| `tools/latent_structure_inferer.py` | 推断隐性组织结构假设 |
| `tools/org_skill_writer.py` | 将分析结果写入结构化 Skill 文件 |
| `tools/version_manager.py` | 管理版本、回滚和归档 |
| `organizations/{slug}/` | 每个组织或项目的工作目录 |
| `docs/` | 实验说明、发布说明、后续计划等配套文档 |

## 五、Quickstart：第一次怎么跑

如果你想让外部试用者真的能从零开始，最重要的不是“讲理念”，而是给出一条**第一次就能照抄的最小路径**。下面这套 Quickstart，就是当前版本建议直接放进发布页的最小使用方式。

### 1. 准备一个组织目录

在仓库根目录下新建一个组织目录，例如 `organizations/demo-team/`。

```text
organizations/demo-team/
├── meta.json
├── evidence/
│   ├── docs/
│   ├── messages/
│   ├── meetings/
│   ├── decisions/
│   └── snapshots/
├── normalized/
├── derived/
├── outputs/
└── versions/
```

你也可以直接执行下面这组命令：

```bash
mkdir -p organizations/demo-team/{evidence/docs,evidence/messages,evidence/meetings,evidence/decisions,evidence/snapshots,normalized,derived,outputs,versions}
```

### 2. 写一个最小 `meta.json`

```json
{
  "name": "Demo Team",
  "slug": "demo-team",
  "scope": "一个跨职能项目组",
  "user_role": "项目协调 / 运营接口",
  "core_problem": "决策路径不清，推进责任反复漂移",
  "stay_leave_question": "这是不是一个还能修的系统",
  "suspected_pattern": "信息不透明、多人协调但单点拍板缺失",
  "interaction_targets": ["老板", "产品经理", "技术负责人"],
  "available_sources": ["群聊", "会议纪要", "决策记录"]
}
```

### 3. 把材料原样丢进 `evidence/`

这一步最重要的原则是：**不要为了“看起来专业”而过度预处理。** 当前版本设计的前提，就是尽量接住现实里本来就粗糙的工作痕迹。[2]

| 你手头有什么 | 放到哪里 | 备注 |
| --- | --- | --- |
| 一段用户自述 | `evidence/docs/` | 可以是口语化 Markdown / txt |
| 连续群聊导出 | `evidence/messages/` | txt / md / csv 都可尝试 |
| 会议纪要或转写 | `evidence/meetings/` | 不要求统一模板 |
| 任务分派、待办流、OKR | `evidence/decisions/` | 粗糙文本也可以 |
| 截图、流程图、表格快照 | `evidence/snapshots/` | 作为补充上下文 |

### 4. 运行最小分析链路

下面这组命令对应当前仓库里最稳定、最值得公开展示的最小闭环：

```bash
python3 tools/evidence_indexer.py \
  --org-dir organizations/demo-team

python3 tools/evidence_normalizer.py \
  --org-dir organizations/demo-team \
  --output normalized/evidence_units.json

python3 tools/thread_reconstructor.py \
  --input organizations/demo-team/normalized/evidence_units.json \
  --output organizations/demo-team/derived/thread_map.json

python3 tools/noise_filter.py \
  --evidence-input organizations/demo-team/normalized/evidence_units.json \
  --thread-input organizations/demo-team/derived/thread_map.json \
  --output organizations/demo-team/derived/signal_scores.json

python3 tools/relationship_mapper.py \
  --threads organizations/demo-team/derived/thread_map.json \
  --scores organizations/demo-team/derived/signal_scores.json \
  --output organizations/demo-team/derived/relationship_map.json

python3 tools/latent_structure_inferer.py \
  --thread-input organizations/demo-team/derived/thread_map.json \
  --relation-input organizations/demo-team/derived/relationship_map.json \
  --score-input organizations/demo-team/derived/signal_scores.json \
  --output organizations/demo-team/derived/latent_hypotheses.json
```

### 5. 你会得到什么

最小闭环跑完后，当前版本至少应该生成下面几类产物：

| 文件 | 含义 | 适合拿来做什么 |
| --- | --- | --- |
| `normalized/evidence_units.json` | 标准化后的证据单元 | 检查原始材料是否被正确吸收 |
| `derived/thread_map.json` | 重建后的上下文线程 | 看讨论链有没有被串起来 |
| `derived/signal_scores.json` | 信号评分结果 | 过滤闲聊和低价值噪音 |
| `derived/relationship_map.json` | 关系边集合 | 看谁在请求、汇报、拍板、协调、卡住 |
| `derived/latent_hypotheses.json` | 保守的结构假设 | 形成第一版组织判断 |

### 6. 如果你想写回成 Skill 文件

当前仓库还提供了一个 Skill 写入器，用于把结构化结论写回可复用文件：

```bash
python3 tools/org_skill_writer.py \
  --action create \
  --slug demo-team \
  --name "Demo Team" \
  --meta organizations/demo-team/meta.json \
  --reality path/to/my_structural_reality.md \
  --energy path/to/my_energy_drain.md \
  --decision path/to/stay_or_leave_decision.md \
  --base-dir ./organizations
```

这一步适合在你已经有了比较稳定的解释层文稿之后再执行。换句话说，**当前公开版本最成熟的是分析骨架，不是全自动文稿生成器**。

## 六、标准输出契约示例

为了让其他 Agent、脚本或上层产品更容易接入，当前版本建议至少把下面两层契约讲清楚：一个是 **intake 契约**，一个是 **中间产物契约**。

### 1. Intake 契约

这部分与 `SKILL.md` 保持一致，建议任何上层 Agent 在正式分析前，先收敛到这份最小 JSON。[1]

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

### 2. 中间产物契约

| 文件 | 最小字段关注点 | 用途 |
| --- | --- | --- |
| `evidence_units.json` | `count`、`items[].unit_id`、`items[].source_type`、`items[].primary_speaker` | 确认吸收质量 |
| `thread_map.json` | 线程 ID、参与人、摘要、证据关联 | 确认上下文重建 |
| `signal_scores.json` | `unit_id`、总分、解释因子 | 识别高信号内容 |
| `relationship_map.json` | `source`、`target`、`relation_type`、`evidence_ids` | 识别协作结构 |
| `latent_hypotheses.json` | 假设类型、描述、支撑证据 | 形成保守推断 |

如果要支持二次开发，最推荐的做法不是直接解析自然语言结论，而是**优先消费这五类 JSON 产物**，再由上层 Agent 决定如何生成报告、画像或建议。

## 七、别的 Agent 能不能直接用

可以，但要说得更准确一点：**这是一个“可被别的 Agent 复用的 Skill 骨架”，不是一个对所有 Agent 平台零改造通吃的万能插件。**

它最适合下面这类 Agent 运行环境：能够读取 `SKILL.md`，能够按说明组织目录，能够执行命令行脚本，能够读写 JSON 和 Markdown，并且允许在分析后继续调用自己的语言能力去完成解释层收束。

| Agent 类型 | 直接复用程度 | 说明 |
| --- | --- | --- |
| 具备文件系统与命令执行能力的通用 Agent | 高 | 最适合直接接入当前版本 |
| 支持工具调用的工作流 Agent | 中 | 需要把每个脚本封成节点 |
| 只能纯对话、不能跑脚本的 Agent | 低 | 只能复用方法论，难以直接复用工程链路 |
| 想做 SaaS 化前台的 Agent / App | 中 | 建议把中间产物层当后端能力，对前端另外封装 |

### 外部 Agent 适配时要补的最小解释

如果你希望外部 Agent 生态更顺滑地接入，建议在 README 里明确下面三件事：

1. **触发条件**：什么情况下应该调用这个 Skill，例如“用户在描述团队混乱、权责不清、反复背锅、想判断留熬逃时触发”。
2. **输入边界**：这个 Skill 接受粗糙材料，但仍然需要至少构成一个局部工作场景，而不是几句纯情绪吐槽。
3. **输出边界**：输出的是保守的组织假设与策略建议，不是法律、HR 或心理诊断结论。

## 八、如果现在就发布这个版本，必须带上的解释

这是当前最关键的一节。因为这个项目**已经值得发**，但如果不把解释带齐，很容易被外界误读成“读几段聊天就给公司算命”。当前版本对外发布时，建议务必同时附带下面这些说明。

| 必带解释 | 为什么一定要带 |
| --- | --- |
| 这是 **v0.x 原型**，不是产品终版 | 避免别人用产品预期要求当前仓库 |
| 输出是 **组织假设**，不是最终裁决 | 防止把推断当事实判决 |
| 当前最成熟的是 **分析骨架**，不是一键报告生成 | 避免误解自动化程度 |
| 仓库不附真实敏感样本，使用者需自行脱敏 | 保护隐私，也避免别人以为缺样本就不可用 |
| 最低门槛是“能构成局部工作场景的一组材料” | 防止拿极少上下文硬跑出过度结论 |
| 跨 Agent 可复用，但前提是 Agent 支持文件、命令、JSON | 防止“为什么我在纯聊天机器人里跑不起来” |
| 结果适合做研究、复盘和策略讨论，不适合做纪律处罚依据 | 划清伦理与使用边界 |

### 一个可以直接放在发布页里的版本说明

> 本项目当前公开版本为 **组织蒸馏 Skill 的可运行原型**。它已经可以把群聊、会议纪要、任务分派、用户自述等真实工作痕迹转成结构化中间产物，并据此形成保守的组织诊断假设。我们建议把它理解为一套“组织侦察骨架”，而不是一键生成最终真相的产品。输出结论应被用于复盘、研究、协作策略讨论和 Agent 工作流搭建，而不应被直接视为 HR、法律或纪律处置依据。

## 九、这次发布最好还一起带什么

如果你要把当前版本正式对外发布，除了 README 本身，建议至少同步附上下面几类说明，外部理解成本会低很多。[3][4]

| 优先级 | 建议一起发布的内容 | 作用 |
| --- | --- | --- |
| P0 | 一份真正可复制的 Quickstart | 让第一次试跑的人知道怎么从零开始 |
| P0 | 更收紧的 `SKILL.md` 触发条件与元信息 | 提升跨 Agent 识别稳定性 |
| P0 | 一份脱敏样例目录或脱敏样例截图 | 降低“没有数据就看不懂”的门槛 |
| P1 | 一份外部 Agent 适配说明 | 说明什么平台可直接用，什么平台需改造 |
| P1 | 一份标准输出契约样例 | 方便别人基于 JSON 二次开发报告层 |

如果只能先补一件事，我最建议优先补 **Quickstart + 脱敏样例说明**。因为一个开源项目是否“看起来真的能用”，常常不取决于理念多漂亮，而取决于别人能不能在十分钟内完成第一次成功试跑。

## 十、已知限制

当前版本的局限并不可怕，可怕的是不写清楚。下面这些限制，建议你在公开发布时明确写出来。[3][4]

| 限制 | 当前状态 |
| --- | --- |
| 真实样本依赖较强 | 已验证真实群聊场景有效，但公共脱敏样例仍建议继续补 |
| 解释层口径还可继续收束 | 中间产物比较稳定，最终话术仍可继续打磨 |
| 平台无关性尚未完全验证 | 已适合具备命令执行能力的 Agent，其他平台仍需适配 |
| 一键入口尚不完整 | 当前更像工程原型，不是最终产品界面 |
| 输出不是事实判决 | 仍需结合人类判断、上下文和更多证据交叉验证 |

## 十一、推荐的发布口径

如果你想把这个项目讲得更有意思、也更准确，我建议对外这样介绍它：

> 大家都在做“同事 Skill”“老板 Skill”“办公室人格分析器”，但我们更想做一件反过来的事：不是分析一个人，而是反向蒸馏一个组织。我们想知道的，不是谁天生难搞，而是谁在掌握上下文，谁在转述失真，谁在承担缓冲，谁看起来像 owner、其实并没有拍板权。这个项目就是把群聊、会议、任务分派和用户自述这些日常工作痕迹，重新翻译成可供 Agent 使用的组织分析骨架。

## 参考文档

[1]: ./SKILL.md
[2]: ./docs/FIRST_EXPERIMENT_RUNBOOK.md
[3]: ./docs/OPEN_SOURCE_RELEASE_PLAN.md
[4]: ./docs/NEXT_STEPS_AND_USER_ACTIONS.md
