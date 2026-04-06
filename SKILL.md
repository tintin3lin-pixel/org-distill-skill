---
name: create-organization
description: Distill an organization into an analysis skill focused on information flow, role interfaces, and decision permissions. Use for: creating an organization analysis skill, mapping information flow, diagnosing management interfaces, identifying where context is lost in teams.
---

# 组织蒸馏 Skill 创建器

当用户希望把一个团队、部门、业务线或公司，从“识人”改成“识组织”来分析时，使用这个 Skill。

这个 Skill 的目标不是模仿某个人，而是基于用户提供的文档、聊天记录、会议纪要、邮件、评审意见与截图，生成一个可复用的**组织分析 Skill**。这个 Skill 应该能回答以下问题：

- 这个组织里，哪些角色真正掌握上下文。
- 关键信息是怎么从上到下、从横向到横向流动的。
- 哪些环节在压缩、损耗或阻断信息。
- 低信息输出更像个人问题，还是岗位接口与权限结构问题。

## 触发条件

当用户表达以下意图时启动：

- “帮我做一个组织蒸馏 skill”
- “把这个玩法改成识组织”
- “我想分析一个组织怎么运转”
- “给我做一个团队分析 skill”
- `/create-organization`

当用户要对已有组织 Skill 追加材料或修正判断时，进入更新模式：

- `/update-organization {slug}`
- “我又有新材料了”
- “这个判断不对，应该改成……”
- “补一批会议纪要进去”

当用户说 `/list-organizations` 时，列出所有已生成的组织 Skill。

## 核心输出

创建时必须生成以下三个部分：

| 输出文件 | 作用 |
|---|---|
| `role_interfaces.md` | 识别关键角色分别向谁输出什么、掌握哪层信息、暴露什么接口 |
| `info_flows.md` | 识别关键信息来源、传递路径、压缩节点、损耗节点 |
| `org_diagnosis.md` | 给出组织症状、权限结构、管理接口问题与改进建议 |

最后将三者合并成完整 `SKILL.md`，写入 `organizations/{slug}/`。

## 主流程

### Step 1：基础信息录入

只问最关键的四个问题：

1. 这个组织或团队叫什么名字。
2. 这次分析的边界是什么，是公司、部门、业务线还是项目组。
3. 你在其中处于什么位置，例如下属、平级协作方、中层、核心成员。
4. 你现在最想验证的组织判断是什么。

可以参考 `prompts/intake.md` 的结构来收集信息。

### Step 2：原材料导入

允许用户以以下方式提供材料：

- 上传文件
- 直接粘贴文字
- 提供飞书、钉钉、邮件等导出内容
- 追加会议纪要、评审意见、群聊截图、项目复盘

材料归档到 `organizations/{slug}/evidence/` 下，至少按 `docs`、`messages`、`meetings`、`decisions`、`snapshots` 分类。

### Step 3：组织分析

分析时不要直接问“这个人是什么性格”，而要沿三条线展开：

#### A. 角色接口分析

参考 `prompts/role_interface_analyzer.md`，重点提取：

- 哪些角色向下分发任务
- 哪些角色向上汇报结论
- 哪些角色真正掌握判断过程
- 哪些角色只是接口人或传声筒

产出 `role_interfaces.md`。

#### B. 信息流分析

参考 `prompts/info_flow_analyzer.md`，重点提取：

- 关键判断来自哪里
- 决策如何被翻译成执行要求
- 哪些环节发生上下文损耗
- 哪些岗位长期接收低信息输入

产出 `info_flows.md`。

#### C. 组织诊断分析

参考 `prompts/org_diagnosis_analyzer.md`，重点归纳：

- 低信息更像个体问题还是结构问题
- 信息断层是否明显
- 权责边界是否清晰
- 管理接口是否存在黑箱、拥堵或层层压缩

产出 `org_diagnosis.md`。

### Step 4：写入与生成

调用 `tools/org_skill_writer.py` 完成目录写入，生成：

- 完整组织 Skill：`organizations/{slug}/SKILL.md`
- 角色接口子 Skill：`organizations/{slug}/interfaces_skill.md`
- 信息流子 Skill：`organizations/{slug}/flows_skill.md`
- 组织诊断子 Skill：`organizations/{slug}/diagnosis_skill.md`
- 元数据：`organizations/{slug}/meta.json`

### Step 5：更新与进化

如果用户追加了新材料或要求修正：

- 属于角色接口的新证据，合并进 `role_interfaces.md`
- 属于信息流的新证据，合并进 `info_flows.md`
- 属于诊断判断的修正，合并进 `org_diagnosis.md`

更新前先做版本备份，并重新生成完整 Skill。

## 关键原则

第一，不要把岗位接口问题草率归因为人格问题。

第二，所有判断都尽量锚定证据类型，例如“会议纪要显示”“跨部门扯皮记录显示”“汇报链路显示”。

第三，如果原材料主要来自单一层级，就明确提示：当前蒸馏结果更像该岗位视角下的组织切片，而不是组织全貌。

第四，原材料不足时，必须明确写出“原材料不足”，而不是编造完整诊断。

## 目录约定

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
├── versions/
└── evidence/
    ├── docs/
    ├── messages/
    ├── meetings/
    ├── decisions/
    └── snapshots/
```

## 推荐调用方式

创建组织 Skill：

```bash
python3 tools/org_skill_writer.py --action create --name "商业化中台" --base-dir ./organizations
```

列出组织 Skill：

```bash
python3 tools/org_skill_writer.py --action list --base-dir ./organizations
```

更新组织 Skill：

```bash
python3 tools/org_skill_writer.py --action update --slug biz-middle-platform --base-dir ./organizations
```