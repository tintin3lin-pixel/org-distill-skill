# Quickstart

## Run the sample

在仓库根目录执行下面这组命令。第七步会写入最终结论层输出。

```bash
python3 tools/evidence_indexer.py --org-dir samples/anonymized-minimal
python3 tools/evidence_normalizer.py --org-dir samples/anonymized-minimal
python3 tools/thread_reconstructor.py --org-dir samples/anonymized-minimal
python3 tools/noise_filter.py --org-dir samples/anonymized-minimal
python3 tools/relationship_mapper.py --org-dir samples/anonymized-minimal
python3 tools/latent_structure_inferer.py --org-dir samples/anonymized-minimal
python3 tools/final_report_generator.py --org-dir samples/anonymized-minimal
```

跑完后先看 `samples/anonymized-minimal/derived/` 和 `samples/anonymized-minimal/outputs/`。

## Check the outputs

| 目录 | 文件 | 说明 |
| --- | --- | --- |
| `normalized/` | `evidence_units.json` | 标准化后的证据单元 |
| `derived/` | `thread_map.json` | 线程和上下文重建结果 |
| `derived/` | `signal_scores.json` | 信号评分和噪声过滤结果 |
| `derived/` | `relationship_map.json` | 协作、请求、升级和阻塞关系 |
| `derived/` | `latent_hypotheses.json` | 结构假设与支撑证据 |
| `outputs/` | `analysis_report.md` | 完整分析报告 |
| `outputs/` | `readable_brief.md` | 简明摘要 |
| `outputs/` | `stay_leave_assessment.json` | 结构化去留判断 |
| `outputs/` | `evidence_trace.json` | 结论到证据的映射 |

## Run your own directory

把 `samples/anonymized-minimal` 换成你自己的组织目录，例如：

```bash
python3 tools/evidence_indexer.py --org-dir organizations/your-org
python3 tools/evidence_normalizer.py --org-dir organizations/your-org
python3 tools/thread_reconstructor.py --org-dir organizations/your-org
python3 tools/noise_filter.py --org-dir organizations/your-org
python3 tools/relationship_mapper.py --org-dir organizations/your-org
python3 tools/latent_structure_inferer.py --org-dir organizations/your-org
python3 tools/final_report_generator.py --org-dir organizations/your-org
```

目录结构保持下面这样：

```text
organizations/
  your-org/
    meta.json
    evidence/
      docs/
      messages/
      meetings/
      decisions/
      snapshots/
    normalized/
    derived/
    outputs/
```

| 路径 | 内容 |
| --- | --- |
| `meta.json` | 诊断范围、用户角色、核心问题 |
| `evidence/docs/` | 背景文档、周报、岗位说明、用户自述 |
| `evidence/messages/` | 群聊、私聊摘录、消息导出 |
| `evidence/meetings/` | 会议纪要、转写、同步记录 |
| `evidence/decisions/` | 分工、拍板、责任说明 |
| `evidence/snapshots/` | 看板、流程、界面截图 |

## Minimum input

第一次试自己的数据时，先准备下面这些材料。

| 材料类型 | 放置目录 | 说明 |
| --- | --- | --- |
| 背景说明 | `evidence/docs/` | 项目背景、岗位说明、用户自述 |
| 沟通记录 | `evidence/messages/` | 群聊、私聊摘录、导出记录 |
| 会议纪要 | `evidence/meetings/` | 周会、复盘会、同步会纪要 |
| 任务分派 | `evidence/decisions/` | 分工、拍板、责任说明 |
| 截图材料 | `evidence/snapshots/` | 看板、流程、界面或关键截图 |

## Checkpoints

第一次跑通后，先看下面几个文件。

| 文件 | 先看什么 | 正常表现 |
| --- | --- | --- |
| `normalized/evidence_units.json` | 条目数量和样本内容 | 原始材料已经被拆成证据单元 |
| `derived/thread_map.json` | 线程摘要和参与人 | 上下文能基本串起来 |
| `derived/relationship_map.json` | 关系边和解释字段 | 协作结构已经可见 |
| `derived/latent_hypotheses.json` | 假设文本和证据引用 | 已形成第一版结构判断 |
| `outputs/readable_brief.md` | 核心结论和摘要语气 | 已生成面向人的最终输出 |
| `outputs/stay_leave_assessment.json` | `recommendation` 和 `next_actions` | 已生成可供程序消费的结论 |

## FAQ

| 问题 | 处理方式 |
| --- | --- |
| 输入太少，结论发散 | 补一段关键对话或一份任务分派记录 |
| 最终摘要太薄 | 回看 `latent_hypotheses.json` 和 `relationship_map.json`，补充高价值证据 |
| 想接 Agent 或工作流 | 直接消费 `outputs/` 目录里的四个最终文件 |
| 想看协议和适配方式 | 继续阅读 `SKILL.md` 和 `docs/EXTERNAL_AGENT_ADAPTATION.md` |

