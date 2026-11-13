# Ablation of the genetic algorithm: protocol

The protocol below was fixed before the runs of this experiment (11/11/2026). Measures added afterwards are listed at
the end.

## Question

Does the genetic algorithm (GA) produce a better set of minimal pairs than random sampling of genomes with the same
budget? "Better" means a more diverse set, and a set from which DistilBERT learns something that transfers to other
pairs and to real-world code.

## Design

- **GA arm:** the published synthetic set (`data/synthetic`, 4,000 pairs), produced by `code/generator/ga.py`.
- **Random arm:** `code/generator/random_search.py`, with the same decoder, oracle, validity checks, archive (at most
  3,000 pairs per family, reservoir sampling) and final selection (`select_pairs`, same seed, 4,000 pairs with the same
  number per family). The genomes are drawn uniformly at random. Budget: the 510,000 genomes the GA evaluated
  (10,000 individuals x 51 evaluations), in 51 batches of 10,000. Output: `data/synthetic_random`.
- **Models:** DistilBERT trained exactly as in the synthetic-to-real scenario: 6,400 training and 1,600 validation
  samples, split by pair, same hyperparameters and seeds (1000 x repetition), 3 repetitions.
  - GA arm: the three stage-1 models of the two-stage experiment (`two_stage_ckpt/stage1_rep*.pt`), which are this
    training on the GA set; they are only scored, not trained again.
  - Random arm: three new models trained on the random set (`code/experiments/ga_ablation.py`).

## Measures

1. **Data:**
   - share of valid genomes and number of distinct valid pairs met during the search;
   - distinct structural signatures per 10,000 genomes (the GA logs this per generation);
   - in the final 4,000 pairs: distinct signatures, distinct structures (code with names and numbers replaced),
     mean minimality and mean number of tokens.
2. **Models, main:** accuracy on the 8,000 samples of the other arm (cross-source), with a threshold of 0.5, and the
   share of pairs with both programs correct. Samples whose code also occurs in the training set of the model are
   left out.
3. **Models, secondary:** accuracy and false positive rate (FPR) on the 340 real-world loops, threshold 0.5.

## Reading the results

- With 3 repetitions there is no test of significance. A difference is reported as a difference only when it is larger
  than the spread between repetitions of both arms; otherwise as no detected difference.
- The accuracy on real-world code of models trained only on pairs varies widely between runs with the same seed
  (stage 1 and the synthetic-to-real scenario differ by up to 29 points on the same seed, because of non-deterministic
  GPU operations). The two runs per seed of the GA arm are both reported to show this spread.

## Checks

- Scoring the stage-1 models again must reproduce their stored scores on the real-world loops
  (`results/raw/two_stage/stage1`).
- The number of samples shared by the two sets is recorded.

## Results (11/11/2026)

Tables: `results/tables/ga_ablation_data.csv` and `results/tables/ga_ablation_models.csv` (`ga_ablation_summary.py`).
Log: `results/logs/ga_ablation.log`; search log: `data/synthetic_random/search_log.csv`.

| | GA | Random |
|---|---|---|
| Valid genomes (mean over the 51 evaluations) | 99.8% | 99.2% |
| Distinct valid pairs met | 452,906 | 505,818 |
| Distinct signatures per 10,000 genomes (mean) | 8,281 | 8,051 |
| Distinct signatures in the final 4,000 pairs | 3,692 | 3,654 |
| Distinct structures in the final 4,000 pairs | 4,000 | 4,000 |
| Mean minimality / mean tokens of the final pairs | 0.956 / 77.6 | 0.956 / 77.0 |
| DistilBERT, accuracy on the 8,000 samples of the other arm | 99.87% ± 0.11 | 99.98% ± 0.03 |
| DistilBERT, both programs right, pairs of the other arm | 99.74% ± 0.21 | 99.95% ± 0.07 |
| DistilBERT, accuracy on the 340 real-world loops | 56.6% ± 10.4 | 52.8% ± 20.9 |
| DistilBERT, FPR on the 340 real-world loops | 34.8% ± 9.4 | 38.8% ± 4.3 |

- **Reading, by the rule above:** no detected difference in any model measure. The GA raises the variety of each
  population a little, but the variety of the final set is almost the same, because it comes from the final selection,
  which takes structurally distinct pairs first.
- **Checks:** the stage-1 models reproduce their stored real-world scores exactly (maximum absolute difference 0.0). The
  two sets share no sample, so nothing was left out of the cross-source evaluation. The synthetic-to-real runs of the
  same seeds reached 73.2%, 51.8% and 45.6% on real code, against 44.7%, 64.1% and 60.9% for stage 1.
