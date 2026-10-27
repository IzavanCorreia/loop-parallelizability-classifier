"""Data loading, fold assignment and result storage shared by all experiments.

Positive class = Parallelizable (label 1). The false positive rate is the fraction of Undefined
samples predicted as Parallelizable.

Settings
  hybrid    8,000 synthetic + 340 real samples, stratified group 10-fold CV (strata = label x source,
            groups = synthetic minimal pair or real duplicate group)
  syn2real  train on the 8,000 synthetic samples, test on the 340 real samples
  real      340 real samples only, stratified group 10-fold CV
Every repetition r uses its own partition (seed r) and its own model initialisation; all models use
exactly the same partitions, so the comparisons are paired.
"""

import csv
import json
import os
import re

import numpy as np
from sklearn.model_selection import StratifiedGroupKFold

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
DATA = os.path.join(ROOT, "data")
RESULTS = os.path.join(ROOT, "results")
SEP = "=" * 40
N_FOLDS = 10
VAL_SPLITS = 5          # 1 of 5 group-stratified splits of the training portion = 20% validation


def _load(path):
    txt = open(path, encoding="utf-8").read()
    return [re.sub(r"^Code \d+:\s*\n", "", c.strip()) for c in txt.split(SEP) if c.strip()]


def load_synthetic():
    P = _load(os.path.join(DATA, "synthetic", "Parallelizable_codes.py"))
    U = _load(os.path.join(DATA, "synthetic", "Undefined_codes.py"))
    meta = list(csv.DictReader(open(os.path.join(DATA, "synthetic", "metadata.csv"), encoding="utf-8")))
    items = []
    for i, (p, u, m) in enumerate(zip(P, U, meta)):
        for label, code, tag in ((1, p, "P"), (0, u, "U")):
            items.append({"id": f"syn-{tag}-{i + 1}", "code": code, "label": label, "source": "synthetic",
                          "group": f"syn-{i + 1}", "category": f"family {m['family']}"})
    return items


def load_real():
    meta = list(csv.DictReader(open(os.path.join(DATA, "real", "metadata.csv"), encoding="utf-8")))
    cats = {(r["class"], r["original_class"], r["original_index"]): r["category"]
            for r in csv.DictReader(open(os.path.join(ROOT, "results", "real_dependence_types.csv"), encoding="utf-8"))}
    codes = {cls: _load(os.path.join(DATA, "real", f"{cls}_codes.py")) for cls in ("Parallelizable", "Undefined")}
    items = []
    for m in meta:
        cls, idx = m["class"], int(m["index"])
        items.append({"id": f"real-{cls[0]}-{idx}", "code": codes[cls][idx - 1],
                      "label": 1 if cls == "Parallelizable" else 0, "source": "real",
                      "group": f"real-{m['group']}",
                      "category": cats.get((cls, m["original_class"], m["original_index"]), "")})
    return items


def load_setting(setting):
    syn, real = load_synthetic(), load_real()
    if setting == "hybrid":
        return syn + real
    if setting == "real":
        return real
    if setting == "syn2real":
        return syn + real
    raise ValueError(setting)


def _strata(items):
    return np.array([it["label"] * 2 + (it["source"] == "real") for it in items])


def _groups(items):
    return np.array([it["group"] for it in items])


def splits(items, setting, rep):
    """Yields (fold, train_idx, val_idx, test_idx) for a repetition."""
    idx_all = np.arange(len(items))
    if setting == "syn2real":
        syn = idx_all[[it["source"] == "synthetic" for it in items]]
        real = idx_all[[it["source"] == "real" for it in items]]
        tr, va = _val_split([items[i] for i in syn], rep)
        yield 0, syn[tr], syn[va], real
        return
    strata, groups = _strata(items), _groups(items)
    outer = StratifiedGroupKFold(n_splits=N_FOLDS, shuffle=True, random_state=rep)
    for fold, (trv, te) in enumerate(outer.split(idx_all, strata, groups)):
        tr, va = _val_split([items[i] for i in trv], rep * 100 + fold)
        yield fold, trv[tr], trv[va], te


def _val_split(items, seed):
    inner = StratifiedGroupKFold(n_splits=VAL_SPLITS, shuffle=True, random_state=seed)
    tr, va = next(inner.split(np.zeros(len(items)), _strata(items), _groups(items)))
    return tr, va


def save_folds(items, setting, rep):
    path = os.path.join(RESULTS, "folds", f"{setting}_rep{rep}.csv")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path):
        return
    rows = []
    for fold, tr, va, te in splits(items, setting, rep):
        for part, idx in (("train", tr), ("val", va), ("test", te)):
            rows += [{"id": items[i]["id"], "fold": fold, "part": part} for i in idx]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["id", "fold", "part"])
        w.writeheader()
        w.writerows(rows)


def result_path(setting, model, rep, fold):
    return os.path.join(RESULTS, "raw", setting, model, f"rep{rep}_fold{fold}.npz")


def save_result(setting, model, rep, fold, items, val_idx, test_idx, val_scores, test_scores, info, extra=None):
    """Scores are P(Parallelizable) (or a monotone score, e.g. an SVM decision value)."""
    path = result_path(setting, model, rep, fold)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    arrays = {
        "val_ids": np.array([items[i]["id"] for i in val_idx]),
        "val_y": np.array([items[i]["label"] for i in val_idx]),
        "val_score": np.asarray(val_scores, dtype=np.float64),
        "test_ids": np.array([items[i]["id"] for i in test_idx]),
        "test_y": np.array([items[i]["label"] for i in test_idx]),
        "test_score": np.asarray(test_scores, dtype=np.float64),
        "info": np.array(json.dumps(info)),
    }
    if extra:
        arrays.update(extra)
    np.savez_compressed(path, **arrays)


def set_seed(seed):
    import random
    random.seed(seed)
    np.random.seed(seed)
    try:
        import torch
        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
    except ImportError:
        pass
