# pmf-org-distill-skill

**pmf-org-distill-skill** 是一个把 [colleague-skill][1] 从“识人”改写为“识组织”的工程骨架。它不再试图复刻某个同事的 **persona** 与 **work style**，而是把蒸馏目标切换成一个组织在真实运转中暴露出来的三类结构：**角色接口**、**信息流路径** 与 **权限边界**。[1]

这件事的出发点很直接。很多时候，一个人之所以在蒸馏结果里显得“低信息”“没干货”，并不一定只是因为他本人没有判断力，也可能是因为外部能够拿到的材料，本来就只是他在当前岗位上对外暴露的那一层接口。于是，原本用于“识别一个人”的玩法，顺理成章地可以升级为“识别一个组织如何运转”的玩法。

## 项目目标

这个仓库当前承载的不是完整产品，而是一个**可继续生长的 MVP 工程骨架**。它要先解决的核心问题不是“自动分析得有多聪明”，而是“后续无论由谁继续开发，都能沿着同一套目录约定、文档口径和代码边界往下写”。

从产品角度看，本项目希望回答的是下表中的问题。

| 分析维度 | 本项目要回答什么 |
|---|---|
| 角色接口 | 哪些岗位真的掌握上下文，哪些岗位只是接口人、传声筒或任务分发口 |
| 信息流 | 关键判断从哪里来，经过哪些环节被翻译、压缩、误传或损耗 |
| 权限结构 | 谁能做判断，谁只负责解释，谁承担执行但拿不到背景 |
| 组织症状 | 一线为什么觉得上层很空，高层为什么觉得自己已经讲清楚了 |

因此，本项目最终要生成的不是“某位同事的 AI 替身”，而是一个能围绕**组织切片**进行解释、追问和诊断的分析 Skill。

## 与 colleague-skill 的关系

本项目直接参考了 `titanwings/colleague-skill` 的基本思路、目录组织与写入器机制。[1] 原项目将目标拆成 **Work Skill** 和 **Persona** 两部分，这对于“模仿一个人”非常自然；但当目标从“像某个人”转为“解释某个组织”，输出结构就必须改写。

二者之间的主要映射关系如下。

| colleague-skill | pmf-org-distill-skill | 改写逻辑 |
|---|---|---|
| `work.md` | `role_interfaces.md` | 从“个人如何做事”改成“岗位向外暴露什么接口、掌握哪层信息” |
| `persona.md` | `org_diagnosis.md` | 从“人物风格”改成“组织症状、权限分层与管理问题” |
| 合并后的角色 Skill | 合并后的组织 Skill | 从“这个人像不像”改成“这个组织怎么运转” |
| `knowledge/` | `evidence/` | 从个人材料归档改成组织证据归档 |
| `colleagues/{slug}` | `organizations/{slug}` | 每个组织切片一个目录 |

## 当前实现范围

当前仓库版本聚焦于 **MVP 骨架**，也就是先把目录、写入机制、提示词分层、版本管理入口和证据索引工具搭起来。这样做的目的是让后续继续开发时，不需要重新争论“项目应该长什么样”，而是可以直接在既有骨架上扩展。

目前代码和文档状态如下。

| 模块 | 当前状态 | 说明 |
|---|---|---|
| `SKILL.md` | 已完成 | 定义组织蒸馏的主入口、触发条件、输出结构与工作流 |
| `ARCHITECTURE.md` | 已完成 | 说明产品目标、模块分层、目录设计与命令体系 |
| `README.md` | 已完成 | 说明项目定位、使用方式、开发范围与协作规则 |
| `TODO.md` | 已完成 | 记录后续开发顺序、优先级与验收标准 |
| `tools/org_skill_writer.py` | 已完成 | 支持 `create`、`update`、`list` 三类动作 |
| `tools/evidence_indexer.py` | 已完成 | 扫描证据目录并生成 `evidence_index.json` |
| `tools/version_manager.py` | 已完成基础版 | 支持列出、回滚和清理历史版本 |
| `prompts/` | 已完成骨架版 | 已补齐 intake、analyzer、builder、merge 与 correction 提示词 |
| `references/` | 已完成基础版 | 已补组织信号分类与证据权重说明 |
| 自动采集器 | 预留位 | 仍需按组织分析场景适配飞书、钉钉与邮件采集 |

