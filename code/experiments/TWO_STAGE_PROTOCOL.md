# Two-stage experiment: protocol

The protocol below was fixed before the runs of this experiment. Measures added afterwards are listed at the end.

## Question

Does fine-tuning DistilBERT on the synthetic pairs first, and on the real-world loops afterwards, improve the
classification of real code compared with starting directly from the pre-trained DistilBERT weights? Does the answer
change when fewer labeled real-world loops are available?

## Design

- **Stage 1:** DistilBERT on the 8,000 synthetic samples, exactly as in the synthetic-to-real scenario (6,400 training
  and 1,600 validation samples, same seeds). One model per repetition (3). Only synthetic samples are used, so no
  real-world loop is seen and the same model serves all the folds of a repetition.
- **Stage 2:** inside each fold of the real-only scenario (same partitions, 3 x 10 folds), fine-tuning on the real-world
  training loops with the hyperparameters and seed of the real-only scenario (learning rate 2e-5, at most 10 epochs,
  patience 3, real-world validation loops). The two arms differ only in their initial weights:
  - `scratch`: the pre-trained DistilBERT (the real-only scenario);
  - `pretrained`: the stage-1 weights of the same repetition.
- **Sizes of the real-world training set:** 10%, 25%, 50% and 100% of the training portion of the fold (about 25, 61,
  123 and 245 loops), drawn by group within each class, nested across sizes and equal in both arms. Validation and test
  loops do not change.
- **Total:** 2 arms x 4 sizes x 30 folds = 240 runs.

## Measures

1. **Main:** at 100% of the loops, `pretrained` against `scratch`, accuracy and false positive rate (FPR) with a
   threshold of 0.5 on the real-world test loops.
2. **Secondary:**
   - the same measures at 10%, 25% and 50%;
   - recall and FPR with thresholds chosen on the real-world validation loops for targets of 5% and 1%;
   - AUC on the real-world test loops;
   - accuracy and FPR on the 1,600 samples (800 pairs) of the stage-1 validation split, which are held out from training
     and used in stage 1 only for early stopping.

## Statistics

Wilcoxon signed-rank test and corrected resampled t-test (Nadeau and Bengio) over the 30 paired folds. Rates are
pooled per repetition and averaged over the 3 repetitions. Holm correction over the three reduced sizes, separately for
accuracy and FPR.

## Decision rule

- **Helps:** `pretrained` is better with adjusted p < 0.05 in both the Wilcoxon test and the corrected t-test, with no
  significant worsening in the other metric (accuracy or FPR).
- **Worsens:** the same rule in the opposite direction.
- **Any other case:** no detected difference.
- The conclusion is drawn separately for 100% of the loops and for each reduced size.

## Checks

- `scratch` at 100% must repeat `results/raw/real/distilbert`, and stage 1 must repeat `results/raw/syn2real/distilbert`
  (same seeds and partitions). Differences caused by non-deterministic GPU operations are recorded in
  `results/tables/two_stage_checks.csv`, and the comparison uses the two arms run in this experiment.

## Added after the runs

AUC on the held-out pairs, the share of pairs whose Parallelizable program scores above the Undefined one and the mean
absolute score difference inside a pair (`pairs_auc_mean`, `pairs_p_above_u` and `pairs_score_gap` in
`results/tables/two_stage.csv`). They are descriptive measures.
