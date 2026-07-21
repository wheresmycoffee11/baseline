#!/usr/bin/env python3
"""
Baseline — trend report.

Every number the coach is permitted to cite comes from here. Nothing in this pack does
arithmetic on health data by hand, because a language model doing mental math on someone's
bodyweight is exactly the failure this design exists to prevent.

Usage:
    python3 trend_report.py [--data health/data/daily.csv]
                            [--targets health/targets.json]
                            [--asof YYYY-MM-DD] [--pretty]

Emits a single JSON object on stdout.

Standard library only. Python 3.9+.
"""

import argparse
import csv
import json
import os
import sys
from datetime import datetime, timedelta

KCAL_PER_LB = 3500.0
KCAL_PER_KG = 7700.0

# Windows, in days, that everything is reported over. A coach citing "recently" is
# useless; a coach citing "over the last 14 days" can be checked.
WINDOWS = (7, 14, 28)

NUMERIC = {
    "weight", "body_fat_pct", "lean_mass", "bmi", "rhr", "hrv",
    "sleep_hrs", "sleep_deep", "sleep_rem", "sleep_core",
    "calories_in", "protein_g", "carbs_g", "fat_g", "fiber_g",
    "active_kcal", "basal_kcal", "exercise_min", "steps", "vo2max",
}


# --------------------------------------------------------------------------------------
# Small stats helpers
# --------------------------------------------------------------------------------------

def mean(values):
    return sum(values) / len(values) if values else None


def rounded(value, digits=1):
    return None if value is None else round(value, digits)


def ols_slope(points):
    """Least-squares slope over (x_days, y) pairs. Units of y per day.

    A regression over every reading beats differencing two endpoints: one bad weigh-in
    can't swing it, and it uses the whole window instead of two days of it.
    """
    n = len(points)
    if n < 3:
        return None
    mean_x = sum(x for x, _ in points) / n
    mean_y = sum(y for _, y in points) / n
    numerator = sum((x - mean_x) * (y - mean_y) for x, y in points)
    denominator = sum((x - mean_x) ** 2 for x, _ in points)
    return numerator / denominator if denominator else None


# --------------------------------------------------------------------------------------
# Loading
# --------------------------------------------------------------------------------------

def load_rows(path):
    if not os.path.exists(path):
        raise SystemExit(json.dumps({
            "error": "no_data_file",
            "message": f"{path} not found. Run /coach-import first.",
        }))

    rows = []
    with open(path, "r", encoding="utf-8", newline="") as handle:
        for raw in csv.DictReader(handle):
            date = (raw.get("date") or "").strip()
            if not date:
                continue
            row = {"date": date}
            for key, value in raw.items():
                if key in NUMERIC and value not in (None, ""):
                    try:
                        row[key] = float(value)
                    except ValueError:
                        pass
            rows.append(row)
    rows.sort(key=lambda r: r["date"])
    return rows


def load_targets(path):
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except (json.JSONDecodeError, OSError):
        return {}


def window_rows(rows, asof, days):
    cutoff = (asof - timedelta(days=days - 1)).strftime("%Y-%m-%d")
    stamp = asof.strftime("%Y-%m-%d")
    return [r for r in rows if cutoff <= r["date"] <= stamp]


def series(rows, column):
    return [r[column] for r in rows if column in r]


# --------------------------------------------------------------------------------------
# Sections
# --------------------------------------------------------------------------------------

