# Plan rubric

Score every plan before shipping. Six dimensions, 0–10 each.

**Pass: 48/60 or better, no dimension below 6, both hard gates clear.**

---

## Hard gates

Pass/fail. Failing either means the plan does not ship at any score.

### G1 — Constraint compliance

**The plan uses only equipment listed in `health/profile.md`, and contains nothing the
profile's constraints rule out.**

This is the gate that matters most, because violating it is how a text tool hurts someone.
A plan containing overhead pressing for a person who wrote "no overhead work at load" is
not a plan with a flaw — it's a plan that will injure them, delivered by something they
trusted.

Check each movement against:

- **Equipment.** Listed, or bodyweight. Not "a light barbell if you have one."
- **Injuries and conditions.** Every entry under Constraints. If a constraint is vague
  ("bad knee"), program conservatively and say what you avoided and why, so they can
  correct you.
- **Dislikes.** Not a safety matter, but a plan built from movements someone hates is a
  plan they won't run. If a disliked movement is genuinely the best option, say why and
  offer the alternative anyway.

When a movement pattern can't be trained with what they have, **name the gap** rather than
quietly omitting it. An unbalanced plan presented as balanced is a lie of omission.

### G2 — Safety compliance

Read `reference/safety.md`. The plan fails if it:

- programs through a red flag instead of escalating
- coaches technique on a movement the user reports pain in — that's a referral, and no
  amount of written cueing substitutes for someone watching them move
- ignores a recovery stop from the most recent review
- prescribes a return-to-training progression after illness or injury faster than
  `reference/training-principles.md` section 9 supports

---

## Scored dimensions

### 1. Evidence alignment (0–10)

Volume, intensity, frequency, and progression sit inside the ranges in
`reference/training-principles.md`.

| | |
|---|---|
| 9–10 | Every variable defensible against the doc; deviations are stated and reasoned |
| 6–8 | Broadly sound, one variable drifting outside without comment |
| 3–5 | Volume or intensity chosen by feel |
| 0–2 | Contradicts the evidence layer |

The most common miss: prescribing volume appropriate to a surplus for someone in a
deficit. See section 8 — volume comes down, intensity stays.

### 2. Progression clarity (0–10)

| | |
|---|---|
| 9–10 | The user knows exactly what to change next week, and which lever to reach for when load is capped |
| 6–8 | Progression stated but generic — "add weight when you can" |
| 3–5 | Implied |
| 0–2 | Absent. It's a workout list, not a program |

At capped load this dimension carries the plan. Name the specific lever from section 5 and
the order to spend them in.

### 3. Recovery integration (0–10)

| | |
|---|---|
| 9–10 | Session load matches the profile's schedule and the latest review's recovery state; deload condition stated |
| 6–8 | Reasonable, but doesn't reference actual recovery data |
| 3–5 | Ignores available recovery signals |
| 0–2 | Prescribes more when the data says less |

If the last review flagged under-recovery, this plan is smaller. No exceptions.

### 4. Goal specificity (0–10)

| | |
|---|---|
| 9–10 | Visibly built for this person's stated goal; a different goal would produce a different plan |
| 6–8 | Appropriate but generic |
| 3–5 | A default template with their equipment substituted in |
| 0–2 | Unrelated to the goal |

### 5. Usability (0–10)

| | |
|---|---|
| 9–10 | Executable without interpretation. Sets, reps, rest, and a realistic time estimate that matches their stated session length |
| 6–8 | Clear but over-long, or the time estimate is optimistic |
| 3–5 | Requires decisions the user can't make |
| 0–2 | Unusable as written |

A 45-minute session means 45 minutes including warm-up and rest. Count it honestly. Plans
that run 70 minutes get abandoned in week two, and the user concludes they lack discipline.

### 6. Honesty (0–10)

| | |
|---|---|
| 9–10 | States what the plan can't do; names equipment gaps; sets realistic expectations, especially in a deficit |
| 6–8 | Mostly honest, some overselling |
| 3–5 | Promises outcomes the evidence doesn't support |
| 0–2 | Markets the plan |

In a deficit specifically: say up front that performance will flatten and new muscle
mostly won't arrive (section 8). Setting that expectation at the start is the difference
between a user who holds course and one who quits in week six believing the program
failed.

---

## The loop

Draft → score in a separate pass → revise the failing dimension → re-score in full.
Maximum three cycles. Ship the score line:

```
Rubric: 53/60 (evidence 9, progression 9, recovery 9, specificity 9, usability 8, honesty 9)
```

Never present a sub-threshold plan as finished.

## Diagnosing a stuck score

| Stuck on | Usually means |
|---|---|
| Constraint compliance | You reached for a standard movement without checking the profile. Re-read Constraints and rebuild the slot |
| Progression | Load is capped and you haven't picked a lever. Section 5, in order |
| Usability | The session is too long. Cut accessory volume, not the main work |
| Honesty | You're avoiding telling them something true about their timeline |
