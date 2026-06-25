# Context Router and Governance Pattern

## Purpose
The installer agent should understand that context writes are not freeform.

## Core pattern
- direct low-risk writes may go to workspace, evidence, or personal memory
- reviewed writes are required for canonical knowledge changes, policy changes, and cross-agent behavior changes
- current-state truth belongs in structured systems, not memory

## Minimum governance surfaces
- review queue or equivalent staging layer
- approval owner
- logging for publish / promotion actions
- clear split between human-readable ops output and machine logs
