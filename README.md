# Automatic Loop Parallelizability Classification via Contextual Code Representations: An Intelligent Code Analysis System with Stability and Low False Positive Rate

This repository provides the data and source code required to reproduce the experiments described in the paper:

**Automatic Loop Parallelizability Classification via Contextual Code Representations: An Intelligent Code Analysis System with Stability and Low False Positive Rate**

Preprint:  
https://arxiv.org/abs/2603.30040

---

## Repository Structure

```text
loop-parallelizability-classifier/
│
├── Datasets/
│   │
│   ├── hybrid/
│   │   ├── Parallelizable_codes.py
│   │   └── Undefined_codes.py
│   │
│   └── real/
│       ├── Parallelizable_codes.py
│       └── Undefined_codes.py
│
├── Processing, model and evaluation/
│   └── Project.py
│
├── LICENSE
└── README.md
```

---

## Dataset Description

### `Datasets/hybrid/`

Contains code sequences representing the hybrid dataset split.

- `Parallelizable_codes.py`: contains loops annotated as parallelizable.
- `Undefined_codes.py`: contains loops annotated as non-parallelizable or undefined.

### `Datasets/real/`

Contains manually curated real code snippets.

- `Parallelizable_codes.py`: contains loops annotated as parallelizable.
- `Undefined_codes.py`: contains loops annotated as non-parallelizable or undefined.

---

## Processing, Model and Evaluation

Directory:

```text
Processing, model and evaluation/
```

Contains:

```text
Project.py
```

The script performs:

1. Dataset loading.
2. Subword tokenization.
3. Training of the DistilBERT-based classifier.
4. Evaluation using 10-fold cross-validation and output of final metrics.

---

## How to Use and Reproduce

### Requirements

Python 3.8+

Install required packages:

```bash
pip install transformers torch scikit-learn
```

---

### Running the Pipeline

Execute from the repository root:

```bash
python "Processing, model and evaluation/Project.py"
```

The script automatically executes the complete pipeline:

1. Loads the datasets from `Datasets/`.
2. Applies subword tokenization.
3. Trains the DistilBERT classifier.
4. Performs 10-fold cross-validation and displays the generated evaluation metrics.

---

## Archived Version (Zenodo)

Archived repository version:

https://doi.org/10.5281/zenodo.21013787

---

## License

This repository is distributed under the MIT License.

See:

```text
LICENSE
```

---

## Citation

If you use this repository, please cite:

### Zenodo Repository

```bibtex
@software{correia2026loop_parallelizability_classifier,
  author    = {Izavan dos S. Correia and Henrique C. T. Santos and Tiago A. E. Ferreira},
  title     = {IzavanCorreia/loop-parallelizability-classifier: Initial Release},
  year      = {2026},
  version   = {v1.1.0},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.21013787},
  url       = {https://doi.org/10.5281/zenodo.21013787}
}
```

### arXiv Preprint

```bibtex
@article{correia2026loop_parallelizability,
  author  = {Izavan dos S. Correia and Henrique C. T. Santos and Tiago A. E. Ferreira},
  title   = {Automatic Identification of Parallelizable Loops Using Transformer-Based Source Code Representations},
  year    = {2026},
  journal = {arXiv},
  url     = {https://arxiv.org/abs/2603.30040}
}
```
