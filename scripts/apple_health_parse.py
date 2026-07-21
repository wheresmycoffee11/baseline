#!/usr/bin/env python3
"""
Baseline — Apple Health parser.

Reduces any Apple Health export into one tidy row per day.

Handles both export shapes:

  1. Health Auto Export (the app)  — per-day JSON. Small, incremental, the daily driver.
  2. Stock iOS "Export All Health Data" — export.zip / export.xml. Often 500MB+, so it
     is streamed with iterparse and never loaded into memory. Used once, to backfill
     history.

Usage:
    python3 apple_health_parse.py <path> [options]

    <path> may be:
      export.zip                 stock export (XML is streamed straight out of the zip)
      export.xml                 stock export, already unzipped
      HealthAutoExport-*.json    a single Auto Export file
      a directory                scanned for either shape

Options:
    --out PATH        CSV to upsert into        (default: health/data/daily.csv)
    --units lb|kg     mass units for output     (default: lb)
    --since DATE      ignore records before YYYY-MM-DD
    --selftest        parse a built-in fixture and verify; exit 0 if healthy
    --quiet           suppress the human-readable report (JSON summary still prints)

Exit codes:
    0  success
    1  unreadable or unrecognized input
    2  input parsed but contained zero usable records

Standard library only. Python 3.9+.
"""

import argparse
import csv
import io
import json
import os
import sys
import tempfile
import zipfile
from collections import defaultdict
from datetime import datetime, timedelta
from xml.etree import ElementTree

# --------------------------------------------------------------------------------------
# Schema
# --------------------------------------------------------------------------------------

COLUMNS = [
    "date",
    "weight", "body_fat_pct", "lean_mass", "bmi",
    "rhr", "hrv",
    "sleep_hrs", "sleep_deep", "sleep_rem", "sleep_core",
    "calories_in", "protein_g", "carbs_g", "fat_g", "fiber_g",
    "active_kcal", "basal_kcal", "exercise_min", "steps", "vo2max",
    "entry_source",
]

# How each metric collapses to a single daily value.
#   sum_sources   sum every source (nutrition — food apps don't overlap)
#   sum_max_src   sum per source, keep the largest (steps/energy — phone+watch double-count)
#   first         earliest reading of the day (morning weigh-in convention)
#   mean          average of the day's readings
#   last          most recent reading of the day
AGGREGATION = {
    "steps": "sum_max_src", "active_kcal": "sum_max_src",
    "basal_kcal": "sum_max_src", "exercise_min": "sum_max_src",
    "calories_in": "sum_sources", "protein_g": "sum_sources",
    "carbs_g": "sum_sources", "fat_g": "sum_sources", "fiber_g": "sum_sources",
    "weight": "first", "body_fat_pct": "first", "lean_mass": "first", "bmi": "first",
    "hrv": "mean",
    "rhr": "last", "vo2max": "last",
}

# Health Auto Export JSON metric names -> our columns
HAE_MAP = {
    "weight_body_mass": "weight",
    "body_fat_percentage": "body_fat_pct",
    "lean_body_mass": "lean_mass",
    "body_mass_index": "bmi",
    "resting_heart_rate": "rhr",
    "heart_rate_variability": "hrv",
    "dietary_energy": "calories_in",
    "protein": "protein_g",
    "carbohydrates": "carbs_g",
    "total_fat": "fat_g",
    "fiber": "fiber_g",
    "active_energy": "active_kcal",
    "basal_energy_burned": "basal_kcal",
    "apple_exercise_time": "exercise_min",
    "step_count": "steps",
    "vo2_max": "vo2max",
}

