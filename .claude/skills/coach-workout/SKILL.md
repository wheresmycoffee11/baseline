---
name: coach-workout
description: Builds training — a single session, a week, or a four-week block — around the equipment, schedule, injuries, and goal in the user's profile, adjusted for their current recovery state. Use when the user says "/coach-workout", "build me a workout", "what should I train today", "give me a weekly plan", "make me a program", or asks what to do in the gym. Do NOT use for diet or calorie changes — use /coach-review. Do NOT use for logging a completed session — use /coach-log. Do NOT use for first-time setup — use /coach-setup. Do NOT use to coach technique on a movement the user reports pain in; that is a referral, not a programming problem.
---

# Coach Workout

## Read first

1. `reference/safety.md` — red flags, scope, when to refer out.
2. `health/profile.md` — **equipment, constraints, experience, schedule, dislikes.** The
   Constraints section is a hard gate, not a preference.
3. `reference/training-principles.md` — the evidence layer. Section 5 for capped load,
   section 8 for training in a deficit, section 9 for returning after a layoff.
4. The most recent file in `health/reviews/` — current recovery state and whatever the
   last review asked them to change.
5. `health/data/workouts.csv` — what they've actually been doing, as opposed to what was
   last prescribed.

If there's no profile, run `/coach-setup` first. Do not improvise defaults; a plan built
on guessed equipment is a plan nobody can run.

## Step 1 — Check recovery before you program

```bash
python3 scripts/trend_report.py --data health/data/daily.csv \
  --targets health/targets.json
```

Read `recovery` and `flags`.

- **Red flag** → no plan. Escalate per `reference/safety.md`.
- **Recovery gate active** (two or more of: HRV at or below 90% of baseline, resting heart
  rate 5+ above, sleep under 6h) → build a *smaller* week. Cut sets 30–50%, keep the
  sessions and the intensity. Say why in the plan.
- **A signal marked `valid: false`** → don't count it, and don't silently drop it either.
  Say which one is unavailable.
- **Data too thin to judge** → program conservatively and say so.

Doing this after drafting defeats the point. Recovery sets the size of the week.

## Step 2 — Establish the constraints

Write them down before you write a single exercise:

- Days per week and minutes per session, from the profile. **Take these literally.** Four
  45-minute sessions means four, and 45 minutes including warm-up and rest.
- Equipment, exactly as listed, with loads.
- Every injury and condition. For each, the movements it rules out.
- Dislikes.
- Goal and phase — cutting, gaining, maintaining.

Any movement you're about to program gets checked against this list. Every one.

## Step 3 — Build

**Split.** Match it to frequency. 2 days → full body. 3 → full body or push/pull/legs.
4 → upper/lower twice. 5+ → body-part or upper/lower/full. Total weekly volume per muscle
matters more than how it's divided (section 4).

**Volume.** Section 2 for ranges. **In a deficit, volume comes down and intensity stays**
(section 8) — the reverse of what most people do, and worth stating explicitly because
they'll be tempted to correct it.

**Load is usually capped.** Home equipment runs out long before the user does, especially
for legs. Don't treat it as a limitation to apologize for — pick a lever from section 5 and
name it: reps, then tempo and eccentrics, then unilateral work, then range of motion, then
density, then proximity to failure. Spend them in that order.

**Movement gaps.** If they have no pulling option, say so and recommend a band. Do not
present an unbalanced plan as balanced.

## Step 4 — Output

**A single session:**

- Name and time estimate
- Warm-up, 5–10 min, specific to what follows
- Main work: exercise, sets, reps, rest, target RIR
- Cooldown
- Notes: form cues, scaling up and down

**A week:** the split, each session in the format above, and how to progress next week.

**A four-week block:** weekly structure, what changes each week, week 4 as a deload, and
what to reassess at the end.

Always include: **what to do when a session goes badly.** Under-slept, short on time,
something hurts. A plan without an off-ramp gets abandoned the first bad week rather than
scaled.

## Step 5 — Score and revise

Run the loop in `plan-rubric.md`. Scoring is a separate pass. Maximum three cycles. Ship
the score line.

## Step 6 — Save

Write to `health/plans/YYYY-MM-DD-plan.md`.

---

## Scope

**v1 does single sessions, weeks, and four-week blocks.** Not longer periodization, not
competition prep, not peaking for a test. Those need someone watching the athlete, and
this tool can't.

## Things that will make this plan bad

- **Programming a movement their profile rules out.** The one genuinely dangerous failure.
  Check every exercise against Constraints.
- **Ignoring the recovery read** because the plan you drafted is nicer than the one the
  data supports.
- **Sessions that overrun.** 45 minutes means 45. Count warm-up and rest honestly.
- **Novelty in a deficit.** Not the time to learn movements or chase PRs (section 8).
- **Apologizing for their equipment.** Capped load is a programming problem with six known
  solutions, not a deficiency.
- **Promising hypertrophy in a deficit.** Say plainly that strength can hold but new muscle
  mostly won't arrive. Setting that expectation now prevents them quitting in week six
  believing they failed.

## Calibration

`gold-example.md` is a full worked week for the sample profile — capped dumbbells, a
shoulder that won't tolerate overhead load, and an active fat-loss deficit. Read it before
your first plan.
