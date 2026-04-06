"""
组织蒸馏项目的证据索引器。

用途：
1. 扫描 organizations/{slug}/evidence 目录
2. 统计 docs/messages/meetings/decisions/snapshots 五类材料数量
3. 生成 evidence_index.json，供后续分析器与 meta.json 更新使用

用法：
    python3 tools/evidence_indexer.py --org-dir ./organizations/biz-middle-platform
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


CATEGORIES = ["docs", "messages", "meetings", "decisions", "snapshots"]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def collect_files(base: Path, category: str) -> list[dict]:
    target_dir = base / "evidence" / category
    if not target_dir.exists():
        return []

    items: list[dict] = []
    for path in sorted(target_dir.rglob("*")):
        if not path.is_file():
            continue
        stat = path.stat()
        items.append(
            {
                "path": str(path.relative_to(base)),
                "name": path.name,
                "suffix": path.suffix.lower(),
                "size_bytes": stat.st_size,
                "modified_at": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
            }
        )
    return items


def build_index(org_dir: Path) -> dict:
    result = {
        "organization_dir": str(org_dir),
        "generated_at": now_iso(),
        "source_stats": {},
        "sources": {},
    }

    for category in CATEGORIES:
        files = collect_files(org_dir, category)
        result["source_stats"][category] = len(files)
        result["sources"][category] = files

    result["total_files"] = sum(result["source_stats"].values())
    return result


def update_meta(org_dir: Path, source_stats: dict) -> None:
    meta_path = org_dir / "meta.json"
    if not meta_path.exists():
        return

    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except Exception:
        return

    meta["source_stats"] = source_stats
    meta["updated_at"] = now_iso()
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="组织蒸馏证据索引器")
    parser.add_argument("--org-dir", required=True, help="组织目录，例如 ./organizations/biz-middle-platform")
    args = parser.parse_args()

    org_dir = Path(args.org_dir).expanduser().resolve()
    if not org_dir.exists():
        raise SystemExit(f"找不到组织目录：{org_dir}")

    index = build_index(org_dir)
    output_path = org_dir / "evidence_index.json"
    output_path.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    update_meta(org_dir, index["source_stats"])

    print(f"✅ 已生成证据索引：{output_path}")
    print(json.dumps(index["source_stats"], ensure_ascii=False))


if __name__ == "__main__":
    main()
