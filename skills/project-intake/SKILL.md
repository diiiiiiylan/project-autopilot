---
name: project-intake
description: Project intake Skill for plan mode, new projects, product starts, and ambiguous non-trivial modifications. Use to ask only key questions about size, boundary, acceptance, forbidden actions, delivery target, and concurrency. Do not use for trivial fixes or explanation-only requests.
---

# Project Intake

Turn unclear user language into an executable project brief.

## Steps

1. Translate the request into problem, user scenario, expected outcome, deliverables, acceptance criteria, constraints, and risks.
2. Ask only for missing details that materially change the main path.
3. If missing details do not change a safe path, proceed with conservative assumptions and record them.
4. Capture project size, boundaries, forbidden actions, delivery target, verification standard, and concurrency preference.
5. Hand the brief to `$project-staffing` and `$project-domain-router` for medium or larger work.

## Question Pool

- What product outcome must be true at the end?
- What is out of scope or forbidden?
- What is the minimum useful version?
- Which data, accounts, production systems, paid services, or public publishing actions are restricted?
- What verification evidence should be required before completion?
- What concurrency cap should be used if the project becomes large?
