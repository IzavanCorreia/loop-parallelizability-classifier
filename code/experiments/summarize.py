"""Turns the raw predictions in results/raw into the tables of the paper (CSV + LaTeX) and the
statistics. Every number of the manuscript comes from the files this script writes.

E2  model comparison on the hybrid set (3 x 10-fold): accuracy, precision, recall, F1, FPR, AUC
E3  real code: (a) syn2real, (b) real samples inside the hybrid folds, (c) real-only CV;
    per-dependence-type accuracy on real code
E4  FPR control: threshold chosen on validation for FPR <= 5% and 1%, effect on the test set
E5  checkpoint selection inside each fold (DistilBERT): lowest validation loss vs lowest validation FPR
E6  stability: spread over folds and repetitions, worst/best fold
E7  efficiency: parameters, training and inference time
Statistics: Friedman test over models, Wilcoxon signed-rank (Holm) and the corrected resampled
t-test (Nadeau & Bengio, 2003) of DistilBERT against each baseline.
"""

import glob
import json
import os
import sys
from collections import defaultdict

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.metrics import roc_auc_score

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402

MODELS = ["lr", "svm", "dnn", "cnn", "ngram", "distilbert"]
NAMES = {"lr": "Logistic regression", "svm": "Linear SVM", "dnn": "DNN", "cnn": "CNN", "ngram": "N-gram LR",
         "distilbert": "DistilBERT"}
OUT = os.path.join(common.RESULTS, "tables")
N_BOOT = 2000


def load_runs(setting, model):
    runs = []
    for path in sorted(glob.glob(os.path.join(common.RESULTS, "raw", setting, model, "rep*_fold*.npz"))):
        d = np.load(path, allow_pickle=False)
        name = os.path.basename(path)[:-4]
        rep, fold = int(name.split("_")[0][3:]), int(name.split("_")[1][4:])
        run = {k: d[k] for k in d.files if k != "info"}
        run.update(rep=rep, fold=fold, info=json.loads(str(d["info"])))
        runs.append(run)
    return runs


def metrics(y, score, thr):
    pred = (score > thr).astype(int)
    tp = int(((pred == 1) & (y == 1)).sum())
    tn = int(((pred == 0) & (y == 0)).sum())
    fp = int(((pred == 1) & (y == 0)).sum())
    fn = int(((pred == 0) & (y == 1)).sum())
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0
    out = {"accuracy": (tp + tn) / len(y), "precision": prec, "recall": rec,
           "f1": 2 * prec * rec / (prec + rec) if prec + rec else 0.0,
           "fpr": fp / (fp + tn) if fp + tn else 0.0,
           "tp": tp, "tn": tn, "fp": fp, "fn": fn}
    out["auc"] = roc_auc_score(y, score) if len(set(y)) == 2 else float("nan")
    return out


def describe(values):
    v = np.asarray(values, dtype=float)
    n = len(v)
    sd = v.std(ddof=1) if n > 1 else 0.0
    h = stats.t.ppf(0.975, n - 1) * sd / np.sqrt(n) if n > 1 else 0.0
    return {"mean": v.mean(), "sd": sd, "median": np.median(v), "min": v.min(), "max": v.max(),
            "ci_low": v.mean() - h, "ci_high": v.mean() + h, "n": n}


def bootstrap_ci(y, score, thr, groups, metric, seed=0):
    """Percentile bootstrap over groups (duplicate real samples are resampled together)."""
    rng = np.random.default_rng(seed)
    uniq = np.unique(groups)
    idx_by_g = {g: np.where(groups == g)[0] for g in uniq}
    vals = []
    for _ in range(N_BOOT):
        pick = rng.choice(uniq, len(uniq), replace=True)
        idx = np.concatenate([idx_by_g[g] for g in pick])
        vals.append(metrics(y[idx], score[idx], thr)[metric])
    return np.percentile(vals, [2.5, 97.5])


def fold_table(setting, subset=None):
    """One row per (model, rep, fold) with the test metrics; subset filters test ids by prefix."""
    rows = []
    for m in MODELS:
        for r in load_runs(setting, m):
            ids, y, s = r["test_ids"], r["test_y"], r["test_score"]
            if subset:
                keep = np.char.startswith(ids.astype(str), subset)
                ids, y, s = ids[keep], y[keep], s[keep]
            row = {"model": m, "rep": r["rep"], "fold": r["fold"]}
            row.update(metrics(y, s, r["info"]["threshold"]))
            rows.append(row)
    return pd.DataFrame(rows)


