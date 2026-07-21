# Recovery Principles

The evidence behind how Baseline reads HRV, resting heart rate, and sleep — and, more
importantly, how much weight those signals can actually carry.

Recovery metrics are where consumer wearable marketing has run furthest ahead of the
science. A ring that assigns a "Readiness Score" of 68 is presenting an opaque transform
of two or three noisy signals as though it were a measurement. It isn't. Under-claim
here. A coach who says the data is ambiguous, when it is, keeps their credibility for the
day the data is genuinely clear.

Read `reference/safety.md` alongside this. Red flags there override everything here.

---

## 1. The central principle: personal baseline, never population norms

**This is the whole rationale for the tool's name. It is the first thing to get right and
the easiest thing to get wrong.**

An HRV of 45 ms is meaningless as an absolute number. HRV varies enormously between
people — by age, genetics, fitness, measurement method, and body position — to the point
that two healthy people can differ several-fold. Comparing one person's 45 to another
person's 90 tells you approximately nothing about who is better recovered. The same 45
against *that person's own* 4-week average of 62 is a real signal worth discussing.

Plews et al. (2013) make the case directly: HRV monitoring is only defensible against an
individual's own established baseline, using rolling averages rather than single values,
because between-person variation swamps the within-person signal.

Practical consequences for every review Baseline writes:

- **Never** cite an age-group or population "normal" for HRV. There is no clinically
  useful normal range for a consumer wearable HRV number.
- Report deviations in the person's own units: "your 7-day average is 12% below your
  30-day average," not "your HRV is low."
- A new user has no baseline. **Do not interpret recovery data in the first 3–4 weeks.**
  Say plainly that you're still collecting a baseline. That is a complete answer.
- If `trend_report.py` hasn't produced a rolling average, there is no recovery read to
  give. Don't improvise one.

The same logic applies to resting heart rate and to sleep duration. Everything below is
downstream of this section.

---

## 2. HRV — what it reflects, and what it doesn't

### What it is, and what it isn't

Heart rate variability is the variation in time between consecutive heartbeats; vagally
mediated indices reflect parasympathetic input to the heart. That is the honest
description of what's being measured.

It is *not* a "recovery score," a measure of fitness, a stress meter, or a readout of how
hard you can train today. Those are interpretive layers stacked on an autonomic
measurement, each adding noise. Buchheit (2014) argues most contradictory findings in this
literature come from methodological inconsistency and misinterpretation rather than
limitations of the measurement — the interpretation is where things break.

Even the direction of change isn't always obvious. Plews et al. (2013) found that in elite
athletes *both* increases and decreases in HRV have been associated with negative
adaptation, and that improvements in cardiorespiratory fitness have shown up alongside
decreases in HRV. Do not present "HRV down = bad" as settled.

### Why single readings are close to useless

Day-to-day variability in resting HRV is large even in healthy people with nothing wrong.
A 14-day study in healthy adults (*Sensors*, 2025) found a mean within-person coefficient
of variation for daily RMSSD of 0.37 — roughly 37% swing around a person's own mean —
with individual CVs ranging from 0.14 to 0.71. Buchheit (2014) reports a day-to-day CV of
around 12% for RMSSD under controlled morning measurement conditions, and far worse for
spectral indices such as LF/HF (CV ≈ 82%, which is why Baseline ignores them entirely).

Either figure is larger than most of the changes people want to act on. **A single day's
HRV reading cannot be distinguished from noise.** Treat it that way.

### Rolling averages are the only defensible read

Plews et al. (2014) tested how many days must be averaged to approximate a full week's
signal, and concluded practitioners need a **minimum of 3 valid, randomly distributed
readings per week**. Buchheit (2014) recommends collecting on waking at least 3–4 times a
week and averaging.

Baseline's read:

- **7-day rolling average** compared against a **28–30-day rolling average**. This is the
  comparison to coach from.
- Require at least 3 valid readings in the 7-day window. Below that, report insufficient
  data rather than a noisy average.
- Never coach from a day-over-day change.

### Measurement windows

The 1996 Task Force standard defines two recording windows — short-term 5-minute and
24-hour — and Buchheit (2014) describes 5–10 minute recordings on waking, supine or
seated, as field best practice. Consumer devices do neither. Apple Watch samples
opportunistically across the day and night, in unspecified windows, using wrist
photoplethysmography rather than ECG, so the timing, duration, and body position behind
any given value are largely unknown to you.

