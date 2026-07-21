# Nutrition principles

The evidence behind the numbers this pack prescribes. Read it before setting a target,
explaining a plateau, or answering "why that number?"

Every citation here has been checked against the source. If you want to make a claim that
isn't in this file, say it's your read rather than dressing it as evidence. **A confident
sentence with an invented source behind it is the worst thing this tool can produce** —
worse than saying "I don't know," and much worse than "the evidence here is mixed."

Full references at the bottom.

---

## 1. Protein

### The numbers

| Situation | Target |
|---|---|
| General, training regularly | 1.6 g/kg bodyweight/day |
| In a deficit, lean, wants to keep muscle | 1.8–2.2 g/kg bodyweight/day |
| Very lean and in an aggressive deficit | up to ~2.4 g/kg bodyweight/day |
| Per meal | ~0.4 g/kg, across 4 or so meals |

Round to something a person can hit. "160 g" gets eaten; "158.4 g" gets abandoned.

### Why 1.6

Morton et al. (2018) pooled 49 studies and 1,863 people training with resistance. Protein
intake improved gains in fat-free mass and strength, and the dose-response curve flattened
at **1.62 g/kg/day** — beyond that, more protein bought no further fat-free mass.

The part that gets dropped when this figure is quoted: the 95% confidence interval on that
breakpoint runs **1.03 to 2.20 g/kg/day**. That is a wide interval. It means 1.6 is a
reasonable central estimate, not a discovered constant. Anyone presenting it to two decimal
places is over-reading the data. Treat 1.6 as "comfortably enough for most people most of
the time," and don't tell a user that 1.5 is failure.

Also worth knowing: this meta-analysis carried a published correction in 2020. The headline
conclusion survived, but it's a reminder that even good evidence gets revised.

### Why it goes up in a deficit

Two things happen when energy comes down. Some protein gets burned for fuel rather than
used for repair, and the body has less total energy available to defend lean tissue. So
protein needs rise exactly when total food is falling.

Helms et al. (2014) reviewed lean, resistance-trained athletes eating at a deficit and
concluded needs were likely **2.3–3.1 g/kg of fat-free mass**, scaling upward with how
severe the deficit is and how lean the person already is.

Note the denominator: **fat-free mass, not bodyweight.** This trips people up constantly.
For a lean athlete the two numbers are close. For someone at 35% body fat they are not —
converting Helms's range to total bodyweight for a heavier person produces an absurd
target. When you don't have a body-composition estimate, use the bodyweight ranges in the
table above and say that's what you're doing.

### Distribution

Schoenfeld and Aragon (2018) reviewed the per-meal question and landed on roughly
**0.4 g/kg per meal across at least four meals** to maximize the anabolic response. The
ISSN position stand (Jäger et al., 2017) similarly puts a useful single dose at about
0.25 g/kg, or 20–40 g absolute.

How much this matters in practice: less than the total. Distribution is a refinement you
suggest once someone is reliably hitting their daily number. Telling a person who eats
90 g a day to spread it across four meals is solving the wrong problem.

### What gets over-claimed

- **"High protein damages your kidneys."** Not supported in healthy people at these
  intakes. With existing kidney disease it's a clinical question — a doctor's call.
- **The anabolic window.** Post-workout urgency has not held up well. Total daily intake
  dominates; timing is a small effect on top of it.
- **A hard per-meal ceiling.** The "only 30 g can be used" claim comes from studies of
  fast-digesting protein in isolation. Whole meals digest slower, which plausibly extends
  the usable window. Don't tell someone their large dinner was wasted.
- **Protein powder.** It's food. Convenient, unremarkable. No supplement recommendations
  beyond that.

---

## 2. Energy balance and rate of change

### Sizing the deficit

Aim for **0.5–1.0% of bodyweight per week**, with most people best served near 0.5–0.7%.
In practice that's roughly a 15–25% cut from maintenance. The floors in `safety.md`
override anything computed here.

