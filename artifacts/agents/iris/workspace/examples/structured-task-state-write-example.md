# Example — Structured Task State Write

This example uses the **live [Org] legacy Lark Base task tracker via app identity** as the current executable fallback path.

## Actual write that landed

A real task was created to prove the V1 structured-state write path:

- record id: `recvnwKxNmYE5k`
- title: `Iris V1 closure — validate live operating loop`
- business line: `[Org]`
- priority: `🟡 Medium`
- owner: `[Founder 1]`
- status: `Done = false`
- deadline: `2026-07-04`

## Why this example matters

- It proves Iris can create a real structured task record instead of leaving the work only in chat or workspace notes.
- It gives the V1 closure pass a real system-of-record anchor for later human testing.
- It demonstrates the current fallback rule: target layer is Lark Tasks, executable path today is the legacy Base tracker.

## Good interpretation

- This does **not** mean Base is the long-term preferred execution layer.
- It means the runtime now has one verified live write path while default Lark Tasks are not yet exposed through tools.
