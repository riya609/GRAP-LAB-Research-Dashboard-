# Expected output contracts (verified by `tests/test_pipeline.py`)
| Artifact | Contract |
|---|---|
| `data/interim/daily.parquet`/`.csv` | one row per date, unique, sorted; columns: date, pm25, grap_stage, wind, blh, temp, rh, precip |
| `data/processed/model_frame.csv` | no NaN; has `y`, `D`, `y_lag1`, `y_lag2` and all controls |
| `reports/primary_result.json` | keys: beta, pct_change, ci_low, ci_high, n, hac_lags |
| `reports/robustness.csv` | columns: check, estimate, ci_low, ci_high |
| Synthetic recovery | planted effect of -12% recovered within +/-4 percentage points; placebo CIs cover 0 |