For a surplus, slower still: **0.25–0.5% of bodyweight per week.** Gaining faster mostly
gains fat.

### Why ~1%/week is the ceiling

Garthe et al. (2011) randomized elite athletes to lose weight at **0.7%/week vs 1.4%/week**,
both lifting four times a week. Both groups lost fat. The slow group gained lean body mass
and increased 1RM strength; the fast group did not. Same destination, different body
composition on arrival.

This is a small study in trained athletes, so don't oversell it as a universal law. But it
points where everything else points: past about 1%/week, the extra weight coming off
increasingly isn't fat. That's why `safety.md` caps at 1.0%.

The framing that lands with people: going faster doesn't get you there sooner in any way
that matters. It gets you to a lighter version of the same body composition, usually with
worse training sessions and a harder time holding the result.

### The 3,500 kcal rule and why it fails

The heuristic — 3,500 kcal ≈ 1 lb of fat, or 7,700 kcal ≈ 1 kg — is fine for one thing:
sizing an initial deficit. A 500 kcal/day deficit implying about a pound a week is a
reasonable starting estimate.

It is wrong as a **prediction of what will happen over months**, and it's worth
understanding why. Hall and Chow (2013) put it directly: the flaw isn't the number, it's
the assumption that the deficit stays constant. As someone loses weight they get smaller,
so they burn less at rest and less in motion. The gap between intake and expenditure
narrows on its own, without anyone eating more. The static rule ignores this and therefore
predicts endless linear loss with no plateau.

Hall et al. (2011, *Lancet*) modeled the dynamics and found bodyweight responds to an
intake change with a **half-time of roughly one year** — most of the eventual change shows
up slowly, and a sustained deficit settles into a new steady weight rather than continuing
down forever.

What this means at the coaching desk:

- Use 3,500 kcal/lb to **size** a deficit. Never to **forecast** month six.
- A plateau after several months is the expected behavior of the system, not a personal
  failure and not evidence of a "broken metabolism."
- If a user's loss is slower than the arithmetic predicted, the arithmetic was wrong before
  they were.

---

## 3. Why the scale lies day to day

**This is the single most repeated message in this pack. It is not a disclaimer — it's the
main finding, and users need it more than once.**

Body fat changes slowly. Bodyweight changes fast, because most of what the scale measures
day to day isn't fat:

- **Water.** The largest source of noise by far, and it moves with everything below.
- **Sodium.** A high-salt meal can hold multiple pounds of water for a day or two. The
  effect is real, transient, and has nothing to do with fat.
- **Glycogen.** Stored carbohydrate binds water with it — roughly 3 g of water per gram of
  glycogen. This is why cutting carbs produces a dramatic first week and why reintroducing
  them produces an alarming "gain" that is nothing of the kind.
- **Gut contents.** Food and waste in transit have weight. Fiber intake, meal timing, and
  bowel regularity all move the number.
- **The menstrual cycle.** Fluid retention varies predictably across the cycle for many
  people, commonly by several pounds, typically peaking in the late luteal phase. If a user
  menstruates, compare weeks to the same phase of the previous cycle rather than reading a
  premenstrual week as a stall. This varies a lot between individuals; the pattern in their
  own data beats any textbook curve.
- **Training.** A hard or novel session causes muscle damage, inflammation, and fluid
  retention. The scale can go *up* after the training that's working.

None of these are fat. All of them are larger, on any given morning, than a day's worth of
actual fat change.

### The consequence

**A 7-day rolling average is the only honest read.** A single morning weight carries so
much noise that it contains almost no information about fat mass. Seven days of daily
weights averaged together cancels most of it.

Rules for using it:

- Compare **this week's average to last week's average.** Never today to yesterday.
- Give any change **two to three weeks** before acting. One flat week is not a plateau; it
  is a normal week.
- Daily weighing is fine and actually helps — it feeds the average. Reacting to daily
  weights is what causes harm.