def pooled_real(setting):
    """Pools the predictions on real samples of a setting: one prediction per real sample and repetition."""
    out = {}
    real = {it["id"]: it for it in common.load_real()}
    for m in MODELS:
        per_rep = defaultdict(lambda: {"ids": [], "y": [], "s": [], "thr": 0.5})
        for r in load_runs(setting, m):
            keep = np.char.startswith(r["test_ids"].astype(str), "real-")
            per_rep[r["rep"]]["ids"] += list(r["test_ids"][keep])
            per_rep[r["rep"]]["y"] += list(r["test_y"][keep])
            per_rep[r["rep"]]["s"] += list(r["test_score"][keep])
            per_rep[r["rep"]]["thr"] = r["info"]["threshold"]
        out[m] = {rep: {"ids": np.array(v["ids"]), "y": np.array(v["y"]), "s": np.array(v["s"]),
                        "thr": v["thr"], "groups": np.array([real[i]["group"] for i in v["ids"]]),
                        "category": np.array([real[i]["category"] for i in v["ids"]])}
                  for rep, v in per_rep.items()}
    return out


def summary_rows(df, label):
    rows = []
    for m in MODELS:
        sub = df[df.model == m]
        if sub.empty:
            continue
        row = {"setting": label, "model": NAMES[m], "runs": len(sub)}
        for k in ("accuracy", "precision", "recall", "f1", "fpr", "auc"):
            d = describe(sub[k])
            row.update({f"{k}_mean": d["mean"], f"{k}_sd": d["sd"], f"{k}_ci_low": d["ci_low"],
                        f"{k}_ci_high": d["ci_high"], f"{k}_min": d["min"], f"{k}_max": d["max"]})
        rep_means = sub.groupby("rep")["accuracy"].mean()
        row["accuracy_sd_between_reps"] = rep_means.std(ddof=1) if len(rep_means) > 1 else 0.0
        rows.append(row)
    return rows


def corrected_t(diffs, n_train, n_test):
    """Nadeau & Bengio (2003) corrected resampled t-test for repeated k-fold CV."""
    d = np.asarray(diffs, dtype=float)
    n = len(d)
    var = d.var(ddof=1)
    if var == 0:
        return float("inf"), 0.0
    t = d.mean() / np.sqrt((1 / n + n_test / n_train) * var)
    return t, 2 * stats.t.sf(abs(t), n - 1)


def holm(pvals):
    order = np.argsort(pvals)
    adj = np.empty(len(pvals))
    running = 0.0
    for rank, i in enumerate(order):
        running = max(running, (len(pvals) - rank) * pvals[i])
        adj[i] = min(1.0, running)
    return adj


def stats_tests(df, setting, label=None):
    """Friedman over all models and Wilcoxon (Holm) of DistilBERT against each model on fold-level accuracy;
    the corrected resampled t-test is also computed. label names the rows (defaults to the setting)."""
    label = label or setting
    out = []
    piv = df.pivot_table(index=["rep", "fold"], columns="model", values="accuracy")
    models = [m for m in MODELS if m in piv.columns]
    piv = piv[models].dropna()
    if len(models) >= 3 and len(piv) > 2:
        chi, p = stats.friedmanchisquare(*[piv[m] for m in models])
        out.append({"setting": label, "test": "Friedman (accuracy, all models)", "statistic": chi, "p": p, "n": len(piv)})
    runs = load_runs(setting, "distilbert")
    n_train = np.mean([r["info"]["n_train"] + r["info"]["n_val"] for r in runs]) if runs else 1
    n_test = np.mean([r["info"]["n_test"] for r in runs]) if runs else 1
    pw = []
    for m in models:
        if m == "distilbert" or "distilbert" not in piv.columns:
            continue
        diff = piv["distilbert"] - piv[m]
        w = stats.wilcoxon(piv["distilbert"], piv[m]) if (diff != 0).any() else None
        t, pt = corrected_t(diff, n_train, n_test)
        pw.append({"setting": label, "test": f"DistilBERT vs {NAMES[m]}", "mean_diff_acc": diff.mean(),
                   "wilcoxon_p": w.pvalue if w else 1.0, "corrected_t": t, "corrected_t_p": pt, "n": len(diff)})
    if pw:
        for row, adj in zip(pw, holm(np.array([r["wilcoxon_p"] for r in pw]))):
            row["wilcoxon_p_holm"] = adj
        for row, adj in zip(pw, holm(np.array([r["corrected_t_p"] for r in pw]))):
            row["corrected_t_p_holm"] = adj
    return out, pw


