---
name: project-staffing
description: Dynamic staffing Skill for adding, removing, or simulating departments and employees while controlling token cost. Use for medium, large, enterprise, unclear staffing, overlapping responsibilities, or concurrency planning. Do not use for small direct tasks.
---

# Project Staffing

Choose the smallest team that preserves structure and independent verification.

The user should not have to manually pick departments for normal project work. The project lead uses this Skill to auto-size the roster, explain only the chosen roster when useful, and adjust staffing as scope and remaining context change.

## Rules

- Small: project lead only.
- Medium: lead plus at most two execution workers. People operations is simulated by the lead unless staffing conflict exists.
- Large: lead, requirements architecture, development, QA, independent review; people operations may check conflicts.
- Enterprise: add temporary documentation, security, performance, release, or domain specialists only when their scope is independent.

## Add Employees When

- Work is isolated by module, risk type, or verification surface.
- Implementation and testing can proceed without editing the same files.
- A missing specialty would create a real project gap.
- Independent review is needed before completion.

## Remove Employees When

- A task is done, scope shrinks, roles overlap, or sequential work is cheaper than coordination.
- Two workers would investigate or modify the same files, modules, or acceptance gate.

Never exceed concurrency 4. Record role, input, output, allowed file access, and acceptance evidence for every active worker.

## Context-Aware Staffing

- Prefer fewer active workers when remaining context is low.
- Add a worker only if its task can be specified from durable OpenSpec/fallback state without requiring hidden chat context.
- Before compaction or resume, deactivate workers whose scope is done or unclear.
- After resume, rebuild staffing from durable state instead of previous chat assumptions.
