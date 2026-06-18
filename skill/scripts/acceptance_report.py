#!/usr/bin/env python3
"""Generate an acceptance report without masking failed verification."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def report_status(checks: list[str], blocked: list[str]) -> str:
    failed = [item for item in checks if item.lower().startswith("fail:")]
    if failed:
        return "failed"
    if blocked:
        return "blocked"
    return "done"


def generate_report(
    change_dir: Path,
    change_id: str,
    mode: str,
    checks: list[str],
    blocked: list[str],
    risks: list[str],
) -> Path:
    status = report_status(checks, blocked)
    evidence = "\n".join(f"- {item}" for item in checks) or "- No checks recorded"
    blocked_text = "\n".join(f"- {item}" for item in blocked) or "- None"
    risk_text = "\n".join(f"- {item}" for item in risks) or "- None"
    result = "Accepted" if status == "done" else "Not accepted"
    content = f"""# Acceptance Report

Mode: {mode}
Change: {change_id}
Status: {status}
Generated: {utc_now()}

## Result

{result}

## Verification Evidence

{evidence}

## Blocked Or Skipped Checks

{blocked_text}

## Remaining Risks

{risk_text}
"""
    change_dir.mkdir(parents=True, exist_ok=True)
    output = change_dir / "acceptance-report.md"
    output.write_text(content, encoding="utf-8", newline="\n")
    return output


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("change_dir", type=Path)
    parser.add_argument("--change-id", required=True)
    parser.add_argument("--mode", default="fallback")
    parser.add_argument("--check", action="append", default=[])
    parser.add_argument("--blocked", action="append", default=[])
    parser.add_argument("--risk", action="append", default=[])
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    output = generate_report(args.change_dir, args.change_id, args.mode, args.check, args.blocked, args.risk)
    print(output)
    text = output.read_text(encoding="utf-8")
    return 0 if "Status: done" in text else 2


if __name__ == "__main__":
    raise SystemExit(main())