- When a user reports a single day's number with alarm, respond to the trend, and say why.

If someone finds daily weighing distressing, drop the frequency or drop it entirely.
Adherence to a plan they can tolerate beats a slightly cleaner dataset. See the disordered
eating section of `safety.md` — the pattern-watch signals there override everything in this
section.

---

## 4. TDEE: estimation vs. observation

### Start with an equation, then abandon it

Use **Mifflin-St Jeor** (Mifflin et al., 1990) for resting metabolic rate:

```
RMR (men)   = 10 × weight(kg) + 6.25 × height(cm) − 5 × age(y) + 5
RMR (women) = 10 × weight(kg) + 6.25 × height(cm) − 5 × age(y) − 161
```

Then multiply by an activity factor (roughly 1.2 sedentary to 1.7 very active) to get TDEE.

Mifflin-St Jeor was derived from 498 healthy adults and is generally the most reliable of
the common predictive equations. It's also, on the original regression, R² = 0.71 — it
explains most of the variance between people and misses a meaningful chunk. Individuals
land well off the prediction in both directions, and the activity multiplier is a cruder
guess than the equation it multiplies.

So: the equation is a **starting point for week one**, and nothing more.

### Observation beats prediction

After two to three weeks of logged intake and daily weights, back-calculate:

```
observed maintenance = average daily intake − (weekly weight change in kg × 7700 / 7)
```

Weight change is **signed**: negative when losing, positive when gaining. So someone eating
2,000 kcal and losing 0.5 kg/week has an observed maintenance of 2,000 − (−550) = 2,550.
Getting this sign backwards produces a target that makes the problem worse, so sanity-check
the direction: **losing weight always implies maintenance above current intake.** Use 3500
instead of 7700 if working in pounds.

This uses that person's actual body in their actual life, including whatever their activity
multiplier really is. It beats any equation, and the gap is often several hundred calories.
Once you have three or more weeks of clean data, the observed number is the real target and
the equation should be discarded, not averaged in.

Two conditions on trusting it: intake logging has to be roughly honest, and the weight
change has to come from **rolling averages** (Section 3), not endpoint weights.

`scripts/trend_report.py` does this calculation. Per `CLAUDE.md`, cite its output — don't
do this arithmetic yourself.

### Adaptive thermogenesis

Energy expenditure falls during weight loss by more than body size alone accounts for. Part
is simply being a smaller body; part is a genuine downregulation — reduced non-exercise
movement, hormonal shifts, more efficient muscle.

**How large and how persistent this is remains genuinely contested, and you should say so
rather than picking a side.** The best-known data, Fothergill et al. (2016), followed
*Biggest Loser* contestants and found resting metabolic rate still suppressed six years
later despite substantial weight regain. It was disputed on publication, and notably one of
its own authors later published a reinterpretation (Hall, 2022) arguing the effect had been
overstated by the original analysis. That's an unusually honest scientific record, and it
means the honest coaching answer is a range, not a number.

What's safe to tell a user:

- Expenditure does fall during a deficit, by more than size alone predicts. This is real.
- The magnitude is uncertain and the extreme figures come from extreme interventions —
  30 weeks of severe restriction and heavy exercise is not a normal diet.
- Practically it doesn't change the plan. Their **observed** maintenance already contains
  whatever adaptation they have. Recalculate it periodically and it stays current.
- It is not permanent metabolic damage, and it is not a reason to think fat loss is
  impossible for them.

---

## 5. Diet breaks and refeeds

**Definitions.** A *diet break* is one to two weeks eating at maintenance. A *refeed* is a
day or two of higher intake, usually from carbohydrate, inside a continuing deficit.

**Honest summary: the evidence is genuinely mixed, and it splits by population.**

**The supportive result.** Byrne et al. (2018), the MATADOR study, ran 51 men with obesity
through either continuous restriction or intermittent restriction — 2-week diet blocks
alternating with 2-week maintenance blocks. Intermittent restriction produced greater
weight and fat loss for the same number of restricted weeks, and blunted the drop in
resting energy expenditure. A well-designed trial with a clear positive result.

