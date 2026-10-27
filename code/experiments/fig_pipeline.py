"""Figure 1: overview of the approach, drawn in TikZ (fig_pipeline.tex) and compiled to a vector PDF for the
English and the Portuguese manuscripts."""

import os

from tikz import compile_tikz, save

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))


def main():
    pdf = compile_tikz("fig_pipeline")
    save(pdf, *(os.path.join(ROOT, d, "figures", "fig_pipeline.pdf") for d in ("latex", "latex_ptbr")))
    print("written fig_pipeline.pdf (latex/figures, latex_ptbr/figures)")


if __name__ == "__main__":
    main()
