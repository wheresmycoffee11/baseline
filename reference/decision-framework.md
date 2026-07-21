# Decision framework

The ordered rules `/coach-review` executes. Walk them top to bottom, every time. Do not
reorder them, do not skip ahead because something further down looks more interesting,
and cite the rule that fired.

Every threshold below points at a specific field in the output of
`scripts/trend_report.py`. If you're about to state a number that isn't in that JSON,
stop — you're making it up.

---

## Before anything: which window to trust

The report gives 7, 14, and 28-day windows. They disagree, sometimes sharply, and picking
the flattering one is the easiest way to lie with real data.

- **Rate-of-change decisions run on the 14-day window** (`weight.windows.14d`). Seven days
  of weight is mostly noise — in testing, a 7-day slope read −0.82%/week on the same data
  where 14 days read −0.21%. Fourteen days is the shortest window that's stable enough to
  act on.
- **The 7-day rolling average** (`weight.current_7d_avg`) is for *describing* where someone
  is right now, and for the week-over-week comparison. Not for deciding a rate.
- **28 days** is context: is this a two-week blip or a month-long pattern?
- **Never cite a single day's weight as evidence of anything.** If the user does it, say
  so — kindly, once. Daily movement is water, sodium, glycogen, and gut contents.

---

## Gate 0 — Safety

Read `flags[]`. Any flag with `severity: "red"` ends the review.

Ship the concern and nothing else. No target changes, no training notes, no "but
otherwise you're doing great" — that sentence is how a person talks themselves out of
seeing a doctor.

Amber flags don't stop the review, but they must be addressed somewhere in it and they
constrain what you're allowed to recommend (see Gate 3).

Full escalation language and the red-flag list live in `reference/safety.md`. Read it.

---

## Gate 1 — Is there enough data?

Read `coverage`.

| Condition | Response |
|---|---|
| `sufficient_for_weight_verdict: false` (under 10 weigh-ins in 14 days) | No weight verdict. No calorie change. The one recommendation is to weigh in more consistently. |
| `sufficient_for_intake_verdict: false` (under 10 logged days) | No macro verdict, no calorie target change. |
| `food_logging_active: false` (under 4 logged days in 14) | **Observed-only mode.** See below. |
| `data_is_stale: true` | Lead with it. Advice on three-week-old numbers is fiction. |

**Never change a target on thin data.** The temptation is real — the user asked a
question and "not enough data yet" feels like a non-answer. It isn't. It's the only
honest one, and saying it plainly builds more trust than a confident guess that turns out
wrong.

### Observed-only mode

Plenty of people never log food. Baseline still works, it just coaches differently:

- Use `energy.tdee_observed` if available; otherwise weight trend alone
- Coach steps, sleep, training consistency, and behavior
- Ask what changed rather than inferring it from macros you can't see
- Recommend food logging **once**, framed as what it would unlock. Then let it go. A
  coach who brings it up every week gets ignored on everything else.

---

## Gate 2 — Adherence before the program

Read `intake.adherence`.

**If calorie adherence is under 80%, do not change any target.** Not the calories, not
the macros, not the training. The plan is not what's broken.

This is the rule most likely to be violated, because changing a number feels like
coaching and asking about someone's Saturday doesn't. But cutting the target of a plan
that isn't being followed just widens the gap between the plan and the person, and the
next review will show worse adherence, not better.

Instead, find the leak. The daily rows are right there:

- **Which days?** Weekends and weekdays are usually different problems with different
  fixes.
- **What's the pattern?** Steady overshoot means the target is wrong. A few large spikes
  against otherwise good days means specific situations are the problem — travel, social
  meals, one bad evening.
- **Did logging stop, or did intake rise?** Missing rows on the worst days are a signal in
  themselves, and worth naming without judgment.

Then prescribe exactly one behavioral change aimed at the leak.

**Cap the ceiling before you lower the floor.** When someone's weekdays are fine and their
weekends undo them, a hard upper limit on the bad days beats cutting an already-hard
weekday target. It's more survivable, it protects the days that are working, and it
usually closes more of the gap.

---

## Gate 3 — Recovery before intensity

Read `recovery`. If `recovery.hrv.valid` is false, that signal is out — either the
baseline is too thin or heart-rate medication is flagged. Say which; don't silently drop
it.

The gate fires when **at least two** of these are true:

- `recovery.hrv.pct_of_baseline` ≤ 90
- `recovery.rhr.delta` ≥ 5 bpm
- `recovery.sleep.mean_7d` < 6, or `nights_below_floor_7d` ≥ 4

**Two, not one.** Real under-recovery shows up across several signals at once. One bad
HRV week on its own is noise, and over-reacting to it is the most common failure in
consumer recovery tracking — it trains people to distrust the tool.

