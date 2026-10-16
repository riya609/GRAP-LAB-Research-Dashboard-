# Did Delhi's GRAP Stage III/IV Reduce PM2.5? A Preregistered, Reproducible Analysis

Turns a public air-quality dataset into a **falsifiable question** and locks the analysis plan *before* outcome patterns are inspected.

| Required proof | Where |
|---|---|
| Preregistration document | `docs/PREREGISTRATION.md` (+ SHA-256 in `docs/PREREG.lock`, changes in `docs/deviations.md`) |
| Reproducible repo | `data/{raw,interim,processed}`, `notebooks/`, `reports/`, `src/grapkit/` |
| Environment lockfile | `requirements.lock` (pinned) |
| Synthetic pipeline test | `tests/test_pipeline.py` + `docs/output_contracts.md` |

## Quick start
```bash
make install && make test      # data-blind pipeline check on synthetic fixtures (planted -12% effect)
make verify                    # confirms prereg is untouched
make synthetic                 # demo run -> reports/
make real                      # after adding data/interim/daily.csv (see docs/DATA_GUIDE.md)
```

## Design in one paragraph
Primary model: OLS on log PM2.5 with GRAP-active indicator, lagged outcome, weather and calendar controls, Newey-West SEs,
plus block bootstrap. Because GRAP is triggered by pollution itself, a verdict of "reduction" requires passing placebo shifts,
a flexible-trigger control, and leave-one-winter-out stability. Otherwise it reports "not robust" - a valid, publishable result.

## What the synthetic check already caught
The data-blind test exposed a flaw in the original plan (a lead-of-exposure test is mechanically non-zero when triggers depend on
lagged outcomes). It was fixed *before* touching real data and logged in `docs/deviations.md` - the workflow working as intended.
