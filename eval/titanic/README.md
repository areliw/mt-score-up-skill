# Titanic — a measurable exemplar for `ml-judgment`

The A/B scorecard shows skills *changing what a weak model answers*. This folder does
something stricter: it puts a **number** on one skill's judgment using real code on a
real dataset, so you can see the value isn't just rhetoric.

## The claim being tested

`ml-judgment`'s #1 anti-pattern:

> ทำ feature selection / preprocessing บนข้อมูลทั้งก้อน **ก่อน** แบ่ง train/test (data leakage)
> → metric สวยหลอก แล้วพังตอนเจอข้อมูลจริง

In plain terms: if you pick "the best features" while looking at the labels of your test
data, your score is inflated by information you won't have at deployment. The skill says
*do the selection inside cross-validation*. Does that actually matter, and by how much?

## The experiment

Same data (Kaggle Titanic `train.csv`), same model (logistic regression), same selector
(`SelectKBest`, k=20), same 5-fold CV. We bolt **200 pure-noise columns** onto the real
features so the leak has something to exploit. Then we change **exactly one thing**:

| variant | what it does | what `ml-judgment` says |
|---|---|---|
| **LEAKY** | `SelectKBest` fit on the **full** dataset, *then* cross-validate | the anti-pattern |
| **PROPER** | `SelectKBest` lives **inside** the pipeline, re-fit on each training fold only | the fix |

## The result

```
LEAKY  (select on full data, no ml-judgment): ROC-AUC = 0.850
PROPER (select inside CV folds, ml-judgment): ROC-AUC = 0.819
INFLATION fabricated by the leak           : +0.031 AUC
```

That **+0.031 AUC is fake**. It's the score you'd put in a slide deck or a paper, and it
would evaporate the moment the model met data whose labels the selector never got to peek
at. A reviewer who trusts the 0.850 deploys a model that actually performs at 0.819 (or
worse). The only difference between the honest number and the inflated one is *where the
feature selection happens* — precisely the judgment the skill encodes.

Reproduce it:

```bash
python leakage_demo.py path/to/train.csv      # or pass titanic.zip
```

(Seeds are fixed in the script, so a given environment is deterministic. The exact
numbers above are illustrative — `requirements.txt` pins only minimum versions, so a
different scikit-learn build may shift the digits slightly. What's stable is the
*direction and rough size*: PROPER comes out below LEAKY by a few hundredths of AUC.)

## Honest caveats

- The 200 synthetic noise columns **amplify** the leak to make it legible in one run. On a
  clean dataset with few features the inflation is smaller — but the leak **essentially
  always inflates the metric**, working against honest evaluation, and it grows with the
  number of features and preprocessing steps that touch the labels. The mechanism, not the
  exact magnitude, is the lesson.
- This demonstrates **one** of `ml-judgment`'s traps (selection leakage). It's the most
  measurable one; others (target leakage from future columns, train/serve skew) are real
  but harder to stage in 60 lines.
- A frontier model writing this pipeline would likely avoid the leak unprompted — matching
  the A/B finding that these skills are for **weaker models / non-experts**, who genuinely
  reach for the leaky version because it's the obvious one and it scores higher.

That last point is the whole thesis in one number: the leaky path is *seductive* (it looks
better), and the skill's job is to make you give up 0.031 of fake AUC for an honest model.
