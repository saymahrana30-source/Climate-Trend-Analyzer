"""Anomaly detection: z-score on deseasonalised, detrended residuals + Isolation Forest."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

from src import config


def _zscores(g: pd.DataFrame, col: str, log: bool = False) -> pd.Series:
    """Detrend, remove the seasonal cycle, then standardise within each calendar month.

    Rainfall is log-transformed first because it is right-skewed (a few huge values would
    otherwise inflate the standard deviation and trigger lots of false alarms).
    """
    vals = np.log1p(g[col].values) if log else g[col].values.astype(float)
    x = np.arange(len(g))
    detr = vals - np.polyval(np.polyfit(x, vals, 1), x)
    s = pd.Series(detr, index=g.index)
    months = g["month"]
    z = (s - s.groupby(months).transform("mean")) / s.groupby(months).transform("std")
    return z


def detect(df) -> pd.DataFrame:
    out = []
    for region, g in df.groupby("region"):
        g = g.sort_values("date").copy()
        g["temp_zscore"] = _zscores(g, "temperature_c").round(2)
        g["rain_zscore"] = _zscores(g, "rainfall_mm", log=True).round(2)
        feats = g[["temp_zscore", "rain_zscore"]].values
        iso = IsolationForest(contamination=0.01, random_state=config.SEED).fit(feats)
        g["iso_flag"] = (iso.predict(feats) == -1)
        g["is_anomaly"] = ((g["temp_zscore"].abs() > config.TEMP_Z_THRESHOLD)
                           | (g["rain_zscore"] > config.RAIN_Z_THRESHOLD)
                           | (g["rain_zscore"] < -config.DROUGHT_Z_THRESHOLD))
        out.append(g)
    return pd.concat(out, ignore_index=True)


def anomaly_table(scored: pd.DataFrame) -> pd.DataFrame:
    a = scored[scored["is_anomaly"]].copy()

    def label(r):
        if abs(r["temp_zscore"]) > config.TEMP_Z_THRESHOLD:
            return "Heatwave" if r["temp_zscore"] > 0 else "Cold snap"
        return "Extreme rainfall" if r["rain_zscore"] > 0 else "Drought month"
    a["event_type"] = a.apply(label, axis=1)
    cols = ["date", "region", "event_type", "temperature_c", "rainfall_mm", "temp_zscore", "rain_zscore"]
    a = a[cols].sort_values("date").reset_index(drop=True)
    config.TABLE_DIR.mkdir(parents=True, exist_ok=True)
    a.to_csv(config.TABLE_DIR / "anomaly_table.csv", index=False)
    return a


def evaluate(scored: pd.DataFrame) -> dict:
    """Because we injected known anomalies, we can measure precision / recall."""
    truth = scored["is_injected_anomaly"] == 1
    pred = scored["is_anomaly"]
    tp = int((truth & pred).sum())
    fp = int((~truth & pred).sum())
    fn = int((truth & ~pred).sum())
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    return {"true_positives": tp, "false_positives": fp, "false_negatives": fn,
            "precision": round(precision, 3), "recall": round(recall, 3)}


def plot_anomalies(scored, region="Gujarat-West India"):
    g = scored[scored["region"] == region]
    a = g[g["is_anomaly"]]
    fig, ax = plt.subplots(figsize=(13, 6))
    ax.plot(g["date"], g["temperature_c"], color="#8d99ae", linewidth=1, label="Monthly temperature")
    ax.scatter(a["date"], a["temperature_c"], color="#d1495b", s=60, zorder=3, label="Anomaly")
    ax.set(title=f"Detected Climate Anomalies - {region}", xlabel="Year", ylabel="Temperature (°C)")
    ax.legend()
    path = config.FIG_DIR / "11_anomaly_detection.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


def run(df):
    scored = detect(df)
    table = anomaly_table(scored)
    metrics = evaluate(scored)
    plot_anomalies(scored)
    return scored, table, metrics
