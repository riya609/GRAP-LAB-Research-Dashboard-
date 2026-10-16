import json, numpy as np, pandas as pd
from grapkit.simulate import make_synthetic
from grapkit.pipeline import build_frame, fit_primary, CONTROLS
from grapkit.robustness import run_all

DIWALI = ["2019-10-27", "2020-11-14"]


def frame():
    daily, true_pct = make_synthetic()
    return daily, build_frame(daily, DIWALI), true_pct


def test_interim_contract():
    daily, _, _ = frame()
    assert daily["date"].is_unique and daily["date"].is_monotonic_increasing
    for c in ["date", "pm25", "grap_stage", "wind", "blh", "temp", "rh", "precip"]:
        assert c in daily.columns


def test_model_frame_contract():
    _, df, _ = frame()
    assert not df[["y", "D"] + CONTROLS].isna().any().any()
    assert set(df["D"].unique()) <= {0, 1}


def test_lags_only_link_consecutive_days():
    _, df, _ = frame()
    prev = np.log(pd.Series(make_synthetic()[0].set_index("date")["pm25"]))
    chk = df.set_index("date")
    expected = prev.shift(1).reindex(chk.index)
    assert np.allclose(chk["y_lag1"], expected, equal_nan=False)


def test_recovers_planted_effect():
    """Average over seeds (single draws are noisy with ~4% treated days); also check CI coverage."""
    est, cover = [], 0
    for seed in range(1, 9):
        daily, true_pct = make_synthetic(seed=seed)
        _, s = fit_primary(build_frame(daily, DIWALI))
        est.append(s["pct_change"]); cover += s["ci_low"] <= true_pct <= s["ci_high"]
    assert abs(np.mean(est) - true_pct) < 3.0
    assert cover >= 5   # HAC CIs mildly under-cover with ~4% treated days; the prereg adds a block-bootstrap CI


def test_placebos_show_no_spurious_reduction():
    daily, df, _ = frame()
    rob = run_all(df, daily, DIWALI)
    pl = rob[rob.check.str.startswith("placebo")]
    assert len(pl) == 4
    assert (pl.ci_high >= 0).all()


def test_robustness_contract():
    daily, df, _ = frame()
    rob = run_all(df, daily, DIWALI)
    assert list(rob.columns) == ["check", "estimate", "ci_low", "ci_high"]