The workaround is consistency, not precision: encourage a fixed context (overnight or on
waking, same device, same wrist), and accept that absolute values are device-specific.
If someone switches from an Apple Watch to an Oura ring, **their baseline resets.** Say
so, and start over.

### SDNN vs RMSSD, and why it matters here

Two time-domain indices dominate:

- **RMSSD** — root mean square of successive differences. Reflects short-term, vagally
  mediated variation. The index the athlete-monitoring literature almost entirely uses,
  and the one most robust to short recordings.
- **SDNN** — standard deviation of all normal-to-normal intervals. Reflects total
  variability from all sources.

**Apple Health reports SDNN** (`heartRateVariabilitySDNN` in HealthKit). Two consequences.

**Comparability.** The Task Force (1996) is blunt that SDNN is not a well-defined
statistical quantity because it depends on recording length — longer recordings capture
more sources of variation and produce systematically higher values, so **SDNN values from
recordings of different durations should not be compared to each other.** Apple does not
surface the duration behind each sample, so some of the day-to-day scatter in an Apple HRV
series is measurement artifact, not physiology.

**Translation.** Nearly every threshold, CV, and smallest-worthwhile-change figure in this
literature was derived from RMSSD, and those numbers **do not transfer cleanly to SDNN.**
Any threshold Baseline applies to Apple HRV data is borrowed from a different index. Do
not present borrowed thresholds as precise.

### What magnitude is worth acting on

Buchheit (2014) estimates the smallest worthwhile change in resting vagal HRV at roughly
**+3%**, and reports a signal-to-noise ratio for resting HRV of **0.8** — meaning the
typical training-induced change is *smaller than the measurement error*. That is the most
important number in this document.

Baseline's working thresholds, stated as the rough heuristics they are:

| 7-day avg vs 28-day avg | Read |
|---|---|
| Within ±5% | Normal fluctuation. Say nothing. |
| 5–10% below | Watch. Not actionable alone. |
| >10% below, 3+ days, plus corroborating signals | Treat as a genuine under-recovery pattern |
| Any large sustained deviation | See section 8 — this may not be a training question |

**Be honest about the uncertainty.** These cut-points are not validated for consumer SDNN
data in general populations. They are a defensible convention, not a measurement. Say
"below your usual range" rather than implying a threshold was crossed.

---

## 3. Resting heart rate — cruder, steadier, often more useful

RHR carries less information than HRV but carries it more reliably, and for a consumer
tool that trade is usually worth taking.

Buchheit (2014) puts resting HR's signal-to-noise ratio at 0.7 versus 0.8 for resting HRV
— practically the same — and reports correlations between HR-based measures and
performance or overreaching status only slightly weaker than the HRV equivalents
(*r* = 0.81 vs 0.88 for non-functional overreaching; *r* = 0.73 vs 0.76 for 10 km
performance). Since RHR is simpler to measure, better standardized across devices, and
easier for a non-expert to understand, it is frequently the more actionable of the two.

**Establishing the baseline.** Same construction as HRV: 7-day rolling average against a
28–30-day rolling average, from overnight or waking values, same device throughout. Allow
3–4 weeks before interpreting anything.

**What a sustained elevation suggests.** A rise of roughly 5+ bpm above baseline sustained
across several days is a real signal — accumulated fatigue, incomplete recovery,
inadequate sleep, or an incubating illness. Radin et al. (2020) used elevated resting
heart rate plus sleep changes across ~47,000 Fitbit users to improve state-level
influenza-like illness surveillance.

Note the shape of that claim: it is a *population* signal about the timing of flu season,
not a per-person diagnostic. An individual's RHR bump does not mean they have the flu. It
means something is different. Baseline notes it; it does not name a cause.

Sustained elevations of 15+ bpm above baseline, or absolute RHR above 100, are red flags
in `reference/safety.md` and route to a clinician, not to a deload.

---

## 4. What confounds both signals

Before treating any deviation as training stress, rule these out. Most "bad recovery
days" are one of these, and asking one question resolves it.

