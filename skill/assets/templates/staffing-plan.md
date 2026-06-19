# Staffing Plan

Mode: {{mode}}
Change: {{change_id}}
Project size: {{project_size}}
Maximum concurrency: {{max_concurrency}}

## Lead

- Role: project lead thread
- Marker: {{lead_thread_role}}
- Responsibility: clarify requirements, coordinate departments, own acceptance, and produce final report.
- File edits: allowed when directly executing main-thread work.

## Active Departments

{{active_departments}}

## Available But Inactive Departments

{{inactive_departments}}

## Add Staff When

- Independent module, risk type, or verification surface appears.
- The role has clear input, output, acceptance method, and non-overlapping scope.
- Parallel work saves more context than it costs to coordinate.

## Remove Staff When

- Work completes.
- Scope overlaps another active worker.
- The project shrinks or becomes sequential.
- Coordination costs more than direct lead-thread execution.
