"""
职场生存军师 Skill 文件写入器。

负责将生成的 my_structural_reality.md、my_energy_drain.md、stay_or_leave_decision.md
写入到标准目录结构，并生成 meta.json 与完整 SKILL.md。
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


SKILL_MD_TEMPLATE = """---
name: survival_guide_{slug}
description: {name} 的职场生态位与去留生存指南
---

# {name} 职场生存指南

## 侦察范围

- **组织/目标名称**：{name}
- **分析边界**：{scope}
- **我的当前位置**：{user_position}
- **我的初始怀疑**：{org_hypothesis}

---

## PART A：我的真实生态位 (谁在吸血，我在替谁背锅？)

{reality_content}

---

## PART B：我的内耗与价值流 (我在做无用功吗？)

{energy_content}

---

## PART C：去留决断 (赶紧跑还是继续苟？)

{decision_content}

---

## 生存推演规则

接收到与该环境相关的问题时，按如下“职场马基雅维利”原则处理：

1. **禁用管理学黑话**：不要说“赋能、对齐、颗粒度”，直接翻译成“替人干活、陪人开会、细节背锅”。
2. **利益绝对优先**：分析任何事情，只看“我”赚了（权力、经验、钱、闲）还是亏了（精力、情绪、背锅风险）。
3. **识别真实权力**：谁能决定你的绩效？谁在拿你的成果邀功？指出真正的利益链条。
4. **结论先行**：如果用户问“怎么办”，直接给出【苟着】、【提桶跑路】或【虚与委蛇】的明确策略及理由。
5. **证据不足不乱猜**：如果材料看不出深浅，直接说“聊天记录不够，看不出这里面的水有多深”。
"""


REALITY_ONLY_TEMPLATE = """---
name: survival_{slug}_reality
description: {name} 的真实生态位画像
---

{reality_content}
"""


ENERGY_ONLY_TEMPLATE = """---
name: survival_{slug}_energy
description: {name} 的内耗与价值流分析
---

{energy_content}
"""


DECISION_ONLY_TEMPLATE = """---
name: survival_{slug}_decision
description: {name} 的去留决断
---

{decision_content}
"""


DEFAULT_REALITY = """# 真实生态位画像

## 当前探测状态

**⚠️ 证据不足，无法定位你的真实生态位。**

## 建议补充弹药

想知道你是不是“工具人”或者“背锅侠”？优先补充能够体现“谁在给你派活，你做完给了谁”的材料：
- 领导给你派活的聊天截图
- 跨部门扯皮、甩锅的群聊记录
- 你的汇报对象对你工作成果的评价或修改意见
"""


DEFAULT_ENERGY = """# 内耗与价值流分析

## 当前探测状态

**⚠️ 证据不足，无法计算你的精力损耗率。**

## 建议补充弹药

想知道你的时间是不是被狗吃了？优先补充以下材料：
- 没完没了的拉齐会议纪要
- 流程审批卡点的截图
- 领导朝令夕改的指令记录
- 你每天高频对接的人的沟通记录
"""


DEFAULT_DECISION = """# 去留决断

## 当前探测状态

**⚠️ 证据不足，现在瞎建议你离职或留下都是害你。**

## 决断核心原则

