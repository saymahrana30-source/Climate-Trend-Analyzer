# Architecture

| Module | Input | Output |
|---|---|---|
| `data_generator.py` | seed, region settings | `data/raw/climate_raw.csv` (messy, 2,425 rows) |
| `preprocessing.py` | raw CSV | `data/processed/climate_clean.csv` (2,400 rows, 0 missing) + features |
| `eda.py` | clean data | 8 charts (`01`-`08`) |
| `trend_analysis.py` | clean data | regression + Kendall table, STL, charts `09`-`10` |
| `anomaly_detection.py` | clean data | z-scores, anomaly table, precision/recall, chart `11` |
| `forecasting.py` | clean data | holdout metrics, 10-year forecast, chart `12` |
| `report.py` | all results | `reports/insights_report.md` |

Flow: generate → clean → (EDA | trends | anomalies | forecast) → report/dashboard.

**Anomaly method:** detrend (linear) → remove monthly seasonal mean → standardize per calendar month → flag |z| > 3.0 (temperature), z > 2.5 (rain), z < -3.5 (drought). Rainfall is log-transformed because it is right-skewed. Isolation Forest flags are stored as a second opinion (`iso_flag`).