**The null result.** Peos et al. (2021), the ICECAP trial, ran the same idea in
resistance-trained adults over 12 weeks of moderate restriction. **No significant
difference** between continuous and intermittent groups in fat loss, fat-free mass,
strength, endurance, or resting energy expenditure. A pre-specified secondary analysis
found the 1-week break produced small increases in bodyweight, fat-free mass, and resting
energy expenditure, and a measurable improvement in muscle endurance — but no fat-loss
advantage.

**How to read the split.** These populations differ in ways that plausibly matter: degree
of obesity, deficit severity, training status, and study length. MATADOR ran 30 weeks;
ICECAP ran 15. It's reasonable to think breaks help more with larger deficits sustained
longer, and matter less for a moderate 12-week cut in a trained person. That's a
hypothesis, not a finding — say it as one.

**What to actually do:**

- Don't sell a diet break as a fat-loss accelerator. That's the claim the evidence does not
  reliably support.
- Do offer one as a **psychological and adherence tool** — that's where the honest case
  sits. A person who takes a planned week at maintenance and returns beats one who quits in
  week nine.
- Expect the scale to rise a few pounds from glycogen and water (Section 3) and warn the
  user in advance, or the bounce will read as failure.
- Refeeds are fine if the person likes them. Frame as preference, not physiology.
- **Breaks are eaten at maintenance, not without limit** — and a break is a planned part of
  the plan, not a lapse. Nothing is being "cheated on" or "made up for."

---

## 6. Fiber, and why macro composition matters less than adherence

### Fiber

**Target 25–30 g/day.** Reynolds et al. (2019) pooled 185 prospective studies and 58
trials — around 135 million person-years — and found intakes of **25–29 g daily** adequate,
with dose-response data suggesting further benefit above 30 g.

This is observational for the long-term health outcomes, so causal strength is limited. But
it's a large, consistent body of evidence and the intervention is low-risk. For this tool's
purposes there's also a nearer-term reason: fiber increases satiety, which makes a deficit
easier to hold — and per Section 7, that's the thing that determines the outcome.

If someone is increasing fiber substantially, ramp it over a couple of weeks and increase
fluids. And expect Section 3 to apply: more fiber means more gut contents, which shows up
on the scale as weight that isn't fat.

### Macro composition

**Beyond hitting protein and fiber, the carbohydrate-to-fat split barely matters for fat
loss.** Set it by preference — what the person likes eating, what fits their culture and
schedule, what keeps them full.

The ISSN position stand on diets and body composition (Aragon et al., 2017) reviewed diet
types and eating styles across the literature and repeatedly lands on the same place:
adherence to an energy deficit governs the outcome, not macronutrient architecture.

The cleanest single trial is Gardner et al. (2018), DIETFITS: 609 adults randomized to a
healthy low-fat or healthy low-carbohydrate diet for 12 months, with real support — 22
group sessions with health educators. **No significant difference in weight change between
groups.** The study also tested whether genotype pattern or baseline insulin secretion
predicted which diet suited whom. Neither did. The individual variation *within* each group
dwarfed the difference *between* them.

That last point is the useful one for a coach. When a user asks "is keto better for me?",
the answer isn't that keto is bad. It's that the question has been tested and the diet type
isn't what separates the people who succeed from the people who don't.

Do not sort foods into good and bad, clean and dirty, allowed and cheating. Beyond being
wrong, it's the framing that most reliably produces the restrict-and-rebound cycle
`safety.md` tells you to watch for.

---

## 7. Adherence

**Adherence is the strongest predictor of outcome. Not the diet, not the macros, not the
training split. Design for it first and optimize second.**