## 仓库目录

当前仓库建议按照如下结构理解。

```text
pmf-org-distill-skill/
├── SKILL.md
├── README.md
├── ARCHITECTURE.md
├── TODO.md
├── prompts/
│   ├── intake.md
│   ├── role_interface_analyzer.md
│   ├── info_flow_analyzer.md
│   ├── org_diagnosis_analyzer.md
│   ├── interface_builder.md
│   ├── flow_builder.md
│   ├── diagnosis_builder.md
│   ├── merger.md
│   └── correction_handler.md
├── tools/
│   ├── org_skill_writer.py
│   ├── evidence_indexer.py
│   └── version_manager.py
├── organizations/
│   └── .gitkeep
├── references/
│   ├── org_signal_taxonomy.md
│   ├── evidence_weighting.md
│   └── api_reference.md
├── scripts/
└── templates/
```

其中，真正会被项目长期依赖的核心目录是 `prompts/`、`tools/`、`organizations/` 与 `references/`。`scripts/` 和 `templates/` 是初始化骨架自带目录，当前并不是主开发重点，可以保留，也可以在后续确认无用后收缩。

## 组织 Skill 的输出结构

一旦创建某个组织切片，对应目录会落在 `organizations/{slug}/` 下，并包含至少以下文件。

| 文件 | 作用 |
|---|---|
| `role_interfaces.md` | 描述关键角色分别向上、向下、向平级输出什么，以及他们掌握哪层信息 |
| `info_flows.md` | 描述关键信息在组织中如何流动、压缩、损耗与再解释 |
| `org_diagnosis.md` | 描述组织症状、权限边界、管理接口问题与改进建议 |
| `interfaces_skill.md` | 角色接口子 Skill |
| `flows_skill.md` | 信息流子 Skill |
| `diagnosis_skill.md` | 组织诊断子 Skill |
| `SKILL.md` | 汇总三者后的完整组织分析 Skill |
| `meta.json` | 组织元数据、版本号、来源统计与诊断标记 |
| `evidence_index.json` | 证据目录扫描结果 |
| `versions/` | 历史版本备份目录 |
| `evidence/` | 原始材料归档目录 |

推荐的组织目录结构如下。

```text
organizations/{slug}/
├── SKILL.md
├── role_interfaces.md
├── info_flows.md
├── org_diagnosis.md
├── interfaces_skill.md
├── flows_skill.md
├── diagnosis_skill.md
├── meta.json
├── evidence_index.json
├── versions/
└── evidence/
    ├── docs/
    ├── messages/
    ├── meetings/
    ├── decisions/
    └── snapshots/
```

## 快速开始

在工程层面，当前最常用的是三个脚本：组织 Skill 写入器、证据索引器和版本管理器。下面的命令基于当前已实现的接口编写。

### 1. 创建一个新的组织 Skill

```bash
cd /path/to/pmf-org-distill-skill
python3 tools/org_skill_writer.py --action create --name "商业化中台" --base-dir ./organizations
```

如果你已经准备好了更完整的元数据和三份分析文件，也可以在创建时显式传入。

```bash
python3 tools/org_skill_writer.py \
  --action create \
  --slug biz-middle-platform \
  --meta ./meta.json \
  --interfaces ./role_interfaces.md \
  --flows ./info_flows.md \
  --diagnosis ./org_diagnosis.md \
  --base-dir ./organizations
```

### 2. 查看已经创建过的组织 Skill

```bash
python3 tools/org_skill_writer.py --action list --base-dir ./organizations
```

### 3. 追加增量判断或修正某个组织 Skill

```bash
python3 tools/org_skill_writer.py \
  --action update \
  --slug biz-middle-platform \
  --interfaces-patch ./patches/interfaces_patch.md \
  --flows-patch ./patches/flows_patch.md \
  --diagnosis-patch ./patches/diagnosis_patch.md \
  --base-dir ./organizations
```

