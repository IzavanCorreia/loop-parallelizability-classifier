# Loop parallelizability classification: execution-verified minimal pairs, dependence oracle and DistilBERT

This repository contains the data, code and raw results of the manuscript

**Automatic loop parallelizability classification via contextual code representations: execution-verified
synthetic loops and evaluation on human-written code**
Izavan dos S. Correia, Henrique C. T. Santos, Tiago A. E. Ferreira (manuscript under review).

Version 2.0.5 corresponds to this manuscript. It has the same data, models and raw results as v2.0.0 to v2.0.4
and adds:

- an ablation of the genetic algorithm: random sampling of the same number of genomes, with the same decoder,
  oracle, archive and final selection (`code/generator/random_search.py`, set in `data/synthetic_random`), and
  DistilBERT trained on the random set and compared with the models trained on the set of the genetic algorithm
  (`code/experiments/ga_ablation.py`, `ga_ablation_summary.py`, protocol and results in
  `code/experiments/GA_ABLATION_PROTOCOL.md`). The two sets are equivalent;
- analyses of a review of the text, computed from the existing results: one-line surface rules on the
  human-written loops (`real_rules.json`), the loops that read a neighbor element (`neighbor_reads.csv`), near
  duplicates (`near_duplicates.csv`) and the number of Undefined loops per test fold (`protocol_sizes.csv`).

The manuscript now calls the set of 340 loops written by people *human-written* (it was *real-world* before). In
the code and in the file names it is still called `real`, for example in the settings `syn2real` and `real`.

