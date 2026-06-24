---
name: project-context-continuity
description: Context continuity Skill for non-trivial projects. Use to monitor remaining context, write OpenSpec or fallback state before compaction, restore from source-of-truth after resume, prevent hallucinated continuation, and coordinate task ownership from durable records. Do not use for tiny one-shot tasks.
---

# Project Context Continuity

Keep project work coherent across long threads, context compression, resumes, and multi-agent handoffs.

## Source Of Truth

- Use native OpenSpec change files when available.
- If OpenSpec is unavailable, use the project-local `.project-autopilot/changes/<change-id>/` fallback.
- Treat chat history as evidence, not as the source of truth.
- Record goal, scope, assumptions, decisions, task registry, owners, verification evidence, blocked checks, and final status in durable files.

## Context Budget

- At project start, create or refresh a compact state file.
- Before delegating, record each worker's role, scope, allowed files, expected output, and acceptance gate.
- When the thread grows long, the task becomes multi-phase, or compaction/resume is likely, update the OpenSpec/fallback state before more implementation.
- After any resume or context transition, read the OpenSpec/fallback state before acting. Do not rely on memory alone.

## Anti-Hallucination Rules

- If a needed decision, test result, file path, or owner is not in the durable state or current files, mark it unknown and verify.
- Do not invent completed work after compaction.
- Do not re-run or duplicate a task already claimed, in review, done, cancelled, or blocked in the task registry.
- If state is missing, rebuild it from files and commands before proceeding.

## Output

Return current phase, state location, known completed work, active owners, next tasks, verification evidence, blockers, and what must be refreshed before continuing.
