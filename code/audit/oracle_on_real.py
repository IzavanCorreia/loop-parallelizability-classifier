"""Runs the dependence oracle over the 340 real-world samples and measures agreement with the
researchers' labels (Cohen's kappa on the samples the oracle can analyse)."""

import csv
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "code", "generator"))
from oracle import analyze_isolated  # noqa: E402

SEP = "=" * 40


def load(path):
    txt = open(path, encoding="utf-8").read()
    return [re.sub(r"^Code \d+:\s*\n", "", c.strip()) for c in txt.split(SEP) if c.strip()]


def cohen_kappa(a, b):
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(a) | set(b)) / (n * n)
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


def main():
    data_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "data", "real")
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "results", "real_oracle.csv")
    rows = []
    for cls in ["Parallelizable", "Undefined"]:
        for i, code in enumerate(load(os.path.join(data_dir, f"{cls}_codes.py")), 1):
            r = analyze_isolated(code)
            rows.append({"class": cls, "index": i, "oracle": r["label"] or "n/a", "reason": r["reason"], "code": code})
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    analysed = [r for r in rows if r["oracle"] != "n/a"]
    print(f"analysable: {len(analysed)}/{len(rows)}")
    print("not analysable reasons:", Counter(r["reason"].split(":")[0] for r in rows if r["oracle"] == "n/a"))
    for cls in ["Parallelizable", "Undefined"]:
        sub = [r for r in analysed if r["class"] == cls]
        print(f"{cls}: n={len(sub)} oracle={Counter(r['oracle'] for r in sub)}")
    agree = sum(r["class"] == r["oracle"] for r in analysed)
    print(f"agreement: {agree}/{len(analysed)} = {agree/len(analysed)*100:.1f}%")
    print(f"Cohen's kappa: {cohen_kappa([r['class'] for r in analysed], [r['oracle'] for r in analysed]):.3f}")
    print("disagreement reasons:", Counter(r["reason"] for r in analysed if r["class"] != r["oracle"]).most_common(10))
    print("written:", out)


if __name__ == "__main__":
    main()