Version 2.0.4 added a two-stage experiment: DistilBERT fine-tuned on the synthetic pairs first and on the
human-written loops afterwards (`code/experiments/two_stage.py`, protocol in
`code/experiments/TWO_STAGE_PROTOCOL.md`). Versions 2.0.1 to 2.0.3 added the statistical tests, the evolution of
the genetic algorithm, the persistent errors, the score distributions, the tests on the false positive rate and
the accuracy by family (`code/experiments/extra_analyses.py`), and the TikZ diagrams. The releases v1.x contain the
data and code of an earlier version of this work, posted on arXiv (https://arxiv.org/abs/2603.30040).

## Overview

- **Task.** Each sample is a Python function or script with a target loop, labeled *Parallelizable* or
  *Undefined*.
  - A loop is Parallelizable when its iterations can run concurrently and in any order without changing the
    result. Scalars written before being read and not used after the loop, and appends to an output list that is
    not read in the loop (the *map* pattern), are accepted.
  - Accumulators, reductions, recurrences, reads of elements written by other iterations, early exits, `while`
    loops and values used after the loop make a loop Undefined.
  - When loops are nested, the label refers to the outermost loop.
- **Synthetic data.**
  - A decoder turns each genome into a minimal pair of loops. The two programs of a pair share names, data,
    iteration form and auxiliary statements, and differ only in the statement that creates or removes a
    dependence between iterations.
  - A dynamic dependence oracle executes every loop and confirms its label.
  - A genetic algorithm (DEAP) with fitness sharing is the search mechanism over the genomes; random sampling of
    the same number of genomes gives an equivalent set.
- **Human-written data.** 340 short Python snippets collected one by one from public repositories, processed
  and evaluated by the researchers, and checked by the same oracle. The set extends the 338 loops of the previous study (170 Parallelizable and 168 Undefined) with two
  Undefined loops.
- **Models.**
  - DistilBERT (fine-tuned on the source text);
  - the four models of the previous study (logistic regression, linear SVM, DNN and CNN on integer token
    identifiers);
  - a logistic regression on token n-grams.
- **Scenarios.**
  - hybrid (synthetic and human-written loops, 3 × stratified group 10-fold cross-validation);
  - synthetic to human (training on synthetic loops, testing on the 340 human-written loops; `syn2real` in the code);
  - human only (3 × stratified group 10-fold cross-validation; `real` in the code);
  - two-stage training of DistilBERT (the pairs first, then the human-written loops of each human-only fold),
    against human-only training, with 10%, 25%, 50% and 100% of the human-written training loops.

## Repository structure

```text
data/
  synthetic/   Parallelizable_codes.py, Undefined_codes.py: 4,000 minimal pairs (8,000 samples)
               metadata.csv: family, iteration form, wrapper, domain, minimality, tokens, oracle reason, genome
               ga_log.csv, generator_config.json: run of the genetic algorithm; README.md: dataset notes
  synthetic_random/  the same files for the random-sampling ablation (search_log.csv instead of ga_log.csv)
  real/        human-written set: Parallelizable_codes.py (176 loops), Undefined_codes.py (164 loops)
               metadata.csv: original class and index, adjudication flag, cross-validation group
               CHANGELOG.md: minimal fixes and adjudicated labels
code/
  generator/   loopgen.py (genome decoder, 9 loop families), ga.py (genetic algorithm),
               random_search.py (random sampling of genomes, ablation), oracle.py (dynamic dependence oracle),
               test_oracle.py (24 hand-labeled cases)
  experiments/ run.py (one model, one scenario), common.py (data and partitions), classic.py (models of
               the previous study and n-gram reference), bert.py (DistilBERT), summarize.py (tables and
               statistics), make_tables.py, figures.py (data plots), extra_analyses.py (genetic algorithm,
               persistent errors, score distributions, tests on the false positive rate, accuracy by family,
               neighbor reads and near duplicates), fig_pipeline.py and fig_graphical_abstract.py (TikZ
               diagrams: fig_pipeline.tex, graphical_abstract.tex, figstyle.tex, compiled by tikz.py),
               launch_cpu.sh, launch_gpu.sh,
               two_stage.py, two_stage_summary.py, launch_two_stage.sh, TWO_STAGE_PROTOCOL.md (two-stage experiment),
               ga_ablation.py, ga_ablation_summary.py, GA_ABLATION_PROTOCOL.md (ablation of the genetic algorithm)
  audit/       oracle_on_real.py (oracle on the human-written loops, Cohen's kappa),
               real_dependence_types.py (dependence types), synthetic_rules.py (one-line surface rules)
results/
  raw/<scenario>/<model>/rep{r}_fold{k}.npz   validation and test scores of every run
  raw/two_stage/<arm>_f<percent>/rep{r}_fold{k}.npz   the same for the two-stage experiment, plus held-out pair scores
  raw/ga_ablation/<arm>/rep{r}_fold0.npz   scores of the ablation, on the human-written loops and on the other set
  folds/       partitions of every scenario and repetition
  tables/      CSV and JSON files with all numbers reported in the manuscript
  real_dependence_types.csv, real_oracle_before_adjudication.csv, ga_run.log
```

Samples in the `*_codes.py` files are blocks that start with `Code i:` and are separated by a line of 40 `=`
characters. In the synthetic sets, `Code i` of the two files form the minimal pair `i`.

## Requirements

Python 3.12 and the packages in `requirements.txt`:

```bash
pip install -r requirements.txt
```

DistilBERT was trained on an NVIDIA GeForce RTX 3050 GPU with 6 GB of memory (about 8 minutes per fold of
the hybrid scenario). The other models run on the CPU.

The two diagrams (Figure 1 and the graphical abstract) need `pdflatex` with the `pgf`, `standalone` and `dejavu`
packages, on the PATH or in the folder given by the `TEX_BIN` environment variable. The PNG of the graphical
abstract also needs `pypdfium2` (optional).

## Reproducing the study

All commands run from the repository root.

1. **Oracle tests**

   ```bash
   python code/generator/test_oracle.py
   ```

2. **Synthetic data** (optional; `data/synthetic` and `data/synthetic_random` already hold the sets used in the
   manuscript)

   ```bash
   python code/generator/ga.py --out data/synthetic --seed 42
   python code/generator/random_search.py --out data/synthetic_random --seed 42    # ablation, about 2 minutes
   ```

3. **Human-written labels and dependence types**

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
   bash code/experiments/launch_two_stage.sh    # two-stage experiment, about 2 hours on the GPU
   python code/experiments/ga_ablation.py --arm random    # ablation, about 30 minutes on the GPU
   python code/experiments/ga_ablation.py --arm ga        # needs the stage-1 models of two_stage.py
   ```

   The `ga` arm of the ablation scores the three stage-1 models of the two-stage experiment again, which
   `two_stage.py --stage 1` saves in the folder given by `TWO_STAGE_CKPT` (they are not distributed because of
   their size; their scores are in `results/raw/ga_ablation/ga`).

5. **Tables, statistics and figures**

   ```bash
   python code/audit/synthetic_rules.py
   python code/experiments/summarize.py
   python code/experiments/two_stage_summary.py
   python code/experiments/ga_ablation_summary.py
   python code/experiments/make_tables.py
   python code/experiments/figures.py
   python code/experiments/extra_analyses.py
   python code/experiments/fig_pipeline.py
   python code/experiments/fig_graphical_abstract.py
   ```

   - `synthetic_rules.py` writes `synthetic_rules.json` and `real_rules.json`; `summarize.py` writes the other
     tables of `results/tables`; `extra_analyses.py` adds `ga_evolution.csv`, `ga_summary.csv`, `real_errors.csv`,
     `error_summary.csv`, `score_summary.csv`, `tests_fpr.csv`, `family_accuracy.csv`, `neighbor_reads.csv` and
     `near_duplicates.csv`; `two_stage_summary.py` adds `two_stage.csv`, `two_stage_tests.csv`,
     `two_stage_stage1.csv` and `two_stage_checks.csv`; `ga_ablation_summary.py` adds `ga_ablation_data.csv` and
     `ga_ablation_models.csv`.
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
  version   = {v2.0.5},
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
