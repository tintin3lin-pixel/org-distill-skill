# Sample data

`samples/anonymized-minimal/` 是公开样例目录。先跑这套样例，再换成你自己的数据目录。

> 这份样例是合成脱敏数据，不对应任何真实个人、真实公司或真实项目。

## What is in the sample

| 路径 | 作用 |
| --- | --- |
| `samples/anonymized-minimal/meta.json` | 一次最小诊断任务的边界描述 |
| `samples/anonymized-minimal/evidence/docs/` | 背景说明和用户自述 |
| `samples/anonymized-minimal/evidence/messages/` | 群聊或消息节选 |
| `samples/anonymized-minimal/evidence/meetings/` | 会议纪要或转写节选 |
| `samples/anonymized-minimal/evidence/decisions/` | 任务分派与行动项记录 |
| `samples/anonymized-minimal/normalized/` | 标准化结果 |
| `samples/anonymized-minimal/derived/` | 线程、关系和结构假设 |
| `samples/anonymized-minimal/outputs/` | 最终结论层输出 |

## How to use it

按 `../QUICKSTART.md` 里的命令跑一遍样例。跑完后先看三处：输入目录长什么样，`derived/` 里有什么中间产物，`outputs/` 里有什么最终输出。

## What can be committed

公开仓库里只放合成样例、脱敏模板和结构示例，不放真实内部材料。

| 可以放 | 不要放 |
| --- | --- |
| 合成示例、脱敏模板、字段说明 | 真实群聊导出、真实会议纪要、真实项目代号 |
| 目录协议、运行脚本、样例 `meta.json` | 带人名、手机号、邮箱、客户名的原始材料 |
| 中间产物结构示例 | 能反推出真实组织身份的上下文碎片 |

## If you build your own sample

准备可共享样例时，至少满足下面这些要求。

| 要求 | 说明 |
| --- | --- |
| 人物不可逆 | 所有人名、群名、项目名都替换为不可逆代号 |
| 场景可理解 | 替换后仍保留最小协作逻辑 |
| 结构保留 | 不要删空请求、汇报、升级、阻塞等关键关系 |
| 边界明确 | 明确标注“合成 / 脱敏样例” |
