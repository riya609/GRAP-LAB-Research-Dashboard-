# Deviation log
| Timestamp (UTC) | Section changed | What changed | Reason | Before/after outcome look? |
|---|---|---|---|---|
| 2026-10-16 | Analysis plan -> robustness #2, decision rule | Replaced "lead of exposure (t+1)" test with "flexible trigger control" (y_lag1 squared and cubed) | Synthetic pipeline check showed lead test is mechanically non-zero because GRAP triggers depend on lagged AQI | Before any real outcome look (synthetic data only); prereg re-locked as v1.1 |
| 2026-10-16 | Analysis plan -> robustness #1, decision rule | Placebo criterion changed from "CI includes 0" to "no placebo CI entirely below 0" | Synthetic check: clustered pollution episodes give mildly positive placebo estimates; the real risk is a spurious reduction | Before any real outcome look (synthetic only); re-locked as v1.2 |
