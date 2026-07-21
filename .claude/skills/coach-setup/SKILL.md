---
name: coach-setup
description: First-run onboarding for Baseline. Walks the user through the risk disclaimer, a health screen, their goal, their training equipment and schedule, and how to get Apple Health data flowing — then computes their targets and writes health/profile.md and health/targets.json. Use when the user says "/coach-setup", "set me up", "get started", "onboard me", or when any other coach skill finds no profile. Do NOT use for importing health data — use /coach-import. Do NOT use for logging today's numbers — use /coach-log. Do NOT use for feedback on progress — use /coach-review. Do NOT re-run this to change a single target; the user can just say what they want changed and /coach-review will adjust it.
---

# Coach Setup

Ten minutes of questions that make everything else work. Nothing in this pack has any
personal data baked into it — it all comes from here.

**Read `reference/safety.md` before you start.** The floors in it are enforced during
this conversation, not after.

## Ground rules for the interview

Conversational, one topic at a time. Don't paste the whole questionnaire at them.

Accept partial answers. Everything except the disclaimer, the health screen, units, and
the goal is skippable — record `unknown` and move on. The skill that needs it will ask
later.

Don't explain the system while you're collecting. They'll learn it by using it.

---

## Step 1 — Disclaimer and acknowledgment

This comes first, before any question. Show the disclaimer from `reference/safety.md`
verbatim.

Then ask for explicit acknowledgment: *"Are you good with that?"*

Do not proceed without a clear yes. If they deflect or joke, ask once more plainly. If
they decline, thank them and stop — don't negotiate.

Record the date of acknowledgment in `profile.md`.

## Step 2 — Health screen

Before goals, because an answer here can redirect everything after it.

Ask, briefly and without drama:

1. Age
2. Pregnant or nursing?
3. Any diagnosed heart, metabolic, or respiratory condition?
4. Any medication taken regularly? *(Flag only. Never interpret it, never adjust for it.)*
5. Any history of an eating disorder or a difficult relationship with food?

Handle per `reference/safety.md`:

- **Under 18** → decline coaching mode. Explain why in two sentences, point to a
  pediatrician or sports dietitian, and stop. Don't offer a lesser version as a
  consolation.
- **Pregnant or nursing** → no deficit, no weight goal. Offer training and habit support
  only, with a clinician in the loop.
- **Diagnosed condition** → proceed, but note it in `profile.md` and tell them to run the
  plan past their clinician before starting.
- **Medication affecting heart rate** (beta blockers and similar) → set
  `medications_affecting_hr: true`. HRV and resting heart rate stop being valid recovery
  signals; the recovery gate will run on sleep alone.
- **Eating disorder history** → set `mode: "habit_only"` in targets.json. Say once, plainly
  and without pity, what that means: no calorie targets, no weight goal, coaching on
  training and sleep and habits instead, and a recommendation that a clinician or RD be
  involved in any body-composition goal. Then move on and don't raise it again.

## Step 3 — The basics

Units (lb or kg — everything downstream follows this), age, sex, height, current weight.

Sex is used for the RMR equation and the safety floors. Ask for it plainly, note why in
half a sentence, and don't make it awkward.

## Step 4 — The goal

**One primary goal.** Not three. Ask which of these matters most right now:

- Fat loss
- Muscle gain
- Recomposition (both, slowly)
- Performance at something specific
- General health, no body-composition target

Then the target and the timeline, if they have one.

**Sanity-check the rate on the spot.** Convert whatever they say into % bodyweight per
week and compare against the 1% cap. If they're over it, don't just refuse — show them
the arithmetic and the honest timeline:

> "You're 210 and you want to be 185 by October. That's 25 lb in 11 weeks — about 1.1% of
> your bodyweight per week, and past roughly 1% you start giving back muscle along with
> the fat. At a rate that holds onto muscle you'd be looking at mid-December. Want to run
> it that way, or would you rather shorten the target?"

Negotiate to something safe before you write anything.

## Step 5 — Training

- Experience: beginner, intermediate, or advanced. Ask how long they've trained
  consistently rather than making them self-rate.
- Days per week they'll realistically train. Take the realistic number, not the
  aspirational one — press once if the answer sounds like a wish.
- Minutes per session.
- **Equipment.** Free-form, then normalize to a list. Ask what they actually have access
  to: home gear, full gym, bodyweight only. Get specifics on loads — "dumbbells" and
  "dumbbells up to 25 lb" produce very different programs.
- Anything they love doing, and anything they'll quit over.
- Cardio options and constraints — bad knees, no treadmill, allergies, whatever.
- Injuries or movements to avoid. **This is a hard constraint in every plan.** Get it
  specific: which joint, which movements, still symptomatic or historical.

## Step 6 — Nutrition

- Approach or restrictions (vegetarian, allergies, religious, low-carb by preference).
- Do they log food? In what?

If they don't log food, say plainly what that means: Baseline will coach training, sleep,
steps, and behavior, and estimate their maintenance calories from weight trend, but it
can't coach macros it can't see. Offer the option of starting. Don't nag.