Dansinger et al. (2005) randomized people to Atkins, Ornish, Weight Watchers, or Zone —
four diets with sharply different rules. One-year weight loss was comparable across all
four. Within every group, **adherence predicted results**; overall adherence rates were low
regardless of assignment. Different roads, same finding: whether they followed it mattered,
which one it was didn't.

Gardner (2018) points the same way from a different angle, and a secondary analysis of that
trial found dietary adherence associated with weight-loss success in both arms.

### What this means for how you coach

**An unfollowed plan isn't a failed plan. It's the wrong plan.** This is the reframe that
matters, and it changes what you do next. When someone hasn't hit their targets, the
diagnostic question is never "why aren't you trying harder?" It's "what about this plan
doesn't fit your life?"

Usually the answer is concrete and fixable: the target was too aggressive, the food doesn't
suit them, the schedule assumed a life they don't lead, the protein number requires cooking
they have no time for.

Practical rules:

- **Cap the ceiling before lowering the floor.** When someone stalls, reining in the highest
  days almost always beats cutting an already-hard target — more effective and more
  survivable.
- **A 90%-adhered moderate deficit beats a 50%-adhered aggressive one.** Reach for the
  smallest deficit that still moves the number.
- **One change at a time.** Change three things and you learn nothing.
- **Adherence data is information, not a character assessment.** "You hit protein 4 of 7
  days" is a fact about a plan, not a verdict on a person.
- **Never respond to poor adherence by tightening targets.** A plan too hard to follow will
  not be followed harder.
- **Sustainability is a design constraint.** Ask what they'd do for a year. Anything they
  wouldn't is worth less than it looks on paper.

---

## What this document does not cover

This is general nutrition guidance for healthy adults who want to change body composition.
It is not clinical practice, and the boundary matters.

Outside this tool's scope entirely:

- Any medical condition and any nutrition interacting with one — diabetes, thyroid, kidney
  or liver disease, cardiovascular disease, GI disorders, PCOS
- Bloodwork. This tool does not interpret lab values, ever
- Medications, including how any drug interacts with intake or bodyweight
- Pregnancy, nursing, fertility nutrition, and anyone under 18
- Eating disorders and disordered eating, which need clinical treatment — see `safety.md`
- Food allergies, intolerances, and clinical elimination protocols
- Micronutrient status and supplementation beyond noting protein powder is food
- Competition weight-cutting, dehydration protocols, physique peaking
- Post-surgical nutrition, including bariatric

### Refer to a registered dietitian when

- Any condition above is present, or the user takes any regular medication
- The user is under 18, pregnant, or nursing
- BMI is under 18.5, or any signal from the disordered eating section of `safety.md` appears
- Weight is changing in a way the data doesn't explain
- The user has a real medical question — "should I be worried about X?" is a doctor's
  question
- Something doesn't add up and you're reaching for a speculative explanation

"Nutritionist" is not a protected term in most places; **registered dietitian** (RD/RDN, or
dietitian in the UK) is. Point users to the protected title.

Say the referral in one sentence, say who to ask, and stop.

---

## References

All verified against the source publication.
1. Jäger R, Kerksick CM, Campbell BI, et al. **International Society of Sports Nutrition
   Position Stand: protein and exercise.** *Journal of the International Society of Sports
   Nutrition.* 2017;14:20. doi:10.1186/s12970-017-0177-8
2. Aragon AA, Schoenfeld BJ, Wildman R, et al. **International Society of Sports Nutrition
   position stand: diets and body composition.** *Journal of the International Society of
   Sports Nutrition.* 2017;14:16. doi:10.1186/s12970-017-0174-y
3. Morton RW, Murphy KT, McKellar SR, et al. **A systematic review, meta-analysis and
   meta-regression of the effect of protein supplementation on resistance training-induced
   gains in muscle mass and strength in healthy adults.** *British Journal of Sports
   Medicine.* 2018;52(6):376–384. doi:10.1136/bjsports-2017-097608
   *(A correction was published in 2020; the primary conclusion was unchanged.)*
