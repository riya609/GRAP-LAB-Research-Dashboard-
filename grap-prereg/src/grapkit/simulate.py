"""Synthetic fixture generator with a KNOWN planted effect. Used for the data-blind pipeline check."""
import numpy as np
import pandas as pd


def make_synthetic(true_pct=-12.0, years=8, seed=7):
    rng = np.random.default_rng(seed)
    dates = []
    for y in range(2019, 2019 + years):
        dates.append(pd.date_range(f"{y}-10-01", f"{y+1}-02-28"))
    dates = pd.DatetimeIndex(np.concatenate([d.values for d in dates]))
    n = len(dates)
    wind = np.clip(rng.gamma(4, 0.5, n), 0.2, None)
    blh = np.clip(rng.normal(600, 200, n), 80, None)
    temp = 15 - 8 * np.cos((dates.dayofyear - 20) / 365 * 2 * np.pi) + rng.normal(0, 2, n)
    rh = np.clip(rng.normal(60, 15, n), 10, 100)
    precip = np.clip(rng.exponential(0.4, n) * (rng.random(n) < 0.12), 0, None)
    beta_true = np.log(1 + true_pct / 100)
    # latent "stagnation" drives both pollution and the trigger, so there is real confounding
    stag = np.zeros(n)
    y = np.zeros(n)
    D = np.zeros(n)
    y[0] = 4.0
    for t in range(1, n):
        stag[t] = 0.6 * stag[t - 1] + rng.normal(0, 1)
        D[t] = 1.0 if (y[t - 1] > 4.2 and rng.random() < 0.8) else 0.0
        y[t] = (
            1.4 + 0.65 * y[t - 1]
            - 0.18 * np.log(wind[t]) - 0.15 * np.log(blh[t] / 600)
            - 0.01 * (temp[t] - 10) + 0.004 * (rh[t] - 60) - 0.4 * precip[t]
            + 0.05 * stag[t] + beta_true * D[t] + rng.normal(0, 0.18)
        )
    df = pd.DataFrame(dict(date=dates, pm25=np.exp(y), grap_stage=np.where(D == 1, 3, 0),
                           wind=wind, blh=blh, temp=temp, rh=rh, precip=precip))
    return df, true_pct
