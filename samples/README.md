# Anonymized Sample Guide

`samples/` 目录的作用，不是替代真实世界的复杂材料，而是给第一次接触 `pmf-org-distill-skill` 的人一个**看得见、能照抄、不会泄露隐私**的起点。[1]

## 一、这份样例是什么

当前仓库附带的 `samples/anonymized-minimal/`，是一套**合成脱敏样例**。它只模拟了一个跨职能项目组里常见的推进混乱场景，用来展示这个 Skill 需要什么输入、会生成什么中间产物，以及应该如何理解输出边界。[1] [2]

> 它不是某个真实团队的改名版，也不对应任何真实个人、公司或项目。

## 二、为什么不直接放真实样本

原因很简单：这个项目面向的材料，本身往往就是最容易包含敏感信息的那类内部通讯数据，例如群聊、会议纪要、任务分派记录和项目文档。即便做过部分替换，真实样本仍然可能在上下文组合后暴露组织信息，因此当前公开仓库**不提交任何真实内部材料**。[1] [3]

| 公开仓库里允许放什么 | 公开仓库里不应放什么 |
| --- | --- |
| 合成示例、脱敏模板、字段说明 | 真实群聊导出、真实会议纪要、真实项目代号 |
| 目录协议、运行脚本、样例 `meta.json` | 带人名、手机号、邮箱、客户名的原始材料 |
| 中间产物结构示例 | 可逆推出真实组织身份的上下文碎片 |

## 三、样例目录包含什么

| 路径 | 作用 |
| --- | --- |
| `samples/anonymized-minimal/meta.json` | 一次最小诊断任务的边界描述 |
| `samples/anonymized-minimal/evidence/docs/` | 用户自述类输入 |
| `samples/anonymized-minimal/evidence/messages/` | 群聊或消息节选 |
| `samples/anonymized-minimal/evidence/meetings/` | 会议纪要或转写节选 |
| `samples/anonymized-minimal/evidence/decisions/` | 任务分派与行动项记录 |
| `samples/anonymized-minimal/normalized/` | 运行后生成的标准化结果 |
| `samples/anonymized-minimal/derived/` | 运行后生成的线程、关系与结构假设 |
| `samples/anonymized-minimal/outputs/` | 上层 Agent 或人工可继续写入的解释层产物 |

## 四、建议怎么用这份样例

第一次接触项目时，最推荐的方式不是直接读 README，而是先用样例目录跑一遍 Quickstart。这样你能更快建立三个概念：第一，输入长什么样；第二，中间产物长什么样；第三，为什么这个项目强调“保守组织假设”而不是“直接判案”。[2] [4]

## 五、如果你要自己做脱敏

如果你打算把自己的组织材料改造成可共享样例，建议至少满足下面四条原则。

| 原则 | 解释 |
| --- | --- |
| 人物不可逆 | 所有人名、群名、项目名都应替换为不可逆代号 |
| 场景可理解 | 替换后仍要保留最小协作逻辑，否则样例失去教学意义 |
| 结构保留 | 不要把请求、汇报、升级、阻塞等关键关系删空 |
| 边界明确 | 明确标注“合成 / 脱敏样例”，不要让外部误以为是真实证据 |

## References

[1]: ../README.md "pmf-org-distill-skill README"
[2]: ../QUICKSTART.md "Quickstart"
[3]: ../docs/OPEN_SOURCE_RELEASE_PLAN.md "Open Source Release Plan"
[4]: ../docs/KNOWN_LIMITS_AND_MISREADINGS.md "Known Limits and Misreadings"
