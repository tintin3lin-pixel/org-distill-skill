# Chat CSV 兼容性验证说明

本说明用于记录 **官方 harness** 在真实微信群聊导出 CSV 样本上的兼容性修复结果，重点回答本轮改造是否已经把“整份 CSV 当作一个材料整体吸收”的旧行为，修正为“按消息逐行吸收并进入后续分析链路”的新行为。

## 修复目标

本轮修复聚焦 `tools/evidence_normalizer.py` 的输入兼容性增强，目标不是为某一份样本写特判，而是为 **群聊类 CSV 材料** 增加一条稳定、可回退的标准化分支。新的处理逻辑会先识别是否属于聊天导出 CSV，再按行读取消息，尽量保留时间戳、说话人、消息内容、附件来源和行级追踪信息。

## 本轮验证结论

在真实微信群聊导出 CSV 样本上，修复后的官方链路已经完成以下变化。

| 验证项 | 修复前 | 修复后 |
|---|---|---|
| `normalized/evidence_units.json` 中对聊天 CSV 的吸收粒度 | 整份 CSV 仅生成 1 个 evidence unit | 按行生成消息单元 |
| 官方 normalizer 对聊天 CSV 的识别方式 | 无专门识别，直接按普通文本处理 | 通过列结构识别聊天 CSV，并走逐行标准化分支 |
| 行级追踪能力 | 不具备 | `source_path` 带 `#row-{id}`，可回溯到原 CSV 行 |
| 后续链路可消费性 | 很弱，线程与关系层几乎失真 | 线程、关系、假设层均已能消费多条消息单元 |

## 核心观察

本次重跑后的 `organizations/test-org/normalized/evidence_units.json` 中，`count` 已达到 **12721**，且聊天材料从第二条起即表现为标准化后的单条消息单元，而非整份 CSV 被折叠为一个对象。这说明官方 normalizer 已能把群聊 CSV 正常拆成可分析的 message 级证据。

同时，后续官方链路已继续产出：

| 中间产物 | 本轮结果 |
|---|---|
| `derived/thread_map.json` | 已生成线程结构，并引用大量 message 级 evidence refs |
| `derived/relationship_map.json` | 已生成 **43** 条关系边 |
| `derived/latent_hypotheses.json` | 已生成保守型假设输出 |
| `outputs/readable_brief.md` | 已生成面向用户的简明结论 |

## 兼容性增强点

当前修复包含以下几项通用增强能力。

| 能力 | 说明 |
|---|---|
| 聊天 CSV 结构识别 | 通过 `talker`、`msg`、`CreateTime` 等关键列检测聊天导出格式 |
| 多消息类型兼容 | 对 `text`、`file`、`image`、`video`、`voice`、`sticker`、`location` 等类型生成规范化文本 |
| 行级元数据保留 | 保存 `row_index`、`row_id`、`MsgSvrID`、`is_sender`、`attachment_src`、`csv_columns` |
| 会话级上下文保留 | 自动补入 `conversation_id`、`topic_hint`、`thread_hint`、`context_hint` |
| @提及参与者抽取 | 从文本中提取 `@name`，补入 `participants`，改善后续关系建模基础 |

## 隐私与开源边界

本次验证使用了真实组织样本，因此 **不建议把 `organizations/test-org/` 下的原始材料与派生产物直接公开入库**。更适合公开的是：

1. `tools/evidence_normalizer.py` 的通用兼容性修复；
2. 本说明这类不暴露原文内容的验证结论；
3. 后续可补充一份脱敏或合成的最小样本，用于公开演示。

## 对外可引用的一句话版本

> 这次修复后，组织诊断 Skill 已经能把微信群聊导出 CSV 直接吸收进官方分析链路，按消息逐行标准化，再继续完成线程重建、关系映射和组织假设生成，而不再把整份聊天记录误当成单条证据。
