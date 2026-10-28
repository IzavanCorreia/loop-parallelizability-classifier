"""Graphical abstract (required by Applied Soft Computing; readable at 5 x 13 cm, at least 531 x 1328 px).
Drawn in TikZ (graphical_abstract.tex) at its reading size; the numbers are read from results/tables, so the
image always matches the paper. Writes latex/figures/graphical_abstract.pdf and, when pypdfium2 is available,
a 600 dpi PNG for the submission system."""

import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402
from tikz import compile_tikz, save  # noqa: E402


def values():
    tables = os.path.join(common.RESULTS, "tables")
    syn = pd.read_csv(os.path.join(tables, "summary.csv"))
    syn = 100 * syn[syn.setting == "hybrid, synthetic test samples"].set_index("model").accuracy_mean
    real_all = pd.read_csv(os.path.join(tables, "real_code.csv"))
    real = real_all[real_all.setting == "(c) real only"].set_index("model")
    syn_real = real_all[real_all.setting == "(a) synthetic only -> real"].set_index("model").loc["DistilBERT"]
    fc = pd.read_csv(os.path.join(tables, "fpr_control.csv"))
    thr = fc[(fc.setting == "real") & (fc.alpha == 0.05)].groupby("model").first()
    prev = syn[["Logistic regression", "Linear SVM", "DNN", "CNN"]]
    v = {"synPrevMin": prev.min(), "synPrevMax": prev.max(), "synNgram": syn["N-gram LR"],
         "synBert": syn["DistilBERT"],
         "synRealAcc": 100 * syn_real.accuracy_mean, "synRealFpr": 100 * syn_real.fpr_mean,
         "realBertAcc": 100 * real.loc["DistilBERT", "accuracy_mean"], "realBertFpr": 100 * real.loc["DistilBERT", "fpr_mean"],
         "realNgAcc": 100 * real.loc["N-gram LR", "accuracy_mean"], "realNgFpr": 100 * real.loc["N-gram LR", "fpr_mean"],
         "thrBertTpr": 100 * thr.loc["distilbert", "tpr_mean"], "thrBertFpr": 100 * thr.loc["distilbert", "fpr_mean"],
         "thrNgTpr": 100 * thr.loc["ngram", "tpr_mean"], "thrNgFpr": 100 * thr.loc["ngram", "fpr_mean"]}
    return "".join(f"\\def\\{k}{{{x:.1f}}}\n" for k, x in v.items())


def main():
    pdf = compile_tikz("graphical_abstract", {"ga_values.tex": values()})
    out = os.path.join(common.ROOT, "latex", "figures", "graphical_abstract")
    save(pdf, out + ".pdf", os.path.join(common.ROOT, "latex_ptbr", "figures", "graphical_abstract.pdf"))
    try:
        import pypdfium2 as pdfium
    except ImportError:
        print("written", out + ".pdf (no PNG: pypdfium2 not installed)")
        return
    image = pdfium.PdfDocument(pdf)[0].render(scale=600 / 72).to_pil()
    image.save(out + ".png", dpi=(600, 600))
    print("written", out + ".pdf/.png", image.size)


if __name__ == "__main__":
    main()
