"""
组织蒸馏 Skill 文件写入器。

负责将生成的 role_interfaces.md、info_flows.md、org_diagnosis.md
写入到标准目录结构，并生成 meta.json 与完整 SKILL.md。

用法示例：
    python3 tools/org_skill_writer.py --action create --slug biz-middle-platform \
        --meta meta.json \
        --interfaces role_interfaces.md \
        --flows info_flows.md \
        --diagnosis org_diagnosis.md \
        --base-dir ./organizations

    python3 tools/org_skill_writer.py --action update --slug biz-middle-platform \
        --interfaces-patch interfaces_patch.md \
        --flows-patch flows_patch.md \
        --diagnosis-patch diagnosis_patch.md \
        --base-dir ./organizations

    python3 tools/org_skill_writer.py --action list --base-dir ./organizations
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
name: organization_{slug}
description: {name} 的组织信息流与权限结构分析 Skill
---

# {name}

## 分析范围

- **组织名称**：{name}
- **分析边界**：{scope}
- **用户位置**：{user_position}
- **初始假设**：{org_hypothesis}

---

## PART A：角色接口画像

{interfaces_content}

---

## PART B：信息流画像

{flows_content}

---

## PART C：组织诊断

{diagnosis_content}

---

## 运行规则

接收到与该组织相关的问题时，按如下顺序处理：

1. 先判断问题涉及哪个角色接口与哪个信息层。
2. 再结合信息流路径分析信息从哪里来、在哪一层被压缩或损耗。
3. 最后基于现有证据给出组织诊断，不要把结构问题轻易归因为个人品质问题。
4. 若证据不足，必须明确指出“原材料不足”以及缺的是哪一类材料。
"""


INTERFACES_ONLY_TEMPLATE = """---
name: organization_{slug}_interfaces
description: {name} 的角色接口画像
---

{interfaces_content}
"""


FLOWS_ONLY_TEMPLATE = """---
name: organization_{slug}_flows
description: {name} 的信息流画像
---

{flows_content}
"""


DIAGNOSIS_ONLY_TEMPLATE = """---
name: organization_{slug}_diagnosis
description: {name} 的组织诊断
---

{diagnosis_content}
"""


DEFAULT_INTERFACES = """# 角色接口画像

## 当前状态

原材料不足，尚未形成稳定的角色接口画像。

## 建议补充

优先补充能够体现“谁向谁输出什么”的材料，例如：

- 任务分发记录
- 跨部门对齐纪要
- 汇报与评审材料
- 群聊中的职责边界争议
"""


DEFAULT_FLOWS = """# 信息流画像

## 当前状态

原材料不足，尚未形成稳定的信息流判断。

## 建议补充

优先补充能够体现信息如何流动和压缩的材料，例如：

- 决策传达链路
- 多层级汇报记录
- 会议纪要与后续执行偏差
- 高层结论到执行层动作之间的转换记录
"""


