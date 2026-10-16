"""Preregistered pipeline: clean -> features -> primary model. No outcome-conditional choices allowed here."""
import json
import numpy as np
import pandas as pd
import statsmodels.api as sm

HAC_LAGS = 5
CONTROLS = ["y_lag1", "y_lag2", "ln_wind", "ln_blh", "temp", "rh", "precip", "trend"]


def diwali_mask(dates, diwali_dates):
    dates = pd.Series(pd.to_datetime(dates)).reset_index(drop=True)
    m = pd.Series(False, index=dates.index)
    for d in pd.to_datetime(diwali_dates):
        m |= ((dates - d).abs().dt.days <= 1)
    return m.values


def build_frame(daily, diwali_dates=(), drop_diwali=True):
    df = daily.sort_values("date").drop_duplicates("date").reset_index(drop=True).copy()
    df["date"] = pd.to_datetime(df["date"])
    for c in ["wind", "blh", "temp", "rh", "precip"]:
        df[c] = df[c].interpolate(limit=2, limit_direction="both")
    df["y"] = np.log(df["pm25"])
    df["y_lag1"] = df["y"].shift(1)
    df["y_lag2"] = df["y"].shift(2)
    df["D"] = (df["grap_stage"] >= 3).astype(int)
    df["ln_wind"] = np.log(df["wind"])
    df["ln_blh"] = np.log(df["blh"])
    df["trend"] = (df["date"].dt.year - df["date"].dt.year.min()).astype(float)
    # lag columns must only link consecutive days
    gap = df["date"].diff().dt.days != 1
    df.loc[gap, "y_lag1"] = np.nan
    df.loc[gap | gap.shift(1, fill_value=False), "y_lag2"] = np.nan
    if drop_diwali and len(diwali_dates):
        df = df[~diwali_mask(df["date"], diwali_dates)]
    df = df.dropna(subset=["y", "D"] + CONTROLS).reset_index(drop=True)
    return df


def design(df, extra=(), controls=None):
    controls = CONTROLS if controls is None else controls
    X = df[["D"] + list(extra) + list(controls)].copy()
    dow = pd.get_dummies(df["date"].dt.dayofweek, prefix="dow", drop_first=True).astype(float)
    mon = pd.get_dummies(df["date"].dt.month, prefix="mon", drop_first=True).astype(float)
    X = pd.concat([X, dow, mon], axis=1)
    return sm.add_constant(X.astype(float), has_constant="add")


def fit_primary(df, extra=(), controls=None, lags=HAC_LAGS, coef="D"):
    X = design(df, extra, controls)
    res = sm.OLS(df["y"], X).fit(cov_type="HAC", cov_kwds={"maxlags": lags})
    b = res.params[coef]
    lo, hi = res.conf_int().loc[coef]
    return res, dict(beta=float(b), pct_change=float(100 * (np.exp(b) - 1)),
                     ci_low=float(100 * (np.exp(lo) - 1)), ci_high=float(100 * (np.exp(hi) - 1)),
                     n=int(res.nobs), hac_lags=lags)


def block_bootstrap(df, B=2000, block=7, seed=1):
    rng = np.random.default_rng(seed)
    n = len(df)
    nb = int(np.ceil(n / block))
    out = []
    X = design(df).values
    y = df["y"].values
    j = list(design(df).columns).index("D")
    for _ in range(B):
        starts = rng.integers(0, n - block, nb)
        idx = np.concatenate([np.arange(s, s + block) for s in starts])[:n]
        try:
            beta = np.linalg.lstsq(X[idx], y[idx], rcond=None)[0][j]
        except np.linalg.LinAlgError:
            continue
        out.append(100 * (np.exp(beta) - 1))
    return float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5))


def save_primary(summary, path):
    with open(path, "w") as f:
        json.dump(summary, f, indent=2)
