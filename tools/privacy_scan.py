#!/usr/bin/env python3
"""Scan release files for common secrets, local paths, and publish-risk files."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


SKIP_DIRS = {".git", "node_modules", "__pycache__", ".cache", "dist", "out"}
SKIP_SUFFIXES = {".pyc", ".pyo", ".mp4", ".png", ".jpg", ".jpeg", ".gif", ".ico"}
RISK_FILENAMES = {".env", ".env.local", "auth.json", "config.toml", "history.jsonl"}

PATTERNS = {
    "openai_key": re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    "github_token": re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
    "aws_access_key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "private_key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "windows_user_path": re.compile(r"[A-Za-z]:" + re.escape("\\") + r"Users" + re.escape("\\")),
    "repo_absolute_path": re.compile(r"[A-Za-z]:" + re.escape("\\") + r"codex" + re.escape("\\")),
    "unix_home_path": re.compile(r"/(?:Users|home)/[A-Za-z0-9._-]+"),
}


def should_skip(path: Path) -> bool:
    if any(part in SKIP_DIRS for part in path.parts):
        return True
    return path.suffix.lower() in SKIP_SUFFIXES


def scan(root: Path) -> list[str]:
    findings: list[str] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or should_skip(path):
            continue
        rel = path.relative_to(root)
        if path.name in RISK_FILENAMES:
            findings.append(f"risk-file:{rel}")
        text = path.read_text(encoding="utf-8", errors="ignore")
        for name, pattern in PATTERNS.items():
            if pattern.search(text):
                findings.append(f"{name}:{rel}")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    args = parser.parse_args()
    findings = scan(args.root.resolve())
    if findings:
        for finding in findings:
            print(f"FOUND {finding}")
        return 1
    print("privacy scan passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