4. Helms ER, Zinn C, Rowlands DS, Brown SR. **A systematic review of dietary protein during
   caloric restriction in resistance trained lean athletes: a case for higher intakes.**
   *International Journal of Sport Nutrition and Exercise Metabolism.* 2014;24(2):127–138.
5. Garthe I, Raastad T, Refsnes PE, Koivisto A, Sundgot-Borgen J. **Effect of two different
   weight-loss rates on body composition and strength and power-related performance in elite
   athletes.** *International Journal of Sport Nutrition and Exercise Metabolism.*
   2011;21(2):97–104. doi:10.1123/ijsnem.21.2.97
6. Mifflin MD, St Jeor ST, Hill LA, Scott BJ, Daugherty SA, Koh YO. **A new predictive
   equation for resting energy expenditure in healthy individuals.** *American Journal of
   Clinical Nutrition.* 1990;51(2):241–247.
7. Schoenfeld BJ, Aragon AA. **How much protein can the body use in a single meal for
   muscle-building? Implications for daily protein distribution.** *Journal of the
   International Society of Sports Nutrition.* 2018;15:10. doi:10.1186/s12970-018-0215-1
8. Hall KD, Chow CC. **Why is the 3500 kcal per pound weight loss rule wrong?**
   *International Journal of Obesity.* 2013;37(12):1614.
9. Hall KD, Sacks G, Chandramohan D, et al. **Quantification of the effect of energy
   imbalance on bodyweight.** *The Lancet.* 2011;378(9793):826–837.
   doi:10.1016/S0140-6736(11)60812-X
10. Byrne NM, Sainsbury A, King NA, Hills AP, Wood RE. **Intermittent energy restriction
    improves weight loss efficiency in obese men: the MATADOR study.** *International Journal
    of Obesity.* 2018;42(2):129–138.
11. Peos JJ, Helms ER, Fournier PA, et al. **Continuous versus intermittent dieting for fat
    loss and fat-free mass retention in resistance-trained adults: the ICECAP trial.**
    *Medicine & Science in Sports & Exercise.* 2021;53(8):1685–1698.
    doi:10.1249/MSS.0000000000002636
12. Peos JJ, Helms ER, Fournier PA, et al. **A 1-week diet break improves muscle endurance
    during an intermittent dieting regime in adult athletes: a pre-specified secondary
    analysis of the ICECAP trial.** *PLOS ONE.* 2021;16(2):e0247292.
    doi:10.1371/journal.pone.0247292
13. Fothergill E, Guo J, Howard L, et al. **Persistent metabolic adaptation 6 years after
    "The Biggest Loser" competition.** *Obesity.* 2016;24(8):1612–1619.
    doi:10.1002/oby.21538 *(Contested — see reference 14.)*
14. Hall KD. **Energy compensation and metabolic adaptation: "The Biggest Loser" study
    reinterpreted.** *Obesity.* 2022;30(1):11–13. doi:10.1002/oby.23308
15. Reynolds A, Mann J, Cummings J, Winter N, Mete E, Te Morenga L. **Carbohydrate quality
    and human health: a series of systematic reviews and meta-analyses.** *The Lancet.*
    2019;393(10170):434–445. doi:10.1016/S0140-6736(18)31809-9
16. Dansinger ML, Gleason JA, Griffith JL, Selker HP, Schaefer EJ. **Comparison of the
    Atkins, Ornish, Weight Watchers, and Zone diets for weight loss and heart disease risk
    reduction: a randomized trial.** *JAMA.* 2005;293(1):43–53. doi:10.1001/jama.293.1.43
17. Gardner CD, Trepanowski JF, Del Gobbo LC, et al. **Effect of low-fat vs low-carbohydrate
    diet on 12-month weight loss in overweight adults and the association with genotype
    pattern or insulin secretion: the DIETFITS randomized clinical trial.** *JAMA.*
    2018;319(7):667–679. doi:10.1001/jama.2018.0245
