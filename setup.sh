#!/usr/bin/env bash
# Baseline — setup. Safe to re-run; it never overwrites your data.
#
#   bash setup.sh            install here (skills work only in this folder)
#   bash setup.sh --global   install to ~/.baseline (skills work everywhere)
#   bash setup.sh --uninstall  remove a global install, keeping your data
set -euo pipefail

cd "$(dirname "$0")"
SOURCE="$(pwd)"
HOME_DIR="$HOME/.baseline"
SKILLS_DIR="$HOME/.claude/skills"
MODE="local"

case "${1:-}" in
  --global)    MODE="global" ;;
  --uninstall) MODE="uninstall" ;;
  --help|-h)   sed -n '2,7p' "$0" | sed 's/^# \?//'; exit 0 ;;
  "")          ;;
  *)           echo "Unknown option: $1. Try --help." >&2; exit 1 ;;
esac

say()  { printf '%s\n' "$1"; }
ok()   { printf '  ok    %s\n' "$1"; }
warn() { printf '  note  %s\n' "$1"; }
fail() { printf '  FAIL  %s\n' "$1" >&2; }

say ""
say "Baseline — setup"
say "================"
say ""

# --- Uninstall ------------------------------------------------------------------------
if [ "$MODE" = "uninstall" ]; then
  for skill in coach-setup coach-import coach-log coach-review coach-workout; do
    [ -d "$SKILLS_DIR/$skill" ] && rm -rf "$SKILLS_DIR/$skill" && ok "removed $skill"
  done
  say ""
  if [ -d "$HOME_DIR/health" ]; then
    say "  Your data is untouched at $HOME_DIR/health"
    say "  Delete it yourself if you want it gone — this script won't."
  fi
  say ""
  exit 0
fi

# --- Python ---------------------------------------------------------------------------
if ! command -v python3 >/dev/null 2>&1; then
  fail "python3 not found."
  say ""
  say "  macOS:   xcode-select --install"
  say "  Linux:   sudo apt install python3     (or your package manager)"
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

# --- Where things live ----------------------------------------------------------------
if [ "$MODE" = "global" ]; then
  TARGET="$HOME_DIR"
  mkdir -p "$TARGET"
  # Program files are replaced on every install; health/ is never touched.
  for dir in reference scripts sample-data; do
    rm -rf "$TARGET/$dir"
    cp -R "$SOURCE/$dir" "$TARGET/$dir"
  done
  cp "$SOURCE/CLAUDE.md" "$TARGET/CLAUDE.md"
  cp "$SOURCE/README.md" "$TARGET/README.md"
  ok "pack installed to $TARGET"
else
  TARGET="$SOURCE"
fi

for dir in health/data/inbox health/data/processed health/reviews health/plans; do
  mkdir -p "$TARGET/$dir"
done
ok "health/ scaffolded"

# --- Starter files (never clobbered) --------------------------------------------------
if [ ! -f "$TARGET/health/journal.md" ]; then
  cat > "$TARGET/health/journal.md" <<'EOF'
# Journal

How things actually felt. Sleep quality, stress, soreness, travel, illness, anything the
numbers won't show. Newest at the top.

Add entries by talking to Claude — `/coach-log` — or just type them here yourself.
EOF
  ok "journal.md created"
else
  warn "journal.md already exists — left alone"
fi

HEADER='date,weight,body_fat_pct,lean_mass,bmi,rhr,hrv,sleep_hrs,sleep_deep,sleep_rem,sleep_core,calories_in,protein_g,carbs_g,fat_g,fiber_g,active_kcal,basal_kcal,exercise_min,steps,vo2max,entry_source'
if [ ! -f "$TARGET/health/data/daily.csv" ]; then
  printf '%s\n' "$HEADER" > "$TARGET/health/data/daily.csv"
  ok "daily.csv created"
else
  ROWS=$(( $(wc -l < "$TARGET/health/data/daily.csv") - 1 ))
  warn "daily.csv already has $ROWS days — left alone"
fi

[ -f "$TARGET/health/data/workouts.csv" ] || \
  printf 'date,type,duration_min,kcal,distance,notes\n' > "$TARGET/health/data/workouts.csv"

# --- Install skills -------------------------------------------------------------------
if [ "$MODE" = "global" ]; then
  mkdir -p "$SKILLS_DIR"
  # The skills ship with paths relative to the repo. A global install has to rewrite
  # them to absolute, or every script call breaks the moment you're standing somewhere
  # else — which is the entire point of installing globally.
  python3 - "$SOURCE" "$SKILLS_DIR" "$HOME_DIR" <<'PY'
import os, re, shutil, sys

