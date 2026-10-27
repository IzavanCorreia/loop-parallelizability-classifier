"""Runs one model on one setting for the given repetitions; finished folds are skipped, so an
interrupted run can simply be started again.

  python run.py --model distilbert --setting hybrid --reps 0 1 2
  python run.py --model lr --setting syn2real --reps 0 1 2
  python run.py --model dnn --setting real --reps 0 --smoke     (2 folds, tiny training set)
"""

import argparse
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402

MODELS = ["lr", "svm", "dnn", "cnn", "ngram", "distilbert"]
SETTINGS = ["hybrid", "syn2real", "real"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", choices=MODELS, required=True)
    ap.add_argument("--setting", choices=SETTINGS, required=True)
    ap.add_argument("--reps", type=int, nargs="+", default=[0, 1, 2])
    ap.add_argument("--folds", type=int, nargs="*", default=None)
    ap.add_argument("--smoke", action="store_true", help="2 folds on small subsets, results under raw_smoke")
    args = ap.parse_args()
    if args.smoke:
        common.RESULTS = os.path.join(common.RESULTS, "smoke")
    items = common.load_setting(args.setting)
    codes = np.array([it["code"] for it in items], dtype=object)
    y = np.array([it["label"] for it in items])
    for rep in args.reps:
        common.save_folds(items, args.setting, rep)
        for fold, tr, va, te in common.splits(items, args.setting, rep):
            if args.folds is not None and fold not in args.folds:
                continue
            if args.smoke and fold > 1:
                break
            if os.path.exists(common.result_path(args.setting, args.model, rep, fold)):
                continue
            if args.smoke:
                rng = np.random.default_rng(0)
                tr = rng.choice(tr, min(len(tr), 400), replace=False)
                va = rng.choice(va, min(len(va), 100), replace=False)
            seed = 1000 * rep + fold
            common.set_seed(seed)
            t = time.time()
            extra = None
            if args.model == "distilbert":
                import bert
                s_va, s_te, info, extra = bert.run(codes[tr], y[tr], codes[va], y[va], codes[te], seed)
            else:
                import classic
                s_va, s_te, info = classic.run(args.model, codes[tr], y[tr], codes[va], y[va], codes[te], seed)
            info.update({"seed": seed, "n_train": len(tr), "n_val": len(va), "n_test": len(te)})
            common.save_result(args.setting, args.model, rep, fold, items, va, te, s_va, s_te, info, extra)
            pred = (s_te > info["threshold"]).astype(int)
            yt = y[te]
            acc = (pred == yt).mean()
            fpr = ((pred == 1) & (yt == 0)).sum() / max(1, (yt == 0).sum())
            print(f"[{args.model} {args.setting} rep{rep} fold{fold}] acc={acc*100:.2f}% FPR={fpr*100:.2f}% "
                  f"({time.time() - t:.0f}s)", flush=True)


if __name__ == "__main__":
    main()
