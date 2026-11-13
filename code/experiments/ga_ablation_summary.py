"""Summary of the ablation of the genetic algorithm (GA_ABLATION_PROTOCOL.md).

Writes results/tables/ga_ablation_data.csv (one row per arm: search and final-set statistics) and, when the model
runs exist, results/tables/ga_ablation_models.csv (one row per arm and repetition, plus mean and sd).
"""

import csv
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "generator"))
import common  # noqa: E402
from ga import normalise  # noqa: E402
from loopgen import NUM_EXPR  # noqa: E402

TABLES = os.path.join(common.RESULTS, "tables")
ARMS = {"ga": ("synthetic", "ga_log.csv"), "random": ("synthetic_random", "search_log.csv")}


def data_row(arm):
    folder, logname = ARMS[arm]
    d = os.path.join(common.DATA, folder)
    meta = list(csv.DictReader(open(os.path.join(d, "metadata.csv"), encoding="utf-8")))
    log = list(csv.DictReader(open(os.path.join(d, logname), encoding="utf-8")))
    P = common._load(os.path.join(d, "Parallelizable_codes.py"))
    sigs = set()
    for m in meta:
        g = list(map(int, m["genome"].split()))
        sigs.add((m["family"], m["form"], m["wrapper"], m["kind"], m["lang"], g[11] % len(NUM_EXPR), g[16] % 16))
    per_pop = [int(r["distinct_signatures"]) for r in log]
    valid = [float(r["valid_frac"]) for r in log]
    return {"arm": arm, "genomes": 510000, "valid_first": valid[0], "valid_last": valid[-1],
            "valid_mean": round(float(np.mean(valid)), 4), "valid_unique_seen": int(log[-1]["valid_unique_seen"]),
            "signatures_per_10k_first": per_pop[0], "signatures_per_10k_last": per_pop[-1],
            "signatures_per_10k_mean": round(float(np.mean(per_pop)), 1),
            "final_pairs": len(meta), "final_signatures": len(sigs),
            "final_structures": len({normalise(p) for p in P}),
            "final_minimality": round(float(np.mean([float(m["minimality"]) for m in meta])), 4),
            "final_tokens": round(float(np.mean([int(m["n_tokens"]) for m in meta])), 1),
            "final_forms": len({(m["family"], m["form"]) for m in meta}),
            "final_domains": len({m["domain"] for m in meta})}


def model_rows():
    rows = []
    for arm in ARMS:
        for rep in range(3):
            path = common.result_path("ga_ablation", arm, rep, 0)
            if not os.path.exists(path):
                return None
            z = np.load(path, allow_pickle=False)
            yt, st = z["test_y"], z["test_score"]
            pt = (st > 0.5).astype(int)
            oy, os_, oid = z["other_y"], z["other_score"], z["other_ids"]
            # samples of the other arm whose code is also in this model's training set are left out
            items = {it["id"]: it["code"] for it in common.load_synthetic()}
            items.update({f"rnd-{k}": v for k, v in _random_codes().items()})
            train_codes = {items[i] for i in z["train_ids"]}
            keep = np.array([items[i] not in train_codes for i in oid])
            po = (os_ > 0.5).astype(int)
            ok = (po == oy) & keep
            # pair accuracy: both programs of a pair right (pairs with a left-out sample are skipped)
            pair_ok, pair_n = 0, 0
            groups = {}
            for i, sid in enumerate(oid):
                groups.setdefault(sid.rsplit("-", 2)[0] + "-" + sid.rsplit("-", 1)[1], []).append(i)
            for idx in groups.values():
                if len(idx) == 2 and keep[idx].all():
                    pair_n += 1
                    pair_ok += int((po[idx] == oy[idx]).all())
            row = {"arm": arm, "rep": rep,
                   "real_acc": 100 * (pt == yt).mean(),
                   "real_fpr": 100 * ((pt == 1) & (yt == 0)).sum() / (yt == 0).sum(),
                   "other_acc": 100 * ok.sum() / keep.sum(),
                   "other_fpr": 100 * ((po == 1) & (oy == 0) & keep).sum() / ((oy == 0) & keep).sum(),
                   "other_pair_acc": 100 * pair_ok / pair_n, "other_left_out": int((~keep).sum()),
                   "val_acc": 100 * ((z["val_score"] > 0.5).astype(int) == z["val_y"]).mean()}
            if arm == "ga":
                s1 = np.load(common.result_path("two_stage", "stage1", rep, 0))
                row["check_max_abs_diff_stage1"] = float(np.abs(s1["test_score"] - st).max())
                s2 = np.load(common.result_path("syn2real", "distilbert", rep, 0))
                row["syn2real_run_real_acc"] = 100 * ((s2["test_score"] > 0.5).astype(int) == s2["test_y"]).mean()
            rows.append(row)
    for arm in ARMS:
        sub = [r for r in rows if r["arm"] == arm]
        for stat, f in (("mean", np.mean), ("sd", lambda v: np.std(v, ddof=1))):
            rows.append({"arm": arm, "rep": stat, **{k: round(float(f([r[k] for r in sub])), 4)
                                                      for k in sub[0] if k not in ("arm", "rep")}})
    return rows


_RND = None


def _random_codes():
    global _RND
    if _RND is None:
        d = os.path.join(common.DATA, "synthetic_random")
        P = common._load(os.path.join(d, "Parallelizable_codes.py"))
        U = common._load(os.path.join(d, "Undefined_codes.py"))
        _RND = {}
        for i, (p, u) in enumerate(zip(P, U), 1):
            _RND[f"P-{i}"], _RND[f"U-{i}"] = p, u
    return _RND


def write(path, rows):
    keys = list(dict.fromkeys(k for r in rows for k in r))
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for r in rows:
            w.writerow({k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()})
    print("written", path)


def main():
    data = [data_row(a) for a in ARMS]
    ga_codes = {it["code"] for it in common.load_synthetic()}
    shared = sum(c in ga_codes for c in _random_codes().values())
    for r in data:
        r["samples_shared_with_other_arm"] = shared
    write(os.path.join(TABLES, "ga_ablation_data.csv"), data)
    for r in data:
        print(r)
    rows = model_rows()
    if rows:
        write(os.path.join(TABLES, "ga_ablation_models.csv"), rows)
        for r in rows:
            print(r)


if __name__ == "__main__":
    main()
