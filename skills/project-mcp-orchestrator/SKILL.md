---
name: project-mcp-orchestrator
description: MCP and application connection governance Skill. Use to identify required applications and MCPs, search official/community registries, request permission for install or creation, and plan custom MCPs only when needed. Never install, enable, create, or call external account tools without approval.
---

# Project MCP Orchestrator

Govern application and MCP connections.

## Discovery Order

1. Check official MCP Registry.
2. Check `modelcontextprotocol/servers`.
3. Check GitHub MCP Registry and `github.com/mcp`.
4. Check Awesome/community MCP sources.
5. Check the target project's official documentation.
6. If no suitable MCP exists, prepare a custom MCP plan.

## Permission Gate

When an app or MCP gap is found and that connection is needed or materially improves the main path, pause immediately and ask before downloading applications, installing MCPs, enabling MCP servers, creating custom MCPs, or calling tools that require a logged-in external account. Explain capability, lost capability if skipped, install path, network/account/cost needs, security boundary, verification command, and rollback. Do not wait until final reporting.

Custom MCPs require stable repeated need, safe command boundary, non-secret env names, port policy, validation command, and rollback path.
