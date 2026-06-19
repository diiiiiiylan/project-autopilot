# Staffing Model

Use this model to add or remove departments without wasting token budget.

## Project Sizes

- Small: one clear local change, one owner, no public interface, no migration, no new dependency, no release risk. Use only the project lead/main thread.
- Medium: multiple files or one cross-module behavior with limited risk. Use the project lead plus at most two active workers.
- Large: multiple modules, public contracts, migration, new dependency, security, release, or independent QA/review needs. Use the project lead plus required departments, with concurrency capped at 4.
- Enterprise: long-running or multi-phase work. Add temporary specialists only when their scope is independent and has clear input, output, and acceptance evidence.

## Add Employees When

- Work can be isolated by module, risk type, or verification surface.
- Implementation and testing can proceed without editing the same files.
- A missing specialty would create project structure gaps.
- Independent review is needed before completion.
- Parallel work saves more context than it costs to coordinate.

## Remove Or Deactivate Employees When

- Their task is done.
- Scope shrinks or becomes sequential.
- Two workers would investigate or edit the same area.
- The lead thread can safely handle the task directly.
- Coordination overhead is higher than the task risk.

## Default Rosters

- Small: project lead only.
- Medium: project lead, requirements architecture, development. QA may be simulated by the lead unless verification is large enough to isolate.
- Large: project lead, requirements architecture, development, quality assurance, independent review. People operations is optional and only active for staffing conflicts.
- Enterprise: start with the large roster, then add temporary specialists such as documentation, security, performance, or release only when each has a non-overlapping scope.

## Concurrency Rules

- Maximum concurrency is 4.
- Prefer 1 for small, 2 for medium, and 3-4 for large.
- Do not run workers in parallel when one needs another worker's output.
- Do not assign the same files, modules, or acceptance gate to two active workers.
- Use the project lead thread as the final coordinator and acceptance owner.
