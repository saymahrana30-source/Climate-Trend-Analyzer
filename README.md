# 🌍 Climate Trend Analyzer

An end-to-end data science project that analyzes 50 years (1975-2024) of climate data across four regions to uncover **long-term warming trends, seasonal patterns, extreme-weather anomalies, and 10-year forecasts**.

> **Data note:** built with a *virtual simulation* of NASA/NOAA-style station data (seasonality + warming trend + noise + deliberately messy values), so the full pipeline runs without institutional access. Replace `data/raw/climate_raw.csv` with real data using the same columns to analyze real records.

## 🎯 Problem Statement
Governments, agritech firms, energy utilities and city planners need to know *how fast* a region is warming, *when* extreme events occur, and *what to expect next*. This project turns raw, messy climate records into clear, decision-ready insights.

## 🛠 Tech Stack
Python · Pandas · NumPy · Matplotlib · Seaborn · SciPy · Statsmodels (STL, ARIMA) · Scikit-learn (Linear Regression, Isolation Forest) · Plotly · Streamlit · Pytest

## 🏗 Architecture
```
Simulated data → Cleaning → EDA charts → Trend analysis → Anomaly detection → Forecasting → Report + Dashboard
 (src/data_generator) (preprocessing) (eda) (trend_analysis) (anomaly_detection) (forecasting)  (report / app)
```

## 📁 Folder Structure
```
Climate-Trend-Analyzer/
├── app/streamlit_app.py      # interactive dashboard
├── data/raw | processed      # raw simulated CSV and cleaned CSV
├── docs/                     # architecture + interview guide
├── outputs/figures | tables  # 12 charts and 4 result tables
├── reports/insights_report.md
├── screenshots/terminal | code
├── src/                      # config, data_generator, preprocessing, eda,
│                             # trend_analysis, anomaly_detection, forecasting, report
├── tests/test_pipeline.py    # 6 automated tests
├── main.py                   # one command runs everything
└── requirements.txt
```

## ⚙️ Installation
Python 3.10+ recommended.

**Windows (PowerShell)**
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
**Mac / Linux**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## ▶️ How to Run
```bash
python main.py                      # full pipeline (default region: Gujarat-West India)
python main.py --region "Sahel Africa"
pytest -v                           # run tests
streamlit run app/streamlit_app.py  # launch dashboard
```
Outputs: `outputs/figures/*.png`, `outputs/tables/*.csv`, `reports/insights_report.md`.

## 🧪 Simulation Workflow
1. **Generate** monthly data for 4 regions: temperature = base + seasonal sine wave + warming trend + noise; monsoon-shaped rainfall; humidity linked to rain; global CO₂ and sea-level series.
2. **Inject realities:** ~2% missing values, `-99` sensor error codes, 25 duplicate rows.
3. **Inject ground-truth events:** heatwaves, cold snaps, extreme-rain months (so detection can be *measured*).
4. **Clean:** dedupe, parse dates, replace error codes, time-aware interpolation.
5. **Analyze:** trends → anomalies → forecasts → report.

## 📊 Results (default run)
| Finding | Result |
|---|---|
| Regional warming | All 4 regions significantly warming (p < 0.001); fastest **Northern Europe +0.35 °C/decade** |
| CO₂ vs temperature | r = 0.93 (annual means) |
| Anomaly detection | 25 anomalous months; **precision 84%, recall 88%** vs injected events |
| Forecast (10-yr holdout) | Linear Regression RMSE ≈ 0.26 °C vs ARIMA ≈ 0.27 °C (Gujarat-West India) |

Full table: [`reports/insights_report.md`](reports/insights_report.md)

> Honest caveats: anomaly thresholds were tuned on the simulated data, and on this smooth synthetic series simple linear regression performs as well as ARIMA. Real data would be noisier and favor richer models.

## 📸 Screenshots
**Charts**

| Temperature trend | Anomalies | Forecast |
|---|---|---|
| ![](outputs/figures/01_temperature_trend.png) | ![](outputs/figures/11_anomaly_detection.png) | ![](outputs/figures/12_forecast.png) |

**Terminal & code proof** → see [`screenshots/`](screenshots/README.md)

![Pipeline run](screenshots/terminal/11_full_pipeline_run_summary.png)
![Tests](screenshots/terminal/12_pytest_results.png)

## 🚀 Future Improvements
Real NASA GISTEMP / NOAA data · city-level forecasting · SARIMA / Prophet / LSTM · live weather API · geospatial map dashboard · climate risk scoring · pollution-climate analysis.

## 🎓 Learning Outcomes
Time-series decomposition, trend significance testing, z-score and Isolation Forest anomaly detection, forecast validation with a holdout, modular pipeline design, testing, and dashboarding.

## 👤 Author
**Saymah** - B.E. student, Vadodara, Gujarat, India
