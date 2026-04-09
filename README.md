# 🗡️ 职场生存军师 ( org-distill-skill)

**职场生存军师** 是一个职场生态位诊断项目。

本项目呈现“打工人视角的生存决断引擎”，从真实的文档、消息和会议记录中，提炼出职场中真实存在的：**吸血背锅链条**、**时间精力内耗** 与 **核心利益去留**。

## 🎯 项目目标与定位

这个仓库是**可迭代的 MVP 工程骨架**。

从产品角度看，本项目回答以下问题：

| 侦察维度 | 本项目要回答什么 |
|---|---|
| 真实生态位 | 到底是谁在给我派烂活？谁拿了我的产出邀功？我是不是隐形背锅侠？ |
| 内耗与价值流 | 我的精力被哪些无效扯皮吸干了？我现在干的活有不可替代的护城河吗？ |
| 去留决断 | 在这里还能搞到钱、长本事、攒人脉吗？我是该【苟住】还是【提桶跑路】？ |

## 🧬 参考与结构映射

本项目直接参考了 `titanwings/colleague-skill` 的基础工程思路，但在输出结构和价值观上进行重写。二者之间的映射关系如下：

| colleague-skill | org-distill-skill (当前) | 重构逻辑 |
|---|---|---|
| `work.md` | `my_structural_reality.md` | 从“如何做事”改为“被谁白嫖、替谁背锅的生态位” |
| `persona.md` | `stay_or_leave_decision.md` | 从“人物性格”改为“极其现实的利益盘点与去留决断” |
| `knowledge/` | `evidence/` | 保持不变，作为评判职场险恶的输入弹药库 |
| `colleagues/{slug}` | `organizations/{slug}` | 每个侦察目标（组织切片）一个目录 |

## 📊 当前实现范围 (MVP 进展)

当前仓库版本已完成 **MVP 骨架**的建设，实现了 Python 工具的纯粹化与 Prompt 逻辑的业务化解耦。目前代码和文档状态如下：

| 模块 | 当前状态 | 说明 |
|---|---|---|
| `SKILL.md` | ✅ 已重构 | 顶层系统指令，已切换为职场生存与利益盘点导向 |
| `ARCHITECTURE.md` 等 | ✅ 已重构 | 工程规范与架构说明已适配新结构 |
| `tools/org_skill_writer.py` | ✅ 已适配 | 底层写入器，支持基于 reality, energy, decision 参数的增量更新 |
| `tools/evidence_indexer.py` | ✅ 已完成 | 证据雷达，扫描资料库目录并回写 meta 统计 |
| `tools/version_manager.py` | ✅ 已完成 | 时光机，支持历史版本的备份、回滚与清理 |
| `prompts/` | ✅ 灵魂注入 | 利益导向的分析/合并/排版提示词 |
| 自动采集器 | ⏳ 预留位 | 仍需针对飞书、钉钉、邮件补充自动化材料的脚本 |

## 📂 核心目录与输出结构

核心代码位于 `prompts/` 与 `tools/`。一旦创建一个生存档案，生成目录将落在 `organizations/{slug}/` 下，结构如下：

    organizations/{slug}/
    ├── my_structural_reality.md   # 【核心输出】真实生态位画像
    ├── my_energy_drain.md         # 【核心输出】内耗与价值流分析
    ├── stay_or_leave_decision.md  # 【核心输出】最终去留决断
    ├── SKILL.md                   # 针对该目标的子调度指令
    ├── meta.json                  # 档案元数据、版本号统计
    ├── evidence_index.json        # 原始资料盘点结果
    ├── versions/                  # 时光机备份目录
    └── evidence/                  # 原始材料归档目录
        ├── docs/
        ├── messages/
        ├── meetings/
        └── decisions/

## 🚀 快速开始

在工程层面，当前最常用的是三个脚本：档案写入器、证据扫描器和时光机。

**1. 建立一个新的生存档案**
    python3 tools/org_skill_writer.py --action create --name "某某业务线" --slug target-org --base-dir ./organizations

**2. 重新盘点证据弹药库** (放入材料后执行)
    python3 tools/evidence_indexer.py --org-dir ./organizations/target-org

**3. 追加新的内幕材料或修正判断** (增量更新)
    python3 tools/org_skill_writer.py \
      --action update \
      --slug target-org \
      --reality-patch ./patches/reality_patch.md \
      --energy-patch ./patches/energy_patch.md \
      --decision-patch ./patches/decision_patch.md \
      --base-dir ./organizations

**4. 查看、回滚历史版本**
    python3 tools/version_manager.py --action list --org-dir ./organizations/target-org
    python3 tools/version_manager.py --action rollback --org-dir ./organizations/target-org --version v1

## 🛡️ 开发与协作原则 (IMPORTANT)

这个项目最重要的不是一时写出多少花哨功能，而是保持整个仓库在持续迭代中**概念一致、逻辑纯粹**。后续接手开发必须遵守以下底线：

1. **禁绝管理学词汇**：我们是帮打工人排雷的军师，凡涉及业务分析的 Prompt，必须是利益第一。
2. **Python 只负责搬砖**：不要把任何字符串推断、内容解析的业务逻辑写进 Python 脚本里，代码只做文件调度，推断全部交给 Prompt。
3. **先证据、后判断**：所有新增的分析维度，都必须锚定 `evidence/` 中的真实材料，没有证据就拒绝输出结论。
4. **小步修改、全局一致**：如果要修改生成文件名或新增模块，必须先更新 `ARCHITECTURE.md` 等架构规范文档，再动代码。

## 🗺️ 下一步工作与迭代方向

接下来的高优先级迭代方向：

| 优先级 | 迭代任务 | 目的 |
|---|---|---|
| **P0** | **接入自动化采集器** | 适配飞书、钉钉接口，自动将聊天记录、会议纪要按格式清洗并归档至 `evidence/`，免除手动拖拽。 |
| **P1** | **增强证据标签系统** | 在 `evidence_indexer.py` 中增加对关键人物的标签识别，记录某份截图涉及了哪些“利益方”。 |
| **P2** | **结构化高管画像提取** | 在现有组织切片基础上，进一步反向提炼“上级/老板的防御型画像”（他最怕什么，最想要什么）。 |
| **P3** | **图谱化利益可视化** | 结合前端工具，将 `my_structural_reality.md` 中的甩锅链条生成可视化的“职场利益流向图谱”。 |

## References

[1]: https://github.com/titanwings/colleague-skill "titanwings/colleague-skill"
