---
name: project-gpt-consultation
description: GPT consultation Skill for project planning. Use before finalizing a non-trivial project plan, architecture proposal, expert distillation, or skillbox change when the user expects GPT discussion first. If no callable GPT or web ChatGPT tool is available, pause immediately and ask for authorization or a fallback choice. Do not pretend consultation happened.
---

# Project GPT Consultation

Use this Skill to make external or separate GPT consultation an explicit pre-plan gate.

## Required Gate

- Before finalizing a non-trivial project plan, architecture proposal, external Skill integration, expert distillation, or MCP/app strategy, check whether GPT consultation is required by user instruction or project policy.
- If a callable GPT, web ChatGPT, or approved consultation thread/tool is available, ask the consultation questions and incorporate the answer into the plan.
- If no callable tool is available, pause immediately and ask the user to authorize a tool, provide a GPT conversation result, or approve a local fallback.
- Do not continue to final方案 as if consultation happened.

## Consultation Brief

Send the consultant:

- Goal and product context.
- Current constraints and forbidden actions.
- Proposed architecture or plan.
- Open questions and tradeoffs.
- Evidence needed for acceptance.
- Specific request: identify missing risks, simpler approaches, required dependencies, and validation gaps.

## Output

Record consultation source, timestamp, questions asked, answer summary, decisions changed, unresolved risks, and whether fallback was used.
