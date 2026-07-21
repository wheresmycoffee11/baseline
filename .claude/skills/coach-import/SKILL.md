---
name: coach-import
description: Pulls Apple Health exports into Baseline's daily record. Detects whether the file is a stock export.zip/export.xml or Health Auto Export JSON, runs the streaming parser, upserts health/data/daily.csv, and reports what actually landed. Use when the user says "/coach-import", "import my health data", "I dropped my export in", "sync my data", or after any mention of a new export being available. Do NOT use for typing in numbers by hand — use /coach-log. Do NOT use for analysis or recommendations — use /coach-review. Do NOT use for first-time onboarding — use /coach-setup.
---

# Coach Import

Thin wrapper around `scripts/apple_health_parse.py`. The parser does the work; this skill
finds the files, runs it, and tells the truth about the result.

## Run it

1. **Check the inbox.** `health/data/inbox/` — look for `export.zip`, `export.xml`, or
   `HealthAutoExport-*.json`.

   Empty? Say so and give both paths for getting data in (see `README.md`). Don't guess at
   other locations. If the user says the file is somewhere else, use that path.

2. **Read units** from `health/targets.json`. If there's no targets file the user hasn't
   onboarded — run `/coach-setup` first.

3. **Run the parser** on the whole inbox directory. It auto-detects each file's shape, so
   one invocation handles a mixed drop:

   ```bash
   python3 scripts/apple_health_parse.py health/data/inbox \
     --out health/data/daily.csv --units lb
   ```

   Large stock exports take a few minutes and print progress to stderr. Say that up front
   so a long pause doesn't read as a hang.

4. **Parse the JSON summary** on stdout — the last line. Every number you report comes
   from it. Do not count rows yourself, and do not estimate.

5. **Move processed files** to `health/data/processed/` so the next run doesn't redo them.
   The parser is idempotent, so a re-run is harmless — this is just hygiene.

## Report

Use the real figures from the summary:

```
Imported 412 days (2025-04-02 to 2026-07-21).
118 added, 294 updated. 1,204,881 records read.

Missing entirely: hrv, rhr
```

Then, only when there's something worth saying:

- **HRV or resting heart rate missing** → flag it. This is the most common and most
  invisible setup failure: they're off by default in some Auto Export configurations, and
  absent data looks exactly like a rest day. Without them the recovery gate can't fire.
  Tell them which metrics to enable.
- **Nutrition missing** → note it once, explain observed-only mode in a sentence, don't
  nag. Plenty of people never log food and Baseline still works.
- **Warnings in the summary** → surface them plainly. `truncated_xml` means the export is
  incomplete and should be re-generated on the phone.
- **Enough data now** → if `rows_total` crosses 14, offer `/coach-review`.

## Rules

- **Never fabricate counts.** If the summary didn't parse, say the import ran but you
  couldn't read the result, and show the raw output.
- **Never edit `daily.csv` by hand here.** The parser owns that file. Manual corrections
  go through `/coach-log`, which knows not to trample device data.
- **Don't editorialize on the numbers.** Import reports what landed. Interpretation is
  `/coach-review`'s job, and doing it here produces off-the-cuff advice with none of the
  framework or safety checks attached.

## Failure modes

| Symptom | What to do |
|---|---|
| Exit 1, "not a readable zip" | The download is corrupt or partial. Re-export from the phone. |
| Exit 2, zero records | File parsed but held nothing usable — usually the wrong file, e.g. `export_cda.xml`. |
| `python3: command not found` | Point at the install instructions in `README.md`. |
| Runs several minutes on a stock export | Normal. 500MB+ files are expected. |
| Everything imported but all nutrition is empty | Their food app isn't writing to Apple Health, or the metric isn't enabled in Auto Export. |
