# 文档总览

`docs/` 目录不再承担内部协作备忘的角色，而是专门服务于**公开仓库的外部阅读与二次开发**。如果你是第一次来到这个项目，可以把这里理解成一张中文导航页：先看必读，再按需要深入。

## 一、对外必读

下面这些文档，适合第一次接触项目、准备试跑样例、或打算把它接入自己 Agent / 工作流的开发者优先阅读。

| 文档 | 作用 | 适合谁 |
| --- | --- | --- |
| [`../README.md`](../README.md) | 项目首页，回答“这是什么、为什么要做、怎么开始” | 所有人 |
| [`../QUICKSTART.md`](../QUICKSTART.md) | 用公开脱敏样例跑通最小链路的最快路径 | 第一次试跑的人 |
| [`../SKILL.md`](../SKILL.md) | 把仓库当成 Skill 接入 Agent 时的主入口 | Agent 开发者、集成方 |
| [`../samples/README.md`](../samples/README.md) | 说明公开样例是什么、能做什么、不能代表什么 | 首次使用者 |
| [`EXTERNAL_AGENT_ADAPTATION.md`](./EXTERNAL_AGENT_ADAPTATION.md) | 说明如何接入其他 Agent 或工作流系统 | 集成方 |
| [`KNOWN_LIMITS_AND_MISREADINGS.md`](./KNOWN_LIMITS_AND_MISREADINGS.md) | 说明项目边界、误用风险与公开版不承诺的能力 | 所有人 |

## 二、深入参考

当你已经理解项目定位，准备做二次开发、前端承接或协议消费时，再进入下面这些文档会更合适。

| 文档 | 作用 | 适合谁 |
| --- | --- | --- |
| [`DIAGNOSIS_OUTPUT_CONTRACT.md`](./DIAGNOSIS_OUTPUT_CONTRACT.md) | 定义组织诊断输出层的目标、双层输出原则与表达边界 | 需要消费结果的开发者 |
| [`STANDARD_OUTPUT_CONTRACT_EXAMPLE.md`](./STANDARD_OUTPUT_CONTRACT_EXAMPLE.md) | 用标准化样例说明外部系统应优先读取哪些中间产物 | 做二次开发或工作流消费的人 |
| [`FRONTEND_EXPRESSION_GUIDE.md`](./FRONTEND_EXPRESSION_GUIDE.md) | 说明前端或表达层如何把结构判断写得清楚、克制、可传播 | 前端、产品、内容层开发者 |
| [`CHAT_CSV_COMPATIBILITY_VALIDATION.md`](./CHAT_CSV_COMPATIBILITY_VALIDATION.md) | 记录聊天 CSV 标准化兼容修复的验证结论 | 处理导出材料兼容性的人 |
| [`ORG_DISTILL_FRAMEWORK_V2.md`](./ORG_DISTILL_FRAMEWORK_V2.md) | 解释当前组织蒸馏方法的分析框架与判断骨架 | 想理解方法论的人 |

## 三、这个目录里不再放什么

为了让仓库可以直接切换为 public，`docs/` 目录不再保留以下类型的文件：

| 不再保留的内容 | 原因 |
| --- | --- |
| 内部发布计划、上线清单、下一步行动备忘 | 这类信息对外部开发者帮助有限，且容易暴露协作过程痕迹 |
| 一次性实验 runbook、个人工作草稿 | 更适合留在私有协作空间，而不是公开仓库主干 |
| 通用脚手架英文占位文档 | 会制造语言割裂感，也会降低项目完成度观感 |

## 四、建议阅读顺序

如果你只是想快速判断这个项目是否值得 fork，可以按下面顺序阅读。

1. 先看 [`../README.md`](../README.md)
2. 再看 [`../QUICKSTART.md`](../QUICKSTART.md)
3. 如果要接入 Agent，再看 [`../SKILL.md`](../SKILL.md) 与 [`EXTERNAL_AGENT_ADAPTATION.md`](./EXTERNAL_AGENT_ADAPTATION.md)
4. 如果要做产品化或二次开发，再看输出契约与深入参考文档

这套分层的目的只有一个：**让公开仓库先回答外部开发者真正关心的问题，再把更深的实现与方法论留给需要的人继续读。**
