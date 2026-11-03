"""Tables and tests of the two-stage experiment (two_stage.py), with the rules fixed in
TWO_STAGE_PROTOCOL.md before the runs.

  two_stage.csv        one row per arm and budget: rates on the real test loops (predictions of each
                       repetition pooled, mean over 3 repetitions), rates with thresholds for a target FPR,
                       rates on the 1,600 held-out synthetic samples, training effort
  two_stage_tests.csv  pretrained - scratch per budget: fold-level Wilcoxon and corrected t-test, Holm over
                       the three reduced budgets, decision by the criterion of the protocol
  two_stage_stage1.csv stage 1 per repetition: synthetic validation and real test accuracy
  two_stage_checks.csv reproduction of the original runs (same seeds and partitions)
"""

import os
import sys

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402
from summarize import OUT, bootstrap_ci, corrected_t, holm, load_runs, metrics, threshold_for_fpr  # noqa: E402
from two_stage import ARMS, BUDGETS, SETTING  # noqa: E402

ALPHA = 0.05
STAGE1 = {r["rep"]: r for r in load_runs(SETTING, "stage1")}


def pooled(runs):
    """Test labels, scores and groups pooled over the folds of each repetition."""
    real = {it["id"]: it for it in common.load_real()}
    out = {}
    for rep in sorted({r["rep"] for r in runs}):
        rr = [r for r in runs if r["rep"] == rep]
        ids = np.concatenate([r["test_ids"] for r in rr])
        out[rep] = {"y": np.concatenate([r["test_y"] for r in rr]), "s": np.concatenate([r["test_score"] for r in rr]),
                    "g": np.array([real[str(i)]["group"] for i in ids])}
    return out


def target_rates(runs, alpha):
    """FPR and recall on the test loops with the threshold chosen on the validation loops of each run."""
    fpr, tpr = [], []
    for rep in sorted({r["rep"] for r in runs}):
        c = np.zeros(4)
        for r in (x for x in runs if x["rep"] == rep):
            m = metrics(r["test_y"], r["test_score"], threshold_for_fpr(r["val_y"], r["val_score"], alpha))
            c += [m["tp"], m["tn"], m["fp"], m["fn"]]
        fpr.append(c[2] / (c[2] + c[1]))
        tpr.append(c[0] / (c[0] + c[3]))
    return np.mean(fpr), np.mean(tpr)


def pair_scores(run):
    """Exploratory, added after the runs: share of held-out pairs whose Parallelizable program scores above the
    Undefined one, and the mean absolute score difference inside a pair."""
    ids = STAGE1[run["rep"]]["val_ids"].astype(str)
    score = dict(zip(ids, run["pairs_score"]))
    pairs = sorted({i.split("-")[2] for i in ids})
    diff = np.array([score[f"syn-P-{p}"] - score[f"syn-U-{p}"] for p in pairs])
    return (diff > 0).mean(), np.abs(diff).mean()


def summary_row(arm, pct, runs):
    reps = pooled(runs)
    per = [metrics(v["y"], v["s"], 0.5) for v in reps.values()]
    row = {"arm": arm, "budget": pct, "runs": len(runs), "n_train_mean": np.mean([r["info"]["n_train"] for r in runs])}
    for k in ("accuracy", "recall", "fpr", "auc"):
        vals = [p[k] for p in per]
        row[f"{k}_mean"], row[f"{k}_sd"] = np.mean(vals), np.std(vals, ddof=1)
    y = np.concatenate([v["y"] for v in reps.values()])
    s = np.concatenate([v["s"] for v in reps.values()])
    g = np.concatenate([v["g"] for v in reps.values()])
    for k in ("accuracy", "fpr"):
        row[f"{k}_boot_low"], row[f"{k}_boot_high"] = bootstrap_ci(y, s, 0.5, g, k)
    for alpha in (0.05, 0.01):
        row[f"fpr_at_{alpha}"], row[f"tpr_at_{alpha}"] = target_rates(runs, alpha)
    pairs = [metrics(r["pairs_y"], r["pairs_score"], 0.5) for r in runs]
    for k in ("accuracy", "fpr", "auc"):
        row[f"pairs_{k}_mean"] = np.mean([p[k] for p in pairs])
        row[f"pairs_{k}_sd"] = np.std([p[k] for p in pairs], ddof=1)
    above, gap = zip(*[pair_scores(r) for r in runs])
    row["pairs_p_above_u"], row["pairs_score_gap"] = np.mean(above), np.mean(gap)
    row["best_epoch_mean"] = np.mean([r["info"]["best_epoch"] for r in runs])
    row["epochs_run_mean"] = np.mean([r["info"]["epochs_run"] for r in runs])
    row["train_time_s_mean"] = np.mean([r["info"]["train_time_s"] for r in runs])
    return row


def fold_rows(runs):
    rows = []
    for r in runs:
        m = metrics(r["test_y"], r["test_score"], 0.5)
        p = metrics(r["pairs_y"], r["pairs_score"], 0.5)
        rows.append({"rep": r["rep"], "fold": r["fold"], "accuracy": m["accuracy"], "fpr": m["fpr"], "recall": m["recall"],
                     "pairs_accuracy": p["accuracy"], "n_train": r["info"]["n_train"] + r["info"]["n_val"],
                     "n_test": r["info"]["n_test"]})
    return pd.DataFrame(rows).set_index(["rep", "fold"]).sort_index()


