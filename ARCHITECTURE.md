# pmf-org-distill-skill 架构设计

## 一、项目目标

这个项目不是再去“蒸馏一个人”，而是把原来的 colleague-skill 改写成一个**识别组织信息流、权限边界与经验沉淀方式**的 meta-skill。

它的核心输出不再是 `work + persona` 两件套，而是围绕组织运转本身生成三类结果：

| 输出层 | 目标 | 对应文件 |
|---|---|---|
| Interface Layer | 识别不同岗位对外暴露的信息接口与行为接口 | `role_interfaces.md` |
| Flow Layer | 识别信息如何在组织内流动、压缩、损耗、升级 | `info_flows.md` |
| Diagnostic Layer | 归纳组织症状、权限结构、管理风险与改进建议 | `org_diagnosis.md` |

最终生成的完整 Skill，不是模仿某个人说话，而是让代理在面对“这个组织怎么运转”“为什么这里的人蒸出来都很空”“哪个岗位拿不到上下文”这类问题时，能够按照材料里呈现出的组织逻辑来分析与回答。

## 二、产品定位

这个 Skill 本质上是一个**组织蒸馏器**。

它服务的不是“替代某个同事”，而是帮助用户从聊天记录、文档、会议纪要、评审意见、老板指令、跨部门扯皮记录等材料里，提炼出三件事情：第一，哪些角色掌握了真正的上下文；第二，信息是如何在不同层级之间被翻译和损耗的；第三，低信息输出究竟是个人问题，还是组织接口问题。

## 三、与 colleague-skill 的结构映射

| colleague-skill 旧结构 | org-distill 新结构 | 改造说明 |
|---|---|---|
| `work.md` | `role_interfaces.md` | 从个人做事方法改为岗位对外接口、职责边界、可见信息层 |
| `persona.md` | `org_diagnosis.md` | 从个人风格改为组织症状、管理风格、权限分布、风险判断 |
| 合并 SKILL | `SKILL.md` | 改为组织分析代理，默认先读接口，再看流动，再做诊断 |
| `knowledge/` | `evidence/` | 原材料按文档、消息、会议、结构化记录分类归档 |
| `colleagues/{slug}` | `organizations/{slug}` | 每个组织或团队一个目录 |

## 四、核心工作流

### 1. Intake

用户触发 `/create-organization` 后，不是先描述某个人，而是先描述这个组织的观察范围。最少需要四类输入：组织名或代号、分析边界、用户所处位置、已有材料来源。

建议的 intake 字段如下：

| 字段 | 说明 |
|---|---|
| `name` | 组织、团队、业务线或项目组名称 |
| `scope` | 本次要蒸馏的是整个公司、某个部门、某个业务单元还是项目组 |
| `user_position` | 用户在其中的位置，如下属、平级协作方、中层管理者、核心成员 |
| `org_hypothesis` | 用户的初始判断，例如“高层有判断但传不到一线” |
| `sources` | 飞书、钉钉、邮件、会议纪要、评审文档、群聊截图等 |

### 2. Evidence Ingestion

数据导入保留 colleague-skill 的自动采集思路，但分析目标改变：不再主要按“谁说过什么”拆，而是按“什么材料能证明组织怎么运转”拆。

原材料归档建议如下：

```text
organizations/{slug}/evidence/
├── docs/
├── messages/
├── meetings/
├── decisions/
└── snapshots/
```

### 3. Analysis Pipeline

组织蒸馏的分析分三条线并行概念化，但在实现上可以先串行：

#### A. Role Interface Analyzer

提取不同岗位的对外接口，回答：

- 这个角色通常向下输出什么
- 这个角色通常向上汇报什么
- 这个角色掌握的是上下文、判断过程，还是已经压缩过的结论
- 这个角色的典型行为是分发任务、协调冲突、做取舍，还是只负责传声

输出文件：`role_interfaces.md`

#### B. Information Flow Analyzer

提取信息流路径，回答：

- 关键判断来自哪里
- 在哪些层级发生了压缩
- 哪些接口存在上下文丢失
- 哪些岗位长期处于低信息输入/输出状态

