#!/usr/bin/env bash
# Baseline — one-time scaffolding. Safe to re-run; it never overwrites your data.
set -euo pipefail

cd "$(dirname "$0")"

say()  { printf '%s\n' "$1"; }
ok()   { printf '  ok    %s\n' "$1"; }
warn() { printf '  note  %s\n' "$1"; }
fail() { printf '  FAIL  %s\n' "$1" >&2; }

say ""
say "Baseline — setup"
say "================"
say ""

# --- Python ---------------------------------------------------------------------------
if ! command -v python3 >/dev/null 2>&1; then
  fail "python3 not found."
  say ""
  say "  macOS:  xcode-select --install"
  say "  Linux:  sudo apt install python3     (or your package manager)"
  say "  Windows: https://python.org/downloads  (tick 'Add to PATH')"
  say ""
  exit 1
fi

PY_VERSION="$(python3 -c 'import sys; print("%d.%d" % sys.version_info[:2])')"
if ! python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)'; then
  fail "Python $PY_VERSION found, but 3.9 or newer is required."
  exit 1
fi
ok "python3 $PY_VERSION"

# --- Directories ----------------------------------------------------------------------
for dir in health/data/inbox health/data/processed health/reviews health/plans; do
  mkdir -p "$dir"
done
ok "health/ scaffolded"

# --- Starter files (never clobbered) --------------------------------------------------
if [ ! -f health/journal.md ]; then
  cat > health/journal.md <<'EOF'
# Journal

How things actually felt. Sleep quality, stress, soreness, travel, illness, anything the
numbers won't show. Newest at the top.

Add entries by talking to Claude — `/coach-log` — or just type them here yourself.
EOF
  ok "health/journal.md created"
else
  warn "health/journal.md already exists — left alone"
fi

if [ ! -f health/data/daily.csv ]; then
  printf 'date,weight,body_fat_pct,lean_mass,bmi,rhr,hrv,sleep_hrs,sleep_deep,sleep_rem,sleep_core,calories_in,protein_g,carbs_g,fat_g,fiber_g,active_kcal,basal_kcal,exercise_min,steps,vo2max,entry_source\n' > health/data/daily.csv
  ok "health/data/daily.csv created"
else
  ROWS=$(( $(wc -l < health/data/daily.csv) - 1 ))
  warn "health/data/daily.csv already has $ROWS days — left alone"
fi

if [ ! -f health/data/workouts.csv ]; then
  printf 'date,type,duration_min,kcal,distance,notes\n' > health/data/workouts.csv
  ok "health/data/workouts.csv created"
fi

# --- Parser self-test -----------------------------------------------------------------
say ""
say "Testing the Apple Health parser..."
if python3 scripts/apple_health_parse.py --selftest >/dev/null 2>&1; then
  ok "parser self-test passed"
else
  fail "parser self-test failed — something is wrong with this install."
  say ""
  python3 scripts/apple_health_parse.py --selftest || true
  exit 1
fi

# --- Next steps -----------------------------------------------------------------------
say ""
say "Setup complete."
say ""
if [ -f health/profile.md ]; then
  say "  You're already onboarded. Drop new exports in health/data/inbox/"
  say "  and run /coach-import."
else
  say "  Next:  claude"
  say "         /coach-setup"
  say ""
  say "  Ten minutes of questions and you're running."
fi
say ""
say "  Reminder: this is not medical advice, and the person who wrote it is"
say "  not a doctor, dietitian, or trainer. Use at your own risk."
say ""
