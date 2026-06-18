#!/usr/bin/env python3
"""Detect duplicate task fingerprints in a project-autopilot registry."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


def find_duplicates(registry_path: Path) -> list[dict[str, object]]:
    data = json.loads(registry_path.read_text(encoding="utf-8"))
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for task in data.get("tasks", {}).values():
        grouped[str(task.get("fingerprint", ""))].append(task)
    return [
        {"fingerprint": fp, "tasks": tasks}
        for fp, tasks in grouped.items()
        if fp and len(tasks) > 1
    ]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("registry", type=Path)
    args = parser.parse_args(argv)
    duplicates = find_duplicates(args.registry)
    print(json.dumps({"duplicates": duplicates}, ensure_ascii=False, indent=2, sort_keys=True))
    return 1 if duplicates else 0


if __name__ == "__main__":
    raise SystemExit(main())
