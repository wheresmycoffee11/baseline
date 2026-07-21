#!/usr/bin/env python3
"""
Baseline — synthetic sample data generator.

Builds the fake 6-week dataset in sample-data/. It exists so people can see what
Baseline does before trusting it with their own numbers, and so the gold examples have a
fixed case to be graded against.

The scenario is deliberately chosen. Someone in a fat-loss phase:

  Weeks 1-2  good adherence, losing about 0.8 lb/week. Working.
  Weeks 3-4  weekends slip badly. Weekly average intake climbs, weight goes flat.
  Weeks 5-6  a rough patch of sleep and suppressed HRV, adherence still leaky.

The naive read of a stall is "cut calories." Here that would be wrong — intake has drifted
above target and sleep has fallen apart, so the correct answer is to fix adherence and
recovery first. Any coach worth trusting has to reach that conclusion, which is exactly
what the gold example grades.

Seeded, so it regenerates identically. Standard library only.

Usage:
    python3 scripts/make_sample_data.py [--out sample-data/daily.csv]
"""

import argparse
import csv
import os
import random
from datetime import datetime, timedelta

START = datetime(2026, 5, 20)
DAYS = 42
SEED = 20260520

COLUMNS = [
    "date", "weight", "body_fat_pct", "lean_mass", "bmi", "rhr", "hrv",
    "sleep_hrs", "sleep_deep", "sleep_rem", "sleep_core",
    "calories_in", "protein_g", "carbs_g", "fat_g", "fiber_g",
    "active_kcal", "basal_kcal", "exercise_min", "steps", "vo2max", "entry_source",
]

TARGETS = {
    "units": "lb",
    "calorie_target": 2100,
    "calorie_band": [1950, 2250],
    "protein_floor_g": 150,
    "step_floor": 8000,
    "sleep_floor_hrs": 7,
    "weight_change_target_pct_bw_per_wk": -0.5,
    "training_days": 4,
    "mode": "standard",
    "medications_affecting_hr": False,
    "derived": {"rmr": 1815, "tdee_est": 2650, "tdee_observed": None},
    "safety": {"min_calories": 1500, "max_loss_rate_pct_bw_wk": 1.0,
               "min_bodyfat_target_pct": 8},
}

PROFILE = """# Profile — sample

This is fabricated data for demonstration. Nobody's real numbers are in here.

Disclaimer acknowledged: 2026-05-20

## About
41, male, 5'11" (180 cm), started at 205 lb. Units: lb.

## Goal
Fat loss. Target 185 lb, no hard deadline. Negotiated rate: about 0.5% of bodyweight
per week, roughly 1 lb.

## Training
Intermediate — lifting on and off for eight years. Four days a week, 45 minutes.
Equipment: adjustable dumbbells to 50 lb, a bench, a pull-up bar, one 35 lb kettlebell.
Likes lifting, tolerates walking, will quit over burpees. Cardio: outdoor walking only.

## Constraints
Left shoulder is cranky overhead — no barbell press, no overhead work at load.

## Nutrition
No restrictions. Logs food in MyFitnessPal most weekdays, worse on weekends.

## Recovery
In bed around 11pm, up at 6am. Desk job. Stress moderate, higher near month end.

## Data
Health Auto Export daily. Stock export backfilled at setup.

## Notes
Travels for work roughly one week a month, which is when things fall apart.
"""


