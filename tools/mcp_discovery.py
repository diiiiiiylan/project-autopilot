#!/usr/bin/env python3
"""Read-only MCP source discovery for project-autopilot."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "references" / "registries" / "mcp-sources.json"


KNOWN_HINTS = {
    "github": ["official-mcp-registry", "github-mcp"],
    "git": ["official-mcp-registry", "github-mcp"],
    "browser": ["official-mcp-registry", "mcpservers-community"],
    "chrome": ["official-mcp-registry", "mcpservers-community"],
    "filesystem": ["modelcontextprotocol-servers"],
    "file": ["modelcontextprotocol-servers"],
    "database": ["official-mcp-registry", "modelcontextprotocol-servers", "mcpservers-community"],
    "postgres": ["official-mcp-registry", "modelcontextprotocol-servers"],
    "figma": ["official-mcp-registry", "mcpservers-community"],
}


def load_sources() -> list[dict[str, object]]:
    payload = json.loads(REGISTRY.read_text(encoding="utf-8"))
    return list(payload["sources"])


def discover(query: str) -> dict[str, object]:
    text = query.lower()
    sources = load_sources()
    ids: list[str] = []
    for keyword, source_ids in KNOWN_HINTS.items():
        if keyword in text:
            ids.extend(source_ids)
    if not ids:
        ids = ["official-mcp-registry", "modelcontextprotocol-servers", "mcpservers-community"]
    deduped = list(dict.fromkeys(ids))
    candidates = [source for source in sources if source["id"] in deduped]
    return {
        "query": query,
        "candidates": candidates,
        "install_permitted": False,
        "create_permitted": False,
        "custom_mcp_plan_required": "unknown tool" in text or "no mcp" in text or "找不到" in text,
        "permission_required_before_install_or_create": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query")
    args = parser.parse_args()
    print(json.dumps(discover(args.query), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
