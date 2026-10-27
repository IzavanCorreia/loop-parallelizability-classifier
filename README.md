# Loop parallelizability classification: evolutionary minimal pairs, dependence oracle and DistilBERT

This repository contains the data, code and raw results of the manuscript

**Automatic loop parallelizability classification via contextual code representations: evolutionary data
generation and evaluation on real-world code**
Izavan dos S. Correia, Henrique C. T. Santos, Tiago A. E. Ferreira (manuscript under review).

Version 2.0.0 corresponds to this manuscript. The releases v1.x contain the data and code of an earlier version
of this work, posted on arXiv (https://arxiv.org/abs/2603.30040).

## Overview

- **Task.** Each sample is a Python function or script with a target loop, labeled *Parallelizable* or
  *Undefined*.
  - A loop is Parallelizable when its iterations can run concurrently and in any order without changing the
    result. Appending to an output list that is not read in the loop (the *map* pattern) is accepted.
  - Accumulators, reductions, recurrences, reads of elements written by other iterations, early exits, `while`
    loops and values used after the loop make a loop Undefined.
  - When loops are nested, the label refers to the outermost loop.
- **Synthetic data.**
  - A genetic algorithm (DEAP) evolves genomes that are decoded into minimal pairs of loops.
  - The two programs of a pair share names, data, iteration form and auxiliary statements, and differ only in
    the statement that creates or removes a dependence between iterations.
  - A dynamic dependence oracle executes every loop and confirms its label.
- **Real-world data.** 340 Python loops collected from public repositories, processed and evaluated by the
  researchers, and checked by the same oracle.
- **Models.**
  - DistilBERT (fine-tuned on the source text);
  - the four models of the previous study (logistic regression, linear SVM, DNN and CNN on integer token
    identifiers);
  - a logistic regression on token n-grams.
- **Scenarios.**
  - hybrid (synthetic and real-world loops, 3 × stratified group 10-fold cross-validation);
  - synthetic to real (training on synthetic loops, testing on the 340 real-world loops);
  - real only (3 × stratified group 10-fold cross-validation).

## Repository structure

```text
data/
  synthetic/   Parallelizable_codes.py, Undefined_codes.py: 4,000 minimal pairs (8,000 samples)
               metadata.csv: family, iteration form, wrapper, domain, minimality, tokens, oracle reason, genome
               ga_log.csv, generator_config.json: run of the genetic algorithm; README.md: dataset notes
  real/        Parallelizable_codes.py (176 loops), Undefined_codes.py (164 loops)
               metadata.csv: original class and index, adjudication flag, cross-validation group
               CHANGELOG.md: minimal fixes and adjudicated labels
code/
  generator/   loopgen.py (genome decoder, 9 loop families), ga.py (genetic algorithm),
               oracle.py (dynamic dependence oracle), test_oracle.py (24 hand-labeled cases)
  experiments/ run.py (one model, one scenario), common.py (data and partitions), classic.py (models of
               the previous study and n-gram reference), bert.py (DistilBERT), summarize.py (tables and
               statistics), make_tables.py, figures.py, fig_pipeline.py, fig_graphical_abstract.py,
               launch_cpu.sh, launch_gpu.sh
  audit/       oracle_on_real.py (oracle on the real-world loops, Cohen's kappa),
               real_dependence_types.py (dependence types), synthetic_rules.py (one-line surface rules)
results/
  raw/<scenario>/<model>/rep{r}_fold{k}.npz   validation and test scores of every run
  folds/       partitions of every scenario and repetition
  tables/      CSV files with all numbers reported in the manuscript
  real_dependence_types.csv, real_oracle_before_adjudication.csv, ga_run.log
```

Samples in the `*_codes.py` files are blocks that start with `Code i:` and are separated by a line of 40 `=`
characters. In the synthetic set, `Code i` of the two files form the minimal pair `i`.

## Requirements

Python 3.12 and the packages in `requirements.txt`:

```bash
pip install -r requirements.txt
```

DistilBERT was trained on an NVIDIA GeForce RTX 3050 laptop GPU with 6 GB of memory (about 8 minutes per fold of
the hybrid scenario). The other models run on the CPU.

## Reproducing the study

All commands run from the repository root.

1. **Oracle tests**

   ```bash
   python code/generator/test_oracle.py
   ```

2. **Synthetic data** (optional; `data/synthetic` already holds the set used in the manuscript)

   ```bash
   python code/generator/ga.py --out data/synthetic --seed 42
   ```

3. **Real-world labels and dependence types**

   ```bash
   python code/audit/oracle_on_real.py
   python code/audit/real_dependence_types.py
   ```

4. **Experiments** (optional; `results/raw` already holds every run). Finished folds are skipped, so an
   interrupted run can be started again.

   ```bash
   python code/experiments/run.py --model distilbert --setting hybrid --reps 0 1 2
   # models: lr, svm, dnn, cnn, ngram, distilbert; settings: hybrid, syn2real, real
   bash code/experiments/launch_cpu.sh    # all models except DistilBERT
   bash code/experiments/launch_gpu.sh    # DistilBERT
   ```

5. **Tables, statistics and figures**

   ```bash
   python code/audit/synthetic_rules.py
   python code/experiments/summarize.py
   python code/experiments/make_tables.py
   python code/experiments/figures.py
   ```

   - `summarize.py` writes `results/tables`.
   - `make_tables.py` and the figure scripts write LaTeX table bodies and PDF figures to `latex/`.

## License

MIT License (see `LICENSE`).

## Citation

Data and code (Zenodo):

```bibtex
@software{correia2026loop_parallelizability_classifier,
  author    = {Izavan dos S. Correia and Henrique C. T. Santos and Tiago A. E. Ferreira},
  title     = {IzavanCorreia/loop-parallelizability-classifier: Data and code},
  year      = {2026},
  version   = {v2.0.0},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.21013787},
  url       = {https://doi.org/10.5281/zenodo.21013787}
}
```

Previous study:

```bibtex
@article{correia2026a,
  author  = {Izavan dos S. Correia and Henrique C. T. Santos and Tiago A. E. Ferreira},
  title   = {Discovering software parallelization points using deep neural networks},
  journal = {Array},
  volume  = {30},
  pages   = {100781},
  year    = {2026},
  doi     = {10.1016/j.array.2026.100781}
}
```
