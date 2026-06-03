#!/usr/bin/env python3
"""
Titanic leakage demo — a MEASURABLE exemplar for the `ml-judgment` skill.

ml-judgment's #1 anti-pattern: "ทำ feature selection / preprocessing บนข้อมูลทั้งก้อน
ก่อนแบ่ง train/test (data leakage) → metric สวยหลอก แล้วพังตอนเจอข้อมูลจริง."

This script proves that trap is real and puts a NUMBER on it. We take the same data,
the same model, the same k, and change ONLY one thing — whether feature selection
happens before the cross-validation split (LEAKY) or inside each fold (PROPER) —
and measure how much ROC-AUC the leak fabricates.

Why it bites hard here: we bolt 200 pure-noise columns onto the real Titanic
features. Selecting "the best 20 features" while peeking at the labels of the whole
dataset will pick noise columns that happen to correlate with the test-fold labels
too → the score is inflated by information that won't exist at deployment.

Usage:
    python leakage_demo.py [path/to/train.csv | path/to/titanic.zip]
    # default: looks for ./train.csv, else ./titanic.zip

Data: Kaggle "Titanic - Machine Learning from Disaster" (train.csv). Not committed
here (it's Kaggle's). Numbers below were produced with the seeds set in this file.
"""
from __future__ import annotations

import io
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline

SEED = 42
N_NOISE = 200          # junk columns — the leak's playground
K = 20                 # features the selector keeps
FOLDS = 5


def load_titanic(arg: str | None) -> pd.DataFrame:
    """Load train.csv from a csv path, a zip, or sensible defaults."""
    candidates = [arg] if arg else []
    candidates += ["train.csv", "titanic.zip"]
    for c in candidates:
        if not c:
            continue
        p = Path(c)
        if not p.exists():
            continue
        if p.suffix == ".zip":
            with zipfile.ZipFile(p) as z:
                with z.open("train.csv") as fh:
                    return pd.read_csv(io.BytesIO(fh.read()))
        return pd.read_csv(p)
    raise SystemExit(
        "train.csv not found. Pass a path: python leakage_demo.py path/to/train.csv "
        "(get it from kaggle.com/c/titanic)."
    )


def build_xy(df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    """Real Titanic signal + 200 noise columns. Target = Survived."""
    y = df["Survived"].to_numpy()
    real = pd.DataFrame(
        {
            "Pclass": df["Pclass"],
            "Age": df["Age"].fillna(df["Age"].median()),
            "Fare": df["Fare"].fillna(df["Fare"].median()),
            "SibSp": df["SibSp"],
            "Parch": df["Parch"],
            "Sex": (df["Sex"] == "male").astype(int),
        }
    ).to_numpy()
    rng = np.random.default_rng(SEED)
    noise = rng.standard_normal((len(df), N_NOISE))
    X = np.hstack([real, noise])
    return X, y


def main() -> int:
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    df = load_titanic(arg)
    X, y = build_xy(df)
    cv = StratifiedKFold(n_splits=FOLDS, shuffle=True, random_state=SEED)
    clf = lambda: LogisticRegression(max_iter=1000)

    # --- LEAKY: select features on the FULL data (labels of every fold are peeked) ---
    X_leaky = SelectKBest(f_classif, k=K).fit_transform(X, y)  # <-- the leak
    auc_leaky = cross_val_score(clf(), X_leaky, y, cv=cv, scoring="roc_auc").mean()

    # --- PROPER: selection lives INSIDE the pipeline → re-fit on each train fold only ---
    proper = Pipeline([("sel", SelectKBest(f_classif, k=K)), ("clf", clf())])
    auc_proper = cross_val_score(proper, X, y, cv=cv, scoring="roc_auc").mean()

    print(f"LEAKY  (select on full data, no ml-judgment): ROC-AUC = {auc_leaky:.3f}")
    print(f"PROPER (select inside CV folds, ml-judgment): ROC-AUC = {auc_proper:.3f}")
    print(f"INFLATION fabricated by the leak           : {auc_leaky - auc_proper:+.3f} AUC")
    print()
    print("The LEAKY number is what you'd report and brag about. The PROPER number is")
    print("what the model actually delivers on unseen data. The gap is pure illusion —")
    print("exactly the trap ml-judgment tells you to design out by selecting inside CV.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