def weight_section(rows, asof, units):
    out = {"units": units, "windows": {}}
    kcal_per_unit = KCAL_PER_LB if units == "lb" else KCAL_PER_KG

    for days in WINDOWS:
        subset = window_rows(rows, asof, days)
        weights = series(subset, "weight")
        entry = {"readings": len(weights), "mean": rounded(mean(weights), 2)}

        if len(weights) >= 3:
            origin = datetime.strptime(subset[0]["date"], "%Y-%m-%d")
            points = [
                ((datetime.strptime(r["date"], "%Y-%m-%d") - origin).days, r["weight"])
                for r in subset if "weight" in r
            ]
            slope = ols_slope(points)
            if slope is not None:
                per_week = slope * 7
                entry["change_per_week"] = rounded(per_week, 2)
                avg = mean(weights)
                if avg:
                    entry["pct_bw_per_week"] = rounded(per_week / avg * 100, 2)
        out["windows"][f"{days}d"] = entry

    # Current = the 7-day rolling average, never the latest reading. Daily scale movement
    # is water and gut contents; treating it as signal is the most common self-coaching
    # error there is.
    recent = series(window_rows(rows, asof, 7), "weight")
    prior = series(
        [r for r in rows
         if (asof - timedelta(days=13)).strftime("%Y-%m-%d") <= r["date"]
         <= (asof - timedelta(days=7)).strftime("%Y-%m-%d")],
        "weight",
    )
    out["current_7d_avg"] = rounded(mean(recent), 2)
    out["prior_7d_avg"] = rounded(mean(prior), 2)
    if out["current_7d_avg"] is not None and out["prior_7d_avg"] is not None:
        delta = out["current_7d_avg"] - out["prior_7d_avg"]
        out["week_over_week_change"] = rounded(delta, 2)
        if out["prior_7d_avg"]:
            out["week_over_week_pct_bw"] = rounded(delta / out["prior_7d_avg"] * 100, 2)

    all_weights = series(rows, "weight")
    if all_weights:
        out["first_recorded"] = rounded(all_weights[0], 2)
        out["latest_reading"] = rounded(all_weights[-1], 2)
        out["total_change"] = rounded(all_weights[-1] - all_weights[0], 2)
    out["kcal_per_unit"] = kcal_per_unit
    return out


def intake_section(rows, asof, targets):
    band = targets.get("calorie_band")
    protein_floor = targets.get("protein_floor_g")
    out = {"windows": {}, "calorie_band": band, "protein_floor_g": protein_floor}

    for days in WINDOWS:
        subset = window_rows(rows, asof, days)
        entry = {"days_in_window": len(subset)}
        for column, label in (("calories_in", "calories"), ("protein_g", "protein"),
                              ("carbs_g", "carbs"), ("fat_g", "fat"), ("fiber_g", "fiber")):
            values = series(subset, column)
            entry[f"{label}_mean"] = rounded(mean(values), 1)
            entry[f"{label}_logged_days"] = len(values)
        out["windows"][f"{days}d"] = entry

    # Adherence over 14 days: long enough to be meaningful, short enough to be current.
    subset = window_rows(rows, asof, 14)
    calories = series(subset, "calories_in")
    proteins = series(subset, "protein_g")

    adherence = {"window_days": 14, "logged_days": len(calories)}
    if calories and band and len(band) == 2:
        in_band = sum(1 for c in calories if band[0] <= c <= band[1])
        adherence["calorie_days_in_band"] = in_band
        adherence["calorie_adherence_pct"] = rounded(in_band / len(calories) * 100, 0)
    if proteins and protein_floor:
        hits = sum(1 for p in proteins if p >= protein_floor)
        adherence["protein_days_at_floor"] = hits
        adherence["protein_adherence_pct"] = rounded(hits / len(proteins) * 100, 0)

    step_floor = targets.get("step_floor")
    steps = series(subset, "steps")
    if steps and step_floor:
        hits = sum(1 for s in steps if s >= step_floor)
        adherence["step_days_at_floor"] = hits
        adherence["step_adherence_pct"] = rounded(hits / len(steps) * 100, 0)

    out["adherence"] = adherence
    return out


