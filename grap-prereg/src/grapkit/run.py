"""python -m grapkit.run [--synthetic]  -> writes reports/ and data/processed/"""
import argparse, os
import pandas as pd
from .pipeline import build_frame, fit_primary, block_bootstrap, save_primary
from .robustness import run_all, decision
from .simulate import make_synthetic

DIWALI = ["2019-10-27", "2020-11-14", "2021-11-04", "2022-10-24", "2023-11-12", "2024-11-01", "2025-10-20"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--synthetic", action="store_true")
    ap.add_argument("--daily", default="data/interim/daily.csv")
    a = ap.parse_args()
    daily = make_synthetic()[0] if a.synthetic else pd.read_csv(a.daily, parse_dates=["date"])
    df = build_frame(daily, DIWALI)
    os.makedirs("data/processed", exist_ok=True); os.makedirs("reports", exist_ok=True)
    df.to_csv("data/processed/model_frame.csv", index=False)
    _, prim = fit_primary(df)
    prim["boot_ci"] = block_bootstrap(df)
    save_primary(prim, "reports/primary_result.json")
    rob = run_all(df, daily, DIWALI)
    rob.to_csv("reports/robustness.csv", index=False)
    print(prim); print(rob.round(2).to_string(index=False)); print(decision(prim, rob))


if __name__ == "__main__":
    main()
