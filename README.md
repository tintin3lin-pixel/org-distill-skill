# org-distill-skill

大家都在蒸馏个人。

蒸馏同事，蒸馏老板，蒸馏前同事，蒸馏“那个总在群里发一句话就消失的人”。既然都蒸到这一步了，我们不如把尺度再拉大一点：**别只蒸馏一个人了，直接蒸馏整个组织。**

说白了，很多打工人的真正问题，从来不只是“这个同事烦不烦”或者“老板是不是情绪不稳定”。更真实的问题是：**这家公司到底怎么运转，信息到底怎么流，谁在拍板，谁在背锅，我在里面到底算什么位置，我还值不值得继续留。**

这个仓库就是为这件事做的。

它是一个开源 Skill / 分析骨架。你把自己手上已经看得到的材料——比如群聊记录、会议纪要、工作文档、任务分派、决策痕迹、阶段性截图——按目录放进去，它就会尝试从这些“信息界面”里，反向还原你所在组织的真实运转方式。

## 这到底是什么

**通过你已经接触到的信息切面，重建组织里的信息流、关系链、决策权和责任分配。**

很多时候，最折磨人的不是工作量，而是你根本不知道：为什么信息总晚你一步，为什么你负责却没有权限，为什么有人天天发号施令但关键时刻又不担责。你以为自己在处理“人际问题”，其实你撞到的是一整套组织结构问题。

| 你脑子里真正想问的 | 这个项目想帮你看清什么 |
| --- | --- |
| 这家公司到底靠不靠谱 | 信息流是不是长期混乱，决策是不是稳定，责任是不是总在下沉 |
| 我在里面到底是什么位置 | 你是 owner、缓冲层、传话筒、执行核心，还是标准背锅位 |
| 我现在难受，是暂时磨合还是系统性问题 | 这是阶段性混乱，还是组织本身就有结构性消耗 |
| 我该不该继续留 | 你看到的是成长空间，还是一个会持续榨干上下文的人肉中间层 |

“蒸馏个人”已经很火了，而现实一点说，**你老板大概率也已经在想怎么用 AI 提高效率、替代流程，甚至替代某些人。** 既然打不过，那就先加入。

与其被动等别人分析你，不如先把你所在的组织看明白。

我们“说不清楚但天天发生”的东西，整理成一个可以复盘、可以讨论、可以继续扩展的分析过程。

## 你怎么用它

最简单的理解方式就是四步：**fork 一份自己的副本，放入你的私有材料，运行分析链路，读结果。**

| 步骤 | 你要做什么 | 结果是什么 |
| --- | --- | --- |
| 第一步 | fork 或复制这个仓库，作为你自己的版本 | 你有了一个可以自由修改的组织蒸馏工作台 |
| 第二步 | 把你的材料放进 `organizations/<your-org>/evidence/` | 项目拿到组织运转的原始证据 |
| 第三步 | 跑一遍分析链路 | 原始材料被整理成线程、关系、信号和结构假设 |
| 第四步 | 继续生成最终结论层输出 | 你会得到易读摘要、结构化去留判断和证据映射 |

## 你的数据应该放哪

你自己的真实材料，应该放在下面这个目录结构里：

```text
organizations/
  your-org/
    evidence/
      docs/
      messages/
      meetings/
      decisions/
      snapshots/
```

这些目录分别对应不同证据来源。你可以从最小集开始，不用一上来就把所有历史都塞进去。通常来说，一段关键群聊、一份会议纪要、一个任务交接文档，再加几张关键截图，就已经足够还原出一部分真实结构了。

| 目录 | 适合放什么 |
| --- | --- |
| `docs/` | 方案文档、交接文档、周报、汇报材料 |
| `messages/` | 群聊记录、私聊摘录、沟通转写 |
| `meetings/` | 会议纪要、录音转写、会后结论 |
| `decisions/` | 拍板记录、任务分配、口头决策整理 |
| `snapshots/` | 流程截图、任务看板、关键界面截图 |

## 最小上手路径

如果你只是想先看懂这套东西怎么跑，建议先用仓库里的公开样例过一遍，再换成你自己的材料。这样你会更容易理解每一步到底在干什么，而不是一上来就把私人数据扔进去然后盯着输出发愣。

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

如果你已经准备好换成自己的数据，把上面的 `samples/anonymized-minimal` 改成你自己的组织目录，比如：

```bash
python3 tools/evidence_indexer.py --org-dir organizations/your-org
python3 tools/evidence_normalizer.py --org-dir organizations/your-org
python3 tools/thread_reconstructor.py --org-dir organizations/your-org
python3 tools/noise_filter.py --org-dir organizations/your-org
python3 tools/relationship_mapper.py --org-dir organizations/your-org
python3 tools/latent_structure_inferer.py --org-dir organizations/your-org
python3 tools/final_report_generator.py --org-dir organizations/your-org
```

跑完之后，你会同时看到一组中间结果和四个最终输出文件。它们仍然不是“命运判决书”，而是把组织蒸馏过程收束成更容易消费的结论层：哪些线程在反复断裂，谁总是拥有上下文，谁总是在传话，谁承担结果但没有对应权限，以及当前更接近“继续修”还是“准备撤退”的保守判断。

## 你最终能得到什么


| 最终你会读到的东西 | 作用 |
| --- | --- |
| `outputs/analysis_report.md` | 查看严谨版组织诊断报告 |
| `outputs/readable_brief.md` | 快速读懂一句话判词、你的位置和留走倾向 |
| `outputs/stay_leave_assessment.json` | 让 Agent、前端或工作流读取结构化结论 |
| `outputs/evidence_trace.json` | 回看关键判断到底对应了哪些证据 |

| 最终你可能看清的东西 | 典型表现 |
| --- | --- |
| 信息到底卡在哪 | 同样的问题反复转述，关键上下文只掌握在少数人手里 |
| 谁在真正驱动协作 | 表面 owner 和实际 owner 不是一个人 |
| 谁在承担结构性风险 | 有人负责结果，但没有资源、权限和前置信息 |
| 组织问题是偶发还是系统性的 | 混乱是不是长期重复出现，而不是某次单点事故 |
| 你的位置值不值得继续投入 | 你是在积累势能，还是只是在高强度消耗自己 |

如果你最近经常有这种感觉——活是你干，信息不给你，决策不是你做，锅最后还得你背——那你大概率不是单纯“最近状态不好”。你可能只是终于开始看见组织本身了。


## 这个仓库目前是什么状态

当前版本是一个**可 fork、可试跑、可继续改写的 v0.x 开源原型**。

它已经足够让你把自己的材料接进来，跑出第一轮组织蒸馏结果，并继续生成一套保守但可直接消费的最终结论层输出；但它还不是那种“上传一个压缩包，立刻生成完美报告”的消费级产品。如果你想要的是一个能自己继续改、能接 Agent、能接前端、能接工作流的开源骨架，那它已经进入能直接公开协作的状态。

## 从哪里继续看

如果你已经决定试试，可以看看几个文件。

| 文档 | 作用 |
| --- | --- |
| [`QUICKSTART.md`](./QUICKSTART.md) | 第一轮试跑的最短路径 |
| [`SKILL.md`](./SKILL.md) | 作为 Skill 接入时的执行协议 |
| [`samples/README.md`](./samples/README.md) | 公开样例怎么组织、边界在哪 |
| [`docs/README.md`](./docs/README.md) | 对外文档总入口 |
| [`references/README.md`](./references/README.md) | 方法论和字段参考 |