| Confound | Effect |
|---|---|
| **Alcohol** | Large, dose-dependent. Suppresses HRV and raises heart rate during early sleep. |
| **Illness / infection** | Raises RHR, disturbs HRV. Often precedes symptoms. |
| **Poor or short sleep** | Both signals degrade. |
| **Dehydration** | Raises RHR. |
| **Heat** | Elevated ambient or body temperature raises RHR. |
| **Late or large meals** | Digestion elevates HR and suppresses overnight HRV. |
| **Travel / time zone shift** | Circadian disruption confounds both for several days. |
| **Menstrual cycle phase** | Systematic, expected, not a recovery problem. |
| **Medications, especially cardiac** | **Can invalidate both signals entirely.** |

**Alcohol** is the largest confound Baseline will encounter and the one users least
expect. Pietilä et al. (2018), studying nocturnal autonomic regulation in a large
real-world sample of Finnish employees, found acute alcohol intake measurably reduced
parasympathetic-dominant recovery during the first hours of sleep, scaling with dose. If
someone drank last night, their recovery data is describing the drink. Ask before
interpreting, and ask without moralizing.

**Menstrual cycle phase** is systematic and *expected*. Schmalenberger et al. (2019), a
systematic review and meta-analysis of within-person changes across the cycle, found
vagally mediated HRV decreases significantly in the luteal phase, with follow-up work
pointing to progesterone as the driver. Coach it as a known cyclical pattern, not
under-recovery. If cycle phase is tracked, expect the luteal dip and don't deload for it.

### Medications — the hard stop

**Beta blockers and other cardiac medications invalidate HRV and resting heart rate as
recovery signals.** This is not an "interpret with caution" case. Beta blockade
pharmacologically suppresses heart rate and alters HRV indices by design — well documented
in the cardiology literature (e.g. *JACC*, 1994; *Scientific Reports*, 2023, on beta
blockade and circadian HRV). Antiarrhythmics, some antidepressants, and stimulants also
alter autonomic measures.

When a medication is flagged at onboarding, per `reference/safety.md`:

- The recovery gate runs on **sleep alone**.
- Do not report HRV or RHR trends, and do not interpret them "adjusted for" the drug.
- Do not comment on the medication, its effects, dose, or interactions. Note once that a
  clinician should be in the loop, and move on.

The failure this prevents is real: a beta-blocked user has permanently low HRV and low RHR
that will read as either heroic fitness or chronic under-recovery depending which way you
squint. Both would be fabrications.

---

## 5. Sleep

### Duration

The AASM and Sleep Research Society joint consensus statement (Watson et al., 2015)
recommends adults **sleep 7 or more hours per night on a regular basis** to promote
optimal health, noting that regularly sleeping less than 7 hours is associated with
adverse outcomes including weight gain, hypertension, cardiovascular disease, depression,
and increased mortality risk.

That is the anchor. It is a general adult health recommendation, not an athletic
optimization target, and Baseline should not inflate it into one. There is no strong
evidence base for a consumer tool telling someone they need 9 hours.

For training specifically, Fullagar et al. (2015) reviewed the effects of sleep loss on
exercise performance and on physiological and cognitive responses to exercise. The honest
summary: performance is frequently impaired following sleep loss, but findings conflict
and the extent and mechanisms remain uncertain, with cognitive and perceptual effects
appearing more consistent than raw physical output. Present it that way — "short sleep
tends to make training feel harder and go worse," not "sleep debt costs you X% of your
squat."

### What consumer sleep staging can and cannot tell you

Be blunt with users here, because the marketing is not.

Chinoy et al. (2021) tested seven consumer sleep-tracking devices against polysomnography
across three lab nights including a disrupted-sleep condition. **Sleep stage**
classification performance was highly variable, and the authors concluded these devices
"in their current form, are still best utilized for tracking sleep-wake outcomes and not
sleep stages."

So:

- **Reasonably usable:** total sleep time, bed time, wake time, sleep-wake patterns,
  night-to-night consistency.
- **Not reliable enough to coach from:** deep sleep minutes, REM minutes, and any score
  built on top of them.

Baseline does not coach to deep-sleep or REM numbers. If a user asks why their deep sleep
was 42 minutes, the correct answer is that consumer devices don't classify stages
accurately enough for that number to mean anything, and that total duration and
consistency are the parts worth looking at. Say it once, plainly, without apology.

### Consistency and sleep debt

**Consistency** — stable sleep and wake times — is worth coaching and is something
consumer devices capture well. Erratic timing across a week is often more tractable than
total duration, and it's the intervention with the fewest trade-offs.

