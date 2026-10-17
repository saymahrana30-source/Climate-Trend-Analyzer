"""Forecasting: Linear Regression vs ARIMA, validated on a 10-year holdout."""
import warnings

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from statsmodels.tsa.arima.model import ARIMA

from src import config

warnings.filterwarnings("ignore")


def _annual(df, region):
    s = df[df["region"] == region].groupby("year")["temperature_c"].mean()
    return s


def compare_models(df, region, holdout: int = 10) -> pd.DataFrame:
    s = _annual(df, region)
    train, test = s.iloc[:-holdout], s.iloc[-holdout:]

    lr = LinearRegression().fit(train.index.values.reshape(-1, 1), train.values)
    lr_pred = lr.predict(test.index.values.reshape(-1, 1))

    arima = ARIMA(train.values, order=(1, 1, 1), trend="t").fit()
    ar_pred = arima.forecast(holdout)

    rows = []
    for name, pred in [("Linear Regression", lr_pred), ("ARIMA(1,1,1)+drift", ar_pred)]:
        rows.append({"region": region, "model": name,
                     "MAE": round(mean_absolute_error(test, pred), 3),
                     "RMSE": round(float(np.sqrt(mean_squared_error(test, pred))), 3)})
    return pd.DataFrame(rows)


def forecast_future(df, region, years: int = config.FORECAST_YEARS) -> pd.DataFrame:
    s = _annual(df, region)
    future_years = np.arange(s.index.max() + 1, s.index.max() + 1 + years)
    lr = LinearRegression().fit(s.index.values.reshape(-1, 1), s.values)
    lin = lr.predict(future_years.reshape(-1, 1))
    res = ARIMA(s.values, order=(1, 1, 1), trend="t").fit()
    fc = res.get_forecast(years)
    ci = fc.conf_int(alpha=0.05)
    return pd.DataFrame({"region": region, "year": future_years,
                         "linear_forecast_c": lin.round(2),
                         "arima_forecast_c": fc.predicted_mean.round(2),
                         "arima_lower_95": ci[:, 0].round(2), "arima_upper_95": ci[:, 1].round(2)})


def plot_forecast(df, region):
    s = _annual(df, region)
    fc = forecast_future(df, region)
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(s.index, s.values, "o-", color="#2e86ab", label="Observed annual mean")
    ax.plot(fc["year"], fc["arima_forecast_c"], "--", color="#d1495b", linewidth=2, label="ARIMA forecast")
    ax.plot(fc["year"], fc["linear_forecast_c"], ":", color="#2a9d8f", linewidth=2, label="Linear forecast")
    ax.fill_between(fc["year"], fc["arima_lower_95"], fc["arima_upper_95"], color="#d1495b", alpha=0.15,
                    label="95% interval")
    ax.set(title=f"{config.FORECAST_YEARS}-Year Temperature Forecast - {region}",
           xlabel="Year", ylabel="Annual mean temperature (°C)")
    ax.legend()
    path = config.FIG_DIR / "12_forecast.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


def run(df, focus_region="Gujarat-West India"):
    metrics = pd.concat([compare_models(df, r) for r in df["region"].unique()], ignore_index=True)
    forecasts = pd.concat([forecast_future(df, r) for r in df["region"].unique()], ignore_index=True)
    plot_forecast(df, focus_region)
    config.TABLE_DIR.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(config.TABLE_DIR / "forecast_metrics.csv", index=False)
    forecasts.to_csv(config.TABLE_DIR / "forecast_table.csv", index=False)
    return metrics, forecasts