# Stock export.xml HealthKit type identifiers -> our columns
HK_MAP = {
    "HKQuantityTypeIdentifierBodyMass": "weight",
    "HKQuantityTypeIdentifierBodyFatPercentage": "body_fat_pct",
    "HKQuantityTypeIdentifierLeanBodyMass": "lean_mass",
    "HKQuantityTypeIdentifierBodyMassIndex": "bmi",
    "HKQuantityTypeIdentifierRestingHeartRate": "rhr",
    "HKQuantityTypeIdentifierHeartRateVariabilitySDNN": "hrv",
    "HKQuantityTypeIdentifierDietaryEnergyConsumed": "calories_in",
    "HKQuantityTypeIdentifierDietaryProtein": "protein_g",
    "HKQuantityTypeIdentifierDietaryCarbohydrates": "carbs_g",
    "HKQuantityTypeIdentifierDietaryFatTotal": "fat_g",
    "HKQuantityTypeIdentifierDietaryFiber": "fiber_g",
    "HKQuantityTypeIdentifierActiveEnergyBurned": "active_kcal",
    "HKQuantityTypeIdentifierBasalEnergyBurned": "basal_kcal",
    "HKQuantityTypeIdentifierAppleExerciseTime": "exercise_min",
    "HKQuantityTypeIdentifierStepCount": "steps",
    "HKQuantityTypeIdentifierVO2Max": "vo2max",
}

SLEEP_TYPE = "HKCategoryTypeIdentifierSleepAnalysis"

# Sleep stage values -> which bucket they feed. "InBed" and "Awake" are not sleep.
SLEEP_STAGES = {
    "HKCategoryValueSleepAnalysisAsleepDeep": "sleep_deep",
    "HKCategoryValueSleepAnalysisAsleepREM": "sleep_rem",
    "HKCategoryValueSleepAnalysisAsleepCore": "sleep_core",
    "HKCategoryValueSleepAnalysisAsleepUnspecified": "sleep_core",
    "HKCategoryValueSleepAnalysisAsleep": "sleep_core",
}

KG_PER_LB = 0.45359237
ROUND = {
    "weight": 2, "body_fat_pct": 1, "lean_mass": 2, "bmi": 1,
    "rhr": 0, "hrv": 1, "vo2max": 1,
    "sleep_hrs": 2, "sleep_deep": 2, "sleep_rem": 2, "sleep_core": 2,
    "calories_in": 0, "protein_g": 1, "carbs_g": 1, "fat_g": 1, "fiber_g": 1,
    "active_kcal": 0, "basal_kcal": 0, "exercise_min": 0, "steps": 0,
}


class ParseError(Exception):
    """Input could not be read or understood."""


# --------------------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------------------

