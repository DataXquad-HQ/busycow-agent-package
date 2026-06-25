# Iris Output Contracts

## Daily operating brief
Should include:
- key state changes
- blocked items
- missing owners / deadlines
- pending approvals
- required human decisions
- source-of-truth or context-risk items only if material

## Source-of-truth check
Must include:
- information type being checked
- expected authority layer
- actual source being used
- whether the source is correct, degraded, or wrong
- consequence if the wrong source is used

## Context conflict check
Must include:
- conflicting statements quoted clearly
- source class for each statement
- authority ranking
- materiality assessment
- stop / verify / escalate recommendation

## Review queue triage
Must include:
- only the meaningful queue items
- why each item matters now
- missing metadata if incomplete
- one of: review now / hold / reject / gather evidence / escalate

## Handoff briefing
Must include:
- task title
- owner
- deadline
- current status
- why it matters
- relevant decision/policy
- evidence links
- recall query
- expected output
- approval boundary
- escalation trigger

## Scenario mode boundary
When the user is providing a test case or example rather than asking for the final business artifact:
- say explicitly that the case is being treated as validation input
- capture context and task state only as needed for the test
- do not expand into the full downstream deliverable unless the user asks
- return to the original build/workflow after the validation step

## Weekly memory audit
Must include:
- only meaningful findings
- promotion candidates with destination and rationale
- stale / conflicting memory notes
- explicit statement when input is thin or confidence is degraded

## Validation rule
Before any daily or weekly cron summary is sent:
- check the output against the nearest schema in `schemas/`
- score it against the matching rubric in `evaluators/`
- compare tone and structure against the closest example in `examples/`
- if it resembles an anti-example, rewrite before sending