def threshold_for_fpr(y_val, s_val, alpha):
    """Smallest threshold whose validation FPR is <= alpha (maximises TPR under the constraint)."""
    neg = np.sort(s_val[y_val == 0])
    if len(neg) == 0:
        return 0.5
    k = int(np.floor(alpha * len(neg)))          # at most k negatives above the threshold
    return neg[len(neg) - k - 1] if k < len(neg) else -np.inf


# (validation samples used to pick the threshold, test samples it is applied to), by setting
FPR_PARTS = {"hybrid": (("all", "all"), ("all", "real"), ("real", "real")),
             "real": (("all", "all"),),
             "syn2real": (("all", "all"),)}


def _part(ids, y, s, part):
    if part == "all":
        return y, s
    keep = np.char.startswith(ids.astype(str), "real-")
    return y[keep], s[keep]


def _rates(c):
    return {"fpr": c["fp"] / (c["fp"] + c["tn"]), "tpr": c["tp"] / (c["tp"] + c["fn"]),
            "accuracy": (c["tp"] + c["tn"]) / (c["tp"] + c["tn"] + c["fp"] + c["fn"])}


def fpr_control(setting):
    """Threshold chosen on validation for FPR <= alpha, applied to the test samples of the same run.
    In the hybrid setting the threshold is chosen either on all validation samples or on the real
    ones only. Rates on all hybrid test samples are fold means (as in the hybrid table); rates on
    real test samples pool the folds of each repetition (as in the real-code table)."""
    rows = []
    for m in MODELS:
        for r in load_runs(setting, m):
            for val_part, test_part in FPR_PARTS[setting]:
                vy, vs = _part(r["val_ids"], r["val_y"], r["val_score"], val_part)
                y, s = _part(r["test_ids"], r["test_y"], r["test_score"], test_part)
                thrs = {"base": r["info"]["threshold"], 0.05: threshold_for_fpr(vy, vs, 0.05),
                        0.01: threshold_for_fpr(vy, vs, 0.01)}
                for key, thr in thrs.items():
                    mt = metrics(y, s, thr)
                    rows.append({"model": m, "rep": r["rep"], "fold": r["fold"], "rule": key,
                                 "val_part": val_part, "test_part": test_part, "val_neg": int((vy == 0).sum()),
                                 **{k: mt[k] for k in ("tp", "tn", "fp", "fn")}})
    df = pd.DataFrame(rows)
    if df.empty:
        return df
    pooled = setting != "hybrid"
    out = []
    for (m, vp, tp), g in df.groupby(["model", "val_part", "test_part"]):
        pool = pooled or tp == "real"
        res = {}
        for key, gk in g.groupby("rule"):
            units = [gg[["tp", "tn", "fp", "fn"]].sum() for _, gg in gk.groupby("rep")] if pool else \
                [row for _, row in gk[["tp", "tn", "fp", "fn"]].iterrows()]
            rates = pd.DataFrame([_rates(u) for u in units])
            res[key] = {"fpr_mean": rates.fpr.mean(), "fpr_max": rates.fpr.max(), "tpr_mean": rates.tpr.mean(),
                        "accuracy_mean": rates.accuracy.mean(), "units": len(rates)}
        for alpha in (0.05, 0.01):
            out.append({"model": m, "alpha": alpha, "val_part": vp, "test_part": tp,
                        "aggregation": "pooled per repetition" if pool else "mean over folds",
                        **res[alpha], "base_fpr_mean": res["base"]["fpr_mean"], "base_tpr_mean": res["base"]["tpr_mean"],
                        "val_neg_mean": g.val_neg.mean()})
    return pd.DataFrame(out)


def checkpoint_selection(setting):
    rows = []
    for r in load_runs(setting, "distilbert"):
        vs, ts, vl = r["epoch_val_scores"], r["epoch_test_scores"], r["epoch_val_loss"]
        vfpr = [metrics(r["val_y"], vs[e], 0.5)["fpr"] for e in range(len(vl))]
        e_loss = int(np.argmin(vl))
        e_fpr = int(min(range(len(vl)), key=lambda e: (vfpr[e], vl[e])))
        a, b = metrics(r["test_y"], ts[e_loss], 0.5), metrics(r["test_y"], ts[e_fpr], 0.5)
        rows.append({"rep": r["rep"], "fold": r["fold"], "epoch_loss": e_loss + 1, "epoch_fpr": e_fpr + 1,
                     "test_fpr_loss_rule": a["fpr"], "test_fpr_fpr_rule": b["fpr"],
                     "test_acc_loss_rule": a["accuracy"], "test_acc_fpr_rule": b["accuracy"],
                     "test_recall_loss_rule": a["recall"], "test_recall_fpr_rule": b["recall"]})
    return pd.DataFrame(rows)


