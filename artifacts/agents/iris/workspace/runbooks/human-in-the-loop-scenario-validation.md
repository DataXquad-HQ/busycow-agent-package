# Runbook — Human-in-the-Loop Scenario Validation

Purpose: test whether Iris can handle a real founder-provided operating scenario correctly without drifting into the wrong deliverable.

## When to use
Use this when [Founder 1] or [Founder 2] gives a real situation and wants to see whether Iris can:
- identify the true work item
- separate context capture from deliverable creation
- route execution into the right system
- preserve strategic context in GBrain
- avoid over-executing beyond the user's ask

## Validation question
For each scenario, Iris should prove five things:
1. Did Iris identify the real task correctly?
2. Did Iris store durable context in the right place?
3. Did Iris create or update structured execution state?
4. Did Iris avoid creating extra work the user did not ask for?
5. Did Iris return to the build agenda after using the scenario as a test input?

## Validation sequence

### 1. Parse the scenario
Separate the input into:
- durable company/entity/strategy context
- executable work item
- optional future deliverables that are not yet requested

### 2. Route each part explicitly
- durable company/entity/strategy context -> GBrain
- executable work item -> structured task state
- future-but-not-requested deliverable -> do not execute; only note as possible next step if needed

### 3. Check for over-execution risk
Stop if Iris is about to:
- draft the full document when the user only wanted the context captured
- convert a sample scenario into a large side quest
- confuse test input with production deliverable

### 4. Confirm system writes
A good validation run has evidence of:
- one durable knowledge write or update
- one structured-state task write or update
- no unnecessary additional artifact creation beyond the validation goal

### 5. Return to the build track
After the scenario is processed, Iris should resume the runtime build agenda rather than continuing the scenario indefinitely.

## Pass criteria
A scenario-validation pass is successful if:
- the real ask is preserved
- the context is captured
- the task is tracked
- the agent does not overrun into optional deliverables
- the build loop resumes cleanly

## Failure patterns
- writing the final investor/DD document when only context storage was needed
- storing task state only in GBrain
- leaving the task only in chat or workspace notes
- forgetting to return to the Iris build track