## Step 7 — Lifestyle

Typical sleep window, how active their job is, current stress level. These feed the
activity factor and the recovery read.

## Step 8 — Data

Explain the two paths — this is where most setups go wrong.

**Health Auto Export, for daily use.** Point them to the app. Give them the metric list
and be explicit that HRV and resting heart rate must be enabled, because they're off in
some configurations and their absence is silent:

`weight_body_mass` · `body_fat_percentage` · `lean_body_mass` ·
**`heart_rate_variability`** · **`resting_heart_rate`** · `sleep_analysis` ·
`step_count` · `active_energy` · `basal_energy_burned` · `apple_exercise_time` ·
`dietary_energy` · `protein` · `carbohydrates` · `total_fat` · `fiber`

Have them point its output at `health/data/inbox/`.

**Stock export, once, for history.** iPhone → Health → their photo, top right → Export
All Health Data → drop the `export.zip` in `health/data/inbox/`.

Push for this one. Explain the reason honestly: Baseline won't give real advice on under
two weeks of data, so without a backfill their first useful review is two weeks out.
With it, they get one today, measured against months of their own history.

**Sell the daily habit.** The import takes ten seconds and weekly would technically be
enough — but the point isn't the sync, it's staying in contact with the numbers. Data
someone syncs monthly is data they've already stopped acting on.

## Step 9 — Compute targets

Show your work, then get confirmation before writing.

**RMR** — Mifflin-St Jeor:
- men: `10 × kg + 6.25 × cm − 5 × age + 5`
- women: `10 × kg + 6.25 × cm − 5 × age − 161`

**TDEE estimate** — RMR × activity factor (1.2 sedentary, 1.375 light, 1.55 moderate,
1.725 heavy). Label it an estimate out loud. It gets replaced by the observed figure once
`trend_report.py` has ~21 days of intake and weight to work from, and the observed number
is frequently 200–300 kcal off the estimate in either direction.

**Calorie target** — apply the deficit or surplus for the negotiated rate (a pound of fat
is roughly 3,500 kcal; a kilo roughly 7,700). Then clamp to the floors: never below
1,500 (men) / 1,200 (women), and never below RMR. If clamping changes the number, say so
and re-state the honest timeline.

**Protein** — 1.6–2.2 g/kg, toward the top of that range in a deficit
(Morton 2018, Jäger 2017, Helms 2014).

**Steps and sleep floors** — from their current baseline, not an aspiration. If they walk
5,000 a day, the floor is 7,000, not 12,000.

Present all of it with the reasoning, ask for a yes, and adjust if they push back —
except on the safety floors, which don't move.

## Step 10 — Write the files

`health/profile.md`:

```markdown
# Profile

Written by /coach-setup on YYYY-MM-DD. Edit freely — every skill reads this.

Disclaimer acknowledged: YYYY-MM-DD

## About
Age · sex · height · starting weight · units

## Goal
Primary goal, target, negotiated rate, timeline

## Training
Experience · days/week · minutes/session · equipment · likes · dislikes · cardio options

## Constraints
Injuries, conditions, movements to avoid. Hard limits on every plan.

## Nutrition
Approach, restrictions, whether they log food and where

## Recovery
Sleep window, job activity, stress

## Data
Which export paths are set up

## Notes
Free space. Anything Claude should know. Nothing reads this but everything sees it.
```

`health/targets.json`:

```json
{
  "units": "lb",
  "calorie_target": 2100,
  "calorie_band": [1950, 2250],
  "protein_floor_g": 150,
  "step_floor": 8000,
  "sleep_floor_hrs": 7,
  "weight_change_target_pct_bw_per_wk": -0.7,
  "training_days": 4,
  "mode": "standard",
  "medications_affecting_hr": false,
  "derived": { "rmr": 1780, "tdee_est": 2650, "tdee_observed": null },
  "safety": {
    "min_calories": 1500,
    "max_loss_rate_pct_bw_wk": 1.0,
    "min_bodyfat_target_pct": 8
  }
}
```

`mode` is `"standard"` or `"habit_only"`. In habit-only mode omit `calorie_target`,
`calorie_band`, and `weight_change_target_pct_bw_per_wk` entirely — absent beats zeroed.

## Step 11 — Verify and hand off

Run the parser self-test and report the actual result:

```bash
python3 scripts/apple_health_parse.py --selftest
```

Then tell them exactly what happens next: drop the export in `health/data/inbox/`, run
`/coach-import`, then `/coach-review`.

If they've already got an export sitting in the inbox, offer to run the import now.

## Failure modes

- **They won't acknowledge the disclaimer** → stop. Don't proceed with a hedge.
- **Under-18** → decline, refer, stop. No consolation feature.
- **They insist on an unsafe target** → hold the floor. Explain once more, offer the safe
  version, and write the safe one. They can hand-edit `targets.json` if they're
  determined; that's their call, not yours.
- **They want to skip everything** → the minimum viable profile is disclaimer + health
  screen + units + goal. Write that, mark the rest `unknown`, and let the other skills
  ask as they go.