def energy_section(rows, asof, targets, units):
    """Back-calculate what this person actually burns.

    Prediction equations are a starting guess and routinely miss by a couple hundred
    calories. Observed intake measured against observed weight change is the real number,
    and it needs about three weeks before it means anything.
    """
    out = {
        "rmr_estimate": (targets.get("derived") or {}).get("rmr"),
        "tdee_estimate": (targets.get("derived") or {}).get("tdee_est"),
        "tdee_observed": None,
        "observed_basis_days": 0,
        "confidence": "none",
    }

    subset = window_rows(rows, asof, 28)
    calories = series(subset, "calories_in")
    weights = [(r["date"], r["weight"]) for r in subset if "weight" in r]

    if len(calories) >= 14 and len(weights) >= 10:
        origin = datetime.strptime(weights[0][0], "%Y-%m-%d")
        points = [((datetime.strptime(d, "%Y-%m-%d") - origin).days, w) for d, w in weights]
        slope = ols_slope(points)  # units per day
        if slope is not None:
            kcal_per_unit = KCAL_PER_LB if units == "lb" else KCAL_PER_KG
            out["tdee_observed"] = int(round(mean(calories) - slope * kcal_per_unit))
            out["observed_basis_days"] = len(calories)
            out["confidence"] = "good" if len(calories) >= 21 else "provisional"
            out["note"] = (
                "Back-calculated from logged intake and measured weight change. Only as "
                "good as the food logging behind it."
            )
    else:
        out["note"] = (
            f"Needs 14+ logged intake days and 10+ weigh-ins in a 28-day window; "
            f"have {len(calories)} and {len(weights)}."
        )

    subset7 = window_rows(rows, asof, 7)
    for column, key in (("active_kcal", "active_kcal_7d_mean"),
                        ("basal_kcal", "basal_kcal_7d_mean")):
        out[key] = rounded(mean(series(subset7, column)), 0)
    return out


def recovery_section(rows, asof, targets):
    """HRV and resting heart rate, always against the person's own 28-day baseline.

    Population norms are meaningless here. An HRV of 45 is unremarkable next to a
    stranger's 90 and alarming next to your own 70.
    """
    out = {"hrv": {}, "rhr": {}, "sleep": {}}
    blocked = bool(targets.get("medications_affecting_hr"))

    for column, key in (("hrv", "hrv"), ("rhr", "rhr")):
        recent = series(window_rows(rows, asof, 7), column)
        baseline = series(window_rows(rows, asof, 28), column)
        section = {
            "readings_7d": len(recent),
            "readings_28d": len(baseline),
            "mean_7d": rounded(mean(recent), 1),
            "baseline_28d": rounded(mean(baseline), 1),
        }
        if section["mean_7d"] is not None and section["baseline_28d"]:
            delta = section["mean_7d"] - section["baseline_28d"]
            section["delta"] = rounded(delta, 1)
            section["pct_of_baseline"] = rounded(
                section["mean_7d"] / section["baseline_28d"] * 100, 1)
        if blocked:
            section["valid"] = False
            section["note"] = (
                "Medication affecting heart rate is flagged in the profile. HRV and "
                "resting heart rate are not usable recovery signals here."
            )
        elif len(baseline) < 14:
            section["valid"] = False
            section["note"] = f"Only {len(baseline)} readings in 28 days — no stable baseline yet."
        elif len(recent) < 3:
            # Per reference/recovery-principles.md: day-to-day HRV varies enormously
            # within a person (mean within-subject CV ~0.37, Sensors 2025), so one or two
            # readings cannot establish a weekly average. Treating them as one is how a
            # tool ends up prescribing a deload off a single bad night.
            section["valid"] = False
            section["note"] = (
                f"Only {len(recent)} reading(s) in the last 7 days — need 3+ before a "
                "weekly average means anything."
            )
        else:
            section["valid"] = True
        out[key] = section

    floor = targets.get("sleep_floor_hrs", 7)
    for days in (7, 28):
        values = series(window_rows(rows, asof, days), "sleep_hrs")
        out["sleep"][f"mean_{days}d"] = rounded(mean(values), 2)
        out["sleep"][f"nights_{days}d"] = len(values)
    week = series(window_rows(rows, asof, 7), "sleep_hrs")
    out["sleep"]["floor_hrs"] = floor
    out["sleep"]["nights_below_floor_7d"] = sum(1 for v in week if v < floor)
    out["sleep"]["nights_under_6h_7d"] = sum(1 for v in week if v < 6)
    return out


