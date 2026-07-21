---
name: coach-log
description: Records anything the phone didn't catch — a weigh-in, a meal, hours slept, an HRV reading, a workout, or how the week actually felt. Accepts free-form input and writes to health/data/daily.csv and health/journal.md. Use when the user says "/coach-log", "log my weight", "I slept badly", "fasted 18 hours", "did legs today", "squats felt heavy", or states any health number conversationally. Do NOT use for bulk Apple Health exports — use /coach-import. Do NOT use for analysis, verdicts, or recommendations — use /coach-review. Do NOT use for building a workout — use /coach-workout. Do NOT use for first-time setup — use /coach-setup.
---

# Coach Log

The gaps. Apple Health covers weight, sleep, steps, and heart data; it does not know you
fasted, that your knee hurt, or that the session felt like moving furniture. That context
is what makes a review readable a month later.

## Two destinations

**Numbers → `health/data/daily.csv`.** Upsert the row for that date.

**Everything else → `health/journal.md`.** Newest at the top, dated.

Most inputs produce both. "Slept about five hours, felt wrecked, skipped the workout" is a
sleep value *and* a journal line, and the journal line is the one that explains next week's
numbers.

## Rules for writing to the CSV

**Never overwrite device data with a manual entry without asking.** If the row already has
a value from `apple_health` and the user gives a different one, ask which is right. A
smart scale and a bathroom scale disagreeing is worth thirty seconds; silently clobbering
the record is not.

**Mark the source.** Set `entry_source` to `manual`, or append `+manual` if the row already
carries `apple_health`. The review needs to know which numbers came from a device.

**Only what they said.** No filling in gaps, no carrying yesterday forward, no estimating
a meal. A missing cell is honest; an invented one corrupts every average built on it.

**Default to today**, but ask if it's ambiguous. "Logged 2,100 calories" the morning after
a big day usually means yesterday.

## Parsing free-form input

Take it however it arrives:

- `"183.2, slept 7h, 1800 cal, 160p"` — a batch
- `"hrv was 52 this morning"` — one reading
- `"fasted 18 hours"` — journal, plus the fasting note
- a screenshot of a health app — read it, extract, confirm what you took
- `"legs today, squats felt heavy at 185"` — journal plus a `workouts.csv` row

Ambiguous units are worth one question. `"weight 92"` from someone on `lb` is a person who
switched scales or means kilos, and either way you shouldn't guess.

## Echo what you wrote

Always. One or two lines, showing the actual values and the date:

```
Logged for 21 July: weight 183.2, sleep 7.0h, 1,800 kcal, 160g protein.
Journal: "felt flat all afternoon"
```

The user needs to catch a misparse now, not discover it inside a review three weeks later.

## Stay in your lane

**Do not analyze.** Not even a little. "Nice, that's your best protein day this week" is a
verdict, and verdicts belong to `/coach-review` where the framework and the safety gates
apply. Logging that quietly editorializes becomes coaching without any of the checks.

The exception is safety. If something in the input hits a red flag in
`reference/safety.md` — chest pain, fainting, dizziness during training, a disordered-eating
pattern — respond to that immediately and directly. Don't file it away for the weekly
review. Read `reference/safety.md` for the language.

## Trends worth noticing

If the user asks a direct question while logging — "is that good?", "am I on track?" —
don't answer from the row in front of you. Offer the review:

> That's logged. Want me to run `/coach-review`? A single day won't tell either of us much,
> but two weeks will.

That isn't a deflection. It's the honest answer, and it's the same principle the whole pack
runs on.
