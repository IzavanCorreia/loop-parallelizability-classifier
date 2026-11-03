"""Two-stage training: DistilBERT fine-tuned on the synthetic pairs, then on the real-world loops.

Stage 1 repeats the syn2real training (one model per repetition, synthetic samples only, so no real
loop is seen). Stage 2 runs inside each real-only fold, with the partitions, hyperparameters and seeds
of the real-only setting. The two arms differ only in the starting weights:
  scratch     the pre-trained DistilBERT (the real-only setting)
  pretrained  the stage-1 weights of the same repetition
Each arm runs with 10%, 25%, 50% and 100% of the real training loops, drawn by group and class, nested
and equal in both arms; validation and test loops do not change. Every run also scores the 1,600
synthetic validation samples of stage 1, which that stage used only for early stopping.
The protocol was fixed before the runs (TWO_STAGE_PROTOCOL.md). Finished runs are skipped.

  python two_stage.py --stage 1
  python two_stage.py --stage 2
  python two_stage.py --stage 2 --arms scratch --budgets 100 --reps 0 --folds 0     (one run)
"""

import argparse
import os
import sys
import time

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bert  # noqa: E402
import common  # noqa: E402

SETTING = "two_stage"
BUDGETS = [10, 25, 50, 100]
ARMS = ["scratch", "pretrained"]
CKPT = os.environ.get("TWO_STAGE_CKPT", os.path.join(common.RESULTS, "two_stage_ckpt"))


def ckpt_path(rep):
    return os.path.join(CKPT, f"stage1_rep{rep}.pt")


def synthetic_split(rep):
    """The items of the syn2real setting and its training, validation and test indices for a repetition."""
    items = common.load_setting("syn2real")
    _, tr, va, te = next(common.splits(items, "syn2real", rep))
    return items, tr, va, te


def budget_subset(items, tr, pct, rep, fold):
    """pct% of the training indices, drawn by group within each class; nested across budgets."""
    if pct == 100:
        return tr
    rng = np.random.RandomState(100000 + 1000 * rep + fold)
    keep = []
    for label in (0, 1):
        idx = [i for i in tr if items[i]["label"] == label]
        groups = sorted({items[i]["group"] for i in idx})
        rng.shuffle(groups)
        target, chosen = round(len(idx) * pct / 100), []
        for g in groups:
            if len(chosen) >= target:
                break
            chosen += [i for i in idx if items[i]["group"] == g]
        keep += chosen
    return np.array(sorted(keep))


def stage1(reps):
    os.makedirs(CKPT, exist_ok=True)
    for rep in reps:
        if os.path.exists(ckpt_path(rep)) and os.path.exists(common.result_path(SETTING, "stage1", rep, 0)):
            continue
        items, tr, va, te = synthetic_split(rep)
        codes = np.array([it["code"] for it in items], dtype=object)
        y = np.array([it["label"] for it in items])
        seed = 1000 * rep
        common.set_seed(seed)
        t = time.time()
        s_va, s_te, info, extra = bert.run(codes[tr], y[tr], codes[va], y[va], codes[te], seed, return_state=True)
        torch.save(extra.pop("state"), ckpt_path(rep))
        info.update({"seed": seed, "n_train": len(tr), "n_val": len(va), "n_test": len(te)})
        common.save_result(SETTING, "stage1", rep, 0, items, va, te, s_va, s_te, info, extra)
        acc = ((s_te > 0.5).astype(int) == y[te]).mean()
        print(f"[stage1 rep{rep}] real acc={acc*100:.2f}% best_epoch={info['best_epoch']} ({time.time() - t:.0f}s)",
              flush=True)


def stage2(reps, folds, arms, budgets):
    items = common.load_setting("real")
    codes = np.array([it["code"] for it in items], dtype=object)
    y = np.array([it["label"] for it in items])
    for rep in reps:
        syn_items, _, syn_va, _ = synthetic_split(rep)
        pair_codes = [syn_items[i]["code"] for i in syn_va]
        pair_y = np.array([syn_items[i]["label"] for i in syn_va])
        state = None
        for fold, tr, va, te in common.splits(items, "real", rep):
            if folds is not None and fold not in folds:
                continue
            for pct in budgets:
                sub = budget_subset(items, tr, pct, rep, fold)
                for arm in arms:
                    model = f"{arm}_f{pct}"
                    if os.path.exists(common.result_path(SETTING, model, rep, fold)):
                        continue
                    if arm == "pretrained" and state is None:
                        state = torch.load(ckpt_path(rep), map_location="cpu", weights_only=True)
                    seed = 1000 * rep + fold
                    common.set_seed(seed)
                    t = time.time()
                    s_va, s_te, info, extra = bert.run(
                        codes[sub], y[sub], codes[va], y[va], codes[te], seed,
                        init_state=state if arm == "pretrained" else None, codes_extra=pair_codes)
                    extra["pairs_score"] = extra.pop("extra_score")
                    extra["pairs_y"] = pair_y
                    info.update({"seed": seed, "n_train": len(sub), "n_val": len(va), "n_test": len(te),
                                 "arm": arm, "budget": pct})
                    common.save_result(SETTING, model, rep, fold, items, va, te, s_va, s_te, info, extra)
                    yt, pred = y[te], (s_te > 0.5).astype(int)
                    acc = (pred == yt).mean()
                    fpr = ((pred == 1) & (yt == 0)).sum() / max(1, (yt == 0).sum())
                    pairs = ((extra["pairs_score"] > 0.5).astype(int) == pair_y).mean()
                    print(f"[{model} rep{rep} fold{fold}] n={len(sub)} acc={acc*100:.2f}% FPR={fpr*100:.2f}% "
                          f"pairs={pairs*100:.2f}% best={info['best_epoch']} ({time.time() - t:.0f}s)", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", type=int, choices=[1, 2], required=True)
    ap.add_argument("--reps", type=int, nargs="+", default=[0, 1, 2])
    ap.add_argument("--folds", type=int, nargs="*", default=None)
    ap.add_argument("--arms", nargs="+", default=ARMS, choices=ARMS)
    ap.add_argument("--budgets", type=int, nargs="+", default=BUDGETS)
    args = ap.parse_args()
    if args.stage == 1:
        stage1(args.reps)
    else:
        stage2(args.reps, args.folds, args.arms, args.budgets)


if __name__ == "__main__":
    main()