def training_section(rows, asof, targets):
    out = {"windows": {}}
    for days in WINDOWS:
        subset = window_rows(rows, asof, days)
        steps = series(subset, "steps")
        minutes = series(subset, "exercise_min")
        active = series(subset, "active_kcal")
        out["windows"][f"{days}d"] = {
            "steps_mean": rounded(mean(steps), 0),
            "steps_days": len(steps),
            "exercise_min_mean": rounded(mean(minutes), 0),
            "exercise_min_total": rounded(sum(minutes), 0) if minutes else None,
            "active_kcal_mean": rounded(mean(active), 0),
        }
    out["step_floor"] = targets.get("step_floor")
    out["training_days_target"] = targets.get("training_days")
    return out


def coverage_section(rows, asof):
    out = {"total_days_on_record": len(rows)}
    if rows:
        out["first_date"] = rows[0]["date"]
        out["last_date"] = rows[-1]["date"]
        gap = (asof - datetime.strptime(rows[-1]["date"], "%Y-%m-%d")).days
        out["days_since_last_entry"] = gap
        out["data_is_stale"] = gap > 3

    for days in WINDOWS:
        subset = window_rows(rows, asof, days)
        out[f"last_{days}d"] = {
            "days_with_any_data": len(subset),
            "weigh_ins": len(series(subset, "weight")),
            "intake_logged": len(series(subset, "calories_in")),
            "sleep_nights": len(series(subset, "sleep_hrs")),
            "hrv_readings": len(series(subset, "hrv")),
            "rhr_readings": len(series(subset, "rhr")),
        }

    fortnight = out.get("last_14d", {})
    out["sufficient_for_weight_verdict"] = fortnight.get("weigh_ins", 0) >= 10
    out["sufficient_for_intake_verdict"] = fortnight.get("intake_logged", 0) >= 10
    out["food_logging_active"] = fortnight.get("intake_logged", 0) >= 4
    return out


def flags_section(weight, recovery, intake, coverage, targets):
    """Precomputed safety-relevant conditions.

    These exist so a red flag can't be missed by a model skimming the numbers. The
    framework still has to be read; this just makes the dangerous cases loud.
    """
    flags = []
    safety = targets.get("safety") or {}

    pct = weight.get("week_over_week_pct_bw")
    max_rate = safety.get("max_loss_rate_pct_bw_wk", 1.0)
    if pct is not None:
        if pct <= -2.0:
            flags.append({
                "id": "rapid_weight_loss", "severity": "red",
                "detail": f"Down {abs(pct)}% of bodyweight week over week. Above 2% warrants "
                          "a clinician, not a program change.",
            })
        elif pct < -max_rate:
            flags.append({
                "id": "loss_too_fast", "severity": "amber",
                "detail": f"Losing {abs(pct)}% of bodyweight per week, above the "
                          f"{max_rate}% cap.",
            })

    rhr = recovery.get("rhr", {})
    if rhr.get("valid") and rhr.get("delta") is not None:
        if rhr["delta"] >= 15 or (rhr.get("mean_7d") or 0) > 100:
            flags.append({
                "id": "rhr_elevated_severe", "severity": "red",
                "detail": f"Resting heart rate {rhr['delta']:+} bpm vs baseline. Outside "
                          "what training stress explains.",
            })
        elif rhr["delta"] >= 5:
            flags.append({
                "id": "rhr_elevated", "severity": "amber",
                "detail": f"Resting heart rate {rhr['delta']:+} bpm vs 28-day baseline.",
            })

    hrv = recovery.get("hrv", {})
    if hrv.get("valid") and hrv.get("pct_of_baseline") is not None:
        if hrv["pct_of_baseline"] <= 90:
            flags.append({
                "id": "hrv_suppressed", "severity": "amber",
                "detail": f"HRV at {hrv['pct_of_baseline']}% of the 28-day baseline.",
            })

    sleep = recovery.get("sleep", {})
    if (sleep.get("mean_7d") or 99) < 6:
        flags.append({
            "id": "sleep_deficient", "severity": "amber",
            "detail": f"Averaging {sleep['mean_7d']}h over 7 nights.",
        })

    band = intake.get("calorie_band")
    floor = safety.get("min_calories")
    week = intake.get("windows", {}).get("7d", {})
    if floor and week.get("calories_mean") and week["calories_logged_days"] >= 4:
        if week["calories_mean"] < floor:
            flags.append({
                "id": "intake_below_floor", "severity": "red",
                "detail": f"Averaging {week['calories_mean']} kcal, below the {floor} floor.",
            })

    if coverage.get("data_is_stale"):
        flags.append({
            "id": "stale_data", "severity": "info",
            "detail": f"No data for {coverage['days_since_last_entry']} days.",
        })

    return flags


