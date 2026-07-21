# Review rubric

Score every review against this before shipping it. Six dimensions, 0–10 each.

**Pass: 48/60 or better, with no dimension below 6, and both hard gates clear.**

Score honestly. A rubric you always pass is a rubric that isn't measuring anything — if
your first drafts never score below 50, you're grading the draft you wanted to write
rather than the one on the page.

---

## Hard gates

These are pass/fail. Failing either means the review does not ship at any score.

### G1 — Data fidelity

**Every number in the review appears in the `scripts/trend_report.py` output.**

Not "is consistent with." Appears in. If you wrote "you're averaging about 2,200
calories," that figure must be in the JSON. Derived arithmetic done in your head — adding
two windows, converting a rate, estimating a weekly total — is a fail even when it's
correct, because the next one won't be.

The only permitted arithmetic is subtraction between two figures that both appear in the
report, and only when you show it.

Why this is absolute: a fabricated number in health advice is worse than no advice. It
is confidently wrong, unfalsifiable by the reader, and it is the single failure mode that
would make this tool dangerous rather than merely unhelpful.

### G2 — Safety compliance

Read `reference/safety.md`. The review fails if it:

- proceeds past a red flag with coaching instead of escalation
- sets any target below a hard floor
- recommends a rate of loss above 1% bodyweight per week
- treats weight, calories, or body composition as coachable in `habit_only` mode
- interprets a medication, symptom, or lab value
- responds to a disordered-eating signal by tightening anything

---

## Scored dimensions

### 1. Framework fidelity (0–10)

Gates walked in order, and the review names which rule fired.

| | |
|---|---|
| 9–10 | Gates walked in order; the governing rule is named; where a lower gate stopped a higher one from being reached, that's stated |
| 6–8 | Right conclusion, but the path isn't visible — reader can't tell why *this* recommendation |
| 3–5 | Gates skipped or reordered; jumped to the interesting finding |
| 0–2 | Freelanced entirely |

The common failure: adherence is under 80% but the review adjusts a target anyway,
because changing a number feels like coaching and asking about someone's Saturday doesn't.

### 2. Single-lever discipline (0–10)

| | |
|---|---|
| 9–10 | Exactly one change, or an explicit and well-argued zero |
| 6–8 | One primary change, but secondary suggestions blur it |
| 3–5 | Two or three changes presented as a set |
| 0–2 | A list |

Noticing something is not the same as prescribing it. You may name a second issue as
next-in-line; you may not instruct on it.

### 3. Actionability (0–10)

| | |
|---|---|
| 9–10 | Executable tomorrow without interpretation. Specific number, specific days, expected effect, re-check date |
| 6–8 | Clear but soft — "focus on weekends" rather than a ceiling and a figure |
| 3–5 | Restates the goal as if it were a plan |
| 0–2 | Advice that could be given to anyone |

"Eat less on weekends" fails. "Cap Saturday and Sunday at 2,400" passes.

### 4. Honesty about uncertainty (0–10)

| | |
|---|---|
| 9–10 | States what the data can't support; flags thin coverage; distinguishes measurement from inference; says "not enough data" where true |
| 6–8 | Broadly honest, but a couple of claims outrun their evidence |
| 3–5 | Consistently more confident than the data warrants |
| 0–2 | Presents inference as measurement |

Specifically: never present an HRV threshold as measured (see
`reference/recovery-principles.md`), never treat a single day's weight as signal, and
never imply a back-calculated TDEE is more precise than the food logging behind it.

### 5. Prioritization and signal (0–10)

| | |
|---|---|
| 9–10 | Biggest lever first; under ~600 words; nothing present that doesn't change what the reader does |
| 6–8 | Right priority, padded |
| 3–5 | Buries the finding under a metrics recap |
| 0–2 | A dashboard in prose |

The reader has a body, not a spreadsheet. If everything is included, nothing is
prioritized.

### 6. Tone (0–10)

| | |
|---|---|
| 9–10 | Plain, direct, non-judgmental. Names what's working specifically. Treats adherence as information |
| 6–8 | Fine, with some hedging or filler |
| 3–5 | Moralizing, cheerleading, or clinical coldness |
| 0–2 | Shames, or congratulates something that shouldn't be |

Never moralize about food or a missed session. No "cheating," no "earning," no "being
good." Never congratulate a large loss without checking how it happened.

---

## The loop

1. Draft.
2. Score against all six, writing the score line out. Scoring is a **separate pass** —
   don't score while drafting, you'll grade your intentions.
3. Below threshold? Revise the specific dimension that failed. Not a general polish.
4. Re-score in full. A revision that fixes dimension 3 often breaks dimension 5.
5. Maximum three cycles. Still failing? Ship it with the score line and say which
   dimension is short and why.

Never present a sub-threshold review as finished.

**Ship the score line.** It goes at the foot of the review:

```
Rubric: 52/60 (framework 9, lever 9, actionable 9, honesty 8, signal 9, tone 8)
```

This is not decoration. Self-scoring is weaker than an independent reviewer, so the
transparency is doing the work the independent reviewer would have done — it lets the
reader see what the review thinks of itself.

---

## Diagnosing a stuck score

| Stuck on | Usually means |
|---|---|
| Data fidelity | You're reaching for a number the report doesn't have. That's a data gap — say so, don't estimate around it |
| Actionability | The recommendation isn't concrete because the diagnosis isn't. Go back to the daily rows |
| Single-lever | You found two real problems. Pick the upstream one; the other often resolves on its own |
| Signal | You're explaining your reasoning instead of giving the verdict. Cut the methodology |
| Honesty | You want to say something the data won't support. Say the smaller true thing |
