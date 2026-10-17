# Climate Trend Analyzer - Insights Report
_Generated on 17 Oct 2026 from simulated data (1975-2024)_

## Key Findings
1. **4 of 4 regions show statistically significant warming.** Fastest: **Northern Europe** at **+0.35 °C/decade**.
2. **CO₂ and temperature are strongly correlated** (r = 0.93 on annual means).
3. **Sea level rose ~344 mm** over the period (simulated).
4. **25 anomalous months** flagged (precision 84%, recall 88% against injected events).
5. **Best forecaster:** Linear Regression (mean RMSE 0.307 °C on a 10-year holdout).

## Trend Table
| region             |   slope_c_per_decade |   r_squared |   p_value |   kendall_tau | trend   |
|:-------------------|---------------------:|------------:|----------:|--------------:|:--------|
| Northern Europe    |                0.346 |       0.756 |  2.68e-16 |         0.708 | Warming |
| Sahel Africa       |                0.338 |       0.705 |  2.6e-14  |         0.678 | Warming |
| Gujarat-West India |                0.252 |       0.58  |  1.33e-10 |         0.563 | Warming |
| Pacific Coast US   |                0.196 |       0.382 |  1.76e-06 |         0.442 | Warming |

## Forecast for 2034 (ARIMA)
| region             |   arima_forecast_c |   arima_lower_95 |   arima_upper_95 |
|:-------------------|-------------------:|-----------------:|-----------------:|
| Gujarat-West India |              28.5  |            27.89 |            29.11 |
| Northern Europe    |              10.05 |             9.48 |            10.61 |
| Pacific Coast US   |              15.32 |            14.6  |            16.03 |
| Sahel Africa       |              30.96 |            30.32 |            31.59 |

## Who Can Use This
- **Agritech:** shift crop calendars as seasonal rainfall patterns move.
- **Energy:** plan cooling demand using regional warming rates.
- **Urban planning:** use extreme-event frequency to size drainage and heat-action plans.

> Note: data is simulated for demonstration. Swap in NASA GISTEMP / NOAA CSVs with the same column names to analyse real records.