def efficiency():
    rows = []
    for m in MODELS:
        runs = load_runs("hybrid", m)
        if not runs:
            continue
        n_te = np.array([r["info"]["n_test"] for r in runs])
        # linear models: one weight per input feature plus the bias (first fold; the input width of the
        # four baselines follows the padding length fitted in each fold)
        info0 = runs[0]["info"]
        params = info0["n_params"] if "n_params" in info0 else info0["n_features"] + 1
        rows.append({"model": NAMES[m], "params": params,
                     "train_time_s_mean": np.mean([r["info"]["train_time_s"] for r in runs]),
                     "infer_ms_per_sample": 1000 * np.mean([r["info"]["infer_time_s"] for r in runs] / n_te),
                     "epochs_mean": np.mean([r["info"].get("epochs_run", 0) for r in runs]),
                     "best_epoch_mean": np.mean([r["info"].get("best_epoch", 0) for r in runs]),
                     "peak_vram_gb_max": max(r["info"].get("peak_vram_gb", 0) for r in runs)})
    return pd.DataFrame(rows)


def syn2real_runs():
    """Synthetic -> real: validation accuracy (synthetic) against accuracy on the real loops, per run."""
    rows = []
    for m in MODELS:
        for r in load_runs("syn2real", m):
            thr = r["info"]["threshold"]
            rows.append({"model": NAMES[m], "rep": r["rep"],
                         "val_accuracy": metrics(r["val_y"], r["val_score"], thr)["accuracy"],
                         "real_accuracy": metrics(r["test_y"], r["test_score"], thr)["accuracy"]})
    return pd.DataFrame(rows)


def protocol_sizes():
    """Mean sizes of the training, validation and test portions (DistilBERT runs; all models share them)."""
    rows = []
    for setting in ("hybrid", "real", "syn2real"):
        runs = load_runs(setting, "distilbert")
        if not runs:
            continue
        real_val = [np.char.startswith(r["val_ids"].astype(str), "real-").sum() for r in runs]
        real_test = [np.char.startswith(r["test_ids"].astype(str), "real-").sum() for r in runs]
        n_tr = [r["info"]["n_train"] for r in runs]
        n_real = len(common.load_real())
        real_tr = [(n_real - v - t) if setting != "syn2real" else 0 for v, t in zip(real_val, real_test)]
        rows.append({"setting": setting, "n_train_mean": np.mean(n_tr), "n_val_mean": np.mean([r["info"]["n_val"] for r in runs]),
                     "n_test_mean": np.mean([r["info"]["n_test"] for r in runs]),
                     "real_train_mean": np.mean(real_tr), "real_val_mean": np.mean(real_val),
                     "real_test_mean": np.mean(real_test),
                     "real_share_train": np.mean(np.array(real_tr) / np.array(n_tr)),
                     "val_neg_mean": np.mean([(r["val_y"] == 0).sum() for r in runs])})
    return pd.DataFrame(rows)


def real_tables():
    rows, cat_rows = [], []
    for setting, label in (("syn2real", "(a) synthetic only -> real"), ("hybrid", "(b) hybrid, real test samples"),
                           ("real", "(c) real only")):
        pooled = pooled_real(setting)
        for m in MODELS:
            reps = pooled.get(m, {})
            if not reps:
                continue
            per = [metrics(v["y"], v["s"], v["thr"]) for v in reps.values()]
            row = {"setting": label, "model": NAMES[m], "reps": len(per)}
            for k in ("accuracy", "precision", "recall", "f1", "fpr", "auc"):
                vals = [p[k] for p in per]
                row[f"{k}_mean"], row[f"{k}_sd"] = np.mean(vals), (np.std(vals, ddof=1) if len(vals) > 1 else 0.0)
            # bootstrap over the real samples, pooling the repetitions: a resampled group brings its
            # predictions from every repetition, so the interval reflects the 340-sample test set
            y_all = np.concatenate([v["y"] for v in reps.values()])
            s_all = np.concatenate([v["s"] for v in reps.values()])
            g_all = np.concatenate([v["groups"] for v in reps.values()])
            thr = next(iter(reps.values()))["thr"]
            for k in ("accuracy", "fpr"):
                lo, hi = bootstrap_ci(y_all, s_all, thr, g_all, k)
                row[f"{k}_boot_low"], row[f"{k}_boot_high"] = lo, hi
            rows.append(row)
            for v in reps.values():
                pred = (v["s"] > v["thr"]).astype(int)
                for cat in np.unique(v["category"]):
                    k = v["category"] == cat
                    cat_rows.append({"setting": label, "model": NAMES[m], "category": cat,
                                     "label": "Parallelizable" if v["y"][k][0] == 1 else "Undefined",
                                     "n": int(k.sum()), "correct": float((pred[k] == v["y"][k]).mean())})
    cats = pd.DataFrame(cat_rows)
    if not cats.empty:
        cats = cats.groupby(["setting", "model", "category", "label"]).agg(
            n=("n", "max"), correct=("correct", "mean")).reset_index()
    return pd.DataFrame(rows), cats