def paired(a, b, metric):
    """pretrained (a) minus scratch (b) over the same folds."""
    d = a[metric] - b[metric]
    w = stats.wilcoxon(a[metric], b[metric]).pvalue if (d != 0).any() else 1.0
    t, pt = corrected_t(d, a.n_train.mean(), a.n_test.mean())
    return {"metric": metric, "mean_diff": d.mean(), "wins": int((d > 0).sum()), "ties": int((d == 0).sum()),
            "losses": int((d < 0).sum()), "wilcoxon_p": w, "corrected_t": t, "corrected_t_p": pt}


def significant(row, sign):
    return np.sign(row["mean_diff"]) == sign and row["wilcoxon_p_final"] < ALPHA and row["corrected_t_p_final"] < ALPHA


def tests(folds):
    rows = []
    for pct in BUDGETS:
        for metric in ("accuracy", "fpr"):
            rows.append({"budget": pct, **paired(folds["pretrained", pct], folds["scratch", pct], metric)})
    df = pd.DataFrame(rows)
    df["wilcoxon_p_final"], df["corrected_t_p_final"] = df.wilcoxon_p, df.corrected_t_p
    for metric in ("accuracy", "fpr"):
        k = (df.metric == metric) & (df.budget != 100)
        df.loc[k, "wilcoxon_p_final"] = holm(df.loc[k, "wilcoxon_p"].values)
        df.loc[k, "corrected_t_p_final"] = holm(df.loc[k, "corrected_t_p"].values)
    verdict = {}
    for pct, g in df.groupby("budget"):
        acc, fpr = g[g.metric == "accuracy"].iloc[0], g[g.metric == "fpr"].iloc[0]
        better = significant(acc, 1) or significant(fpr, -1)
        worse = significant(acc, -1) or significant(fpr, 1)
        verdict[pct] = "helps" if better and not worse else "worsens" if worse and not better else "no detected difference"
    df["decision"] = df.budget.map(verdict)
    return df


def stage1_rows():
    rows = []
    for r in load_runs(SETTING, "stage1"):
        rows.append({"rep": r["rep"], "best_epoch": r["info"]["best_epoch"], "train_time_s": r["info"]["train_time_s"],
                     "val_accuracy": metrics(r["val_y"], r["val_score"], 0.5)["accuracy"],
                     "real_accuracy": metrics(r["test_y"], r["test_score"], 0.5)["accuracy"]})
    return pd.DataFrame(rows)


def checks():
    rows = []
    for new, old, tag in (("scratch_f100", ("real", "distilbert"), "scratch_f100 x real/distilbert"),
                          ("stage1", ("syn2real", "distilbert"), "stage1 x syn2real/distilbert")):
        a = {(r["rep"], r["fold"]): r for r in load_runs(SETTING, new)}
        b = {(r["rep"], r["fold"]): r for r in load_runs(*old)}
        keys = sorted(set(a) & set(b))
        same_ids = all((a[k]["test_ids"] == b[k]["test_ids"]).all() and (a[k]["val_ids"] == b[k]["val_ids"]).all() for k in keys)
        pa = np.concatenate([a[k]["test_score"] > 0.5 for k in keys])
        pb = np.concatenate([b[k]["test_score"] > 0.5 for k in keys])
        ya = np.concatenate([a[k]["test_y"] for k in keys])
        rows.append({"comparison": tag, "runs": len(keys), "same_partitions": same_ids,
                     "predictions_changed": int((pa != pb).sum()), "predictions": len(pa),
                     "accuracy_new": (pa == ya).mean(), "accuracy_original": (pb == ya).mean()})
    return pd.DataFrame(rows)


def main():
    rows, folds = [], {}
    for pct in BUDGETS:
        for arm in ARMS:
            runs = load_runs(SETTING, f"{arm}_f{pct}")
            if len(runs) != 30:
                sys.exit(f"{arm}_f{pct}: {len(runs)} of 30 runs")
            rows.append(summary_row(arm, pct, runs))
            folds[arm, pct] = fold_rows(runs)
    table, test = pd.DataFrame(rows), tests(folds)
    pairs = pd.DataFrame([{"budget": pct, **paired(folds["pretrained", pct], folds["scratch", pct], "pairs_accuracy")}
                          for pct in BUDGETS])
    test = pd.concat([test, pairs], ignore_index=True)
    table.to_csv(os.path.join(OUT, "two_stage.csv"), index=False)
    test.to_csv(os.path.join(OUT, "two_stage_tests.csv"), index=False)
    s1, ck = stage1_rows(), checks()
    s1.to_csv(os.path.join(OUT, "two_stage_stage1.csv"), index=False)
    ck.to_csv(os.path.join(OUT, "two_stage_checks.csv"), index=False)
    with pd.option_context("display.width", 220, "display.max_columns", 40, "display.float_format", "{:.4f}".format):
        print(table[["arm", "budget", "n_train_mean", "accuracy_mean", "accuracy_sd", "recall_mean", "fpr_mean", "fpr_sd",
                     "auc_mean", "fpr_at_0.05", "tpr_at_0.05", "pairs_accuracy_mean", "pairs_fpr_mean", "best_epoch_mean"]])
        print(test[["budget", "metric", "mean_diff", "wins", "ties", "losses", "wilcoxon_p", "wilcoxon_p_final",
                    "corrected_t_p", "corrected_t_p_final", "decision"]])
        print(s1)
        print(ck)


if __name__ == "__main__":
    main()
