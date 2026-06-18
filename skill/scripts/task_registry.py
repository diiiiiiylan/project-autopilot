#!/usr/bin/env python3
"""Task registry with stable fingerprints and atomic claims."""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


VALID_STATES = {
    "pending",
    "claimed",
    "in_progress",
    "blocked",
    "review",
    "done",
    "cancelled",
}
ACTIVE_STATES = {"claimed", "in_progress", "review", "done"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def normalize_text(value: str) -> str:
    return " ".join((value or "").strip().lower().split())


def task_fingerprint(title: str, body: str = "", scope: str = "") -> str:
    payload = json.dumps(
        {
            "title": normalize_text(title),
            "body": normalize_text(body),
            "scope": normalize_text(scope),
        },
        ensure_ascii=True,
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def stable_task_id(title: str, body: str = "", scope: str = "") -> str:
    return "task-" + task_fingerprint(title, body, scope)[:16]


def default_registry() -> dict[str, Any]:
    return {"version": 1, "tasks": {}}


def load_registry(path: Path) -> dict[str, Any]:
    if not path.exists():
        return default_registry()
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict) or "tasks" not in data:
        raise ValueError(f"Invalid task registry: {path}")
    return data


def atomic_write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
        os.replace(tmp_name, path)
    finally:
        with contextlib.suppress(FileNotFoundError):
            os.unlink(tmp_name)


class FileLock:
    def __init__(self, path: Path, timeout: float = 10.0) -> None:
        self.path = path
        self.timeout = timeout
        self.fd: int | None = None

    def __enter__(self) -> "FileLock":
        self.path.parent.mkdir(parents=True, exist_ok=True)
        deadline = time.time() + self.timeout
        while True:
            try:
                self.fd = os.open(str(self.path), os.O_CREAT | os.O_EXCL | os.O_RDWR)
                os.write(self.fd, str(os.getpid()).encode("ascii"))
                return self
            except FileExistsError:
                if time.time() >= deadline:
                    raise TimeoutError(f"Could not acquire lock: {self.path}")
                time.sleep(0.05)

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        if self.fd is not None:
            os.close(self.fd)
        with contextlib.suppress(FileNotFoundError):
            self.path.unlink()


def ensure_task(
    registry_path: Path,
    title: str,
    body: str = "",
    scope: str = "",
    owner: str = "",
    status: str = "pending",
) -> dict[str, Any]:
    if status not in VALID_STATES:
        raise ValueError(f"Invalid status: {status}")
    task_id = stable_task_id(title, body, scope)
    fp = task_fingerprint(title, body, scope)
    with FileLock(registry_path.with_suffix(registry_path.suffix + ".lock")):
        registry = load_registry(registry_path)
        task = registry["tasks"].get(task_id)
        if task is None:
            task = {
                "id": task_id,
                "fingerprint": fp,
                "title": title,
                "body": body,
                "scope": scope,
                "owner": owner,
                "status": status,
                "created_at": utc_now(),
                "updated_at": utc_now(),
            }
            registry["tasks"][task_id] = task
        else:
            task["updated_at"] = utc_now()
        atomic_write_json(registry_path, registry)
        return task


def claim_task(
    registry_path: Path,
    title: str,
    body: str = "",
    scope: str = "",
    owner: str = "main",
) -> dict[str, Any]:
    task_id = stable_task_id(title, body, scope)
    fp = task_fingerprint(title, body, scope)
    with FileLock(registry_path.with_suffix(registry_path.suffix + ".lock")):
        registry = load_registry(registry_path)
        for existing in registry["tasks"].values():
            if existing.get("fingerprint") == fp and existing.get("id") != task_id:
                if existing.get("status") in ACTIVE_STATES or existing.get("status") == "pending":
                    return {
                        "claimed": False,
                        "reason": "duplicate_fingerprint",
                        "existing": existing,
                    }
        task = registry["tasks"].get(task_id)
        if task and task.get("status") in ACTIVE_STATES:
            return {"claimed": False, "reason": "already_active", "existing": task}
        if task and task.get("status") == "cancelled":
            return {"claimed": False, "reason": "cancelled", "existing": task}
        if task is None:
            task = {
                "id": task_id,
                "fingerprint": fp,
                "title": title,
                "body": body,
                "scope": scope,
                "created_at": utc_now(),
            }
            registry["tasks"][task_id] = task
        task.update({"status": "claimed", "owner": owner, "updated_at": utc_now()})
        atomic_write_json(registry_path, registry)
        return {"claimed": True, "task": task}


def set_status(registry_path: Path, task_id: str, status: str, evidence: str = "") -> dict[str, Any]:
    if status not in VALID_STATES:
        raise ValueError(f"Invalid status: {status}")
    with FileLock(registry_path.with_suffix(registry_path.suffix + ".lock")):
        registry = load_registry(registry_path)
        task = registry["tasks"].get(task_id)
        if task is None:
            raise KeyError(f"Task not found: {task_id}")
        task["status"] = status
        task["updated_at"] = utc_now()
        if evidence:
            task.setdefault("evidence", []).append({"at": utc_now(), "text": evidence})
        atomic_write_json(registry_path, registry)
        return task


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("add", "claim"):
        cmd = sub.add_parser(name)
        cmd.add_argument("registry", type=Path)
        cmd.add_argument("--title", required=True)
        cmd.add_argument("--body", default="")
        cmd.add_argument("--scope", default="")
        cmd.add_argument("--owner", default="main")
    status = sub.add_parser("status")
    status.add_argument("registry", type=Path)
    status.add_argument("task_id")
    status.add_argument("status", choices=sorted(VALID_STATES))
    status.add_argument("--evidence", default="")
    listing = sub.add_parser("list")
    listing.add_argument("registry", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "add":
        result = ensure_task(args.registry, args.title, args.body, args.scope, args.owner)
    elif args.command == "claim":
        result = claim_task(args.registry, args.title, args.body, args.scope, args.owner)
    elif args.command == "status":
        result = set_status(args.registry, args.task_id, args.status, args.evidence)
    else:
        result = load_registry(args.registry)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
