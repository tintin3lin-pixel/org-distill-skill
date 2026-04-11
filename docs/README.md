# Documentation

`docs/` 里放方法文档、输出契约和接入说明。先跑样例，再按需要查对应文件。

## Start here

第一次进入仓库，先看下面这几份。

| 文档 | 用途 | 适合谁 |
| --- | --- | --- |
| [`../README.md`](../README.md) | 了解项目定位、输入输出和目录结构 | 所有人 |
| [`../QUICKSTART.md`](../QUICKSTART.md) | 用公开样例快速试跑 | 第一次使用者 |
| [`../SKILL.md`](../SKILL.md) | 按 Skill 方式接入仓库 | Agent 开发者、集成方 |
| [`../samples/README.md`](../samples/README.md) | 查看公开样例的范围和限制 | 第一次使用者 |
| [`EXTERNAL_AGENT_ADAPTATION.md`](./EXTERNAL_AGENT_ADAPTATION.md) | 了解外部 Agent 或工作流接入方式 | 集成方 |
| [`KNOWN_LIMITS_AND_MISREADINGS.md`](./KNOWN_LIMITS_AND_MISREADINGS.md) | 查看已知局限和常见误读 | 所有人 |

## Build and integration

跑通主链路后，继续看下面这些文件。

| 文档 | 用途 | 适合谁 |
| --- | --- | --- |
| [`DIAGNOSIS_OUTPUT_CONTRACT.md`](./DIAGNOSIS_OUTPUT_CONTRACT.md) | 定义诊断输出层结构和边界 | 结果消费方、后端开发者 |
| [`STANDARD_OUTPUT_CONTRACT_EXAMPLE.md`](./STANDARD_OUTPUT_CONTRACT_EXAMPLE.md) | 提供标准输出样例 | 二次开发者、工作流集成方 |
| [`FRONTEND_EXPRESSION_GUIDE.md`](./FRONTEND_EXPRESSION_GUIDE.md) | 说明前端和表达层如何展示结果 | 前端、产品、内容层开发者 |
| [`ORG_DISTILL_FRAMEWORK_V2.md`](./ORG_DISTILL_FRAMEWORK_V2.md) | 说明当前分析框架 | 需要理解方法的人 |

## Reading order

如果你只是想判断仓库能不能用，按下面顺序读。

| 顺序 | 文档 | 目的 |
| --- | --- | --- |
| 1 | [`../README.md`](../README.md) | 先看输入、输出和目录结构 |
| 2 | [`../QUICKSTART.md`](../QUICKSTART.md) | 跑通公开样例 |
| 3 | [`../SKILL.md`](../SKILL.md) | 了解 Skill 接入方式 |
| 4 | [`EXTERNAL_AGENT_ADAPTATION.md`](./EXTERNAL_AGENT_ADAPTATION.md) | 设计外部 Agent 接入 |
| 5 | 输出契约与框架文档 | 做产品化、接前端或二次开发 |

## What is in this directory

| 类型 | 你会看到什么 |
| --- | --- |
| 接入说明 | `EXTERNAL_AGENT_ADAPTATION.md` 等接入文档 |
| 输出契约 | 输出字段、样例和消费方式 |
| 方法文档 | 当前分析框架和已知限制 |