**Do not present that 90% as a measured threshold.** Per
`reference/recovery-principles.md`, essentially every published HRV cut-point was derived
from RMSSD, while Apple Health reports SDNN — so the number is borrowed from a different
index, and within-person day-to-day variation is large enough (mean CV ≈ 0.37) that
Buchheit puts the signal-to-noise ratio of resting HRV below 1. It is a defensible
convention, not a measurement.

Say **"below your usual range"**, not "you crossed the threshold." Read that file before
you say anything about HRV at all; it is more skeptical than the consumer-wearable
framing most people arrive with, and that skepticism is the point.

The report marks a signal `valid: false` when the baseline is too thin, when there are
fewer than three readings in the week, or when heart-rate medication is flagged. **An
invalid signal cannot count toward the two.** Say which one dropped out and why rather
than quietly running the gate on what's left.

**HRV above baseline is not a green light.** This gate is deliberately one-directional —
it fires on suppression only — but that is a design choice about which errors are
tolerable, not a claim that high HRV means recovered. Plews et al. found that in elite
athletes *both* directions have been linked to negative adaptation, and that fitness
gains have shown up alongside HRV *decreases*. So never answer "your HRV is up, push
harder." If someone is well recovered, the evidence for that is training performance and
how they feel, not a number that moved the way they hoped.

When it fires, the one change is a recovery intervention, in this order:

1. **Sleep**, if that's the signal that's off. Everything else is downstream.
2. **Training volume** — cut sets by 30–50% for a week. Keep the sessions, shrink them.
3. **Intensity**, only if volume has already come down and things haven't recovered.
4. **A full deload week**, if this has persisted past two weeks.

Diet targets are untouched while this gate is active. Adding a deficit on top of
under-recovery is how people get hurt or quit.

---

## Rule 4 — Fat loss: rate check

Only reached if Gates 0–3 are clear, adherence is at or above 80%, and the goal is fat
loss. Read `weight.windows.14d.pct_bw_per_week` against
`targets.weight_change_target_pct_bw_per_wk`.

| Observed rate | Response |
|---|---|
| Within ±0.25% of target | **Change nothing.** Say so plainly, name what's working, give the next review date. |
| Slower than target by more than 0.25% for 2+ weeks | Reduce calories 5–10%, **or** raise the step floor. One, not both. |
| Faster than 1% BW/week | Raise calories 5–10%. Name the muscle-loss risk. This is not "ahead of schedule." |
| Flat for 14+ days | Same as "slower," but check `energy.tdee_observed` first — see below. |

**Check observed TDEE before cutting.** If `energy.tdee_observed` has landed and differs
from `energy.tdee_estimate` by more than about 150 kcal, the original target was built on
a bad estimate. Correct the target to match reality and explain that — it's a better
answer than an arbitrary 10% cut, and it's the kind of thing that makes someone trust the
system.

**Never cut below `targets.safety.min_calories` or below `energy.rmr_estimate`.** If the
arithmetic wants to go there, the answer is more activity or a slower timeline, not less
food.

**Wait at least 14 days between calorie changes.** Anything faster and you can't attribute
the result to the change.

---

## Rule 5 — Muscle gain

- Gaining under 0.25% BW/month with good adherence → increase calories 5%
- Gaining faster than 0.5% BW/week → reduce 5%; most of that is not muscle
- Protein below `targets.protein_floor_g` → fix that before touching calories

## Rule 6 — Recomposition

Expect the scale to sit still. Say so up front, repeatedly, because a flat scale reads as
failure to almost everyone. Coach on training progression, `body_fat_pct` if a smart
scale is feeding it (with the caveat that consumer body-fat readings are directionally
useful at best), strength trend, and how clothes fit. Do not chase scale movement.

## Rule 7 — Performance stall

Gate 3 first — most stalls are under-recovery wearing a costume. If recovery is clean and
a lift hasn't moved in three or more exposures, change one variable per
`reference/training-principles.md`: rep range, exercise variation, volume, or proximity
to failure.

---

## Rule 8 — One change

**At most one diet change and one training change per review.** Usually that means one
change total.

Every recommendation ships with:

- What to do, concretely enough to act on tomorrow
- What you expect to happen, in numbers
- When to re-check — normally 14 days

Changing three things at once means learning nothing from any of them. And a person given
three instructions follows zero.

---

## The most common correct answer

**Change nothing.**

When adherence is good and the rate is in band, the job is to say so, name specifically
what's working so it gets repeated, and get out of the way. A review that manufactures an
adjustment to feel useful is worse than no review — it churns a plan that's working and
teaches the user that the tool always wants something changed.

Write it as a verdict, not an apology:

> Nothing to change. You're down 1.6 lb over 14 days, which is 0.55% of bodyweight per
> week and right where we aimed. Protein hit the floor on 12 of 14 days. Keep going.
> Next check-in 14 July.