def main():
    os.makedirs(OUT, exist_ok=True)
    summary, tests, pairwise, worst = [], [], [], []
    for setting, label in (("hybrid", "hybrid"), ("real", "real only")):
        df = fold_table(setting)
        if df.empty:
            continue
        df.to_csv(os.path.join(OUT, f"folds_{setting}.csv"), index=False)
        summary += summary_rows(df, label)
        if setting == "real":
            t, pw = stats_tests(df, setting)
            tests += t
            pairwise += pw
        for m in MODELS:
            sub = df[df.model == m]
            if len(sub):
                w, b = sub.loc[sub.accuracy.idxmin()], sub.loc[sub.accuracy.idxmax()]
                worst.append({"setting": label, "model": NAMES[m], "worst_acc": w.accuracy, "worst_rep": w.rep,
                              "worst_fold": w.fold, "worst_fpr": w.fpr, "best_acc": b.accuracy,
                              "max_fpr": sub.fpr.max(), "folds_zero_fp": int((sub.fp == 0).sum())})
    syn = fold_table("hybrid", subset="syn-")
    if not syn.empty:
        summary += summary_rows(syn, "hybrid, synthetic test samples")
        t, pw = stats_tests(syn, "hybrid", "hybrid, synthetic test samples")
        tests += t
        pairwise += pw
    pd.DataFrame(summary).to_csv(os.path.join(OUT, "summary.csv"), index=False)
    pd.DataFrame(tests).to_csv(os.path.join(OUT, "tests_friedman.csv"), index=False)
    pd.DataFrame(pairwise).to_csv(os.path.join(OUT, "tests_pairwise.csv"), index=False)
    pd.DataFrame(worst).to_csv(os.path.join(OUT, "stability.csv"), index=False)
    real, cats = real_tables()
    real.to_csv(os.path.join(OUT, "real_code.csv"), index=False)
    cats.to_csv(os.path.join(OUT, "real_code_by_category.csv"), index=False)
    pd.concat([fpr_control(s).assign(setting=s) for s in ("hybrid", "real", "syn2real")], ignore_index=True) \
        .to_csv(os.path.join(OUT, "fpr_control.csv"), index=False)
    ck = checkpoint_selection("hybrid")
    if not ck.empty:
        ck.to_csv(os.path.join(OUT, "checkpoint_selection_folds.csv"), index=False)
        res = {"runs": len(ck), "same_epoch": int((ck.epoch_loss == ck.epoch_fpr).sum())}
        for k in ("fpr", "acc", "recall"):
            a, b = ck[f"test_{k}_loss_rule"], ck[f"test_{k}_fpr_rule"]
            res[f"{k}_loss_rule_mean"], res[f"{k}_fpr_rule_mean"] = a.mean(), b.mean()
            res[f"{k}_wilcoxon_p"] = stats.wilcoxon(a, b).pvalue if (a != b).any() else 1.0
        pd.DataFrame([res]).to_csv(os.path.join(OUT, "checkpoint_selection.csv"), index=False)
    efficiency().to_csv(os.path.join(OUT, "efficiency.csv"), index=False)
    protocol_sizes().to_csv(os.path.join(OUT, "protocol_sizes.csv"), index=False)
    syn2real_runs().to_csv(os.path.join(OUT, "syn2real_runs.csv"), index=False)
    print("tables written to", OUT)
    with pd.option_context("display.width", 200, "display.max_columns", 30, "display.float_format", "{:.4f}".format):
        s = pd.DataFrame(summary)
        if not s.empty:
            print(s[["setting", "model", "runs", "accuracy_mean", "accuracy_sd", "fpr_mean", "f1_mean", "auc_mean"]])
        if not real.empty:
            print(real[["setting", "model", "reps", "accuracy_mean", "fpr_mean", "recall_mean", "auc_mean"]])


if __name__ == "__main__":
    main()