**Sleep debt** is best framed as a rolling cumulative shortfall against the person's own
target (7+ hours, or whatever is set in `health/targets.json`) over 7 and 14 days. It's a
bookkeeping device, not a precise physiological quantity — there is no validated exchange
rate for "paying back" lost sleep. Use it to show a pattern, not to settle an account.

One short night is not sleep debt. Three or four in a week is a pattern.

---

## 6. Reading the signals together

**No single metric drives a decision.** This is the operative rule.

Each signal alone has a signal-to-noise ratio below 1, a large day-to-day CV, and half a
dozen confounds. Agreement across independent signals is what makes a read defensible;
Buchheit (2014) treats the various heart-rate-derived measures as complementary, with
convergence across them carrying the interpretive weight.

### What a genuine under-recovery pattern looks like

Look for **most of these, sustained over 3+ days**, with confounds ruled out:

- 7-day HRV average trending below the 28-day average by more than ~10%
- Resting heart rate elevated ~5+ bpm above baseline
- Sleep duration short or disrupted across multiple nights
- Subjective state degraded — fatigue, low motivation, poor mood, elevated soreness,
  sessions feeling disproportionately hard
- Performance actually declining — loads down, paces slower, sessions being cut short
- A plausible cause: a heavy training block, a life stressor, travel, illness

Subjective state and performance are not soft supporting evidence — they are often the
most reliable inputs available. The 2025 *Sensors* study found daily RMSSD did track
self-reported sleep quality, fatigue, and stress, but as an association across many
observations, not as a per-day diagnostic. If someone feels fine and is training well, a
dipping HRV number is weak grounds for changing anything.

### Normal noise, and the failure mode to guard against

**The most common failure mode in this domain is over-reacting to one bad night.** It is
also the one most likely to make a user distrust the tool, because they can feel that
they're fine.

Given a within-person CV around 12–37%, a single reading 20% below average is an
*expected* occurrence, not a signal. It will happen regularly to a perfectly recovered
person.

Do not flag under-recovery when:

- Only one day is off
- Only one metric is off and the others are unremarkable
- The person feels fine and their training is going fine
- There is an obvious confound (a drink, a late meal, a hot room, a flight, luteal phase)
- The baseline is younger than 3–4 weeks

In all of those cases, the correct output is that this looks like normal fluctuation and
nothing needs to change. Say it with conviction. Manufacturing a concern to seem useful is
worse than saying nothing.

---

## 7. What to actually do about it

When a genuine multi-signal pattern is confirmed, work the ladder in order. Start at the
top. Escalate only if the pattern persists.

**0. Nothing.** The default. One night, one metric, an obvious confound, or a person who
feels fine — the answer is normal fluctuation. Do not skip this rung; it is the correct
answer most of the time.

**1. Sleep first.** Always the first real intervention and the one with the best evidence
behind it (Watson et al., 2015; Fullagar et al., 2015). Extend duration toward 7+ hours,
stabilize bed and wake times, address obvious disruptors. Nothing further down this ladder
works if sleep is the problem, and sleep is very often the problem. Give it 3–5 days
before escalating.

**2. Reduce training volume.** Cut sets, distance, or session length while holding
intensity and frequency. Roughly 20–40% less volume for a week. Preserves the stimulus and
the habit while lowering total load.

**3. Reduce intensity.** If a volume cut hasn't moved the pattern, drop the hard sessions,
keep the easy ones, stay under threshold. Keep moving — complete rest is rarely right at
this stage.

**4. Deload.** A structured week at substantially reduced volume *and* intensity, with an
explicit return date. Not an indefinite retreat. If a deload doesn't resolve the pattern,
this has stopped being a training question — go to section 8.

Two standing notes: every rung is reversible and should be reassessed against the same
rolling averages that triggered it, so don't leave someone deloaded because nobody
checked. And frame all of it as load management, never as failure.

---

## 8. When a recovery signal is a medical signal

There is a point where the answer stops being "train less" and becomes "see a doctor."
Baseline must not coach past that line.

The red-flag list in `reference/safety.md` governs — sustained RHR 15+ bpm above baseline
or above 100, a sharp HRV drop alongside signs of illness, chest pain or fainting, lost
menstrual period, and the rest. Those route out immediately, and the review ships that
concern alone. Three recovery-specific additions:

- A large HRV deviation persisting 2+ weeks despite genuine load reduction and improved
  sleep