DEFAULT_DIAGNOSIS = """# 组织诊断

## 当前状态

原材料不足，暂不对组织下结论。

## 初步判断原则

在证据不足时，不要直接把低信息输出理解为个人无能，更可能是岗位接口、权限结构或信息传递机制造成的结果。
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


def render_skill_md(meta: dict, slug: str, interfaces_content: str, flows_content: str, diagnosis_content: str) -> str:
    return SKILL_MD_TEMPLATE.format(
        slug=slug,
        name=meta.get("name", slug),
        scope=meta.get("scope", "未指定"),
        user_position=meta.get("user_position", "未指定"),
        org_hypothesis=meta.get("org_hypothesis", "暂无"),
        interfaces_content=interfaces_content,
        flows_content=flows_content,
        diagnosis_content=diagnosis_content,
    )


def create_skill(
    base_dir: Path,
    slug: str,
    meta: dict,
    interfaces_content: str,
    flows_content: str,
    diagnosis_content: str,
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

    (org_dir / "role_interfaces.md").write_text(interfaces_content + "\n", encoding="utf-8")
    (org_dir / "info_flows.md").write_text(flows_content + "\n", encoding="utf-8")
    (org_dir / "org_diagnosis.md").write_text(diagnosis_content + "\n", encoding="utf-8")

    skill_md = render_skill_md(meta, slug, interfaces_content, flows_content, diagnosis_content)
    (org_dir / "SKILL.md").write_text(skill_md + "\n", encoding="utf-8")

    name = meta.get("name", slug)
    (org_dir / "interfaces_skill.md").write_text(
        INTERFACES_ONLY_TEMPLATE.format(slug=slug, name=name, interfaces_content=interfaces_content) + "\n",
        encoding="utf-8",
    )
    (org_dir / "flows_skill.md").write_text(
        FLOWS_ONLY_TEMPLATE.format(slug=slug, name=name, flows_content=flows_content) + "\n",
        encoding="utf-8",
    )
    (org_dir / "diagnosis_skill.md").write_text(
        DIAGNOSIS_ONLY_TEMPLATE.format(slug=slug, name=name, diagnosis_content=diagnosis_content) + "\n",
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
    for file_name in (
        "SKILL.md",
        "role_interfaces.md",
        "info_flows.md",
        "org_diagnosis.md",
        "interfaces_skill.md",
        "flows_skill.md",
        "diagnosis_skill.md",
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
    interfaces_patch: Optional[str] = None,
    flows_patch: Optional[str] = None,
    diagnosis_patch: Optional[str] = None,
) -> str:
    meta_path = org_dir / "meta.json"
    if not meta_path.exists():
        raise FileNotFoundError(f"找不到 meta.json: {meta_path}")

    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    current_version = meta.get("version", "v1")
    backup_current_version(org_dir, current_version)

    interfaces_content = append_patch((org_dir / "role_interfaces.md").read_text(encoding="utf-8"), interfaces_patch)
    flows_content = append_patch((org_dir / "info_flows.md").read_text(encoding="utf-8"), flows_patch)
    diagnosis_content = append_patch((org_dir / "org_diagnosis.md").read_text(encoding="utf-8"), diagnosis_patch)

    (org_dir / "role_interfaces.md").write_text(interfaces_content.rstrip() + "\n", encoding="utf-8")
    (org_dir / "info_flows.md").write_text(flows_content.rstrip() + "\n", encoding="utf-8")
    (org_dir / "org_diagnosis.md").write_text(diagnosis_content.rstrip() + "\n", encoding="utf-8")

    slug = meta.get("slug", org_dir.name)
    name = meta.get("name", slug)

    (org_dir / "SKILL.md").write_text(
        render_skill_md(meta, slug, interfaces_content, flows_content, diagnosis_content).rstrip() + "\n",
        encoding="utf-8",
    )
    (org_dir / "interfaces_skill.md").write_text(
        INTERFACES_ONLY_TEMPLATE.format(slug=slug, name=name, interfaces_content=interfaces_content).rstrip() + "\n",
        encoding="utf-8",
    )
    (org_dir / "flows_skill.md").write_text(
        FLOWS_ONLY_TEMPLATE.format(slug=slug, name=name, flows_content=flows_content).rstrip() + "\n",
        encoding="utf-8",
    )
    (org_dir / "diagnosis_skill.md").write_text(
        DIAGNOSIS_ONLY_TEMPLATE.format(slug=slug, name=name, diagnosis_content=diagnosis_content).rstrip() + "\n",
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
    parser = argparse.ArgumentParser(description="组织蒸馏 Skill 文件写入器")
    parser.add_argument("--action", required=True, choices=["create", "update", "list"])
    parser.add_argument("--slug", help="组织 slug（用于目录名）")
    parser.add_argument("--name", help="组织名称")
    parser.add_argument("--meta", help="meta.json 文件路径")
    parser.add_argument("--interfaces", help="role_interfaces.md 文件路径")
    parser.add_argument("--flows", help="info_flows.md 文件路径")
    parser.add_argument("--diagnosis", help="org_diagnosis.md 文件路径")
    parser.add_argument("--interfaces-patch", help="role_interfaces.md 增量内容文件路径")
    parser.add_argument("--flows-patch", help="info_flows.md 增量内容文件路径")
    parser.add_argument("--diagnosis-patch", help="org_diagnosis.md 增量内容文件路径")
    parser.add_argument("--base-dir", default="./organizations", help="组织 Skill 根目录")

    args = parser.parse_args()
    base_dir = Path(args.base_dir).expanduser()

    if args.action == "list":
        organizations = list_organizations(base_dir)
        if not organizations:
            print("暂无已创建的组织 Skill")
            return
        print(f"已创建 {len(organizations)} 个组织 Skill：\n")
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
        interfaces_content = ensure_text(args.interfaces, DEFAULT_INTERFACES)
        flows_content = ensure_text(args.flows, DEFAULT_FLOWS)
        diagnosis_content = ensure_text(args.diagnosis, DEFAULT_DIAGNOSIS)

        org_dir = create_skill(base_dir, slug, meta, interfaces_content, flows_content, diagnosis_content)
        print(f"✅ 组织 Skill 已创建：{org_dir}")
        print(f"   触发词：/{slug}")
        return

    if args.action == "update":
        if not args.slug:
            print("错误：update 操作需要 --slug", file=sys.stderr)
            sys.exit(1)
        org_dir = base_dir / args.slug
        if not org_dir.exists():
            print(f"错误：找不到组织 Skill 目录 {org_dir}", file=sys.stderr)
            sys.exit(1)

        new_version = update_skill(
            org_dir,
            interfaces_patch=args.interfaces_patch,
            flows_patch=args.flows_patch,
            diagnosis_patch=args.diagnosis_patch,
        )
        print(f"✅ 组织 Skill 已更新到 {new_version}：{org_dir}")
        return


if __name__ == "__main__":
    main()