输出文件：`info_flows.md`

#### C. Organization Diagnosis Analyzer

基于前两者归纳组织症状，回答：

- 低信息到底更像个人问题还是结构问题
- 组织是否存在“上层有判断，下层只收口号”的断层
- 是否存在接口拥堵、职责模糊、过度汇报、决策黑箱等现象
- 如果要改进，最优先补什么接口

输出文件：`org_diagnosis.md`

## 五、生成内容规范

### 1. role_interfaces.md

这个文件描述组织中关键角色分别暴露了什么信息层、承担什么接口责任。建议固定结构如下：

```markdown
# 角色接口画像

## 角色一：直属老板
### 对下输出
### 对上输出
### 对平级协作输出
### 可见信息层
### 典型接口问题

## 角色二：中层负责人
...
```

### 2. info_flows.md

这个文件描述信息在组织中的来源、路径、损耗点与放大点。建议固定结构如下：

```markdown
# 信息流画像

## 关键信息源
## 主要流动路径
## 压缩与损耗节点
## 权限边界
## 高信息岗位与低信息岗位
## 典型断层案例
```

### 3. org_diagnosis.md

这个文件是最终判断层。建议固定结构如下：

```markdown
# 组织诊断

## 组织运转摘要
## 主要症状
## 权限结构判断
## 信息分层判断
## 管理接口判断
## 风险列表
## 优先级最高的改进建议
```

## 六、代码模块设计

代码层保持与原项目相似的“prompt + writer + versioning + collectors”结构，但变量名和输出目标改成组织导向。

```text
pmf-org-distill-skill/
├── SKILL.md
├── ARCHITECTURE.md
├── README.md
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
│   ├── version_manager.py
│   ├── evidence_indexer.py
│   ├── feishu_auto_collector.py
│   ├── dingtalk_auto_collector.py
│   └── email_parser.py
├── organizations/
│   └── .gitkeep
└── references/
    ├── org_signal_taxonomy.md
    └── evidence_weighting.md
```

## 七、核心数据结构

建议 `meta.json` 至少包含以下字段：

```json
{
  "name": "商业化中台",
  "slug": "biz-middle-platform",
  "scope": "销售支持与交付协同",
  "user_position": "平级协作方",
  "org_hypothesis": "高层判断没有有效传导到执行层",
  "version": "v1",
  "created_at": "2026-04-06T00:00:00Z",
  "updated_at": "2026-04-06T00:00:00Z",
  "source_stats": {
    "docs": 0,
    "messages": 0,
    "meetings": 0,
    "decisions": 0
  },
  "diagnostic_flags": [
    "possible_context_loss",
    "unclear_decision_boundary"
  ]
}
```

## 八、命令设计

| 命令 | 作用 |
|---|---|
| `/create-organization` | 创建一个新的组织蒸馏项目 |
| `/update-organization {slug}` | 追加新材料或修正已有判断 |
| `/list-organizations` | 列出所有已生成的组织 Skill |
| `/organization-rollback {slug} {version}` | 回滚到某个历史版本 |

## 九、MVP 实现范围

第一版先做最小可用框架，不追求把所有采集器都重写完。

MVP 范围包括：

| 模块 | 本轮状态 |
|---|---|
| Skill 入口 SKILL.md | 实现 |
| prompts 骨架 | 实现 |
| `org_skill_writer.py` | 实现 |
| `version_manager.py` | 适配实现 |
| `evidence_indexer.py` | 实现基础版 |
| Feishu / DingTalk / 邮件采集器 | 先保留接口与占位说明 |
| GitHub 仓库初始化 | 实现 |

## 十、实现原则

第一，保持与原项目足够相似，这样迁移成本最低。

第二，输出重心从“模仿一个人”切换到“解释一个组织”。

第三，所有生成结果都必须带上“证据意识”，也就是不要直接下人格结论，而要尽量说明这是从哪些材料、哪个岗位接口、哪条信息路径里推出来的。

第四，先搭出稳定骨架，再逐步替换具体 prompt 与采集器。
