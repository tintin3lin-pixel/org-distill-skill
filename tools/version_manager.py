"""
职场生存军师 Skill 的版本管理工具。

支持：
1. 列出历史生存档案版本
2. 回滚到指定版本
3. 清理过多历史版本
"""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

# 【核心改动】修改了需要被版本追踪的文件名，与生存军师的新输出对齐
TRACKED_FILES = [
    "SKILL.md",
    "my_structural_reality.md",
    "my_energy_drain.md",
    "stay_or_leave_decision.md",
    "reality_skill.md",
    "energy_skill.md",
    "decision_skill.md",
    "meta.json",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def list_versions(org_dir: Path) -> list[str]:
    versions_dir = org_dir / "versions"
    if not versions_dir.exists():
        return []
    return sorted([p.name for p in versions_dir.iterdir() if p.is_dir()])


def rollback(org_dir: Path, version: str) -> None:
    version_dir = org_dir / "versions" / version
    if not version_dir.exists():
        raise SystemExit(f"找不到版本目录：{version_dir}")

    for file_name in TRACKED_FILES:
        src = version_dir / file_name
        if src.exists():
            shutil.copy2(src, org_dir / file_name)

    meta_path = org_dir / "meta.json"
    if meta_path.exists():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        meta["updated_at"] = now_iso()
        meta["rolled_back_from"] = version
        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def cleanup(org_dir: Path, keep: int = 10) -> None:
    versions = list_versions(org_dir)
    if len(versions) <= keep:
        return
    for version in versions[:-keep]:
        shutil.rmtree(org_dir / "versions" / version, ignore_errors=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="职场生存军师 Skill 版本管理器")
    parser.add_argument("--action", required=True, choices=["list", "rollback", "cleanup"])
    parser.add_argument("--org-dir", required=True, help="档案目录")
    parser.add_argument("--version", help="要回滚的版本")
    parser.add_argument("--keep", type=int, default=10, help="cleanup 时保留的版本数量")
    args = parser.parse_args()

    org_dir = Path(args.org_dir).expanduser().resolve()
    if not org_dir.exists():
        raise SystemExit(f"找不到档案目录：{org_dir}")

    if args.action == "list":
        versions = list_versions(org_dir)
        if not versions:
            print("暂无历史版本")
            return
        for version in versions:
            print(version)
        return

    if args.action == "rollback":
        if not args.version:
            raise SystemExit("rollback 操作需要 --version")
        rollback(org_dir, args.version)
        print(f"✅ 已回滚到版本：{args.version}")
        return

    if args.action == "cleanup":
        cleanup(org_dir, args.keep)
        print(f"✅ 已清理旧版本，保留最近 {args.keep} 个")


if __name__ == "__main__":
    main()
