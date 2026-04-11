# org-distill-skill

`org-distill-skill` 用来整理组织诊断材料。输入可以是聊天记录、会议纪要、任务分派、项目文档和截图；输出包括线程重建、关系映射、结构假设，以及最后的可读报告和结构化判断。

这个仓库按目录读取材料，然后依次执行七个脚本。你可以先跑公开样例，再把 `--org-dir` 换成自己的目录。

## Run the sample

```bash
git clone https://github.com/tintin3lin-pixel/org-distill-skill.git
cd org-distill-skill

python3 tools/evidence_indexer.py --org-dir samples/anonymized-minimal
python3 tools/evidence_normalizer.py --org-dir samples/anonymized-minimal
python3 tools/thread_reconstructor.py --org-dir samples/anonymized-minimal
python3 tools/noise_filter.py --org-dir samples/anonymized-minimal
python3 tools/relationship_mapper.py --org-dir samples/anonymized-minimal
python3 tools/latent_structure_inferer.py --org-dir samples/anonymized-minimal
python3 tools/final_report_generator.py --org-dir samples/anonymized-minimal
```

跑完后先看 `samples/anonymized-minimal/derived/` 和 `samples/anonymized-minimal/outputs/`。

## Input layout

把每次分析放在一个独立目录里。原始材料放进 `evidence/`，其余目录由脚本写入。

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

| 路径 | 放什么 |
| --- | --- |
| `meta.json` | 分析范围、用户角色、核心问题 |
| `evidence/docs/` | 背景文档、周报、交接文档、汇报材料 |
| `evidence/messages/` | 群聊记录、私聊摘录、导出消息 |
| `evidence/meetings/` | 会议纪要、录音转写、同步记录 |
| `evidence/decisions/` | 拍板记录、任务分派、责任说明 |
| `evidence/snapshots/` | 看板截图、流程截图、关键界面 |

第一次试自己的数据时，至少准备一份背景说明、一段关键对话、一份会议纪要或同步记录，再加一份任务分派材料。材料越贴近真实协作过程，结果越稳定。

## What the pipeline writes

前六步会在 `normalized/` 和 `derived/` 下写中间产物，第七步会在 `outputs/` 下写最终结论层文件。

| 目录 | 文件 | 作用 |
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

## Pipeline steps

| Step | Script | Main output |
| --- | --- | --- |
| 1 | `tools/evidence_indexer.py` | `evidence_index.json` |
| 2 | `tools/evidence_normalizer.py` | `normalized/evidence_units.json` |
| 3 | `tools/thread_reconstructor.py` | `derived/thread_map.json` |
| 4 | `tools/noise_filter.py` | `derived/signal_scores.json` |
| 5 | `tools/relationship_mapper.py` | `derived/relationship_map.json` |
| 6 | `tools/latent_structure_inferer.py` | `derived/latent_hypotheses.json` |
| 7 | `tools/final_report_generator.py` | `outputs/` 下的结论层文件 |

## Repository layout

| 路径 | 说明 |
| --- | --- |
| `tools/` | 主分析脚本 |
| `samples/` | 公开脱敏样例 |
| `docs/` | 方法、输出契约和接入说明 |
| `references/` | 字段与表达层参考 |
| `QUICKSTART.md` | 最短试跑路径 |
| `SKILL.md` | Skill 接入协议 |

## Notes

这个仓库给出的是基于证据的组织分析结果，适合复盘、研究、诊断和产品接入。它不替代法律判断、纪律处分或正式人事决策。

如果你要接 Agent、前端或工作流，直接读 `outputs/` 目录即可；如果你要调试推断过程，再回看 `normalized/` 和 `derived/`。

## Read next

| 文档 | 说明 |
| --- | --- |
| [`QUICKSTART.md`](./QUICKSTART.md) | 试跑命令、检查点和常见问题 |
| [`SKILL.md`](./SKILL.md) | Skill 接入要求和输入输出协议 |
| [`samples/README.md`](./samples/README.md) | 公开样例范围和脱敏约定 |
| [`docs/README.md`](./docs/README.md) | 文档入口 |
| [`references/README.md`](./references/README.md) | 字段和表达层参考 |
