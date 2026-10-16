"""All robustness checks fixed in the preregistration."""
import pandas as pd
from .pipeline import fit_primary, build_frame, CONTROLS


def _row(name, s):
    return dict(check=name, estimate=s["pct_change"], ci_low=s["ci_low"], ci_high=s["ci_high"])


def run_all(df, daily=None, diwali_dates=()):
    rows = []
    for k in (-28, -14, 14, 28):
        d = df.copy()
        d["D"] = d["D"].shift(k).fillna(0)
        rows.append(_row(f"placebo_shift_{k:+d}", fit_primary(d)[1]))
    d = df.copy()
    d["y_lag1_sq"] = d["y_lag1"] ** 2
    d["y_lag1_cu"] = d["y_lag1"] ** 3
    rows.append(_row("flexible_trigger", fit_primary(d, extra=["y_lag1_sq", "y_lag1_cu"])[1]))
    rows.append(_row("ar_1_only", fit_primary(df, controls=[c for c in CONTROLS if c != "y_lag2"])[1]))
    if daily is not None:
        full = build_frame(daily, diwali_dates, drop_diwali=False)
        rows.append(_row("include_diwali", fit_primary(full)[1]))
    d = df.copy()
    d["winter"] = d["date"].apply(lambda x: x.year if x.month >= 10 else x.year - 1)
    for w in sorted(d["winter"].unique()):
        rows.append(_row(f"leave_out_winter_{w}", fit_primary(d[d["winter"] != w])[1]))
    return pd.DataFrame(rows)


def decision(primary, rob):
    placebo_ok = all((r.ci_high >= 0) for r in rob.itertuples() if r.check.startswith("placebo"))
    flex = rob[rob.check == "flexible_trigger"].iloc[0]
    lead_ok = bool(flex.ci_high < 0)
    loo = rob[rob.check.str.startswith("leave_out")]
    sign_ok = (loo.estimate < 0).all() if primary["pct_change"] < 0 else False
    claim = primary["ci_high"] < 0 and placebo_ok and lead_ok and sign_ok
    return dict(primary_ci_below_zero=bool(primary["ci_high"] < 0), placebo_ok=bool(placebo_ok),
                flexible_trigger_ok=bool(lead_ok), loo_sign_stable=bool(sign_ok),
                verdict="consistent with a reduction" if claim else "not robust")
