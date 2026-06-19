# Emotional Debt — Replication Package

Replication package for the paper:

> **Can We Empirically Trace How Burnout Turns into Emotional Debt and Emotional Smells?**  
> Giammaria Giordano, Francesco Maria Torino, Fabio Palomba  
> Pegaso University · University of Salerno, 2026

## Website

The interactive replication package is published at:

**https://giammariagiordano.github.io/emotional_smell/**

The site presents the abstract, conceptual model, all PLS-SEM results, survey constructs, and step-by-step replication instructions.

## What This Repository Contains

```
emotional_smell/
├── index.html                        # GitHub Pages site (single-page app)
├── Emotional Debt.pdf                # Paper (preprint)
└── replication-package/
    ├── Data/
    │   ├── survey.csv                # Raw Qualtrics export
    │   └── survey_pls.csv            # Cleaned dataset ready for SmartPLS
    ├── Scripts/
    │   └── format_for_plssem.py      # Data preparation pipeline
    ├── Survey/
    │   └── Qualtrics Survey Software.pdf   # Survey instrument
    ├── Pls-sem/
    │   ├── SmartPls project/         # SmartPLS 4 project files (.splsm, .splsrp)
    │   └── Exports/                  # Raw SmartPLS output spreadsheets
    └── Conceptual/
        └── Tesi progetto.pdf         # Conceptual model diagram
```

## How to Replicate the Analysis

### 1. Prerequisites

- Python 3.8+ with `pandas` and `numpy`
- [SmartPLS 4](https://www.smartpls.com/) (free academic license available)

### 2. Data Preparation

```bash
pip install pandas numpy

python "replication-package/Scripts/format_for_plssem.py" \
  --in  "replication-package/Data/survey.csv" \
  --out "replication-package/Data/survey_pls.csv"
```

The script auto-detects the data start row, filters incomplete responses, applies attention-check filters, selects construct columns, and outputs a clean CSV.

### 3. PLS-SEM in SmartPLS 4

1. Open the `.splsm` project from `Pls-sem/SmartPls project/`
2. Run **PLS Algorithm** — verify outer loadings > 0.70, AVE > 0.50
3. Run **Bootstrapping** — 5,000 subsamples, two-tailed, α = 0.05
4. Run **PLSpredict** — verify PLS RMSE < LM RMSE for all indicators
5. Compare your output against the spreadsheets in `Pls-sem/Exports/`

### 4. Key Results to Verify

| Path | β | T-value | p-value |
|------|---|---------|---------|
| Burnout → Emotional Debt | 0.783 | 17.233 | < 0.001 |
| Burnout → Emotional Smells | 0.618 | 7.938 | < 0.001 |
| Emotional Debt → Emotional Smells | 0.432 | 2.670 | 0.008 |

R² Emotional Debt = 0.613 · R² Emotional Smells = 0.454 · Mediation: **partial**

## Citation

```bibtex
@inproceedings{giordano2026emotionaldebt,
  title     = {Can We Empirically Trace How Burnout Turns into Emotional Debt and Emotional Smells?},
  author    = {Giordano, Giammaria and Torino, Francesco Maria and Palomba, Fabio},
  year      = {2026},
  note      = {Replication package: https://giammariagiordano.github.io/emotional_smell/}
}
```

## Contact

Giammaria Giordano — giammaria.giordano@unipegaso.it
