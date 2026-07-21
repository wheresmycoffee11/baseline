# Gold example — a worked review

The calibration reference. Read it before your first review.

Run against `sample-data/` as of 2026-06-30. Reproduce the input with:

```bash
python3 scripts/trend_report.py --data sample-data/daily.csv \
  --targets sample-data/targets.json --pretty
```

**This case is a trap.** The scale has stalled in a fat-loss phase, and the obvious move —
cut calories — is wrong. Getting it right requires walking the gates in order rather than
jumping to the interesting number.

---

## The review

> ## Weekly review — 30 June 2026
>
> **Where you are**
>
> Your 7-day average is 202.7 lb, down 0.3 from the week before. Over 14 days you're
> losing 0.43 lb a week — 0.21% of bodyweight. You aimed for 0.5%. So it's moving, at
> roughly half the pace you planned.
>
> **What's working**
>
> Your weekdays are dialled in. Over the last 14 days weekday intake averaged 2,118
> against a 2,100 target — 18 calories off across ten days. That is genuinely hard to do,
> and it is the reason this is a fixable problem rather than a plan problem.
>
> **What's actually happening**
>
> Weekends. Same window, weekend intake averaged 2,610 — 510 a day over target. Across two
> days a week that's about 1,020 calories, which is most of your weekly deficit handed
> back.
>
> It isn't only food. Weekend steps averaged 4,620 against 8,410 on weekdays, so the same
> two days cut intake up and activity down together.
>
> Calorie adherence over 14 days is 54% — 7 days in band out of 13 logged. One Saturday
> has no food logged at all. I'd guess it wasn't the quietest day of the fortnight.
>
> **The one change**
>
> A weekend ceiling: 2,400 on Saturday and Sunday.
>
> Not 2,100. A weekend target identical to your weekday target is a rule you'd break by
> lunch, and a ceiling you break is worse than no ceiling. 2,400 still covers a real dinner
> out, and it takes the weekend excess from about 1,020 a week to about 600.
>
> **Weekdays stay exactly as they are.** Do not cut them. They're hitting target and
> cutting a number you're already hitting just makes you hungry without making you lighter.
>
> **What I'm not changing, and why**
>
> Your 2,100 target stays. With adherence at 54%, changing a target you aren't currently
> hitting only widens the gap between the plan and what you do.
>
> One thing to flag, not to act on yet: your actual maintenance looks like about 2,445,
> back-calculated from 27 days of logged intake against measured weight change. Setup
> estimated 2,650. That gap means your 2,100 target was always going to produce slower loss
> than the 0.5% you wanted — even at perfect adherence. It needs correcting. But correcting
> a target using data this leaky would just bake the leak into the new number. Weekends
> first, then we set it properly.
>
> **Recovery**
>
> Nothing concerning. Sleep averaged 7.1 hours over the last week, up from a rough patch
> mid-month. HRV and resting heart rate are both sitting in your normal range.
>
> **Next review: 14 July.**
>
> What I expect: weekend average under 2,400, adherence above 75%, and the 14-day rate
> moving toward 0.3%/week. If weekends hold and the rate still lags, that's when we correct
> the target — and we'll know the number is real.
>
> ```
> Rubric: 54/60 (framework 10, lever 9, actionable 9, honesty 9, signal 8, tone 9)
> ```

---

## Why it scores what it does

**Framework fidelity — 10.** The gates ran in order and the stop is visible. Gate 0 clear
(no red flags). Gate 1 clear (14 weigh-ins, 13 logged days). **Gate 2 fired** at 54%
adherence, which froze every target. Rule 4's rate check was therefore never reached — and
the review says so out loud in "What I'm not changing," rather than leaving the reader to
wonder whether the stall was noticed.

**Single-lever — 9.** One instruction: a weekend ceiling. Three other real findings are
named and explicitly not prescribed — the TDEE gap, the weekend step collapse, and protein
(weekday average 140 against a 150 floor, 38% adherence). Losing a point because the step
observation sits close to reading as a second instruction. It's kept because it explains
*why* weekends cost double, not as a second task.

**Actionability — 9.** A number, the days, the mechanism, and the expected effect. Someone
can execute this on Saturday without interpreting anything.

**Honesty — 9.** Three places the review declines to overreach: it calls the unlogged
Saturday a guess rather than a fact; it gives the TDEE figure with its basis (27 days,
logged intake) so the reader can weigh it; and it doesn't claim the weekend fix will reach
target, because the arithmetic says it won't. That last one matters — promising a result
the numbers don't support is how a tool loses someone in a fortnight.

**Signal — 8.** 430 words. The verdict is in the first two sentences. Docked for the
recovery section, which could be one line, and for "What I'm not changing" running long —
though the TDEE explanation earns most of its length.

**Tone — 9.** "That is genuinely hard to do" is specific praise for a specific behaviour,
not cheerleading. The unlogged Saturday is handled with a light touch and no accusation.
No moralizing about the weekend.

## What it deliberately does not do

**It doesn't cut calories.** The obvious read of a stall. Gate 2 forbids it, and the
diagnosis shows why it would have been actively harmful: weekdays are already on target,
so a cut lands entirely on the five days that are working and does nothing to the two that
aren't.

**It doesn't fix the TDEE estimate**, despite having a good 27-day figure and knowing the
target is wrong. Correcting a target from leaky data bakes the leak in. Sequencing beats
completeness.

**It doesn't call HRV a green light.** HRV sat at 109% of baseline — above it. The review
says "normal range" and moves on. Per `reference/recovery-principles.md`, direction is not
reliably meaningful, and "your HRV is up, push harder" is a claim the evidence won't carry.

**It doesn't cite a single day's weight.** The latest reading was 200.89 — nearly two
pounds below the 7-day average, and the most encouraging number available. Quoting it
would have been the friendliest possible lie.

## The failure mode this case exists to catch

A review that opens with "you've stalled — let's drop to 1,900" scores well on
actionability and terribly everywhere else. It's confident, concrete, and wrong: it
punishes five compliant days to fix two non-compliant ones, and it moves a target the user
demonstrably isn't following.

If your draft reaches for the calorie target before it has looked at the weekday/weekend
split, stop and re-walk the gates.
