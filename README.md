# Baseline

Point Claude Code at your Apple Health data and get honest, evidence-based feedback on
your diet and your training.

Named for the principle underneath it: you are measured against **your own baseline**,
never against population averages. Your HRV means nothing next to a stranger's. It means
a great deal next to your own last four weeks.

---

## Use at your own risk

**Chris DuBois is not a doctor, not a registered dietitian, and not a certified personal
trainer. In fact, you should probably only listen to him about positioning for marketing
agencies.**

Baseline is software. It reads numbers off your phone and applies published research to
them. It has never examined you, does not know your medical history, and cannot tell the
difference between a plateau and a thyroid problem.

Nothing here is medical advice. Talk to an actual clinician before you change how you eat
or start training — particularly if you have any existing condition, take any medication,
or are pregnant or nursing.

If something feels wrong in your body, believe your body over this software.

---

## What it actually does

You feed it your Apple Health export. It keeps a tidy record, and once a week you ask it
how you're doing. It answers with numbers from your own data and, at most, one thing to
change.

That last part is the design. Most fitness software drowns you in dashboards, or hands
you five adjustments at once so nothing can be attributed to anything. Baseline follows a
fixed decision framework and changes one variable at a time — and when the honest answer
is *keep doing exactly what you're doing*, it says that instead of inventing work.

It will also refuse. It won't set a target below your metabolic floor, won't chase a rate
of loss above 1% of bodyweight per week, and won't coach a weight goal at all for someone
who tells it they have a history of disordered eating.

## What it can't do

Coaching your diet requires knowing what you ate. Apple Health gives up weight, sleep,
steps, and heart data for free — nutrition only shows up if you log food in something
that writes to Health (MyFitnessPal, Cronometer, LoseIt).

If you don't log food, Baseline still works. It runs in observed-only mode: it estimates
your actual maintenance calories by working backwards from weight change, and it coaches
training, sleep, steps, and behavior. That's genuinely useful. It just isn't diet
coaching, and it won't pretend to be.

---

## Setup

**You need:** an iPhone, [Claude Code](https://claude.com/claude-code), and Python 3.9 or
newer (macOS already has it).

```bash
git clone https://github.com/wheresmycoffee11/baseline.git
cd baseline
bash setup.sh --global
```

Then open Claude Code **anywhere** and run `/coach-setup`. About ten minutes of questions
covering your goal, your equipment, your schedule, and a short health screen.

### Two ways to install

**Global — recommended.** `bash setup.sh --global` puts the five commands in
`~/.claude/skills/` and your data in `~/.baseline/health/`. Baseline then works from any
directory, forever, including from whatever project you happen to have open. Remove it
later with `bash setup.sh --uninstall`, which leaves your data alone.

**Local.** `bash setup.sh` keeps everything inside the cloned folder. Nothing touches the
rest of your machine — but **Claude Code only sees the commands when you run it from
inside that folder.** Open Claude anywhere else and `/coach-review` simply won't exist.
That surprises people, so pick global unless you have a reason not to.

Either way, re-running setup is safe. It replaces program files and never touches
`health/`.

### Getting your data in

Two Apple Health exports, doing two different jobs. **Start with the free one.**

**Stock export — free, and enough on its own.**

On your iPhone: Health → your photo (top right) → Export All Health Data. You get an
`export.zip`, often a large one. Drop it in `health/data/inbox/` and run `/coach-import`.

Do this on day one. Baseline refuses to give real advice on less than two weeks of data,
so without a backfill your first useful review is a fortnight away — which is exactly
when people abandon a new system. With it, you get a real review immediately, measured
against months or years of your own history.

The catch is that it's a full dump every time. Minutes to generate, no automation. Fine
weekly, tedious daily.

**Health Auto Export — paid, and worth it if you'll use this daily.**

[Health Auto Export](https://apps.apple.com/app/health-auto-export/id1115567069) writes
small daily JSON files and can do it automatically in the background.

**Be aware of the cost before you commit.** The free tier gives you widgets and an in-app
dashboard and *no export at all*. Exporting needs a paid tier; background automation —
the part that makes a daily habit effortless — needs Premium, sold as a subscription or a
one-time lifetime purchase. There's a seven-day trial.

Nobody is locked out by this. The stock export path is free and fully supported. You're
buying convenience, not capability.

If you do use it, point its output at `health/data/inbox/` and enable at minimum:

`weight_body_mass` · `body_fat_percentage` · `lean_body_mass` ·
**`heart_rate_variability`** · **`resting_heart_rate`** · `sleep_analysis` ·
`step_count` · `active_energy` · `basal_energy_burned` · `apple_exercise_time` ·
`dietary_energy` · `protein` · `carbohydrates` · `total_fat` · `fiber`

Do not skip HRV and resting heart rate. They're off in some configurations, and they're
what the recovery logic runs on. Without them Baseline can't tell an under-recovered week
from a lazy one — and it won't know to tell you, because missing data looks identical to
a rest day.

### The loop

Drop new files in, then:

```
/coach-import        # ten seconds
```

Daily if you can, even though weekly would do. The point isn't the sync — it's staying in
contact with the numbers often enough for them to stay real to you. Data you look at once
a month is data you've already stopped acting on.

Then weekly:

```
/coach-review        # how am I doing, what should I change
/coach-workout       # build me this week's training
```

---

### Try it before you trust it

There's a fabricated six-week dataset in `sample-data/` — someone mid fat-loss phase whose
weekends have quietly come apart. Ask for a review against it and you'll see exactly what
Baseline does with real-looking numbers, without handing over your own:

```
/coach-review using sample-data/
```

None of it is anyone's real data.

## Commands

| Command | What it's for |
|---|---|
| `/coach-setup` | First run. Goal, equipment, schedule, health screen, targets. |
| `/coach-import` | Pull in new Apple Health exports. |
| `/coach-log` | Anything your phone didn't catch — "slept badly", "fasted 18h", "squats felt heavy". |
| `/coach-review` | The weekly check-in. Verdict plus at most one change. |
| `/coach-workout` | A session, a week, or a four-week block built around your equipment. |

---

## Your data stays yours

Everything lives in `health/` as plain CSV and markdown on your own machine. Nothing is
uploaded, no account, no service. `health/` is gitignored, so a careless `git push` can't
leak it.

Plain files also mean you can read your own history without this tool, and delete it
without asking anyone.

---

## Where the advice comes from

The recommendations aren't improvised. They come from published work, cited inline in
`reference/`:

- **Nutrition** — ISSN position stands on protein (Jäger 2017) and diet composition
  (Aragon 2017); Morton 2018 on protein intake; Helms 2014; Garthe 2011 on rate of loss
- **Training** — Schoenfeld on volume and frequency (2016, 2017); Schoenfeld & Grgic
  2021; ACSM progression guidelines; WHO 2020 activity guidelines; Seiler on intensity
  distribution
- **Recovery** — Plews 2013 and Buchheit 2014 on reading HRV against individual
  baselines; AASM/SRS sleep consensus

Where the evidence is genuinely uncertain, the reference docs say so rather than picking
a side and sounding confident.

---

## License

MIT. Do what you like with it.

Built by [Chris DuBois](https://github.com/wheresmycoffee11).
