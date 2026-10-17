# Interview Guide

**30-second pitch:** "I built a Climate Trend Analyzer that cleans 50 years of simulated multi-region climate data, measures warming trends with significance tests, detects heatwaves and extreme rainfall with z-scores, and forecasts 10 years ahead. It reaches 84% precision and 88% recall on injected anomalies, and has a Streamlit dashboard plus automated tests."

**Likely questions**
1. *Why simulated data?* No institutional access; simulation lets me inject known anomalies and measure detection quality. The pipeline accepts real NASA/NOAA CSVs with the same columns.
2. *How did you find the trend?* Linear regression on annual means (°C/decade) plus Kendall tau as a non-parametric check.
3. *How do you detect anomalies?* Remove trend and seasonality, standardize per month, threshold the z-score; Isolation Forest as a second view.
4. *Why log-transform rainfall?* It is right-skewed; without it, false alarms spiked (precision fell to ~32%).
5. *Linear vs ARIMA?* Compared on a 10-year holdout; linear matched or beat ARIMA on this smooth synthetic data. Real data would need re-validation.
6. *Limitations?* Thresholds tuned on simulated data; annual forecasts only; no spatial modeling.

**Resume bullets**
- Built an end-to-end climate analytics pipeline (Python, pandas, statsmodels, scikit-learn) covering cleaning, trend testing, anomaly detection and ARIMA/linear forecasting on 50 years of multi-region data.
- Detected extreme-weather months with detrended, seasonally-adjusted z-scores (84% precision, 88% recall on injected events); validated forecasts on a 10-year holdout.
- Delivered a modular codebase with 6 pytest tests, 12 charts, an auto-generated insights report and a Streamlit dashboard.
