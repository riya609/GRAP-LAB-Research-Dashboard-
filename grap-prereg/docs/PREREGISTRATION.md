# Analysis Preregistration

**Project:** Did Delhi's GRAP Stage III/IV restrictions reduce PM2.5 after accounting for weather?
**Status:** LOCKED before any outcome-versus-exposure relationship is inspected. Hash in `docs/PREREG.lock`.
**Version:** 1.2 (see deviations.md entries 1-2: pre-data fixes from the synthetic check)

## Research question
Among winter days (1 Oct - 28 Feb) in Delhi-NCR, does a day under active GRAP Stage III or IV restrictions have lower
PM2.5 than comparable days without those restrictions, after adjusting for meteorology and recent pollution history?

Falsifiable form: the adjusted effect of GRAP Stage III+ on log daily PM2.5 is negative, and its 95% CI excludes zero.
If the CI includes zero or the estimate is positive, the hypothesis is not supported.

## Hypotheses
- **H0:** beta_GRAP = 0 (no adjusted association between active Stage III+ and next-day log PM2.5).
- **H1:** beta_GRAP < 0 (expected direction: restrictions on construction, trucks and diesel generators lower PM2.5).
- Two-sided test at alpha = 0.05 for inference. The one-sided direction is stated only as the expectation.
- Secondary (descriptive, no confirmatory claim): effect is larger at Stage IV than Stage III.

**Causal caveat declared in advance:** stages are triggered by forecast/observed AQI, so exposure is confounded by
pollution level. We therefore estimate a *conditional association with lagged-outcome adjustment*, and call it a
causal effect only if the robustness checks below all agree.

## Population, sample, and exclusions
- **Target population:** Delhi-NCR ambient air, winter season.
- **Unit of analysis:** city-day (mean of all CPCB stations reporting in Delhi, >= 75% of stations required per day).
- **Observation window:** 1 Oct 2019 - 28 Feb 2026, winter days only (GRAP in current form began Oct 2017; 2017-18
  excluded because stage definitions changed).
- **Inclusion:** days with valid PM2.5 and all meteorology covariates.
- **Exclusions:** (a) days with < 75% station coverage; (b) the 3 days around Diwali (day of, +/-1) because fireworks are an
  unmodelled shock - kept in a robustness run instead; (c) 2020-03-24 to 2020-06-30 (COVID lockdown) is outside winter anyway,
  but the 2020-21 winter is retained and flagged.
- **Stopping rule:** fixed window above. No data are added or dropped after the first outcome-exposure look.

## Variables and measures
- **Outcome Y:** log(PM2.5 at day t), daily mean ug/m3, CPCB.
- **Exposure D:** 1 if GRAP Stage III or IV was in force on day t (from CAQM orders), else 0.
- **Predictors / controls X:** log PM2.5 at t-1 and t-2, 10 m wind speed, boundary-layer height, 2 m temperature,
  relative humidity, precipitation (ERA5 daily means), day-of-week dummies, winter-month dummies, linear year trend.
- **Transformations:** natural log for PM2.5; wind speed and boundary-layer height log-transformed; continuous covariates
  standardised using training-window means (whole sample, fixed here).
- **Missing data:** meteorology gaps <= 2 days linearly interpolated; larger gaps -> row dropped. PM2.5 never imputed.
  Report the count of dropped days.

## Analysis plan
- **Primary model:** OLS of Y on D and X with Newey-West (HAC) standard errors, 5 lags.
- **Assumption checks:** residual autocorrelation (Ljung-Box), heteroskedasticity (Breusch-Pagan), VIF < 10, influence (Cook's D).
- **Alpha:** 0.05, two-sided.
- **Effect size:** percent change = 100 * (exp(beta_D) - 1) with 95% CI from the HAC interval. R^2 and partial R^2 of D reported.
- **Uncertainty:** HAC 95% CI plus 2,000-replicate moving-block bootstrap (block length 7 days) CI for the percent change.
- **Robustness checks (all fixed now):**
  1. Placebo exposure: shift D by +/-14 and +/-28 days (expect ~0 or positive, never a clear reduction).
  2. Flexible trigger control: add squared and cubed log PM2.5 at t-1, because stages are triggered by lagged AQI
     thresholds (a lead-of-exposure test is NOT used: the trigger depends on the outcome series, so leads are mechanically
     correlated - found during the synthetic pipeline check, see `docs/deviations.md`).
  3. Placebo shifts above serve as the negative control.
  4. Alternative lags (AR 1 vs AR 1-3).
  5. Include Diwali days.
  6. Leave-one-winter-out: refit dropping each winter; report range of beta_D.
  7. Stage IV-only vs Stage III-only coefficients (secondary).
- **Decision rule:** Claim "consistent with a reduction" only if the primary CI is < 0 AND no placebo CI lies entirely below 0 (episodes cluster in time, so a positive placebo is expected; a spurious *reduction* is the failure we guard against) AND the
  flexible-trigger estimate is still < 0 (CI upper bound < 0) AND the leave-one-out sign never flips. Otherwise report as "not robust".
- **Multiple comparisons:** one confirmatory test (primary). All else labelled exploratory/robustness.

## Deviations
Record every later deviation from this plan in `docs/deviations.md` with a timestamp and reason.
Never edit this file after locking; the lock hash will no longer match.