def parse_ts(value):
    """Apple writes '2026-07-15 06:30:00 -0400' in both export shapes.

    The offset is the device's local time, which is what we want: a day boundary should
    mean midnight where the user was standing, not midnight UTC. Returns a
    timezone-aware datetime, or None if unparseable.
    """
    if not value:
        return None
    text = value.strip()
    for fmt in ("%Y-%m-%d %H:%M:%S %z", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    try:  # ISO-8601 fallback, in case a future export version switches format
        return datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None


def convert_mass(value, source_unit, target_unit):
    """Normalize a mass to the user's chosen unit."""
    src = (source_unit or "").lower()
    if src in ("lb", "lbs", "pound", "pounds"):
        kg = value * KG_PER_LB
    elif src in ("kg", "kilogram", "kilograms"):
        kg = value
    elif src in ("st", "stone"):
        kg = value * 6.35029318
    else:
        return value  # unknown unit — pass through untouched rather than corrupt it
    return kg if target_unit == "kg" else kg / KG_PER_LB


def normalize(column, value, unit, target_units):
    """Apply per-metric unit fixes. Returns None to drop an implausible value."""
    if value is None:
        return None
    if column in ("weight", "lean_mass"):
        return convert_mass(value, unit, target_units)
    if column == "body_fat_pct":
        # HealthKit stores body fat as a fraction (0.217); Auto Export sends 21.7.
        # Anything at or below 1 is a fraction. Nobody's body fat is 1%.
        pct = value * 100 if value <= 1.0 else value
        return pct if 1 <= pct <= 75 else None
    if column == "exercise_min" and (unit or "").lower() in ("s", "sec", "second", "seconds"):
        return value / 60.0
    return value


def rounded(column, value):
    digits = ROUND.get(column)
    if digits is None:
        return value
    value = round(value, digits)
    return int(value) if digits == 0 else value


def union_hours(intervals):
    """Total hours covered by intervals, merging overlaps.

    Sleep is the one metric where naive summing is badly wrong: a phone and a watch and
    a sleep app can each report the same night, and stages within one source can abut or
    overlap. Merging first is the only way to get a truthful number.
    """
    if not intervals:
        return 0.0
    ordered = sorted(intervals)
    merged = [list(ordered[0])]
    for start, end in ordered[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return sum((e - s).total_seconds() for s, e in merged) / 3600.0


# --------------------------------------------------------------------------------------
# Accumulator
# --------------------------------------------------------------------------------------

class DayAccumulator:
    """Collects raw readings keyed by date, then collapses them per AGGREGATION."""

    def __init__(self, target_units, since=None):
        self.units = target_units
        self.since = since
        # date -> column -> list of (timestamp, value, source)
        self.readings = defaultdict(lambda: defaultdict(list))
        # date -> bucket -> list of (start, end) per source
        self.sleep = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
        self.skipped_types = defaultdict(int)
        self.record_count = 0
        self.warnings = defaultdict(int)

    def _in_range(self, day):
        return not self.since or day >= self.since

    def add(self, column, timestamp, value, source, unit):
        if timestamp is None or value is None:
            self.warnings["unparseable_record"] += 1
            return
        day = timestamp.strftime("%Y-%m-%d")
        if not self._in_range(day):
            return
        value = normalize(column, value, unit, self.units)
        if value is None:
            self.warnings["implausible_value"] += 1
            return
        self.readings[day][column].append((timestamp, value, source or "unknown"))
        self.record_count += 1

    def add_sleep(self, bucket, start, end, source):
        if not start or not end or end <= start:
            return
        # Sleep belongs to the day you woke up, not the day you lay down.
        day = end.strftime("%Y-%m-%d")
        if not self._in_range(day):
            return
        self.sleep[day][source or "unknown"][bucket].append((start, end))
        self.record_count += 1

    def _collapse(self, entries, how):
        if not entries:
            return None
        if how == "first":
            return min(entries, key=lambda e: e[0])[1]
        if how == "last":
            return max(entries, key=lambda e: e[0])[1]
        if how == "mean":
            return sum(e[1] for e in entries) / len(entries)
        if how == "sum_sources":
            return sum(e[1] for e in entries)
        if how == "sum_max_src":
            # Phone and watch both report steps for the same walk. Summing them inflates
            # the day; picking the single richest source is the honest approximation.
            totals = defaultdict(float)
            for _, value, source in entries:
                totals[source] += value
            return max(totals.values())
        raise ValueError(f"unknown aggregation: {how}")

    def rows(self):
        days = set(self.readings) | set(self.sleep)
        for day in sorted(days):
            row = {"date": day}
            for column, entries in self.readings[day].items():
                value = self._collapse(entries, AGGREGATION.get(column, "last"))
                if value is not None:
                    row[column] = rounded(column, value)

            per_source = self.sleep.get(day)
            if per_source:
                # Score each source by how much sleep it saw, keep the most complete one.
                # Merging across sources would stack a watch's night onto a sleep app's.
                best, best_total = None, -1.0
                for source, buckets in per_source.items():
                    total = union_hours([iv for ivs in buckets.values() for iv in ivs])
                    if total > best_total:
                        best, best_total = buckets, total
                if best_total > 0:
                    row["sleep_hrs"] = rounded("sleep_hrs", best_total)
                    for bucket in ("sleep_deep", "sleep_rem", "sleep_core"):
                        if best.get(bucket):
                            row[bucket] = rounded(bucket, union_hours(best[bucket]))
            yield row


# --------------------------------------------------------------------------------------
# Readers
# --------------------------------------------------------------------------------------

def read_hae_json(path, acc):
    """Health Auto Export — already aggregated per day, so this is mostly a key remap."""
    try:
        with open(path, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
    except json.JSONDecodeError as exc:
        raise ParseError(f"{os.path.basename(path)} is not valid JSON ({exc})")

    metrics = (payload.get("data") or {}).get("metrics") or []
    if not metrics and "metrics" in payload:
        metrics = payload["metrics"]

    for metric in metrics:
        name = metric.get("name")
        unit = metric.get("units")
        points = metric.get("data") or []

        if name == "sleep_analysis":
            for point in points:
                source = point.get("source")
                start = parse_ts(point.get("sleepStart"))
                end = parse_ts(point.get("sleepEnd"))
                stages = {k: point.get(k) for k in ("deep", "rem", "core")}
                if start and end:
                    # Auto Export gives stage totals as hours, not intervals. Synthesize
                    # a single interval for the night, then carry stage totals directly.
                    day = end.strftime("%Y-%m-%d")
                    if acc._in_range(day):
                        total = point.get("totalSleep")
                        if total is None:
                            total = sum(v for v in stages.values() if v) or None
                        if total:
                            acc.readings[day]["sleep_hrs"].append((end, total, source))
                        for key, column in (("deep", "sleep_deep"), ("rem", "sleep_rem"),
                                            ("core", "sleep_core")):
                            if stages.get(key):
                                acc.readings[day][column].append((end, stages[key], source))
                        acc.record_count += 1
            continue

        column = HAE_MAP.get(name)
        if not column:
            acc.skipped_types[name] += 1
            continue
        for point in points:
            acc.add(column, parse_ts(point.get("date")), point.get("qty"),
                    point.get("source"), unit)


def read_stock_xml(stream, acc, progress=None):
    """Stream the stock export.

    export.xml routinely runs past 500MB with a million-plus records, so we iterate and
    discard: clear each element after reading it, and periodically drop the root's
    accumulated children. Memory stays flat regardless of file size.
    """
    context = ElementTree.iterparse(stream, events=("start", "end"))
    try:
        _, root = next(context)
    except (StopIteration, ElementTree.ParseError) as exc:
        raise ParseError(f"could not read XML: {exc}")

    seen = 0
    try:
        for event, elem in context:
            if event != "end":
                continue
            tag = elem.tag

            if tag == "Record":
                rtype = elem.get("type")
                if rtype == SLEEP_TYPE:
                    bucket = SLEEP_STAGES.get(elem.get("value"))
                    if bucket:
                        acc.add_sleep(bucket, parse_ts(elem.get("startDate")),
                                      parse_ts(elem.get("endDate")), elem.get("sourceName"))
                else:
                    column = HK_MAP.get(rtype)
                    if column:
                        try:
                            value = float(elem.get("value"))
                        except (TypeError, ValueError):
                            value = None
                        # Weigh-ins and body comp use startDate; cumulative metrics are
                        # credited to the day the interval ended.
                        stamp = elem.get("startDate") if AGGREGATION.get(column) == "first" \
                            else elem.get("endDate") or elem.get("startDate")
                        acc.add(column, parse_ts(stamp), value,
                                elem.get("sourceName"), elem.get("unit"))
                    elif rtype:
                        acc.skipped_types[rtype] += 1

                seen += 1
                if progress and seen % 250_000 == 0:
                    progress(seen)

            elif tag == "Workout":
                acc.skipped_types["Workout"] += 1

            if tag in ("Record", "Workout", "ActivitySummary", "Correlation"):
                elem.clear()
                root.clear()  # the parser keeps appending finished children here
    except ElementTree.ParseError as exc:
        # A half-downloaded export is the common cause. Keep what we parsed and say so.
        acc.warnings["truncated_xml"] += 1
        if acc.record_count == 0:
            raise ParseError(
                f"XML ended unexpectedly at record ~{seen} and nothing usable was read "
                f"({exc}). The export is probably incomplete — re-export from your iPhone."
            )


def open_input(path, acc, progress=None):
    """Detect what we were handed and route it."""
    if not os.path.exists(path):
        raise ParseError(f"no such file or directory: {path}")

    if os.path.isdir(path):
        json_files = sorted(
            os.path.join(path, name) for name in os.listdir(path)
            if name.lower().endswith(".json") and not name.startswith(".")
        )
        xml_files = [
            os.path.join(path, name) for name in os.listdir(path)
            if name.lower() in ("export.xml", "export_cda.xml")
        ]
        zips = [
            os.path.join(path, name) for name in os.listdir(path)
            if name.lower().endswith(".zip")
        ]
        if not (json_files or xml_files or zips):
            raise ParseError(
                f"{path} has no Apple Health exports in it. Expected export.zip, "
                "export.xml, or HealthAutoExport-*.json files."
            )
        for archive in zips:
            open_input(archive, acc, progress)
        for xml_file in xml_files:
            open_input(xml_file, acc, progress)
        for json_file in json_files:
            read_hae_json(json_file, acc)
        return

    lower = path.lower()
    if lower.endswith(".zip"):
        try:
            with zipfile.ZipFile(path) as archive:
                members = [n for n in archive.namelist()
                           if n.lower().endswith("export.xml") and "__MACOSX" not in n]
                if not members:
                    raise ParseError(
                        f"{os.path.basename(path)} contains no export.xml. Make sure this "
                        "is the archive from Health > your photo > Export All Health Data."
                    )
                # Read the XML straight out of the archive — no temp file, no extraction.
                for member in members:
                    with archive.open(member) as stream:
                        read_stock_xml(stream, acc, progress)
        except zipfile.BadZipFile:
            raise ParseError(f"{os.path.basename(path)} is not a readable zip archive.")
    elif lower.endswith(".xml"):
        with open(path, "rb") as stream:
            read_stock_xml(stream, acc, progress)
    elif lower.endswith(".json"):
        read_hae_json(path, acc)
    else:
        raise ParseError(
            f"don't know how to read {os.path.basename(path)}. Expected .zip, .xml, "
            "or .json."
        )


# --------------------------------------------------------------------------------------
# Output
# --------------------------------------------------------------------------------------

def upsert_csv(rows, out_path, source_label):
    """Merge new rows into daily.csv.

    Device data fills device columns; anything a human typed in via /coach-log stays put
    unless this import actually has a value for that cell. Losing a hand-logged meal to
    a re-import would be unforgivable.
    """
    existing = {}
    if os.path.exists(out_path):
        with open(out_path, "r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                if row.get("date"):
                    existing[row["date"]] = row

    added = updated = 0
    for row in rows:
        date = row["date"]
        payload = {k: v for k, v in row.items() if v not in (None, "")}
        if date in existing:
            current = existing[date]
            changed = False
            for key, value in payload.items():
                if key == "date":
                    continue
                if str(current.get(key, "")) != str(value):
                    current[key] = value
                    changed = True
            if changed:
                marks = set(filter(None, (current.get("entry_source") or "").split("+")))
                marks.add(source_label)
                current["entry_source"] = "+".join(sorted(marks))
                updated += 1
        else:
            payload["entry_source"] = source_label
            existing[date] = payload
            added += 1

    tmp_fd, tmp_path = tempfile.mkstemp(dir=os.path.dirname(out_path) or ".", suffix=".tmp")
    try:
        with os.fdopen(tmp_fd, "w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=COLUMNS, extrasaction="ignore")
            writer.writeheader()
            for date in sorted(existing):
                writer.writerow(existing[date])
        os.replace(tmp_path, out_path)  # atomic: a crash mid-write can't corrupt the file
    except BaseException:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise

    return added, updated, len(existing)


# --------------------------------------------------------------------------------------
# Self-test
# --------------------------------------------------------------------------------------

SELFTEST_XML = """<?xml version="1.0" encoding="UTF-8"?>
<HealthData locale="en_US">
 <Record type="HKQuantityTypeIdentifierBodyMass" sourceName="Scale" unit="lb"
   startDate="2026-03-01 06:30:00 -0500" endDate="2026-03-01 06:30:00 -0500" value="200.0"/>
 <Record type="HKQuantityTypeIdentifierBodyMass" sourceName="Scale" unit="lb"
   startDate="2026-03-01 19:00:00 -0500" endDate="2026-03-01 19:00:00 -0500" value="203.5"/>
 <Record type="HKQuantityTypeIdentifierBodyFatPercentage" sourceName="Scale" unit="%"
   startDate="2026-03-01 06:30:00 -0500" endDate="2026-03-01 06:30:00 -0500" value="0.22"/>
 <Record type="HKQuantityTypeIdentifierStepCount" sourceName="iPhone" unit="count"
   startDate="2026-03-01 08:00:00 -0500" endDate="2026-03-01 09:00:00 -0500" value="3000"/>
 <Record type="HKQuantityTypeIdentifierStepCount" sourceName="Watch" unit="count"
   startDate="2026-03-01 08:00:00 -0500" endDate="2026-03-01 09:00:00 -0500" value="3200"/>
 <Record type="HKQuantityTypeIdentifierStepCount" sourceName="Watch" unit="count"
   startDate="2026-03-01 17:00:00 -0500" endDate="2026-03-01 18:00:00 -0500" value="1800"/>
 <Record type="HKQuantityTypeIdentifierHeartRateVariabilitySDNN" sourceName="Watch" unit="ms"
   startDate="2026-03-01 04:00:00 -0500" endDate="2026-03-01 04:00:00 -0500" value="60"/>
 <Record type="HKQuantityTypeIdentifierHeartRateVariabilitySDNN" sourceName="Watch" unit="ms"
   startDate="2026-03-01 05:00:00 -0500" endDate="2026-03-01 05:00:00 -0500" value="80"/>
 <Record type="HKQuantityTypeIdentifierDietaryProtein" sourceName="MFP" unit="g"
   startDate="2026-03-01 12:00:00 -0500" endDate="2026-03-01 12:00:00 -0500" value="40"/>
 <Record type="HKQuantityTypeIdentifierDietaryProtein" sourceName="MFP" unit="g"
   startDate="2026-03-01 19:00:00 -0500" endDate="2026-03-01 19:00:00 -0500" value="65"/>
 <Record type="HKCategoryTypeIdentifierSleepAnalysis" sourceName="Watch"
   value="HKCategoryValueSleepAnalysisAsleepCore"
   startDate="2026-02-28 23:00:00 -0500" endDate="2026-03-01 03:00:00 -0500"/>
 <Record type="HKCategoryTypeIdentifierSleepAnalysis" sourceName="Watch"
   value="HKCategoryValueSleepAnalysisAsleepDeep"
   startDate="2026-03-01 03:00:00 -0500" endDate="2026-03-01 04:30:00 -0500"/>
 <Record type="HKCategoryTypeIdentifierSleepAnalysis" sourceName="Watch"
   value="HKCategoryValueSleepAnalysisAsleepREM"
   startDate="2026-03-01 04:30:00 -0500" endDate="2026-03-01 06:00:00 -0500"/>
 <Record type="HKCategoryTypeIdentifierSleepAnalysis" sourceName="OtherApp"
   value="HKCategoryValueSleepAnalysisAsleepCore"
   startDate="2026-02-28 23:30:00 -0500" endDate="2026-03-01 05:00:00 -0500"/>
 <Record type="HKCategoryTypeIdentifierSleepAnalysis" sourceName="Watch"
   value="HKCategoryValueSleepAnalysisInBed"
   startDate="2026-02-28 22:00:00 -0500" endDate="2026-03-01 07:00:00 -0500"/>
 <Record type="HKQuantityTypeIdentifierDistanceWalkingRunning" sourceName="iPhone" unit="mi"
   startDate="2026-03-01 08:00:00 -0500" endDate="2026-03-01 09:00:00 -0500" value="1.5"/>
</HealthData>
"""

SELFTEST_EXPECTED = {
    "date": "2026-03-01",
    "weight": 200.0,      # first reading of the day, not the evening one
    "body_fat_pct": 22.0,  # 0.22 fraction promoted to percent
    "steps": 5000,         # Watch 3200+1800 beats iPhone 3000; not 8000
    "hrv": 70.0,           # mean of 60 and 80
    "protein_g": 105.0,    # summed across the day
    "sleep_hrs": 7.0,      # Watch stages merged; OtherApp's overlapping night discarded
    "sleep_deep": 1.5,
    "sleep_rem": 1.5,
    "sleep_core": 4.0,
}


def run_selftest():
    acc = DayAccumulator(target_units="lb")
    read_stock_xml(io.BytesIO(SELFTEST_XML.encode("utf-8")), acc)
    rows = list(acc.rows())

    failures = []
    if len(rows) != 1:
        failures.append(f"expected 1 day, got {len(rows)}")
    else:
        row = rows[0]
        for key, want in SELFTEST_EXPECTED.items():
            got = row.get(key)
            if key == "date":
                if got != want:
                    failures.append(f"date: expected {want}, got {got}")
                continue
            if got is None or abs(float(got) - float(want)) > 0.011:
                failures.append(f"{key}: expected {want}, got {got}")

    if failures:
        print("SELFTEST FAILED", file=sys.stderr)
        for line in failures:
            print(f"  - {line}", file=sys.stderr)
        return 1

    print("Self-test passed. Parser handles unit conversion, source de-duplication,")
    print("overlapping sleep records, and daily aggregation correctly.")
    return 0


# --------------------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------------------

def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Turn an Apple Health export into one row per day.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("path", nargs="?", help="export.zip, export.xml, HAE .json, or a folder")
    parser.add_argument("--out", default="health/data/daily.csv")
    parser.add_argument("--units", choices=("lb", "kg"), default="lb")
    parser.add_argument("--since", help="ignore records before YYYY-MM-DD")
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)

    if args.selftest:
        return run_selftest()
    if not args.path:
        parser.error("a path is required (or use --selftest)")

    if args.since:
        try:
            datetime.strptime(args.since, "%Y-%m-%d")
        except ValueError:
            print("--since must look like YYYY-MM-DD", file=sys.stderr)
            return 1

    def progress(count):
        if not args.quiet:
            print(f"  ... {count:,} records", file=sys.stderr)

    acc = DayAccumulator(target_units=args.units, since=args.since)
    try:
        if not args.quiet:
            print(f"Reading {args.path} ...", file=sys.stderr)
        open_input(args.path, acc, progress)
    except ParseError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    rows = list(acc.rows())
    if not rows:
        print("Error: parsed the input but found no usable health records.", file=sys.stderr)
        print(json.dumps({"days_written": 0, "rows_added": 0, "rows_updated": 0}))
        return 2

    out_dir = os.path.dirname(args.out)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    label = "apple_health"
    added, updated, total = upsert_csv(rows, args.out, label)

    coverage = defaultdict(int)
    for row in rows:
        for key, value in row.items():
            if key != "date" and value not in (None, ""):
                coverage[key] += 1

    summary = {
        "days_written": len(rows),
        "date_min": rows[0]["date"],
        "date_max": rows[-1]["date"],
        "rows_added": added,
        "rows_updated": updated,
        "rows_total": total,
        "records_read": acc.record_count,
        "units": args.units,
        "coverage": dict(sorted(coverage.items())),
        "missing": sorted(set(AGGREGATION) - set(coverage)),
        "skipped_types": len(acc.skipped_types),
        "warnings": dict(acc.warnings),
        "out": args.out,
    }

    if not args.quiet:
        print(f"\nParsed {acc.record_count:,} records into {len(rows)} days "
              f"({rows[0]['date']} to {rows[-1]['date']})", file=sys.stderr)
        print(f"Wrote {args.out}: {added} added, {updated} updated, {total} total\n",
              file=sys.stderr)
        if summary["missing"]:
            print(f"No data for: {', '.join(summary['missing'])}", file=sys.stderr)
        if acc.warnings:
            print(f"Warnings: {dict(acc.warnings)}", file=sys.stderr)

    print(json.dumps(summary))  # stdout stays machine-readable for the skill to parse
    return 0


if __name__ == "__main__":
    sys.exit(main())