- Recovery signals deteriorating while training load is *falling*
- Sleep persistently disrupted for weeks with no obvious cause

Refer out cleanly: one clear message, no training advice attached, no "but otherwise
you're doing great." And do not name a cause. Baseline does not diagnose, does not
speculate about what a number might mean medically, and does not offer differentials.
*"This is outside what training stress explains, please get it looked at"* is the complete
message.

---

## What this document does not cover

Out of scope here and out of scope for the tool:

- **Diagnosis of anything** — including overtraining syndrome, which is a clinical
  diagnosis of exclusion, not something a wearable detects
- **Sleep disorders** — apnea, insomnia, restless legs, narcolepsy, circadian rhythm
  disorders. Suspected apnea especially (loud snoring, witnessed breathing pauses,
  unexplained daytime sleepiness) is a referral, not a coaching topic
- **Supplements and medications** — no recommendations, dosing, interactions, or
  commentary on what someone already takes, melatonin and magnesium included
- **Bloodwork and biomarkers** — cortisol, testosterone, thyroid panels, CGM data
- **Blood pressure, SpO2, ECG, AFib notifications, respiratory rate** — none are read as
  recovery inputs; a wearable AFib notification goes to a doctor
- **Recovery modalities** — cold plunge, sauna, compression, massage. Evidence is mixed to
  weak; Baseline takes no position
- **Pregnancy, postpartum, perimenopause** — all materially change autonomic and sleep
  patterns. Refer out
- **Pediatric and adolescent recovery** — coaching mode is 18+

When a question lands here, say so in one sentence, say who to ask instead, and stop.

---

## References

All verified. Do not add to this list without checking the source directly.

1. Plews DJ, Laursen PB, Stanley J, Kilding AE, Buchheit M. Training adaptation and heart
   rate variability in elite endurance athletes. *Sports Med.* 2013;43(9):773–781.
2. Buchheit M. Monitoring training status with HR measures: do all roads lead to Rome?
   *Front Physiol.* 2014;5:73. doi:10.3389/fphys.2014.00073
3. Plews DJ, Laursen PB, Le Meur Y, Hausswirth C, Kilding AE, Buchheit M. Monitoring
   training with heart-rate variability: how much compliance is needed for valid
   assessment? *Int J Sports Physiol Perform.* 2014;9(5):783–790.
4. Watson NF, et al. Recommended amount of sleep for a healthy adult: a joint consensus
   statement of the AASM and Sleep Research Society. *J Clin Sleep Med* / *SLEEP.* 2015.
   doi:10.5664/jcsm.4758
5. Fullagar HHK, Skorski S, Duffield R, Hammes D, Coutts AJ, Meyer T. Sleep and athletic
   performance. *Sports Med.* 2015;45:161–186.
6. Task Force of the ESC and NASPE. Heart rate variability: standards of measurement,
   physiological interpretation, and clinical use. *Circulation.* 1996;93:1043–1065.
7. Chinoy ED, Cuellar JA, et al. Performance of seven consumer sleep-tracking devices
   compared with polysomnography. *SLEEP.* 2021;44(5):zsaa291.
8. Pietilä J, Helander E, Korhonen I, Myllymäki T, Kujala UM, Lindholm H. Acute effect of
   alcohol intake on cardiovascular autonomic regulation during the first hours of sleep.
   *JMIR Ment Health.* 2018;5(1):e23.
9. Radin JM, Wineinger NE, Topol EJ, Steinhubl SR. Harnessing wearable device data to
   improve state-level real-time surveillance of influenza-like illness in the USA.
   *Lancet Digit Health.* 2020.
10. Schmalenberger KM, et al. Within-person changes in cardiac vagal activity across the
    menstrual cycle: a systematic review and meta-analysis. *J Clin Med.* 2019;8(11):1946.
11. Associations between daily heart rate variability and self-reported wellness: a 14-day
    observational study in healthy adults. *Sensors.* 2025;25(14):4415. (41 participants,
    424 daily observations; mean within-person RMSSD CV = 0.37.)
12. Apple Inc. `heartRateVariabilitySDNN`, HealthKit developer documentation. Confirms
    Apple Health reports HRV as SDNN.
13. Beta blockade: Effect of beta-blockade on heart rate variability in patients with
    coronary artery disease. *JACC.* 1994. And: Investigating the effects of beta-blockers
    on circadian heart rhythm using heart rate variability. *Sci Rep.* 2023.
