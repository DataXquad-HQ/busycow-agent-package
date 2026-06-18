# Cron Recovery / Resume Handling

Use this when a scheduled reporting workflow needs to be resumed, retried, or repaired.

## First rule: inspect before acting
Always start by listing jobs.
Do not guess a `job_id`.

Typical sequence:
1. `cronjob(action='list')`
2. identify the target job and current status
3. choose the right recovery path below

## Recovery paths by status

### 1. `paused`
Use when the schedule is intentionally halted and you want normal recurring execution to continue.

Action:
- `cronjob(action='resume', job_id='...')`

Optional follow-up:
- if you want to verify immediately after resuming, use `cronjob(action='run', job_id='...')`

### 2. job logic is wrong, but the schedule should stay
Use when the prompt, attached skills, schedule text, or delivery target needs correction.

Action order:
1. `cronjob(action='update', job_id='...', ...)`
2. `cronjob(action='run', job_id='...')` to verify the repaired version now
3. let the recurring schedule continue normally

### 3. last run failed, but the job definition is still correct
Use when the failure was transient (temporary network issue, channel outage, upstream data unavailable).

Action:
- `cronjob(action='run', job_id='...')`

Do **not** rewrite the skill or prompt if the underlying logic is still correct.

### 4. delivery failed after report generation
Use when the report logic succeeded but channel delivery broke.

Action order:
1. fix the delivery target or channel path
2. if job config must change, `update`
3. `run` once to redeliver

Do not paste the full report into the backend receipt as a workaround.

### 5. recurring job no longer wanted
Action order:
1. `cronjob(action='list')`
2. confirm the exact job
3. `cronjob(action='remove', job_id='...')`

### 6. one-shot schedule missed or needs replay
If the job still exists, prefer:
- `cronjob(action='run', job_id='...')`

If the original one-shot job was removed or must change meaningfully, create a new one-shot job instead of pretending the old schedule can be resumed.

## Decision rule: `resume` vs `run`

Use `resume` when:
- you want the paused recurring schedule to continue

Use `run` when:
- you want an immediate manual retry or verification run
- the last run failed transiently
- you repaired the job and want to test it now

Often the right repair for a paused recurring job is:
- `resume` to restore normal automation
- then `run` once for immediate verification

## Safe recovery checklist
Before declaring recovery complete:
- correct `job_id` verified from `list`
- if the issue was logic, the job was `update`d before rerun
- if the issue was only transient, use `run` without unnecessary rewrites
- if the job is recurring and had been paused, use `resume` rather than only `run`
- after repair, confirm whether the backend receipt and business-channel delivery both behaved as intended

## Common mistakes
- guessing `job_id`
- using `run` when you actually meant to restore the recurring schedule with `resume`
- using `resume` on a broken job before fixing the prompt/skills/delivery config
- deleting and recreating a healthy job when a simple `run` would retry it
- hiding delivery failure by dumping the full report into the final cron receipt
