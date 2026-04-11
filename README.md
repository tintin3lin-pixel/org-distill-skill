# pmf-org-distill-skill

大家都在讲怎么蒸馏一个人：做“同事 Skill”，做“老板 Skill”，做各种办公室人格分析器。但现实里，很多人真正焦虑的不是“这个人到底什么性格”，而是另一件事：**这个组织到底是怎么运转的。**

比如你会怀疑，老板是不是已经在找一个可以替代你的人；你会感觉团队里有些人看起来在负责，其实根本拍不了板；你也会发现，很多问题不是谁坏，而是信息一层层传下来以后已经变形了。于是我们想做的，不是继续分析某一个人，而是**反过来，蒸馏出一个组织。**

这个项目做的事情很简单：把群聊、会议纪要、任务分派、用户自述这些工作痕迹收集起来，整理成一套**组织分析骨架**，交给 Agent 继续使用。它不负责给谁下性格结论，也不假装一眼看穿办公室政治。它更像一个开源的组织诊断底座，帮你回答一些更实际的问题：谁掌握上下文，谁在中间转述，谁在承担缓冲，谁像 owner 但其实没有决定权。

| 你可以怎么用它 | 适合谁 |
| --- | --- |
| 当成一个可 fork 的开源仓库继续改 | 想做组织分析、协作诊断、工作流产品的开发者 |
| 当成一个可安装 / 可改写的 Skill 骨架 | 具备目录管理、命令执行和 JSON 处理能力的 Agent |
| 当成一套组织观察方法来复用 | 研究者、内容创作者、组织顾问、独立分析者 |

## 这个项目在解决什么问题

很多“职场分析”最后都会变成一句话：判断这个人好不好相处，那个老板是不是有问题。但真实工作里，更常见的情况是：**你碰到的不是某一个人的问题，而是整个组织的结构问题。**

这个仓库想解决的，就是这种“总觉得哪里不对，但又说不清”的时刻。它会尽量把这种模糊感觉拆成更具体的问题：到底是谁掌握上下文，信息是在哪一层开始失真，谁在反复当传话筒和缓冲层，谁看起来负责很多事、其实并没有真正的决定权。这样你最后看到的，就不只是情绪判断，而是一张更接近真实协作关系的组织草图。

## 你会得到什么

当前版本已经能把多类输入整理成一条最小分析链路。它更像一个 **v0.x 可运行原型**，而不是一个面向普通用户的一键化成品。

| 能力 | 当前状态 | 说明 |
| --- | --- | --- |
| 多源材料吸收 | 可用 | 支持 `docs`、`messages`、`meetings`、`decisions`、`snapshots` 等输入 |
| 中间分析链路 | 可用 | 可产出标准化证据、线程、信号评分、关系图谱和隐性结构假设 |
| Skill 写出 | 可用 | 可将分析结果整理为后续 Agent 易消费的结构化结果 |
| 脱敏样例试跑 | 可用 | 仓库附带最小公开样例，可直接跑通主链路 |
| 一键产品体验 | 暂未完成 | 仍更适合开发者、研究者和具备执行能力的 Agent |

## 最快开始方式

第一次上手，建议直接使用仓库内的公开脱敏样例，而不是立刻拿极少量、严重缺上下文的私人截图硬跑。

```bash
git clone https://github.com/tintin3lin-pixel/org-distill-skill.git
cd org-distill-skill

python3 tools/evidence_indexer.py \
  --org-dir samples/anonymized-minimal

python3 tools/evidence_normalizer.py \
  --org-dir samples/anonymized-minimal

python3 tools/thread_reconstructor.py \
  --org-dir samples/anonymized-minimal

python3 tools/noise_filter.py \
  --org-dir samples/anonymized-minimal

python3 tools/relationship_mapper.py \
  --org-dir samples/anonymized-minimal

python3 tools/latent_structure_inferer.py \
  --org-dir samples/anonymized-minimal
```

跑完之后，你会在样例目录下看到一组中间产物，例如证据单元、线程映射、信号评分、关系图谱和隐性结构假设。更完整的首轮试跑说明，请看 [`QUICKSTART.md`](./QUICKSTART.md)。

## 作为 Skill 或 Agent 模块使用

如果你的 Agent 能做下面这些事，它基本就可以接入这个仓库：读取 `SKILL.md`、组织本地目录、执行 Python 脚本、读写 JSON / Markdown，并在中间结果之上继续生成解释层输出。

使用时，最重要的不是“让模型直接猜”，而是先让它遵循仓库里的**输入目录协议**和**分步分析链路**。

| 入口 | 作用 |
| --- | --- |
| [`SKILL.md`](./SKILL.md) | 定义 Skill 的触发条件、输入边界、执行流程和输出要求 |
| [`QUICKSTART.md`](./QUICKSTART.md) | 给第一次试跑的人一条可复制的最短路径 |
| [`docs/README.md`](./docs/README.md) | 对外文档总览，区分“必读”和“深入参考” |
| [`docs/EXTERNAL_AGENT_ADAPTATION.md`](./docs/EXTERNAL_AGENT_ADAPTATION.md) | 说明如何把当前仓库接到其他 Agent 或工作流系统里 |
| [`references/api_reference.md`](./references/api_reference.md) | 说明输入目录、关键产物字段和消费方式 |

