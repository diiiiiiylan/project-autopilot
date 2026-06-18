# Department Contracts

## Requirements Architecture Department

Clarifies requirements, investigates the codebase, analyzes impact, designs the approach, and defines acceptance criteria. It does not perform unrelated implementation.

## Development Department

Implements bounded changes and necessary tests. It follows the spec and does not expand scope independently.

## Quality Assurance Department

Designs tests, reproduces failures, runs regression checks, and collects acceptance evidence. It avoids duplicating development implementation work.

## Independent Review Department

Uses read-only review by default. It checks correctness, security, maintainability, missed requirements, and test gaps. It does not accept unsupported developer conclusions.

## Delegation Limits

Use task titles in the form `XX部门：具体任务`. Maximum concurrency target is 4. Maximum delegation depth is 1. Do not delegate overlapping files or sequential dependencies as parallel work.
