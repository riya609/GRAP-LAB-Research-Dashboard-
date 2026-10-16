
from pathlib import Path
import json

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


# ---------- PROJECT PATHS: PRESERVED ----------
ROOT = Path(__file__).resolve().parent / "grap-prereg"
REPORTS = ROOT / "reports"
RESULT_FILE = REPORTS / "primary_result.json"
ROBUST_FILE = REPORTS / "robustness.csv"


# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="GRAP Research Dashboard",
    page_icon="🌫️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------- PREMIUM NAVY + TEAL THEME ----------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0b1220, #101b2d);
        color: #edf4ff;
    }

    [data-testid="stSidebar"] {
        background: #0a1120;
        border-right: 1px solid #24344b;
    }

    [data-testid="stMetric"] {
        background: #162338;
        border: 1px solid #2a405a;
        padding: 18px;
        border-radius: 14px;
    }

    [data-testid="stMetricLabel"] {
        color: #a9bdd4;
    }

    [data-testid="stMetricValue"] {
        color: #55e0c0;
    }

    h1, h2, h3 {
        color: #f2f7ff;
    }

    div[data-testid="stAlert"] {
        border-radius: 12px;
    }

    div[data-testid="stDownloadButton"] button {
        background: #123d43;
        color: white;
        border: 1px solid #2dd4bf;
        border-radius: 9px;
    }

    div[data-testid="stDownloadButton"] button:hover {
        background: #17615f;
        color: white;
        border-color: #55e0c0;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid #2a405a;
        border-radius: 10px;
        overflow: hidden;
    }

    hr {
        border-color: #2a405a;
    }

    .section-note {
        color: #9fb2c8;
        font-size: 0.9rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------- SIDEBAR NAVIGATION ----------
st.sidebar.markdown(
    """
    <div style="padding:12px 4px 20px 4px;">
        <h2 style="color:#55E0C0; margin-bottom:4px;">
            GRAP<span style="color:#F2F7FF;">.LAB</span>
        </h2>
        <p style="color:#9FB2C8; font-size:12px;">
            AIR QUALITY RESEARCH
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Overview",
        "Primary Analysis",
        "Robustness Checks",
        "Downloads",
    ],
    key="navigation_page",
)

st.sidebar.markdown("---")
st.sidebar.caption("Research prototype • Synthetic demo")


# ---------- DASHBOARD HEADER ----------
st.title("🌫️ Delhi GRAP & PM2.5 Research Dashboard")
st.caption("Preregistered statistical analysis | Research prototype")

st.warning(
    "SYNTHETIC DEMO: Current report values are from simulated data. "
    "They are not estimates from real Delhi air-quality observations."
)


# ---------- CHECK REPORT FILES ----------
if not RESULT_FILE.exists():
    st.error(f"Primary result file not found: {RESULT_FILE}")
    st.stop()

if not ROBUST_FILE.exists():
    st.error(f"Robustness file not found: {ROBUST_FILE}")
    st.stop()


# ---------- LOAD EXISTING REPORTS ----------
try:
    with open(RESULT_FILE, encoding="utf-8") as f:
        result = json.load(f)

    robust = pd.read_csv(ROBUST_FILE)

    pct = float(result["pct_change"])
    low = float(result["ci_low"])
    high = float(result["ci_high"])

except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
    st.error(f"Unable to load the research reports: {exc}")
    st.stop()


# ---------- ROBUSTNESS FILTER ----------
if "check" in robust.columns:
    available_checks = (
        robust["check"].dropna().astype(str).unique().tolist()
    )

    selected_checks = st.sidebar.multiselect(
        "ROBUSTNESS FILTER",
        options=available_checks,
        default=available_checks,
        help="Select the robustness checks shown in the graph and table.",
        key="robustness_filter",
    )

    filtered_robust = robust[
        robust["check"].astype(str).isin(selected_checks)
    ].copy()

else:
    filtered_robust = robust.copy()
    st.sidebar.info(
        "The check column is missing. Showing all available rows."
    )


# ---------- OVERVIEW PAGE ----------
if page == "Overview":
    st.subheader("Primary Model Results")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Estimated PM2.5 change",
        f"{pct:.2f}%",
    )

    c2.metric(
        "95% confidence interval",
        f"{low:.2f}% to {high:.2f}%",
    )

    c3.metric(
        "Observations",
        f"{int(result['n']):,}",
    )

    c4.metric(
        "HAC lags",
        str(result["hac_lags"]),
    )

    st.divider()

    st.subheader("Research Summary")

st.caption("Key findings from the current research prototype")

# Summary KPI cards
s1, s2 = st.columns(2)

with s1:
    st.markdown("#### Estimated PM2.5 change")
    st.metric("Model estimate", f"{pct:.2f}%")

with s2:
    st.markdown("#### 95% confidence interval")
    st.metric("Reported interval", f"{low:.2f}% to {high:.2f}%")

s3, s4 = st.columns(2)

with s3:
    st.markdown("#### Observations")
    st.metric("Reported sample size", f"{int(result['n']):,}")

with s4:
    st.markdown("#### Robustness review")
    st.metric("Status", "Review required")

st.divider()

st.markdown("### Key Finding")

if high < 0:
    st.success(
        "The reported confidence interval lies entirely below zero, "
        "indicating a negative association in the fitted model."
    )
elif low > 0:
    st.info(
        "The reported confidence interval lies entirely above zero, "
        "indicating a positive association in the fitted model."
    )
else:
    st.info(
        "The reported confidence interval crosses zero. "
        "The estimate is not clearly distinguishable from zero "
        "at the 95% confidence level."
    )

st.markdown("### Research Limitations")

st.warning(
    "Current results use simulated data, not real Delhi air-quality "
    "observations. The model does not establish causation. "
    "Review the robustness checks, data quality and potential "
    "confounding factors before drawing conclusions."
)

st.caption(
    "Source: Existing primary_result.json and project reports."
)

# ---------- PRIMARY ANALYSIS PAGE ----------
if page == "Primary Analysis":
    st.subheader("1. Primary Effect Estimate")

    fig, ax = plt.subplots(figsize=(10, 3.2))

    ax.errorbar(
        pct,
        0,
        xerr=[[pct - low], [high - pct]],
        fmt="o",
        capsize=7,
        markersize=8,
    )

    ax.axvline(0, linestyle="--")
    ax.set_yticks([0])
    ax.set_yticklabels(["GRAP estimate"])
    ax.set_xlabel("Estimated percentage change in PM2.5")
    ax.set_title("Primary estimate with 95% confidence interval")
    ax.grid(axis="x", alpha=0.25)

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.caption(
        "A confidence interval entirely below zero indicates a negative "
        "estimated association in this model; it does not by itself "
        "establish causation."
    )

    st.divider()

    # Interpretation is intentionally on the Primary Analysis page.
    st.subheader("2. Automatic Result Interpretation")

    if high < 0:
        st.write(
            f"The primary model estimates a {abs(pct):.2f}% reduction. "
            f"Its reported confidence interval ranges from "
            f"{low:.2f}% to {high:.2f}%, entirely below zero."
        )

    elif low > 0:
        st.write(
            "The primary model estimates a positive change, "
            "with the reported confidence interval entirely above zero."
        )

    else:
        st.write(
            "The reported confidence interval crosses zero, so the "
            "primary estimate is not clearly distinguishable from zero "
            "at the 95% level."
        )

    st.info(
        "Interpretation is conditional on the model and data. "
        "Robustness checks, the preregistered decision rule, data quality "
        "and confounding factors must also be considered before drawing "
        "a conclusion."
    )


# ---------- ROBUSTNESS CHECKS PAGE ----------
elif page == "Robustness Checks":
    st.subheader("1. Robustness Analysis")

    required_columns = {
        "check",
        "estimate",
        "ci_low",
        "ci_high",
    }

    if not required_columns.issubset(filtered_robust.columns):
        missing = required_columns - set(filtered_robust.columns)

        st.error(
            "The robustness report is missing required columns: "
            + ", ".join(sorted(missing))
        )

    elif filtered_robust.empty:
        st.info(
            "No robustness checks are selected. "
            "Choose one or more checks in the sidebar filter."
        )

    else:
        data = filtered_robust.dropna(
            subset=["check", "estimate", "ci_low", "ci_high"]
        ).copy()

        data = data.iloc[::-1].reset_index(drop=True)

        if data.empty:
            st.info("The selected robustness checks have no complete rows.")

        else:
            # Validate confidence intervals before plotting.
            valid = (
                (data["ci_low"] <= data["estimate"])
                & (data["estimate"] <= data["ci_high"])
            )

            if not valid.all():
                st.warning(
                    "Some rows have estimates outside their confidence "
                    "intervals. Those rows are excluded from the graph."
                )
                data = data.loc[valid].reset_index(drop=True)

            if not data.empty:
                fig2, ax2 = plt.subplots(
                    figsize=(10, max(4, len(data) * 0.42))
                )

                y = list(range(len(data)))

                ax2.errorbar(
                    data["estimate"],
                    y,
                    xerr=[
                        data["estimate"] - data["ci_low"],
                        data["ci_high"] - data["estimate"],
                    ],
                    fmt="o",
                    capsize=3,
                )

                ax2.axvline(0, linestyle="--")
                ax2.set_yticks(y)
                ax2.set_yticklabels(data["check"])
                ax2.set_xlabel("Estimated percentage change")
                ax2.set_title(
                    "Robustness checks with confidence intervals"
                )
                ax2.grid(axis="x", alpha=0.25)

                fig2.tight_layout()
                st.pyplot(fig2)
                plt.close(fig2)

    # The robustness table belongs on this page, not Downloads.
    st.divider()
    st.subheader("2. Robustness Results Table")

    st.dataframe(
        filtered_robust,
        use_container_width=True,
        hide_index=True,
    )

    st.caption(
        "The filter above controls which checks are displayed. "
        "Estimates are based on the existing research report."
    )


# ---------- DOWNLOADS PAGE ----------
elif page == "Downloads":
    st.subheader("Research Output Downloads")

    st.write(
        "Download the existing research outputs for review, "
        "reproducibility and academic presentation."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            "Download primary result (JSON)",
            data=RESULT_FILE.read_bytes(),
            file_name="primary_result.json",
            mime="application/json",
            use_container_width=True,
        )

    with col2:
        st.download_button(
            "Download robustness results (CSV)",
            data=ROBUST_FILE.read_bytes(),
            file_name="robustness.csv",
            mime="text/csv",
            use_container_width=True,
        )

    st.divider()

    st.subheader("Export Preview")
    st.caption("Primary result file")
    st.json(result)

    st.caption("Robustness results preview")
    st.dataframe(
        filtered_robust,
        use_container_width=True,
        hide_index=True,
    )


# ---------- FOOTER ----------
st.divider()

st.caption(
    "GRAP.LAB | Research prototype | Academic and internship demonstration"
)