## 公开版信息架构

为了让这个仓库可以直接作为 public 项目对外开放，当前文档已经按“先上手、再接入、再深入”的顺序收口。陌生读者不需要先读内部过程文档，也不应该先看到团队草稿。

### 对外必读

| 文档 | 你会得到什么 |
| --- | --- |
| [`README.md`](./README.md) | 项目定位、适用场景和最快入口 |
| [`QUICKSTART.md`](./QUICKSTART.md) | 第一次试跑所需的最短路径 |
| [`SKILL.md`](./SKILL.md) | 作为 Skill 安装或调用时的主协议 |
| [`samples/README.md`](./samples/README.md) | 公开脱敏样例的边界与使用方式 |
| [`docs/README.md`](./docs/README.md) | 更完整的中文文档导航 |
| [`docs/KNOWN_LIMITS_AND_MISREADINGS.md`](./docs/KNOWN_LIMITS_AND_MISREADINGS.md) | 能力边界与误读风险 |

### 深入参考

| 文档 | 适合谁 |
| --- | --- |
| [`ARCHITECTURE.md`](./ARCHITECTURE.md) | 想重构主链路或理解整体工程设计的人 |
| [`ENGINEERING_GUIDELINES.md`](./ENGINEERING_GUIDELINES.md) | 想长期维护仓库结构一致性的人 |
| [`docs/DIAGNOSIS_OUTPUT_CONTRACT.md`](./docs/DIAGNOSIS_OUTPUT_CONTRACT.md) | 想消费结果或做前后端承接的人 |
| [`docs/STANDARD_OUTPUT_CONTRACT_EXAMPLE.md`](./docs/STANDARD_OUTPUT_CONTRACT_EXAMPLE.md) | 想按标准字段做二次开发的人 |
| [`docs/FRONTEND_EXPRESSION_GUIDE.md`](./docs/FRONTEND_EXPRESSION_GUIDE.md) | 想把诊断结果写成用户可读表达的人 |
| [`references/README.md`](./references/README.md) | 想继续查方法论、分类法和字段参考的人 |

## 适合用在什么场景

这个项目适合在你已经拿到一组**能构成局部工作场景**的材料时使用。比如，一段用户自述加一段关键群聊，或者一次会议纪要加一份任务分派记录。它最适合的问题，不是“帮我判断这个人好不好相处”，而是下面这些更结构化的问题。

| 更适合的问题 | 不适合的问题 |
| --- | --- |
| 谁掌握上下文，谁在做转述与缓冲 | 单凭几句对话给某个人做性格判决 |
| 信息在哪些接口上失真 | 把输出当作 HR、法律或纪律处理依据 |
| 谁看似负责、实际没有拍板权 | 在证据极少时要求它给出确定结论 |
| 这是执行问题还是结构问题 | 把它当成零配置、零判断的一键产品 |

## 目录结构

如果你打算 fork 这个仓库继续改，最值得先理解的不是首页文案，而是主链路和目录协议。

| 目录 / 文件 | 作用 |
| --- | --- |
| `tools/` | 主分析链路脚本，包括索引、标准化、线程重建、信号过滤、关系映射与隐性结构推断 |
| `prompts/` | 面向解释层或补充分析的提示词模板 |
| `samples/anonymized-minimal/` | 公开脱敏样例，可直接用于首次验证 |
| `organizations/` | 真实运行时建议放置组织分析输入与输出的目录 |
| `docs/` | 对外说明文档，已按“必读 / 深入参考”做导航收口 |
| `references/` | 方法论、信号分类与字段参考 |

## 隐私与边界

公开仓库里的样例都是**合成脱敏数据**，用于展示目录协议、字段约定和最小可运行链路，不对应任何真实组织。你在真实场景中使用它时，仍然需要自行完成脱敏、权限控制和额外判断。

更重要的是，当前输出应被理解为**基于证据的保守假设**，而不是事实裁决。它适合做复盘、研究、协作诊断和 Agent 工作流搭建，不适合直接拿去做纪律处罚或法律判断。

详细边界请继续阅读 [`samples/README.md`](./samples/README.md) 和 [`docs/KNOWN_LIMITS_AND_MISREADINGS.md`](./docs/KNOWN_LIMITS_AND_MISREADINGS.md)。

## 项目状态

本项目当前处于 **v0.x 开源原型** 阶段。它已经足够让开发者 fork、试跑、改写和接入 Agent，但首页不承诺“即装即用的一键成品体验”。如果你正需要的，是一个可改、可接、可扩的组织分析骨架，那么它已经进入可以公开协作的状态。
