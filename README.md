# pmf-org-distill-skill

`pmf-org-distill-skill` 是一个从 [colleague-skill](https://github.com/titanwings/colleague-skill) 演化出来的组织蒸馏项目。它不再试图把某个同事“蒸馏成一个人格 + 工作方法的代理”，而是把蒸馏目标改成**组织的信息流、角色接口与权限结构**。[1]

这个项目的核心判断是：很多时候，一个人被蒸馏出来显得“低信息、没干货”，未必只是这个人本身没有东西，也可能是因为你手里拿到的，只是他在当前岗位上对外暴露的那一层接口。于是，原来的“识人”玩法，可以进一步升级成“识组织”玩法。

## 为什么要做这个改写

原始的 colleague-skill 把输出分成 **Work Skill** 和 **Persona** 两部分，也就是工作能力与人物风格。[1] 这对“模仿一个人”来说很自然，但对“理解一个组织怎么运转”来说还不够。

因为一个组织真正值得蒸馏的，通常不是某个人说话像不像，而是下面这些结构性问题：

| 问题类型 | 组织蒸馏要回答什么 |
|---|---|
| 角色接口 | 哪些岗位真的掌握上下文，哪些岗位只是传声筒 |
| 信息流 | 关键判断从哪里来，在哪些层被压缩、误传或损耗 |
| 权限结构 | 谁能做决策，谁只能转述结论，谁承担执行但拿不到背景 |
| 组织症状 | 为什么一线总觉得上层空，高层又觉得自己已经讲得很清楚 |

因此，本项目将 colleague-skill 的两层结构，重写为一个更适合组织分析的三层结构。

## 核心输出结构

| 文件 | 作用 |
|---|---|
| `role_interfaces.md` | 描述关键角色分别向上、向下、向平级输出什么，以及他们掌握哪层信息 |
| `info_flows.md` | 描述信息在组织中如何流动、压缩、损耗与再解释 |
| `org_diagnosis.md` | 总结组织症状、权限边界、管理接口问题与改进建议 |
| `SKILL.md` | 将三者合并为一个完整的组织分析 Skill |

换句话说，这个项目最终生成的不是“某某同事版 AI”，而是一个“这个组织怎么运转”的分析代理。

## 当前仓库状态

当前版本先实现 **MVP 骨架**，也就是先把框架、目录、关键脚手架代码与写入机制搭好，便于后续继续补 prompt、接采集器、加分析逻辑。

目前已经包含：

| 模块 | 状态 | 说明 |
|---|---|---|
| `SKILL.md` | 已完成 | 定义组织蒸馏的触发条件、主流程与输出规范 |
| `ARCHITECTURE.md` | 已完成 | 描述整体产品目标、模块映射与实现路线 |
| `tools/org_skill_writer.py` | 已完成 | 支持创建、更新、列出组织 Skill |
| `tools/evidence_indexer.py` | 已完成 | 扫描证据目录并生成索引与来源统计 |
| `prompts/` | 待补齐 | 下一步补完整的 intake / analyzer / builder 提示词 |
| `version_manager.py` | 待适配 | 将从参考项目迁移并改造成组织版本 |

## 目录结构

```text
pmf-org-distill-skill/
├── SKILL.md
├── README.md
├── ARCHITECTURE.md
├── TODO.md
├── prompts/
├── tools/
│   ├── org_skill_writer.py
│   └── evidence_indexer.py
├── organizations/
└── references/
```

生成后的组织 Skill 目录结构如下：

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

### 1. 创建一个组织 Skill

```bash
cd /path/to/pmf-org-distill-skill
python3 tools/org_skill_writer.py --action create --name "商业化中台" --base-dir ./organizations
```

### 2. 查看已生成的组织 Skill

```bash
python3 tools/org_skill_writer.py --action list --base-dir ./organizations
```

### 3. 为某个组织补充增量内容

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

## 设计原则

这个项目在设计上遵循四条原则。

第一，**尽量复用原 colleague-skill 的稳定工程骨架**，例如目录布局、写入器思路、版本管理方式，而不是完全另起炉灶。[1]

第二，**把判断重点从人格模拟切换成组织解释**。也就是说，不再把“他说话冷不冷、会不会甩锅”当成最高优先级，而是把“他在这个岗位上能看到什么、不能看到什么”当成更重要的判断对象。

第三，**所有判断都尽量与证据类型绑定**。材料来自会议纪要、群聊、评审记录还是老板发言，会直接影响我们对组织的理解深度。

第四，**先做稳定骨架，再补全复杂能力**。MVP 先搭结构与代码骨架，后续再逐步补自动采集、Prompt 细化、版本回滚和报告生成。

## 下一步开发计划

后续最重要的工作主要有三类。

| 优先级 | 事项 | 说明 |
|---|---|---|
| P0 | 完善 prompts | 补齐 intake、角色接口分析、信息流分析、组织诊断分析与 builder 模板 |
| P1 | 接入版本管理 | 将参考项目中的版本管理器改造成组织目录与文件命名 |
| P1 | 增强证据处理 | 为不同材料类型增加归档、提要、权重标注和证据链组织 |
| P2 | 保留自动采集接口 | 适配飞书、钉钉、邮件等采集器到组织分析场景 |
| P2 | 生成结构化报告 | 在 Skill 之外输出一份适合阅读的组织诊断报告 |

## 参考来源

本项目的目录结构、生成机制与最初的产品思路，直接参考了 `titanwings/colleague-skill` 开源仓库中的 `README_EN.md`、`SKILL.md`、`docs/PRD.md` 与 `tools/skill_writer.py` 等文件。[1]

## References

[1]: https://github.com/titanwings/colleague-skill "titanwings/colleague-skill"