### 4. 重新索引证据目录

```bash
python3 tools/evidence_indexer.py --org-dir ./organizations/biz-middle-platform
```

### 5. 查看、回滚或清理历史版本

```bash
python3 tools/version_manager.py --action list --org-dir ./organizations/biz-middle-platform
python3 tools/version_manager.py --action rollback --org-dir ./organizations/biz-middle-platform --version v1
python3 tools/version_manager.py --action cleanup --org-dir ./organizations/biz-middle-platform --keep 10
```

## 开发与协作原则

这个项目最重要的不是一时写出多少功能，而是保持整个仓库在持续迭代中**概念一致、命名一致、目录一致、输出一致**。如果这些基本秩序先乱了，后面的 Prompt、采集器和分析器越多，整个项目反而会越难维护。

因此，当前仓库默认遵守以下原则。

| 原则 | 含义 |
|---|---|
| 先骨架、后智能 | 优先保证目录、接口和输出稳定，再补复杂分析能力 |
| 先证据、后判断 | 所有组织结论都尽量锚定材料来源与证据类型 |
| 先结构、后性格 | 优先判断岗位接口和信息分层，避免轻易把问题归因为人格缺陷 |
| 先兼容、后重构 | 尽量复用原项目稳定结构，减少迁移成本 |
| 小步修改、全局一致 | 每次改动不宜太散，改一处就同步更新文档与命名约定 |

如果后续由另一个代码助手继续开发，建议把本仓库视为**规范先于功能**的项目。也就是说，在新增功能前，先确保文档、命名和接口约定不被破坏。

## 建议的开发顺序

从工程推进角度看，当前最合理的顺序不是同时铺开所有方向，而是先把最影响一致性的部分稳定下来。建议顺序如下。

| 顺序 | 任务 | 原因 |
|---|---|---|
| 1 | 固化 README、ARCHITECTURE、TODO 与工程规范文档 | 先统一项目语言和边界 |
| 2 | 让 `org_skill_writer.py`、`evidence_indexer.py`、`version_manager.py` 通过基础自测 | 先稳住核心脚手架 |
| 3 | 用一个样例组织目录跑通 create / update / index / rollback | 先验证最小闭环 |
| 4 | 细化 `prompts/` 的输入输出格式 | 让后续分析逻辑有统一模板 |
| 5 | 再接入飞书、钉钉、邮件等采集器 | 避免上游接得太早、下游结构未稳 |
| 6 | 最后补报告生成、可视化和更复杂的自动化能力 | 在稳定骨架上扩展，而不是反过来 |

## GitHub 与仓库管理建议

按照当前约定，所有相关仓库建议统一以 **`pmf-`** 作为前缀，便于后续在同一账号下进行项目管理与横向识别。对于新建远程仓库，默认应优先使用**私有仓库**，除非用户明确要求公开，以降低中间版本和半成品暴露的风险。

在协作方式上，GitHub 应承担的是**版本管理与协作审阅**的角色，而不是替代本地结构设计。也就是说，本地目录、文档和脚本必须先能自洽，再推送到远程；否则远程仓库只会放大不一致，而不会自动修复它。

## 下一步工作

当前阶段，最值得优先推进的工作主要有三类。第一，是继续完善工程规范，让不同开发者或不同代理接手时仍然写在同一套框架里。第二，是补齐样例与自测，让脚手架从“看起来完整”变成“确实能跑通最小闭环”。第三，是在此基础上再逐步增加更复杂的采集与分析能力。

更细的待办事项已经整理在 `TODO.md` 中。建议后续所有实现，都以 `ARCHITECTURE.md` 和工程规范文档为边界，再决定是否改动目录、命名或行为接口。

## 参考来源

本仓库的整体改写思路、目录映射与初始实现方式，主要参考 `titanwings/colleague-skill` 开源仓库中的 `README_EN.md`、`SKILL.md`、`docs/PRD.md` 与 `tools/skill_writer.py` 等内容。[1]

## References

[1]: https://github.com/titanwings/colleague-skill "titanwings/colleague-skill"
