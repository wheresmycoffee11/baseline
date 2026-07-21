---
name: coach-review
description: The weekly check-in. Reads the trend report, walks the decision framework, and delivers a verdict plus at most one thing to change — often nothing. Use when the user says "/coach-review", "how am I doing", "what should I change", "review my week", "check in", or asks whether their diet or training is working. Do NOT use for importing data — use /coach-import. Do NOT use for logging numbers — use /coach-log. Do NOT use for building a workout or training block — use /coach-workout. Do NOT use for first-time onboarding — use /coach-setup. Do NOT run this on fewer than 14 days of data expecting a full verdict; it will correctly refuse and tell the user to keep logging.
---

# Coach Review

The skill this pack exists for. Everything else feeds it.

## Read first, every time

1. `reference/safety.md` — floors, red flags, scope. Non-negotiable.
2. `reference/decision-framework.md` — the ordered gates you're about to walk.
3. `health/profile.md` — goal, constraints, equipment, what they told you at setup.
4. The most recent file in `health/reviews/` — so you don't contradict yourself or
   re-recommend something already in flight.
5. `health/journal.md`, recent entries — the context the numbers can't carry.

Pull in `reference/nutrition-principles.md`, `training-principles.md`, or
`recovery-principles.md` when a recommendation touches them. Don't read all three by
reflex.

## Step 1 — Run the numbers

```bash
python3 scripts/trend_report.py --data health/data/daily.csv \
  --targets health/targets.json --pretty
```

**Do this before you form an opinion.** Reading the CSV first and then running the script
to confirm what you already decided is backwards, and it's how invented numbers get in.

If the script errors or the data file is missing, say so and stop. Do not read the CSV
and do the arithmetic yourself — that's a hard rubric fail and the reason the script
exists.

Every figure you cite comes from this output. See gate G1 in `review-rubric.md`.

## Step 2 — Walk the gates

In order, per `reference/decision-framework.md`:

- **Gate 0** — red flags. Any `severity: "red"` and the review is an escalation, full stop.
- **Gate 1** — data sufficiency. Thin data means a tracking fix, not a program change.
- **Gate 2** — adherence. Under 80% and no target moves. Find the leak instead.
- **Gate 3** — recovery. Two corroborating signals before you touch training.
- **Rules 4–7** — the goal-specific rate checks.
- **Rule 8** — one change.

When a gate stops you from reaching a lower rule, **say so in the review.** "I'm not
changing your calories, and here's why" is more useful than silence, and it stops the
user wondering whether you noticed.

### Finding the leak

When Gate 2 fires, the daily rows are the evidence. Read them directly and look for:

- **Which days.** Split weekday and weekend and compare the means. This is the single
  most common pattern and it's invisible in a weekly average.
- **Steady drift or spikes.** Consistent overshoot means the target is wrong. A few large
  days against otherwise good ones means specific situations are the problem.
- **Missing rows.** Days that weren't logged are usually not the light ones. Name it
  without accusation — "one Saturday isn't logged" is a fact, not a charge.
- **What else moves with it.** Steps often collapse on the same days intake climbs. That
  doubles the gap and it's worth showing.

## Step 3 — Draft

Fixed sections, in this order. Skip any that has nothing to say — an empty heading is
noise.

**Where you are.** The 7-day average, the week-over-week change, and the 14-day rate
against target. Three sentences.

**What's working.** Specific, not encouraging. "Your weekdays averaged 2,118 against a
2,100 target" tells someone what to keep doing. "Great consistency!" doesn't.

**What's actually happening.** The diagnosis, with the numbers that support it.

**The one change.** Concrete enough to execute tomorrow. A number, the days it applies
to, and what you expect it to do.

**What I'm not changing, and why.** Where a gate held you back, or where you spotted
something real that isn't this week's priority.

**Recovery.** Only if there's something to say. "Nothing concerning" in one line beats a
paragraph of normal readings.

**Next review.** A date, and what you expect to see by then.

## Step 4 — Score and revise

Run the loop in `review-rubric.md`. Scoring is a separate pass from drafting. Maximum
three cycles. Ship the score line.

## Step 5 — Save

Write to `health/reviews/YYYY-MM-DD-review.md`. Next week's review reads it.

If you changed `health/targets.json`, say exactly what changed and why, in the review.
Never edit targets silently.

---

## The answer that's usually right

**Change nothing.**

When adherence is good and the rate is in band, say so, name what's working so it gets
repeated, and stop. A review that manufactures an adjustment to justify its own existence
churns a working plan and teaches the user that this tool always wants something changed —
after which they stop reading it.

Write it as a verdict, not an apology. See the closing example in
`reference/decision-framework.md`.

## Things that will make this review bad

- **Doing arithmetic yourself.** The most likely serious failure. Run the script.
- **Coaching the interesting finding instead of the important one.** A subtle recovery
  pattern is more fun to write about than "your weekends are the whole problem."
- **Changing a target during a Gate 2 stop.** Feels like coaching. Is not.
- **Treating HRV above baseline as a green light.** It isn't one. See
  `reference/decision-framework.md`.
- **Hedging.** If the data supports a verdict, give it. If it doesn't, say that. The
  space between those is where useless reviews live.
- **Length.** Under 600 words. Everything you include competes with the one thing you
  want them to do.

## Calibration

`gold-example.md` is a full worked review against `sample-data/`, annotated with why it
scores what it does. Read it before your first review. The case it handles is deliberately
a trap — the obvious read of that stall is wrong.