def build_day(index, rng):
    """One day. Phase-dependent, with enough noise to look like a real person."""
    date = START + timedelta(days=index)
    week = index // 7
    weekend = date.weekday() >= 5

    # --- intake -----------------------------------------------------------------------
    # Weeks 0-1 adherent. From week 2 the weekends come apart, which is the whole point
    # of the scenario: the target never changed, the behavior did.
    if week <= 1:
        calories = rng.gauss(2080, 110) if not weekend else rng.gauss(2210, 160)
        protein = rng.gauss(158, 14)
    elif week <= 3:
        calories = rng.gauss(2150, 130) if not weekend else rng.gauss(2850, 320)
        protein = rng.gauss(148, 20)
    else:
        calories = rng.gauss(2120, 140) if not weekend else rng.gauss(2650, 280)
        protein = rng.gauss(143, 22)

    # Weekend logging is patchy — the days people most want to forget are the days they
    # least often log. Absent rows are part of what a coach has to reason about.
    logged = not (weekend and rng.random() < 0.45)

    # --- weight -----------------------------------------------------------------------
    # A smooth trend plus daily noise. The noise is the point: any single reading here is
    # nearly meaningless, which is what the rolling average exists to solve.
    if index <= 13:
        trend = 205.0 - 0.115 * index
    elif index <= 27:
        trend = 205.0 - 0.115 * 13 - 0.012 * (index - 13)      # the stall
    else:
        trend = 205.0 - 0.115 * 13 - 0.012 * 14 - 0.055 * (index - 27)
    weight = trend + rng.gauss(0, 0.62)

    # --- recovery ---------------------------------------------------------------------
    # A bad stretch in week 4: short sleep, HRV down, resting heart rate up. Real
    # under-recovery shows up on several signals at once, not one.
    rough = 28 <= index <= 34
    if rough:
        sleep = rng.gauss(5.7, 0.5)
        hrv = rng.gauss(48, 5)
        rhr = rng.gauss(62, 2.2)
    else:
        sleep = rng.gauss(7.1, 0.65)
        hrv = rng.gauss(62, 7)
        rhr = rng.gauss(56, 2.0)
    sleep = max(4.0, sleep)

    deep = sleep * rng.uniform(0.15, 0.22)
    rem = sleep * rng.uniform(0.18, 0.25)
    core = sleep - deep - rem

    # --- activity ---------------------------------------------------------------------
    trained = date.weekday() in (0, 1, 3, 4) and rng.random() > 0.12
    steps = rng.gauss(9200 if not weekend else 7100, 1900)
    if rough:
        steps *= 0.82
    exercise = rng.gauss(52, 9) if trained else rng.gauss(14, 7)
    active = rng.gauss(620, 90) if trained else rng.gauss(330, 70)

    row = {
        "date": date.strftime("%Y-%m-%d"),
        "weight": round(weight, 2),
        "body_fat_pct": round(22.4 - 0.035 * index + rng.gauss(0, 0.18), 1),
        "lean_mass": round(weight * (1 - (22.4 - 0.035 * index) / 100), 2),
        "bmi": round(weight / (70.87 ** 2) * 703, 1),
        "rhr": int(round(rhr)),
        "hrv": round(hrv, 1),
        "sleep_hrs": round(sleep, 2),
        "sleep_deep": round(deep, 2),
        "sleep_rem": round(rem, 2),
        "sleep_core": round(core, 2),
        "active_kcal": int(round(max(120, active))),
        "basal_kcal": int(round(rng.gauss(1830, 45))),
        "exercise_min": int(round(max(0, exercise))),
        "steps": int(round(max(1200, steps))),
        "entry_source": "apple_health",
    }

    if logged:
        row["calories_in"] = int(round(max(900, calories)))
        row["protein_g"] = round(max(50, protein), 1)
        row["carbs_g"] = round(max(40, calories * rng.uniform(0.30, 0.42) / 4), 1)
        row["fat_g"] = round(max(25, calories * rng.uniform(0.27, 0.36) / 9), 1)
        row["fiber_g"] = round(rng.gauss(21, 6), 1)

    return row


def main():
    parser = argparse.ArgumentParser(description="Generate Baseline's sample dataset.")
    parser.add_argument("--out", default="sample-data/daily.csv")
    args = parser.parse_args()

    rng = random.Random(SEED)
    rows = [build_day(i, rng) for i in range(DAYS)]

    out_dir = os.path.dirname(args.out)
    os.makedirs(out_dir, exist_ok=True)

    with open(args.out, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    import json
    with open(os.path.join(out_dir, "targets.json"), "w", encoding="utf-8") as handle:
        json.dump(TARGETS, handle, indent=2)
    with open(os.path.join(out_dir, "profile.md"), "w", encoding="utf-8") as handle:
        handle.write(PROFILE)

    logged = sum(1 for r in rows if "calories_in" in r)
    print(f"Wrote {len(rows)} days to {args.out} ({logged} with food logged)")
    print(f"Range: {rows[0]['date']} to {rows[-1]['date']}")
    print(f"Weight: {rows[0]['weight']} -> {rows[-1]['weight']}")


if __name__ == "__main__":
    main()