source, skills_dir, home = sys.argv[1], sys.argv[2], sys.argv[3]
tilde = home.replace(os.path.expanduser("~"), "~", 1)

# Longest prefixes first so health/data/ doesn't get half-rewritten by health/.
PREFIXES = ("health/data/", "health/", "reference/", "scripts/", "sample-data/")

def absolutize(text):
    for prefix in PREFIXES:
        # Only rewrite a path that isn't already absolute or tilde-anchored.
        text = re.sub(r"(?<![\w/~.-])" + re.escape(prefix), f"{tilde}/{prefix}", text)
    return text

installed = []
for name in ("coach-setup", "coach-import", "coach-log", "coach-review", "coach-workout"):
    src = os.path.join(source, ".claude", "skills", name)
    dst = os.path.join(skills_dir, name)
    if os.path.isdir(dst):
        shutil.rmtree(dst)
    os.makedirs(dst)
    for entry in os.listdir(src):
        if not entry.endswith(".md"):
            continue
        body = open(os.path.join(src, entry), encoding="utf-8").read()
        # Sibling files (gold-example.md, the rubrics) travel with the skill — leave them.
        open(os.path.join(dst, entry), "w", encoding="utf-8").write(absolutize(body))
    installed.append(name)

print("\n".join(f"  ok    /{n}" for n in installed))

# Verify every rewritten path actually resolves. A skill that points at a file which
# isn't there fails silently at the worst moment — mid-review, on someone's health data —
# so catch it at install time instead.
broken, siblings = [], {"gold-example.md", "review-rubric.md", "plan-rubric.md"}
# Created by /coach-setup or /coach-import, so absent on a fresh install by design.
RUNTIME = ("/health/",)
for name in installed:
    for entry in os.listdir(os.path.join(skills_dir, name)):
        path = os.path.join(skills_dir, name, entry)
        body = open(path, encoding="utf-8").read()
        for ref in re.findall(r"~/[\w./-]+\.(?:py|md|csv|json)", body):
            if any(marker in ref for marker in RUNTIME):
                continue
            if not os.path.exists(os.path.expanduser(ref)):
                broken.append(f"{name}/{entry} -> {ref}")
        # A bare reference-doc filename means the prefix was missing before rewriting,
        # so it silently stayed relative and now points at a sibling that doesn't exist.
        for ref in re.findall(r"`([\w-]+\.(?:py|md))`", body):
            if ref in siblings:
                continue
            if os.path.exists(os.path.join(skills_dir, name, ref)):
                continue
            if os.path.exists(os.path.join(home, ref)):   # root docs: README.md, CLAUDE.md
                continue
            if True:
                broken.append(f"{name}/{entry} -> bare `{ref}` (missing directory prefix)")

if broken:
    print("\n  FAIL  installed skills reference paths that do not exist:")
    for line in sorted(set(broken)):
        print(f"          {line}")
    sys.exit(1)
print("  ok    all skill file references resolve")
PY
  ok "skills installed to $SKILLS_DIR"
fi

# --- Parser self-test -----------------------------------------------------------------
say ""
say "Testing the Apple Health parser..."
if python3 "$TARGET/scripts/apple_health_parse.py" --selftest >/dev/null 2>&1; then
  ok "parser self-test passed"
else
  fail "parser self-test failed — something is wrong with this install."
  say ""
  python3 "$TARGET/scripts/apple_health_parse.py" --selftest || true
  exit 1
fi

# --- Next steps -----------------------------------------------------------------------
say ""
say "Setup complete."
say ""
if [ "$MODE" = "global" ]; then
  say "  Baseline now works from any directory. Your data lives in"
  say "  $HOME_DIR/health and stays there."
  say ""
  if [ -f "$TARGET/health/profile.md" ]; then
    say "  You're already onboarded. Drop exports in"
    say "  $HOME_DIR/health/data/inbox/ and run /coach-import."
  else
    say "  Next:  open Claude Code anywhere and run /coach-setup"
  fi
  say ""
  say "  To remove later:  bash setup.sh --uninstall  (keeps your data)"
else
  say "  Installed here only. Claude Code must be run FROM this folder —"
  say "  the skills won't exist anywhere else."
  say ""
  if [ -f "$TARGET/health/profile.md" ]; then
    say "  You're already onboarded. Drop exports in health/data/inbox/"
    say "  and run /coach-import."
  else
    say "  Next:  claude"
    say "         /coach-setup"
  fi
  say ""
  say "  Prefer it available everywhere?  bash setup.sh --global"
fi
say ""
say "  Reminder: this is not medical advice, and the person who wrote it is"
say "  not a doctor, dietitian, or trainer. Use at your own risk."
say ""
