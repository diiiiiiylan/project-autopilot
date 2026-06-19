---
name: project-superpowers-routing
description: Superpowers routing Skill for strict engineering workflow. Use to map tasks to brainstorming, writing plans, executing plans, TDD, systematic debugging, code review, finishing branches, and verification before completion.
---

# Project Superpowers Routing

Use installed Superpowers Skills as the strict engineering process layer.

## Routing Map

- Ambiguous product or architecture choice: `superpowers:brainstorming`
- Implementation plan: `superpowers:writing-plans`
- Executing an approved plan: `superpowers:executing-plans`
- New behavior with testable logic: `superpowers:test-driven-development`
- Bug reproduction and root cause: `superpowers:systematic-debugging`
- Parallel worker setup: `superpowers:dispatching-parallel-agents`
- Review request or response: `superpowers:requesting-code-review`, `superpowers:receiving-code-review`
- Completion gate: `superpowers:verification-before-completion`

If a Superpowers Skill is not installed, state the missing capability and use the local project-autopilot fallback flow.
