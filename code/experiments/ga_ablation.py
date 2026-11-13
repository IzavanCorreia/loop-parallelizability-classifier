"""Ablation of the genetic algorithm (GA_ABLATION_PROTOCOL.md): DistilBERT trained on the random-search pairs
against DistilBERT trained on the GA pairs, same protocol as the synthetic-to-real scenario.

  python ga_ablation.py --arm random      trains 3 models on data/synthetic_random (finished runs are skipped)
  python ga_ablation.py --arm ga          scores the 3 stage-1 models (trained on the GA pairs) again

Every model is scored on the 340 real-world loops (test) and on the 8,000 samples of the other arm (extra).
Results: results/raw/ga_ablation/<arm>/rep<r>_fold0.npz
"""

import argparse
import csv
import os
import sys
import time

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bert  # noqa: E402
import common  # noqa: E402

SETTING = "ga_ablation"
CKPT = os.environ.get("TWO_STAGE_CKPT", os.path.join(common.RESULTS, "two_stage_ckpt"))


def load_pairs(folder, prefix):
    P = common._load(os.path.join(common.DATA, folder, "Parallelizable_codes.py"))
    U = common._load(os.path.join(common.DATA, folder, "Undefined_codes.py"))
    meta = list(csv.DictReader(open(os.path.join(common.DATA, folder, "metadata.csv"), encoding="utf-8")))
    items = []
    for i, (p, u, m) in enumerate(zip(P, U, meta)):
        for label, code, tag in ((1, p, "P"), (0, u, "U")):
            items.append({"id": f"{prefix}-{tag}-{i + 1}", "code": code, "label": label, "source": "synthetic",
                          "group": f"{prefix}-{i + 1}", "category": f"family {m['family']}"})
    return items


def arm_items(arm):
    """Synthetic samples of the arm followed by the real-world loops, as in the syn2real setting."""
    syn = common.load_synthetic() if arm == "ga" else load_pairs("synthetic_random", "rnd")
    return syn + common.load_real()


def other_items(arm):
    return load_pairs("synthetic_random", "rnd") if arm == "ga" else common.load_synthetic()


@torch.no_grad()
def score(state, codes):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = bert.AutoModelForSequenceClassification.from_pretrained(bert.MODEL_NAME, num_labels=2)
    model.load_state_dict(state)
    model = model.to(device)
    s, _ = bert._predict(model, bert._loader(codes, np.zeros(len(codes), dtype=int), False), device)
    del model
    if device == "cuda":
        torch.cuda.empty_cache()
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", choices=["random", "ga"], required=True)
    ap.add_argument("--reps", type=int, nargs="+", default=[0, 1, 2])
    args = ap.parse_args()
    items = arm_items(args.arm)
    codes = np.array([it["code"] for it in items], dtype=object)
    y = np.array([it["label"] for it in items])
    other = other_items(args.arm)
    o_codes = np.array([it["code"] for it in other], dtype=object)
    o_y = np.array([it["label"] for it in other])
    o_ids = np.array([it["id"] for it in other])
    for rep in args.reps:
        path = common.result_path(SETTING, args.arm, rep, 0)
        if os.path.exists(path):
            continue
        _, tr, va, te = next(common.splits(items, "syn2real", rep))
        seed = 1000 * rep
        common.set_seed(seed)
        t = time.time()
        if args.arm == "random":
            s_va, s_te, info, extra = bert.run(codes[tr], y[tr], codes[va], y[va], codes[te], seed, codes_extra=o_codes)
            extra["other_score"] = extra.pop("extra_score")
        else:
            state = torch.load(os.path.join(CKPT, f"stage1_rep{rep}.pt"), map_location="cpu", weights_only=True)
            s_va, s_te = score(state, codes[va]), score(state, codes[te])
            info = {"threshold": 0.5, "source": f"stage1_rep{rep}.pt (scored again)"}
            extra = {"other_score": score(state, o_codes)}
        extra.update({"other_y": o_y, "other_ids": o_ids,
                      "train_ids": np.array([items[i]["id"] for i in tr])})
        info.update({"seed": seed, "n_train": len(tr), "n_val": len(va), "n_test": len(te), "arm": args.arm})
        common.save_result(SETTING, args.arm, rep, 0, items, va, te, s_va, s_te, info, extra)
        acc = ((s_te > 0.5).astype(int) == y[te]).mean()
        oacc = ((extra["other_score"] > 0.5).astype(int) == o_y).mean()
        print(f"[{args.arm} rep{rep}] real acc={acc*100:.2f}% other-arm acc={oacc*100:.2f}% ({time.time() - t:.0f}s)",
              flush=True)


if __name__ == "__main__":
    main()