# --------------------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------------------

def build(rows, targets, asof):
    units = targets.get("units", "lb")
    mode = targets.get("mode", "standard")

    coverage = coverage_section(rows, asof)
    weight = weight_section(rows, asof, units)
    intake = intake_section(rows, asof, targets)
    energy = energy_section(rows, asof, targets, units)
    recovery = recovery_section(rows, asof, targets)
    training = training_section(rows, asof, targets)
    flags = flags_section(weight, recovery, intake, coverage, targets)

    report = {
        "generated_for": asof.strftime("%Y-%m-%d"),
        "units": units,
        "mode": mode,
        "coverage": coverage,
        "weight": weight,
        "intake": intake,
        "energy": energy,
        "recovery": recovery,
        "training": training,
        "flags": flags,
    }

    if mode == "habit_only":
        # Enforced here rather than left to the prompt. If the numbers aren't in the
        # payload, no amount of drift can put weight-loss coaching back in front of
        # someone who told us they have a history of disordered eating.
        report["weight"] = {
            "suppressed": True,
            "reason": "habit_only mode — weight trend and calorie verdicts are withheld.",
        }
        report["intake"] = {
            "suppressed": True,
            "reason": "habit_only mode — calorie targets and adherence are withheld.",
            "protein_floor_g": targets.get("protein_floor_g"),
            "windows": {"7d": {"protein_mean":
                               intake["windows"]["7d"].get("protein_mean")}},
        }
        report["energy"] = {"suppressed": True, "reason": "habit_only mode."}
        report["flags"] = [f for f in flags if f["id"] not in
                           ("loss_too_fast", "intake_below_floor")]

    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description="Compute Baseline's trend report.")
    parser.add_argument("--data", default="health/data/daily.csv")
    parser.add_argument("--targets", default="health/targets.json")
    parser.add_argument("--asof", help="YYYY-MM-DD; defaults to the last day on record")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args(argv)

    rows = load_rows(args.data)
    if not rows:
        print(json.dumps({
            "error": "no_rows",
            "message": f"{args.data} has no dated rows yet. Run /coach-import.",
        }))
        return 2

    targets = load_targets(args.targets)

    if args.asof:
        try:
            asof = datetime.strptime(args.asof, "%Y-%m-%d")
        except ValueError:
            print(json.dumps({"error": "bad_asof", "message": "--asof must be YYYY-MM-DD"}))
            return 1
    else:
        asof = datetime.strptime(rows[-1]["date"], "%Y-%m-%d")

    report = build(rows, targets, asof)
    print(json.dumps(report, indent=2 if args.pretty else None, sort_keys=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