别谈什么“公司愿景”和“团队氛围”。在补齐材料前，先问自己三个极其现实的问题：
1. 在这里，我能赚到高于市场价的钱吗？
2. 在这里，我能学到下家愿意高薪买单的本事吗？
3. 在这里，我能攒下以后用得着的靠谱人脉吗？
（如果都是 NO，你其实心里已经有答案了）
"""


def slugify(name: str) -> str:
    text = name.strip().lower()
    text = re.sub(r"[^a-z0-9\u4e00-\u9fff\-_\s]", "", text)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "organization"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_text(path: Optional[str], default: str) -> str:
    if not path:
        return default
    return Path(path).read_text(encoding="utf-8").strip() or default


def render_skill_md(meta: dict, slug: str, reality_content: str, energy_content: str, decision_content: str) -> str:
    return SKILL_MD_TEMPLATE.format(
        slug=slug,
        name=meta.get("name", slug),
        scope=meta.get("scope", "未指定"),
        user_position=meta.get("user_position", "未指定"),
        org_hypothesis=meta.get("org_hypothesis", "暂无"),
        reality_content=reality_content,
        energy_content=energy_content,
        decision_content=decision_content,
    )


def create_skill(
    base_dir: Path,
    slug: str,
    meta: dict,
    reality_content: str,
    energy_content: str,
    decision_content: str,
) -> Path:
    org_dir = base_dir / slug
    org_dir.mkdir(parents=True, exist_ok=True)

    for subdir in (
        "versions",
        "evidence/docs",
        "evidence/messages",
        "evidence/meetings",
        "evidence/decisions",
        "evidence/snapshots",
    ):
        (org_dir / subdir).mkdir(parents=True, exist_ok=True)

    # 【核心改动】修改了输出的文件名
    (org_dir / "my_structural_reality.md").write_text(reality_content + "\n", encoding="utf-8")
    (org_dir / "my_energy_drain.md").write_text(energy_content + "\n", encoding="utf-8")
    (org_dir / "stay_or_leave_decision.md").write_text(decision_content + "\n", encoding="utf-8")

    skill_md = render_skill_md(meta, slug, reality_content, energy_content, decision_content)
    (org_dir / "SKILL.md").write_text(skill_md + "\n", encoding="utf-8")

    name = meta.get("name", slug)
    (org_dir / "reality_skill.md").write_text(
        REALITY_ONLY_TEMPLATE.format(slug=slug, name=name, reality_content=reality_content) + "\n",
        encoding="utf-8",
    )
    (org_dir / "energy_skill.md").write_text(
        ENERGY_ONLY_TEMPLATE.format(slug=slug, name=name, energy_content=energy_content) + "\n",
        encoding="utf-8",
    )
    (org_dir / "decision_skill.md").write_text(
        DECISION_ONLY_TEMPLATE.format(slug=slug, name=name, decision_content=decision_content) + "\n",
        encoding="utf-8",
    )

    meta["slug"] = slug
    meta.setdefault("source_stats", {"docs": 0, "messages": 0, "meetings": 0, "decisions": 0})
    meta.setdefault("diagnostic_flags", [])
    meta.setdefault("created_at", now_iso())
    meta["updated_at"] = now_iso()
    meta["version"] = "v1"

    (org_dir / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return org_dir


def backup_current_version(org_dir: Path, version: str) -> None:
    version_dir = org_dir / "versions" / version
    version_dir.mkdir(parents=True, exist_ok=True)
    # 【核心改动】修改了备份追踪的文件名
    for file_name in (
        "SKILL.md",
        "my_structural_reality.md",
        "my_energy_drain.md",
        "stay_or_leave_decision.md",
        "reality_skill.md",
        "energy_skill.md",
        "decision_skill.md",
        "meta.json",
    ):
        src = org_dir / file_name
        if src.exists():
            shutil.copy2(src, version_dir / file_name)


def next_version(current: str) -> str:
    match = re.match(r"v(\d+)", current or "")
    if not match:
        return "v2"
    return f"v{int(match.group(1)) + 1}"


def append_patch(current: str, patch: Optional[str]) -> str:
    if not patch:
        return current
    patch_text = Path(patch).read_text(encoding="utf-8").strip()
    if not patch_text:
        return current
    return current.rstrip() + "\n\n" + patch_text + "\n"


def update_skill(
    org_dir: Path,
    reality_patch: Optional[str] = None,
    energy_patch: Optional[str] = None,
    decision_patch: Optional[str] = None,
) -> str:
    meta_path = org_dir / "meta.json"
    if not meta_path.exists():
        raise FileNotFoundError(f"找不到 meta.json: {meta_path}")

    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    current_version = meta.get("version", "v1")
    backup_current_version(org_dir, current_version)

    # 【核心改动】修改了更新时读取的文件名
    reality_content = append_patch((org_dir / "my_structural_reality.md").read_text(encoding="utf-8"), reality_patch)
    energy_content = append_patch((org_dir / "my_energy_drain.md").read_text(encoding="utf-8"), energy_patch)
    decision_content = append_patch((org_dir / "stay_or_leave_decision.md").read_text(encoding="utf-8"), decision_patch)

    (org_dir / "my_structural_reality.md").write_text(reality_content.rstrip() + "\n", encoding="utf-8")
    (org_dir / "my_energy_drain.md").write_text(energy_content.rstrip() + "\n", encoding="utf-8")
    (org_dir / "stay_or_leave_decision.md").write_text(decision_content.rstrip() + "\n", encoding="utf-8")

    slug = meta.get("slug", org_dir.name)
    name = meta.get("name", slug)

    (org_dir / "SKILL.md").write_text(
        render_skill_md(meta, slug, reality_content, energy_content, decision_content).rstrip() + "\n",
        encoding="utf-8",
    )
    (org_dir / "reality_skill.md").write_text(
        REALITY_ONLY_TEMPLATE.format(slug=slug, name=name, reality_content=reality_content).rstrip() + "\n",
        encoding="utf-8",
    )
    (org_dir / "energy_skill.md").write_text(
        ENERGY_ONLY_TEMPLATE.format(slug=slug, name=name, energy_content=energy_content).rstrip() + "\n",
        encoding="utf-8",
    )
    (org_dir / "decision_skill.md").write_text(
        DECISION_ONLY_TEMPLATE.format(slug=slug, name=name, decision_content=decision_content).rstrip() + "\n",
        encoding="utf-8",
    )

    meta["version"] = next_version(current_version)
    meta["updated_at"] = now_iso()
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return meta["version"]


def list_organizations(base_dir: Path) -> list[dict]:
    if not base_dir.exists():
        return []

    results: list[dict] = []
    for org_dir in sorted(base_dir.iterdir()):
        if not org_dir.is_dir():
            continue
        meta_path = org_dir / "meta.json"
        if not meta_path.exists():
            continue
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        results.append(
            {
                "slug": meta.get("slug", org_dir.name),
                "name": meta.get("name", org_dir.name),
                "scope": meta.get("scope", "未指定"),
                "user_position": meta.get("user_position", "未指定"),
                "version": meta.get("version", "v1"),
                "updated_at": meta.get("updated_at", ""),
            }
        )
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="职场生存军师 Skill 文件写入器")
    parser.add_argument("--action", required=True, choices=["create", "update", "list"])
    parser.add_argument("--slug", help="组织 slug（用于目录名）")
    parser.add_argument("--name", help="组织名称")
    parser.add_argument("--meta", help="meta.json 文件路径")
    
    # 【核心改动】修改了命令行参数名，使其与新结构对应
    parser.add_argument("--reality", help="my_structural_reality.md 文件路径")
    parser.add_argument("--energy", help="my_energy_drain.md 文件路径")
    parser.add_argument("--decision", help="stay_or_leave_decision.md 文件路径")
    parser.add_argument("--reality-patch", help="my_structural_reality.md 增量内容")
    parser.add_argument("--energy-patch", help="my_energy_drain.md 增量内容")
    parser.add_argument("--decision-patch", help="stay_or_leave_decision.md 增量内容")
    
    parser.add_argument("--base-dir", default="./organizations", help="组织 Skill 根目录")

    args = parser.parse_args()
    base_dir = Path(args.base_dir).expanduser()

    if args.action == "list":
        organizations = list_organizations(base_dir)
        if not organizations:
            print("暂无已建立的档案")
            return
        print(f"已建立 {len(organizations)} 份生存档案：\n")
        for item in organizations:
            updated = item["updated_at"][:10] if item["updated_at"] else "未知"
            print(f"  [{item['slug']}]  {item['name']}")
            print(f"    范围: {item['scope']}  位置: {item['user_position']}  版本: {item['version']}  更新: {updated}")
            print()
        return

    if args.action == "create":
        meta: dict = {}
        if args.meta:
            meta = json.loads(Path(args.meta).read_text(encoding="utf-8"))
        if args.name:
            meta["name"] = args.name
        name = meta.get("name") or args.slug
        if not name:
            print("错误：create 操作需要 --name、--slug 或 --meta", file=sys.stderr)
            sys.exit(1)

        slug = args.slug or slugify(name)
        reality_content = ensure_text(args.reality, DEFAULT_REALITY)
        energy_content = ensure_text(args.energy, DEFAULT_ENERGY)
        decision_content = ensure_text(args.decision, DEFAULT_DECISION)

        org_dir = create_skill(base_dir, slug, meta, reality_content, energy_content, decision_content)
        print(f"✅ 生存档案已建立：{org_dir}")
        print(f"   触发词：/{slug}")
        return

    if args.action == "update":
        if not args.slug:
            print("错误：update 操作需要 --slug", file=sys.stderr)
            sys.exit(1)
        org_dir = base_dir / args.slug
        if not org_dir.exists():
            print(f"错误：找不到档案目录 {org_dir}", file=sys.stderr)
            sys.exit(1)

        new_version = update_skill(
            org_dir,
            reality_patch=args.reality_patch,
            energy_patch=args.energy_patch,
            decision_patch=args.decision_patch,
        )
        print(f"✅ 档案已更新到 {new_version}：{org_dir}")
        return


if __name__ == "__main__":
    main()
