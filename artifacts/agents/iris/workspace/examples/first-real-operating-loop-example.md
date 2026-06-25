# Example — First Real Operating Loop

## Scenario
A partner follow-up is mentioned in chat as if it is already owned, but the task tracker still shows no accountable owner. At the same time, repeated chat suggests a new partner-enablement rule may be needed.

## Good V1 behavior

1. **Scan for signal**
   - Iris finds one partner follow-up with no owner and one review candidate that may affect partner process.

2. **Check source of truth**
   - Iris confirms that chat memory says the follow-up is "covered".
   - Iris confirms the task system still shows no owner.
   - Result: task system wins for current state.

3. **Resolve only the material conflict**
   - Iris treats this as material because unowned partner follow-up can delay outreach.

4. **Route the task**
   - Iris creates or updates the routed work item.
   - Owner is explicit.
   - Why-it-matters and deadline are attached.

5. **Create the handoff**
   - Iris prepares a handoff packet with evidence links and approval boundary.

6. **Stage governed knowledge separately**
   - The repeated partner-enablement pattern is not written straight into canonical knowledge.
   - Iris stages a review item instead.

7. **Send the operating brief**

**Main takeaway: execution can move today, but one ownership gap and one governance item need attention.**

- **Verified** — The partner follow-up is still unowned in the task system.
- **Verified** — Chat context was ahead of the system of record, so the status needed correction.
- **Risk** — A repeated enablement pattern may matter, but it is not approved doctrine yet.
- **Recommendation** — Assign the partner follow-up owner now and keep the enablement change in review until approved.

## Why this is a good V1 loop
- It uses the right authority layer for current status.
- It turns a signal into assigned work.
- It keeps governance separate from execution.
- It ends with a short human-readable brief instead of a process dump.
