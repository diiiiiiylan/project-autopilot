# Acceptance Gates

## Discover Commands

Find real commands from project instructions, package manifests, CI configs, build files, test configs, and README files. Do not invent checks.

## Gate Types

Apply the relevant existing gates: formatting, linting, type checking, unit tests, integration tests, end-to-end tests, build, smoke tests, and artifact existence checks.

## Failure Repair

When a gate fails, run up to three repair rounds:

1. Locate the root cause.
2. Apply the smallest relevant fix.
3. Re-run the complete applicable gate set.

## Completion Rule

A task is complete only when applicable checks pass or a real blocker is recorded with impact and substitute evidence. Generated code alone is not completion.
