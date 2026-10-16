# GRAP-LAB | Air Quality Research Dashboard

An interactive research dashboard for exploring Graded Response Action Plan (GRAP) interventions and PM2.5-related statistical analysis.

## Overview

GRAP-LAB is a Python and Streamlit-based research project designed to present statistical results, robustness checks, and visual summaries through an interactive web interface.

The dashboard organizes analysis outputs into accessible sections to support exploratory analysis and transparent reporting.

> **Research data notice:** The currently included results are synthetic demonstration data. They are intended to demonstrate the dashboard and analysis workflow, not to establish real-world effects of GRAP interventions or represent verified Delhi air-quality observations.

## Key Features

- **Overview:** A summary of the analysis and key indicators.
- **Primary Analysis:** Presentation of the primary statistical estimate and its confidence interval.
- **Robustness Checks:** Comparison of estimates across alternative analysis checks.
- **Interactive Visualizations:** Graphs and tables for exploring reported results.
- **Downloads:** Access to available analysis outputs.
- **Research Transparency:** Clear distinction between demonstration results and real-world evidence.

## Technology Stack

- Python
- Streamlit
- Pandas
- NumPy
- Matplotlib
- JSON and CSV for analysis outputs
- Git and GitHub for version control

## Project Structure

```text
grap-prereg-project/
├── app.py
├── requirements.txt
├── README.md
└── grap-prereg/
    ├── data/
    ├── docs/
    ├── notebooks/
    ├── reports/
    │   ├── primary_result.json
    │   ├── robustness.csv
    │   └── figures/
    ├── scripts/
    ├── src/
    ├── tests/
    └── README.md
```

## Run Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/riya609/GRAP-LAB-Research-Dashboard-.git
   cd GRAP-LAB-Research-Dashboard-
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   ```

   Windows PowerShell:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the dashboard:

   ```bash
   streamlit run app.py
   ```

## Research Methodology

The dashboard displays a primary statistical estimate, its confidence interval, and robustness-check results using the supplied analysis output files.

Interpretation should consider the underlying data, study design, assumptions, uncertainty, and limitations. The current synthetic outputs are for demonstration only and should not be treated as empirical findings.

## Limitations and Future Work

- Replace synthetic demonstration outputs with verified, appropriately documented observations before making empirical claims.
- Document data sources, collection periods, variable definitions, and preprocessing steps.
- Explain the statistical model, assumptions, and confidence-interval methodology.
- Add reproducible evaluation and automated tests for the analysis pipeline.
- Include clearly labelled dashboard screenshots and verified results.

## Disclaimer

This project is intended for research exploration and educational demonstration. It does not establish that GRAP interventions caused a change in PM2.5 levels. Conclusions about real-world effects require suitable empirical data and a defensible research design.

## Author

**Riya Maheshwari**  
B.Tech — Computer Science and Engineering (Data Science)

GitHub: [riya609](https://github.com/riya609)
